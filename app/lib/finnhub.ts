const BASE = 'https://finnhub.io/api/v1';

export async function fetchFinnhub(path: string, params: Record<string, string>): Promise<any> {
  const url = new URL(`${BASE}${path}`);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  url.searchParams.set('token', process.env.FINNHUB_API_KEY ?? '');
  const response = await fetch(url, { next: { revalidate: 300 } });
  if (!response.ok) throw new Error(`Finnhub error ${response.status}`);
  return response.json();
}
