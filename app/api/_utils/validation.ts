import { z } from 'zod';

export const symbolSchema = z.string().trim().toUpperCase().regex(/^[A-Z0-9]{1,5}$/);

export const tradeSchema = z.object({
  symbol: symbolSchema,
  type: z.enum(['market', 'limit', 'stop_limit']),
  qty: z.number().int().positive(),
  limit_price: z.number().positive().optional(),
  stop_price: z.number().positive().optional(),
  legs: z.array(z.object({ symbol: z.string(), side: z.enum(['buy', 'sell']), ratio_qty: z.string() })).optional()
});
