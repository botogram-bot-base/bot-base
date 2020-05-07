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
from json import dump
from os import environ
from typing import List, Union, TextIO


def env_to_json(config_path: Union[str, TextIO],
                dictionary: dict = None
                ) -> bool:
    """Converts the env config variables to a json file

    Parameters
    ----------
    config_path: str
         Path of the config file

    dictionary: dict, Optional
        pass dictionary to parse or None to get the env dictionary
    Returns
    -------
    bool
        It's True if the config parameters it's ok
    """

    def populate_dict(keys: List[str], dict_append: dict) -> None:
        key = keys.pop(0)
        if len(keys) > 0:
            # if key is not the last element
            if key not in dict_append:
                # if key is not a key of a dict create a dictionary
                dict_append[key] = dict()
            populate_dict(keys, dict_append[key])
            return
        else:
            dict_append[key] = value
            return

    if dictionary is None:
        dictionary = environ
    # if the env variable ENABLE_ENV return False
    if dictionary.get("ENABLE_ENV", False) is False:
        return False
    else:
        del dictionary["ENABLE_ENV"]
    config_json = dict()
    for keys, value in dictionary.items():
        keys = keys.split("@")
        populate_dict(keys, config_json)

    # export dict to json file
    if type(config_path) is str:
        with open(config_path, 'w') as config_file:
            dump(config_json, config_file, indent=2,
                 ensure_ascii=False)
    else:
        dump(config_json, config_path, indent=2,
             ensure_ascii=False)
    return True


if __name__ == '__main__':
    print(env_to_json("foo.json"))
