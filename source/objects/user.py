import redis
from source.objects.config_parser import ConfigParser
from botogram import User as bUser
from typing import Union
from datetime import datetime as dt
config = ConfigParser("data/configs/config.json")

r = redis.Redis(host=config.redis.IP, db=config.redis.DATABASE, port=config.redis.PORT, password=config.redis.PASSWORD,
                decode_responses=True)
# Connect to the redis database


class User:
    """The User object represents a Telegram user in the redis database. It contains the user username (if present),
    his Telegram ID, First Name, Last Name and last activity

    Attributes
    ----------
    id : int
        An Integer representing the user's Telegram ID
    first_name : str
        A string representing the users's First Name on Telegram
    last_name : str, optional
        A string representing the user's Last Name on Telegram, defaults to "" if the user doesn't have a last name
        on Telegram
    username : str, optional
        A string representing the user's Username on Telegram, defaults to "" if the user doesn't have an username on
        Telegram
    last_activity : float
        User's last activity on the BOT

    Methods
    -------
    state(new_state: str = "")
        Sets a new state for the user or returns the current one
    """

    def __init__(self, botogram_user: bUser = None, telegram_id: int = 0):
        """Initializes the user entry in redis or gets the user data, if already present
        Parameters
        ----------
        botogram_user : botogram.User, optional
            The Telegram user to be saved/recalled from redis, leave empty to use the Telegram id
        telegram_id : int, optional
            The Telegram ID of the user to be recalled from redis, leave empty to use the botogram User

        Raises
        ------
        ValueError
            If neither the botogram_user nor telegram_id is provided
        """

        if not all((botogram_user, telegram_id)):           # If both arguments are left to be default
            raise ValueError("Expected either botogram_user or telegram_id values")  # Raise a ValueError
            #                                                                          (at least one is required)

        if botogram_user and not telegram_id:               # If a botogram User is passed
            self.id = botogram_user.id                      # Save its id as an attribute
            self.redis_hash = f"user:{self.id}"             # Get it's redis hash from the id

            if not (self._get_redis_value(self.id)):            # If its user data is not present on redis
                self.first_name = botogram_user.first_name      # Save its first name on tg as an attribute
                self.last_name = botogram_user.last_name        # Save its last name on tg as an attribute
                #                                                 (None if not present)
                self.username = botogram_user.username          # Save its username on tg as an attribute
                #                                                 (None if not present)
                self.last_activity = dt.timestamp(dt.now())

                self._set_redis_value("first_name", self.first_name)    # Set its first name on redis
                self._set_redis_value("last_name", self.last_name)      # Set its last name on redis
                self._set_redis_value("username", self.username)        # Set its username on redis

            else:
                self.first_name = self._get_redis_value("first_name")
                self.last_name = self._get_redis_value("last_name")
                self.username = self._get_redis_value("username")

    def _get_redis_value(self, key: str, type_of_return: type = str) -> Union[str, int, float, bool]:
        """Function which simplifies the redis hget function

        Parameters
        ----------
        key : str
            The key to get from redis
        type_of_return : type, optional
            How to return the value, either as a str, an int or a float, defaults to str

        Returns
        -------
        Union[str, int, float]
            The value which corresponds to the provided key, either an int, a float or a str

        Raises
        ------
        TypeError
            If the requested value is not an int or a float, and it's requested as such, raise a TypeError
        """

        value = r.hget(self.redis_hash, key)                        # Get the key value from Redis
        if type_of_return is int:                                   # If it's requested as an int
            try:                                                    # Try to cast and return
                return int(value)
            except ValueError:
                raise TypeError("The requested value from Redis is not an int")  # Alert if not possible
        elif type_of_return is float:                               # If it's requested as a float
            try:                                                    # Try to cast and return
                return float(value)
            except ValueError:
                raise TypeError("The requested value from Redis is not a float")  # Alert if not possible
        return value

    def _set_redis_value(self, key: str, value: Union[str, int]) -> bool:
        """Function which simplifies the redis hset function
        Parameters
        ----------
        key : str
            The key to set on redis
        value : str or int

        Returns
        -------
        bool
            True if the operation succeeded, False otherwise
        """

        return r.hset(self.redis_hash, key, value)

    def state(self, new_state: str = ""):
        """Function which sets a new user state or returns the current one if no new one is provided
        Parameters
        ----------
        new_state : str, optional
            The new state to be set, the current state is returned if it's not provided

        Returns
        -------
        Union[str, bool]
            Returns a str representing the user's state or True if the state was set successfully
        """

        if not new_state:
            return self._get_redis_value("state")

        self._set_redis_value("state", new_state)
        return True
