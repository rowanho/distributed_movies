# saved as greeting-client.py
import Pyro4
#returns a float divisble by 0.5 - the rating of a movie
def ask_update_movie_rating():
    valid = False
    while not valid:
        input_movie_rating = input("Enter your rating: ")
        try:
            movie_rating = float(input_movie_rating)
            if movie_rating >= 0.5 and movie_rating <= 5.0:
                if (movie_rating *  2).is_integer():
                    valid = True
        except:
            print("Please enter a valid rating")
        if not valid:
            print("Please enter a valid rating")
    return movie_rating

def add_movie_rating(frontend):
    movie_name = input("Enter the name of the movie to update")
    movie_rating = ask_update_movie_rating()
    print("Adding rating %f for movie name %s..."%(movie_rating,movie_name))
    # actually call the remote functions here


def get_movie_rating(frontend):
    user_id = int(input("Enter user id: "))
    movie_id = int(input("Enter movie_id: "))
    # actually call the remote functions here
    return frontend.get_user_rating(user_id,movie_id)


def main():
    frontend = Pyro4.Proxy("PYRONAME:frontend")    # use name server object lookup uri shortcut
    rating = get_movie_rating(frontend)
    print("Rating: ",rating)
if __name__ == "__main__":
    main()
