# 🧠 Matching Engine & Order Book in Python

This project is a professional-grade **matching engine and order book implementation** built from scratch using **Python, OOP, and SOLID principles**. Designed with clarity, extensibility, and performance in mind, it supports:

- ✅ Market and Limit Orders
- ✅ Partial Fills and Order Conversions
- ✅ Liquidity Management
- ✅ Heap-based Order Book Prioritization
- ✅ Interface-driven Architecture (SOLID/ISP)
- ✅ Trade History Logging and Matching Engine Abstraction

## ⚙️ Motivation

This project demonstrates strong **software engineering practices** applied to a real-world **financial market problem**. It's intended to showcase:

- Deep understanding of **financial markets** and **trading mechanics**
- Strong grasp of **object-oriented design (OOP)**
- Commitment to **clean, maintainable, and extensible code**
- Knowledge of **SOLID principles** in practice

If you're a fintech, hedge fund, or looking for a backend engineer with financial expertise — let's talk! 👇

## 🧩 Key Components

### 🧱 Order Types
- `LimitOrder`: Price-based order with time priority (FIFO)
- `MarketOrder`: Executes immediately against best available prices
- `ConvertibleMarketOrder`: Market order that can convert to limit if not fully filled

### 🔁 Matching Strategies
- `MarketOrderMatching`: Matches market orders against the order book
- `LimitOrderMatching`: Matches limit orders with price-time priority
- Strategy pattern allows easy swapping/custom logic.

### 📚 Trade Management
- `TradeManager`: Handles recording and listing of trades
- Follows Interface Segregation Principle with separate concerns (`record`, `list`)

## ▶️ Usage Example

Here's a simple usage example to get started with the matching engine:

```python
from core.matching import LimitOrderMatching, MarketOrderMatching
from core.factory import OrderFactory
from core.orders import LimitOrder, MarketOrder
from services.trade_manager import TradeManager
from core.orderbook import HeapOrderBook

# Setup: Register order types and matching strategies
strategies = {
    "limit": LimitOrderMatching(),
    "market": MarketOrderMatching(),
}

OrderFactory.register_order_type("limit", LimitOrder)
OrderFactory.register_order_type("market", MarketOrder)

# Initialize the order book
order_book = HeapOrderBook("BTC-USD", TradeManager(), strategies)

# Add limit orders (buy & sell)
order_book.addOrder("limit", OrderFactory.create_order("limit", 1, 100, 10, "buy", "BTC-USD"))
order_book.addOrder("limit", OrderFactory.create_order("limit", 2, 105, 5, "sell", "BTC-USD"))

# Top-of-book inspection
order_book.getBidOrder()
order_book.getAskOrder()

# Add a market order that triggers matching
order_book.addOrder("market", OrderFactory.create_order("market", 3, 15, "buy", "BTC-USD"))

# Print recorded trades
order_book.trade_manager.list_trades()


### 🧠 Design Principles
- **OOP**: Modular, encapsulated components
- **SOLID**:
  - Single Responsibility: Classes are focused and clean
  - Open/Closed: Add new order types without changing existing logic
  - Liskov: Consistent type usage and inheritance
  - Interface Segregation: Split interfaces to avoid bloated contracts
  - Dependency Inversion: Matching logic depends on abstractions

## 🧪 Tests

Basic tests are available in `/tests`. Run with:

# 1. Navigate to the root of the project (where this README is)
cd path/to/project-root

# 2. Create a virtual environment in the root directory
python -m venv venv

# 3. Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the test suite
pytest tests/

