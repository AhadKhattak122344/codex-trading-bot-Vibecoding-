import { describe, it, expect } from 'vitest';
import { validateRisk } from '../app/lib/risk';

describe('validateRisk', () => {
  it('flags position over limit', () => {
    const result = validateRisk({ equity: 10000, estimatedMargin: 1200, dailyPnl: -100 });
    expect(result.withinPositionLimit).toBe(false);
  });
});
