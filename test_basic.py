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
