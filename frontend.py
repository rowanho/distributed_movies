# saved as greeting-server.py
import Pyro4
import threading

class NoFreeServerException(Exception):
    pass
@Pyro4.expose
class FrontEnd(object):
    def register_user(self):
        #get a replica implementation of the function
        replica_id = get_free_server()
        if replica_id != 0:
            replica = Pyro4.Proxy("PYRONAME:" + replica_id +".replica")
            return replica.register_user()
        else:
            raise NoFreeServerException("Couldn't find a free server")
    def add_rating(self,movie_name,user_id):
        replica_id = get_free_server()
        if replica_id != 0:
            #get a replica implementation of the function
            replica = Pyro4.Proxy("PYRONAME:replica")
            return movie_updates.add_rating()
        else:
            raise NoFreeServerException("Couldn't find a free server")

    def get_overall_rating(self,movie_name):
        replica_id = get_free_server()
        if replica_id != 0:
            replica = Pyro4.Proxy("PYRONAME:" + replica_id +".replica")
            #list of tuples containing (movie_id,movie_name)
            possible_movies = replica.get_movies(movie_name)
            print(possible_movies[0][0])
            rating = replica.get_overall_rating(possible_movies[0][0])
            return possible_movies[0][1],rating
        else:
            raise NoFreeServerException("Couldn't find a free server")

#input - the Pyro4 ns object
#iterates through servers on the name system and returns the uuid of the one that is free
#if it can't find one, returns 0
def get_free_server():
    ns = Pyro4.locateNS()
    for key in ns.list():
        if 'replica' in key:
            replica_status = Pyro4.Proxy("PYRONAME:" + key)
            is_free = False
            try:
                status = replica_status.get_status()
                print(status)
                if status == 'free':
                    is_free = True
            except:
                continue
            if is_free:
                return key.split('.')[0]
    return 0


#register all the classes here
def main():
    daemon = Pyro4.Daemon()                # make a Pyro daemon
    ns = Pyro4.locateNS()                  # find the name server
    uri = daemon.register(FrontEnd)   # register the greeting maker as a Pyro object
    ns.register("frontend", uri)   # register the object with a name in the name server
    print("Ready.")
    def my_loop():
        threading.Timer(3.0, my_loop).start()
        print("First free server found: ",get_free_server())
    my_loop()
    daemon.requestLoop()                   # start the event loop of the server to wait for calls
if __name__ == "__main__":
    main()
