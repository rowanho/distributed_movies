# saved as greeting-server.py
import Pyro4
@Pyro4.expose
class Movie_Updates(object):
    def register_user(self):
        #get a replica implementation of the function
        movie_updates = Pyro4.Proxy("PYRONAME:replica.movie.updates")
        return movie_updates.register_user()
    def add_rating(self,movie_name,user_id):
        #get a replica implementation of the function
        movie_updates = Pyro4.Proxy("PYRONAME:replica.movie.updates")
        return movie_updates.add_rating()
@Pyro4.expose
class Movie_Queries(object):
    def get_overall_rating(self,movie_name):
        movie_queries = Pyro4.Proxy("PYRONAME:replica.movie.queries")
        #list of tuples containing (movie_id,movie_name)
        possible_movies = movie_queries.get_movies(movie_name)
        rating = movie_queries.get_overall_rating(possible_movies[0][0])
        return rating

#register all the classes here
def main():
    daemon = Pyro4.Daemon()                # make a Pyro daemon
    ns = Pyro4.locateNS()                  # find the name server
    uri = daemon.register(Movie_Updates)   # register the greeting maker as a Pyro object
    ns.register("frontend.movie.updates", uri)   # register the object with a name in the name server
    uri2 = daemon.register(Movie_Queries)
    ns.register("frontend.movie.queries",uri2)
    print("Ready.")
    daemon.requestLoop()                   # start the event loop of the server to wait for calls
if __name__ == "__main__":
    main()
