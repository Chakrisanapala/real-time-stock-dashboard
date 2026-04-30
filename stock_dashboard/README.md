# 📈 TradeView — Real-Time Stock Market Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=flat&logo=chartdotjs&logoColor=white)
![Yahoo Finance](https://img.shields.io/badge/Data-Yahoo%20Finance-720E9E?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

A full-featured real-time stock market dashboard built with Python Flask and Chart.js. Track live prices, technical indicators, and market data for US and Indian stocks with an auto-refreshing dark-themed UI.

---

## ✨ Features

- **Live Stock Data** — Real-time prices via Yahoo Finance (`yfinance`)
- **Interactive Price Chart** — Smooth gradient line chart with zoom-friendly tooltips
- **Volume Analysis** — Color-coded volume bars (green = up day, red = down day)
- **Technical Indicators**
  - RSI (14) with visual overbought / oversold gauge
  - MACD with signal line and crossover detection
  - Moving Averages (MA20, MA50) with trend colouring
- **Period Selector** — 1D / 5D / 1M / 6M / 1Y / 5Y with auto-adjusted intervals
- **Scrolling Ticker Tape** — Live prices for all watchlist stocks in the header
- **Watchlist Sidebar** — Pre-loaded with FAANG + Indian blue-chips (Reliance, TCS, Infosys)
- **Symbol Search** — Search any Yahoo Finance–listed stock by ticker
- **Auto-Refresh** — Chart and stats refresh every 60 seconds automatically
- **Financial Metrics** — Market cap, P/E ratio, EPS, dividend yield, beta, 52-week range

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.10+, Flask 3.0 |
| Market Data | yfinance (Yahoo Finance API) |
| Data Processing | Pandas, NumPy |
| Charts | Chart.js 4.4 |
| Frontend | Vanilla HTML / CSS / JS |

---

## 📁 Project Structure

```
stock_dashboard/
├── app.py                  # Flask backend — API routes, data processing, indicators
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore
├── templates/
│   └── dashboard.html      # Full frontend (Chart.js, CSS, JS all in one file)
└── static/                 # Reserved for future CSS/JS assets
    ├── css/
    └── js/
```

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/stock-dashboard.git
cd stock-dashboard
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in your browser
```
http://localhost:5001
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main dashboard UI |
| `GET` | `/api/stock/<symbol>` | Full OHLCV data + indicators |
| `GET` | `/api/stock/AAPL?period=1Y` | With period filter |
| `GET` | `/api/search?q=TSLA` | Search stock by symbol |
| `POST` | `/api/watchlist` | Batch current prices for sidebar |

### Example — Fetch stock data
```bash
curl http://localhost:5001/api/stock/AAPL?period=1M
```

### Example — Search a symbol
```bash
curl http://localhost:5001/api/search?q=INFY
```

---

## 📈 Technical Indicators Reference

| Indicator | Calculation | Signal |
|-----------|-------------|--------|
| **RSI (14)** | Relative Strength Index | >70 = overbought, <30 = oversold |
| **MACD** | EMA(12) − EMA(26) | Line > Signal = bullish crossover |
| **MA(20)** | 20-period simple moving average | Price above = bullish |
| **MA(50)** | 50-period simple moving average | Price above = bullish |

---

## 🌐 Supported Markets

- **US Equities** — AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, etc.
- **Indian Equities** — RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, etc.
- **ETFs** — SPY, QQQ, NIFTY50, etc.
- Any symbol available on [Yahoo Finance](https://finance.yahoo.com)

---

## ⚠️ Notes

- Market data is sourced from Yahoo Finance — delays typically 15 minutes for free-tier data.
- For true real-time data, consider paid APIs such as Alpha Vantage, Polygon.io, or Twelve Data.
- This project is for **educational and demonstration purposes only** — not financial advice.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📝 License

MIT License — free for personal and commercial use.

---

*Built as part of the 1-Month Python Developer Internship at Codec Technologies*
