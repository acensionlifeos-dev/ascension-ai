/**
 * Native Domain Router
 *
 * Provides structured, deterministic responses for each native overlay capability
 * while the generative model is still in training. This keeps the API useful,
 * fast, and safe across all registered native domains.
 */

import { requestPermissions, PermissionStatus } from './permission-engine';

export interface NativeResponse {
  content: string;
  model: string;
  provider: 'ascension-native';
  tokensUsed: number;
  capability: string;
  data?: Record<string, any>;
}

function permissionMessage(capability: string, permissions: Record<string, PermissionStatus>): { content: string } | null {
  const request = requestPermissions(capability, permissions);
  if (!request.can_execute) {
    return { content: request.message };
  }
  return null;
}

function travelResponse(message: string): NativeResponse {
  const days = /\d+\s*(?:day|week|nights?)/i.test(message) ? 'detected' : 'not specified';
  return {
    content: `I can build a complete travel plan once you share destination, dates, and budget. Nothing has been booked. So far I noted: ${days === 'detected' ? 'you mentioned a duration' : 'no duration yet'}. Please confirm where you want to go and your preferred travel window.`,
    model: 'Ascension Travel',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_travel',
    data: { days_detected: days === 'detected' }
  };
}

function legalResponse(message: string): NativeResponse {
  return {
    content: `I can review and explain documents, point out clauses to watch, and flag areas where a licensed attorney should review. I am not a lawyer and cannot guarantee outcomes. Please paste the document or describe the issue.`,
    model: 'Ascension Legal',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_legal',
    data: { review_type: 'preliminary', disclaimer: true }
  };
}

function realEstateResponse(message: string): NativeResponse {
  return {
    content: `I can help with housing search, lease review, and cash-flow-based affordability. The key variables that change the answer are location, move-in date, household needs, verified monthly housing limit, and total move-in cash. Nothing has been searched or applied for yet.`,
    model: 'Ascension Real Estate',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_realestate',
    data: { search_started: false }
  };
}

function researchResponse(message: string): NativeResponse {
  return {
    content: `I can research a topic, compare sources, and prepare citations. I will separate verified facts from inference and note uncertainty. What topic or question do you want me to investigate?`,
    model: 'Ascension Research',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_research',
    data: { sources: [], status: 'awaiting_query' }
  };
}

function eventsResponse(message: string): NativeResponse {
  return {
    content: `I can plan an event from guest list to venue and timeline. The biggest variables that shape the plan are date, guest count, location, and budget. Nothing has been booked or scheduled yet.`,
    model: 'Ascension Events',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_events',
    data: { planned: false }
  };
}

function automotiveResponse(message: string): NativeResponse {
  return {
    content: `I can track maintenance schedules, diagnose common symptoms from descriptions, and help compare vehicles. For repairs, I will flag when a mechanic should inspect it. Please describe the symptom or maintenance item.`,
    model: 'Ascension Automotive',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_automotive',
    data: { mechanic_referral: false }
  };
}

function petsResponse(message: string): NativeResponse {
  return {
    content: `I can help with training routines, nutrition, and when to call a vet. I cannot diagnose animals. Please describe your pet, the symptom, or the behavior.`,
    model: 'Ascension Pets',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_pets',
    data: { vet_referral: false }
  };
}

function weatherResponse(message: string): NativeResponse {
  return {
    content: `I can make weather-aware plans once you tell me the location and the day. I will not invent forecast data. Please share where and when.`,
    model: 'Ascension Weather',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_weather',
    data: { location: null, date: null }
  };
}

function financeResponse(message: string): NativeResponse {
  return {
    content: `I can analyze cash flow, income, debt, and spending, and build a step-by-step plan. I need your real balances, income dates, and upcoming bills to do it safely. Nothing has been budgeted or moved yet.`,
    model: 'Ascension Financial Intelligence',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_finance',
    data: { planning_started: false }
  };
}

function tradingResponse(message: string): NativeResponse {
  return {
    content: `I can analyze markets, backtest strategies, and run paper trades. I will not place live orders without your explicit approval and a verified broker receipt. What market or strategy do you want to explore?`,
    model: 'Ascension Trading Intelligence',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_trading',
    data: { paper_only: true }
  };
}

