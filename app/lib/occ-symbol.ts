export function buildOccSymbol(
  underlying: string,
  expiration: string,
  type: 'C' | 'P',
  strike: number
): string {
  const root = underlying.toUpperCase().padEnd(6, ' ');
  const date = expiration.replaceAll('-', '').slice(2);
  const strikePart = String(Math.round(strike * 1000)).padStart(8, '0');
  return `${root}${date}${type}${strikePart}`.replaceAll(' ', '');
}
