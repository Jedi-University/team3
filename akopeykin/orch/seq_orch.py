from orch.orch import Orch


class SeqOrch(Orch):

    def run(self, worker, tasks: list) -> list:
        return list(map(worker, tasks))
