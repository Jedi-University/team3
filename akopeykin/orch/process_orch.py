from concurrent.futures import ProcessPoolExecutor

from orch.orch import Orch


class ProcessOrch(Orch):

    def run(self, worker, tasks: list) -> list:
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            result = executor.map(worker, tasks)
        return result