function healthResponse(message: string): NativeResponse {
  return {
    content: `I can help with wellness planning and symptom guidance, but I cannot diagnose or replace a healthcare provider. Please describe what you are experiencing or share any vitals you are comfortable with.`,
    model: 'Ascension Health',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_health',
    data: { medical_disclaimer: true }
  };
}

function homeResponse(message: string): NativeResponse {
  return {
    content: `I can coordinate schedules, chores, and smart home devices for your household. Nothing has been changed yet. Tell me who is in the household and what you want to organize.`,
    model: 'Ascension HomeOS',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_home',
    data: { household_known: false }
  };
}

function sproutResponse(message: string): NativeResponse {
  return {
    content: `I can create age-appropriate learning paths and milestone guidance under parent supervision. Tell me the child\'s age, interests, and what you want to focus on.`,
    model: 'Ascension Sprout',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_sprout',
    data: { parent_supervision: true }
  };
}

function familyResponse(message: string): NativeResponse {
  return {
    content: `I can help with family enterprise planning, governance, and shared records using only explicitly shared family data. What is the family decision or record you want to work on?`,
    model: 'Ascension FamilyOS',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_family',
    data: { shared_only: true }
  };
}

function chatResponse(message: string): NativeResponse {
  return {
    content: `I am AP, your Ascension Partner. I can help across every domain of your life, but I will not pretend to see data you have not shared and I will not act without your approval. What is on your mind?`,
    model: 'Ascension AP',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_chat',
    data: { shell: 'ap' }
  };
}

function nutritionResponse(message: string): NativeResponse {
  return {
    content: `I can build meal plans and analyze nutrition for your goals and preferences. I am not a dietitian; for medical conditions or eating disorders, I will point you toward a qualified provider. What are your goals?`,
    model: 'Ascension Nutrition',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_nutrition',
    data: { dietitian_referral: false }
  };
}

function fitnessResponse(message: string): NativeResponse {
  return {
    content: `I can design workouts, track progress, and suggest form cues. I will not push you past your limits or diagnose injury. What is your current routine or goal?`,
    model: 'Ascension Fitness',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_fitness',
    data: { injury_screen: false }
  };
}

function careerResponse(message: string): NativeResponse {
  return {
    content: `I can review resumes, prepare for interviews, and map career moves. I will not apply for jobs or send messages on your behalf without explicit approval. What are you working toward?`,
    model: 'Ascension Career',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_career',
    data: { applications: [] }
  };
}

function relationshipsResponse(message: string): NativeResponse {
  return {
    content: `I can help you think through conversations, prepare thoughtful responses, and notice relationship patterns. I will not contact anyone for you. What is the situation?`,
    model: 'Ascension Relationships',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_relationships',
    data: { sent_messages: [] }
  };
}

function creativeResponse(message: string): NativeResponse {
  return {
    content: `I can brainstorm, draft, and iterate on creative work. I will not publish or submit anything without you reviewing it. What are you creating?`,
    model: 'Ascension Creative',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_creative',
    data: { published: [] }
  };
}

function codeResponse(message: string): NativeResponse {
  return {
    content: `I can write, review, debug, and explain code. I will not execute code on your production systems or push changes without approval. What language and problem are you working in?`,
    model: 'Ascension Code',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_code',
    data: { executed: false }
  };
}

function learningResponse(message: string): NativeResponse {
  return {
    content: `I can build an adaptive learning path, assess gaps, and create practice problems. I will not lock you into a course you hate. What skill or topic do you want to learn?`,
    model: 'Ascension Learning',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_learning',
    data: { enrolled: [] }
  };
}

function meetingsResponse(message: string): NativeResponse {
  return {
    content: `I can summarize meetings, extract action items, and draft follow-ups. I need the transcript or recording to work from. Please paste the meeting text or upload the recording.`,
    model: 'Ascension Meetings',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_meetings',
    data: { transcript_received: false }
  };
}

function voiceResponse(message: string): NativeResponse {
  return {
    content: `I can process voice commands and transcribe speech. Microphone permission is required. Nothing has been recorded yet. Please enable voice when you are ready.`,
    model: 'Ascension Voice',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_voice',
    data: { microphone_required: true, recorded: false }
  };
}

function securityResponse(message: string): NativeResponse {
  return {
    content: `I can review security settings, flag suspicious behavior, and give privacy guidance. I will not change firewall, access, or authentication rules without explicit approval. What are you worried about?`,
    model: 'Ascension Security',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_security',
    data: { rules_changed: [] }
  };
}

