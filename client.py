# saved as greeting-client.py
import Pyro4
import lib.custom_exceptions

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
    print("Getting rating..")
    return frontend.add_rating(user_id,movie_id,movie_rating)

def get_all_ratings(frontend):
    valid = False
    while not valid:
        try:
            movie_id = int(input("Enter movie id: "))
            valid = True
        except:
            print("Error, please enter a valid integer.")
    print("getting ratings..")
    return frontend.get_all_ratings(movie_id)

def get_user_rating(frontend):
    user_id = int(input("Enter user id: "))
    movie_id = int(input("Enter movie id: "))
    # actually call the remote functions here
    return frontend.get_user_rating(user_id,movie_id)


def main():
    frontend = Pyro4.Proxy("PYRONAME:frontend")    # use name server object lookup uri shortcut
    exit = False
    while not exit:
        i = input("Enter 1 to get ratings for a movie, 2 to add a new rating, or q to quit: ")
        if i == '1':
            ratings = get_all_ratings(frontend)
            print(ratings)
        elif i == '2':
            res = add_movie_rating(frontend)
            print(res)
        elif i == 'q':
            print('Exiting..')
            exit = True
        else:
            print("Please enter a valid input (1,2 or q).")
if __name__ == "__main__":
    main()
