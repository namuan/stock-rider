import yfinance
from time import sleep


class StockDataProvider:
    def download(self, ticker, interval, start, end):
        print("Requesting ticker {}".format(ticker))
        sleep(0.5)
        opts = dict(
            tickers=ticker, interval=interval, start=start, end=end, progress=False
        )
        return yfinance.download(**opts)

    def download_for_period(self, ticker, period, interval):
        sleep(0.1)
        opts = dict(tickers=ticker, interval=interval, period=period, progress=False)
        return yfinance.download(**opts)

    def check(self, ticker):
        return self.download_for_period(ticker, "1d", "1d")


stock_data_provider = StockDataProvider()
