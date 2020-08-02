import logging

from pandas import DataFrame
from tqdm import tqdm

from krider.stock_data_provider import stock_data_provider
from krider.stock_store import stock_store
from krider.ticker_data import ticker_data
from krider.utils.timing_decorator import timeit
from datetime import datetime

class HistoricalDataDownloader:

    def _download_and_save_ticker_data(self, ticker, ticker_exchange, interval, start_dt, end_dt):
        logging.info("Scanning {} between {} and {}".format(ticker, start_dt, end_dt))
        try:
            data = stock_data_provider.download_between_dates(
                ticker,
                interval,
                start_dt.strftime("%Y-%m-%d"),
                end_dt.strftime("%Y-%m-%d"),
            )
            if not data.empty:
                data["Exchange"] = ticker_exchange
                stock_store.save(ticker, data)
        except Exception as e:
            logging.warning(
                "Something went wrong when processing ticker {}. Continuing ...".format(
                    ticker
                ), e


            )

    @timeit
    def run_with(self, interval, start_dt, end_dt, stocks=None):
        exchange_tickers: DataFrame = ticker_data.load_exchange_tickers()

        if stocks:
            selected_stocks = stocks.split(",")
            exchange_tickers = exchange_tickers[exchange_tickers.index.isin(selected_stocks)]

        for ticker, ticker_df in tqdm(exchange_tickers.iterrows()):
            ticker_exchange = ticker_df["exchange"]
            start_dt = stock_store.find_start_time(ticker, start_dt)
            end_dt = end_dt if end_dt else datetime.now()
            self._download_and_save_ticker_data(ticker, ticker_exchange, interval, start_dt, end_dt)

        return "All done."


historical_data_downloader = HistoricalDataDownloader()
