from sqlalchemy import Column, Integer, String, create_engine, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Top(Base):
    __tablename__ = 'top'
    id = Column(Integer, primary_key=True, nullable=False)
    org_name = Column(String(250), nullable=False)
    repo_name = Column(String(250), nullable=False)
    stars_count = Column(Integer, nullable=False)


class DB():

    def __init__(self, db_path: str = 'sqlalchemy.db', table: Base = Top):
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.table = table

        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)

    def del_table(self):
        session = self.DBSession()
        session.execute(delete(self.table))
        session.commit()

    def load(self, top: list):
        session = self.DBSession()
        session.execute(delete(self.table))

        for t in top:
            row = self.table(**t)
            session.add(row)
        session.commit()

    def get(self) -> list:
        session = self.DBSession()
        top = session.query(self.table).all()
        return top


if __name__ == '__main__':
    pass
