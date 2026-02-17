import { NextRequest, NextResponse } from 'next/server';
import { tradeSchema } from '../_utils/validation';
import { alpaca } from '../../lib/alpaca';

export async function POST(req: NextRequest) {
  const payload = tradeSchema.parse(await req.json());
  const order = await alpaca.createOrder(payload as any);
  return NextResponse.json(order);
}
