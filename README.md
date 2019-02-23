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


Client program:

Follow the prompts to query and update ratings. A user can
add a movie rating, query all ratings for a movie, or query a specific rating by a user.
The client should correctly validate inputs, and the server/client handles issues such as
an attempt to fetch data for a movie id that does not exist.
The replicas load the "small" dataset from https://grouplens.org/datasets/movielens/latest/
