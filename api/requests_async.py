import aiohttp

from api.requests import Requests


class RequestsAsync(Requests):

    # def __init__(self, session, user: str, password: str,
    def __init__(self, user: str, password: str,
                 *args, **kwargs):
        self.auth = aiohttp.BasicAuth(user, password)

    # async def get(self, url, **kwargs):
    #     if not hasattr(self, 'session'):
    #         self.session = aiohttp.ClientSession()
    #     params = kwargs
    #     headers = {'Accept': 'application/vnd.github.v3+json'}
    #     response = await self.session.get(url)
    #     # print(f'[RequestsAsync] {type(response)} {response.links}')
    #     # print(f'[RequestsAsync] {await response.json()}')
    #     # async with resp:
    #     #     assert resp.status == 200
    #     return response

    async def get(self, url, **kwargs):
        params = kwargs
        headers = {'Accept': 'application/vnd.github.v3+json'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   headers=headers,
                                   params=params,
                                   auth=self.auth) as response:
                result = {'json': await response.json()}
                if 'next' in response.links:
                    result['url'] = response.links['next']['url']

        return result


if __name__ == '__main__':
    pass