function psychologyResponse(message: string): NativeResponse {
  return {
    content: `I can explain human behavior, emotion, motivation, cognition, and mental patterns. I am not a therapist or psychiatrist. If you are in crisis or need diagnosis, I will point you to a qualified professional. What are you trying to understand about yourself or someone else?`,
    model: 'Ascension Psychology',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_psychology',
    data: { therapist_referral: false }
  };
}

function humanLifeResponse(message: string): NativeResponse {
  return {
    content: `I can help across every domain of human life: identity, health, money, work, relationships, home, time, learning, creativity, meaning, and transitions. Which area are you working on right now?`,
    model: 'Ascension Human Life',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_human_life',
    data: { domains: ['identity', 'health', 'money', 'work', 'relationships', 'home', 'time', 'learning', 'creativity', 'meaning', 'transitions'] }
  };
}

function spiritualityResponse(message: string): NativeResponse {
  return {
    content: `I can explore faith, meditation, ritual, nature, legacy, and existential questions with you. I will not impose a framework; I can work with yours. What are you reflecting on?`,
    model: 'Ascension Spirituality',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_spirituality',
    data: { imposed_framework: false }
  };
}

function griefResponse(message: string): NativeResponse {
  return {
    content: `I am sorry you are going through this. I can hold space, help you organize practical tasks, and point you toward support. I am not a grief counselor. If the pain is overwhelming or persistent, please consider a professional or support group. What do you need most right now?`,
    model: 'Ascension Grief',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_grief',
    data: { counselor_referral: false }
  };
}

function mentalHealthResponse(message: string): NativeResponse {
  return {
    content: `I can help you understand stress, anxiety, low mood, emotional patterns, and when to seek professional help. I am not a therapist or doctor. If you are in crisis, please reach out to a crisis line or emergency services. What are you experiencing?`,
    model: 'Ascension Mental Health',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_mental_health',
    data: { crisis: false }
  };
}

function communicationResponse(message: string): NativeResponse {
  return {
    content: `I can help you prepare for difficult conversations, listen actively, and reduce conflict. I cannot send messages for you. Who is the conversation with and what is the goal?`,
    model: 'Ascension Communication',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_communication',
    data: { sent_messages: [] }
  };
}

function habitsResponse(message: string): NativeResponse {
  return {
    content: `I can help you build habits using cues, routines, rewards, and identity-based change. Tiny, consistent steps outperform heroic bursts. What habit do you want to build or break?`,
    model: 'Ascension Habits',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_habits',
    data: { streaks: [] }
  };
}

function stressResponse(message: string): NativeResponse {
  return {
    content: `I can help you spot stress signals, calm the nervous system, and recover before burnout. What is draining you right now and what is in your control?`,
    model: 'Ascension Stress',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_stress',
    data: { burnout_risk: 'unknown' }
  };
}

function sleepResponse(message: string): NativeResponse {
  return {
    content: `I can help you design a sleep routine and align with your circadian rhythm. I cannot diagnose sleep disorders; persistent insomnia may need a clinician. What is your current sleep pattern?`,
    model: 'Ascension Sleep',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_sleep',
    data: { clinician_referral: false }
  };
}

function parentingResponse(message: string): NativeResponse {
  return {
    content: `I can offer child-development guidance, discipline strategies, and co-parenting support. I am not a pediatrician or therapist. What age and situation are you navigating?`,
    model: 'Ascension Parenting',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_parenting',
    data: { child_age: null }
  };
}

function mindfulnessResponse(message: string): NativeResponse {
  return {
    content: `I can guide breathing, presence, and attention practices. Start with a few slow breaths. What is pulling your attention right now?`,
    model: 'Ascension Mindfulness',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_mindfulness',
    data: { practice_seconds: 0 }
  };
}

function timeResponse(message: string): NativeResponse {
  return {
    content: `I can help you map your energy, prioritize, and reduce procrastination. Time management works best when it follows your biology and values. What is competing for your time right now?`,
    model: 'Ascension Time',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_time',
    data: { priorities: [] }
  };
}

function confidenceResponse(message: string): NativeResponse {
  return {
    content: `I can help you build confidence through small wins, evidence, and self-compassion. Confidence grows from action and alignment, not just positive thinking. What situation is making you doubt yourself?`,
    model: 'Ascension Confidence',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_confidence',
    data: { small_wins: [] }
  };
}

