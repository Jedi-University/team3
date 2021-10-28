from githubcred import cred
from githuborgs.githuborgs import GHubSQL

# cred = {'user': '',
#         'password': ''}
DB_PATH = 'sqlalchemy.db'
ORGS_N = 20
TOPS_N = 20
PROCESSES = 20


if __name__ == '__main__':
    gh = GHubSQL(db_path=DB_PATH)
    gh.fetch(tops_n=TOPS_N, orgs_n=ORGS_N, processes=PROCESSES, **cred)
    gh.show()
