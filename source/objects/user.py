import redis
from source.objects.config_parser import ConfigParser
from botogram import User as bUser
config = ConfigParser("data/configs/config.json")

r = redis.Redis(host=config.redis.IP, db=config.redis.DATABASE, port=config.redis.PORT, password=config.redis.PASSWORD)
# Connect to the redis database


class User:
    """The User object represents a Telegram user in the redis database. It contains the user username (if present),
    his Telegram ID, First Name, Last Name and last activity

    Attributes
    ----------
    id : int
        An Integer representing the user's Telegram ID
    first_name: str
        A string representing the users's First Name on Telegram
    last_name: str
        A string representing the user's Last Name on Telegram"""

    def __init__(self, botogram_user: bUser = None, telegram_id: int = 0):
        """Initializes the user entry in redis or gets the user data, if already present
        :param botogram_user botogram.User type, it represents the user to get the info for
        :param telegram_id:"""

        if not all((botogram_user, telegram_id)):           # If both arguments are left to be default
            raise ValueError("Expected either botogram_user or telegram_id values")  # Raise a ValueError
            #                                                                          (at least one is required)

        if botogram_user and not telegram_id:               # If a botogram User is passed
            self.id = botogram_user.id                      # Save its id as an attribute
            self.redis_hash = f"user:{self.id}"             # Get it's redis hash from the id

            if not (self._get_redis_value(self.id)):            # If its user data is not present on redis
                self.first_name = botogram_user.first_name      # Save its first name on tg as an attribute
                self.last_name = botogram_user.last_name        # Save its last name on tg as an attribute
            #                                                     (None if not present)
                self._set_redis_value("first_name", self.first_name)    # Set its first name on redis
                self._set_redis_value("last_name", self.last_name)      # Set its last name on redis

            else:
                self.first_name = self._get_redis_value("first_name")
                self.last_name = self._get_redis_value("last_name")

    def _get_redis_value(self, key: str):
        """Function which simplifies the redis hget function"""
        return r.hget(self.redis_hash, key)

    def _set_redis_value(self, key: str, value):
        """Function which simplifies the redis hset function"""
        return r.hset(self.redis_hash, key, value)

    def state(self, new_state: str):
        pass
