from concurrent.futures import ProcessPoolExecutor

from orch.orch import Orch


class ProcessOrch(Orch):

    def run(self) -> list:
        orgs_repos_url = self.workers[0].run()
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            top_repos = executor.map(self.workers[1].run, orgs_repos_url)
        repos = sum(top_repos, [])
        top = self.workers[2].run(repos)
        return top

