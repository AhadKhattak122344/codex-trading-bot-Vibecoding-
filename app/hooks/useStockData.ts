'use client';
import { useEffect, useState } from 'react';
import type { AggregatedStockData } from '../types';

export function useStockData(symbol: string) {
  const [data, setData] = useState<AggregatedStockData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/data/${symbol}`)
      .then(res => res.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, [symbol]);

  return { data, loading };
}
