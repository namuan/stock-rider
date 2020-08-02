import logging

import numpy as np
import pandas as pd
from pandas import DataFrame

from krider.notifications.console_notifier import notifier
from krider.stock_store import stock_store
from krider.ticker_data import ticker_data
from krider.utils.timing_decorator import timeit

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class VolumeAnalysisTask:
    @timeit
    def run_with(self, period):
        valid_tickers = [
            ticker for ticker in ticker_data.load_valid_tickers()
            if ticker == "KODK"
        ]
        for ticker in valid_tickers:
            logging.debug("Running analysis on {}".format(ticker))
            selected_data: DataFrame = stock_store.data_for_ticker(ticker, period)
            if selected_data.empty:
                continue

            if self._if_anomaly_found(selected_data):
                # self._back_test_anomalies(selected_data)
                packaged_output = self._prepare_output(selected_data.iloc[0])
                notifier.send_notification(ticker, packaged_output)

        return "All done"

    def _back_test_anomalies(self, df):
        mean = np.mean(df["Volume"])
        df["Volume_Activity"] = df["Volume"] > (10 * mean)
        logging.debug(df.where(df["Volume_Activity"] == True).dropna())

    def _if_anomaly_found(self, df):
        mean = np.mean(df["Volume"])
        previous_session_vol = df["Volume"].iloc[0]
        return previous_session_vol > (10 * mean)

    def _prepare_output(self, df):
        return df


volume_analysis_task = VolumeAnalysisTask()
