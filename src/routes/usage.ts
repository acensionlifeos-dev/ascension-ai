/**
 * Usage Routes - Get usage statistics
 */

import { Router, Response } from 'express';
import pool from '../models/database';
import { AuthRequest } from '../middleware/auth';

const router = Router();

/**
 * GET /api/v1/usage
 * Get user's usage statistics
 */
router.get('/', async (req: AuthRequest, res: Response) => {
  try {
    const result = await pool.query(
      `SELECT 
         COUNT(*) as total_requests,
         SUM(tokens_used) as total_tokens,
         SUM(cost_cents) as total_cost_cents,
         AVG(duration_ms) as avg_duration_ms
       FROM usage_logs
       WHERE user_id = $1`,
      [req.user?.id]
    );
    
    res.json({ usage: result.rows[0] });
  } catch (error) {
    console.error('Usage query error:', error);
    res.status(500).json({ error: 'Failed to get usage' });
  }
});

/**
 * GET /api/v1/usage/daily
 * Get daily usage summary
 */
router.get('/daily', async (req: AuthRequest, res: Response) => {
  try {
    const result = await pool.query(
      `SELECT * FROM daily_usage_summaries
       WHERE user_id = $1
       ORDER BY date DESC
       LIMIT 30`,
      [req.user?.id]
    );
    
    res.json({ dailyUsage: result.rows });
  } catch (error) {
    console.error('Daily usage query error:', error);
    res.status(500).json({ error: 'Failed to get daily usage' });
  }
});

/**
 * GET /api/v1/usage/by-provider
 * Get usage by provider
 */
router.get('/by-provider', async (req: AuthRequest, res: Response) => {
  try {
    const result = await pool.query(
      `SELECT 
         model_provider,
         COUNT(*) as requests,
         SUM(tokens_used) as tokens,
         SUM(cost_cents) as cost_cents
       FROM usage_logs
       WHERE user_id = $1
       GROUP BY model_provider`,
      [req.user?.id]
    );
    
    res.json({ byProvider: result.rows });
  } catch (error) {
    console.error('Provider usage query error:', error);
    res.status(500).json({ error: 'Failed to get provider usage' });
  }
});

export default router;
