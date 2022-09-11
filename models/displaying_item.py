# pylint: disable=invalid-name, too-many-instance-attributes


from dataclasses import dataclass

from models.base import BaseDataclass


@dataclass
class DisplayingItem(BaseDataclass):
    warehouseName: str = ''
    quantity: str = 0
    name: str = ''
    barcode: str = ''
    sales: int = 0