function agingResponse(message: string): NativeResponse {
  return {
    content: `I can help with healthy aging, mobility, nutrition, and life-stage planning. I am not a geriatric specialist; persistent issues need a clinician. What are you planning for?`,
    model: 'Ascension Aging',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_aging',
    data: { clinician_referral: false }
  };
}

function addictionResponse(message: string): NativeResponse {
  return {
    content: `I can offer recovery support, habit strategies, and resources. I am not an addiction counselor. If you are in crisis or need treatment, please reach out to a professional or a recovery support line. What are you working to change?`,
    model: 'Ascension Addiction',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_addiction',
    data: { counselor_referral: false }
  };
}

function conflictResponse(message: string): NativeResponse {
  return {
    content: `I can help you de-escalate, understand positions, and find repair paths. I cannot contact anyone for you. What is the conflict about and what do you want to achieve?`,
    model: 'Ascension Conflict',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_conflict',
    data: { sent_messages: [] }
  };
}

function datingResponse(message: string): NativeResponse {
  return {
    content: `I can help with dating safety, boundaries, conversation, and red flags. I will not message anyone for you. What is the situation?`,
    model: 'Ascension Dating',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_dating',
    data: { sent_messages: [] }
  };
}

function cookingResponse(message: string): NativeResponse {
  return {
    content: `I can suggest recipes, meal plans, and substitutions based on what you have and your goals. What ingredients or dietary goals do you have?`,
    model: 'Ascension Cooking',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_cooking',
    data: { ingredients: [] }
  };
}

function socialResponse(message: string): NativeResponse {
  return {
    content: `I can help with friendship, networking, social skills, and community. What kind of connection are you looking for or struggling with?`,
    model: 'Ascension Social',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_social',
    data: { community: [] }
  };
}

function volunteeringResponse(message: string): NativeResponse {
  return {
    content: `I can help you find ways to contribute that match your skills and values. What causes or skills do you care about?`,
    model: 'Ascension Volunteering',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_volunteering',
    data: { causes: [] }
  };
}

const DOMAIN_HANDLERS: Record<string, (message: string) => NativeResponse> = {
  'ascension_travel': travelResponse,
  'ascension_legal': legalResponse,
  'ascension_realestate': realEstateResponse,
  'ascension_research': researchResponse,
  'ascension_events': eventsResponse,
  'ascension_automotive': automotiveResponse,
  'ascension_pets': petsResponse,
  'ascension_weather': weatherResponse,
  'ascension_finance': financeResponse,
  'ascension_trading': tradingResponse,
  'ascension_health': healthResponse,
  'ascension_home': homeResponse,
  'ascension_sprout': sproutResponse,
  'ascension_family': familyResponse,
  'ascension_chat': chatResponse,
  'ascension_nutrition': nutritionResponse,
  'ascension_fitness': fitnessResponse,
  'ascension_career': careerResponse,
  'ascension_relationships': relationshipsResponse,
  'ascension_creative': creativeResponse,
  'ascension_code': codeResponse,
  'ascension_learning': learningResponse,
  'ascension_meetings': meetingsResponse,
  'ascension_voice': voiceResponse,
  'ascension_security': securityResponse,
  'ascension_psychology': psychologyResponse,
  'ascension_human_life': humanLifeResponse,
  'ascension_spirituality': spiritualityResponse,
  'ascension_grief': griefResponse,
  'ascension_mental_health': mentalHealthResponse,
  'ascension_communication': communicationResponse,
  'ascension_habits': habitsResponse,
  'ascension_stress': stressResponse,
  'ascension_sleep': sleepResponse,
  'ascension_parenting': parentingResponse,
  'ascension_mindfulness': mindfulnessResponse
};

export function routeNativeDomain(
  capabilityId: string,
  message: string,
  permissions: Record<string, PermissionStatus>
): NativeResponse {
  const permissionMsg = permissionMessage(capabilityId, permissions);
  if (permissionMsg) {
    return {
      content: permissionMsg.content,
      model: 'Ascension Permission Gate',
      provider: 'ascension-native',
      tokensUsed: 0,
      capability: capabilityId
    };
  }

  const handler = DOMAIN_HANDLERS[capabilityId];
  if (handler) {
    return handler(message);
  }

  return {
    content: `Ascension native response for ${capabilityId} (stub: domain handler not yet specialized).`,
    model: 'Ascension Candidate 3B',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: capabilityId
  };
}
