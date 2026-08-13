import { getRequiredPermissions, requestPermissions, grantPermission } from '../src/services/permission-engine';

describe('Permission Engine', () => {
  test('ascension_trading requires paper trading permission', () => {
    const scopes = getRequiredPermissions('ascension_trading');
    expect(scopes.length).toBeGreaterThan(0);
    expect(scopes.some(s => s.id === 'trading.paper')).toBe(true);
  });

  test('prediction-market intelligence requires paper permission and not live trading permission', () => {
    const scopes = getRequiredPermissions('ascension_prediction_markets');
    expect(scopes.map(scope => scope.id)).toEqual(['trading.paper']);
  });

  test('missing permissions block execution but allow preparation', () => {
    const result = requestPermissions('ascension_trading', {});
    expect(result.can_execute).toBe(false);
    expect(result.can_prepare).toBe(true);
    expect(result.missing.length).toBeGreaterThan(0);
    expect(result.message).toContain('I need permission');
    expect(result.message).toContain('Nothing has been saved');
  });

  test('granted permissions enable execution', () => {
    const context = { 'trading.paper': grantPermission('trading.paper', {}) };
    const result = requestPermissions('ascension_trading', context);
    expect(result.can_execute).toBe(true);
    expect(result.missing.length).toBe(0);
  });

  test('vision requires camera.read', () => {
    const scopes = getRequiredPermissions('ascension_vision');
    expect(scopes.some(s => s.id === 'camera.read')).toBe(true);
  });

  test('health requires health.read', () => {
    const scopes = getRequiredPermissions('ascension_health');
    expect(scopes.some(s => s.id === 'health.read')).toBe(true);
  });
});
