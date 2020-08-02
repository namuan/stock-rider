import logging
from tqdm import tqdm

from krider.stock_data_provider import stock_data_provider
from krider.ticker_data import ticker_data
from krider.utils.timing_decorator import timeit


class FilterValidTickers:
    @timeit
    def run_with(self):
        all_tickers = ticker_data.load_all_tickers()
        valid_tickers = []
        for ticker in tqdm(all_tickers):
            data = stock_data_provider.check(ticker)
            if not data.empty:
                logging.debug(">>> Adding {} to valid tickers".format(ticker))
                valid_tickers.append(ticker)

        ticker_data.save_valid_tickers(valid_tickers)
        return "All done."


filter_valid_tickers = FilterValidTickers()
