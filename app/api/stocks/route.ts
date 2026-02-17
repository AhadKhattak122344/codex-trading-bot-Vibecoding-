import { NextResponse } from 'next/server';

const SP500_FALLBACK = ['AAPL', 'MSFT', 'NVDA', 'SPY', 'AMZN', 'META', 'GOOGL', 'TSLA'];

export async function GET() {
  return NextResponse.json({ symbols: SP500_FALLBACK, source: 'fallback' });
}
