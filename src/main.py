# pylint: disable=too-many-locals


import datetime
from collections import defaultdict
from pprint import pprint

import asyncio

from writer.gtables_api import add_item_data, setup
from models.sales import SalesStatistics
from models.stocks_v2 import StocksV2Statistics
from models.displaying_item import DisplayingItem
from libs.exceptions import RequestError


async def cron_update(current_date: datetime.date = None):
    if current_date is None:
        current_date = datetime.date.today()
    next_date = current_date + datetime.timedelta(days=1)
    next_date = next_date.strftime('%Y-%m-%d')
    current_date = current_date.strftime('%Y-%m-%d')
    items_data = defaultdict(DisplayingItem)

    stocks_v2_stats = StocksV2Statistics()
    try:
        await asyncio.sleep(1)
        stocks_v2_response = await stocks_v2_stats.make_request(skip=0, take=1000)
        for stock_v2_item in stocks_v2_stats.parse_response(stocks_v2_response):
            for stock_item in stock_v2_item.stocks:
                item = items_data[(stock_item['barcode'], stock_item['warehouseName'])]
                item.barcode = stock_item['barcode']
                item.name = stock_item['name']
                item.quantity = stock_item['stock']
                item.warehouseName = stock_item['warehouseName']
    except RequestError as err:
        print('Stocks: ', err.message)

    sales_stats = SalesStatistics()
    barcodes = defaultdict(int)
    try:
        await asyncio.sleep(1)
        sales_response = await sales_stats.make_request(dateFrom=next_date)
        for sale_item in sales_stats.parse_response(sales_response):
            if sale_item.saleID.startswith('S') and sale_item.date.startswith(current_date):
                barcodes[sale_item.barcode] += 1
        for key in items_data.keys():
            items_data[key].sales += barcodes[key[0]]
    except RequestError as err:
        print('Orders: ', err.message)

    grouped_data = defaultdict(DisplayingItem)
    for key, data in items_data.items():
        item = grouped_data[(data.name, data.warehouseName)]
        item.name = data.name
        item.warehouseName = data.warehouseName
        item.barcode = data.barcode
        item.sales += data.sales
        item.quantity += data.quantity

    gconfig = setup()
    for key, data in grouped_data.items():
        print(data)
        await asyncio.sleep(1)
        add_item_data(
            worksheet=gconfig['worksheet'],
            name=data.name + f' ({key[1]})',
            day_range_index=gconfig['current_week_range'].index(current_date),
            orders=data.sales,
            stocks=data.quantity,
            warehouse=key[1]
        )


if __name__ == '__main__':
    date = datetime.date.today() - datetime.timedelta(days=0)
    asyncio.run(cron_update(date))
