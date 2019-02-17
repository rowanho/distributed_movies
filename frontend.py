# saved as greeting-server.py
import Pyro4
import threading
from uuid import uuid1
from lib.vector_clock import vector_clock
class NoFreeServerException(Exception):
    pass
    ### Custom exceptions
class InvalidMovieIdException(Exception):
    pass

class InvalidRatingIdException(Exception):
    pass

@Pyro4.expose
class FrontEnd(object):
    def __init__(self):
        #prev keeps track of the timestamp of the most recent data the client has accessed
        self.prev_timestamp = vector_clock([])


    def add_rating(self,user_id,movie_id,rating):
        key = get_free_server()
        if key != -1:
            with Pyro4.Proxy("PYRONAME:" + key) as replica:
                operation_id = str(uuid1())
                try:
                    timestamp = self.prev_timestamp.vector
                    res = replica.add_rating(operation_id,timestamp,user_id,movie_id,rating)
                    self.prev_timestamp.updateToMax(res["timestamp"])
                    return "Successfully added rating!"
                except InvalidMovieIdException:
                    return "Could not find movie with that id!"
        else:
            raise NoFreeServerException("Couldn't find a free server")


    def get_user_rating(self,user_id,movie_id):
        key = get_free_server()
        if key != -1:
            with Pyro4.Proxy("PYRONAME:" + key) as replica:
                timestamp = self.prev_timestamp.vector
                res = replica.get_user_rating(timestamp,user_id,movie_id)
                self.prev_timestamp.updateToMax(res["timestamp"])
                return res["rating"]
        else:
            raise NoFreeServerException("Couldn't find a free server")

    def get_all_ratings(self,movie_id):
        key = get_free_server()
        if key != -1:
            with Pyro4.Proxy("PYRONAME:" + key) as replica:
                timestamp = self.prev_timestamp.vector
                res = replica.get_all_ratings(timestamp,movie_id)
                self.prev_timestamp.updateToMax(res["timestamp"])
                return res["ratings"]
        else:
            raise NoFreeServerException("Couldn't find a free server")

#iterates through servers on the name system and returns the first one that is free
#if it can't find one, returns -1
def get_free_server():
    ns = Pyro4.locateNS()
    for key in ns.list():
        if 'replica' in key:
            with Pyro4.Proxy("PYRONAME:" + key) as replica:
                is_free = False
                try:
                    print(key)
                    print(replica)
                    print('getting status')
                    if replica.get_status() == 'free':
                        print('free')
                        is_free = True
                except:
                    continue
                if is_free:
                    return key
            print(replica)
    return -1 # if no free server found

#register all the classes here
def main():
    daemon = Pyro4.Daemon()                # make a Pyro daemon
    ns = Pyro4.locateNS()
    uri = daemon.register(FrontEnd)   # register the Pyro object
    ns.register("frontend", uri)   # register the object with a name in the name server
    print("Ready.")
    #def my_loop():
    #    threading.Timer(3.0, my_loop).start()
    #    print("First free server found: ",get_free_server())
    #my_loop()
    daemon.requestLoop()                   # start the event loop of the server to wait for calls
if __name__ == "__main__":
    main()
