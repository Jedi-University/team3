from worker.worker_gh import WorkerGH


class WorkerStarsTop(WorkerGH):

    def run(self, repos: list):
        return self.get_stars_top(repos)


if __name__ == '__main__':
    pass
