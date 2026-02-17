import { NextResponse } from 'next/server';
import { alpaca } from '../../lib/alpaca';

export async function GET() {
  return NextResponse.json(await alpaca.getPositions());
}
