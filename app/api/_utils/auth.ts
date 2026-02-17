import { NextRequest } from 'next/server';

export function checkApiSecret(req: NextRequest): boolean {
  const expected = process.env.API_SECRET;
  if (!expected) return true;
  return req.headers.get('x-api-secret') === expected;
}

export function checkCronSecret(req: NextRequest): boolean {
  const expected = process.env.CRON_SECRET;
  if (!expected) return true;
  return req.headers.get('authorization') === `Bearer ${expected}`;
}
