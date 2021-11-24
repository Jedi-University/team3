import aiohttp
import asyncio

from api.requests import Requests


class RequestsAsync(Requests):

    def __init__(self, user: str, password: str,
                 *args, **kwargs):
        self.auth = aiohttp.BasicAuth(user, password)

    async def get(self, url, mapper, **kwargs):
        params = kwargs
        headers = {'Accept': 'application/vnd.github.v3+json'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   headers=headers,
                                   params=params,
                                   auth=self.auth) as response:
                result = await mapper(response)
        return result
