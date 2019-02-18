### Custom exceptions


#Raised by: Front end
#Caught by: Client
#Raise this exception if we can't find a free server (from the front end)
class NoFreeServerException(Exception):
    pass

#Raised by: Replica
#Caught by: Front end
#Note: Whether a movie id exists or not can only be checked if we have the data ie by the replica
#The client side can perform simple validation such as whether the movie id is actually number
class InvalidMovieIdException(Exception):
    pass

#Raised by: Replica
#Caught by: Front end
class InvalidRatingIdException(Exception):
    pass

#Raised by: replica
#Caught by: Front end
class NotUpToDateException(Exception):
    pass
