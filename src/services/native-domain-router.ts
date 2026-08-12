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
  'ascension_chat': chatResponse
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
