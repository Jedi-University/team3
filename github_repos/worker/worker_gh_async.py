import asyncio

from api.requests_async import RequestsAsync

from worker.worker import Worker


class WorkerGHAsync(Worker):

    def __init__(self, tops_n: int, requests: RequestsAsync,
                 *args, **kwargs):
        self.tops_n = tops_n
        self.requests = requests

    async def get_json_async(self, response):
        return await response.json()

    async def get_json(self, response):
        # loop = asyncio.get_event_loop()
        # json = loop.run_until_complete(self.get_json_async(response))
        # json = loop.call_soon(self.get_json_async, response)
        # json = loop.create_task(self.get_json_async(response))
        # json = asyncio.wait_for(self.get_json_async(response), None)
        json = await self.get_json_async(response)
        # print(f'json: {str(json)[:150]}')
        return json

    async def response_mapper(self, response):
        result = {'json': await self.get_json(response)}
        if 'next' in response.links:
            result['url'] = response.links['next']['url']
        return result

    async def get_api_response(self, url, **kwargs):
        response = await self.requests.get(
            url, mapper=self.response_mapper, **kwargs)
        return response

    def get_stars_top(self, repos: list) -> list:
        repos.sort(key=lambda x: x['stars_count'], reverse=True)
        return repos[:self.tops_n]

    def run(self):
        pass
