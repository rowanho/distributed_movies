import Pyro4


def test_basic():
    with Pyro4.Proxy("PYRONAME:frontend") as frontend:
        frontend.add_rating(5,5,4.5)
        frontend.add_rating(4,1,4)
        frontend.add_rating(1,3,5)
        print(frontend.get_user_rating(5,5)[1])
        print(frontend.get_user_rating(4,1)[1])
        print(frontend.get_user_rating(1,3)[1])

def test_concurrent():
    #two different "clients" add rating to same booking
    #second one should get returned, as later
    with Pyro4.Proxy("PYRONAME:frontend") as frontend:
        frontend.add_rating(5,5,4.5)

    with  Pyro4.Proxy("PYRONAME:frontend") as frontend:
        frontend.add_rating(5,5,4)
        print(frontend.get_user_rating(5,5)[1])

def main():
    test_basic()
    test_concurrent()

if __name__ == "__main__":
    main()
