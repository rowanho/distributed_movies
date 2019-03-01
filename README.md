Requirements:
python 3.7
pyro4

Running the program on linux:

    chmod +x start_script.sh
    source start_script.sh

This starts the pyro name service, 3 instances of replica.py, and frontend.py.


Run the client with:

    python3 client.py

To kill the processes after they are finished running, use the command:

    kill $(jobs -p)

Interacting with the client:

Follow the prompts to query and update ratings. A user can add a movie rating,
get all ratings for a movie id, or get a specific rating by user id & movie id.

System information and guarantees:
- The replicas load the "small" dataset from https://grouplens.org/datasets/movielens/latest/

- Replicas gossip at a fixed interval(1 second), each replica gossips to up to 2 available servers.

- The front end server attempts to find a server which is reporting as "available" (ie neither "offline" or "overloaded")

- Replicas that are online have a 20% chance of going down (reporting as "offline") every 1 second, and a 50% chance of coming back online (if
offline) every second. Whenever the front end server needs to use a replica, the replica reports itself as "overloaded" for that period.

- The server/client handles invalid input formats and movies/ratings that do not exist.

- Consistency ensured so that a client's queries respect at least the updates they have made,
 by keeping a timestamp "prev" for each client.
