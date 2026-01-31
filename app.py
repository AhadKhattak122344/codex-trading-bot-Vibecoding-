"""
SPY Trading Bot - Streamlit Application
=======================================
Main application interface for the AI-powered SPY trading bot.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import pytz

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="SPY AI Trading Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import our modules
from config.settings import get_settings
from core import get_ollama_client, get_sentiment_analyzer, get_trading_engine
from models import Sentiment, DataSource, TradeAction
from utils.helpers import (
    get_market_status, format_currency, format_percent,
    get_color_for_sentiment, get_color_for_value, time_ago
)


# Custom CSS for beautiful styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables */
    :root {
        --bg-dark: #0a0a0f;
        --bg-card: #12121a;
        --bg-card-hover: #1a1a25;
        --accent-green: #00ff88;
        --accent-red: #ff4757;
        --accent-blue: #4facfe;
        --accent-yellow: #ffd93d;
        --text-primary: #ffffff;
        --text-secondary: #8b8b9a;
        --border-color: #2a2a3a;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }
    
    /* Main title */
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ff88 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
    }
    
    .subtitle {
        font-family: 'Space Grotesk', sans-serif;
        color: #8b8b9a;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #12121a 0%, #1a1a25 100%);
        border: 1px solid #2a2a3a;
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #4facfe;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(79, 172, 254, 0.15);
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-family: 'Space Grotesk', sans-serif;
        color: #8b8b9a;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Sentiment indicator */
    .sentiment-bullish {
        color: #00ff88;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }
    
    .sentiment-bearish {
        color: #ff4757;
        text-shadow: 0 0 20px rgba(255, 71, 87, 0.5);
    }
    
    .sentiment-neutral {
        color: #ffd93d;
        text-shadow: 0 0 20px rgba(255, 217, 61, 0.5);
    }
    
    /* Signal badge */
    .signal-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .signal-buy {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
        color: #000;
        box-shadow: 0 4px 20px rgba(0, 255, 136, 0.4);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, #ff4757 0%, #ff2744 100%);
        color: #fff;
        box-shadow: 0 4px 20px rgba(255, 71, 87, 0.4);
    }
    
    .signal-hold {
        background: linear-gradient(135deg, #ffd93d 0%, #ffcc00 100%);
        color: #000;
        box-shadow: 0 4px 20px rgba(255, 217, 61, 0.4);
    }
    
    /* Status indicators */
    .status-online {
        display: inline-flex;
        align-items: center;
        color: #00ff88;
    }
    
    .status-offline {
        display: inline-flex;
        align-items: center;
        color: #ff4757;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-dot.online {
        background: #00ff88;
        box-shadow: 0 0 10px #00ff88;
    }
    
    .status-dot.offline {
        background: #ff4757;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Data table */
    .dataframe {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.875rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #12121a;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00ff88 0%, #4facfe 100%);
    }
    
    /* News card */
    .news-card {
        background: #12121a;
        border: 1px solid #2a2a3a;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }
    
    .news-card:hover {
        border-color: #4facfe;
        background: #1a1a25;
    }
    
    .news-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .news-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #8b8b9a;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.auto_refresh = False
        st.session_state.last_analysis = None
        st.session_state.news_items = []
        st.session_state.sentiment_results = []


def render_header():
    """Render the application header."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<h1 class="main-title">📈 SPY AI Trading Bot</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Powered by Ollama LLM • Real-time Sentiment Analysis</p>', unsafe_allow_html=True)
    
    with col2:
        market_status = get_market_status()
        status_class = "online" if market_status['is_open'] else "offline"
        st.markdown(f"""
        <div style="text-align: right; padding-top: 1rem;">
            <div class="status-{status_class}">
                <span class="status-dot {status_class}"></span>
                Market {market_status['status']}
            </div>
            <div style="color: #8b8b9a; font-size: 0.8rem; margin-top: 0.25rem;">
                {market_status['next_event']}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with controls and status."""
    with st.sidebar:
        st.markdown("### ⚙️ Controls")
        
        # Analysis controls
        if st.button("🔄 Run Analysis", use_container_width=True, type="primary"):
            run_analysis()
        
        st.session_state.auto_refresh = st.toggle(
            "Auto-refresh (5 min)",
            value=st.session_state.auto_refresh
        )
        
        st.divider()
        
        # System Status
        st.markdown("### 📊 System Status")
        
        settings = get_settings()
        status = settings.get_status()
        
        for service, is_active in status.items():
            icon = "✅" if is_active else "❌"
            st.markdown(f"{icon} **{service.title()}**")
        
        # Ollama model info
        ollama = get_ollama_client()
        if ollama.is_available:
            st.markdown(f"🤖 Model: `{settings.ollama.model}`")
        
        st.divider()
        
        # Risk Settings
        st.markdown("### ⚠️ Risk Settings")
        st.markdown(f"""
        - Stop Loss: **{settings.trading.stop_loss_percent * 100:.1f}%**
        - Take Profit: **{settings.trading.take_profit_percent * 100:.1f}%**
        - Max Position: **{settings.trading.max_position_size * 100:.0f}%**
        - Min Confidence: **{settings.trading.min_confidence_score * 100:.0f}%**
        """)
        
        st.divider()
        
        # Reset button
        if st.button("🗑️ Reset Portfolio", use_container_width=True):
            engine = get_trading_engine()
            engine.reset_portfolio()
            st.success("Portfolio reset!")
            st.rerun()


def run_analysis():
    """Run sentiment analysis and generate trading signal."""
    analyzer = get_sentiment_analyzer()
    engine = get_trading_engine()
    
    with st.spinner("Fetching news from all sources..."):
        news_items = analyzer.fetch_all_news()
        st.session_state.news_items = news_items
    
    if not news_items:
        st.warning("No news items fetched. Check API configurations.")
        return
    
    with st.spinner("Analyzing sentiment with AI..."):
        progress_bar = st.progress(0)
        
        def update_progress(current, total):
            progress_bar.progress(current / total)
        
        results = analyzer.analyze_batch(news_items, progress_callback=update_progress)
        st.session_state.sentiment_results = results
        
        progress_bar.empty()
    
    # Get aggregate sentiment
    sentiment = analyzer.get_aggregate_sentiment(news_items, force_refresh=True)
    st.session_state.last_analysis = sentiment
    
    # Generate signal
    signal = engine.generate_signal(sentiment)
    st.session_state.last_signal = signal
    
    st.success(f"Analysis complete! Analyzed {len(results)} items.")


def render_market_overview():
    """Render market overview section."""
    engine = get_trading_engine()
    market_data = engine.get_market_data()
    
    st.markdown("### 📊 Market Overview")
    
    cols = st.columns(5)
    
    with cols[0]:
        price_color = "#00ff88" if market_data.change_percent >= 0 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SPY Price</div>
            <div class="metric-value" style="color: {price_color}">
                ${market_data.current_price:.2f}
            </div>
            <div style="color: {price_color}; font-size: 0.9rem;">
                {format_percent(market_data.change_percent)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Today's Range</div>
            <div class="metric-value" style="color: #4facfe; font-size: 1.2rem;">
                ${market_data.low_price:.2f} - ${market_data.high_price:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        rsi_color = "#ff4757" if market_data.rsi and market_data.rsi > 70 else "#00ff88" if market_data.rsi and market_data.rsi < 30 else "#ffd93d"
        rsi_val = f"{market_data.rsi:.1f}" if market_data.rsi else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RSI (14)</div>
            <div class="metric-value" style="color: {rsi_color}">
                {rsi_val}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        sma_status = "Above" if market_data.is_above_sma20 else "Below"
        sma_color = "#00ff88" if market_data.is_above_sma20 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SMA 20</div>
            <div class="metric-value" style="color: {sma_color}; font-size: 1.2rem;">
                {sma_status}
            </div>
            <div style="color: #8b8b9a; font-size: 0.8rem;">
                ${market_data.sma_20:.2f if market_data.sma_20 else 0:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[4]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Trend</div>
            <div class="metric-value" style="font-size: 1.2rem;">
                {market_data.trend_direction}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_sentiment_dashboard():
    """Render the sentiment analysis dashboard."""
    st.markdown("### 🧠 AI Sentiment Analysis")
    
    if st.session_state.last_analysis is None:
        st.info("👆 Click 'Run Analysis' in the sidebar to start sentiment analysis")
        return
    
    sentiment = st.session_state.last_analysis
    
    # Sentiment gauge and metrics
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Sentiment gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sentiment.weighted_score * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#8b8b9a"},
                'bar': {'color': "#4facfe"},
                'bgcolor': "#1a1a25",
                'borderwidth': 2,
                'bordercolor': "#2a2a3a",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(255, 71, 87, 0.3)'},
                    {'range': [40, 60], 'color': 'rgba(255, 217, 61, 0.3)'},
                    {'range': [60, 100], 'color': 'rgba(0, 255, 136, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "#fff", 'width': 4},
                    'thickness': 0.75,
                    'value': sentiment.weighted_score * 100
                }
            },
            title={'text': "Sentiment Score", 'font': {'color': '#fff', 'size': 16}}
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#fff'},
            height=250,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Signal strength text
        signal_strength = sentiment.get_signal_strength()
        sentiment_class = "bullish" if "BULLISH" in signal_strength else "bearish" if "BEARISH" in signal_strength else "neutral"
        
        st.markdown(f"""
        <div style="text-align: center;">
            <span class="sentiment-{sentiment_class}" style="font-size: 1.5rem; font-weight: 600;">
                {signal_strength}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Sentiment breakdown
        breakdown_cols = st.columns(3)
        
        with breakdown_cols[0]:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">Bullish</div>
                <div class="metric-value sentiment-bullish">{sentiment.bullish_count}</div>
                <div style="color: #00ff88;">{sentiment.bullish_ratio * 100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with breakdown_cols[1]:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">Bearish</div>
                <div class="metric-value sentiment-bearish">{sentiment.bearish_count}</div>
                <div style="color: #ff4757;">{sentiment.bearish_ratio * 100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with breakdown_cols[2]:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">Neutral</div>
                <div class="metric-value sentiment-neutral">{sentiment.neutral_count}</div>
                <div style="color: #ffd93d;">{(1 - sentiment.bullish_ratio - sentiment.bearish_ratio) * 100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Source breakdown pie chart
        if sentiment.sources_analyzed:
            fig_pie = px.pie(
                values=list(sentiment.sources_analyzed.values()),
                names=list(sentiment.sources_analyzed.keys()),
                color_discrete_sequence=['#4facfe', '#00ff88', '#ffd93d', '#ff4757'],
                hole=0.4
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#fff'},
                height=200,
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig_pie, use_container_width=True)


def render_trading_signal():
    """Render the current trading signal."""
    st.markdown("### 🎯 Trading Signal")
    
    if not hasattr(st.session_state, 'last_signal') or st.session_state.last_signal is None:
        st.info("Run analysis to generate a trading signal")
        return
    
    signal = st.session_state.last_signal
    engine = get_trading_engine()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Signal badge
        signal_class = "buy" if signal.action == TradeAction.BUY else "sell" if signal.action in [TradeAction.SELL, TradeAction.CLOSE] else "hold"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem 0;">
            <div class="signal-badge signal-{signal_class}">
                {signal.action.value}
            </div>
            <div style="margin-top: 1rem; color: #8b8b9a;">
                Confidence: <strong style="color: #fff;">{signal.confidence * 100:.1f}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Execute button
        if signal.action in [TradeAction.BUY, TradeAction.SELL, TradeAction.CLOSE]:
            if st.button(f"Execute {signal.action.value}", use_container_width=True, type="primary"):
                trade = engine.execute_signal(signal)
                if trade:
                    st.success(f"Trade executed: {trade.notes}")
                    st.rerun()
                else:
                    st.warning("Trade not executed - check conditions")
    
    with col2:
        st.markdown("**Signal Details:**")
        
        details = {
            "Entry Price": f"${signal.entry_price:.2f}" if signal.entry_price else "N/A",
            "Stop Loss": f"${signal.stop_loss:.2f}" if signal.stop_loss else "N/A",
            "Take Profit": f"${signal.take_profit:.2f}" if signal.take_profit else "N/A",
            "Position Size": f"{signal.position_size} shares" if signal.position_size else "N/A",
            "Risk/Reward": f"{signal.risk_reward_ratio:.2f}" if signal.risk_reward_ratio else "N/A"
        }
        
        for key, value in details.items():
            st.markdown(f"- **{key}:** {value}")
        
        st.markdown("**Reasoning:**")
        st.markdown(f"_{signal.reasoning}_")


def render_portfolio():
    """Render portfolio section."""
    st.markdown("### 💼 Portfolio (Paper Trading)")
    
    engine = get_trading_engine()
    portfolio = engine.get_portfolio_summary()
    
    cols = st.columns(5)
    
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Value</div>
            <div class="metric-value" style="color: #4facfe;">
                {format_currency(portfolio['total_value'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        pnl_color = get_color_for_value(portfolio['total_pnl'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total P&L</div>
            <div class="metric-value" style="color: {pnl_color};">
                {format_currency(portfolio['total_pnl'])}
            </div>
            <div style="color: {pnl_color}; font-size: 0.9rem;">
                {format_percent(portfolio['total_pnl_percent'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Cash Balance</div>
            <div class="metric-value" style="font-size: 1.5rem;">
                {format_currency(portfolio['cash_balance'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SPY Shares</div>
            <div class="metric-value" style="font-size: 1.5rem;">
                {portfolio['spy_shares']}
            </div>
            <div style="color: #8b8b9a; font-size: 0.8rem;">
                Avg: {format_currency(portfolio['spy_avg_cost'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[4]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Win Rate</div>
            <div class="metric-value" style="font-size: 1.5rem;">
                {portfolio['win_rate']:.1f}%
            </div>
            <div style="color: #8b8b9a; font-size: 0.8rem;">
                {portfolio['total_trades']} trades
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_recent_news():
    """Render recent news feed."""
    st.markdown("### 📰 Recent News Feed")
    
    if not st.session_state.news_items:
        st.info("Run analysis to fetch news")
        return
    
    # Show recent news with sentiment
    news_items = st.session_state.news_items[:10]
    results_dict = {item.id: result for item, result in st.session_state.sentiment_results}
    
    for item in news_items:
        result = results_dict.get(item.id)
        
        if result:
            sentiment_class = "bullish" if result.sentiment == Sentiment.BULLISH else "bearish" if result.sentiment == Sentiment.BEARISH else "neutral"
            sentiment_icon = "🟢" if result.sentiment == Sentiment.BULLISH else "🔴" if result.sentiment == Sentiment.BEARISH else "🟡"
        else:
            sentiment_class = "neutral"
            sentiment_icon = "⚪"
        
        source_icon = "🔵" if item.source == DataSource.REDDIT else "🐦" if item.source == DataSource.TWITTER else "📰"
        
        st.markdown(f"""
        <div class="news-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="news-title">{item.title[:100]}...</div>
                <span class="sentiment-{sentiment_class}">{sentiment_icon}</span>
            </div>
            <div class="news-meta">
                {source_icon} {item.source.value.title()} • {item.author[:20] if item.author else 'Unknown'} • {time_ago(item.timestamp)}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_trade_history():
    """Render trade history table."""
    st.markdown("### 📜 Trade History")
    
    engine = get_trading_engine()
    
    if not engine.trade_history:
        st.info("No trades executed yet")
        return
    
    # Build trade history dataframe
    trades_data = []
    for trade in engine.trade_history[-20:][::-1]:
        trades_data.append({
            'ID': trade.id,
            'Action': trade.signal.action.value,
            'Price': f"${trade.executed_price:.2f}" if trade.executed_price else "N/A",
            'P&L': format_currency(trade.profit_loss) if trade.profit_loss else "Open",
            'P&L %': format_percent(trade.profit_loss_percent) if trade.profit_loss_percent else "-",
            'Status': trade.status.value,
            'Time': trade.executed_at.strftime('%Y-%m-%d %H:%M') if trade.executed_at else "N/A"
        })
    
    df = pd.DataFrame(trades_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def main():
    """Main application entry point."""
    load_custom_css()
    init_session_state()
    
    render_header()
    render_sidebar()
    
    st.divider()
    
    # Main content area
    render_market_overview()
    
    st.divider()
    
    # Sentiment and Signal columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_sentiment_dashboard()
    
    with col2:
        render_trading_signal()
    
    st.divider()
    
    render_portfolio()
    
    st.divider()
    
    # News and History tabs
    tab1, tab2 = st.tabs(["📰 News Feed", "📜 Trade History"])
    
    with tab1:
        render_recent_news()
    
    with tab2:
        render_trade_history()
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        time.sleep(300)  # 5 minutes
        run_analysis()
        st.rerun()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #8b8b9a; padding: 1rem 0;">
        ⚠️ <strong>Disclaimer:</strong> This is for educational purposes only. Do not trade real money without extensive testing.
        <br>
        Built with ❤️ using Streamlit & Ollama
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
