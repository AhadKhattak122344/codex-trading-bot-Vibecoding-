import yahooFinance from 'yahoo-finance2';

export async function getYahooHistory(symbol: string, days = 100) {
  const period1 = new Date(Date.now() - days * 24 * 60 * 60 * 1000);
  return yahooFinance.historical(symbol, { period1, interval: '1d' });
}
