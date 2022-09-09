from dataclasses import dataclass
from typing import Iterable

from models.base import BaseStatistics, BaseDataclass


@dataclass
class Orders(BaseDataclass):
    gNumber: str
    date: str
    lastChangeDate: str
    supplierArticle: str
    techSize: str
    barcode: str
    totalPrice: float
    discountPercent: int
    warehouseName: str
    oblast: str
    incomeID: int
    odid: int
    nmId: int
    subject: str
    category: str
    brand: str
    isCancel: bool
    cancel_dt: str
    sticker: str
    srid: float


class OrdersStatistics(BaseStatistics):
    def __init__(self) -> None:
        super(OrdersStatistics, self).__init__()
        self.path = '/api/v1/supplier/orders'

    def parse_response(self, json_response, *args, **kwargs) -> Iterable[Orders]:
        for item_dict in json_response:
            yield Orders(**item_dict)
