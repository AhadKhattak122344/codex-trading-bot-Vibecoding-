# 🚀 SPY Trading Bot with AI Sentiment Analysis

A production-grade trading bot that uses **Ollama AI** to analyze news sentiment from Reddit, Twitter, and local news APIs to make intelligent SPY ETF trading decisions.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Ollama](https://img.shields.io/badge/Ollama-AI-green.svg)

---

## 📋 SUPER SIMPLE SETUP INSTRUCTIONS

### Step 1: Install Python (if you don't have it)

1. Go to https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the installer
4. **IMPORTANT**: Check the box that says "Add Python to PATH" ✅
5. Click "Install Now"

### Step 2: Install Ollama (the AI brain)

1. Go to https://ollama.ai
2. Click "Download"
3. Install it like any normal program
4. Open your terminal/command prompt and type:
   ```
   ollama pull llama3.2
   ```
5. Wait for it to download (this might take a few minutes)

### Step 3: Open VS Code and Set Up the Project

1. Open VS Code
2. Click `File` → `Open Folder`
3. Select the `spy_trading_bot` folder
4. Open a terminal in VS Code: Click `Terminal` → `New Terminal`

### Step 4: Create a Virtual Environment (keeps things clean)

Copy and paste this into your terminal:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal line.

### Step 5: Install All the Libraries

Copy and paste this ONE command:

```bash
pip install streamlit pandas numpy plotly requests praw tweepy python-dotenv aiohttp beautifulsoup4 ta yfinance ollama httpx
```

Wait for everything to install (1-2 minutes).

### Step 6: Set Up Your API Keys

1. Open the file called `.env.example`
2. Save it as `.env` (just remove the `.example` part)
3. Fill in your API keys (see the API Setup Guide below)

### Step 7: Run the Bot! 🎉

```bash
streamlit run app.py
```

A browser window will open with your trading bot!

---

## 🔑 API Setup Guide (Get Your Keys)

### Reddit API (Free)
1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..."
3. Name: "SPY Trading Bot"
4. Select "script"
5. Redirect URI: http://localhost:8080
6. Click "create app"
7. Copy the ID under your app name → `REDDIT_CLIENT_ID`
8. Copy the secret → `REDDIT_CLIENT_SECRET`

### Twitter/X API (Free tier available)
1. Go to https://developer.twitter.com/
2. Sign up for a developer account
3. Create a new project/app
4. Copy your Bearer Token → `TWITTER_BEARER_TOKEN`

### News API (Free)
1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Sign up (free)
4. Copy your API key → `NEWS_API_KEY`

### Alpha Vantage (Free - for stock data backup)
1. Go to https://www.alphavantage.co/support/#api-key
2. Get your free API key
3. Copy it → `ALPHA_VANTAGE_KEY`

---

## 📁 Project Structure

```
spy_trading_bot/
├── app.py                 # Main Streamlit application
├── config/
│   └── settings.py        # Configuration settings
├── core/
│   ├── __init__.py
│   ├── ollama_client.py   # Ollama AI integration
│   ├── sentiment_analyzer.py  # Sentiment analysis engine
│   └── trading_engine.py  # Trading logic & signals
├── data_sources/
│   ├── __init__.py
│   ├── reddit_client.py   # Reddit data fetcher
│   ├── twitter_client.py  # Twitter/X data fetcher
│   └── news_client.py     # News API fetcher
├── models/
│   ├── __init__.py
│   └── schemas.py         # Data models
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Utility functions
├── .env.example           # Example environment file
├── requirements.txt       # Python dependencies
└── README.md              # This file!
```

---

## ⚠️ IMPORTANT DISCLAIMERS

1. **This is for EDUCATIONAL PURPOSES only**
2. **Do NOT trade real money** without extensive testing
3. **Paper trade first** - use simulated money
4. The creators are not responsible for any financial losses
5. Always consult a financial advisor before trading

---

## 🆘 Troubleshooting

### "Ollama not found"
- Make sure Ollama is running (open the Ollama app)
- In terminal, type: `ollama serve`

### "Module not found"
- Make sure you activated the virtual environment
- Re-run: `pip install -r requirements.txt`

### "API Error"
- Double-check your API keys in the `.env` file
- Make sure there are no extra spaces

### Still stuck?
- Ask on Stack Overflow with tag `streamlit`
- Check the Ollama Discord community

---

## 📜 License

MIT License - Use freely, but remember: trade responsibly!

---

Made with ❤️ and AI
