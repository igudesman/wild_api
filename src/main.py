# pylint: disable=too-many-locals


import datetime
from collections import defaultdict
from pprint import pprint

import asyncio
from tqdm import tqdm

from writer.gtables_api import add_item_data, setup
from models.sales import SalesStatistics
from models.stocks_v2 import StocksV2Statistics
from models.orders import OrdersStatistics
from models.stocks import StocksStatistics
from models.displaying_item import DisplayingItem
from libs.exceptions import RequestError


async def cron_update(raw_current_date: datetime.date = None):
    if raw_current_date is None:
        raw_current_date = datetime.date.today()
    raw_date_for_stocks = raw_current_date - datetime.timedelta(days=7)
    date_for_stocks = raw_date_for_stocks.strftime('%Y-%m-%d')
    current_date = raw_current_date.strftime('%Y-%m-%d')
    items_data = defaultdict(DisplayingItem)

    # stocks_v2_stats = StocksV2Statistics()
    # try:
    #     await asyncio.sleep(1)
    #     stocks_v2_response = await stocks_v2_stats.make_request(skip=0, take=1000)
    #     for stock_v2_item in stocks_v2_stats.parse_response(stocks_v2_response):
    #         for stock_item in stock_v2_item.stocks:
    #             item = items_data[(stock_item['barcode'], stock_item['warehouseName'])]
    #             item.barcode = stock_item['barcode']
    #             item.name = stock_item['name']
    #             item.quantity = stock_item['stock']
    #             item.warehouseName = stock_item['warehouseName']
    # except RequestError as err:
    #     print('Stocks: ', err.message)

    stocks_stats = StocksStatistics()
    try:
        await asyncio.sleep(1)
        stocks_response = await stocks_stats.make_request(dateFrom=date_for_stocks)
        for stock_item in stocks_stats.parse_response(stocks_response):
            item = items_data[(stock_item.supplierArticle, stock_item.warehouseName)]
            item.warehouseName = stock_item.warehouseName
            item.supplierArticle = stock_item.supplierArticle
            item.quantity += stock_item.quantity
            item.subject = stock_item.subject
    except RequestError as err:
        print('Stocks: ', err.message)

    sales_stats = SalesStatistics()
    try:
        await asyncio.sleep(1)
        sales_response = await sales_stats.make_request(dateFrom=current_date, flag=1)
        for sale_item in sales_stats.parse_response(sales_response):
            if sale_item.saleID.startswith('S') and sale_item.date.startswith(current_date):
                # if (sale_item.supplierArticle, sale_item.warehouseName) not in items_data:
                #     print((sale_item.supplierArticle, sale_item.warehouseName))
                items_data[(sale_item.supplierArticle, sale_item.warehouseName)].sales += 1
    except RequestError as err:
        print('Sales: ', err.message)

    orders_stats = OrdersStatistics()
    try:
        await asyncio.sleep(1)
        orders_response = await orders_stats.make_request(dateFrom=current_date, flag=1)
        for order_item in orders_stats.parse_response(orders_response):
            items_data[(order_item.supplierArticle, order_item.warehouseName)].orders += 1
    except RequestError as err:
        print('Orders: ', err.message)
    #
    # grouped_data = defaultdict(DisplayingItem)
    # for key, data in items_data.items():
    #     item = grouped_data[(data.name, data.warehouseName)]
    #     item.name = data.name
    #     item.warehouseName = data.warehouseName
    #     item.barcode = data.barcode
    #     item.sales += data.sales
    #     item.quantity += data.quantity

    gconfig = setup(raw_current_date)
    for key, data in tqdm(items_data.items()):
        await asyncio.sleep(2)
        if data.supplierArticle is not None and data.warehouseName is not None and data.supplierArticle != '' and data.warehouseName != '':
            print(data)
            add_item_data(
                worksheet=gconfig['worksheet'],
                full_name=data.subject + ', ' + data.supplierArticle + f' ({data.warehouseName})',
                name=data.subject + ', ' + data.supplierArticle,
                day_range_index=gconfig['current_week_range'].index(current_date),
                orders=data.orders,
                sales=data.sales,
                stocks=data.quantity,
                warehouse=data.warehouseName
            )


if __name__ == '__main__':
    date = datetime.date.today() - datetime.timedelta(days=4)
    asyncio.run(cron_update(date))
