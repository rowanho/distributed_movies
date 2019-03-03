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

The client program prints out the results of the query, as well as giving
the name of the movie corresponding to the given id, or an error message.


System information:
- The replicas load the "small" dataset from https://grouplens.org/datasets/movielens/latest/. They use
an in memory model, so restarting the programs will reset the data.

- Replicas gossip at a fixed interval(1 second), each replica gossips to up to 2 available servers.

- The front end can only use replicas reporting as "available" (neither "offline" or "overloaded")

- Every second, Replicas have a 30% chance of becoming "offline", and a 50% chance of coming back "online" (if "offline"). If a replica becomes "offline" whilst the front end is calling a remote method on it, the front end attempts to use another replica.

- "Offline" replicas neither send or recieve gossip.

- Whenever the front end server uses a replica, the replica reports itself as "overloaded" for that period.

- "Overloaded" replicas can send (but not recieve) gossip.

- The client/server handle invalid queries where a movie id or a rating (movie id + user id) is not in the dataset.

- Consistency ensured so that a client's queries respect at least the updates they have made,
 by keeping a timestamp "prev" for each client. Therefore updated ratings can be queried by movie/user id
 and the new rating should be present in the data returned by the server.
