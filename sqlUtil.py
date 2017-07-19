from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

#ORM基类
Base = declarative_base()

def initDB():
    engine = create_engine('sqlite:///alphabull.db')
    dbSession = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
    Base.metadata.create_all(bind=engine)
    return dbSession