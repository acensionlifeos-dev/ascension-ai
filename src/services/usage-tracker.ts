/**
 * Usage Tracker - Logs usage for monitoring (no limits)
 */

import pool from '../models/database';

export interface UsageLogData {
  modelProvider: 'openai' | 'anthropic' | 'google' | 'midjourney' | 'elevenlabs' | 'suno' | 'runway' | 'luma' | 'stability' | 'custom';
  modelName: string;
  requestType: 'chat' | 'image' | 'code' | 'audio' | 'video' | 'data' | 'web' | 'business' | 'social' | 'health' | 'intelligence';
  tokensUsed: number;
  costCents: number;
  durationMs: number;
}

export async function logUsage(userId: number, data: UsageLogData) {
  try {
    await pool.query(
      `INSERT INTO usage_logs (
         user_id,
         model_provider,
         model_name,
         request_type,
         tokens_used,
         cost_cents,
         duration_ms
       ) VALUES ($1, $2, $3, $4, $5, $6, $7)`,
      [
        userId,
        data.modelProvider,
        data.modelName,
        data.requestType,
        data.tokensUsed,
        data.costCents,
        data.durationMs
      ]
    );
    
    // Update daily summary
    await updateDailySummary(userId, data);
  } catch (error) {
    console.error('Usage log error:', error);
    // Don't throw - usage logging shouldn't break the main flow
  }
}

async function updateDailySummary(userId: number, data: UsageLogData) {
  const today = new Date().toISOString().split('T')[0];
  
  try {
    await pool.query(
      `INSERT INTO daily_usage_summaries (
         user_id,
         date,
         total_requests,
         total_tokens,
         total_cost_cents
       ) VALUES ($1, $2, 1, $3, $4)
       ON CONFLICT (user_id, date)
       DO UPDATE SET
         total_requests = daily_usage_summaries.total_requests + 1,
         total_tokens = daily_usage_summaries.total_tokens + $3,
         total_cost_cents = daily_usage_summaries.total_cost_cents + $4`,
      [
        userId,
        today,
        data.tokensUsed,
        data.costCents
      ]
    );
  } catch (error) {
    console.error('Daily summary update error:', error);
  }
}
