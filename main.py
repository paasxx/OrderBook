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

    ob.getBid()
    ob.getAsk()
    ob.trade_manager.list_trades()

     # Buy limit orders
    order1 = OrderFactory.create_order(
        order_type="limit", order_id=1, price=15, quantity=100, order_side="buy", asset="BTC-USD"
    )
    order2 = OrderFactory.create_order(
        order_type="limit", order_id=2, price=23.5, quantity=100, order_side="buy", asset="BTC-USD"
    )
    order3 = OrderFactory.create_order(
        order_type="limit", order_id=3, price=25, quantity=100, order_side="buy", asset="BTC-USD"
    )
    order4 = OrderFactory.create_order(
        order_type="limit", order_id=4, price=250, quantity=100, order_side="buy", asset="BTC-USD"
    )

    # Sell limit orders
    order5 = OrderFactory.create_order(
        order_type="limit", order_id=5, price=23.5, quantity=100, order_side="sell", asset="BTC-USD"
    )
    order6 = OrderFactory.create_order(
        order_type="limit", order_id=6, price=25, quantity=100, order_side="sell", asset="BTC-USD"
    )
    order7 = OrderFactory.create_order(
        order_type="limit", order_id=7, price=50, quantity=100, order_side="sell", asset="BTC-USD"
    )
    order8 = OrderFactory.create_order(
        order_type="limit", order_id=8, price=250, quantity=100, order_side="sell", asset="BTC-USD"
    )


    # Add all limit orders to the book
    for order in [order1, order2, order3, order4, order5, order6, order7, order8]:
        ob.addOrder(order_type="limit", order=order)

    ob.getBid()
    ob.getAsk()
    ob.trade_manager.list_trades()
    ob.listAsk(10)
    ob.listBid(10)

    # Market order with fallback behavior
    order9 = OrderFactory.create_order(
        order_type="market", order_id=9, quantity=20, order_side="buy", asset="BTC-USD", partial_fill_behavior="convert_to_limit"
    )

    ob.addOrder("market", order9)

    ob.trade_manager.list_trades()
    # ob.listAsk(10)
    # ob.listBid(10)


createOrderBook()
