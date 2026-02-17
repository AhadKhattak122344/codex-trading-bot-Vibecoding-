import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';
import { incrementHashBy } from './cache';

const openai = process.env.OPENAI_API_KEY ? new OpenAI({ apiKey: process.env.OPENAI_API_KEY }) : null;
const anthropic = process.env.ANTHROPIC_API_KEY ? new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY }) : null;

async function trackUsage(model: string, input: number, output: number) {
  const key = `ai-usage:${new Date().toISOString().slice(0, 10)}`;
  await incrementHashBy(key, `${model}:input`, input);
  await incrementHashBy(key, `${model}:output`, output);
}

export async function callOpenAI(prompt: string): Promise<string> {
  if (!openai) throw new Error('OPENAI_API_KEY missing');
  const result = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }]
  });
  const text = result.choices[0]?.message.content ?? '';
  await trackUsage('gpt-4o', result.usage?.prompt_tokens ?? 0, result.usage?.completion_tokens ?? 0);
  return text;
}

export async function callAnthropic(prompt: string): Promise<string> {
  if (!anthropic) throw new Error('ANTHROPIC_API_KEY missing');
  const result = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1000,
    messages: [{ role: 'user', content: prompt }]
  });
  const text = result.content[0]?.type === 'text' ? result.content[0].text : '';
  await trackUsage('claude-sonnet-4-20250514', result.usage.input_tokens, result.usage.output_tokens);
  return text;
}
