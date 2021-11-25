from datetime import datetime

from loguru import logger

from git_app_config import db, orch


class App():
    def __init__(self, orch, db):
        self.orch = orch
        self.db = db

    def fetch(self):
        db.delete()
        top = self.orch.run()
        db.store(top=top)

    def show(self):
        top = db.get()

        header = 'id, org_name, repo_name, stars_count'
        result = [f'{t.id}, {t.org_name}, {t.repo_name}, {t.stars_count}'
                  for t in top]
        result = [header, *result]
        result = '\n'.join(result)
        logger.info(result)


if __name__ == '__main__':
    app = App(orch=orch, db=db)
    start_time = datetime.now()
    app.fetch()
    time_delta = datetime.now() - start_time
    logger.info(f'seconds: {time_delta.total_seconds()}')
    app.show()
