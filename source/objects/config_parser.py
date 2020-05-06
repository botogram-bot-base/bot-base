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

from json import load, dumps
from typing import Union, List, Dict


class _ConfigCategory:
    """A category inside the config file. This class represents an entry in
    the config file with a name and a set of keys/a list.

    The attribute "keys" is only a placeholder. Suppose we have the following
    category:
        {"category_name: {"key1": "value1", "key2": "value2"}}
    The corresponding _ConfigCategory object will have the following
    attributes:
        category_name.name = category_name
        category_name.key1 = value1
        category_name.key2 = value2

    Do not use this class alone. If you want to work with the config file
    use the Config class.

    Attributes
    ----------
    name : str
        The name of the category, and how it is saved inside the json file
    list : list, optional
        The list this category represents, if present. It's not possible to
        define a category both as a list or as a set of keys (with the
        exception where one of the keys' value is a list)
    keys : Union[str, int, float, list, dict], optional
        It represents an entry in this category keys list. It can be a
        number, a string, a list or another dictionary (treated as
        subcategory, so it's advised to use the
        _ConfigCategory.add_category() method for that).

    Methods
    -------
    add_keys(keys: Dict[float, int, str, bool, None, List[float, int, str,
    bool, None]])
        Add new keys into the category. Every key:value pair will be saved
        as an attribute with the following format:
            category.key = value
        It raises a ValueError if there is an already defined list.
        Every value passed to this method MUST BE SUPPORTED BY JSON

    add_list(list_to_add: List[float, int, str, bool, None])
        Assign a list to the category. It raises a ValueError if there are
        already defined keys, because a category can't be both a dictionary
        and a list.
        Every value inside the list MUST BE SUPPORTED BY JSON

    add_category(new_category_name: str)
        Add a new subcategory to the current one. It will be saved as a
        parameter, with the name passed to "new_category_name" and value
        _ConfigCategory(new_category_name)

    as_dict() -> Union[list, dict]
        Returns the dictionary or list representation of the category.
    """
    list: list

    def __init__(self, name: str, keys:
                 Union[Dict[str, Union[float, bool, int, str, None]],
                       List[Union[float, bool, int, str, None]], None] = None):
        """Initialize the category by assigning it a name and a set of keys
        or a list if specified

        Parameters
        ----------
        name : str
            The category name
        keys : Union[Dict[float, bool, int, str, None], List[float, bool,
                     int, str, None], None], optional
            The keys to set at category creation time, leave empty to
            initialize an empty category.
        """

        self.name = name        # Save the category name

        if keys:                # If keys are passed
            if type(keys) is list:
                self.add_list(keys)

            elif type(keys) is dict:
                keys_to_be_added = dict()
                for key, value in keys.items():
                    if type(value) in [dict, list]:
                        setattr(self, key, _ConfigCategory(key, value))
                    else:
                        keys_to_be_added[key] = value
                self.add_keys(keys_to_be_added)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<ConfigCategory object ({self.name})"

    def add_keys(self, keys: Dict[str, Union[float, int,
                                  str, None, bool, List[Union[int, float, str,
                                                        None, bool, List]]]]):
        """This method allow to add a new set of keys to the current
        category.

        Parameters
        ----------
        keys : Dict[str, Union[float, int, str, bool, None, List[Union[int,
        float, str, bool, None, list]]]]
            The keys to add to the category, formatted as a dictionary where
            the key is a string and the value can be whatever is supported
            by JSON.

        Raises
        ------
        ValueError:
            Since the category can be either a list or a set of keys,
            but not both at the same time, a ValueError is raised if there
            is an attempt to add keys to an already defined-as-a-list category
        """

        try:                # Check if there is a list defined
            if self.list:
                raise ValueError("A category cannot be both a list and a "
                                 "dictionary. A list was already declared for "
                                 "this category.")  # Raise a ValueError if so
        except AttributeError:  # else
            for key, value in keys.items():  # For every key: value pair passed
                setattr(self, key.replace('-', '_'), value)  # Set an
                # attribute which has the key with - replaced by _ as the
                # attribute name and his value as the corresponding
                # attribute value

    def add_list(self, list_to_add: List[Union[int, float, str, None, bool,
                                         List]]):
        """This method allows to add a new list to the category. It cannot
        be used in conjunction with the add_keys() method, or a ValueError
        is raised.

        Parameters
        ----------
        list_to_add : List[Union[int, float, str, None, bool, list]]
            The list to add to this category. It will be saved as the value
            of this category name key

        Raises
        ------
        ValueError:
            Since a category cannot be a list and a dictionary at the same
            time, if some keys were added, a ValueError is raised when
            attempting to add the list
        """

        keys = [key for key in dir(self) if not key.startswith("__") and key
                != "list" and not callable(getattr(self, key)) and key !=
                "name"]
        if keys:
            print(keys)
            raise ValueError("A category cannot be both a list and a "
                             "dictionary. Keys were already declared for "
                             "this category.")
        self.list = list_to_add

    def add_category(self, new_category_name: str):
        """This method allows to add a new subcategory to the current one,
        saved as an attribute with new_category_name as its name and a new
        _ConfigCategory object as its value

        Parameters
        ----------
        new_category_name : str
            The name of the new subcategory
        """

        setattr(self, new_category_name, _ConfigCategory(new_category_name))

    def as_dict(self) -> Union[List, dict]:
        """This method allows to parse the current category as a dictionary,
        formatted like this:
            {category_name: {key1: value1}}
        or
            {category_name: [value1, value2]}
        or any other variant, and it includes any possibile subcategory as
        well

        Returns
        -------
        Union[dict, list]:
            The dictionary or list which represents this category
        """

        try:
            return self.list
        except AttributeError:
            keys = [key for key in dir(self) if
                    not key.startswith("__") and key
                    != "list" and not callable(getattr(self, key)) and key
                    != "name"]

            key_dict = dict()
            for key in keys:
                if type(getattr(self, key)) is not _ConfigCategory:
                    key_dict[key] = getattr(self, key)
                else:
                    key_dict[key] = getattr(self, key).as_dict()
            # category_dict = dict()
            # category_dict[self.name] = key_dict
            return key_dict


