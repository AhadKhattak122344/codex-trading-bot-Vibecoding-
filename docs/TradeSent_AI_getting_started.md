# TradeSent.AI beginner walkthrough

This guide is written for a Windows user working in VS Code who wants to build a beginner-friendly, sentiment-driven demo trading bot similar to the description provided (real-time Reddit/Twitter sentiment + 10-year market data backtesting + Alpaca paper trading). It walks slowly through each step, from installing tools to writing minimal code you can extend.

> ⚠️ **Risk note:** This is for educational use on paper trading accounts only. Real-money trading carries risk. Review broker terms and test thoroughly.

## 1) Install the basics on Windows
1. Install **Git for Windows**: <https://git-scm.com/download/win> (choose defaults, enable "Git Bash").
2. Install **Python 3.11+**: <https://www.python.org/downloads/> (check "Add Python to PATH").
3. Install **VS Code**: <https://code.visualstudio.com/>.
4. Install **Node.js 18+** (needed for Socket.IO frontend dev): <https://nodejs.org/>.
5. Create a folder for the project (for example `C:\TradeSentAI`).
6. Sign up for required accounts/keys:
   - **Alpaca** paper trading API keys: <https://alpaca.markets/>.
   - **Twitter/X API** (Elevated or v2+ with filtered stream) for tweets.
   - **Reddit API**: create a script app at <https://www.reddit.com/prefs/apps>.
   - (Optional) **GroqCloud/Claude/OpenAI** API keys for LLM sentiment layering.

## 2) Clone and open in VS Code
```bash
# in Git Bash or Windows Terminal
cd C:\
git clone https://github.com/your-username/codex-trading-bot-Vibecoding-.git
cd codex-trading-bot-Vibecoding-
code .
```
VS Code will open in the project folder.

## 3) Create and activate a Python virtual environment
```bash
python -m venv .venv
# activate in PowerShell
. .venv\\Scripts\\Activate.ps1
# or in Git Bash
source .venv/Scripts/activate
```

## 4) Install backend dependencies
Install libraries for data, backtesting, sentiment, and the REST/WebSocket API layer.
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
Notes:
- A `requirements.txt` is included in the repo with all needed packages.
- `backtrader` handles backtesting on 10-year OHLC data.
- `transformers` + `torch` let you load **FinBERT** for financial sentiment.
- `praw` (Reddit) and `tweepy` (Twitter) handle ingestion.
- `flask-socketio` + `eventlet` enable low-latency server push to a browser UI.

## 5) Create the project folders and files in VS Code
You can do this either with commands or directly inside VS Code. Pick whichever feels easier.

### Option A: create folders/files from the terminal (quick)
```bash
mkdir -p backend data
code backend/data.py backend/backtest.py backend/sentiment.py backend/broker.py backend/app.py
```
This opens the files in VS Code. Paste the snippets from sections 8–12 into the matching files.

### Option B: create inside VS Code (click-by-click)
1. In VS Code Explorer, click **New Folder** → name it `backend`.
2. Right-click the `backend` folder → **New File** → type `data.py`, then paste the section 8 code.
3. Repeat for `backtest.py`, `sentiment.py`, `broker.py`, and `app.py` using the matching code sections (9–12).
4. Create a `data` folder (for downloaded CSVs) via **New Folder** → `data`.

## 6) (Optional) Install frontend helper tools
If you want a small dashboard with live sentiment, install UI tooling:
```bash
npm install -g yarn
# later in a /ui folder you can run: yarn create react-app tradesent-ui
```

## 7) Plan the project structure
A minimal, VS Code–friendly layout:
```
.
├── README.md
├── docs/
├── backend/
│   ├── app.py              # Flask + Socket.IO server
│   ├── sentiment.py        # FinBERT/LLM sentiment scoring
│   ├── data.py             # Historical data download & caching
│   ├── broker.py           # Alpaca paper trading helpers
│   └── backtest.py         # Strategy + backtesting harness
└── ui/                     # (Optional) React front-end
```
You can create these files gradually as you follow the snippets below.

## 8) Download 10 years of data
Use `yfinance` to fetch a decade of daily candles and cache to disk so backtests are fast.
```python
# backend/data.py
from pathlib import Path
import yfinance as yf
import pandas as pd

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def load_history(ticker: str = "SPY", years: int = 10) -> pd.DataFrame:
    df = yf.download(ticker, period=f"{years}y", interval="1d", auto_adjust=True)
    csv_path = DATA_DIR / f"{ticker}_{years}y.csv"
    df.to_csv(csv_path)
    return df

if __name__ == "__main__":
    print(load_history().tail())
```
Run once with `python backend/data.py` to create `data/SPY_10y.csv`.

