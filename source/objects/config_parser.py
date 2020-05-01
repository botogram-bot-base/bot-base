"""MIT License

Copyright (c) 2020 Francesco Zimbolo A.K.A. Haloghen & Matteo Bocci A.K.A. matteob99

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

import json


class _TelegramConfig:
    """Class which represents the configuration needed for the telegram bot to work
    It contains the bot token and other stuff

    Attributes
    ----------
    TELEGRAM_BOT_TOKEN : str
        It represents the BOT Token on Telegram
    """

    def __init__(self, config_json: dict):
        """Get the bot token from the config json and save it as an attribute

        Parameters
        ----------
        config_json : dict
            The dictionary (json parsed) config file

        Raises
        ------
        KeyError
            If the telegram entry in the config file is not present
        """

        self.TELEGRAM_BOT_TOKEN = config_json["telegram"]["bot-token"]     # Save the telegram bot token as an attribute


class _RedisConfig:
    """Class which represents the configuration needed for redis to successfully connect and work
    It contains the redis IP, port, database and password

    Attributes
    ----------
    IP : str
        The IP where the redis db is located
    PORT : int
        The port used to connect
    DATABASE : int
        The database index used by the bot
    PASSWORD : Union[str, None]
        The password used to connect to the db, None if not present
    """

    def __init__(self, config_json: dict):
        """Parses the redis related config into attributes

        Parameters
        ----------
        config_json : dict
            The dictionary (json parsed) config file

        Raises
        ------
        KeyError
            If the redis entry in the config file is not present
        """

        redis_config = config_json["redis"]                     # Get the redis config

        self.IP = redis_config["ip"]                            # Parse the ip as an attribute
        self.PORT = redis_config["port"]                        # Parse the port
        self.DATABASE = redis_config["database"]                # Parse the database
        self.PASSWORD = redis_config["password"]                # Parse the password


class ConfigParser:
    """Class which parses the config file and gives a nice and parsed, ready to use config

    Attributes
    ----------
    redis : _RedisConfig
        It contains the redis configuration
    telegram : _TelegramConfig
        It contains the telegram bot configuration
    """

    def __init__(self, config_path: str):
        """Opens the config file, parses it as nested dictionaries and gets the relevant infos from it

        Parameters
        ----------
        config_path : str
            The path to the config file
        """
        with open(config_path) as config_file:                  # Open the config file
            config_json = json.load(config_file)                # Parse it to nested dictionaries

        try:
            self.redis = _RedisConfig(config_json)              # Parse it
        except KeyError:
            print("[-] Redis Config not found")                 # Alert if not found

        try:
            self.telegram = _TelegramConfig(config_json)        # Parse it
        except KeyError:
            print("[-] Telegram Config not found")              # Alert if not found
