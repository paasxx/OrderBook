from core.interfaces import TradeManagerInterface
from utils.helpers import print_line
from utils.logger import logger


class TradeManager(TradeManagerInterface):

    def __init__(self):
        self.trades = []

    def record_trade(self, trade):
        self.trades.append(trade)
        logger.info(f"Trade recorded: {trade}")
        print_line()

    def list_trades(self):

        if self.trades:
            logger.info("Trade List:")
            for index, trade in enumerate(self.trades):
                logger.info(f"index: {index}, trade: {trade}")
                print_line()

        else:
            logger.info(f"Trade List are empty!")
            print_line()
