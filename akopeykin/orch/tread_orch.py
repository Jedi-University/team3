from concurrent.futures import ThreadPoolExecutor

from orch.orch import Orch


class TreadOrch(Orch):

    def run(self, worker, tasks: list) -> list:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            result = executor.map(worker, tasks)
        return result
