import logging
from tqdm import tqdm

from krider.stock_data_provider import stock_data_provider
from krider.stock_store import stock_store
from krider.ticker_data import ticker_data
from krider.utils.timing_decorator import timeit


class HistoricalDataDownloader:
    @timeit
    def run_with(self, interval, start_dt, end_dt, stock=None):
        all_tickers = [stock] if stock else ticker_data.load_valid_tickers()
        for ticker in tqdm(all_tickers):
            logging.debug("Scanning stocks between {} and {}".format(start_dt, end_dt))
            try:
                data = stock_data_provider.download(
                    ticker,
                    interval,
                    start_dt.strftime("%Y-%m-%d"),
                    end_dt.strftime("%Y-%m-%d"),
                )
                if not data.empty:
                    stock_store.save(ticker, data)
            except:
                logging.debug(
                    "Something went wrong when processing ticker {}. Continuing ...".format(
                        ticker
                    )
                )

        return "All done."


historical_data_downloader = HistoricalDataDownloader()
