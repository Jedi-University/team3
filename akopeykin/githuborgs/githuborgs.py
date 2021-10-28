from multiprocessing import Pool

import requests
from sqlalchemy import Column, Integer, String, create_engine, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from githubcred import cred

# cred = {'user': '',
#         'password': ''}

DB_PATH = 'sqlalchemy.db'
ORGS_N = 200
TOPS_N = 20
PROCESSES = 20

Base = declarative_base()


class GHub():

    def __init__(self, tops_n: int, orgs_n: int,
                 user: str, password: str, per_page: int = 100,
                 processes: int = 2):
        self.per_page = per_page
        self.tops_n = tops_n
        self.orgs_n = orgs_n
        self.user = user
        self.password = password
        self.processes = processes

    def get_api_response(self, url, **kwargs) -> requests.Response:
        params = kwargs
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.request(
            "GET", url, headers=headers,
            params=params,
            auth=requests.auth.HTTPBasicAuth(self.user, self.password))
        return response

    def get_orgs_url(self):
        url = (f"https://api.github.com/organizations")
        orgs = []
        while len(orgs) < self.orgs_n:
            response = self.get_api_response(url, per_page=self.per_page)
            # print(response, len(response.json()))
            if 'next' in response.links:
                url = response.links['next']['url']
                orgs.extend(response.json())
            else:
                break
        orgs = orgs[:self.orgs_n]
        repos_url = list(map(lambda x: x['repos_url'], orgs))
        return repos_url

    def repo_mapper(self, repo: dict) -> dict:
        return {'id': repo['id'],
                'org_name': repo['owner']['login'],
                'repo_name': repo['name'],
                'stars_count': repo['stargazers_count']}

    def get_repos_sec(self):
        repos_url = self.get_orgs_url()
        top_repos = []
        for url in repos_url:
            response = self.get_api_response(url, per_page=self.per_page)
            repos = response.json()
            repos_info = list(map(self.repo_mapper, repos))
            while 'next' in response.links:
                url = response.links['next']['url']
                response = self.get_api_response(url)
                cur_repos = response.json()
                cur_repos_info = map(self.repo_mapper, cur_repos)
                repos_info.extend(cur_repos_info)

            top_repos.extend(repos_info)
            top_repos.sort(key=lambda x: x['stars_count'], reverse=True)
            top_repos = top_repos[:self.tops_n]

        return top_repos

    def repos_worker(self, url):
        response = self.get_api_response(url, per_page=self.per_page)
        repos = response.json()
        repos_info = list(map(self.repo_mapper, repos))
        while 'next' in response.links:
            url = response.links['next']['url']
            response = self.get_api_response(url)
            cur_repos = response.json()
            cur_repos_info = map(self.repo_mapper, cur_repos)
            repos_info.extend(cur_repos_info)
        repos_info.sort(key=lambda x: x['stars_count'], reverse=True)
        top_repos = repos_info[:self.tops_n]
        return top_repos

    def get_repos(self):
        repos_url = self.get_orgs_url()
        with Pool(processes=self.processes) as pool:
            result = pool.map(self.repos_worker, repos_url)

        # top_repos = reduce(lambda x,y: x+y, result)
        top_repos = sum(result, [])
        top_repos.sort(key=lambda x: x['stars_count'], reverse=True)
        top_repos = top_repos[:self.tops_n]

        return top_repos


class Top(Base):
    __tablename__ = 'top'
    id = Column(Integer, primary_key=True, nullable=False)
    org_name = Column(String(250), nullable=False)
    repo_name = Column(String(250), nullable=False)
    stars_count = Column(Integer, nullable=False)


class GHubSQL():

    def __init__(self, db_path: str = 'sqlalchemy.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)

    def fetch(self, **kwargs):
        tops = GHub(**kwargs).get_repos()
        session = self.DBSession()
        session.execute(delete(Top))

        for top in tops:
            row = Top(**top)
            session.add(row)
        session.commit()

    def show(self):
        session = self.DBSession()

        tops = session.query(Top).all()
        print('id org_name repo_name stars_count')
        for top in tops:
            print(top.id, top.org_name, top.repo_name, top.stars_count)


if __name__ == '__main__':
    gh = GHubSQL(db_path=DB_PATH)
    gh.fetch(tops_n=TOPS_N, orgs_n=ORGS_N, processes=PROCESSES, **cred)
    gh.show()
