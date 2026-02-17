import { describe, it, expect } from 'vitest';
import { calculateGreeks } from '../app/lib/black-scholes';

describe('calculateGreeks', () => {
  it('returns finite values', () => {
    const values = calculateGreeks({ spot: 100, strike: 100, rate: 0.05, volatility: 0.2, timeToExpiry: 30 / 365, isCall: true });
    expect(Number.isFinite(values.delta)).toBe(true);
    expect(Number.isFinite(values.gamma)).toBe(true);
    expect(Number.isFinite(values.theta)).toBe(true);
    expect(Number.isFinite(values.vega)).toBe(true);
    expect(Number.isFinite(values.rho)).toBe(true);
  });
});
