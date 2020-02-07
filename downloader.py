import datetime
import urllib.request

import pandas as pd


DEBUG = True
API_KEY = '9EI4JOJQJD1WR707'

def download():
    market = 'JOH'
    ticker = 'AGL'
    from_date = datetime.date(2020, 1, 1)
    to_date = datetime.date.today().strftime("%Y-%m-%d")

    if DEBUG:
        print('\nDownloading {}:{} from Alpha Vantage API'.format(market, ticker), end='', flush=True)
    data = download_from_alpha_vantage(market, ticker, to_date)

    print(data['dates'])
    data = data[(data['dates'] <= pd.to_datetime(to_date)) & (data['dates'] >= pd.to_datetime(from_date))]
    print(data)

def download_from_alpha_vantage(market, ticker, date):
    data = {'dates': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
    csv = urllib.request.urlopen(alpha_vantage_url(market, ticker, date)).readlines()
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

def alpha_vantage_url(market, ticker, date):
    """
    TODO: Provisions ofr JSON format
    """
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    base = 'https://www.alphavantage.co/query?'
    query = '{}.{}'.format(ticker.upper(), market.upper())
    enddate = '{}%20{},%20{}'.format(dt.strftime('%b'), dt.strftime('%d'), dt.strftime('%Y'))
    output = 'csv'

    url = '{}function={}&symbol={}&outputsize={}&apikey={}&datatype={}'.format(base, 'TIME_SERIES_DAILY', query, 'compact', API_KEY, output)
    print(url)

    return url

download()
