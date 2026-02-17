import { NextRequest, NextResponse } from 'next/server';
import { symbolSchema } from '../../_utils/validation';
import { generateCreditSpreads } from '../../../lib/options';
import { buildOccSymbol } from '../../../lib/occ-symbol';

export async function GET(_req: NextRequest, { params }: { params: { symbol: string } }) {
  const symbol = symbolSchema.parse(params.symbol);
  const expiration = new Date(Date.now() + 35 * 86400000).toISOString().slice(0, 10);
  const mockChain = [
    { symbol: buildOccSymbol(symbol, expiration, 'P', 500), type: 'put', strike: 500, expiration, delta: 0.3, bid: 2.2, ask: 2.3, openInterest: 300, dte: 35 },
    { symbol: buildOccSymbol(symbol, expiration, 'P', 495), type: 'put', strike: 495, expiration, delta: 0.2, bid: 1.3, ask: 1.4, openInterest: 350, dte: 35 }
  ];
  const strategies = generateCreditSpreads(symbol, 505, mockChain);
  return NextResponse.json({ symbol, chain: mockChain, strategies });
}
