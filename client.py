# saved as greeting-client.py
import Pyro4



def get_user_movie_ids():
    valid_user = False
    valid_movie = False
    while not valid_movie:
        input_movie = input("\nEnter movie id: ")
        input_user = input("\nEnter user id: ")
        try:
            movie_id = int(input_movie)
            valid_movie = True
        except:
            print("Please enter a valid integer for movie id (a positive integer)")
    while not valid_user:
        try:
            user_id = int(input_user)
            if user_id > 0:
                valid_user = True
        except:
            print("Please enter a valid integer for user id (a positive integer)")
    return movie_id,user_id


#returns a float divisble by 0.5 - the rating of a movie
def add_movie_rating(frontend):
    valid_rating = False
    movie_id, user_id = get_user_movie_ids()
    while not valid_rating:
        input_movie_rating = input("Enter your rating: ")
        try:
            movie_rating = float(input_movie_rating)
            if movie_rating >= 0.5 and movie_rating <= 5.0:
                if (movie_rating *  2).is_integer():
                    valid_rating = True
        except:
            pass
        if not valid_rating:
            print("Please enter a valid rating (multiple of 0.5 between 0.5 and 5)")
    print("Adding rating..")
    return frontend.add_rating(user_id,movie_id,movie_rating)

#returns the name of a movie and an array of all ratings for a movie
def get_all_ratings(frontend):
    valid = False
    while not valid:
        try:
            movie_id = int(input("\nEnter movie id: "))
            valid = True
        except:
            print("Error, please enter a valid integer.")
    print("Getting ratings..")

    return frontend.get_all_ratings(movie_id)

def get_user_rating(frontend):
    movie_id, user_id = get_user_movie_ids()
    print("Getting rating..")
    # actually call the remote functions here
    return (user_id,) + frontend.get_user_rating(user_id,movie_id)


#ratings
def make_ratings_dict():
    d = {}
    for i in range(11):
        d[i * 0.5] = 0
    return d


#takes in array of ratings and returns a string that shows a nicer representation
def display_ratings_list(movie_name,ratings_list):
    output = "\nRatings for movie ''%s'\n" % (movie_name)
    output += "\nTotal ratings: " + str(len(ratings_list)) + "\n"
    ratings_dict = make_ratings_dict()
    for r in ratings_list:
        ratings_dict[r] += 1
    for key, val in ratings_dict.items():
        if key.is_integer():
            output += str(int(key)) +"   : " + str(val) + "\n"
        else:
            output += str(key) +" : " + str(val) + "\n"
    return output


def main():
    exit = False
    frontend = Pyro4.Proxy("PYRONAME:frontend")
    phrase = "\nEnter 1 to get all ratings for a movie, 2 to get a rating for a specific movie/user,\
 3 to add a new rating, or q to quit:"
    while not exit:
        i = input(phrase)
        if i == '1':
            try:
                movie_name,ratings = get_all_ratings(frontend)
                print(display_ratings_list(movie_name,ratings))
            except Exception as e:
                if str(e) == "InvalidMovieIdException":
                    print("\nMovie id does not exist")
        elif i == '2':
            try:
                user_id,movie_name,rating = get_user_rating(frontend)
                if rating.is_integer():
                    print("\nUser %d rated %s a %d out of 5" % (user_id,movie_name,rating))
                else:
                    print("\nUser %d rated %s a %.1f out of 5" % (user_id,movie_name,rating))
            except Exception as e:
                if str(e) == "InvalidRatingIdException":
                    print("\nRating does not exist for that movie and user")
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
