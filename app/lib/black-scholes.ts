const SQRT_2PI = Math.sqrt(2 * Math.PI);

function normalPdf(x: number): number {
  return Math.exp(-0.5 * x * x) / SQRT_2PI;
}

function erf(x: number): number {
  const sign = x >= 0 ? 1 : -1;
  const a1 = 0.254829592;
  const a2 = -0.284496736;
  const a3 = 1.421413741;
  const a4 = -1.453152027;
  const a5 = 1.061405429;
  const p = 0.3275911;
  const t = 1 / (1 + p * Math.abs(x));
  const y = 1 - (((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t) * Math.exp(-x * x);
  return sign * y;
}

function normalCdf(x: number): number {
  return 0.5 * (1 + erf(x / Math.sqrt(2)));
}

export function calculateGreeks({ spot, strike, rate, volatility, timeToExpiry, isCall }: {
  spot: number; strike: number; rate: number; volatility: number; timeToExpiry: number; isCall: boolean;
}) {
  const d1 = (Math.log(spot / strike) + (rate + (volatility ** 2) / 2) * timeToExpiry) / (volatility * Math.sqrt(timeToExpiry));
  const d2 = d1 - volatility * Math.sqrt(timeToExpiry);
  const delta = isCall ? normalCdf(d1) : normalCdf(d1) - 1;
  const gamma = normalPdf(d1) / (spot * volatility * Math.sqrt(timeToExpiry));
  const theta = -((spot * normalPdf(d1) * volatility) / (2 * Math.sqrt(timeToExpiry))) - (isCall ? rate * strike * Math.exp(-rate * timeToExpiry) * normalCdf(d2) : -rate * strike * Math.exp(-rate * timeToExpiry) * normalCdf(-d2));
  const vega = spot * normalPdf(d1) * Math.sqrt(timeToExpiry) / 100;
  const rho = (isCall ? strike * timeToExpiry * Math.exp(-rate * timeToExpiry) * normalCdf(d2) : -strike * timeToExpiry * Math.exp(-rate * timeToExpiry) * normalCdf(-d2)) / 100;
  return { delta, gamma, theta, vega, rho };
}
