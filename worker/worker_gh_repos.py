from worker.worker_gh import WorkerGH


class WorkerGHRepos(WorkerGH):

    def __init__(self, per_page: int = 100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.per_page = per_page

    def repo_mapper(self, repo: dict) -> dict:
        return {'id': repo['id'],
                'org_name': repo['owner']['login'],
                'repo_name': repo['name'],
                'stars_count': repo['stargazers_count']}

    def run(self, url: str) -> list:
        response = self.get_api_response(url, per_page=self.per_page)
        repos = list(map(self.repo_mapper, response.json()))
        while 'next' in response.links:
            url = response.links['next']['url']
            response = self.get_api_response(url)
            cur_repos = map(self.repo_mapper, response.json())
            repos.extend(cur_repos)
        repos = self.get_stars_top(repos)
        return repos
