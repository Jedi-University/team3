from loguru import logger
from pyspark.sql import SparkSession

from api.requests_sync import RequestsSync
from db.db import DB
from db.top import Top
from githubcred import cred
from orch.spark_orch import SparkOrch
from worker.worker_gh_orgs import WorkerGHOrgs
from worker.worker_gh_repos import WorkerGHRepos

logger.add('log.log', rotation='0.2 MB',
           retention=1, enqueue=True, diagnose=True)

spark = SparkSession.builder.getOrCreate()

db_path = 'sqlalchemy.db'
db = DB(db_path=db_path, table=Top)

config_orgs_top = {'orgs_n': 200,
                   'tops_n': 20}

# Sync requests
requests = RequestsSync(**cred)

config = {**config_orgs_top,
          'requests': requests}

workers = {'orgs': WorkerGHOrgs(**config),
           'repos': WorkerGHRepos(**config)}

# spark
orch = SparkOrch(spark=spark, workers=workers, **config_orgs_top)
