/**
 * Chat Routes - Multi-model chat API
 */

import { Router, Request, Response } from 'express';
import { modelRouter } from '../services/model-router';
import { logUsage } from '../services/usage-tracker';
import { AuthRequest } from '../middleware/auth';

const router = Router();

/**
 * POST /api/v1/chat
 * Send a chat message and get AI response
 */
router.post('/', async (req: AuthRequest, res: Response) => {
  try {
    const { message, capabilityId } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message required' });
    }
    
    const startTime = Date.now();
    
    // Prefer native chat if enabled and no explicit capability requested
    const defaultCapability = process.env.ASCENSION_NATIVE_ENABLED === 'true' && !capabilityId
      ? 'ascension_chat'
      : capabilityId || 'chat_gpt4';
    
    // Route to best provider
    const routingDecision = await modelRouter.route(defaultCapability, req.user?.tier || 'individual');
    
    // Execute request
    const response = await modelRouter.execute(routingDecision, {
      messages: [{ role: 'user', content: message }]
    });
    
    const durationMs = Date.now() - startTime;
    
    // Log usage
    await logUsage(req.user?.id!, {
      modelProvider: routingDecision.provider as any,
      modelName: routingDecision.model,
      requestType: 'chat',
      tokensUsed: response.tokensUsed,
      costCents: Math.ceil(response.tokensUsed * 0.03),
      durationMs
    });
    
    res.json({
      content: response.content,
      model: response.model,
      provider: response.provider,
      capabilityId: defaultCapability,
      tokensUsed: response.tokensUsed,
      costCents: Math.ceil(response.tokensUsed * 0.03),
      durationMs
    });
  } catch (error: any) {
    console.error('Chat error:', error);
    res.status(500).json({ error: error.message || 'Chat failed' });
  }
});

/**
 * POST /api/v1/chat/capability
 * Use a specific capability
 */
router.post('/capability', async (req: AuthRequest, res: Response) => {
  try {
    const { capabilityId, message } = req.body;
    
    if (!capabilityId || !message) {
      return res.status(400).json({ error: 'Capability ID and message required' });
    }
    
    const startTime = Date.now();
    
    // Route to best provider for capability
    const routingDecision = await modelRouter.route(capabilityId, req.user?.tier || 'individual');
    
    // Execute request
    const response = await modelRouter.execute(routingDecision, {
      messages: [{ role: 'user', content: message }]
    });
    
    const durationMs = Date.now() - startTime;
    
    // Log usage
    await logUsage(req.user?.id!, {
      modelProvider: routingDecision.provider as any,
      modelName: routingDecision.model,
      requestType: 'chat',
      tokensUsed: response.tokensUsed,
      costCents: Math.ceil(response.tokensUsed * 0.03),
      durationMs
    });
    
    res.json({
      content: response.content,
      model: response.model,
      provider: response.provider,
      capabilityId,
      tokensUsed: response.tokensUsed,
      costCents: Math.ceil(response.tokensUsed * 0.03),
      durationMs
    });
  } catch (error: any) {
    console.error('Capability chat error:', error);
    res.status(500).json({ error: error.message || 'Capability chat failed' });
  }
});

export default router;
