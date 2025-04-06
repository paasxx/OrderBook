

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