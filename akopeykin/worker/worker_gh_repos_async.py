from worker.worker_gh_async import WorkerGHAsync


class WorkerGHReposAsync(WorkerGHAsync):

    def __init__(self, per_page: int = 100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.per_page = per_page

    def repo_mapper(self, repo: dict) -> dict:
        return {'id': repo['id'],
                'org_name': repo['owner']['login'],
                'repo_name': repo['name'],
                'stars_count': repo['stargazers_count']}

    async def run(self, url: str) -> list:
        response = await self.get_api_response(url, per_page=self.per_page)
        repos = list(map(self.repo_mapper, response['json']))
        while 'url' in response:
            url = response['url']
            response = await self.get_api_response(url)
            cur_repos = map(self.repo_mapper, response['json'])
            repos.extend(cur_repos)
        repos = self.get_stars_top(repos)
        return repos


if __name__ == '__main__':
    pass
