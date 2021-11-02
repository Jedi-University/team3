class Orch():

    def __init__(self, workers: list, max_workers: int = 1,
                 *args, **kwargs) -> None:
        self.workers = workers
        self.max_workers = max_workers

    def run(self):
        pass
