import requests
from api.requests import Requests


class RequestsSync(Requests):

    def __init__(self, user: str, password: str,
                 *args, **kwargs):
        self.auth = requests.auth.HTTPBasicAuth(user, password)

    def get(self, url, **kwargs) -> requests.Response:
        params = kwargs
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.request("GET", url,
                                    headers=headers,
                                    params=params,
                                    auth=self.auth)
        return response


if __name__ == '__main__':
    pass
