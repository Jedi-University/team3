import requests

from orch.orch import Orch


class GHubData():

    def __init__(self, tops_n: int, orgs_n: int,
                 user: str, password: str,
                 orch: Orch, per_page: int = 100, **kwargs):
        self.per_page = per_page
        self.tops_n = tops_n
        self.orgs_n = orgs_n
        self.user = user
        self.password = password
        self.orch = orch

    def get_api_response(self, url, **kwargs) -> requests.Response:
        params = kwargs
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.request(
            "GET", url, headers=headers,
            params=params,
            auth=requests.auth.HTTPBasicAuth(self.user, self.password))
        if response.status_code != 200:
            print(response.status_code, response.text)
        return response

    def get_orgs_url(self):
        url = (f"https://api.github.com/organizations")
        orgs = []
        while len(orgs) < self.orgs_n:
            response = self.get_api_response(url, per_page=self.per_page)
            # print(response, len(response.json()))
            if 'next' in response.links:
                url = response.links['next']['url']
                orgs.extend(response.json())
            else:
                break
        orgs = orgs[:self.orgs_n]
        repos_url = list(map(lambda x: x['repos_url'], orgs))
        return repos_url

    def repo_mapper(self, repo: dict) -> dict:
        return {'id': repo['id'],
                'org_name': repo['owner']['login'],
                'repo_name': repo['name'],
                'stars_count': repo['stargazers_count']}

    def get_stars_top(self, repos: list) -> list:
        repos.sort(key=lambda x: x['stars_count'], reverse=True)
        return repos[:self.tops_n]

    def repos_worker(self, url: str) -> list:
        response = self.get_api_response(url, per_page=self.per_page)
        repos = list(map(self.repo_mapper, response.json()))
        while 'next' in response.links:
            url = response.links['next']['url']
            response = self.get_api_response(url)
            cur_repos = map(self.repo_mapper, response.json())
            repos.extend(cur_repos)

        return self.get_stars_top(repos)

    def get_top(self):
        repos_url = self.get_orgs_url()
        repos = self.orch.run(worker=self.repos_worker, tasks=repos_url)
        repos = sum(repos, [])
        return self.get_stars_top(repos)


if __name__ == '__main__':
    pass
