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
    buy_order = OrderFactory.create_order(
        order_type="limit", order_id=1, price=100, quantity=10, order_side="buy", asset="BTC-USD"
    )
    sell_order = OrderFactory.create_order(
        order_type="limit", order_id=2, price=105, quantity=5, order_side="sell", asset="BTC-USD"
    )

    order_book.addOrder(order_type="limit", order=buy_order)
    order_book.addOrder(order_type="limit", order=sell_order)

    best_bid = order_book.getBid()
    best_ask = order_book.getAsk()

    assert best_bid == 100
    assert best_ask == 105


def test_market_order_executes_trade(order_book):
    buy_order = OrderFactory.create_order(
        order_type="limit", order_id=1, price=100, quantity=10, order_side="buy", asset="BTC-USD"
    )
    sell_order = OrderFactory.create_order(
        order_type="limit", order_id=2, price=99, quantity=5, order_side="sell", asset="BTC-USD"
    )

    order_book.addOrder(order_type="limit", order=buy_order)
    order_book.addOrder(order_type="limit", order=sell_order)

    # This should match against the buy order
    market_order = OrderFactory.create_order(
        order_type="market", order_id=3, quantity=5, order_side="sell", asset="BTC-USD"
    )

    order_book.addOrder(order_type="market", order=market_order)

    trades = order_book.trade_manager.trades

    assert len(trades) == 2
    assert trades[0].buy_order_id == 1
    assert trades[0].sell_order_id == 2
    assert trades[0].filled_quantity == 5
    assert trades[0].execution_price == 99  # Price from limit buy


def test_order_priority(order_book):
    # Same price, different timestamps (lower ID = earlier)
    order1 = OrderFactory.create_order(
        order_type="limit", order_id=1, price=100, quantity=10, order_side="buy", asset="BTC-USD"
    )
    order2 = OrderFactory.create_order(
        order_type="limit", order_id=2, price=100, quantity=10, order_side="buy", asset="BTC-USD"
    )

    order_book.addOrder(order_type="limit", order=order1)
    order_book.addOrder(order_type="limit", order=order2)

    best_bid_order = order_book.getBidOrder()
    assert best_bid_order.order_id == 1

@pytest.fixture
def empty_orderbook():

    strategies = {
        "limit": LimitOrderMatching(),
        "market": MarketOrderMatching(),
    }

    OrderFactory.register_order_type("limit", LimitOrder)
    OrderFactory.register_order_type("market", MarketOrder)
    return HeapOrderBook("BTC-USD", TradeManager(), strategies)

def test_market_order_converts_to_limit_on_no_liquidity(empty_orderbook):
    orderbook = empty_orderbook

    limit_order = LimitOrder(
        order_id=1,
        price=1000,
        quantity=10,
        order_side="buy",
        asset="BTC-USD",
        
    )

    market_order = MarketOrder(
        order_id=2,
        quantity=15,
        order_side="sell",
        asset="BTC-USD",
        partial_fill_behavior="convert_to_limit",
        fallback_price=1500,
    )

    orderbook.addOrder("limit",limit_order)
    orderbook.addOrder("market",market_order)

    assert len(orderbook.buy_orders) == 0
    pending_order = orderbook.sell_orders[0]
    assert pending_order.quantity == 5