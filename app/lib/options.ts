import type { OptionContract, Strategy } from '../types';

export function generateCreditSpreads(symbol: string, underlyingPrice: number, contracts: OptionContract[]): Strategy[] {
  const puts = contracts.filter(c => c.type === 'put' && c.delta <= 0.35 && c.delta >= 0.15 && c.openInterest >= 100);
  const output: Strategy[] = [];

  for (const shortLeg of puts.filter(p => p.delta <= 0.32 && p.delta >= 0.28)) {
    const longLeg = puts.find(p => p.expiration === shortLeg.expiration && p.strike < shortLeg.strike && p.delta <= 0.22 && p.delta >= 0.18);
    if (!longLeg) continue;
    const credit = shortLeg.bid - longLeg.ask;
    if (credit <= 0.1) continue;
    const width = shortLeg.strike - longLeg.strike;
    const maxLoss = width - credit;
    output.push({
      id: `${symbol}-${shortLeg.expiration}-${shortLeg.strike}-${longLeg.strike}`,
      type: 'bull_put_spread',
      expiration: shortLeg.expiration,
      maxProfit: credit * 100,
      maxLoss: maxLoss * 100,
      pop: (1 - Math.abs(shortLeg.delta)) * 100,
      returnOnRisk: (credit / maxLoss) * 100,
      annualizedReturn: ((credit / maxLoss) * (365 / Math.max(1, shortLeg.dte))) * 100,
      breakevens: [shortLeg.strike - credit],
      legs: [
        { symbol: shortLeg.symbol, side: 'sell', quantity: 1 },
        { symbol: longLeg.symbol, side: 'buy', quantity: 1 }
      ],
      marginRequirement: maxLoss * 100,
      underlyingPrice
    });
  }

  return output.slice(0, 5);
}
