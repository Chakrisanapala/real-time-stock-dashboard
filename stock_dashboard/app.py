import json
from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# App Configuration
# ──────────────────────────────────────────────────────────────────────────────
app = Flask(__name__)

POPULAR_STOCKS = [
    {'symbol': 'AAPL',        'name': 'Apple Inc.'},
    {'symbol': 'MSFT',        'name': 'Microsoft Corp.'},
    {'symbol': 'GOOGL',       'name': 'Alphabet Inc.'},
    {'symbol': 'AMZN',        'name': 'Amazon.com'},
    {'symbol': 'TSLA',        'name': 'Tesla Inc.'},
    {'symbol': 'NVDA',        'name': 'NVIDIA Corp.'},
    {'symbol': 'META',        'name': 'Meta Platforms'},
    {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries'},
    {'symbol': 'TCS.NS',      'name': 'TCS (India)'},
    {'symbol': 'INFY.NS',     'name': 'Infosys (India)'},
]

# Maps UI period key → (yfinance period, yfinance interval)
PERIOD_MAP = {
    '1D': ('1d',  '5m'),
    '5D': ('5d',  '15m'),
    '1M': ('1mo', '1h'),
    '6M': ('6mo', '1d'),
    '1Y': ('1y',  '1d'),
    '5Y': ('5y',  '1wk'),
}

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
def safe_val(val, decimals: int = 2, suffix: str = '') -> str:
    """Return a formatted numeric string, or 'N/A' for missing/NaN values."""
    try:
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return 'N/A'
        if isinstance(val, (int, float)):
            return f'{val:,.{decimals}f}{suffix}'
        return str(val)
    except Exception:
        return 'N/A'


def format_large(val) -> str:
    """Format large numbers as $T / $B / $M for readability."""
    try:
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return 'N/A'
        val = float(val)
        if val >= 1e12: return f'${val / 1e12:.2f}T'
        if val >= 1e9:  return f'${val / 1e9:.2f}B'
        if val >= 1e6:  return f'${val / 1e6:.2f}M'
        return f'${val:,.2f}'
    except Exception:
        return 'N/A'


def compute_rsi(closes: pd.Series, window: int = 14):
    delta = closes.diff()
    gain  = delta.clip(lower=0).rolling(window).mean()
    loss  = (-delta.clip(upper=0)).rolling(window).mean()
    rs    = gain / loss
    rsi   = 100 - (100 / (1 + rs))
    last  = rsi.iloc[-1]
    return round(float(last), 1) if not pd.isna(last) else None


def compute_macd(closes: pd.Series):
    ema12  = closes.ewm(span=12).mean()
    ema26  = closes.ewm(span=26).mean()
    line   = ema12 - ema26
    signal = line.ewm(span=9).mean()
    return round(float(line.iloc[-1]), 3), round(float(signal.iloc[-1]), 3)


# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('dashboard.html', stocks=POPULAR_STOCKS)


@app.route('/api/stock/<symbol>')
def get_stock_data(symbol: str):
    period_key = request.args.get('period', '1M')
    period, interval = PERIOD_MAP.get(period_key, ('1mo', '1d'))

    try:
        ticker = yf.Ticker(symbol)
        info   = ticker.info
        hist   = ticker.history(period=period, interval=interval)

        if hist.empty:
            return jsonify({'error': 'No data available for this symbol'}), 404

        # ── Price & Change ──────────────────────────────────────────────────
        current    = float(hist['Close'].iloc[-1])
        prev_close = float(
            info.get('previousClose') or
            (hist['Close'].iloc[-2] if len(hist) > 1 else current)
        )
        change     = current - prev_close
        change_pct = (change / prev_close) * 100 if prev_close else 0

        # ── OHLCV Chart Data ────────────────────────────────────────────────
        time_fmt = '%Y-%m-%d %H:%M' if interval in ('5m', '15m', '1h') else '%Y-%m-%d'
        chart_data = [
            {
                'time':   idx.strftime(time_fmt),
                'open':   round(float(row['Open']),  2),
                'high':   round(float(row['High']),  2),
                'low':    round(float(row['Low']),   2),
                'close':  round(float(row['Close']), 2),
                'volume': int(row['Volume']),
            }
            for idx, row in hist.iterrows()
        ]

        # ── Moving Averages ─────────────────────────────────────────────────
        closes = hist['Close']
        ma20 = round(float(closes.rolling(20).mean().iloc[-1]), 2) if len(closes) >= 20 else None
        ma50 = round(float(closes.rolling(50).mean().iloc[-1]), 2) if len(closes) >= 50 else None

        # ── Technical Indicators ────────────────────────────────────────────
        rsi         = compute_rsi(closes)
        macd, macd_signal = compute_macd(closes)

        return jsonify({
            'symbol':       symbol.upper(),
            'name':         info.get('longName') or info.get('shortName', symbol),
            'currency':     info.get('currency', 'USD'),
            'exchange':     info.get('exchange', ''),
            'sector':       info.get('sector', 'N/A'),
            'current_price': round(current, 2),
            'prev_close':   round(prev_close, 2),
            'change':       round(change, 2),
            'change_pct':   round(change_pct, 2),
            'day_high':     safe_val(info.get('dayHigh')  or hist['High'].max()),
            'day_low':      safe_val(info.get('dayLow')   or hist['Low'].min()),
            'week52_high':  safe_val(info.get('fiftyTwoWeekHigh')),
            'week52_low':   safe_val(info.get('fiftyTwoWeekLow')),
            'market_cap':   format_large(info.get('marketCap')),
            'volume':       f"{int(hist['Volume'].iloc[-1]):,}" if not hist.empty else 'N/A',
            'avg_volume':   format_large(info.get('averageVolume')),
            'pe_ratio':     safe_val(info.get('trailingPE')),
            'eps':          safe_val(info.get('trailingEps')),
            'dividend_yield': safe_val((info.get('dividendYield') or 0) * 100, 2, '%'),
            'beta':         safe_val(info.get('beta')),
            'ma20':         ma20,
            'ma50':         ma50,
            'rsi':          rsi,
            'macd':         macd,
            'macd_signal':  macd_signal,
            'chart_data':   chart_data,
            'period':       period_key,
            'timestamp':    datetime.now().strftime('%H:%M:%S'),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search')
def search_symbol():
    q = request.args.get('q', '').strip().upper()
    if not q:
        return jsonify([])
    try:
        ticker = yf.Ticker(q)
        info   = ticker.info
        if info and info.get('symbol'):
            return jsonify([{
                'symbol':   info.get('symbol', q),
                'name':     info.get('longName') or info.get('shortName', q),
                'exchange': info.get('exchange', ''),
            }])
        return jsonify([])
    except Exception:
        return jsonify([])


@app.route('/api/watchlist', methods=['POST'])
def get_watchlist():
    symbols = request.json.get('symbols', [])
    results = []
    for sym in symbols:
        try:
            t    = yf.Ticker(sym)
            info = t.info
            hist = t.history(period='2d', interval='1d')
            if hist.empty:
                continue
            cur  = float(hist['Close'].iloc[-1])
            prev = float(hist['Close'].iloc[-2]) if len(hist) >= 2 else cur
            chg_pct = ((cur - prev) / prev) * 100 if prev else 0
            results.append({
                'symbol':     sym,
                'name':       info.get('shortName', sym),
                'price':      round(cur, 2),
                'change_pct': round(chg_pct, 2),
                'currency':   info.get('currency', 'USD'),
            })
        except Exception:
            pass
    return jsonify(results)


# ──────────────────────────────────────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5001)
