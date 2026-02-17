export interface AiPanelResult {
  provider: 'openai' | 'anthropic';
  status: 'fulfilled' | 'rejected';
  rawText: string;
  error?: string;
}