## 9) Basic backtest with backtrader
A tiny moving-average crossover strategy you can extend.
```python
# backend/backtest.py
import backtrader as bt
from data import load_history

class SmaCross(bt.Strategy):
    params = dict(fast=10, slow=20)
    def __init__(self):
        close = self.datas[0].close
        self.fast = bt.ind.SMA(close, period=self.p.fast)
        self.slow = bt.ind.SMA(close, period=self.p.slow)
        self.crossover = bt.ind.CrossOver(self.fast, self.slow)
    def next(self):
        if not self.position and self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.sell()

if __name__ == "__main__":
    df = load_history()
    data = bt.feeds.PandasData(dataname=df)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross)
    cerebro.broker.setcash(100_000)
    print("Starting Portfolio Value:", cerebro.broker.getvalue())
    cerebro.run()
    print("Final Portfolio Value:", cerebro.broker.getvalue())
```
Run `python backend/backtest.py` to confirm backtesting works.

## 10) Sentiment ingestion (Reddit + Twitter) and FinBERT scoring
```python
# backend/sentiment.py
import os
import praw
import tweepy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load FinBERT
MODEL = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="TradeSentAI/0.1",
)

# Twitter client
client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

LABELS = ["negative", "neutral", "positive"]

def score_text(text: str) -> dict:
    tokens = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        logits = model(**tokens).logits
        probs = F.softmax(logits, dim=-1).squeeze()
    return {label: float(probs[i]) for i, label in enumerate(LABELS)}

def reddit_headlines(subreddit="wallstreetbets", limit=10):
    for post in reddit.subreddit(subreddit).hot(limit=limit):
        yield post.title

def twitter_headlines(query="SPY", limit=10):
    tweets = client.search_recent_tweets(query=query, max_results=limit)
    if tweets.data:
        for t in tweets.data:
            yield t.text

if __name__ == "__main__":
    for text in list(reddit_headlines())[:3] + list(twitter_headlines())[:3]:
        print(text, score_text(text))
```
Environment variables to set in VS Code `settings.json` or `.env`:
```
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
TWITTER_BEARER_TOKEN=...
```

## 11) Paper trading with Alpaca
```python
# backend/broker.py
import os
from alpaca_trade_api.rest import REST, TimeFrame

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")
BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

client = REST(API_KEY, API_SECRET, BASE_URL)

def submit_market_order(symbol: str, qty: int, side: str):
    order = client.submit_order(symbol=symbol, qty=qty, side=side, type="market", time_in_force="day")
    return order._raw

def account_info():
    return client.get_account()._raw

if __name__ == "__main__":
    print(account_info())
```
Set environment variables:
```
ALPACA_API_KEY=...
ALPACA_API_SECRET=...
```

## 12) Glue it together with Flask + Socket.IO
```python
# backend/app.py
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from sentiment import score_text, reddit_headlines, twitter_headlines
from broker import submit_market_order, account_info

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/health")
def health():
    return {"ok": True}

@app.route("/sentiment")
def sentiment_api():
    ticker = request.args.get("ticker", "SPY")
    texts = list(reddit_headlines(limit=5)) + list(twitter_headlines(query=ticker, limit=5))
    scored = [{"text": t, "scores": score_text(t)} for t in texts]
    socketio.emit("sentiment", scored)
    return jsonify(scored)

@app.route("/trade", methods=["POST"])
def trade_api():
    data = request.get_json(force=True)
    order = submit_market_order(data.get("symbol", "SPY"), int(data.get("qty", 1)), data.get("side", "buy"))
    socketio.emit("order", order)
    return jsonify(order)

@app.route("/account")
def account_api():
    return jsonify(account_info())

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
```
Run locally:
```bash
python backend/app.py
```
Open another terminal and fetch sentiment:
```bash
curl http://127.0.0.1:5000/sentiment
```

## 13) Add a simple web UI (optional)
- Create `ui/` via `yarn create react-app tradesent-ui` and run `yarn start`.
- Use Socket.IO client to subscribe to `sentiment` and `order` events:
```javascript
// ui/src/App.js (excerpt)
import { io } from "socket.io-client";
import { useEffect, useState } from "react";
const socket = io("http://localhost:5000");
function App() {
  const [sentiment, setSentiment] = useState([]);
  useEffect(() => {
    socket.on("sentiment", setSentiment);
    return () => socket.off("sentiment");
  }, []);
  return (
    <div>
      <h1>TradeSent.AI Sentiment</h1>
      <ul>{sentiment.map((s, i) => (<li key={i}>{s.text} — {JSON.stringify(s.scores)}</li>))}</ul>
    </div>
  );
}
export default App;
```

## 14) VS Code quality-of-life setup
- Install the **Python**, **Pylance**, and **ESLint** extensions.
- Create `.env` in the repo root with your secrets so the debugger loads them.
- Configure formatting (e.g., `black` + `isort`) and a `launch.json` to start `backend/app.py`.

## 15) Next steps to reach your vision
- Swap FinBERT with an LLM chain (e.g., Claude, GPT, or Groq Llama 70B) for layered scoring.
- Add a rule engine: combine technical signals (from backtests) with sentiment thresholds.
- Introduce position sizing and risk controls (max loss per day, stop orders, cooldowns).
- Containerize with Docker for reproducible deploys.
- Set up CI to run unit tests and linting before paper trading.

With the steps above, you can iteratively grow from a minimal demo to a full TradeSent.AI-style system while staying beginner-friendly in VS Code on Windows.
