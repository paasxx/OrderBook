import pytest
from core.matching import LimitOrderMatching, MarketOrderMatching
from core.factory import OrderFactory
from core.orders import LimitOrder, MarketOrder
from services.trade_manager import TradeManager
from core.orderbook import HeapOrderBook

@pytest.fixture
def order_book():
    strategies = {
        "limit": LimitOrderMatching(),
        "market": MarketOrderMatching(),
    }
    OrderFactory.register_order_type("limit", LimitOrder)
    OrderFactory.register_order_type("market", MarketOrder)
    return HeapOrderBook("BTC-USD", TradeManager(), strategies)


def test_add_limit_orders(order_book):
    buy_order = OrderFactory.create_order("limit", 1, 100, 10, "buy", "BTC-USD")
    sell_order = OrderFactory.create_order("limit", 2, 105, 5, "sell", "BTC-USD")

    order_book.addOrder("limit", buy_order)
    order_book.addOrder("limit", sell_order)

    best_bid = order_book.getBidOrder()
    best_ask = order_book.getAskOrder()

    assert best_bid.price == 100
    assert best_ask.price == 105


def test_market_order_executes_trade(order_book):
    buy_order = OrderFactory.create_order("limit", 1, 100, 10, "buy", "BTC-USD")
    sell_order = OrderFactory.create_order("limit", 2, 99, 5, "sell", "BTC-USD")

    order_book.addOrder("limit", buy_order)
    order_book.addOrder("limit", sell_order)

    # This should match against the buy order
    market_order = OrderFactory.create_order("market", 3, 5, "sell", "BTC-USD")
    order_book.addOrder("market", market_order)

    trades = order_book.trade_manager.list_trades()

    assert len(trades) == 1
    assert trades[0]["buyer_id"] == 1
    assert trades[0]["seller_id"] == 3
    assert trades[0]["amount"] == 5
    assert trades[0]["price"] == 100  # Price from limit buy


def test_order_priority(order_book):
    # Same price, different timestamps (lower ID = earlier)
    order1 = OrderFactory.create_order("limit", 1, 100, 10, "buy", "BTC-USD")
    order2 = OrderFactory.create_order("limit", 2, 100, 10, "buy", "BTC-USD")

    order_book.addOrder("limit", order1)
    order_book.addOrder("limit", order2)

    best_bid = order_book.getBidOrder()
    assert best_bid.order_id == 1