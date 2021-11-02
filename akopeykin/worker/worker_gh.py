import requests

from worker.worker import Worker


class WorkerGH(Worker):

    def __init__(self, tops_n: int, user: str, password: str,
                 *args, **kwargs):
        self.auth = requests.auth.HTTPBasicAuth(user, password)
        self.tops_n = tops_n

    def get_api_response(self, url, **kwargs) -> requests.Response:
        params = kwargs
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.request("GET", url,
                                    headers=headers,
                                    params=params,
                                    auth=self.auth)
        # if response.status_code != 200:
        # print(response.status_code, response.text)
        return response

    def get_stars_top(self, repos: list) -> list:
        repos.sort(key=lambda x: x['stars_count'], reverse=True)
        return repos[:self.tops_n]

    def run(self):
        pass


if __name__ == '__main__':
    pass
