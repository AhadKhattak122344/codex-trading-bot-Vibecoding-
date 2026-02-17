import { describe, it, expect } from 'vitest';
import { buildOccSymbol } from '../app/lib/occ-symbol';

describe('buildOccSymbol', () => {
  it('builds OCC symbol', () => {
    expect(buildOccSymbol('SPY', '2024-09-20', 'P', 450)).toBe('SPY240920P00450000');
  });
});
