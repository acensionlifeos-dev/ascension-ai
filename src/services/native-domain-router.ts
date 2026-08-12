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

const DOMAIN_HANDLERS: Record<string, (message: string) => NativeResponse> = {
  'ascension_travel': travelResponse,
  'ascension_legal': legalResponse,
  'ascension_realestate': realEstateResponse,
  'ascension_research': researchResponse,
  'ascension_events': eventsResponse,
  'ascension_automotive': automotiveResponse,
  'ascension_pets': petsResponse,
  'ascension_weather': weatherResponse
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
