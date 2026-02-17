# OptionSense AI

OptionSense AI is a Next.js 14 + TypeScript options dashboard for Alpaca paper trading, with market aggregation, options strategy ranking, and parallel AI analysis from OpenAI + Anthropic.

## Stack
- Next.js App Router + TypeScript strict mode
- Tailwind CSS (dark mode default)
- Alpaca Markets (paper trading)
- Finnhub + Yahoo Finance
- OpenAI `gpt-4o` + Anthropic `claude-sonnet-4-20250514`
- Upstash/Vercel KV caching
- Recharts visualizations
- Vitest unit tests

## Quick Start
1. Use Node 18+ and pnpm.
2. Install dependencies:
   ```bash
   pnpm install
   ```
3. Configure environment variables:
   ```bash
   cp .env.example .env.local
   ```
4. Run development server:
   ```bash
   pnpm dev
   ```
5. Open `http://localhost:3000`.

## Required Environment Variables
See `.env.example`:
- `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `ALPACA_BASE_URL`, `ALPACA_DATA_URL`
- `FINNHUB_API_KEY`
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
- `KV_REST_API_URL`, `KV_REST_API_TOKEN`
- `CRON_SECRET`
- `API_SECRET`

## API Routes
- `/api/stocks` S&P 500 list (fallback sample set)
- `/api/data/[symbol]` aggregated data (price, HV, news, ratings)
- `/api/options/[symbol]` chain + generated sample strategies
- `/api/ai/[symbol]` parallel AI calls via `Promise.allSettled`
- `/api/trade` place paper order
- `/api/trade/[orderId]` order status/cancel
- `/api/account` Alpaca account
- `/api/positions` open positions
- `/api/watchlist` KV-backed watchlist CRUD
- `/api/cron/iv-snapshot` weekly IV snapshot (protected by `CRON_SECRET`)
- `/api/cron/equity-snapshot` daily equity snapshot (protected by `CRON_SECRET`)

## Testing
```bash
pnpm test
```

Covers:
- Black-Scholes Greeks
- OCC symbol builder
- Strategy generation
- Risk validation

## Deployment
- Deploy to Vercel.
- `vercel.json` already defines weekly/daily cron jobs.
- Ensure Alpaca options permissions are enabled for your paper account.

## Notes
- This app targets US equity options only.
- No real-money trading is implemented.
- Monetary values should be formatted to 2 decimals in UI; Greeks to 4 decimals where displayed.
