from concurrent.futures import ProcessPoolExecutor

from orch.orch import Orch


class ProcessOrch(Orch):

    def run(self) -> list:
        worker_orgs = self.workers['orgs'].run
        worker_repos = self.workers['repos'].run
        worker_top = self.workers['top'].run

        orgs_repos_url = worker_orgs()
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            top_repos = executor.map(worker_repos, orgs_repos_url)
        repos = sum(top_repos, [])
        top = worker_top(repos)

        return top
