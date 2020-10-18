import csv

MOVIE_DIR = 'ml-latest-small'

##### functions that read/write to csv #####

# returns all movies in a dict of form {movie_id:movie_name,...}
def get_all_movies():
    movie_dict = {}
    with open(MOVIE_DIR +'/movies.csv') as movie_csv:
        reader = csv.reader(movie_csv,delimiter=',',quotechar= '|')
        for i,row in enumerate(reader):
            if i == 0:
                continue
            movie_dict[int(row[0])] = row[1]
    return movie_dict

# returns all ratings in a dict of the form {user_id,movie_id:rating, }
def get_all_ratings():
    ratings = {}
    with open(MOVIE_DIR + '/ratings.csv') as rating_csv:
        reader = csv.reader(rating_csv,delimiter=',',quotechar='|')
        for i,row in enumerate(reader):
            if i == 0:
                continue
            ratings[int(row[0]),int(row[1])] = float(row[2])
    return ratings
