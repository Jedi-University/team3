from orch.orch import Orch


class SeqOrch(Orch):

    def run(self) -> list:
        worker_orgs = self.workers['orgs'].run
        worker_repos = self.workers['repos'].run
        worker_top = self.workers['top'].run

        orgs_repos_url = worker_orgs()
        top_repos = [worker_repos(r) for r in orgs_repos_url]
        repos = sum(top_repos, [])
        top = worker_top(repos)
        
        return top
