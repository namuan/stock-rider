import logging


class ConsoleNotifier:
    def send_notification(self, ticker, packaged_output):
        logging.info("Ticker: {}, {}".format(ticker, packaged_output))


notifier = ConsoleNotifier()
