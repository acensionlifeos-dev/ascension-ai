import { scanSafety } from '../src/services/safety-guard';

describe('Safety Guard', () => {
  test('allows safe messages', () => {
    const result = scanSafety('hello, how are you?');
    expect(result.safe).toBe(true);
    expect(result.action).toBe('allow');
  });

  test('warns on PII in message', () => {
    const result = scanSafety('my ssn is 123-45-6789');
    expect(result.pii_detected).toContain('ssn_usa');
    expect(result.action).toBe('warn');
    expect(result.safe).toBe(true);
  });

  test('escalates on self-harm language', () => {
    const result = scanSafety('I want to end my life');
    expect(result.crisis_detected).toContain('self_harm');
    expect(result.action).toBe('escalate');
    expect(result.level).toBe('critical');
  });

  test('warns on diagnosis request', () => {
    const result = scanSafety('do I have bipolar disorder?');
    expect(result.sensitive_topics).toContain('health_diagnosis_request');
    expect(result.action).toBe('warn');
  });

  test('warns on financial guarantee request', () => {
    const result = scanSafety('guarantee returns and make me rich fast');
    expect(result.sensitive_topics).toContain('financial_guarantee_request');
    expect(result.action).toBe('warn');
  });

  test('flags boundary: asking for third-party private info', () => {
    const result = scanSafety('what is my wife\'s bank password?');
    expect(result.flags).toContain('boundary:third_party_private_info');
  });
});
