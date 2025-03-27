import heapq
from datetime import datetime
from abc import ABC, abstractmethod


# 4️⃣ Interface Segregation Principle (ISP)
# O TradeManagerInterface obriga todas as implementações a terem record_trade e list_trades. Se tivermos um TradeStorage que só armazena mas não lista trades, ele será forçado a implementar um método inútil.
# Sugestão: Criar interfaces menores:

# class TradeRecorder(ABC):
#     @abstractmethod
#     def record_trade(self, trade):
#         pass

# class TradeLister(ABC):
#     @abstractmethod
#     def list_trades(self):
#         pass


# trocar tudo por logging

# import logging
# logger = logging.getLogger(__name__)

# # Substituir prints por:
# logger.info(f"Cancelando ordem {new_order.order_id} por falta de liquidez.")


class AbstractOrder(ABC):
    def __init__(self, order_id: int, quantity: int, order_side: str, asset: str):
        self.order_id = order_id
        self.quantity = quantity
        self.order_side = order_side
        self.asset = asset
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def validate(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be bigger than zero!")

    def __repr__(self):
        return f"Order: {self.order_id}, qty: {self.quantity}, side: {self.order_side}, asset: {self.asset}"

    def __lt__(self, other):
        if not isinstance(other, AbstractOrder):
            return NotImplemented  # Avoid invalid comparisons
        return self.timestamp < other.timestamp


class BaseOrder(AbstractOrder):
    def __init__(
        self,
        order_id: int,
        quantity: int,
        order_side: str,
        asset: str,
        partial_fill_behavior: str,
    ):
        super().__init__(order_id, quantity, order_side, asset)
        self.partial_fill_behavior = partial_fill_behavior


class PricedOrder(AbstractOrder):
    def __init__(self, order_id, price, quantity, order_side, asset):
        super().__init__(order_id, quantity, order_side, asset)
        self.price = price

    def __repr__(self):
        return f"Order: {self.order_id}, price: {self.price} qty: {self.quantity}, side: {self.order_side}, asset: {self.asset}"

    def __lt__(self, other):
        if not isinstance(other, PricedOrder):
            return NotImplemented  # Avoid invalid comparisons
        if self.price == other.price:
            return self.timestamp < other.timestamp
        return (
            self.price > other.price
            if self.order_side == "buy"
            else self.price < other.price
        )


class LimitOrder(PricedOrder):

    def __init__(self, order_id, price, quantity, order_side, asset):
        super().__init__(order_id, price, quantity, order_side, asset)


class MarketOrder(BaseOrder):

    def __init__(
        self, order_id, quantity, order_side, asset, partial_fill_behavior="cancel"
    ):
        super().__init__(order_id, quantity, order_side, asset, partial_fill_behavior)


class ConvertibleMarketOrder(MarketOrder):

    def convert_to_limit(self, price):
        """Convert order to limit if needed, as a market order
        that has to be hanged in book because of lacking liquidity"""

        return LimitOrder(
            self.order_id, price, self.quantity, self.order_side, self.asset
        )


class OrderFactory:

    order_types = {}

    @classmethod
    def register_order_type(cls, order_type, order_class):
        cls.order_types[order_type] = order_class

    @classmethod
    def create_order(cls, order_type, *args, **kwargs):
        if order_type not in cls.order_types:
            raise ValueError(f"Order type: '{order_type}' not registered!")
        return cls.order_types[order_type](*args, **kwargs)


class TradeManagerInterface(ABC):
    @abstractmethod
    def record_trade(self, trade):
        pass

    @abstractmethod
    def list_trades(self):
        pass


class TradeManager(TradeManagerInterface):
    def __init__(self):
        self.trades = []

    def record_trade(self, trade):
        self.trades.append(trade)
        print(f"Trade recorde: {trade}")
        print_line()

    def list_trades(self):

        if self.trades:
            print("Trade List:")
            for index, trade in enumerate(self.trades):
                print(index, trade)
                print_line()

        else:
            print(f"Trade List are empty!")
            print_line()


class OrderBookInterface(ABC):

    @abstractmethod
    def addOrder(self, order_type, order) -> None:
        pass

    @abstractmethod
    def removeOrder(self, order_id: int) -> None:
        pass

    @abstractmethod
    def cleanHeap(self) -> None:
        pass

    @abstractmethod
    def getAskOrder(self) -> None:
        pass

    @abstractmethod
    def getBidOrder(self) -> None:
        pass

    @abstractmethod
    def listAsk(self, depth: int) -> None:
        pass

    @abstractmethod
    def listBid(self, depth: int) -> None:
        pass


class MatchingStrategy(ABC):
    @abstractmethod
    def match(self, orderbook, new_order):
        pass


class MarketOrderMatching(MatchingStrategy):
    def match(self, orderbook: OrderBookInterface, new_order):

        price_quantity = 0
        original_quantity = new_order.quantity
        avg_price = 0

        if new_order.order_side == "buy":

            while orderbook.sell_orders and new_order.quantity > 0:

                best_sell_order = orderbook.sell_orders[0]
                traded_price = best_sell_order.price

                if new_order.quantity >= best_sell_order.quantity:

                    traded_quantity = best_sell_order.quantity
                    price_quantity += traded_quantity * traded_price

                    orderbook.trade_manager.record_trade(
                        Trade(
                            new_order.order_id,
                            best_sell_order.order_id,
                            traded_price,
                            traded_quantity,
                            best_sell_order.asset,
                        )
                    )
                    new_order.quantity -= traded_quantity
                    heapq.heappop(orderbook.sell_orders)

                    if orderbook.sell_orders and orderbook.sell_orders[0].quantity == 0:
                        orderbook.cleanHeap()

                else:

                    traded_quantity = new_order.quantity

                    price_quantity += traded_quantity * traded_price

                    orderbook.trade_manager.record_trade(
                        Trade(
                            new_order.order_id,
                            best_sell_order.order_id,
                            traded_price,
                            traded_quantity,
                            new_order.asset,
                        )
                    )
                    orderbook.sell_orders[0].quantity -= new_order.quantity
                    new_order.quantity = 0

            # Test if there is order quantity left to hang
            if new_order.quantity > 0 and not orderbook.sell_orders:
                if new_order.partial_fill_behavior == "convert_to_limit":
                    best_bid = orderbook.getBidOrder()
                    if best_bid:
                        limit_order = ConvertibleMarketOrder(
                            new_order.order_id,
                            new_order.quantity,
                            new_order.side,
                            new_order.asset,
                        ).convert_to_limit(best_bid)

                        heapq.heappush(orderbook.buy_orders, limit_order)
                    else:
                        raise ValueError(
                            "There is no Bid to convert Market Order to Limit Order"
                        )
                elif new_order.partial_fill_behavior == "cancel":
                    print(
                        f"Cancelando ordem de mercado {new_order.order_id} por falta de liquidez."
                    )

        else:

            while orderbook.buy_orders and new_order.quantity > 0:

                best_buy_order = orderbook.buy_orders[0]
                traded_price = best_buy_order.price

                if new_order.quantity >= orderbook.buy_orders[0].quantity:

                    traded_quantity = best_buy_order.quantity

                    price_quantity += traded_quantity * traded_price
                    orderbook.trade_manager.record_trade(
                        Trade(
                            best_buy_order.order_id,
                            new_order.order_id,
                            traded_price,
                            traded_quantity,
                            best_buy_order.asset,
                        )
                    )

                    new_order.quantity -= traded_quantity
                    heapq.heappop(orderbook.buy_orders)
                    if orderbook.buy_orders and orderbook.buy_orders[0].quantity == 0:
                        orderbook.cleanHeap()
                else:
                    traded_quantity = new_order.quantity
                    price_quantity += traded_quantity * traded_price
                    orderbook.trade_manager.record_trade(
                        Trade(
                            best_buy_order.order_id,
                            new_order.order_id,
                            traded_price,
                            traded_quantity,
                            new_order.asset,
                        )
                    )
                    orderbook.buy_orders[0].quantity -= new_order.quantity

            # Test if there is order quantity left to hang
            if new_order.quantity > 0 and not orderbook.buy_orders:
                if new_order.partial_fill_behavior == "convert_to_limit":
                    best_ask = orderbook.getAskOrder()
                    if best_ask:
                        limit_order = ConvertibleMarketOrder(
                            new_order.order_id,
                            new_order.quantity,
                            new_order.side,
                            new_order.asset,
                        ).convert_to_limit(best_ask)
                        heapq.heappush(orderbook.buy_orders, limit_order)
                elif new_order.partial_fill_behavior == "cancel":
                    print(
                        f"Cancelando ordem de mercado {new_order.order_id} por falta de liquidez."
                    )

        avg_price = price_quantity / original_quantity
        print(f"Average price for Market Order is: {avg_price}")
        print_line()
        print(f"Executando ordem a mercado: {new_order}")
        print_line()
        return avg_price


class LimitOrderMatching(MatchingStrategy):
    def match(self, orderbook: OrderBookInterface, new_order):

        if (
            orderbook.buy_orders
            and orderbook.sell_orders
            and (
                orderbook.buy_orders[0].quantity == 0
                or orderbook.sell_orders[0].quantity == 0
            )
        ):
            orderbook.cleanHeap()

        while (
            orderbook.buy_orders
            and orderbook.sell_orders
            and orderbook.buy_orders[0].price >= orderbook.sell_orders[0].price
        ):
            best_buy_order = orderbook.buy_orders[0]
            best_sell_order = orderbook.sell_orders[0]

            if best_buy_order.quantity >= best_sell_order.quantity:
                orderbook.trade_manager.record_trade(
                    Trade(
                        best_buy_order.order_id,
                        best_sell_order.order_id,
                        best_sell_order.price,
                        best_sell_order.quantity,
                        best_sell_order.asset,
                    )
                )
                best_buy_order.quantity -= best_sell_order.quantity
                heapq.heappop(orderbook.sell_orders)
                if orderbook.buy_orders and best_buy_order.quantity == 0:
                    heapq.heappop(orderbook.buy_orders)

            else:
                orderbook.trade_manager.record_trade(
                    Trade(
                        best_buy_order.order_id,
                        best_sell_order.order_id,
                        best_sell_order.price,
                        best_buy_order.quantity,
                        best_sell_order.asset,
                    )
                )
                best_sell_order.quantity -= best_buy_order.quantity
                heapq.heappop(orderbook.buy_orders)
                if orderbook.sell_orders and best_sell_order.quantity == 0:
                    heapq.heappop(orderbook.sell_orders)

        print(f"Matching ordem limite {new_order}")
        print_line()


class Trade:
    def __init__(
        self,
        buy_order_id: int,
        sell_order_id: int,
        execution_price: float,
        quantity: int,
        asset: str,
    ):
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.execution_price = execution_price
        self.filled_quantity = quantity
        self.asset = asset

    def __repr__(self):
        return f"Trade(buy_order_id={self.buy_order_id}, sell_order_id={self.sell_order_id}, price={self.execution_price}, qty={self.filled_quantity}, asset={self.asset})"


def print_line():
    print("------------------------")


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
            print(f"Adicionando ordem {order_type}: {order}")
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
            print(f"Ask: {self.sell_orders[0].price}")
            print_line()
            return self.sell_orders[0].price
        else:
            print("Ask Book is empty.")
            print_line()

    def getBidOrder(self):
        if self.buy_orders:
            print(f"Bid: {self.buy_orders[0].price}")
            print_line()
            return self.buy_orders[0].price
        else:
            print("Bid Book is empty.")
            print_line()

    def listAsk(self, depth: int):
        """List first (depth) orders in the Ask order book"""
        asks = heapq.nsmallest(depth, self.sell_orders)
        if asks:
            print("Ask Orders:")
            for order in reversed(asks):
                print(
                    f"Order ID:{order.order_id}, Price: {order.price}, Qty: {order.quantity}"
                )
                print_line()
        else:
            print("No Ask Orders Available.")
            print_line()

    def listBid(self, depth: int):
        "List first (depth) orders in the Bid order book."
        bids = heapq.nlargest(depth, self.buy_orders)
        if bids:
            print("Bid Orders:")
            for order in reversed(bids):
                print(
                    f"Order ID: {order.order_id}, Price: {order.price}, Qty: {order.quantity}"
                )
                print_line()
        else:
            print("No Bid orders Available.")
            print_line()


def createOrderBook():

    strategies = {"limit": LimitOrderMatching(), "market": MarketOrderMatching()}

    OrderFactory.register_order_type("limit", LimitOrder)
    OrderFactory.register_order_type("market", MarketOrder)

    ob = HeapOrderBook("BTC-USD", TradeManager(), strategies)

    ob.getBidOrder()
    ob.getAskOrder()
    ob.trade_manager.list_trades()

    order1 = OrderFactory.create_order("limit", 1, 15, 100, "buy", "BTC-USD")
    order2 = OrderFactory.create_order("limit", 2, 23.5, 100, "buy", "BTC-USD")
    order3 = OrderFactory.create_order("limit", 3, 25, 100, "buy", "BTC-USD")
    order4 = OrderFactory.create_order("limit", 4, 250, 100, "buy", "BTC-USD")

    order5 = OrderFactory.create_order("limit", 5, 23.5, 100, "sell", "BTC-USD")
    order6 = OrderFactory.create_order("limit", 6, 25, 100, "sell", "BTC-USD")
    order7 = OrderFactory.create_order("limit", 7, 50, 100, "sell", "BTC-USD")
    order8 = OrderFactory.create_order("limit", 8, 250, 100, "sell", "BTC-USD")

    ob.addOrder("limit", order1)
    ob.addOrder("limit", order2)
    ob.addOrder("limit", order3)
    ob.addOrder("limit", order4)
    ob.addOrder("limit", order5)
    ob.addOrder("limit", order6)
    ob.addOrder("limit", order7)
    ob.addOrder("limit", order8)

    ob.getBidOrder()
    ob.getAskOrder()
    ob.trade_manager.list_trades()
    ob.listAsk(10)
    ob.listBid(10)

    order9 = OrderFactory.create_order("market", 9, 20, "buy", "BTC-USD")

    ob.addOrder("market", order9)

    ob.trade_manager.list_trades()
    # ob.listAsk(10)
    # ob.listBid(10)


createOrderBook()
