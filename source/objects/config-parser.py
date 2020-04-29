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
    It contains the bot token and other stuff"""
    def __init__(self, config_path: str):
        with open(config_path) as config_file:                             # Open the config json file
            config_json = json.load(config_file)                           # Parse it

        self.TELEGRAM_BOT_TOKEN = config_json["telegram"]["bot-token"]     # Save the telegram bot token as an attribute