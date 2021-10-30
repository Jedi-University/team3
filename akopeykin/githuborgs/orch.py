from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# from multiprocessing import Pool


class Orch():

    def __init__(self, max_workers: int = 1, **kwargs) -> None:
        self.max_workers = max_workers

    def run(self):
        pass


class SeqOrch(Orch):

    def run(self, worker, tasks: list) -> list:
        return list(map(worker, tasks))


class PoolOrch(Orch):

    def run(self, worker, tasks: list) -> list:
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
        # with Pool(processes=self.max_workers) as pool:
            result = executor.map(worker, tasks)
        return result


class TreadOrch(Orch):

    def run(self, worker, tasks: list) -> list:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            result = executor.map(worker, tasks)
        return result


class AsincOrch(Orch):
    pass
