from sqlalchemy import Column, Integer, String, create_engine, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.declarative_base import Base


class Top(Base):
    __tablename__ = 'top'
    id = Column(Integer, primary_key=True, nullable=False)
    org_name = Column(String(250), nullable=False)
    repo_name = Column(String(250), nullable=False)
    stars_count = Column(Integer, nullable=False)
