import logging

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError


class StockStore:
    def __init__(self):
        db_engine = create_engine("sqlite:///stockstore.db", echo=False)
        self.db_connection = db_engine.connect()

    def save(self, ticker, data: DataFrame):
        self._create_table_if_required(ticker)
        try:
            data.to_sql(
                ticker,
                self.db_connection,
                if_exists="append",
                index=True,
                index_label="Datetime",
            )
        except IntegrityError as e:
            logging.debug("Unable to save data", e)

        logging.debug("Saving ticker: {} with data: {}".format(ticker, data.shape))

    def data_for_ticker(self, ticker, period):
        sql = f"""
        select * from \"{ticker}\" order by Datetime desc limit {period};
        """
        try:
            pd_sql = pd.read_sql(sql, self.db_connection)
            return pd.DataFrame(pd_sql)
        except OperationalError as e:
            logging.debug("Error when reading data for {} - {}".format(ticker, e.args[0]))
            return pd.DataFrame()

    def _create_table_if_required(self, ticker):
        self.db_connection.execute(
            f"""
        CREATE TABLE IF NOT EXISTS "{ticker}" (
            "Datetime" TIMESTAMP PRIMARY KEY, 
            "Open" FLOAT, 
            "High" FLOAT, 
            "Low" FLOAT, 
            "Close" FLOAT, 
            "Adj Close" FLOAT, 
            "Volume" BIGINT,
            "Exchange" TEXT
        )
        """
        )


stock_store = StockStore()
