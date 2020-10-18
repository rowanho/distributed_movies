import Pyro4
from uuid import uuid4
import threading
import time
import random
import sys
from common_functions.csv_functions import get_all_movies,get_all_ratings
from common_functions.vector_clock import vector_clock

# self.status is either set to 'active', 'over-loaded' or 'offline'
# this can happen when our timestamp is geq the timestamp of the update
# we can then check the timestamps to see if we have recent enough data to respond properly



# Gets a list of all the other replicas registered on pyro
def get_all_replicas(our_id):
    server_ids = []
    ns = Pyro4.locateNS()
    for key in ns.list():
        if 'replica' in key and our_id not in key:
            server_ids.append(key.split('.')[0])
    return server_ids


# Picks some other replicas at random and sends gossip to them
# gossip_msg in format {replica_id:id, timestamp: vector_timestamp, updates:[list of updates]}
def send_gossip(limit,message):
    server_ids = get_all_replicas(message["id"])
    # Pick random server_ids up until the limit
    random.shuffle(server_ids)
    if len(server_ids) < limit:
        limit = len(server_ids)
    count = 0
    for id in server_ids:
        with Pyro4.Proxy("PYRONAME:" + id +".replica") as replica:
            if replica.get_status()== "active" and replica.is_online():
                replica.gossip_recieve(message)
                count += 1
            if count >= limit:
                break

# Takes in an update and timestamp table and returns True iff we can remove it
def can_remove_update(update,timestamp_table):
    for server,vector_timestamp in timestamp_table:
        # If we don't know whether all the servers are caught up with the update, we can't remove it from the log
        if not timestamp_table.is_geq(update["timestamp"]):
            return False
    return True


