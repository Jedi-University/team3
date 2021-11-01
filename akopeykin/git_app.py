from datetime import datetime

from git_app_config import db, ghubdata


class App():
    def __init__(self, ghubdata, db):
        self.ghubdata = ghubdata
        self.db = db

    def fetch(self):
        top = self.ghubdata.get_top()
        db.load(top=top)

    def show(self):
        top = db.get()

        print('id org_name repo_name stars_count')
        for t in top:
            print(t.id, t.org_name, t.repo_name, t.stars_count)


if __name__ == '__main__':
    app = App(ghubdata=ghubdata, db=db)
    start_time = datetime.now()
    app.fetch()
    time_delta = datetime.now() - start_time
    print(f'seconds: {time_delta.total_seconds()}')

    # app.show()
