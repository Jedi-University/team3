from worker.worker import Worker
from api.requests import Requests


class WorkerGH(Worker):

    def __init__(self, tops_n: int, requests: Requests,
                 *args, **kwargs):
        self.tops_n = tops_n
        self.requests = requests

    def get_api_response(self, url, **kwargs):
        response = self.requests.get(url, **kwargs)
        return response

    def get_stars_top(self, repos: list) -> list:
        repos.sort(key=lambda x: x['stars_count'], reverse=True)
        return repos[:self.tops_n]

    def run(self):
        pass
