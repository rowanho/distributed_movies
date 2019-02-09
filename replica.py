import Pyro4
import csv

#TODO - complete functions and classes!
@Pyro4.expose
class Movie_Updates(object):
    def register_user(self):
        return 0
    #updates the movie rating based on a new rating
    def update_rating(self, user_id,movie_id,rating):
        return 0
@Pyro4.expose
class Movie_Queries(object):
    #returns a list of tuples containing movie_ids and full names based on movie name input
    def get_movies(self,movie_string):
        return [(0,'')]
    #gets the rating of a movie by user_id and movie_id
    def get_user_rating(self,user_id,movie_id):
        return 0
    #returns the rating of a movie by all users
    def get_overall_rating(self,movie_id):
        return 0
#register all the classes here
def main():
    daemon = Pyro4.Daemon()                # make a Pyro daemon
    ns = Pyro4.locateNS()                  # find the name server
    uri = daemon.register(Movie_Updates)   # register the greeting maker as a Pyro object
    ns.register("replica.movie.updates", uri)   # register the object with a name in the name server
    uri2 = daemon.register(Movie_Queries)
    ns.register("replica.movie.queries",uri2)
    print("Ready.")
    daemon.requestLoop()                   # start the event loop of the server to wait for calls

if __name__ == "__main__":
    main()
