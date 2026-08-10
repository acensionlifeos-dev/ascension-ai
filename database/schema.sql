-- Ascension AI Database Schema

-- Users table
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  api_key VARCHAR(255) UNIQUE NOT NULL,
  tier VARCHAR(50) DEFAULT 'individual' CHECK (tier IN ('individual', 'professional', 'enterprise', 'custom')),
  tier_expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Usage tracking (for monitoring, not limiting)
CREATE TABLE usage_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  model_provider VARCHAR(50) NOT NULL, -- openai, anthropic, google
  model_name VARCHAR(100) NOT NULL,
  request_type VARCHAR(50) NOT NULL, -- chat, image, code, audio
  tokens_used INTEGER DEFAULT 0,
  cost_cents INTEGER DEFAULT 0,
  duration_ms INTEGER,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Daily usage summaries (for monitoring)
CREATE TABLE daily_usage_summaries (
  id BIGSERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  total_requests INTEGER DEFAULT 0,
  total_tokens INTEGER DEFAULT 0,
  total_cost_cents INTEGER DEFAULT 0,
  by_provider JSONB DEFAULT '{}',
  by_type JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, date)
);

-- Tiers configuration
CREATE TABLE tiers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  monthly_price_cents INTEGER NOT NULL,
  max_rate_per_minute INTEGER DEFAULT 0, -- 0 = unlimited
  features JSONB DEFAULT '[]',
  is_active BOOLEAN DEFAULT true
);

-- Insert default tiers
INSERT INTO tiers (name, monthly_price_cents, max_rate_per_minute, features) VALUES
('individual', 4900, 60, '["chat", "code", "image", "audio"]'::jsonb),
('professional', 19900, 300, '["chat", "code", "image", "audio", "agents", "api"]'::jsonb),
('enterprise', 99900, 0, '["all", "priority", "support", "custom"]'::jsonb),
('custom', 0, 0, '[]'::jsonb);

-- API keys for model providers
CREATE TABLE provider_keys (
  id SERIAL PRIMARY KEY,
  provider VARCHAR(50) NOT NULL, -- openai, anthropic, google
  api_key_name VARCHAR(100) NOT NULL,
  encrypted_key TEXT NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_usage_logs_user ON usage_logs(user_id, created_at DESC);
CREATE INDEX idx_usage_logs_provider ON usage_logs(model_provider, created_at DESC);
CREATE INDEX idx_daily_usage_user ON daily_usage_summaries(user_id, date DESC);
CREATE INDEX idx_users_tier ON users(tier, tier_expires_at);
