import os
from enum import Enum

credentials = {
    'auth': os.getenv('AUTH'),
    'key': os.getenv('KEY'),
    'bot_token': os.getenv('BOT_TOKEN'),
    'spreadsheet_url':
        'https://docs.google.com/spreadsheets/d/1ik4yadseIoMLFOWKpmxwdFfUxcos2hW0BF9WOnUQmhw',
}


class Column(Enum):
    DAY: int = 1
    NAME: int = 2
    WAREHOUSE: int = 3
    ORDERS: int = 4
    SALES: int = 5
    STOCKS: int = 6
