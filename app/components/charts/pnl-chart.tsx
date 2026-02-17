'use client';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export function PnlChart({ data, breakeven }: { data: { price: number; pnl: number }[]; breakeven: number }) {
  return (
    <div className="h-64 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="price" />
          <YAxis />
          <Tooltip />
          <ReferenceLine x={breakeven} strokeDasharray="4 4" />
          <Line type="monotone" dataKey="pnl" stroke="#22c55e" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
