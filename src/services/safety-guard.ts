/**
 * Safety Guard
 *
 * Defensive layer that scans incoming and outgoing content for risks to the
 * individual, their private information, their family, and their business.
 * This is not a replacement for human judgment or professional help.
 */

export interface SafetyResult {
  safe: boolean;
  level: 'none' | 'low' | 'medium' | 'high' | 'critical';
  flags: string[];
  action: 'allow' | 'warn' | 'block' | 'escalate';
  message: string;
  pii_detected: string[];
  crisis_detected: string[];
  sensitive_topics: string[];
}

const CRISIS_PATTERNS: Record<string, RegExp[]> = {
  'self_harm': [
    /\b(?:hurt myself|self[-. ]?harm|cut myself|end it all|end my life|kill myself|suicidal|suicide|no reason to live)\b/gi
  ],
  'harm_to_others': [
    /\b(?:kill them|hurt them|plan to attack|going to shoot|bomb|stab someone|murder)\b/gi
  ],
  'abuse': [
    /\b(?:hitting me|hitting the kids|being abused|domestic violence|he hurts me|she hurts me|afraid of my partner)\b/gi
  ]
};

const PII_PATTERNS: Record<string, RegExp> = {
  'ssn_usa': /\b\d{3}-\d{2}-\d{4}\b/,
  'email': /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/,
  'phone_usa': /\b\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/,
  'credit_card': /\b(?:\d{4}[-\s]?){3}\d{4}\b/,
  'api_key_like': /\b(?:api[_-]?key|token|secret)\s*[:=]\s*['"]?[a-zA-Z0-9]{16,}['"]?/i
};

const SENSITIVE_TOPIC_PATTERNS: Record<string, RegExp> = {
  'health_diagnosis_request': /\b(?:diagnose|tell me if I have|do I have (?:cancer|bipolar|ADHD|diabetes|depression|anxiety|herpes|HIV)|am I pregnant|is this (?:herpes|bipolar|ADHD|cancer|diabetes))\b/gi,
  'legal_advice_request': /\b(?:should I sue|can I get custody|will I go to jail|am I liable|is this legal for me to)\b/gi,
  'financial_guarantee_request': /\b(?:guarantee returns|guaranteed profit|risk-free investment|make me rich fast|double my money)\b/gi,
  'password_or_secret_request': /\b(?:give me your password|what is the admin password|send me the key|what is the secret)\b/gi,
  'personal_info_request': /\b(?:what is their ssn|what is their password|give me their bank|show me their messages)\b/gi
};

export function scanSafety(
  content: string,
  context: { shell?: string; capability?: string } = {}
): SafetyResult {
  const flags: string[] = [];
  const piiDetected: string[] = [];
  const crisisDetected: string[] = [];
  const sensitiveTopics: string[] = [];

  // PII detection
  for (const [name, pattern] of Object.entries(PII_PATTERNS)) {
    if (pattern.test(content)) {
      flags.push(`pii:${name}`);
      piiDetected.push(name);
    }
  }

  // Crisis detection
  for (const [category, patterns] of Object.entries(CRISIS_PATTERNS)) {
    for (const pattern of patterns) {
      if (pattern.test(content)) {
        flags.push(`crisis:${category}`);
        crisisDetected.push(category);
        break;
      }
    }
  }

  // Sensitive topics
  for (const [name, pattern] of Object.entries(SENSITIVE_TOPIC_PATTERNS)) {
    if (pattern.test(content)) {
      flags.push(`sensitive:${name}`);
      sensitiveTopics.push(name);
    }
  }

  // Business/family boundary: never request private info about others
  const thirdPartyInfoPattern = /\b(?:my (?:wife|husband|kid|child|partner|employee|boss|business partner)).*\b(?:password|account|ssn|bank|messages|location|search history|private)\b/gi;
  if (thirdPartyInfoPattern.test(content)) {
    flags.push('boundary:third_party_private_info');
  }

  // Determine level and action
  const hasCrisis = crisisDetected.length > 0;
  const hasHighRisk = sensitiveTopics.includes('health_diagnosis_request') ||
    sensitiveTopics.includes('legal_advice_request') ||
    sensitiveTopics.includes('financial_guarantee_request') ||
    sensitiveTopics.includes('password_or_secret_request');
  const hasPii = piiDetected.length > 0;

  let level: SafetyResult['level'] = 'none';
  let action: SafetyResult['action'] = 'allow';
  let message = 'No safety issues detected.';

  if (hasCrisis) {
    level = 'critical';
    action = 'escalate';
    message = 'This conversation contains signs of possible crisis or harm. I am not a crisis counselor. If you or someone else is in danger, please contact emergency services or a crisis line (988 in the US). You are not alone.';
  } else if (hasHighRisk) {
    level = 'high';
    action = 'warn';
    message = 'This request may involve diagnosis, legal liability, guaranteed returns, or access to secrets. I cannot provide that kind of certainty or access. I can help you prepare to talk to the right professional or protect what is yours.';
  } else if (hasPii) {
    level = 'medium';
    action = 'warn';
    message = 'This message appears to contain personal or sensitive information. I will not save or send anything without your permission. Please be cautious about sharing full SSNs, card numbers, or passwords.';
  } else if (sensitiveTopics.length > 0) {
    level = 'low';
    action = 'warn';
    message = 'This topic is sensitive. I can offer general information and help you think through next steps, but I will not replace a qualified professional.';
  }

  return {
    safe: action === 'allow' || action === 'warn',
    level,
    flags,
    action,
    message,
    pii_detected: piiDetected,
    crisis_detected: crisisDetected,
    sensitive_topics: sensitiveTopics
  };
}
