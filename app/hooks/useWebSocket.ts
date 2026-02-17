'use client';
import { useEffect, useState } from 'react';

export function useWebSocket(_symbol: string) {
  const [connected, setConnected] = useState(false);
  useEffect(() => {
    setConnected(false);
    const timer = setTimeout(() => setConnected(true), 500);
    return () => clearTimeout(timer);
  }, []);
  return { connected };
}
