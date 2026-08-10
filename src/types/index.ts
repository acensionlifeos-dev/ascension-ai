export interface User {
  id: number;
  email: string;
  apiKey: string;
  tier: 'individual' | 'professional' | 'enterprise' | 'custom';
  tierExpiresAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface UsageLog {
  id: number;
  userId: number;
  modelProvider: 'openai' | 'anthropic' | 'google';
  modelName: string;
  requestType: 'chat' | 'image' | 'code' | 'audio';
  tokensUsed: number;
  costCents: number;
  durationMs: number;
  createdAt: Date;
}

export interface DailyUsageSummary {
  id: number;
  userId: number;
  date: Date;
  totalRequests: number;
  totalTokens: number;
  totalCostCents: number;
  byProvider: Record<string, number>;
  byType: Record<string, number>;
  createdAt: Date;
}

export interface ChatRequest {
  message: string;
  model?: string;
  provider?: 'openai' | 'anthropic' | 'google';
  context?: any[];
}

export interface ChatResponse {
  content: string;
  model: string;
  provider: string;
  tokensUsed: number;
  costCents: number;
  durationMs: number;
}

export interface Tier {
  id: number;
  name: string;
  monthlyPriceCents: number;
  maxRatePerMinute: number;
  features: string[];
  isActive: boolean;
}

export interface ProviderKey {
  id: number;
  provider: string;
  apiKeyName: string;
  encryptedKey: string;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}
