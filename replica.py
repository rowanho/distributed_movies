import Pyro4
from uuid import uuid1
import threading
from lib.csv_functions import get_all_movies,get_all_ratings
#simple vector clock object
from lib.vector_clock import vector_clock
#STATUS is either set to 'free','busy' or 'down'
#TODO - complete functions and classes!
def get_all_replicas():
    server_ids = []
    ns = Pyro4.locateNS()
    for key in ns.list():
        if 'replica' in key:
            server_ids += key.split('.')[0]
    return server_ids

####remote functions to get the status of the server####
@Pyro4.expose
class Replica(object):
    def __init__(self,server_ids,id):
        self.status = 'free'
        self.movies = get_all_movies()
        self.ratings = get_all_ratings()
        self.vector_clock = vector_clock(server_ids,id)
    #gets the status of the server
    def get_status(self):
        return self.status
    def recieve_gossip(self,gossip):
        pass
    def register_user(self):
        return 0
    #updates the movie rating based on a new rating
    def update_rating(self, user_id,movie_id,rating):
        return 0
    #returns a list of tuples containing movie_ids and full names based on movie name input
    def get_movies(self,movie_string):
        return csv.csv_get_movies(movie_string)

    #gets the rating of a movie by user_id and movie_id
    def get_user_rating(self,user_id,movie_id):
        return csv.csv_get_user_rating(user_id,movie_id)
    #returns the rating of a movie by all users
    def get_overall_rating(self,movie_id):
        return csv.csv_get_overall_rating(user_id,movie_id)
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
