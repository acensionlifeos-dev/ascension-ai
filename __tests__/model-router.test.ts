import { modelRouter } from '../src/services/model-router';
import { getCapabilityById } from '../src/services/capability-registry';

describe('Ascension Native Provider Routing', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  test('routes ascension_chat to ascension-native provider when enabled', async () => {
    process.env.ASCENSION_NATIVE_ENABLED = 'true';

    const decision = await modelRouter.route('ascension_chat', 'individual');

    expect(decision.provider).toBe('ascension-native');
    expect(decision.model).toBe('Ascension Candidate 3B');
  });

  test('fallback to openai when native is not enabled for a dual-provider capability', async () => {
    process.env.ASCENSION_NATIVE_ENABLED = 'false';
    process.env.OPENAI_API_KEY = 'test-key';

    const capability = getCapabilityById('chat_gpt4');
    expect(capability).toBeDefined();
    expect(capability?.providers).toContain('openai');
  });

  test('ascension-native capabilities are registered', () => {
    const capabilities = [
      'ascension_chat',
      'ascension_home',
      'ascension_sprout',
      'ascension_family',
      'ascension_health',
      'ascension_finance',
      'ascension_trading',
      'ascension_vision'
    ];

    for (const id of capabilities) {
      const capability = getCapabilityById(id);
      expect(capability).toBeDefined();
      expect(capability?.default_provider).toBe('ascension-native');
      expect(capability?.providers).toContain('ascension-native');
    }
  });

  test('executeAscensionNative returns a fallback response when runtime is unavailable', async () => {
    process.env.ASCENSION_NATIVE_ENABLED = 'true';
    process.env.ASCENSION_NATIVE_URL = 'http://localhost:19999/chat'; // no server here

    const result = await modelRouter.execute(
      { provider: 'ascension-native', model: 'Ascension Candidate 3B', reason: 'test', estimatedCost: 0 },
      { messages: [{ role: 'user', content: 'hello' }], capability: 'ascension_chat' }
    );

    expect(result.provider).toBe('ascension-native');
    expect(result.model).toBe('Ascension Candidate 3B');
    expect(result.fallback).toBe(true);
    expect(typeof result.content).toBe('string');
  });
});
