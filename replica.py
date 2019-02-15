import Pyro4
from uuid import uuid1
import threading
import time
import random
from lib.csv_functions import get_all_movies,get_all_ratings
#simple vector clock object
from lib.vector_clock import vector_clock
#STATUS is either set to 'free','busy' or 'down'
#TODO - handle updates - check update log to see whether updates can actually be applied
#this can happen when our timestamp is geq the timestamp of the update
#we can then check the timestamps to see if we have recent enough data to respond properly

### Custom exceptions
class InvalidMovieIdException(Exception):
    pass

class InvalidRatingIdException(Exception):
    pass


#gets a list of all the other replicas registered on pyro
def get_all_replicas():
    server_ids = []
    ns = Pyro4.locateNS()
    for key in ns.list():
        if 'replica' in key:
            server_ids += key.split('.')[0]
    return server_ids


#picks some other replicas at random and sends gossip to them
#gossip_msg in format {replica_id:id, timestamp: vector_timestamp, updates:[list of updates]}
def send_gossip(limit,our_replica):
    server_ids = get_all_replicas()
    #pick random server_ids up until the limit
    random.shuffle(server_ids)
    if len(server_ids) < limit:
        limit = len(server_ids)
    for i in range(limit):
        replica = Pyro4.Proxy("PYRONAME:" + server_ids[i] +".replica")
        replica.gossip_recieve(our_replica.next_gossip_message)
    replica.next_gossip_message = {}


####remote functions to get the status of the server####
@Pyro4.expose
class Replica(object):


    def __init__(self,server_ids,id):
        self.status = 'free'
        self.movies = get_all_movies()
        self.ratings = get_all_ratings()
        #this timestamp is inced whenever we handle an update request
        self.replica_timestamp = vector_clock(server_ids,id)
        #this timestamp is inced whenever we actually add a stable update to the data
        self.value_timestamp = vector_clock(server_ids,id)
        self.update_log = []
        self.executed_operations = []
        self.timestamp_table = []
        #the updates recieved to send in the next gossip message
        next_gossip_message = {"timestamp":self.replica_timestamp,"gossip_data":[]}


    #gets the status of the server
    def get_status(self):
        return self.status

    ### gossip stuff ###

    #recieves gossip messages from another server
    def gossip_recieve(self,gossip_msg):
        pass

    #creates a new gossip message and sends it
    #gossip mesage contains replica timestamp and our update log
    def gossip(self):
        for u in self.update_log
    #checks the update log for updates that can be made stable
    def apply_updates(self):
        for u in self.update_log:
            if not u["stable"] and self.replica_timestamp.is_geq(u["timestamp"]):
                if u["type"] == "add_rating":
                    data = u["data"]
                    add_rating(data["user_id"],data["movie_id"])
                u["stable"] = True

    #handles the front end update request to add a rating
    #for now we don't concern ourselves with the users table and checking whether the movie exists
    def add_rating(self,prev_timestamp,user_id,movie_id):
        if movie_id in movies:
            update =  {"timestamp":self.replica_timestamp.vector,"stable":False,"type":"add_rating","data":{"user_id":user_id,"movie_id":movie_id}}
            self.update_log.append(update)
            self.replica_timestamp.increment()
            return {"timestamp":self.replica_timestamp.vector}
        else:
            raise InvalidMovieIdException('Cannot find movie with that id')


    #applys the update to add a new rating or updates an existing rating
    def apply_add_rating(self, user_id,movie_id):
        if movie_id in movies:
            self.ratings[user_id,movie_id] = rating
            self.executed_operations.append(update)
            self.value_timestamp.increment()



    #gets the rating of a movie by user_id and movie_id
    def get_user_rating(self,prev_timestamp,user_id,movie_id):
        #request can be blocking, we should wait until we have updated out timestamp sufficiently
        while not self.value_timestamp.is_geq(prev_timestamp):
            time.sleep(1.0)
        if (user_id,movie_id) in self.ratings:
            return {"timestamp" : self.replica_timestamp.vector, "rating": self.ratings[user_id,movie_id]}
        else:
            raise InvalidRatingIdException('Cannot find rating with that user/movie id')


    #returns the rating of a movie by all users
    def get_all_ratings(self,prev_timestamp,movie_id):
        while not self.value_timestamp.is_geq(prev_timestamp):
            time.sleep(1.0)
        ratings = []
        #slow - might be faster if we restructured the data
        for key in self.ratings:
            if key[1] == movie_id:
                ratings.append(self.ratings[key])
        return {"timestamp": self.replica_timestamp.vector, "ratings" : ratings}



#register all the classes here
def main():
    server_ids = get_all_replicas()  # get the ids of all the other remote servers
    id_string = str(uuid1())
    server_ids.append(id_string)
    daemon = Pyro4.Daemon()                # make a Pyro daemon
    ns = Pyro4.locateNS()                   # find the name server
    r = Replica(server_ids,id_string)
    uri = daemon.register(r)   # register the object not the class
    ns.register(id_string + ".replica", uri)   # register the object with a name in the name server
    print("Server with id %s is ready." %(id_string))
    #threading.Timer(1.0,send_gossip,args=(r)).start() #gossip messages
    daemon.requestLoop()                   # start the event loop of the server to wait for calls

if __name__ == "__main__":
    main()
