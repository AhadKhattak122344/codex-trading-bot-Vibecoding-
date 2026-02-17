import './globals.css';
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'OptionSense AI',
  description: 'Options trading dashboard with AI sentiment analysis'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>
        <header className="border-b border-slate-800 p-4">
          <nav className="mx-auto flex max-w-7xl gap-4 text-sm">
            <Link href="/dashboard">Dashboard</Link>
            <Link href="/portfolio">Portfolio</Link>
            <Link href="/settings">Settings</Link>
          </nav>
        </header>
        <main className="mx-auto max-w-7xl p-4">{children}</main>
      </body>
    </html>
  );
}
