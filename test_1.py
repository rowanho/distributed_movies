import Pyro4
import random

def test_basic():
    with Pyro4.Proxy("PYRONAME:frontend") as frontend:
        ratings = []
        for i in range(20 * 4):
            ratings.append(random.randint(1,5)/2)
        count = 0
        for m in range(1,21):
            for u in range(1,5):
                frontend.add_rating(m,u,ratings[count])
                count += 1
        count = 0
        for m in range(1,21):
            for u in range(1,5):
                res  = frontend.get_user_rating(m,u)[1]
                assert res == ratings[count]
                count += 1

def test_concurrent():
    #two different "clients" add rating to same booking
    #second one should get returned, as later
    ratings = []
    for i in range(10):
        ratings.append(random.randint(1,5)/2)

    id_pairs = []
    for i in range(1,4):
        for j in range(1,4):
            id_pairs.append((i,j))
    for idp in id_pairs:
        for i in range(5):
            with Pyro4.Proxy("PYRONAME:frontend") as frontend:
                frontend.add_rating(idp[0],idp[1],ratings[2 * i])

            with  Pyro4.Proxy("PYRONAME:frontend") as frontend:
                frontend.add_rating(idp[0],idp[1],ratings[(2 * i) + 1])
                assert frontend.get_user_rating(idp[0],idp[1])[1] == ratings[(2 * i) + 1]
