import Pyro4
from uuid import uuid1
import threading
import random
from lib.csv_functions import get_all_movies,get_all_ratings
#simple vector clock object
from lib.vector_clock import vector_clock
#STATUS is either set to 'free','busy' or 'down'
#TODO - complete functions and classes!

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
def send_gossip(limit,gossip_msg):
    server_ids = get_all_replicas()
    #pick random server_ids up until the limit
    random.shuffle(server_ids)
    if len(server_ids) < limit:
        limit = len(server_ids)
    for i in range(limit):
        replica = Pyro4.Proxy("PYRONAME:" + server_ids[i] +".replica")
        replica.gossip(gossip_msg)


####remote functions to get the status of the server####
@Pyro4.expose
class Replica(object):
    def __init__(self,server_ids,id):
        self.status = 'free'
        self.movies = get_all_movies()
        self.ratings = get_all_ratings()
        self.vector_clock = vector_clock(server_ids,id)
        self.update_log = []
        self.executed_operations = []
        self.vclock_table = []
    #gets the status of the server
    def get_status(self):
        return self.status
    #recieves gossip messages from another server
    def gossip(self,gossip_msg):
        pass
    #adds a new rating or updates an existing rating
    def update_add_rating(self, user_id,movie_id,rating):
        if movie_id in movies:
            ratings[user_id,movie_id] = rating
            self.vector_clock.increment()
        else:
            raise InvalidMovieIdException('Cannot find movie with that id')
    #gets the rating of a movie by user_id and movie_id
    def get_user_rating(self,user_id,movie_id):
        if (user_id,movie_id) in ratings:
            return ratings[user_id,movie_id]
        else:
            raise InvalidRatingIdException('Cannot find rating with that user/movie id')
    #returns the rating of a movie by all users
    def get_overall_rating(self,movie_id):
        total = 0.0
        count = 0
        #slow - might be faster if we restructured the data
        for key in ratings:
            if key[1] == movie_id:
                total += ratings[key]
                count += 1
        if count > 0:
            return total/count
        else:
            return -1
#register all the classes here
def main():
    server_ids = get_all_replicas()  # get the ids of all the other remote servers
    id_string = str(uuid1())
    server_ids.append(id_string)
    daemon = Pyro4.Daemon()                # make a Pyro daemon
    ns = Pyro4.locateNS()                   # find the name server
    r = Replica()
    uri = daemon.register(r)   # register the object not the class
    ns.register(id_string + ".replica", uri)   # register the object with a name in the name server
    print("Server with id %s is ready." %(id_string))
    daemon.requestLoop()                   # start the event loop of the server to wait for calls

if __name__ == "__main__":
    main()
