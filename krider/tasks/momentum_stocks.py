import logging

import pandas as pd
from pandas import DataFrame
from tqdm import tqdm

from krider.bot_config import config
from krider.notifications.console_notifier import console_notifier
from krider.ticker_data import ticker_data
from krider.utils.report_generator import report_generator
from krider.utils.timing_decorator import timeit

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


class MomentumStocksTask:
    @timeit
    def run_with(self, stocks=None):
        exchange_tickers: DataFrame = ticker_data.load_exchange_tickers_or_given_stocks(
            stocks
        )

        collective_post = []

        for ticker, ticker_df in tqdm(
                exchange_tickers.iterrows(), desc=f"Running Momentum stocks finder"
        ):
            logging.debug("Running analysis on {}".format(ticker))

        logging.info(
            "Total {} stocks found ".format(len(collective_post))
        )

        if collective_post:
            content = dict(
                title="[Daily] Momentum stocks",
                flair_id=config("PRICE_MOMENTUM"),
                body=report_generator.wrap_in_banner(collective_post),
            )
            console_notifier.send_notification(content)
        return "All done"


momentum_stocks_task = MomentumStocksTask()
