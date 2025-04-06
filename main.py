from core.matching import LimitOrderMatching, MarketOrderMatching
from core.factory import OrderFactory
from core.orders import LimitOrder, MarketOrder
from services.trade_manager import TradeManager
from core.orderbook import HeapOrderBook


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
