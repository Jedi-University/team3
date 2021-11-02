
class GHubDataAsync():

    def __init__(self, tops_n: int, orgs_n: int,
                 user: str, password: str,
                 orch: Orch, per_page: int = 100, **kwargs):
        self.per_page = per_page
        self.tops_n = tops_n
        self.orgs_n = orgs_n
        self.user = user
        self.password = password
        self.orch = orch


def repos_worker(self, url: str) -> list:
    response = self.get_api_response(url, per_page=self.per_page)
    repos = list(map(self.repo_mapper, response.json()))
    while 'next' in response.links:
        url = response.links['next']['url']
        response = self.get_api_response(url)
        cur_repos = map(self.repo_mapper, response.json())
        repos.extend(cur_repos)

    return self.get_stars_top(repos)

async def async_worker(session, url):
# async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


    while True:
        task = await queue_in.get()
        print(f'{name} task {task}')
        await asyncio.sleep(0)
        r = worker(task)
        queue_out.put_nowait(r)
        queue_in.task_done()
