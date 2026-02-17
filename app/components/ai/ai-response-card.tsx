'use client';
import ReactMarkdown from 'react-markdown';

export function AiResponseCard({ title, text }: { title: string; text: string }) {
  return (
    <article className="rounded-xl border border-slate-800 p-4">
      <h3 className="mb-2 font-semibold">{title}</h3>
      <div className="prose prose-invert max-w-none text-sm">
        <ReactMarkdown>{text}</ReactMarkdown>
      </div>
    </article>
  );
}
