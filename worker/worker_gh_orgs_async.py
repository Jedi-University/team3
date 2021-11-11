from worker.worker_gh_async import WorkerGHAsync


class WorkerGHOrgsAsync(WorkerGHAsync):

    def __init__(self, orgs_n: int, per_page: int = 100,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orgs_n = orgs_n
        self.per_page = per_page

    async def run(self) -> list:
        url = (f"https://api.github.com/organizations")
        response = await self.get_api_response(url,
                                                per_page=self.per_page)
        orgs = response['json']
        while len(orgs) < self.orgs_n and 'url' in response:
            url = response['url']
            response = await self.get_api_response(url,
                                                   per_page=self.per_page)
            orgs.extend(response['json'])
        orgs = orgs[:self.orgs_n]
        repos_url = list(map(lambda x: x['repos_url'], orgs))
        return repos_url
