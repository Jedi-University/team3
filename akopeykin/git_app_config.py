from db.db import DB, Top
from githubcred import cred
# from orch.async_orch import AsyncOrch
from orch.process_orch import ProcessOrch
from orch.seq_orch import SeqOrch
from orch.tread_orch import TreadOrch
from worker.worker_gh_orgs import WorkerGHOrgs
from worker.worker_gh_repos import WorkerGHRepos
from worker.worker_stars_top import WorkerStarsTop

config = {**cred,
          'orgs_n': 200,
          'tops_n': 20}

max_workers = 10

db_path = 'sqlalchemy.db'

workers = [WorkerGHOrgs(**config),
           WorkerGHRepos(**config),
           WorkerStarsTop(**config)]

# orch = SeqOrch(workers=workers)
orch = ProcessOrch(workers=workers, max_workers=max_workers)
# orch = TreadOrch(workers=workers, max_workers=max_workers)
# orch = AsyncOrch(**config)

db = DB(db_path=db_path, table=Top)
