# saved as greeting-server.py
import Pyro4
import threading
from uuid import uuid1
from contextlib import contextmanager
from lib.vector_clock import vector_clock
import lib.custom_exceptions


#custom context manager for opening replica pyro connection and handling status automatically
@contextmanager
def openReplica(key):
    replica = Pyro4.Proxy("PYRONAME:" + key)
    try:
        replica.set_status('over-loaded')
        yield replica
    finally:
        replica.set_status('available')
        replica._pyroRelease()


@Pyro4.expose
class FrontEnd(object):
    def __init__(self):
        #prev keeps track of the timestamp of the most recent data the client has accessed
        self.prev_timestamp = vector_clock([])


    def add_rating(self,user_id,movie_id,rating):
        key = get_free_server()
        if key != -1:
            with openReplica(key) as replica:
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
            with openReplica(key) as replica:
                timestamp = self.prev_timestamp.vector
                res = replica.get_user_rating(timestamp,user_id,movie_id)
                self.prev_timestamp.updateToMax(res["timestamp"])
                return res["rating"]
        else:
            raise NoFreeServerException("Couldn't find a free server")

    def get_all_ratings(self,movie_id):
        key = get_free_server()
        if key != -1:
            with openReplica(key) as replica:
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
                    if replica.get_status() == 'active' and replica.is_online():
                        print("Front end found available server: " + key)
                        is_free = True
                except:
                    continue
                if is_free:
                    return key
            print(replica)
    return -1 # if no free server found

#register on pyro here
def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(FrontEnd)
    ns.register("frontend", uri)
    print("Ready.")
    daemon.requestLoop()
if __name__ == "__main__":
    main()
