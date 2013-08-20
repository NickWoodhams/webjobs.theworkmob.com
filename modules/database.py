from config import app
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import types


__all__ = ['db_session', 'Base', 'engine', 'City', 'Post', 'Update']

engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    convert_unicode=True,
    pool_recycle=3600,
    echo=False,
)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)


class tsvector(types.TypeDecorator):
    impl = types.UnicodeText


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    post_id = Column(BigInteger(12))
    title = Column(tsvector)
    title_tsv = Column(String(160))
    body = Column(Text())
    body_tsv = Column(tsvector)
    email = Column(Text())
    timestamp = Column(DateTime)
    url = Column(String(160))


class Update(Base):
    __tablename__ = 'update'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)


Base.metadata.create_all(bind=engine)
