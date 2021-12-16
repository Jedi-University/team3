import requests
from git_app.api.requests import Requests


class RequestsSync(Requests):

    def __init__(self, user: str, password: str,
                 *args, **kwargs):
        self.auth = requests.auth.HTTPBasicAuth(user, password)

    def get(self, url, mapper, **kwargs) -> requests.Response:
        params = kwargs
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.request("GET", url,
                                    headers=headers,
                                    params=params,
                                    auth=self.auth)
        result = mapper(response)
        return result
