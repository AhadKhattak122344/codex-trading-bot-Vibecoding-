import { DEFAULT_RISK } from './constants';

export function validateRisk({
  equity,
  estimatedMargin,
  dailyPnl,
  maxPositionSizePct = DEFAULT_RISK.maxPositionSizePct,
  maxDailyLossPct = DEFAULT_RISK.maxDailyLossPct
}: {
  equity: number;
  estimatedMargin: number;
  dailyPnl: number;
  maxPositionSizePct?: number;
  maxDailyLossPct?: number;
}) {
  const maxPositionDollars = (equity * maxPositionSizePct) / 100;
  const maxDailyLossDollars = (equity * maxDailyLossPct) / 100;

  return {
    withinPositionLimit: estimatedMargin <= maxPositionDollars,
    withinDailyLossLimit: Math.abs(dailyPnl) <= maxDailyLossDollars,
    maxPositionDollars,
    maxDailyLossDollars
  };
}
