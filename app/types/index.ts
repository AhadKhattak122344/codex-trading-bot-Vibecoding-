export type MarketStatus = 'Market Open' | 'Pre-Market' | 'After Hours' | 'Closed';

export interface OptionContract {
  symbol: string;
  type: 'call' | 'put';
  strike: number;
  expiration: string;
  delta: number;
  bid: number;
  ask: number;
  openInterest: number;
  dte: number;
}

export interface Strategy {
  id: string;
  type: string;
  expiration: string;
  maxProfit: number;
  maxLoss: number;
  pop: number;
  returnOnRisk: number;
  annualizedReturn: number;
  breakevens: number[];
  legs: { symbol: string; side: 'buy' | 'sell'; quantity: number }[];
  marginRequirement: number;
  underlyingPrice: number;
}

export interface AggregatedStockData {
  symbol: string;
  price: number;
  iv: number;
  hv30: number;
  ivRank: number;
  marketStatus: MarketStatus;
  earningsDate?: string;
  news: { headline: string; source: string; date: string; url: string }[];
  ratings: { buy: number; hold: number; sell: number };
}
