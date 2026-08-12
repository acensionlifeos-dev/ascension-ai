/**
 * Chat Routes - Multi-model chat API
 */

import { Router, Request, Response } from 'express';
import { modelRouter } from '../services/model-router';
import { requestPermissions } from '../services/permission-engine';
import { routeNativeDomain } from '../services/native-domain-router';
import { scanSafety } from '../services/safety-guard';
import { logUsage } from '../services/usage-tracker';
import { AuthRequest } from '../middleware/auth';

const DOMAIN_ROUTED_CAPABILITIES = new Set([
  'ascension_travel',
  'ascension_legal',
  'ascension_realestate',
  'ascension_research',
  'ascension_events',
  'ascension_automotive',
  'ascension_pets',
  'ascension_weather',
  'ascension_finance',
  'ascension_trading',
  'ascension_health',
  'ascension_home',
  'ascension_sprout',
  'ascension_family',
  'ascension_chat',
  'ascension_nutrition',
  'ascension_fitness',
  'ascension_career',
  'ascension_relationships',
  'ascension_creative',
  'ascension_code',
  'ascension_learning',
  'ascension_meetings',
  'ascension_voice',
  'ascension_security',
  'ascension_psychology',
  'ascension_human_life',
  'ascension_spirituality',
  'ascension_grief',
  'ascension_mental_health',
  'ascension_communication',
  'ascension_habits',
  'ascension_stress',
  'ascension_sleep',
  'ascension_parenting',
  'ascension_mindfulness',
  'ascension_time',
  'ascension_confidence',
  'ascension_aging',
  'ascension_addiction',
  'ascension_conflict',
  'ascension_dating',
  'ascension_cooking',
  'ascension_social',
  'ascension_volunteering'
]);

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
    
    const safety = scanSafety(message, { shell: 'ap', capability: capabilityId });
    if (safety.action === 'escalate' || safety.action === 'block') {
      return res.status(safety.level === 'critical' ? 200 : 400).json({
        type: 'safety',
        ...safety,
        capabilityId: capabilityId || 'ascension_chat'
      });
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
    const { capabilityId, message, permissions = {} } = req.body;
    
    if (!capabilityId || !message) {
      return res.status(400).json({ error: 'Capability ID and message required' });
    }
    
    const safety = scanSafety(message, { shell: 'ap', capability: capabilityId });
    if (safety.action === 'escalate' || safety.action === 'block') {
      return res.status(safety.level === 'critical' ? 200 : 400).json({
        type: 'safety',
        ...safety,
        capabilityId
      });
    }
    
    const startTime = Date.now();
    
    // AP asks for the permissions it knows it needs before acting
    const permissionRequest = requestPermissions(capabilityId, permissions as any);
    
    if (!permissionRequest.can_execute) {
      return res.json({
        type: 'permission_request',
        capabilityId,
        ...permissionRequest,
        durationMs: Date.now() - startTime
      });
    }
    
    // Fast, structured native domain response for specialized overlays
    if (capabilityId.startsWith('ascension_') && process.env.ASCENSION_NATIVE_ENABLED === 'true') {
      const nativeResponse = routeNativeDomain(capabilityId, message, permissions as any);
      if (DOMAIN_ROUTED_CAPABILITIES.has(capabilityId)) {
        return res.json({
          ...nativeResponse,
          capabilityId,
          durationMs: Date.now() - startTime
        });
      }
    }
    
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
