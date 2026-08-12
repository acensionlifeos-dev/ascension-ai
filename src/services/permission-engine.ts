/**
 * Permission Engine
 *
 * Determines which permissions AP needs before it can safely execute a
 * capability or class of action, and produces a clean permission request
 * surface. This keeps the user in final authority while letting AP be proactive
 * about what would improve its usefulness.
 */

export interface PermissionScope {
  id: string;
  name: string;
  why: string;
  for_capability: string;
  category: 'read' | 'write' | 'external' | 'high_risk' | 'recurring';
  required_for?: string[];
}

export interface PermissionStatus {
  id: string;
  granted: boolean;
  granted_at?: string;
  expires_at?: string;
  conditions?: string[];
}

export interface PermissionRequest {
  capability: string;
  missing: PermissionScope[];
  message: string;
  can_prepare: boolean;
  can_execute: boolean;
}

// Canonical permission scopes for the overlay capabilities and high-risk actions.
export const PERMISSION_SCOPES: Record<string, PermissionScope> = {
  'camera.read': {
    id: 'camera.read',
    name: 'Camera access',
    why: 'Understand your environment, objects, lighting, and spatial context through the device camera.',
    for_capability: 'ascension_vision',
    category: 'read'
  },
  'calendar.read': {
    id: 'calendar.read',
    name: 'Read calendars',
    why: 'See existing events and free time so plans do not conflict.',
    for_capability: 'ascension_home',
    category: 'read'
  },
  'calendar.write': {
    id: 'calendar.write',
    name: 'Write to calendars',
    why: 'Add or update events after you approve each one.',
    for_capability: 'ascension_home',
    category: 'write'
  },
  'finance.read': {
    id: 'finance.read',
    name: 'Read financial context',
    why: 'Build accurate cash-flow, budget, and wealth plans from your real income, bills, and balances.',
    for_capability: 'ascension_finance',
    category: 'read'
  },
  'finance.transact': {
    id: 'finance.transact',
    name: 'Move money',
    why: 'Payments and transfers require explicit approval and a verified provider receipt.',
    for_capability: 'ascension_finance',
    category: 'high_risk'
  },
  'trading.paper': {
    id: 'trading.paper',
    name: 'Paper trading simulation',
    why: 'Backtest and simulate strategies before any real capital is at risk.',
    for_capability: 'ascension_trading',
    category: 'recurring'
  },
  'trading.live': {
    id: 'trading.live',
    name: 'Live trading execution',
    why: 'Place actual orders only after you explicitly confirm each one.',
    for_capability: 'ascension_trading',
    category: 'high_risk'
  },
  'travel.book': {
    id: 'travel.book',
    name: 'Book travel',
    why: 'Reserve flights, hotels, or transport after you review and approve each booking.',
    for_capability: 'ascension_chat',
    category: 'external'
  },
  'documents.submit': {
    id: 'documents.submit',
    name: 'Submit documents externally',
    why: 'Send grants, patents, or business documents to external agencies only after review.',
    for_capability: 'ascension_chat',
    category: 'high_risk'
  },
  'health.read': {
    id: 'health.read',
    name: 'Read health data',
    why: 'Create relevant wellness and recovery guidance from wearables or manually entered vitals.',
    for_capability: 'ascension_health',
    category: 'read'
  },
  'family.read': {
    id: 'family.read',
    name: 'Read shared family data',
    why: 'Coordinate household or family-level plans using explicitly shared information.',
    for_capability: 'ascension_family',
    category: 'read'
  },
  'home.control': {
    id: 'home.control',
    name: 'Control smart home devices',
    why: 'Adjust lights, climate, or other connected devices after you approve.',
    for_capability: 'ascension_home',
    category: 'write'
  },
  'sprout.guide': {
    id: 'sprout.guide',
    name: 'Child development guidance',
    why: 'Offer age-appropriate learning and milestone suggestions under parent supervision.',
    for_capability: 'ascension_sprout',
    category: 'read'
  },
  'device.read': {
    id: 'device.read',
    name: 'Read connected device info',
    why: 'Identify the phone, SoC, partitions, and current firmware version over USB before planning a flash.',
    for_capability: 'ascension_phone_flash',
    category: 'read'
  },
  'device.flash': {
    id: 'device.flash',
    name: 'Flash device firmware',
    why: 'Write a new operating system to a phone over USB only after explicit approval and a verified receipt.',
    for_capability: 'ascension_phone_flash',
    category: 'high_risk'
  }
};

// Permission requirements per capability/action.
const CAPABILITY_PERMISSIONS: Record<string, string[]> = {
  'ascension_vision': ['camera.read'],
  'ascension_finance': ['finance.read'],
  'ascension_trading': ['trading.paper'],
  'ascension_health': ['health.read'],
  'ascension_home': ['calendar.read', 'home.control'],
  'ascension_family': ['family.read'],
  'ascension_sprout': ['sprout.guide'],
  'ascension_phone_flash': ['device.read', 'device.flash']
};

export function getRequiredPermissions(capabilityId: string): PermissionScope[] {
  const ids = CAPABILITY_PERMISSIONS[capabilityId] || [];
  return ids.map(id => PERMISSION_SCOPES[id]).filter(Boolean);
}

export function requestPermissions(
  capabilityId: string,
  context: Record<string, PermissionStatus>
): PermissionRequest {
  const required = getRequiredPermissions(capabilityId);
  const missing = required.filter(scope => !context[scope.id]?.granted);

  if (missing.length === 0) {
    return {
      capability: capabilityId,
      missing: [],
      message: `AP has the permissions it needs for ${capabilityId}.`,
      can_prepare: true,
      can_execute: true
    };
  }

  const names = missing.map(m => m.name).join(', ');
  const whyList = missing.map(m => `• ${m.name}: ${m.why}`).join('\n');

  const message = [
    `Before I can fully help with ${capabilityId}, I need permission for: ${names}.`,
    '',
    whyList,
    '',
    'I can still prepare a draft or explain the plan without these, but I cannot read live data, submit anything, or take external action until you approve each one.',
    'Nothing has been saved or executed yet.'
  ].join('\n');

  return {
    capability: capabilityId,
    missing,
    message,
    can_prepare: true,
    can_execute: false
  };
}

export function grantPermission(
  id: string,
  context: Record<string, PermissionStatus>,
  conditions?: string[]
): PermissionStatus {
  return {
    id,
    granted: true,
    granted_at: new Date().toISOString(),
    conditions: conditions || []
  };
}
