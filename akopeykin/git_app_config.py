from githubcred import cred
from githuborgs.db import DB, Top
from githuborgs.githubdata import GHubData
# from githuborgs.orch import PoolOrch, SeqOrch, TreadOrch, AsyncOrch
from orch.seq_orch import SeqOrch
from orch.process_orch import ProcessOrch
from orch.tread_orch import TreadOrch
from orch.async_orch import AsyncOrch

config = {'orgs_n': 20,
          'tops_n': 20,
          'max_workers': 5}

db_path = 'sqlalchemy.db'

# orch = SeqOrch(**config)
# orch = ProcessOrch(**config)
# orch = TreadOrch(**config)
orch = AsyncOrch(**config)

ghubdata = GHubData(orch=orch, **config, **cred)
db = DB(db_path=db_path, table=Top)
