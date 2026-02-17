import { describe, it, expect } from 'vitest';
import { generateCreditSpreads } from '../app/lib/options';

describe('generateCreditSpreads', () => {
  it('creates at least one spread when contracts are eligible', () => {
    const result = generateCreditSpreads('SPY', 500, [
      { symbol: 'A', type: 'put', strike: 500, expiration: '2026-10-10', delta: 0.3, bid: 2.2, ask: 2.3, openInterest: 300, dte: 30 },
      { symbol: 'B', type: 'put', strike: 495, expiration: '2026-10-10', delta: 0.2, bid: 1.1, ask: 1.2, openInterest: 300, dte: 30 }
    ]);
    expect(result.length).toBe(1);
  });
});
