export const CACHE_TTL = {
  prices: 30,
  news: 60 * 5,
  options: 60 * 60,
  ai: 60 * 15
} as const;

export const DEFAULT_RISK = {
  maxPositionSizePct: 10,
  maxDailyLossPct: 5
} as const;
