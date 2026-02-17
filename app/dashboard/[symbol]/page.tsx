'use client';

import { useStockData } from '../../hooks/useStockData';
import { AiResponseCard } from '../../components/ai/ai-response-card';

export default function SymbolPage({ params }: { params: { symbol: string } }) {
  const { data, loading } = useStockData(params.symbol);
  if (loading) return <div className="animate-pulse">Loading data...</div>;
  if (!data) return <div>No data</div>;

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold">{data.symbol} Detail</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-slate-800 p-4">Price: ${data.price.toFixed(2)}</div>
        <div className="rounded-lg border border-slate-800 p-4">IV/HV: {data.iv.toFixed(2)} / {data.hv30.toFixed(2)}</div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <AiResponseCard title="ChatGPT" text="Awaiting AI analysis." />
        <AiResponseCard title="Claude" text="Awaiting AI analysis." />
      </div>
    </section>
  );
}
