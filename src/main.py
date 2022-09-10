from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

from config import credentials
from models.stocks import StocksStatistics
from models.orders import OrdersStatistics
from libs.exceptions import RequestError

from keyboards import keyboard


bot = Bot(token=credentials['bot_token'])
dp = Dispatcher(bot)


@dp.message_handler(Text(equals='Get stocks'))
async def get_stocks(message: types.Message):
    stocks_stats = StocksStatistics()
    try:
        stocks_response = await stocks_stats.make_request(dateFrom='2022-09-10')
        for stock_item in stocks_stats.parse_response(stocks_response):
            await message.reply(str(stock_item))
            break
    except RequestError as err:
        await message.reply(err.message)


@dp.message_handler(Text(equals='Get orders'))
async def get_orders(message: types.Message):
    orders_stats = OrdersStatistics()
    try:
        orders_response = await orders_stats.make_request(dateFrom='2022-09-09')
        for order_item in orders_stats.parse_response(orders_response):
            await message.reply(str(order_item))
            break
    except RequestError as err:
        await message.reply(err.message)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Hello!', reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
