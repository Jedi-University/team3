
from git_app.api.requests_sync import RequestsSync
from git_app.githubcred import cred
from git_app.worker.worker_gh_orgs import WorkerGHOrgs
from git_app.worker.worker_gh_repos import WorkerGHRepos

config_orgs_top = {'orgs_n': 2,
                   'tops_n': 20}

# Sync requests
requests = RequestsSync(**cred)

config = {**config_orgs_top,
          'requests': requests}

worker_orgs = WorkerGHOrgs(**config)
worker_repos = WorkerGHRepos(**config)