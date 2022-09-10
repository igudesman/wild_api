# pylint: disable=invalid-name, too-many-instance-attributes


from dataclasses import dataclass
from typing import Iterable

from models.base import BaseStatistics, BaseDataclass


@dataclass
class Stocks(BaseDataclass):
    lastChangeDate: str
    supplierArticle: str
    techSize: str
    barcode: str
    quantity: int
    isSupply: bool
    isRealization: bool
    quantityFull: int
    quantityNotInOrders: int
    warehouse: int
    warehouseName: str
    inWayToClient: int
    inWayFromClient: int
    nmId: int
    subject: str
    category: str
    daysOnSite: str
    brand: str
    SCCode: str
    Price: float
    Discount: float


class StocksStatistics(BaseStatistics):
    def __init__(self) -> None:
        super().__init__()
        self.path = '/api/v1/supplier/stocks'

    def parse_response(self, json_response, *args, **kwargs) -> Iterable[Stocks]:
        for item_dict in json_response:
            yield Stocks(**item_dict)
