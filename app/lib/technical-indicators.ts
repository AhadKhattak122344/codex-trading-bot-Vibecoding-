export function calculateHV(closes: number[], days: number): number {
  const subset = closes.slice(-days - 1);
  if (subset.length < 2) return 0;
  const logReturns = subset.slice(1).map((price, idx) => Math.log(price / subset[idx]));
  const mean = logReturns.reduce((sum, value) => sum + value, 0) / logReturns.length;
  const variance = logReturns.reduce((sum, value) => sum + (value - mean) ** 2, 0) / (logReturns.length - 1);
  return Math.sqrt(variance) * Math.sqrt(252) * 100;
}
