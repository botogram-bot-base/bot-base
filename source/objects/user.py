"""MIT License

Copyright (c) 2020 Francesco Zimbolo A.K.A. Haloghen & Matteo Bocci A.K.A.
matteob99

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import redis
# Required to work with redis

from source.objects.config_parser import ConfigParser
# Configuration parser to get redis db info

from botogram import User as bUser
# Get a botogram.User class and save it as bUser

from typing import Union
# Needed for parameters and return hints

from datetime import datetime as dt
# Needed to save the last activity

config = ConfigParser("data/configs/config.json")
# Load the config file and parse it

r = redis.Redis(host=config.redis.IP, db=config.redis.DATABASE,
                port=config.redis.PORT, password=config.redis.PASSWORD,
                decode_responses=True)
# Connect to the redis database


class User:
    """The User object represents a Telegram user in the redis database. It
    contains the user username (if present),
    his Telegram ID, First Name, Last Name and last activity

    Attributes
    ----------
    id : int
        An Integer representing the user's Telegram ID
    first_name : str
        A string representing the users's First Name on Telegram
    last_name : str, optional
        A string representing the user's Last Name on Telegram, defaults to ""
        if the user doesn't have a last name
        on Telegram
    username : str, optional
        A string representing the user's Username on Telegram, defaults to ""
        if the user doesn't have an username on
        Telegram
    last_activity : float
        User's last activity on the BOT

    Methods
    -------
    state(new_state: str = "")
        Sets a new state for the user or returns the current one
    """

    def __init__(self, botogram_user: bUser = None, telegram_id: int = 0):
        """Initializes the user entry in redis or gets the user data, if already
        present

        Parameters
        ----------
        botogram_user : botogram.User, optional
            The Telegram user to be saved/recalled from redis, leave empty to
            use the Telegram id
        telegram_id : int, optional
            The Telegram ID of the user to be recalled from redis, leave empty
            to use the botogram User

        Raises
        ------
        ValueError
            If neither the botogram_user nor telegram_id is provided or if both
            are provided and don't match
        """

        if not all((botogram_user, telegram_id)):
            # If both arguments are left to be default

            raise ValueError("Expected either botogram_user"
                             "or telegram_id values")
            # Raise a ValueError (at least one is required)

        if (botogram_user and not telegram_id
                or botogram_user.id == telegram_id):
            # If a botogram User is passed or both are passed and they match
            self.id = botogram_user.id  # Save its id as an attribute

            self.redis_hash = f"user:{self.id}"
            # Get it's redis hash from the id

            if not (self._get_redis_value("id")):  # If its user data is not
                # present on redis

                self.first_name = botogram_user.first_name
                # Save its first name on tg as an attribute

                self.last_name = botogram_user.last_name
                # Save its last name on tg as an attribute
                # (None if not present)

                self.username = botogram_user.username
                # Save its username on tg as an attribute (None if not present)

                self.last_activity = dt.timestamp(dt.now())
                self._state = "home"

                self._set_redis_value("first_name", self.first_name)
                # Set its first name on redis

                self._set_redis_value("last_name", self.last_name)
                # Set its last name on redis

                self._set_redis_value("username", self.username)
                # Set its username on redis

                self._set_redis_value("last_activity", self.last_activity)
                # Set its last activity on redis

                self.state(self._state)
                # Save the user state

            else:           # If the user is present on redis
                # Get its info
                self.first_name = self._get_redis_value("first_name")
                self.last_name = self._get_redis_value("last_name")
                self.username = self._get_redis_value("username")
                self.last_activity = self._get_redis_value("last_activity",
                                                           float)
                self._state = self.state()

        elif telegram_id and not botogram_user:    # If a telegram id is passed
            self.id = telegram_id                  # Save it as an attribute
            self.redis_hash = f"user:{self.id}"    # Get the redis hash

            # Check if it's present on redis
            if not(self._get_redis_value("id")):
                raise ValueError("User not found in the redis database,"
                                 " cannot utilize the telegram id")
                # Can't get data from an id, so raise ValueError

            # Else get its data
            self.first_name = self._get_redis_value("first_name")
            self.last_name = self._get_redis_value("last_name")
            self.username = self._get_redis_value("username")
            self.last_activity = self._get_redis_value("last_activity", float)
            self._state = self.state()

        else:
            raise ValueError("Both a Botogram User and a Telegram"
                             " ID were passed, but they didn't match")

    def _get_redis_value(self, key: str, type_of_return: type = str
                         ) -> Union[str, int, float, bool]:
        """Function which simplifies the redis hget function

        Parameters
        ----------
        key : str
            The key to get from redis
        type_of_return : type, optional
            How to return the value, either as a str, an int or a float,
            defaults to str

        Returns
        -------
        Union[str, int, float]
            The value which corresponds to the provided key, either an int, a
            float or a str

        Raises
        ------
        TypeError
            If the requested value is not an int or a float, and it's requested
            as such, raise a TypeError
        """

        value = r.hget(self.redis_hash, key)     # Get the key value from Redis
        if type_of_return is int:                # If it's requested as an int
            try:                                 # Try to cast and return
                return int(value)
            except ValueError:
                raise TypeError("The requested value from Redis is not an int")
                # Alert if not possible
        elif type_of_return is float:            # If it's requested as a float
            try:                                 # Try to cast and return
                return float(value)
            except ValueError:
                raise TypeError("The requested value "
                                "from Redis is not a float")
                # Alert if not possible
        return value

    def _set_redis_value(self, key: str, value: Union[str, int, float]
                         ) -> bool:
        """Function which simplifies the redis hset function
        Parameters
        ----------
        key : str
            The key to set on redis
        value : Union[str, int, float]
            The value to set on that key

        Returns
        -------
        bool
            True if the operation succeeded and a new entry was created, False
            if an existing key was altered
        """

        return r.hset(self.redis_hash, key, value)

    def state(self, new_state: str = "") -> Union[str, bool]:
        """Function which sets a new user state or returns the current one if
        no new one is provided
        Parameters
        ----------
        new_state : str, optional
            The new state to be set, the current state is returned if it's not
            provided

        Returns
        -------
        Union[str, bool]
            Returns a str representing the user's state or True if the
            state was set successfully
        """

        if not new_state:
            # If a new state wasn't passed

            return self._get_redis_value("state")
            # Get the current one

        self._set_redis_value("state", new_state)
        # Otherwise set the new state

        return True                                # Return True
