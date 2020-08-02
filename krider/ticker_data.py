from pathlib import Path

import pandas as pd


class TickerData:
    def __init__(self):
        self.all_listed_stocks_path = "data/alllisted.txt"
        self.valid_listed_stocks_path = "data/valid_listed.txt"

    @staticmethod
    def extract_ticker_from(line):
        return line.strip().split(",")[0]

    def load_all_tickers(self):
        return self._extract_tickers(self.all_listed_stocks_path)

    def load_valid_tickers(self):
        return self._extract_tickers(self.valid_listed_stocks_path)

    def save_valid_tickers(self, valid_tickers):
        data_file = Path.cwd().joinpath(self.valid_listed_stocks_path)
        data_file.write_text("\n".join(valid_tickers))

    def load_exchange_tickers(self):
        exchanges = [
            ("nasdaq", "nasdaq-listed.csv"),
            ("amex", "amex-listed.csv"),
            ("nyse", "nyse-listed.csv"),
        ]

        exchange_securities = [s for s in self._extract_data(exchanges)]
        return pd.concat(exchange_securities)

    def _extract_data(self, exchanges):
        for exchange, data_file in exchanges:
            df = self._load_from("data/{}".format(data_file))
            df["exchange"] = exchange
            yield df

    def _load_from(self, listing_path):
        securities_file = Path.cwd().joinpath(listing_path)
        return pd.read_csv(securities_file, index_col=["Symbol"])

    def _extract_tickers(self, file_path):
        data_file = Path.cwd().joinpath(file_path)
        with open(data_file) as f:
            return [self.extract_ticker_from(line) for line in f]


ticker_data = TickerData()
