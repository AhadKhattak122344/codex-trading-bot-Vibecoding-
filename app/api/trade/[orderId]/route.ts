import { NextRequest, NextResponse } from 'next/server';
import { alpaca } from '../../../lib/alpaca';

export async function GET(_req: NextRequest, { params }: { params: { orderId: string } }) {
  const order = await alpaca.getOrder(params.orderId);
  return NextResponse.json(order);
}

export async function DELETE(_req: NextRequest, { params }: { params: { orderId: string } }) {
  await alpaca.cancelOrder(params.orderId);
  return NextResponse.json({ cancelled: true });
}
