import { NextRequest, NextResponse } from 'next/server';
import { checkCronSecret } from '../../_utils/auth';
import { alpaca } from '../../../lib/alpaca';
import { setCache } from '../../../lib/cache';

export async function GET(req: NextRequest) {
  if (!checkCronSecret(req)) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  const acct = await alpaca.getAccount();
  const today = new Date().toISOString().slice(0, 10);
  await setCache(`equity:${today}`, Number(acct.equity), 86400 * 400);
  return NextResponse.json({ ok: true });
}
