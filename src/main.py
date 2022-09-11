# pylint: disable=too-many-locals


import datetime
from collections import defaultdict

import asyncio

from writer.gtables_api import add_item_data, setup
from models.stocks import StocksStatistics
from models.sales import SalesStatistics
from models.displaying_item import DisplayingItem
from libs.exceptions import RequestError


async def cron_update():
    current_date = datetime.date.today().strftime('%Y-%m-%d')

    items_data = defaultdict(DisplayingItem)

    stocks_stats = StocksStatistics()
    try:
        stocks_response = await stocks_stats.make_request(dateFrom=current_date)
        for stock_item in stocks_stats.parse_response(stocks_response):
            item = items_data[(stock_item.nmId, stock_item.warehouseName)]
            item.nmId = stock_item.nmId
            item.subject = stock_item.subject
            item.quantity = stock_item.quantity
            item.warehouseName = stock_item.warehouseName
    except RequestError as err:
        print('Stocks: ', err.message)

    sales_stats = SalesStatistics()
    try:
        sales_response = await sales_stats.make_request(dateFrom=current_date)
        for sale_item in sales_stats.parse_response(sales_response):
            item = items_data[(sale_item.nmId, sale_item.warehouseName)]
            if sale_item.saleID.startswith('S'):
                item.orders += 1
    except RequestError as err:
        print('Orders: ', err.message)

    gconfig = setup()
    for key, data in items_data.items():
        print(data)
        await asyncio.sleep(1)
        add_item_data(
            worksheet=gconfig['worksheet'],
            name=data.subject + f' ({key[1]})',
            day_range_index=gconfig['current_week_range'].index(current_date),
            orders=data.orders,
            stocks=data.quantity,
            warehouse=key[1]
        )


if __name__ == '__main__':
    asyncio.run(cron_update())
