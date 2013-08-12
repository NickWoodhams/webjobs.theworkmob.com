from app import app
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


__all__ = ['db_session', 'City', 'Post']

engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    convert_unicode=True,
    pool_recycle=3600,
)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    post_id = Column(BigInteger(12))
    title = Column(String(160))
    body = Column(Text())
    email = Column(Text())
    timestamp = Column(DateTime)
    url = Column(String(160))


Base.metadata.create_all(bind=engine)
