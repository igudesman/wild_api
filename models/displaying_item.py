from dataclasses import dataclass

from models.base import BaseDataclass


@dataclass
class DisplayingItem(BaseDataclass):
    warehouseName: str = ''
    quantity: str = 0
    subject: str = ''
    nmId: str = ''
    orders: int = 0
