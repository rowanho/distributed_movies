Requirements:
python 3.7
pyro4

Running the program on linux:

In the base directory of the project, run start_script.sh:

    source start_script.sh

This starts the pyro name service, 3 instances of replica.py, and frontend.py.


Run the client with:

    python3 client.py

To kill the processes after they are finished running, use the command:

    kill $(jobs -p)

Interacting with the client:

Follow the prompts to query and update ratings.

A user can add a movie rating, get all ratings for a movie id, or get a specific rating by user id & movie id.

The client program prints out the results of the query, as well as giving
the name of the movie corresponding to the given id, or an error message.


System information:
- The replicas load the "small" dataset from https://grouplens.org/datasets/movielens/latest/.
In memory model, so restarting the programs will reset the data.

- The front end can only use replicas reporting as "available" (neither "offline" or "overloaded").

- Replicas gossip at a fixed interval(1 second), sending data to up to 2 other replicas if "available".

- Every second, Replicas have a 30% chance of becoming "offline", and a 50% chance of coming back "online" (if "offline").

- "Offline" replicas neither send or recieve gossip.

- Whenever the front end server uses a replica, the replica reports itself as "overloaded" for that period.

- "Overloaded" replicas can send (but not recieve) gossip.

- Client/server handle invalid queries where a movie id or a rating (movie + user id) is not in the dataset.

- Consistent service - client's queries respect at least the updates they have made,
 by keeping a vector timestamp "prev" per client. Therefore updated rating/s can be queried by movie/user id
 and the rating/s should be present in the data returned.

 - Global ordering of updates - Ensured by sending and storing the date/time of when each update was sent.
