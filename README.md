Requirements:
python 3.7
pyro4

Running the program:

Run 3 (or more) instances of replica.py
    python3 replica.py &
If you are using more than 3 servers, the number of servers you intend to start needs to be passed
to replica.py, for example to start 4 servers the command:
    python3 replica.py 4 &
would be needed to run 4 times


Run the front end server:
    python3 frontend.py

Run the client:
    python3 client.py


Client program:

Follow the prompts to query and update ratings. A user can
add a movie rating, query all ratings for a movie, or query a specific rating by a user.
The client should correctly validate inputs, and the server/client handles issues such as
an attempt to fetch data for a movie id that does not exist.
The replicas load the "small" dataset from https://grouplens.org/datasets/movielens/latest/
