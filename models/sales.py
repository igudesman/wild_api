# pylint: disable=invalid-name, too-many-instance-attributes


from dataclasses import dataclass
from typing import Iterable

from models.base import BaseStatistics, BaseDataclass


@dataclass
class Sales(BaseDataclass):
    gNumber: str
    date: str
    lastChangeDate: str
    supplierArticle: str
    techSize: str
    barcode: str
    totalPrice: float
    discountPercent: int
    isSupply: bool
    isRealization: bool
    promoCodeDiscount: float
    warehouseName: str
    countryName: str
    oblastOkrugName: str
    regionName: str
    incomeID: int
    saleID: str
    odid: int
    spp: float
    forPay: float
    finishedPrice: float
    priceWithDisc: float
    nmId: int
    subject: str
    category: str
    brand: str
    sticker: str
    srid: str
    IsStorno: str


class SalesStatistics(BaseStatistics):
    def __init__(self) -> None:
        super().__init__()
        self.path = '/api/v1/supplier/sales'

    def parse_response(self, json_response, *args, **kwargs) -> Iterable[Sales]:
        for item_dict in json_response:
            yield Sales(**item_dict)
