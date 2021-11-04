import asyncio

from orch.orch import Orch


class AsyncOrch(Orch):

    def run(self) -> list:
        top = asyncio.run(self.async_run())
        return top

    async def async_run(self) -> list:
        worker_orgs = self.workers['orgs'].run
        worker_repos = self.workers['repos'].run
        worker_top = self.workers['top'].run

        orgs_repos_url = await worker_orgs()

        ## not concurrent
        # top_repos = [await worker_repos(r) for r in orgs_repos_url]
        # concurrent
        tasks = [worker_repos(r) for r in orgs_repos_url]
        top_repos = await asyncio.gather(*tasks)

        repos = sum(top_repos, [])
        top = worker_top(repos)

        return top
