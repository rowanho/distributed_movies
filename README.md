Requirements:
python 3.7
pyro4

Running the program automatically on linux:

Assign the script start_script.sh permissions to execute and run the script:

    ./start_script.sh n

Where n is the number of replica managers to use (an integer >= 3)

Running the program manually:

Start the pyro name service:

    pyro4-ns &

Run 3 (or more) instances of replica.py

    python3 replica.py n &

Where n is the number of replica managers to use (an integer >= 3), and
running replica.py n times.

Run the front end server:

    python3 frontend.py &


Run the client:

    python3 client.py &


Interacting with the client:

Follow the prompts to query and update ratings. A user can add a movie rating,
get all ratings for a movie id, or get a specific rating by user id & movie id.

System information and guarantees:
- The replicas load the "small" dataset from https://grouplens.org/datasets/movielens/latest/

- Replicas have a 10% chance of going down (reporting as "offline") every 1 second, and a 50% chance of coming back online if
offline every second. Whenever a client uses a replica, the replica reports itself as "overloaded" for that period. 

- The server/client handles invalid input formats and movies/ratings that do not exist.

- Consistency ensured so that a client's queries respect at least the updates they have made,
 by keeping a timestamp "prev" for each client.