class Config:
    """This class represents a configuration for the entire project. It
    includes every category created or loaded from the correspondent JSON
    file. The methods included allow to add new categories, parse the config as
    a dictionary or as a JSON, load the configuration from JSON or save it
    as JSON.

    Attributes
    ----------
    default_path : str
        The config file default path, used if no path is specified when
        saving or loading the config file
    categories : _ConfigCategory
        A category inside the config file. Its name won't be "category" but
        will correspond to the name set when calling the add_category()
        method, and its value will be a _ConfigCategory object

    Methods
    -------
    add_category(category_name: str, initial_keys: Union[dict, list, None] =
        None) -> bool:
        This method allows to add a new category to the config file. Passing a
        list or a dictionary (CONTAINING JSON COMPATIBLE OBJECTS) will add
        those to the newly created category

    as_dict() -> dict:
        This method will return the entire config as a dictionary,
        where every key is a category containing other dictionaries or lists

    as_json(indentation: int = 2) -> str:
        This method will return the entire config as a json formatted
        string, ready to be saved. The indentation parameter will define the
        indent of the json parsed string

    save_to_json(path: str, indentation: int = 2) -> bool:
        This method allows to save the configuration to a JSON file at the
        specified path with the specified indentation

    load_from_json(path: str = "") -> bool:
        This method loads the config file from json and parses it into
        nested classes
    """

    def __init__(self, categories: Union[List[
                 _ConfigCategory], None] = None, load_from_json: bool = True,
                 path: str = ""):
        """This method initializes the config object, with the specified
        initial categories (or empty if None is passed)

        Parameters
        ----------
        categories : Union[List[_ConfigCategory], None], optional
            The categories to add to the config, optional, leave empty to
            initialize an empty config file

        load_from_json : bool, optional
            This parameter defines if the config must be loaded from the
            default JSON file when the object is created, defaults to True
        """

        self.default_path = "data/configs/config.json"

        if categories:
            for category in categories:
                setattr(self, category.name, category)
        else:
            if load_from_json:
                self.load_from_json(path=path)

    def add_category(self, category_name: str,
                     initial_keys: Union[dict, list, None] = None):
        """This method allows to add a new category to the configuration

        Parameters
        ----------
        category_name : str
            The name of the new category

        initial_keys : Union[dict, list, None], optional
            The keys to be added to the newly created category
        """

        setattr(self, category_name, _ConfigCategory(category_name,
                                                     initial_keys))

    def as_dict(self) -> dict:
        """This method allows to return the config as a dictionary

        Returns
        -------
        dict:
            The dictionary representing the configuration
        """

        categories = [category for category in dir(self) if not callable(
            getattr(self, category)) and not category.startswith("__")
                      and type(getattr(self, category)) is _ConfigCategory]

        config_dict = dict()

        for category in categories:
            config_dict[category] = getattr(self, category).as_dict()
        return config_dict

    def as_json(self, indentation: int = 2) -> str:
        """This method allows to get the configuration as a json-formatted
        string

        Parameters
        ----------
        indentation : int, optional
            How many spaces to use when indenting the JSON, leave empty to
            use 2

        Returns
        -------
        str:
            The JSON-formatted string representing the config
        """

        config_dict = self.as_dict()

        return dumps(config_dict, indent=indentation, ensure_ascii=True)

    def save_to_json(self, path: str = "", indentation: int = 2) -> bool:
        """This method allows to save the current configuration as a JSON to
        the specified path or the defualt one with the specified indentation or
        the default one

        Parameters
        ----------
        path : str, optional
            The path where to save the JSON, leave empty to use the default
            one
        indentation : int, optional
            How to indent the JSON, leave empty to use the default one, 2
        """

        json_parsed = self.as_json(indentation)

        if not path:
            path = self.default_path

        try:
            with open(path, 'w') as json_file:
                json_file.write(json_parsed)

        except FileExistsError:
            return False

        return True

    def load_from_json(self, path: str = "") -> bool:
        """This method allows to load and parse into objects a JSON config
        file

        Parameters
        ----------
        path : str, optional
            Where the JSON is located, leave empty to use the default one
        """

        if not path:
            path = self.default_path

        try:
            with open(path, 'r') as json_file:
                json_parsed = load(json_file)
        except FileNotFoundError:
            return False

        for category in json_parsed:
            self.add_category(category, initial_keys=json_parsed[category])
