# pylint: disable=too-many-arguments
import datetime
from typing import Union, List, Tuple, Dict

import gspread
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from gspread.client import Client
from gspread.exceptions import WorksheetNotFound

from config import credentials, Column
from libs.tools import get_current_week_range

import re


def get_spreadsheet(client: Client, url: str) -> Spreadsheet:
    return client.open_by_url(url=url)


def get_worksheet(
        spreadsheet: Spreadsheet, title: str, rows: int = 5000, cols: int = 300, **kwargs
) -> Worksheet:
    try:
        return spreadsheet.worksheet(title=title)
    except WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows=rows, cols=cols, **kwargs)


def get_matching_cell_address_for_full_name(
        worksheet: Worksheet, query: any, **kwargs
) -> Union[None, Tuple[int, int]]:
    cell = worksheet.find(query=query, **kwargs)
    if cell is not None:
        return cell.row, cell.col


def get_matching_cell_address_for_name(
        worksheet: Worksheet, query: any, full_name: str, **kwargs
) -> Union[None, Tuple[int, int]]:
    cells = worksheet.findall(query=re.compile(query), **kwargs)
    print(cells)
    if len(cells) != 0:
        return add_item_template(worksheet, full_name, list(get_current_week_range()), cells[0].row, max(map(lambda x: x.col, cells)) + 6)


def add_item_template(worksheet: Worksheet, name: str, week_range: List[str], start_row=None, start_col=None) -> Tuple[int, int]:
    if start_row is None and start_col is None:
        starting_row = len(worksheet.col_values(col=Column.DAY.value)) + 2
        if starting_row + 10 > worksheet.row_count:
            worksheet.add_rows(1000)  # adding extra rows
        names_starting_cell = gspread.cell.rowcol_to_a1(row=starting_row, col=Column.NAME.value)
        names_ending_cell = gspread.cell.rowcol_to_a1(row=starting_row, col=Column.STOCKS.value)

        days_starting_cell = gspread.cell.rowcol_to_a1(row=starting_row + 1, col=Column.DAY.value)
        days_ending_cell = gspread.cell.rowcol_to_a1(row=starting_row + 7, col=Column.DAY.value)

        starting_col = Column.NAME.value
    else:
        names_starting_cell = gspread.cell.rowcol_to_a1(row=start_row, col=start_col)
        names_ending_cell = gspread.cell.rowcol_to_a1(row=start_row, col=start_col + 4)

        days_starting_cell = gspread.cell.rowcol_to_a1(row=start_row + 1, col=start_col - 1)
        days_ending_cell = gspread.cell.rowcol_to_a1(row=start_row + 8, col=start_col - 1)

        starting_row = start_row
        starting_col = start_col

    worksheet.batch_update([
        {
            'range': f'{names_starting_cell}:{names_ending_cell}',
            'values': [[f'{name}', 'Склад', 'Заказы', 'Продажи', 'Остатки']]
        },
        {
            'range': f'{days_starting_cell}:{days_ending_cell}',
            'values': [[day] for day in week_range]
        }
    ])
    return int(starting_row), int(starting_col)


def add_item_data(
        worksheet: Worksheet,
        name: str,
        full_name: str,
        day_range_index: int,
        orders: int,
        sales: int,
        stocks: str,
        warehouse: str
):
    matching_cell = get_matching_cell_address_for_full_name(worksheet, full_name)
    if matching_cell is None:
        print('NOT FOUND FULL NAME')
        matching_cell = get_matching_cell_address_for_name(worksheet, query=name, full_name=full_name)
    if matching_cell is None:
        print('NOT FOUND NAME')
        matching_cell = add_item_template(worksheet, full_name, list(get_current_week_range()))
    converted_starting_cell = gspread.cell.rowcol_to_a1(
        row=matching_cell[0] + day_range_index + 1,
        col=matching_cell[1] + Column.WAREHOUSE.value - 2
    )
    converted_ending_cell = gspread.cell.rowcol_to_a1(
        row=matching_cell[0] + day_range_index + 1,
        col=matching_cell[1] + Column.STOCKS.value - 2
    )
    worksheet.batch_update([
        {
            'range': f'{converted_starting_cell}:{converted_ending_cell}',
            'values': [[warehouse, orders, sales, stocks]]
        }
    ])


def setup(date=None) -> Dict[str, Union[Client, Spreadsheet, Worksheet, List[str]]]:
    gclient = gspread.service_account('writer/service_account.json')
    # gclient = gspread.service_account('service_account.json')
    spread = get_spreadsheet(gclient, credentials['spreadsheet_url'])
    current_week_range = list(get_current_week_range(date))
    work = get_worksheet(spread, current_week_range[0] + ' - ' + current_week_range[-1])
    return {
        'gclient': gclient,
        'spreadsheet': spread,
        'worksheet': work,
        'current_week_range': current_week_range
    }


# if __name__ == '__main__':
#     configs = setup(datetime.date.today() - datetime.timedelta(days=3))
#     print(configs['worksheet'].title)
#     # get_matching_cell_address(configs['worksheet'], re.compile(r'Спреи, спрей_для_волос_15в1'))
#     # print(get_matching_cell_address_for_full_name(configs['worksheet'], 'Спреи, спрей_для_волос_15в1 (Казань)'))
#     print(get_matching_cell_address_for_name(configs['worksheet'], re.compile('форевер_темно-розовый'), 'форевер_темно-розовый (Челны)'))