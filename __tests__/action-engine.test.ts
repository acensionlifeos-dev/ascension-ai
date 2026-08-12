import { prepareAction, executePreparedAction } from '../src/services/action-engine';

describe('Action Engine', () => {
  test('prepares a payment action and flags it as high-risk', () => {
    const proposal = prepareAction('finance.payment', 'ascension_finance', {
      amount: 100,
      destination: ' landlord'
    });
    expect(proposal.requires_approval).toBe(true);
    expect(proposal.risks).toContain('Financial or external consequence');
    expect(proposal.missing).toContain('explicit_user_approval');
    expect(proposal.description).toContain('not executed');
  });

  test('rejects execution without approval', () => {
    const proposal = prepareAction('finance.payment', 'ascension_finance', { amount: 100 });
    const result = executePreparedAction(proposal, false, null);
    expect(result.status).toBe('rejected');
  });

  test('awaits provider receipt for high-risk action even when approved', () => {
    const proposal = prepareAction('trading.live', 'ascension_trading', { amount: 500 });
    const result = executePreparedAction(proposal, true, null);
    expect(result.status).toBe('awaiting_provider_receipt');
  });

  test('completes high-risk action with a verified receipt', () => {
    const proposal = prepareAction('travel.book', 'ascension_chat', {
      dates: '2026-09-01',
      travelers: 1,
      budget_limit: 500
    });
    const receipt = { id: proposal.id, provider: 'test', status: 'completed' as const, confirmed_at: new Date().toISOString(), reference: 'ABC' };
    const result = executePreparedAction(proposal, true, receipt);
    expect(result.status).toBe('completed');
    expect(result.receipt?.reference).toBe('ABC');
  });
});
