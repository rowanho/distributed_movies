# saved as greeting-client.py
import Pyro4
from lib.custom_exceptions import *

#returns a float divisble by 0.5 - the rating of a movie
def add_movie_rating(frontend):
    valid = False
    while not valid:
        input_movie = input("Enter movie id: ")
        input_user = input("Enter user id: ")
        try:
            movie_id = int(input_movie)
            user_id = int(input_user)
        except:
            print("Please enter a valid integer for movie id/user id")
            continue
        input_movie_rating = input("Enter your rating: ")
        try:
            movie_rating = float(input_movie_rating)
            if movie_rating >= 0.5 and movie_rating <= 5.0:
                if (movie_rating *  2).is_integer():
                    valid = True
        except:
            print("Please enter a valid rating (multiple of 0.5 between 0.5 and 5)")
        if not valid:
            print("Please enter a valid rating (multiple of 0.5 between 0.5 and 5)")
    print("Adding rating..")

    return frontend.add_rating(user_id,movie_id,movie_rating)

def get_all_ratings(frontend):
    valid = False
    while not valid:
        try:
            movie_id = int(input("Enter movie id: "))
            valid = True
        except:
            print("Error, please enter a valid integer.")
    print("Getting ratings..")

    return frontend.get_all_ratings(movie_id)

def get_user_rating(frontend):
    valid = False
    while not valid:
        input_movie = input("Enter movie id: ")
        input_user = input("Enter user id: ")
        try:
            movie_id = int(input_movie)
            user_id = int(input_user)
            valid = True
        except:
            print("Please enter a valid integer for movie id/user id")
            continue
    print("Getting rating..")
    # actually call the remote functions here

    return frontend.get_user_rating(user_id,movie_id)

#ratings
def make_ratings_dict():
    d = {}
    for i in range(11):
        d[i * 0.5] = 0
    return d
#takes in array of ratings and returns a string that shows a nicer representation
def display_ratings_list(ratings_list):
    output = "Total ratings: " + str(len(ratings_list)) + "\n"
    ratings_dict = make_ratings_dict()
    for r in ratings_list:
        ratings_dict[r] += 1
    for key, val in ratings_dict.items():
        output += str(key) +" : " + str(val) + "\n"
    return output
def main():
    exit = False
    frontend = Pyro4.Proxy("PYRONAME:frontend")
    phrase = "Enter 1 to get all ratings for a movie, 2 to get a rating for a specific movie/user,\
 3 to add a new rating, or q to quit:"
    while not exit:
        i = input(phrase)
        if i == '1':
            ratings = get_all_ratings(frontend)
            print(display_ratings_list(ratings))
        elif i == '2':
            res = get_user_rating(frontend)
            print(res)
        elif i == '3':
            res = add_movie_rating(frontend)
            print(res)
        elif i == 'q':
            print('Exiting..')
            exit = True
        else:
            print("Please enter a valid input (1,2 or q).")
if __name__ == "__main__":
    main()
