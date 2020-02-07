import sqlalchemy as db

from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_TYPE = 'sqlite'
DB_USER = 'jaycee'
DB_PASSWORD = 'jaycee'
DB_HOST = 'localhost'
DB_NAME = 'db.db'

DEBUG = True

if DB_TYPE == 'sqlite':
    engine = db.create_engine('{}:///{}'.format(DB_TYPE, DB_NAME), echo=DEBUG)
elif DB_TYPE == 'mysql':
    engine = db.create_engine('{}://{}:{}@{}/{}'.format(DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME), echo=DEBUG)

if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

class StockEntry(Base):
    __tablename__ = 'stock_entries'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    price = Column(Float(precision=2))
    stock_id = Column(Integer, ForeignKey('stocks.id'))

    stock = relationship('Stock', back_populates='stock_entries')

    def __repr__(self):
        return '<StockEntry({}:{} - ${} ({}))>'.format(self.stock.market, self.stock.ticker, self.price, self.date)

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    market = Column(String)
    ticker = Column(String)
    available_from = Column(Date)
    available_to = Column(Date)

    def __repr__(self):
        return '<Stock({}:{} ({}) Available: {} - {}>'.format(self.market, self.ticker, self.full_name, self.available_from, available_to)

Session = sessionmaker(bind=engine)
