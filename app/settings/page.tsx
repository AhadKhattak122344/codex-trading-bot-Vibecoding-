export default function SettingsPage() {
  const flags = [
    ['ALPACA_API_KEY', Boolean(process.env.ALPACA_API_KEY)],
    ['FINNHUB_API_KEY', Boolean(process.env.FINNHUB_API_KEY)],
    ['OPENAI_API_KEY', Boolean(process.env.OPENAI_API_KEY)],
    ['ANTHROPIC_API_KEY', Boolean(process.env.ANTHROPIC_API_KEY)]
  ];

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold">Settings</h1>
      {flags.map(([name, ok]) => (
        <div key={name} className="flex items-center gap-2 text-sm">
          <span className={`h-2.5 w-2.5 rounded-full ${ok ? 'bg-emerald-400' : 'bg-red-500'}`} />
          {name}
        </div>
      ))}
    </section>
  );
}
