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

from source.objects.config_parser import Config
# configuration parser to get telegram info

from botogram import create, Buttons as BButtons
# Get botogram.create to save the username of the bot and
# Get a botogram.Buttons class and save it as BButtons

from typing import Union, List
# Needed for parameters and return hints


config = Config()
bot = create(config.telegram.bot_token)

bot_username = bot.itself.username
del bot, create


class _Category:
    """This class represents a category inside the language JSON file,
    located at data/language/lang{LANG}.json

    Attributes
    ----------
    lang : str
        The lang of the message text

    json_lang : dict
        The json that contains all message in the language

    category_name : str
        The represented category name

    Methods
    -------
    name(level: int = 1)
        Gets the category name based on the level

    emoji(level: int = 1)
        Gets the representing emoji based on the level

    name_full(level:int = 1, name_first: bool = True)
        Combines name and emoji based on the level (example "👷 Admin")
    """

    category_name: str

    def __init__(self, lang: Union[str, None] = None):
        """
        Initializes the translate Category, loads the JSON file based on the
        language

        Parameters
        ----------
        lang : str, None, Optional
            The lang of the message text

        """

        self.category_name = ""

        if lang is None:
            self.lang = config.telegram.lang_pref
        else:
            self.lang = lang
        try:
            with open('./data/language/lang' + self.lang + ".json",
                      encoding="utf8") as j:
                self.json_lang = json.load(j)
        except FileNotFoundError:
            self.lang = config.telegram.LANGPREF
            with open('./data/language/lang' + self.lang + ".json",
                      encoding="utf8") as j:
                self.json_lang = json.load(j)[self.category_name]

    def name(self, level: int = 1) -> Union[str, bool]:
        """
        Gets the category name based on the level

        Parameters
        ----------
        level : int, Optional
            The specified level

        Returns
        -------
        Union[str,bool]
            The name or False if not found
        """

        try:
            return self.json_lang[level-1]["name"]
        except (ValueError, IndexError):
            return False

    def emoji(self, level: int = 1) -> Union[str, bool]:
        """
        Gets the category corresponding emoji based off the level

        Parameters
        ----------
        level : int, Optional
            The level of the emoji

        Returns
        -------
        Union[str,bool]
            The corresponding emoji or False if not found
        """

        try:
            return self.json_lang[level-1]["emoji"]
        except (ValueError, IndexError):
            return False

    def name_full(self, level: int = 1, name_first: bool = False
                  ) -> Union[str, bool]:
        """
        Combines the name and corresponding emoji into one string

        Parameters
        ----------
        level : int, Optional
            The level of the name
        name_first : bool, Optional
            False if the emoji must come before the name, True otherwise
            If not specified is False

        Returns
        -------
        Union[str,bool]
            The name and emoji,
            or one of the two if the other is not present
            or False if neither is found
        """

        name = self.name(level)
        emoji = self.emoji(level)

        if name and emoji:
            if not name_first:
                return f"{emoji} {name}"

            else:
                return f"{name} {emoji}"

        elif name:
            return name

        elif emoji:
            return emoji

        else:
            return False


def text_replace(text: str, text_formatting: Union[dict, None] = None
                 ) -> str:
    """
    Replace the key with value in String

    Parameters
    ----------
    text: str
        The string where the words are replaced
    text_formatting: dict
        The dictionary containing "to_be_replaced: replacement" key pairs.
        The first half is the part to be replaced inside the string,
        the second half is the text which replaces the first

    Returns
    -------
    str
        The string with replaced text
    """
    if not text_formatting:
        text_formatting = dict()

    text_formatting.update({"bot_username": bot_username})

    try:
        text = text.format(**text_formatting)

    except (KeyError, ValueError):
        # Try except needed because if a string formatted like this ({a or
        # a}) the format function would fail, and if so the more inefficient
        # method is used

        for key, text_replacement in text_formatting.items():
            text = text.replace("{" + key + "}", text_replacement)
    return text


