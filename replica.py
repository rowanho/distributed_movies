import Pyro4
import csv
from uuid import uuid1
import threading
MOVIE_DIR = 'ml-latest-small'
#STATUS is either set to 'free','busy' or 'down'
#TODO - complete functions and classes!
#raise this error when we can't find a movie
class NullQueryException(Exception):
    pass
#remote functions to get the status of the server
@Pyro4.expose
class Replica(object):
    def __init__(self):
        self.status = 'free'
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
        movie_list = []
        with open(MOVIE_DIR +'/movies.csv') as movie_csv:
            reader = csv.reader(movie_csv,delimiter=',',quotechar= '|')
            for i,row in enumerate(reader):
                if i == 0:
                    continue
                if movie_string.lower() in row[1].lower():
                    movie_list.append((int(row[0]),row[1]))
        if len(movie_list) == 0:
            raise NullQueryException("No movies found")
        else:
            return movie_list

    #gets the rating of a movie by user_id and movie_id
    def get_user_rating(self,user_id,movie_id):
        rating = -1.0
        with open(MOVIE_DIR + '/ratings.csv') as rating_csv:
            reader - csv.reader(rating_csv,delimiter=',',quotechar='|')
            for i,row in enumerate(reader):
                if i == 0:
                    continue
                if int(row[1]) == movie_id and int(row[0])== movie_id:
                    rating = float(row[2])
        if rating == -1.0:
            raise NullQueryException('No ratings found')
        else:
            return rating

    #returns the rating of a movie by all users
    def get_overall_rating(self,movie_id):
        r_count,total_rating = 0,0
        print(movie_id)
        with open(MOVIE_DIR + '/ratings.csv') as rating_csv:
            reader = csv.reader(rating_csv, delimiter=',',quotechar ='|')
            for i,row in enumerate(reader):
                if i == 0:
                    continue
                #if movie_id matches, add the rating to our total
                if int(row[1]) == movie_id:
                    print(row[1])
                    r_count += 1
                    total_rating += float(row[2])
        if r_count == 0:
            raise NullQueryException('No ratings found')
        else:
            return total_rating/r_count


        return 0
#register all the classes here
def main():
    id_string = str(uuid1())
    daemon = Pyro4.Daemon()                # make a Pyro daemon
    ns = Pyro4.locateNS()                  # find the name server
    uri = daemon.register(Replica)   # register the greeting maker as a Pyro object
    ns.register(id_string + ".replica", uri)   # register the object with a name in the name server
    print("Server with id %s is ready." %(id_string))
    daemon.requestLoop()                   # start the event loop of the server to wait for calls

if __name__ == "__main__":
    main()
