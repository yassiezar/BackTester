import sqlalchemy as db
import pandas as pd

from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime


Base = declarative_base()


class Database:
    def __init__(self):
        self.DB_TYPE = 'sqlite'
        self.DB_USER = 'jaycee'
        self.DB_PASSWORD = 'jaycee'
        self.DB_HOST = 'localhost'
        self.DB_NAME = 'db.db'
        self.DEBUG = True

        if self.DB_TYPE == 'sqlite':
            self.engine = db.create_engine('{}:///{}'.format(self.DB_TYPE, self.DB_NAME), echo=self.DEBUG)
        elif self.DB_TYPE == 'mysql':
            self.engine = db.create_engine('{}://{}:{}@{}/{}'.format(self.DB_TYPE, self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME), echo=self.DEBUG)

        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

    def fetch_or_add_stock(self, session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()

        if instance:
            print('Stock exists: {}'.format(instance))
            return instance
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        print('Added stock: {}'.format(instance))
        return instance

    def update_stock_entries(self, session, stock, data, to=None):
        for row in data.itertuples():
            date = row[1].date()#.strftime("%Y-%B-%d")
            close = float(row[5])
            session.add(StockEntry(stock=stock, date=date, close=close))
        stock.available_from = data['dates'].iloc[-1].date()
        stock.available_to = data['dates'].iloc[0].date()
        session.commit()


class StockEntry(Base):
        __tablename__ = 'stock_entries'

        id = Column(Integer, primary_key=True)
        date = Column(Date)
        close = Column(Float(precision=2))
        stock_id = Column(Integer, ForeignKey('stocks.id'))

        stock = relationship('Stock')#, back_populates='stock_entries')

        def __repr__(self):
            return '<StockEntry({}:{} - ${} ({}))>'.format(self.stock.market, self.stock.ticker, self.close, self.date)


class Stock(Base):
        __tablename__ = 'stocks'

        id = Column(Integer, primary_key=True)
        full_name = Column(String)
        market = Column(String)
        ticker = Column(String)
        available_from = Column(Date)
        available_to = Column(Date)

        def __repr__(self):
            return '<Stock({}:{} ({}) Available: {} - {}>'.format(self.market, self.ticker, self.full_name, self.available_from, self.available_to)
