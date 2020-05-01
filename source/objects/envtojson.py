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
import json
from os import getenv


def env_to_json(config_path: str,
                config_example_path: str = "data/configs/config.json.example"
                ) -> bool:
    """Converts the env config variables to a json file

    Parameters
    ----------
    config_path: str
         Path of the config file

    config_example_path: str, optional
          Path of the example config file defaults to
          ""data/configs/config.json.example""


    Returns
    -------
    bool
        It's True if the config parameters it's ok
    """

    with open(config_example_path, 'r') as config_example_file:
        config_example_json = json.load(config_example_file)
    config_json = dict()
    config_json["telegram"] = dict()
    config_json["telegram"]["bot-token"] = getenv("TOKEN-TG", None)
    if config_json["telegram"]["bot-token"] is None:
        return False
    config_json["redis"] = dict()
    config_json["redis"]["ip"] = getenv("REDIS-IP",
                                        config_example_json["redis"]["ip"])
    config_json["redis"]["port"] = getenv("REDIS-PORT",
                                          config_example_json["redis"]["port"])
    config_json["redis"]["database"] = getenv("REDIS-DATABASE",
                                              config_example_json["redis"]
                                              ["database"])
    # check if database is an integer
    try:
        config_json["redis"]["database"] = int(
            config_json["redis"]["database"])
    except ValueError:
        return False
    config_json["redis"]["password"] = getenv("REDIS-PASSWORD",
                                              config_example_json["redis"]
                                              ["password"])
    # export dict to json file
    with open(config_path, 'w') as config_file:
        json.dump(config_json, config_file, indent=2,
                  ensure_ascii=False)
    return True
