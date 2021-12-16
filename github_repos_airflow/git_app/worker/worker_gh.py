from git_app.worker.worker import Worker
from git_app.api.requests import Requests


class WorkerGH(Worker):

    def __init__(self, tops_n: int, requests: Requests,
                 *args, **kwargs):
        self.tops_n = tops_n
        self.requests = requests

    def get_json(self, response):
        return response.json()

    def response_mapper(self, response):
        result = {'json': self.get_json(response)}
        if 'next' in response.links:
            result['url'] = response.links['next']['url']
        return result

    def get_api_response(self, url, **kwargs):
        response = self.requests.get(
            url, mapper=self.response_mapper, **kwargs)
        return response

    def get_stars_top(self, repos: list) -> list:
        repos.sort(key=lambda x: x['stars_count'], reverse=True)
        return repos[:self.tops_n]

    def run(self):
        pass
