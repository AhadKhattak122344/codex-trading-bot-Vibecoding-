import { NextRequest, NextResponse } from 'next/server';
import { buildAiPrompt } from '../../../lib/ai-prompts';
import { callAnthropic, callOpenAI } from '../../../lib/ai-clients';
import { generateCreditSpreads } from '../../../lib/options';
import { buildOccSymbol } from '../../../lib/occ-symbol';

export async function GET(_req: NextRequest, { params }: { params: { symbol: string } }) {
  const symbol = params.symbol.toUpperCase();
  const expiration = new Date(Date.now() + 35 * 86400000).toISOString().slice(0, 10);
  const data = {
    symbol,
    price: 500,
    iv: 24,
    hv30: 18,
    ivRank: 55,
    marketStatus: 'Closed' as const,
    news: [],
    ratings: { buy: 10, hold: 5, sell: 1 }
  };
  const strategies = generateCreditSpreads(symbol, 500, [
    { symbol: buildOccSymbol(symbol, expiration, 'P', 490), type: 'put', strike: 490, expiration, delta: 0.3, bid: 2.1, ask: 2.2, openInterest: 500, dte: 35 },
    { symbol: buildOccSymbol(symbol, expiration, 'P', 485), type: 'put', strike: 485, expiration, delta: 0.2, bid: 1.2, ask: 1.3, openInterest: 510, dte: 35 }
  ]);
  const prompt = buildAiPrompt(data, strategies);
  const [chatGPTResponse, claudeResponse] = await Promise.allSettled([callOpenAI(prompt), callAnthropic(prompt)]);
  return NextResponse.json({ chatGPTResponse, claudeResponse });
}
