from abc import ABC, abstractmethod

class TradeStorage(ABC):

    @abstractmethod
    def record_trade(self,trade):
        pass

class TradeHistory(ABC):

    @abstractmethod
    def list_trades(self):    
        pass

class TradeManagerInterface(TradeStorage, TradeHistory):
    pass

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
