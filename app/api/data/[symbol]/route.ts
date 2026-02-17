import { NextRequest, NextResponse } from 'next/server';
import { symbolSchema } from '../../_utils/validation';
import { logApiError } from '../../_utils/error';
import { fetchFinnhub } from '../../../lib/finnhub';
import { getYahooHistory } from '../../../lib/yahoo';
import { calculateHV } from '../../../lib/technical-indicators';

export async function GET(_req: NextRequest, { params }: { params: { symbol: string } }) {
  try {
    const symbol = symbolSchema.parse(params.symbol);
    const candles = await getYahooHistory(symbol, 100);
    const closes = candles.map(c => Number(c.close ?? 0)).filter(Boolean);
    const price = closes.at(-1) ?? 0;
    const hv30 = calculateHV(closes, 30);
    const news = await fetchFinnhub('/company-news', {
      symbol,
      from: new Date(Date.now() - 7 * 86400000).toISOString().slice(0, 10),
      to: new Date().toISOString().slice(0, 10)
    });
    const ratings = await fetchFinnhub('/stock/recommendation', { symbol });

    return NextResponse.json({
      symbol,
      price,
      iv: 25,
      hv30,
      ivRank: 50,
      marketStatus: 'Closed',
      earningsDate: undefined,
      news: (news ?? []).slice(0, 5).map((n: any) => ({ headline: n.headline, source: n.source, date: n.datetime, url: n.url })),
      ratings: ratings?.[0]
        ? { buy: ratings[0].buy, hold: ratings[0].hold, sell: ratings[0].sell }
        : { buy: 0, hold: 0, sell: 0 }
    });
  } catch (error) {
    logApiError({ route: '/api/data/[symbol]', symbol: params.symbol }, error);
    return NextResponse.json({ error: 'Failed to aggregate stock data' }, { status: 500 });
  }
}
