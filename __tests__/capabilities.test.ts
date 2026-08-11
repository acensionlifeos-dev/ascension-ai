import { getAllCapabilities, getCapabilityById, getCapabilitiesByCategory } from '../src/services/capability-registry';

describe('Capability Registry', () => {
  test('registry contains all major outside-AI replacements as native or available', () => {
    const all = getAllCapabilities();
    expect(all.length).toBeGreaterThan(40);

    const native = all.filter(c => c.providers.includes('ascension-native'));
    expect(native.length).toBeGreaterThanOrEqual(8);
  });

  test('native overlay capabilities exist and are reachable', () => {
    const ids = [
      'ascension_chat',
      'ascension_home',
      'ascension_sprout',
      'ascension_family',
      'ascension_health',
      'ascension_finance',
      'ascension_trading',
      'ascension_vision'
    ];

    ids.forEach(id => {
      const cap = getCapabilityById(id);
      expect(cap).toBeDefined();
      expect(cap?.id).toBe(id);
      expect(cap?.providers).toContain('ascension-native');
    });
  });

  test('category lookup works for native overlay categories', () => {
    expect(getCapabilitiesByCategory('home').length).toBeGreaterThan(0);
    expect(getCapabilitiesByCategory('sprout').length).toBeGreaterThan(0);
    expect(getCapabilitiesByCategory('family').length).toBeGreaterThan(0);
    expect(getCapabilitiesByCategory('health').length).toBeGreaterThan(0);
    expect(getCapabilitiesByCategory('finance').length).toBeGreaterThan(0);
  });

  test('unknown capability returns undefined', () => {
    expect(getCapabilityById('nonexistent_capability_xyz')).toBeUndefined();
  });
});
