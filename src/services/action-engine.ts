/**
 * Action Engine
 *
 * Prepares externally consequential actions for human review and explicit
 * approval. Nothing is claimed as executed without a verified receipt.
 */

export interface ActionProposal {
  id: string;
  type: string;
  capability: string;
  description: string;
  risks: string[];
  requires_approval: boolean;
  prepared_payload: Record<string, any>;
  missing: string[];
}

export interface ActionReceipt {
  id: string;
  provider: string;
  status: 'prepared' | 'approved' | 'rejected' | 'completed';
  confirmed_at?: string;
  reference?: string;
}

const HIGH_RISK_ACTIONS = new Set([
  'finance.payment',
  'finance.transact',
  'trading.live',
  'travel.book',
  'documents.submit',
  'messages.send',
  'home.control',
  'calendar.external_write'
]);

export function prepareAction(
  actionType: string,
  capability: string,
  payload: Record<string, any>
): ActionProposal {
  const isHighRisk = HIGH_RISK_ACTIONS.has(actionType);
  const missing: string[] = [];

  if (isHighRisk) {
    missing.push('explicit_user_approval');
  }

  if (actionType.startsWith('finance.') || actionType === 'trading.live') {
    if (!payload.verified_account) missing.push('verified_account');
    if (!payload.amount) missing.push('amount');
    if (!payload.destination) missing.push('destination');
  }

  if (actionType === 'travel.book') {
    if (!payload.dates) missing.push('dates');
    if (!payload.travelers) missing.push('travelers');
    if (!payload.budget_limit) missing.push('budget_limit');
  }

  if (actionType === 'documents.submit') {
    if (!payload.recipient) missing.push('recipient');
    if (!payload.legal_review) missing.push('legal_review');
  }

  return {
    id: `${actionType}_${Date.now()}`,
    type: actionType,
    capability,
    description: `Prepared ${actionType.replace('.', ' ')} action; not executed.`,
    risks: isHighRisk
      ? ['Financial or external consequence', 'Requires explicit user confirmation']
      : ['Low risk but still needs review'],
    requires_approval: isHighRisk,
    prepared_payload: payload,
    missing
  };
}

export function executePreparedAction(
  proposal: ActionProposal,
  approved: boolean,
  receipt: ActionReceipt | null
): { status: string; receipt?: ActionReceipt } {
  if (!approved) {
    return { status: 'rejected' };
  }

  if (proposal.requires_approval && !receipt) {
    return { status: 'awaiting_provider_receipt' };
  }

  return {
    status: 'completed',
    receipt: receipt || {
      id: proposal.id,
      provider: proposal.prepared_payload.provider || 'mock',
      status: 'completed',
      confirmed_at: new Date().toISOString(),
      reference: 'none'
    }
  };
}
