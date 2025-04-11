from utils.logger import logger
from core.interfaces import OrderBookInterface, TradeManagerInterface, MatchingStrategy
from core.orders import LimitOrder
import heapq
from utils.helpers import print_line


class HeapOrderBook(OrderBookInterface):
    def __init__(
        self,
        asset,
        trade_manager: TradeManagerInterface,
        strategies: dict[str, MatchingStrategy],
    ):
        self.asset = asset
        self.buy_orders = []
        self.sell_orders = []
        self.trade_manager = trade_manager
        self.strategies = strategies
        self.order_map = {}  # Dicionário para armazenar ordens pelo ID

    def addOrder(self, order_type, order):

        self.order_map[order.order_id] = order

        if isinstance(order, LimitOrder):

            if order.order_side == "buy":
                heapq.heappush(self.buy_orders, order)

            elif order.order_side == "sell":
                heapq.heappush(self.sell_orders, order)

        if order_type in self.strategies:
            logger.info(f"Placing order {order_type}: {order}")
            print_line()
            self.strategies[order_type].match(self, order)

    def removeOrder(self, order_id: int):
        if order_id in self.order_map:
            self.order_map[order_id].quantity = 0
            del self.order_map[order_id]
            self.cleanHeap()

    def cleanHeap(self):
        """Remove ordens inválidas do topo da heap"""
        while self.buy_orders and self.buy_orders[0].quantity == 0:
            heapq.heappop(self.buy_orders)
        while self.sell_orders and self.sell_orders[0].quantity == 0:
            heapq.heappop(self.sell_orders)

    def getAskOrder(self):
        if self.sell_orders:
            logger.info(f"Ask: {self.sell_orders[0].price}")
            print_line()
            return self.sell_orders[0].price
        else:
            logger.info("Ask Book is empty.")
            print_line()

    def getBidOrder(self):
        if self.buy_orders:
            logger.info(f"Bid: {self.buy_orders[0].price}")
            print_line()
            return self.buy_orders[0].price
        else:
            logger.info("Bid Book is empty.")
            print_line()

    def listAsk(self, depth: int):
        """List first (depth) orders in the Ask order book"""
        asks = heapq.nsmallest(depth, self.sell_orders)
        if asks:
            logger.info("Ask Orders:")
            for order in reversed(asks):
                logger.info(
                    f"Order ID:{order.order_id}, Price: {order.price}, Qty: {order.quantity}"
                )
                print_line()
        else:
            logger.info("No Ask Orders Available.")
            print_line()

    def listBid(self, depth: int):
        "List first (depth) orders in the Bid order book."
        bids = heapq.nlargest(depth, self.buy_orders)
        if bids:
            logger.info("Bid Orders:")
            for order in reversed(bids):
                logger.info(
                    f"Order ID: {order.order_id}, Price: {order.price}, Qty: {order.quantity}"
                )
                print_line()
        else:
            logger.info("No Bid orders Available.")
            print_line()