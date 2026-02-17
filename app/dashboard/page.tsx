import Link from 'next/link';

export default function DashboardPage() {
  const watchlist = ['SPY', 'AAPL', 'MSFT'];
  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold">OptionSense AI Dashboard</h1>
      <p className="text-sm text-slate-400">Dark-mode default dashboard with watchlist and AI insights.</p>
      <div className="grid gap-3 md:grid-cols-3">
        {watchlist.map(symbol => (
          <Link key={symbol} href={`/dashboard/${symbol}`} className="rounded-lg border border-slate-800 p-4 hover:border-slate-600">
            <h2 className="font-medium">{symbol}</h2>
            <p className="text-xs text-slate-400">IV Rank: 50% · Earnings: 14d</p>
          </Link>
        ))}
      </div>
    </section>
  );
}
