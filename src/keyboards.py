from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

get_stocks_button = KeyboardButton('Get stocks')
get_orders_button = KeyboardButton('Get orders')
keyboard.add(get_stocks_button)
keyboard.add(get_orders_button)


# comment added
