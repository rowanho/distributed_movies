## Running the program on linux:

Create a python >=3.7 environment and install requirements:

    pip install -r requirements.txt
    
In the base directory of the project, run start_script.sh:

    source start_script.sh

This starts the pyro name service, 3 instances of replica.py, and frontend.py.
Each server should print out a message when they are up and running.

Run the client with:

    python3 client.py

To kill the processes after they are finished running, use the command:

    kill $(jobs -p)

Interacting with the client:

- Follow the prompts to query and update ratings.

- A user can add a movie rating, get all ratings for a movie id, or get a specific rating by user id & movie id.

- The client program prints out a display of the results of a query, or an error message if input is invalid.


System information:
-

- The front end can only use replicas reporting as "available" (neither "offline" or "overloaded").

- Replicas gossip at a fixed interval(1 second), sending data to up to 2 other replicas if "available".

- Every second, Replicas have a 30% chance of simulating becoming "offline", and a 50% chance of coming back "online" (if "offline").

- "Offline" replicas neither send or recieve gossip. "Overloaded" replicas send gossip but can't recieve any.

- Whenever the front end server uses a replica, the replica reports itself as "overloaded" for that period.

- Consistent service - client's queries respect at least the updates they have made. Ensured by keeping a timestamp "prev" per client.

 - Global ordering of updates - Ensured by sending and storing the date/time of when each update was sent.
