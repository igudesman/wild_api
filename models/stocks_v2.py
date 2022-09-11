# pylint: disable=invalid-name, too-many-instance-attributes


from dataclasses import dataclass
from typing import Iterable, List, Dict, Union

from models.base import BaseStatistics, BaseDataclass


@dataclass
class StocksV2(BaseDataclass):
    stocks: List[Dict[str, Union[str, List[str]]]]
    total: str


class StocksV2Statistics(BaseStatistics):
    def __init__(self) -> None:
        super().__init__()
        self.path = '/api/v2/stocks'
        self.base_url = 'https://suppliers-api.wildberries.ru'

    def parse_response(self, json_response, *args, **kwargs) -> Iterable[StocksV2]:
        yield StocksV2(**json_response)
