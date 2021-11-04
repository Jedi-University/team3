from worker.worker_gh import WorkerGH


class WorkerGHOrgs(WorkerGH):

    def __init__(self, orgs_n: int, per_page: int = 100,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orgs_n = orgs_n
        self.per_page = per_page

    def run(self) -> list:
        url = (f"https://api.github.com/organizations")
        orgs = []
        while len(orgs) < self.orgs_n:
            response = self.get_api_response(url, per_page=self.per_page)
            orgs.extend(response.json())
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        orgs = orgs[:self.orgs_n]
        repos_url = list(map(lambda x: x['repos_url'], orgs))
        return repos_url
