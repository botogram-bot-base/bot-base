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

from source.objects.config_parser import ConfigParser
# configuration parser to get telegram info

from botogram import create, Buttons as BButtons
# Get botogram for save username of the bot

from typing import Union, List
# Needed for parameters and return hints


config = ConfigParser("data/configs/config.json")
bot = create(config.telegram.BOT_TOKEN)
bot_username = bot.itself.username
del bot, create


class _Category:
    """Get the message text and buttons callbacks / url.

    Attributes
    ----------
    lang: str
        The lang of the message text
    status: str
        The status of the message

    json_lang: dict
        The json that contiens all message in the language

    json_callback: dict
        The json that contiens all callback function

    Methods
    -------

    message(textreplaces: dict = dict())
        Get the message text based on the status and the language.

    callback(btns: BButtons = None, text_button: dict = dict(),
                 text_data: dict = dict())
        Generate the button array

    notify()
        Get the notify text based on the status and the language.

    """
    name_category = None

    def __init__(self, lang: Union[str, None]):
        """
        Initializes the translate Category

        Parameters
        ----------
        lang: str, None, Optional
            The lang of the message text

        """
        if lang is None:
            self.lang = config.telegram.LANGPREF
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
                self.json_lang = json.load(j)[self.name_category]

    def name(self, level: int = 1) -> Union[str, bool]:
        """
        prende il nome della categoria definita dal livello

        Parameters
        ----------
        level: int, Optional
            The level of the name
            If not specified is 1

        Returns
        -------
        str,None
            The name or False if not found
        """
        try:
            return self.jsonlang[level-1]["name"]
        except (ValueError, IndexError):
            return False

    def emoji(self, level: int = 1) -> Union[str, bool]:
        """
        prende il emoji della categoria definita dal livello

        Parameters
        ----------
        level: int, Optional
            The level of the emoji
            If not specified is 1

        Returns
        -------
        str,None
            The emoji or False if not found
        """
        try:
            return self.jsonlang[level-1]["emoji"]
        except (ValueError, IndexError):
            return False

    def name_full(self, level: int = 1, first: bool = True
                  ) -> Union[str, bool]:
        """
        prende il nome della categoria definita dal livello

        Parameters
        ----------
        level: int, Optional
            The level of the name
            If not specified is 1
        first: bool, Optional
            true if emoji first or false if name first
            If not specified is ture

        Returns
        -------
        str,None
            The name and emoji,
            or one of the two if the other is not present
            or False if not any found
        """
        name = self.name(level)
        emoji = self.emoji(level)
        if name and emoji:
            if first:
                return emoji + ' ' + name
            else:
                return name + ' ' + emoji
        elif name:
            return name
        elif emoji:
            return emoji
        else:
            return False


def text_replace(text: str, textreplaces: dict = dict()
                 ) -> str:
    """
    Replace the key with value in String

    Parameters
    ----------
    text: str
        The string where the words are replaced
    textreplaces: dict
        The dictionary when key as replaced

    Returns
    -------
    str
        The string with replaced name
    """
    textreplaces.update({"usernamebot": bot_username})
    try:
        text = text.format(**textreplaces)
    except (KeyError, ValueError):
        for key, textreplace in textreplaces.items():
            text = text.replace("{" + key + "}", textreplace)
    return text


class CallMess:
    """Get the message text and buttons callbacks / url.

    Attributes
    ----------
    lang: str
        The lang of the message text
    status: str
        The status of the message

    json_lang: dict
        The json that contiens all message in the language

    json_callback: dict
        The json that contiens all callback function

    Methods
    -------

    message(textreplaces: dict = dict())
        Get the message text based on the status and the language.

    callback(btns: BButtons = None, text_button: dict = dict(),
                 text_data: dict = dict())
        Generate the button array

    notify()
        Get the notify text based on the status and the language.

    """

    def __init__(self, status: str, lang: Union[str, None] = None):
        """
        Initializes the translate message

        Parameters
        ----------
        status: str
            The status of the message
        lang: str, None, Optional
            The lang of the message text

        """
        if lang is None:
            self.lang = config.telegram.LANGPREF
        else:
            self.lang = lang
        self.status = status
        try:
            with open('./data/language/lang' + self.lang + ".json",
                      encoding="utf8") as j:
                self.json_lang = json.load(j)
        except FileNotFoundError:
            self.lang = config.telegram.LANGPREF
            with open('./data/language/lang' + self.lang + ".json",
                      encoding="utf8") as j:
                self.json_lang = json.load(j)
        with open('./data/callback/callback.json', encoding="utf8") as j:
            self.json_callback = json.load(j)

    def message(self, textreplaces: dict = dict()) -> str:
        """Get the message text based on the status and the language.

        Parameters
        ----------
        textreplaces: dict, Optional
           The dictionary when key as replaced on a message

        Returns
        -------
        str
            The message text translated

        """
        text = self.json_lang["error_msg"]
        category_name = self.status.split('@')[0]
        for category in self.json_lang["category"]:
            if category["category"] == category_name:
                for status in category["status"]:
                    if self.status == status["state"]:
                        if 'text' in status:
                            text = status["text"]
                            break
        return text_replace(text, textreplaces)

    def _callback_text(self, text_button: dict
                       ) -> Union[List[List[str]], bool]:
        """
        Internal function for simplify the code
        return the text of the button or None if not provided

        Parameters
        ----------
        text_button : dict
            The dictionary when key as replaced on a text of the button

        Returns
        -------
        Union[List[List[str]], bool]
            return the array of array of button text or True if buttons is null
            or False if status don't find
        """
        buttons_text = []
        category_name = self.status.split('@')[0]
        for category in self.json_lang["category"]:
            if category["category"] == category_name:
                for status in category["status"]:
                    if self.status == status["state"]:
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

    def _calback_callback(self, btns: BButtons, xbtns: int,
                          buttons_text: List[List[str]],
                          text_data: dict) -> Union[BButtons, None]:
        """
        Internal functio for simplify the code
        return the buttons translated

        Parameters
        ----------

        btns: botogogra.buttons
            The botogram Buttons class
        xbtns: int
            The position to start buttons
        buttons_text: List[List[str]]
            the array of array of button text
        text_data: dict
            The dictionary when key as replaced on a data

        Returns
        -------
        botogram.Buttons, None
            The buttons translated or None if status don't find
        """
        category_name = self.status.split('@')[0]
        x, y = 0, 0

        for category in self.json_callback["category"]:
            if category["category"] == category_name:
                for status in category["status"]:
                    if self.status == status["state"]:
                        if status["buttons"] is None:
                            return btns
                        for rows in status["buttons"]:
                            for button in rows:
                                if button["type"] == "url":
                                    btns[xbtns].url(buttons_text[y][x],
                                                    text_replace(
                                                        button["callback"],
                                                        text_data)
                                                    )
                                elif button["type"] == "callback":
                                    btns[xbtns].callback(buttons_text[y][x],
                                                         button["callback"],
                                                         text_replace(
                                                             button["data"],
                                                             text_data)
                                                         )
                                x += 1
                            x = 0
                            y += 1
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
        btns: botogram.Buttons, optional
          The botogram Buttons class
          If not specified will be created locally
        text_button: dict, Optional
          The dictionary when key as replaced on a text of the button
        text_data: dict, Optional
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

        btns_new = self._calback_callback(btns, xbtns,
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
    name_category = "role"