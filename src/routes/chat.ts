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
  'ascension_volunteering',
  'ascension_focus',
  'ascension_meditation',
  'ascension_garden',
  'ascension_fashion',
  'ascension_repair',
  'ascension_music',
  'ascension_art',
  'ascension_writing',
  'ascension_movies',
  'ascension_books',
  'ascension_news',
  'ascension_sports',
  'ascension_games',
  'ascension_shopping',
  'ascension_investing',
  'ascension_taxes',
  'ascension_insurance',
  'ascension_moving',
  'ascension_cleaning',
  'ascension_philosophy',
  'ascension_history',
  'ascension_science',
  'ascension_math',
  'ascension_language',
  'ascension_culture',
  'ascension_ethics',
  'ascension_environment',
  'ascension_activism',
  'ascension_project',
  'ascension_task',
  'ascension_remote',
  'ascension_interview',
  'ascension_resume',
  'ascension_negotiation',
  'ascension_networking',
  'ascension_leadership',
  'ascension_team',
  'ascension_feedback',
  'ascension_yoga',
  'ascension_running',
  'ascension_swimming',
  'ascension_cycling',
  'ascension_hiking',
  'ascension_climbing',
  'ascension_martialarts',
  'ascension_skincare',
  'ascension_ergonomics',
  'ascension_firstaid',
  'ascension_dance',
  'ascension_photography',
  'ascension_filmmaking',
  'ascension_podcast',
  'ascension_design',
  'ascension_interior_design',
  'ascension_craft',
  'ascension_baking',
  'ascension_mixology',
  'ascension_etiquette',
  'ascension_wedding',
  'ascension_birthday',
  'ascension_party',
  'ascension_holiday',
  'ascension_gift',
  'ascension_funeral',
  'ascension_babyshower',
  'ascension_graduation',
  'ascension_retirement',
  'ascension_anniversary',
  'ascension_homework',
  'ascension_tutor',
  'ascension_school',
  'ascension_college',
  'ascension_scholarship',
  'ascension_exam',
  'ascension_studyskills',
  'ascension_memorization',
  'ascension_presentation',
  'ascension_teaching',
  'ascension_devops',
  'ascension_cloud',
  'ascension_databases',
  'ascension_security_tech',
  'ascension_testing',
  'ascension_cicd',
  'ascension_monitoring',
  'ascension_api',
  'ascension_microservices',
  'ascension_blockchain',
  'ascension_walking',
  'ascension_stretching',
  'ascension_recovery',
  'ascension_supplements',
  'ascension_allergies',
  'ascension_chronic',
  'ascension_disability',
  'ascension_pregnancy',
  'ascension_childbirth',
  'ascension_postpartum'
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
