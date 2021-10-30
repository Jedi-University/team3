from githubcred import cred
from githuborgs.db import DB, Top
from githuborgs.githubdata import GHubData
from githuborgs.orch import PoolOrch, SeqOrch, TreadOrch

config = {'orgs_n': 200,
          'tops_n': 20,
          'max_workers': 20}

db_path = 'sqlalchemy.db'

# orch = SeqOrch(**config)
orch = PoolOrch(**config)
# orch = TreadOrch(**config)

ghubdata = GHubData(orch=orch, **config, **cred)
db = DB(db_path=db_path, table=Top)
