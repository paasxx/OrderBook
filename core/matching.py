from core.interfaces import MatchingStrategy, OrderBookInterface
from core.trades import Trade
import heapq
from core.orders import ConvertibleMarketOrder
from utils.helpers import print_line
from utils.logger import logger


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
                        limit_order = ConvertibleMarketOrder(new_order).convert_to_limit(best_bid)
                        heapq.heappush(orderbook.buy_orders, limit_order)
                    else:
                        raise ValueError(
                            "There is no Bid to convert Market Order to Limit Order"
                        )
                elif new_order.partial_fill_behavior == "cancel":
                    logger.warning(
                        f"Cancelling market order {new_order.order_id} no liquidity in order book."
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
                        limit_order = ConvertibleMarketOrder(new_order).convert_to_limit(best_ask)
                        heapq.heappush(orderbook.buy_orders, limit_order)
                elif new_order.partial_fill_behavior == "cancel":
                    logger.warning(
                        f"Cancelling market order {new_order.order_id}, no liquidity in book order."
                    )

        avg_price = price_quantity / original_quantity if original_quantity else 0
        logger.info(f"Average price for Market Order is: {avg_price}")
        print_line()
        logger.info(f"Matching Market Order: {new_order}")
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

        #logger.info(f"Matching limit order {new_order}")
        #print_line()