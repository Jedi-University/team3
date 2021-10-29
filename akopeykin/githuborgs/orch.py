from multiprocessing import Pool


class Orch():
    def run(self):
        pass


class SeqOrch(Orch):
    def __init__(*args, **kwargs) -> None:
        pass

    def run(self, worker, tasks: list) -> list:
        return list(map(worker, tasks))


class PoolOrch(Orch):
    def __init__(self, processes: int = 1, **kwargs) -> None:
        self.processes = processes

    def run(self, worker, tasks: list) -> list:
        with Pool(processes=self.processes) as pool:
            result = pool.map(worker, tasks)
        return result


class TreadOrch(Orch):
    pass


class AsincOrch(Orch):
    pass
