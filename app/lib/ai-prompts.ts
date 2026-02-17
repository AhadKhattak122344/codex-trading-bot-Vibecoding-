import type { AggregatedStockData, Strategy } from '../types';

export function buildAiPrompt(data: AggregatedStockData, strategies: Strategy[]): string {
  const headlines = data.news.slice(0, 5).map(item => `- ${item.headline} (${item.source}, ${item.date})`).join('\n');
  const list = strategies.map(s => `- ${s.type}: max profit $${s.maxProfit.toFixed(2)}, max loss $${s.maxLoss.toFixed(2)}, POP ${s.pop.toFixed(2)}%`).join('\n');

  return `You are an expert options trader. Analyze ${data.symbol}.\nCurrent Price: $${data.price.toFixed(2)}\nIV: ${data.iv.toFixed(2)}%\nHV30: ${data.hv30.toFixed(2)}%\nIV Rank: ${data.ivRank.toFixed(2)}%\nEarnings: ${data.earningsDate ?? 'N/A'}\nMarket Status: ${data.marketStatus}\nNews:\n${headlines}\nAnalyst Ratings Buy/Hold/Sell: ${data.ratings.buy}/${data.ratings.hold}/${data.ratings.sell}\nStrategies:\n${list}\nReturn JSON with {sentiment,recommendation,confidence,strategy,reasoning,risks} then explanation.`;
}
