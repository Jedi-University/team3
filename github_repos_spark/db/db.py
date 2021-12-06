from sqlalchemy import Column, Integer, String, create_engine, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.declarative_base import Base


class DB():

    def __init__(self, table, db_path: str = 'sqlalchemy.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.table = table

        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)

    def delete(self):
        session = self.DBSession()
        session.execute(delete(self.table))
        session.commit()

    def store(self, top: list):
        session = self.DBSession()
        for t in top:
            row = self.table(**t)
            session.add(row)
        session.commit()

    def get(self) -> list:
        session = self.DBSession()
        top = session.query(self.table).all()
        return top
