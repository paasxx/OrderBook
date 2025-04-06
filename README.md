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

```bash
pytest tests/
