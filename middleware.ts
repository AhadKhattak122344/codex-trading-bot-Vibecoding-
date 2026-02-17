import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/api/cron')) {
    return NextResponse.next();
  }

  if (request.nextUrl.pathname.startsWith('/api')) {
    const response = NextResponse.next();
    response.headers.set('Access-Control-Allow-Origin', '*');
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, x-api-secret, authorization');
    response.headers.set('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS');
    return response;
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/api/:path*']
};
