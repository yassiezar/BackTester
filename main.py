#!/usr/bin/python3

from db import Database, Stock, StockEntry
from downloader import Downloader

import datetime

if __name__ == '__main__':
    ticker = 'AGL'
    market = 'JOH'


    db_handler = Database()
    session = db_handler.Session()
    stock = db_handler.fetch_or_add_stock(session, Stock, full_name="Anglo Gold", ticker=ticker, market=market)

    downloader = Downloader(db_handler)

    # download all records if data not available, else update
    if stock.available_from is None:
        print("Updating")
        data = downloader.download_series(stock)
        db_handler.update_stock_entries(session, stock, data)
    elif stock.available_to is None or (stock.available_to + datetime.timedelta(days=1)) < datetime.date.today():
        print("Out of date")
        data = downloader.download_series(stock, to_date=datetime.date.today().strftime("%Y-%m-%d"))
        db_handler.update_stock_entries(session, stock, data)
    else:
        print("up to date, exiting")
