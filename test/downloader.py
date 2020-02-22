from downloader import Downloader

class DataFetcher:
    downloader = Downloader()
    data = downloader.download_series('agl', 'joh')
    print(data)

df = DataFetcher()
