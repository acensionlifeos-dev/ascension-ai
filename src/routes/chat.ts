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
  'ascension_postpartum',
  'ascension_packing',
  'ascension_commute',
  'ascension_laundry',
  'ascension_organizing',
  'ascension_storage',
  'ascension_decor',
  'ascension_lighting',
  'ascension_sound',
  'ascension_smell',
  'ascension_balcony',
  'ascension_will',
  'ascension_trust',
  'ascension_prenup',
  'ascension_divorce',
  'ascension_custody',
  'ascension_adoption',
  'ascension_immigration',
  'ascension_contracts',
  'ascension_tenant',
  'ascension_landlord',
  'ascension_startup',
  'ascension_business_plan',
  'ascension_marketing',
  'ascension_sales',
  'ascension_brand',
  'ascension_customer_service',
  'ascension_hr',
  'ascension_fundraising',
  'ascension_pitch',
  'ascension_partnerships',
  'ascension_car_buying',
  'ascension_car_maintenance',
  'ascension_motorcycle',
  'ascension_bicycle',
  'ascension_boat',
  'ascension_rv',
  'ascension_electric_vehicle',
  'ascension_public_transit',
  'ascension_rideshare',
  'ascension_flight',
  'ascension_cricket',
  'ascension_basketball',
  'ascension_football',
  'ascension_baseball',
  'ascension_soccer',
  'ascension_tennis',
  'ascension_golf',
  'ascension_hockey',
  'ascension_esports',
  'ascension_fantasy',
  'ascension_horoscope',
  'ascension_astrology',
  'ascension_tarot',
  'ascension_tattoo',
  'ascension_piercing',
  'ascension_perfume',
  'ascension_jewelry',
  'ascension_watch',
  'ascension_shoes',
  'ascension_bag',
  'ascension_wallet',
  'ascension_sunglasses',
  'ascension_haircut',
  'ascension_beard',
  'ascension_makeup',
  'ascension_camping',
  'ascension_fishing',
  'ascension_hunting',
  'ascension_shooting',
  'ascension_archery',
  'ascension_fencing',
  'ascension_boxing',
  'ascension_wrestling',
  'ascension_gymnastics',
  'ascension_skateboarding',
  'ascension_surfing',
  'ascension_skiing',
  'ascension_snowboarding',
  'ascension_ice_skating',
  'ascension_roller_skating',
  'ascension_magic',
  'ascension_comedy',
  'ascension_jokes',
  'ascension_riddles',
  'ascension_puzzles',
  'ascension_standup',
  'ascension_poetry',
  'ascension_lyrics',
  'ascension_storytelling',
  'ascension_fanfiction',
  'ascension_cosplay',
  'ascension_roleplay',
  'ascension_reviews',
  'ascension_trivia',
  'ascension_boardgames',
  'ascension_streaming',
  'ascension_youtube',
  'ascension_tiktok',
  'ascension_instagram',
  'ascension_twitter',
  'ascension_linkedin',
  'ascension_facebook',
  'ascension_reddit',
  'ascension_discord',
  'ascension_slack',
  'ascension_teams',
  'ascension_zoom',
  'ascension_meet',
  'ascension_webex',
  'ascension_obs',
  'ascension_chess',
  'ascension_poker',
  'ascension_blackjack',
  'ascension_betting',
  'ascension_lottery',
  'ascension_auction',
  'ascension_collector',
  'ascension_antiques',
  'ascension_stamps',
  'ascension_coins',
  'ascension_comics',
  'ascension_trading_cards',
  'ascension_vinyl',
  'ascension_concerts',
  'ascension_festivals',
  'ascension_karaoke',
  'ascension_casino',
  'ascension_sports_betting',
  'ascension_daytrading',
  'ascension_swingtrading',
  'ascension_forex',
  'ascension_crypto',
  'ascension_nfts',
  'ascension_mining',
  'ascension_staking',
  'ascension_defi',
  'ascension_dao',
  'ascension_airdrop',
  'ascension_presale',
  'ascension_whitelist',
  'ascension_nodes',
  'ascension_3d_printing',
  'ascension_laser_cutting',
  'ascension_cnc',
  'ascension_woodworking',
  'ascension_metalworking',
  'ascension_welding',
  'ascension_soldering',
  'ascension_electronics',
  'ascension_arduino',
  'ascension_raspberry_pi',
  'ascension_robotics',
  'ascension_drones',
  'ascension_rc',
  'ascension_ham_radio',
  'ascension_astronomy',
  'ascension_photography_gear',
  'ascension_video_editing',
  'ascension_color_grading',
  'ascension_sound_design',
  'ascension_mixing',
  'ascension_mastering',
  'ascension_voiceover',
  'ascension_podcast_production',
  'ascension_youtube_seo',
  'ascension_thumbnail',
  'ascension_branding',
  'ascension_merchandise',
  'ascension_crowdfunding',
  'ascension_patreon',
  'ascension_sponsorships',
  'ascension_affiliate',
  'ascension_ecommerce',
  'ascension_shopify',
  'ascension_woocommerce',
  'ascension_amazon',
  'ascension_ebay',
  'ascension_etsy',
  'ascension_dropshipping',
  'ascension_print_on_demand',
  'ascension_fulfillment',
  'ascension_inventory',
  'ascension_pos',
  'ascension_import',
  'ascension_export',
  'ascension_tariffs',
  'ascension_shipping',
  'ascension_customer_support',
  'ascension_helpdesk',
  'ascension_ticketing',
  'ascension_live_chat',
  'ascension_chatbot',
  'ascension_knowledge_base',
  'ascension_faq',
  'ascension_onboarding',
  'ascension_retention',
  'ascension_churn',
  'ascension_upsell',
  'ascension_cross_sell',
  'ascension_loyalty',
  'ascension_referral',
  'ascension_reputation',
  'ascension_accounting',
  'ascension_bookkeeping',
  'ascension_invoicing',
  'ascension_payroll',
  'ascension_budgeting',
  'ascension_expenses',
  'ascension_business_taxes',
  'ascension_audit',
  'ascension_compliance',
  'ascension_grants',
  'ascension_loans',
  'ascension_credit',
  'ascension_debt',
  'ascension_credit_score',
  'ascension_mortgage',
  'ascension_insurance_review',
  'ascension_policy_review',
  'ascension_deductible',
  'ascension_premium',
  'ascension_hsa',
  'ascension_fsa',
  'ascension_benefits',
  'ascension_open_enrollment',
  'ascension_workers_comp',
  'ascension_liability_insurance',
  'ascension_umbrella_insurance',
  'ascension_flood_insurance',
  'ascension_earthquake_insurance',
  'ascension_pet_insurance',
  'ascension_travel_insurance',
  'ascension_gardening',
  'ascension_landscaping',
  'ascension_lawn_care',
  'ascension_composting',
  'ascension_hydroponics',
  'ascension_aquaponics',
  'ascension_fermentation',
  'ascension_preserving',
  'ascension_canning',
  'ascension_smoking',
  'ascension_bbq',
  'ascension_grilling',
  'ascension_pizza',
  'ascension_bread_making',
  'ascension_sourdough',
  'ascension_meal_prep',
  'ascension_batch_cooking',
  'ascension_freezer_meals',
  'ascension_slow_cooker',
  'ascension_pressure_cooker',
  'ascension_air_fryer',
  'ascension_sous_vide',
  'ascension_dehydrator',
  'ascension_juicing',
  'ascension_smoothies',
  'ascension_protein',
  'ascension_supplements_stack',
  'ascension_pre_workout',
  'ascension_post_workout',
  'ascension_meal_planning',
  'ascension_grocery_list',
  'ascension_meditation_guided',
  'ascension_breathing',
  'ascension_cold_exposure',
  'ascension_heat_exposure',
  'ascension_sauna',
  'ascension_ice_bath',
  'ascension_sleep_hygiene',
  'ascension_nap',
  'ascension_circadian',
  'ascension_journaling',
  'ascension_gratitude',
  'ascension_affirmations',
  'ascension_visualization',
  'ascension_mindset',
  'ascension_resilience',
  'ascension_growth_mindset',
  'ascension_stoicism',
  'ascension_buddhism',
  'ascension_hinduism',
  'ascension_christianity',
  'ascension_islam',
  'ascension_judaism',
  'ascension_taoism',
  'ascension_confucianism',
  'ascension_shinto',
  'ascension_sikhism',
  'ascension_jainism',
  'ascension_bahai',
  'ascension_paganism',
  'ascension_wicca',
  'ascension_druidry',
  'ascension_native_spirituality',
  'ascension_shamanism',
  'ascension_philosophy',
  'ascension_logic',
  'ascension_critical_thinking',
  'ascension_argumentation',
  'ascension_fallacies',
  'ascension_debate',
  'ascension_persuasion',
  'ascension_rapport',
  'ascension_empathy',
  'ascension_charisma',
  'ascension_confidence_building',
  'ascension_assertiveness',
  'ascension_boundaries',
  'ascension_conflict_resolution',
  'ascension_active_listening',
  'ascension_wallet_automation',
  'ascension_fast_turn',
  'ascension_income_split',
  'ascension_inventor_lab',
  'ascension_hardware_prototyping',
  'ascension_youtube_automation',
  'ascension_tiktok_automation',
  'ascension_amsr_studio',
  'ascension_affiliate_automation',
  'ascension_streaming_channel',
  'ascension_streaming_moderator',
  'ascension_overlay_design',
  'ascension_research_assistant',
  'ascension_design_assistant',
  'ascension_crowdfunding_product',
  'ascension_dream_fund',
  'ascension_content_workspace',
  'ascension_content_analytics',
  'ascension_growth_tracker',
  'ascension_revenue_tracker',
  'ascension_content_calendar',
  'ascension_solution_engine',
  'ascension_invention_engine',
  'ascension_video_types',
  'ascension_channel_types',
  'ascension_cash_strategy',
  'ascension_zero_capital',
  'ascension_micro_launch',
  'ascension_service_designer',
  'ascension_idea_validator',
  'ascension_build_path',
  'ascension_compound_engine',
  'ascension_72h_sprint',
  'ascension_risk_budget',
  'ascension_gig_sprint',
  'ascension_money_flip'
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
