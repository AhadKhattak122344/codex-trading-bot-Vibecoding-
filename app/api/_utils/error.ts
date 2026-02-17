export function logApiError(context: Record<string, unknown>, error: unknown) {
  console.error({
    ...context,
    error: error instanceof Error ? error.message : String(error),
    timestamp: new Date().toISOString()
  });
}
