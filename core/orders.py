from datetime import datetime
from abc import ABC, abstractmethod


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
        return f"<{self.__class__.__name__} id={self.order_id}, qty={self.quantity}, side={self.order_side}, asset={self.asset}>"

    @abstractmethod
    def __lt__(self, other):
        pass


class BaseOrder(AbstractOrder):
    def __init__(
        self,
        order_id: int,
        quantity: int,
        order_side: str,
        asset: str,
        partial_fill_behavior: str,
        fallback_price: float,
    ):
        super().__init__(order_id, quantity, order_side, asset)
        self.partial_fill_behavior = partial_fill_behavior
        self.fallback_price = fallback_price

    def __lt__(self, other):
        if not isinstance(other, BaseOrder):
            return NotImplemented  # Avoid invalid comparisons
        return self.timestamp < other.timestamp


class PricedOrder(AbstractOrder):
    def __init__(self, order_id, price, quantity, order_side, asset):
        super().__init__(order_id, quantity, order_side, asset)
        self.price = price

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.order_id}, price: {self.price}, qty={self.quantity}, side={self.order_side}, asset={self.asset}>"
    
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

    def __lt__(self, other):
        if not isinstance(other, LimitOrder):
            return NotImplemented  # Avoid invalid comparisons
        if self.price == other.price:
            return self.timestamp < other.timestamp
        return (
            self.price > other.price
            if self.order_side == "buy"
            else self.price < other.price
        )


class MarketOrder(BaseOrder):

    def __init__(
        self, order_id, quantity, order_side, asset, partial_fill_behavior="cancel", fallback_price = None,
    ):
        super().__init__(order_id, quantity, order_side, asset, partial_fill_behavior, fallback_price)

    def __lt__(self, other):
        if not isinstance(other, MarketOrder):
            return NotImplemented  # Avoid invalid comparisons
        return self.timestamp < other.timestamp


class ConvertibleMarketOrder(MarketOrder):

    def __init__(self, order: MarketOrder):
        super().__init__(order.order_id, order.quantity, order.order_side, order.asset,order.partial_fill_behavior, order.fallback_price)

    def convert_to_limit(self, price):
        """Convert order to limit if needed, as a market order
        that has to be hanged in book because of lacking liquidity"""
        if price is None:
            raise ValueError("Cannot convert to limit order without a price.")

        return LimitOrder(
            self.order_id, price, self.quantity, self.order_side, self.asset
        )