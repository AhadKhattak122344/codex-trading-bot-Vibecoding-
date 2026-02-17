import { Redis } from '@upstash/redis';

const redis = process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN
  ? new Redis({ url: process.env.KV_REST_API_URL, token: process.env.KV_REST_API_TOKEN })
  : null;

export async function getCache<T>(key: string): Promise<T | null> {
  if (!redis) return null;
  return redis.get<T>(key);
}

export async function setCache<T>(key: string, value: T, ttlSeconds: number): Promise<void> {
  if (!redis) return;
  await redis.set(key, value, { ex: ttlSeconds });
}

export async function incrementHashBy(key: string, field: string, increment: number): Promise<void> {
  if (!redis) return;
  await redis.hincrbyfloat(key, field, increment);
}
