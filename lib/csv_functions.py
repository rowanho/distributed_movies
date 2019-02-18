import csv

MOVIE_DIR = 'ml-latest-small'

#####functions that read/write to csv#####

#returns all movies in a dict of form {movie_id:movie_name,...}
def get_all_movies():
    movie_dict = {}
    with open(MOVIE_DIR +'/movies.csv') as movie_csv:
        reader = csv.reader(movie_csv,delimiter=',',quotechar= '|')
        for i,row in enumerate(reader):
            if i == 0:
                continue
            movie_dict[int(row[0])] = row[1]
    return movie_dict

#returns all ratings in a dict of the form {user_id,movie_id:rating, }
def get_all_ratings():
    ratings = {}
    with open(MOVIE_DIR + '/ratings.csv') as rating_csv:
        reader = csv.reader(rating_csv,delimiter=',',quotechar='|')
        for i,row in enumerate(reader):
            if i == 0:
                continue
            ratings[int(row[0]),int(row[1])] = float(row[2])
    return ratings
#gets a list of possible movies in format[(movie_id,movie_name),...] that match an input string
def csv_get_movies(movie_string):
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

#gets the rating of a user by user id and movie id
def csv_get_user_rating(user_id,movie_id):
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
#gets the overall rating of a movie_id for all users, returned as a float
def csv_get_overall_rating(movie_id):
    r_count,total_rating = 0,0
    print(movie_id)
    with open(MOVIE_DIR + '/ratings.csv') as rating_csv:
        reader = csv.reader(rating_csv, delimiter=',',quotechar ='"')
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
