# pylint: disable=too-many-arguments


from typing import Union, List, Tuple, Dict

import gspread
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from gspread.client import Client
from gspread.exceptions import WorksheetNotFound

from config import credentials, Column
from libs.tools import get_current_week_range


def get_spreadsheet(client: Client, url: str) -> Spreadsheet:
    return client.open_by_url(url=url)


def get_worksheet(
        spreadsheet: Spreadsheet, title: str, rows: int = 1000, cols: int = 1000, **kwargs
) -> Worksheet:
    try:
        return spreadsheet.worksheet(title=title)
    except WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows=rows, cols=cols, **kwargs)


def get_matching_cell_address(
        worksheet: Worksheet, query: str, **kwargs
) -> Union[None, Tuple[int, int]]:
    cell = worksheet.find(query=query, **kwargs)
    if cell is not None:
        return int(cell.row), int(cell.col)


def add_item_template(worksheet: Worksheet, name: str, week_range: List[str]) -> Tuple[int, int]:
    starting_row = len(worksheet.col_values(col=Column.DAY.value)) + 2
    if starting_row + 10 > worksheet.row_count:
        worksheet.add_rows(100)  # adding extra rows
    names_starting_cell = gspread.cell.rowcol_to_a1(row=starting_row, col=Column.NAME.value)
    names_ending_cell = gspread.cell.rowcol_to_a1(row=starting_row, col=Column.STOCKS.value)

    days_starting_cell = gspread.cell.rowcol_to_a1(row=starting_row + 1, col=Column.DAY.value)
    days_ending_cell = gspread.cell.rowcol_to_a1(row=starting_row + 7, col=Column.DAY.value)

    worksheet.batch_update([
        {
            'range': f'{names_starting_cell}:{names_ending_cell}',
            'values': [[f'{name}', 'Склад', 'Заказы', 'Остатки']]
        },
        {
            'range': f'{days_starting_cell}:{days_ending_cell}',
            'values': [[day] for day in week_range]
        }
    ])
    return int(starting_row), int(Column.NAME.value)


def add_item_data(
        worksheet: Worksheet,
        name: str,
        day_range_index: int,
        orders: int,
        stocks: str,
        warehouse: str
):
    matching_cell = get_matching_cell_address(worksheet, name)
    if matching_cell is None:
        matching_cell = add_item_template(worksheet, name, list(get_current_week_range()))
    converted_starting_cell = gspread.cell.rowcol_to_a1(
        row=matching_cell[0] + day_range_index + 1,
        col=Column.WAREHOUSE.value
    )
    converted_ending_cell = gspread.cell.rowcol_to_a1(
        row=matching_cell[0] + day_range_index + 1,
        col=Column.STOCKS.value
    )
    worksheet.batch_update([
        {
            'range': f'{converted_starting_cell}:{converted_ending_cell}',
            'values': [[warehouse, orders, stocks]]
        }
    ])


def setup() -> Dict[str, Union[Client, Spreadsheet, Worksheet, List[str]]]:
    gclient = gspread.service_account('writer/service_account.json')
    spread = get_spreadsheet(gclient, credentials['spreadsheet_url'])
    current_week_range = list(get_current_week_range())
    work = get_worksheet(spread, current_week_range[0] + ' - ' + current_week_range[-1])
    return {
        'gclient': gclient,
        'spreadsheet': spread,
        'worksheet': work,
        'current_week_range': current_week_range
    }
