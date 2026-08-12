import { modelRouter } from '../src/services/model-router';
import { responseCache } from '../src/services/response-cache';

describe('Native latency', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
    process.env.ASCENSION_NATIVE_ENABLED = 'true';
    process.env.ASCENSION_NATIVE_URL = 'http://localhost:19999/chat';
    responseCache.invalidate();
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  test('native routing decision is computed in under 5 ms', async () => {
    const start = performance.now();
    const decision = await modelRouter.route('ascension_chat', 'individual');
    const elapsed = performance.now() - start;
    expect(decision.provider).toBe('ascension-native');
    expect(elapsed).toBeLessThan(5);
  });

  test('cached native response returns without network call', async () => {
    responseCache.set('ascension_chat', 'cached benchmark', {
      content: 'cached',
      model: 'Ascension Candidate 3B',
      provider: 'ascension-native',
      tokensUsed: 0
    });

    const start = performance.now();
    const result = await modelRouter.execute(
      { provider: 'ascension-native', model: 'Ascension Candidate 3B', reason: 'test', estimatedCost: 0 },
      { messages: [{ role: 'user', content: 'cached benchmark' }], capability: 'ascension_chat' }
    );
    const elapsed = performance.now() - start;

    expect(result.cached).toBe(true);
    expect(elapsed).toBeLessThan(5);
  });
});
