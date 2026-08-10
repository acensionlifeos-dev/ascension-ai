/**
 * Authentication Middleware
 * Validates API keys and extracts user tier
 */

import { Request, Response, NextFunction } from 'express';
import pool from '../models/database';

export interface AuthRequest extends Request {
  user?: {
    id: number;
    email: string;
    tier: string;
  };
}

export async function authMiddleware(req: AuthRequest, res: Response, next: NextFunction) {
  const apiKey = req.headers['x-api-key'] as string;
  
  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }
  
  try {
    const result = await pool.query(
      'SELECT id, email, tier FROM users WHERE api_key = $1',
      [apiKey]
    );
    
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Invalid API key' });
    }
    
    req.user = result.rows[0];
    next();
  } catch (error) {
    console.error('Auth error:', error);
    res.status(500).json({ error: 'Authentication failed' });
  }
}
