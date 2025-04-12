# 🧠 Matching Engine & Order Book in Python

This project is a professional-grade **matching engine and order book implementation** built from scratch using **Python, OOP, and SOLID principles**. Designed with clarity, extensibility, and performance in mind, it supports:

- ✅ Market and Limit Orders
- ✅ Partial Fills and Order Conversions
- ✅ Fallback Price & Convertible Market Orders
- ✅ Liquidity Management
- ✅ Heap-based Order Book Prioritization
- ✅ Interface-driven Architecture (SOLID/ISP)
- ✅ Trade History Logging and Matching Engine Abstraction
- ✅ **Automatic Matching**: Every order added to the book is immediately called to be matched — no need to call `match()` manually, it already does call match internally, if book is favorable will be matched.


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
- `fallback_price` (optional): Used when market order needs to rest in book as limit

### 🔁 Matching Strategies
- `MarketOrderMatching`: Matches market orders against the order book
- `LimitOrderMatching`: Matches limit orders with price-time priority
- Strategy pattern allows easy swapping/custom logic.

### 📚 Trade Management
- `TradeManager`: Handles recording and listing of trades
- Follows Interface Segregation Principle (ISP) with separate concerns (`record`, `list`)

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
order_book.addOrder(
    order_type="limit",
    order=OrderFactory.create_order(
      "limit", 
      order_id=1, 
      price=100, 
      quantity=10, 
      order_side="buy", 
      asset="BTC-USD"
      )
)
order_book.addOrder(
    order_type="limit",
    order=OrderFactory.create_order(
      "limit", 
      order_id=2, 
      price=105, 
      quantity=5, 
      order_side="sell", 
      asset="BTC-USD"
      )
)

# Top-of-book inspection
order_book.getBid()
order_book.getAsk()

# Add a market order that triggers matching
order_book.addOrder(
    order_type="market",
    order=OrderFactory.create_order(
      "market", 
      order_id=3, 
      quantity=15, 
      order_side="buy", 
      asset="BTC-USD"
      )
)


# log recorded trades
order_book.trade_manager.list_trades()

```

### 🔄 Market Order: Fallback, Fill Behavior, and Conversion

Market orders attempt to execute immediately against the best available prices in the order book.  
If there isn't enough liquidity, you can control the behavior of the order using:

- `fallback_price`: the price used to convert the remaining portion of the market order into a `LimitOrder`
- `fill_behavior`: determines the behavior when the order is **not fully filled**

#### Options for `fill_behavior`:

- `"convert_to_limit"`: executes the quantity that can be filled immediately, and converts the rest into a `LimitOrder`
- `"cancel"` (default): executes the quantity that can be filled immediately, and cancel the remaining quantity.


#### 💡 Example: Market order with automatic conversion

```python
from core.orders import MarketOrder, ConvertibleMarketOrder

# Create a market order to buy 15 BTC
# If not fully filled, convert the remainder into a LimitOrder with price 98
market_order = MarketOrder(
    order_id=4,
    quantity=15,
    order_side="buy",
    asset="BTC-USD",
    fallback_price=98,
    fill_behavior="convert_to_limit",  # Fill what can be filled, convert the rest
)
```

### 🧠 Design Principles
- **OOP**: Modular, encapsulated components
- **SOLID**:
  - Single Responsibility: Classes are focused and clean
  - Open/Closed: Add new order types without changing existing logic
  - Liskov: Consistent type usage and inheritance
    - e.g. `ConvertibleMarketOrder` can replace `MarketOrder` securely, using `fallback_price`
  - Interface Segregation: Split interfaces to avoid bloated contracts
  - Dependency Inversion: Matching logic depends on abstractions

## 🧪 Tests

Basic tests are available in `/tests`. Run with:

### 1. Navigate to the root of the project (where this README is)
```python
cd path/to/project-root
```
### 2. Create a virtual environment in the root directory, if Mac OS use python3
```python
python -m venv venv
```
### 3. Activate the environment
#### On macOS/Linux:
```python
source venv/bin/activate
```
### On Windows:
```python
venv\Scripts\activate
```
### 4. Install dependencies
```python
pip install -r requirements.txt
```
### 5. Run the test suite
```python
pytest tests/
```
### 6. Run main.py to see logs system

📟 You can also run main.py to simulate real-time logs and see terminal output + file logging.
Logs are saved in the logs/ folder with timestamped filenames.

