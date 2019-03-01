# saved as greeting-server.py
import Pyro4
import threading
from uuid import uuid1
from contextlib import contextmanager
from common_functions.vector_clock import vector_clock
import random
import time

#custom context manager for opening replica pyro connection and handling status automatically
@contextmanager
def openReplica(key):
    replica = Pyro4.Proxy("PYRONAME:" + key)
    try:
        replica.set_status('over-loaded')
        yield replica
    finally:
        replica.set_status('active')
        replica._pyroRelease()


@Pyro4.expose
class FrontEnd(object):
    def __init__(self):
        #prev keeps track of the timestamp of the most recent data the client has accessed
        self.prev_timestamp = vector_clock([])


    def add_rating(self,user_id,movie_id,rating):
        done = False
        while not done:
            key = get_free_server()
            if key != -1:
                with openReplica(key) as replica:
                    operation_id = str(uuid1())
                    try:
                        timestamp = self.prev_timestamp.vector
                        res = replica.add_rating(operation_id,timestamp,time.time(),user_id,movie_id,rating)
                        self.prev_timestamp.updateToMax(res["timestamp"])
                        done = True
                        return "Successfully added rating!"
                    except Exception as e:
                        #Raised if movie id not valid
                        if str(e) == "InvalidMovieIdException":
                            done = True
                            return "Movie not in the database"
                        #Raised if server crashes during our interactions
                        elif str(e) == "ServerCrashedException":
                            #try again and get another server
                            continue


    def get_user_rating(self,user_id,movie_id):
        done = False
        while not done:
            key = get_free_server()
            if key != -1:
                with openReplica(key) as replica:
                    try:
                        timestamp = self.prev_timestamp.vector
                        res = replica.get_user_rating(timestamp,user_id,movie_id)
                        self.prev_timestamp.updateToMax(res["timestamp"])
                        return res["movie_name"],res["rating"]
                    except Exception as e:
                        if str(e) == "InvalidRatingIdException":
                            done = True
                            raise Exception("InvalidRatingIdException")
                        elif str(e) == "ServerCrashedException":
                            #try again and get another server
                            continue
                        elif str(e) == "NotUpToDateException": # exception raised because server not up to date
                            continue


    def get_all_ratings(self,movie_id):
        done = False
        while not done:
            key = get_free_server()
            if key != -1:
                with openReplica(key) as replica:
                    timestamp = self.prev_timestamp.vector
                    try:
                        res = replica.get_all_ratings(timestamp,movie_id)
                        self.prev_timestamp.updateToMax(res["timestamp"])
                        done = True
                        return res["movie_name"],res["ratings"]
                    except Exception as e:
                        if str(e) == "InvalidMovieIdException":
                            done = True
                            raise Exception("InvalidMovieIdException")
                        elif str(e) == "ServerCrashedException":
                            #try again and get another server
                            continue
                        elif str(e) == "NotUpToDateException": # exception raised because server not up to date
                            continue


#iterates through servers on the name system and returns the first one that is free
#if it can't find one, returns -1
def get_free_server():
    ns = Pyro4.locateNS()
    keys = list(ns.list().keys())
    random.shuffle(keys)
    for key in keys:
        if 'replica' in key:
            with Pyro4.Proxy("PYRONAME:" + key) as replica:
                is_free = False
                try:
                    if replica.get_status() == 'active' and replica.is_online():
                        is_free = True
                except:
                    continue
                if is_free:
                    return key
    return -1 # if no free server found

#register on pyro here
def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(FrontEnd)
    ns.register("frontend", uri)
    print("Front end server ready: ")
    daemon.requestLoop()
if __name__ == "__main__":
    main()
