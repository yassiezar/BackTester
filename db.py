import sqlalchemy as db

import datetime
import urllib.request
import pandas as pd

from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_TYPE = 'sqlite'
DB_USER = 'jaycee'
DB_PASSWORD = 'jaycee'
DB_HOST = 'localhost'
DB_NAME = 'db.db'

API_KEY = '9EI4JOJQJD1WR707'

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
    close = Column(Float(precision=2))
    stock_id = Column(Integer, ForeignKey('stocks.id'))

    stock = relationship('Stock', back_populates='stock_entries')

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
        return '<Stock({}:{} ({}) Available: {} - {}>'.format(self.market, self.ticker, self.full_name, self.available_from, available_to)

Session = sessionmaker(bind=engine)

def download():
    market = 'JOH'
    ticker = 'AGL'
    from_date = datetime.date(2020, 1, 1)
    to_date = datetime.date.today().strftime("%Y-%m-%d")

    if DEBUG:
        print('Downloading {}:{} from Alpha Vantage API'.format(market, ticker), end='', flush=True)
    data = download_from_alpha_vantage(market, ticker, to_date)

    print(data['dates'])
    data = data[(data['dates'] <= to_date) & (data['dates'] >= pd.to_datetime(from_date))]
    print(data)

def download_from_alpha_vantage(market, ticker, date):
    data = {'dates': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
    csv = urllib.request.urlopen(url(market, ticker, date)).readlines()
    for line in csv[1:]:
        datum = line.decode("ASCII").strip().split(',')
        data['dates'].append(datum[0])
        data['open'].append(datum[1])
        data['high'].append(datum[2])
        data['low'].append(datum[3])
        data['close'].append(datum[4])
        data['volume'].append(datum[5])
    data = pd.DataFrame(data=data, columns=data.keys())
    data['dates'] = pd.to_datetime(data['dates'], format="%Y-%m-%d")

    return data

def url(market, ticker, date):
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        #https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=demo
        base = 'https://www.alphavantage.co/query?'
        query = '{}.{}'.format(ticker.upper(), market.upper())
        enddate = '{}%20{},%20{}'.format(dt.strftime('%b'), dt.strftime('%d'), dt.strftime('%Y'))
        output = 'csv'

        url = '{}function={}&symbol={}&outputsize={}&apikey={}&datatype={}'.format(base, 'TIME_SERIES_DAILY', query, 'compact', API_KEY, output)
        print(url)

        return url

download()
