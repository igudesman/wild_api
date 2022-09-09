from config import credentials
from libs.tools import retry

import urllib.parse
from typing import Dict, List, Union, Iterable, Tuple

import aiohttp
from aiohttp.client_exceptions import ClientResponseError
import asyncio


class BaseDataclass:
    def __init__(self):
        pass


class BaseStatistics:
    def __init__(self):
        self.base_url = 'https://suppliers-stats.wildberries.ru'
        self.path = None

    @retry(max_retries=2)
    async def make_request(self, timeout=3.0, **kwargs) -> Tuple[Union[None, Dict[str, Union[List, str]]], str]:
        kwargs['key'] = credentials['key']
        full_url = urllib.parse.urljoin(self.base_url, self.path)

        async with aiohttp.ClientSession(headers={'Authorization': credentials['auth']}) as session:
            error_message = None
            try:
                response = await session.get(url=full_url, params=kwargs)
                response.raise_for_status()
                return await response.json(), ''
            except ClientResponseError as e:
                if e.status == 429:
                    error_message = e.message
                    await asyncio.sleep(timeout)
            finally:
                await session.close()
            return None, error_message

    def parse_response(self, *args, **kwargs) -> Iterable[BaseDataclass]:
        pass
