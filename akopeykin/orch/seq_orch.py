from orch.orch import Orch


class SeqOrch(Orch):

    def run(self) -> list:
        orgs_repos_url = self.workers[0].run()
        top_repos = [self.workers[1].run(r) for r in orgs_repos_url]
        repos = sum(top_repos, [])
        top = self.workers[2].run(repos)
        return top
