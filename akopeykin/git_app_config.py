from githubcred import cred
from githuborgs.db import DB, Top
from githuborgs.githubdata import GHubData
from githuborgs.orch import PoolOrch, SeqOrch

config = {'orgs_n': 200,
          'tops_n': 20,
          'processes': 20}

db_path = 'sqlalchemy.db'

orch = PoolOrch(**config)
# orch = SeqOrch(**config)

ghubdata = GHubData(orch=orch, **config, **cred)
db = DB(db_path=db_path, table=Top)
