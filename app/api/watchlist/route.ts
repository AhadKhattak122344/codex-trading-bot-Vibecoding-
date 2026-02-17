import { NextRequest, NextResponse } from 'next/server';
import { getCache, setCache } from '../../lib/cache';

const KEY = 'watchlist';

export async function GET() {
  const symbols = (await getCache<string[]>(KEY)) ?? ['SPY'];
  return NextResponse.json({ symbols });
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const current = (await getCache<string[]>(KEY)) ?? [];
  const symbols = [...new Set([...current, String(body.symbol).toUpperCase()])];
  await setCache(KEY, symbols, 86400 * 30);
  return NextResponse.json({ symbols });
}

export async function DELETE(req: NextRequest) {
  const body = await req.json();
  const current = (await getCache<string[]>(KEY)) ?? [];
  const symbols = current.filter(s => s !== String(body.symbol).toUpperCase());
  await setCache(KEY, symbols, 86400 * 30);
  return NextResponse.json({ symbols });
}
