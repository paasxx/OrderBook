

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
        return f"<{self.__class__.__name__} (buy_order_id={self.buy_order_id}, sell_order_id={self.sell_order_id}, price={self.execution_price}, qty={self.filled_quantity}, asset={self.asset})>"