class CallMess:
    """Get the message text and buttons' callbacks / url.

    Attributes
    ----------
    lang : str
        The lang of the message text
    status : str
        The status of the message
    json_lang : dict
        The json that contains all the texts in the specified language
    json_callback : dict
        The json that contains all the callbacks and urls to be assigned to
        the buttons

    Methods
    -------

    message(text_formatting: dict = dict())
        Get the message text based on the status and the language.

    callback(btns: BButtons = None, text_button: dict = dict(),
                 text_data: dict = dict())
        Generate the button array and assign it callbacks and urls

    notify()
        Get the notify text based on the status and the language.
    """

    def __init__(self, status: str, lang: Union[str, None] = None):
        """
        Initializes the translate message

        Parameters
        ----------
        status : str
            The status of the message
        lang : str, None, Optional
            The lang of the message text

        """
        if lang is None:
            self.lang = config.telegram.lang_pref

        else:
            self.lang = lang
        self.status = status
        try:
            with open(f"./data/language/lang{self.lang}.json",
                      encoding="utf8") as j:
                self.json_lang = json.load(j)
        except FileNotFoundError:
            self.lang = config.telegram.lang_pref

            with open(f"./data/language/lang{self.lang}.json",
                      encoding="utf8") as j:
                self.json_lang = json.load(j)
        with open('./data/callback/callback.json', encoding="utf8") as j:
            self.json_callback = json.load(j)

        self.notify = self.notify

    def message(self, text_formatting: Union[dict, None] = None) -> str:
        """Get the message text based on the status and the language.

        Parameters
        ----------
        text_formatting : Union[dict, None], Optional
           The dictionary which contains "to_be_replaced: replacement" key
           pairs, it's used to format the text message by substituting {
           to_be_replaced} with the actual replacement

        Returns
        -------
        str
            The message text in the specified language
        """

        text = self.json_lang["error_msg"]
        category_name = self.status.split('@')[0]

        for category in self.json_lang["category"]:
            if category["category_name"] == category_name:
                for status in category["status"]:
                    if self.status == status["status_name"]:
                        if 'text' in status:
                            text = status["text"]
                            break
        return text_replace(text, text_formatting)

    def _callback_text(self, text_button: dict
                       ) -> Union[List[List[str]], bool]:
        """
        Internal function to simplify the code
        return the text of the button or None if not provided

        Parameters
        ----------
        text_button : dict
            The dictionary containing the button text parts to be replaced

        Returns
        -------
        Union[List[List[str]], bool]
            return the array of array of button text or True if buttons is null
            or False if status don't find
        """

        buttons_text = []
        category_name = self.status.split('@')[0]
        for category in self.json_lang["category"]:
            if category["category_name"] == category_name:
                for status in category["status"]:
                    if self.status == status["status_name"]:
                        if status["buttons"] is None:
                            # if status don't have a button return btns
                            return True
                        for row in status["buttons"]:
                            row_text = []
                            for buttons in row:
                                row_text.append(text_replace(
                                    buttons["text"],
                                    text_button))
                            buttons_text.append(row_text)
                            return buttons_text
        return False

    def _callback_callback(self, btns: BButtons, xbtns: int,
                           buttons_text: List[List[str]],
                           text_data: dict) -> Union[BButtons, None]:
        """
        Internal function to simplify the code
        return the buttons translated

        Parameters
        ----------

        btns : botogram.Buttons
            The botogram Buttons class
        xbtns : int
            The position to start buttons
        buttons_text : List[List[str]]
            the array of array of button text
        text_data : dict
            The dictionary when key as replaced on a data

        Returns
        -------
        Union[botogram.Buttons, None]
            The buttons translated or None if status don't find
        """
        category_name = self.status.split('@')[0]
        column_counter, row_counter = 0, 0

        for category in self.json_callback["category"]:
            if category["category_name"] == category_name:
                for status in category["status_name"]:
                    if self.status == status["status_name"]:
                        if status["buttons"] is None:
                            return btns

                        for rows in status["buttons"]:
                            for button in rows:

                                if button["type"] == "url":
                                    text = buttons_text[row_counter
                                                        ][column_counter]

                                    btns[xbtns
                                         ].url(text, text_replace(
                                                        button["callback"],
                                                        text_data)
                                               )

                                elif button["type"] == "callback":
                                    text = buttons_text[row_counter
                                                        ][column_counter]
                                    btns[xbtns
                                         ].callback(text, button["callback"],
                                                    text_replace(
                                                        button["data"],
                                                        text_data)
                                                    )

                                column_counter += 1

                            column_counter = 0
                            row_counter += 1
                            xbtns += 1
                        return btns
        return None

    def callback(self, btns: BButtons = None,
                 text_button: Union[dict, None] = None,
                 text_data: Union[dict, None] = None) -> BButtons:
        """
        Generate the button array

        Parameters
        ----------
        btns : botogram.Buttons, optional
          The botogram Buttons class
          If not specified will be created locally
        text_button : dict, Optional
          The dictionary when key as replaced on a text of the button
        text_data : dict, Optional
          The dictionary when key as replaced on a data

        Returns
        -------
        botogram.Buttons
            The buttons translated
        """

        if btns is None:
            btns = BButtons()

        if text_button is None:
            text_button = dict()

        if text_data is None:
            text_data = dict()

        xbtns = len(btns._rows)

        if xbtns != 0:
            xbtns += 1

        buttons_text = self._callback_text(text_button)

        if buttons_text is True:
            return btns

        elif buttons_text is False:
            btns[xbtns].callback(self.json_lang["error_button"], 'home')
            return btns

        btns_new = self._callback_callback(btns, xbtns,
                                           buttons_text,
                                           text_data)

        if btns_new:
            return btns_new

        else:
            btns[xbtns].callback(self.json_lang["error_button"], 'home')
            return btns

    def notify(self) -> Union[str, None]:
        """
        Get the notify text based on the status and the language.

        Returns
        -------
        Union[str,None]
            The Value of notify or None if not found
        """

        category_name = self.status.split('@')[0]
        for category in self.json_lang["category"]:
            if category["category"] == category_name:
                for status in category["status"]:
                    if self.status == status["status"]:
                        if "notify" in status:
                            return status["notify"]

        return None


class Role(_Category):
    """
    sub class of _Category
    This class as name_category is role
    """
    category_name = "role"
