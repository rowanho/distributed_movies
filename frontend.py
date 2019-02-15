# saved as greeting-server.py
import Pyro4
import threading
from lib.vector_clock import vector_clock
class NoFreeServerException(Exception):
    pass
@Pyro4.expose
class FrontEnd(object):
    def __init__(self):
        #prev keeps track of the timestamp of the most recent data the client has accessed
        self.prev_timestamp = vector_clock([])


    def add_rating(self,user_id,movie_id):
        replica_id = get_free_server()
        if replica_id != -1:
            #get a replica
            replica = Pyro4.Proxy("PYRONAME:" + replica_id + ".replica")
            res = replica.add_rating(user_id,movie_id)
            self.prev_timestamp.updateToMax(res["timestamp"])
        else:
            raise NoFreeServerException("Couldn't find a free server")


    def get_user_rating(self,user_id,movie_id):
        replica_id = get_free_server()
        if replica_id != -1:
            replica = Pyro4.Proxy("PYRONAME:" + replica_id + ".replica")
            timestamp = self.prev_timestamp.vector
            res = replica.get_user_rating(timestamp,user_id,movie_id)
            self.prev_timestamp.updateToMax(res["timestamp"])
            return res["rating"]
        else:
            raise NoFreeServerException("Couldn't find a free server")

    def get_all_ratings(self,movie_id):
        replica_id = get_free_server()
        if replica_id != -1:
            replica = Pyro4.Proxy("PYRONAME:" + replica_id + ".replica")
            timestamp = self.prev_timestamp.vector
            res = replica.get_all_ratings(timestamp,movie_id)
            self.prev_timestamp.updateToMax(res["timestamp"])
            return res["ratings"]
        else:
            raise NoFreeServerException("Couldn't find a free server")

#iterates through servers on the name system and returns the uuid of the one that is free
#if it can't find one, returns -1
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
