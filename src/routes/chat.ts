/**
 * Chat Routes - Multi-model chat API
 */

import { Router, Request, Response } from 'express';
import { modelRouter } from '../services/model-router';
import { requestPermissions } from '../services/permission-engine';
import { scanSafety } from '../services/safety-guard';
import { logUsage } from '../services/usage-tracker';
import { getAllCapabilities, getCapabilityById } from '../services/capability-registry';
import { AuthRequest } from '../middleware/auth';

const MAX_MESSAGE_LENGTH = 4000;

const ALLOWED_CAPABILITY_IDS = new Set(getAllCapabilities().map(c => c.id));
const DOMAIN_ROUTED_CAPABILITIES = new Set(getAllCapabilities().filter(c => c.default_provider === 'ascension-native').map(c => c.id));

function isValidCapabilityId(capabilityId: any): boolean {
  return typeof capabilityId === 'string' && ALLOWED_CAPABILITY_IDS.has(capabilityId);
}

function isValidMessage(message: any): { valid: boolean; error?: string } {
  if (typeof message !== 'string') {
    return { valid: false, error: 'Message must be a string' };
  }
  const trimmed = message.trim();
  if (trimmed.length === 0) {
    return { valid: false, error: 'Message cannot be empty' };
  }
  if (trimmed.length > MAX_MESSAGE_LENGTH) {
    return { valid: false, error: `Message cannot exceed ${MAX_MESSAGE_LENGTH} characters` };
  }
  return { valid: true };
}

const router = Router();

/**
 * POST /api/v1/chat
 * Send a chat message and get AI response
 */
router.post('/', async (req: AuthRequest, res: Response) => {
  try {
    const { message, capabilityId } = req.body;

    const messageCheck = isValidMessage(message);
    if (!messageCheck.valid) {
      return res.status(400).json({ error: messageCheck.error });
    }

    if (capabilityId !== undefined && !isValidCapabilityId(capabilityId)) {
      return res.status(400).json({ error: 'Invalid capability ID' });
    }

    const safety = scanSafety(message, { shell: 'ap', capability: capabilityId || 'ascension_chat' });
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

    if (!isValidCapabilityId(capabilityId)) {
      return res.status(400).json({ error: 'Invalid or missing capability ID' });
    }

    const messageCheck = isValidMessage(message);
    if (!messageCheck.valid) {
      return res.status(400).json({ error: messageCheck.error });
    }

    const capability = getCapabilityById(capabilityId);
    if (!capability) {
      return res.status(400).json({ error: 'Capability not found' });
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
      if (DOMAIN_ROUTED_CAPABILITIES.has(capabilityId)) {
        const { routeNativeDomain } = await import('../services/native-domain-router');
        const nativeResponse = routeNativeDomain(capabilityId, message, permissions as any);
        return res.json({
          ...nativeResponse,
          capabilityId,
          durationMs: Date.now() - startTime
        });
      }
      return res.status(404).json({ error: `Capability ${capabilityId} has no native route` });
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