#### Remote replica object ####
@Pyro4.expose
class Replica(object):
    def __init__(self,server_ids,id,number_of_servers):
        self.online = True
        self.status = 'active'
        self.id = id
        self.number_of_servers = number_of_servers
        self.movies = get_all_movies()
        self.ratings = get_all_ratings()
       # Needed to handle concurrent updates
        self.date_times = {}
        # Start by initialising all to 0
        for key in self.ratings:
            self.date_times[key] = 0
        # This timestamp is incremented whenever we handle an update request
        self.replica_timestamp = vector_clock(server_ids,id)
        # This timestamp is incremented whenever we actually add a stable update to the data
        self.value_timestamp = vector_clock(server_ids,id)
        self.update_log = {}
        self.executed_operations = []
        self.timestamp_table = {}
        self.crash_probability = 0.3
        self.restore_probability = 0.5
        self.gossip_interval = 1.0
        self.crash_interval = 1.0
        thread = threading.Thread(target=self.run_gossip, args=()) # Separate thread for gossip
        thread.daemon = True
        thread.start()
        thread2 = threading.Thread(target=self.simulate_crash, args=()) # Separate thread for simulating crash
        thread2.daemon = True
        thread2.start()


    # Gets the status of the server
    def get_status(self):
        return self.status

    def set_status(self,status):
        self.status = status

    def is_online(self):
        return self.online

    # Recieves gossip messages from another server
    def gossip_recieve(self,gossip_msg):
        # Update the timestamp in the timestamp table
        if gossip_msg["id"] not in self.timestamp_table:
            self.timestamp_table["id"] = vector_clock([])
        self.timestamp_table["id"].updateToMax(gossip_msg["timestamp"])

        # Add any updates we don't already have to the update log
        for operation_id in gossip_msg["updates"]:
            update = gossip_msg["updates"][operation_id]
            # Update may be stable in other replica but not yet stable in ours
            update["stable"] = False
            if operation_id not in self.update_log:
                self.update_log[operation_id] = update
        # Update out own replica timestamp to reflect the updates we have now recieved
        self.replica_timestamp.updateToMax(gossip_msg["timestamp"])


    # Creates a new gossip message and sends it
    # Gossip mesage contains replica timestamp and our update log
    def gossip(self):
        #ensure we copy data, otherwise dict size may change during serialisation
        send_gossip(2,{"id":self.id,"timestamp":self.replica_timestamp.vector,"updates":self.update_log})


    # Gossips and checks for updates to make stable at fixed intervals
    def run_gossip(self):
        while True:
            lock = threading.Lock()
            with lock:
                if self.online:
                    self.gossip()
                    self.apply_updates()
            time.sleep(self.gossip_interval)

    # Simulates the chance of a server going down
    # Every interval there is the probability that the server crashes
    # If server is offline, it has a probability of coming back
    def simulate_crash(self):
        while True:
            if self.online:
                if random.random() < self.crash_probability:
                    self.online = False
            else:
                if random.random() < self.restore_probability:
                    self.online = True
            time.sleep(self.crash_interval)


    # Checks the update log for updates that can be made stable
    def apply_updates(self):
        # Stabilises updates where it is possible to do so
        for operation_id,u in self.update_log.items():
            if not u["stable"] and self.replica_timestamp.is_geq(u["vector_timestamp"]):
                if u["type"] == "add_rating":
                    data = u["data"]
                    if operation_id not in self.executed_operations:
                        self.apply_add_rating(u["vector_timestamp"],u["date_time"],data["user_id"],data["movie_id"],data["rating"])
                        self.executed_operations.append(operation_id)
                u["stable"] = True

        # Checks the timestamp table to see if we can remove some updates
        # However, we need to know the number of servers to do this
        if len(self.timestamp_table) == self.number_of_servers:
            for id,u in self.update_log.items():
                # Check if we can remove it
                if u["stable"] and can_remove_update(u,self.timestamp_table):
                    del self.update_log[id]


    # Handles the front end update request to add a rating
    # For now we don't concern ourselves with the users table and checking whether the movie exists
    def add_rating(self,operation_id,prev_timestamp,date_time,user_id,movie_id,rating):
        if not self.online:
            raise Exception("ServerCrashedException")
        if movie_id in self.movies:
            update =  {"vector_timestamp":self.replica_timestamp.vector,
            "date_time":date_time,
            "stable":False,"type":"add_rating",
            "data":{"user_id":user_id,
            "movie_id":movie_id,
            "rating":rating}}
            self.update_log[operation_id] = update
            self.replica_timestamp.increment()
            return {"timestamp":self.replica_timestamp.vector}
        else:
            raise Exception('InvalidMovieIdException')


    # Applys the update to add a new rating or updates an existing rating
    def apply_add_rating(self, vector_timestamp,date_time,user_id,movie_id,rating):
        # Concurrency check - if we already have a later update for the same ids,
        # then we shouldn't apply the older update
        if (user_id,movie_id) in self.ratings:
            if self.date_times[user_id,movie_id] < date_time:
                self.date_times[user_id,movie_id] = date_time
                self.ratings[user_id,movie_id] = rating
                self.value_timestamp.updateToMax(vector_timestamp)
        else:
            self.date_times[user_id,movie_id] = date_time
            self.ratings[user_id,movie_id] = rating
            self.value_timestamp.updateToMax(vector_timestamp)

    # Gets the rating of a movie by user_id and movie_id
    def get_user_rating(self,prev_timestamp,user_id,movie_id):
        if not self.online:
            raise Exception("ServerCrashedException")
        # Request can be blocking, we should wait until we have updated out timestamp sufficiently
        if not self.value_timestamp.is_geq(prev_timestamp):
            raise Exception("NotUpToDateException")
        if (user_id,movie_id) in self.ratings:
            movie_name = self.movies[movie_id]
            return {"timestamp" : self.replica_timestamp.vector, "rating": self.ratings[user_id,movie_id],"movie_id":movie_id,"movie_name":movie_name}
        else:
            raise Exception("InvalidRatingIdException")


    # Returns the rating of a movie by all users
    def get_all_ratings(self,prev_timestamp,movie_id):
        if not self.online:
            raise Exception("ServerCrashedException")
        if not self.value_timestamp.is_geq(prev_timestamp):
            raise Exception("NotUpToDateException")
        ratings = []
        # Slow - might be faster if we restructured the data
        movie_exists = False
        for key in self.ratings:
            if key[1] == movie_id:
                movie_exists = True
                ratings.append(self.ratings[key])
        if movie_exists:
            movie_name = self.movies[movie_id]
            return {"timestamp": self.replica_timestamp.vector, "ratings" : ratings,"movie_id":movie_id,"movie_name":movie_name}
        else: # When the movie id isn't valid
            raise Exception("InvalidMovieIdException")



# Register object here
def main():
    try:
        number_of_servers = int(sys.argv[1]) # We need to know this to know if an update has reached all servers
    except:
        number_of_servers = 100000   # Default to 'infinite' servers - ie we never remove updates as we don't know when all servers are reached
    id_string = str(uuid4())
    server_ids = get_all_replicas(id_string)  # Get the ids of all the other remote servers
    server_ids.append(id_string)
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    r = Replica(server_ids,id_string,number_of_servers)
    uri = daemon.register(r)   # Register the object not the class
    ns.register(id_string + ".replica", uri)   # Register the object with a name in the name server
    print("Replica with id %s ready: " % (id_string))

    daemon.requestLoop()                   # Start the event loop of the server to wait for calls

if __name__ == "__main__":
    main()
