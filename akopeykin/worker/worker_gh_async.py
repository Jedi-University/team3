from api.requests_async import RequestsAsync

from worker.worker import Worker


class WorkerGHAsync(Worker):

    def __init__(self, tops_n: int, requests: RequestsAsync,
                 *args, **kwargs):
        self.tops_n = tops_n
        self.requests = requests

    async def get_api_response(self, url, **kwargs):
        response = await self.requests.get(url, **kwargs)
        return response

    def get_stars_top(self, repos: list) -> list:
        repos.sort(key=lambda x: x['stars_count'], reverse=True)
        return repos[:self.tops_n]

    def run(self):
        pass


if __name__ == '__main__':
    pass
