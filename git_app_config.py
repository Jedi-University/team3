from api.requests_async import RequestsAsync
from api.requests_sync import RequestsSync
from db.db import DB
from db.top import Top
from githubcred import cred
from orch.async_orch import AsyncOrch
from orch.process_orch import ProcessOrch
from orch.seq_orch import SeqOrch
from orch.tread_orch import TreadOrch
from worker.worker_gh_orgs import WorkerGHOrgs
from worker.worker_gh_orgs_async import WorkerGHOrgsAsync
from worker.worker_gh_repos import WorkerGHRepos
from worker.worker_gh_repos_async import WorkerGHReposAsync
from worker.worker_stars_top import WorkerStarsTop

db_path = 'sqlalchemy.db'
db = DB(db_path=db_path, table=Top)

config_orgs_top = {'orgs_n': 2,
                   'tops_n': 20}

# Sync requests
requests = RequestsSync(**cred)


config = {**config_orgs_top,
          'requests': requests}

max_workers = 10

workers = {'orgs': WorkerGHOrgs(**config),
           'repos': WorkerGHRepos(**config),
           'top': WorkerStarsTop(**config)}

# sequentional
# orch = SeqOrch(workers=workers)

# processPool
# orch = ProcessOrch(workers=workers, max_workers=max_workers)

# treadPool
orch = TreadOrch(workers=workers, max_workers=max_workers)


# Async requests
requests = RequestsAsync(**cred)

config = {**config_orgs_top,
          'requests': requests}

workers = {'orgs': WorkerGHOrgsAsync(**config),
           'repos': WorkerGHReposAsync(**config),
           'top': WorkerStarsTop(**config)}

# orch = AsyncOrch(workers=workers)
