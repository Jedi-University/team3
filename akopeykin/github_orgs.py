from json.decoder import JSONDecodeError

import requests
from sqlalchemy import Column, Integer, String, create_engine, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from githubcred import password, user

# user = ''
# password = ''
DB_PATH = 'sqlalchemy.db'
ORGS_NUMBER = 200
NUMBER_OF_TOP = 20

Base = declarative_base()


class GHub():

    def __init__(self):
        pass

    def get_api_response(self, url, querystring={}) -> requests.Response:
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.request(
            "GET", url, headers=headers,
            params=querystring,
            auth=requests.auth.HTTPBasicAuth(user, password))
        return response

    def get_orgs(self, orgs_number: int = 30):
        url = (f"https://api.github.com/organizations")
        result = []
        while len(result) < orgs_number:
            response = self.get_api_response(url)
            # print(response, len(response.json()))
            url = response.links['next']['url']
            result += response.json()
        return result[:orgs_number]

    def get_repos(self, orgs_number: int = 200):
        orgs = self.get_orgs(orgs_number=orgs_number)
        result = []
        for row in orgs:
            org_name = row['login']
            url = row['repos_url']
            response = self.get_api_response(url)
            repos = response.json()
            res = [{'id': repo['id'],
                    'org_name': org_name,
                    'stars_count': repo['stargazers_count'],
                    'repo_name': repo['name']} for repo in repos]
            result += res
        result.sort(key=lambda x: x['stars_count'], reverse=True)
        return result


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

    def fetch(self, number_of_top: int = 20, orgs_number: int = 200):
        tops = GHub().get_repos(orgs_number=orgs_number)
        tops = tops[:number_of_top]
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
    # pass
    # result = GHub().get_orgs()
    # result = GHub().get_repos()
    gh = GHubSQL(db_path=DB_PATH)
    gh.fetch(number_of_top=NUMBER_OF_TOP, orgs_number=ORGS_NUMBER)
    gh.show()
