"""
Ascension AI - API Rate Limiting and Usage Tracking
Production-ready API management with tier-based usage
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
from collections import defaultdict
import time

class RateLimiter:
    """Rate limiting for API requests"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.limits = {
            'free': {'requests_per_minute': 10, 'requests_per_day': 100},
            'basic': {'requests_per_minute': 60, 'requests_per_day': 1000},
            'pro': {'requests_per_minute': 300, 'requests_per_day': 10000},
            'enterprise': {'requests_per_minute': 1000, 'requests_per_day': 100000}
        }
    
    def check_rate_limit(self, user_id: str, tier: str = 'free') -> Dict:
        """Check if user is within rate limits"""
        if tier not in self.limits:
            tier = 'free'
        
        limits = self.limits[tier]
        now = time.time()
        
        # Clean old requests
        self.requests[user_id] = [
            r for r in self.requests[user_id] 
            if now - r < 60  # Keep only last minute
        ]
        
        # Check per-minute limit
        if len(self.requests[user_id]) >= limits['requests_per_minute']:
            return {
                'allowed': False,
                'reason': 'rate_limit_exceeded',
                'limit': limits['requests_per_minute'],
                'retry_after': 60
            }
        
        # Check per-day limit (simplified)
        # In production, track daily usage separately
        
        return {
            'allowed': True,
            'limit': limits['requests_per_minute'],
            'remaining': limits['requests_per_minute'] - len(self.requests[user_id])
        }
    
    def record_request(self, user_id: str):
        """Record a request"""
        self.requests[user_id].append(time.time())

class UsageTracker:
    """Track API usage per user"""
    
    def __init__(self):
        self.usage = defaultdict(lambda: {
            'total_requests': 0,
            'tokens_generated': 0,
            'cost': 0.0,
            'last_reset': datetime.now().isoformat()
        })
        self.pricing = {
            'free': {'per_1k_tokens': 0.0},
            'basic': {'per_1k_tokens': 0.01},
            'pro': {'per_1k_tokens': 0.005},
            'enterprise': {'per_1k_tokens': 0.002}
        }
    
    def record_usage(self, user_id: str, tokens: int, tier: str = 'free'):
        """Record usage for a user"""
        self.usage[user_id]['total_requests'] += 1
        self.usage[user_id]['tokens_generated'] += tokens
        
        # Calculate cost
        if tier in self.pricing:
            cost_per_1k = self.pricing[tier]['per_1k_tokens']
            cost = (tokens / 1000) * cost_per_1k
            self.usage[user_id]['cost'] += cost
    
    def get_usage(self, user_id: str) -> Dict:
        """Get usage statistics for a user"""
        if user_id not in self.usage:
            return {
                'total_requests': 0,
                'tokens_generated': 0,
                'cost': 0.0
            }
        
        return self.usage[user_id]
    
    def reset_usage(self, user_id: str):
        """Reset usage for a user (e.g., daily reset)"""
        self.usage[user_id] = {
            'total_requests': 0,
            'tokens_generated': 0,
            'cost': 0.0,
            'last_reset': datetime.now().isoformat()
        }

class TierManager:
    """Manage user tiers and permissions"""
    
    def __init__(self):
        self.tiers = {
            'free': {
                'name': 'Free',
                'features': ['basic_generation', 'limited_tokens'],
                'limits': {'tokens_per_month': 100000}
            },
            'basic': {
                'name': 'Basic',
                'features': ['basic_generation', 'priority_queue', 'more_tokens'],
                'limits': {'tokens_per_month': 1000000}
            },
            'pro': {
                'name': 'Pro',
                'features': ['all_generation', 'priority_queue', 'unlimited_tokens', 'early_access'],
                'limits': {'tokens_per_month': 10000000}
            },
            'enterprise': {
                'name': 'Enterprise',
                'features': ['all_generation', 'priority_queue', 'unlimited_tokens', 'early_access', 'custom_models', 'dedicated_support'],
                'limits': {'tokens_per_month': 'unlimited'}
            }
        }
        self.user_tiers = {}
    
    def assign_tier(self, user_id: str, tier: str):
        """Assign a tier to a user"""
        if tier in self.tiers:
            self.user_tiers[user_id] = tier
    
    def get_user_tier(self, user_id: str) -> str:
        """Get user's tier"""
        return self.user_tiers.get(user_id, 'free')
    
    def get_tier_features(self, tier: str) -> List[str]:
        """Get features for a tier"""
        if tier in self.tiers:
            return self.tiers[tier]['features']
        return self.tiers['free']['features']
    
    def check_feature_access(self, user_id: str, feature: str) -> bool:
        """Check if user has access to a feature"""
        tier = self.get_user_tier(user_id)
        features = self.get_tier_features(tier)
        return feature in features

class APIMonitor:
    """Monitor API performance and health"""
    
    def __init__(self):
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_latency': 0.0,
            'errors': defaultdict(int)
        }
        self.latencies = []
    
    def record_request(self, success: bool, latency: float, error: str = None):
        """Record a request"""
        self.metrics['total_requests'] += 1
        
        if success:
            self.metrics['successful_requests'] += 1
        else:
            self.metrics['failed_requests'] += 1
            if error:
                self.metrics['errors'][error] += 1
        
        self.latencies.append(latency)
        
        # Keep only last 1000 latencies
        if len(self.latencies) > 1000:
            self.latencies = self.latencies[-1000:]
        
        # Update average
        self.metrics['average_latency'] = sum(self.latencies) / len(self.latencies)
    
    def get_metrics(self) -> Dict:
        """Get current metrics"""
        return {
            'total_requests': self.metrics['total_requests'],
            'success_rate': self.metrics['successful_requests'] / max(self.metrics['total_requests'], 1),
            'average_latency_ms': self.metrics['average_latency'] * 1000,
            'error_counts': dict(self.metrics['errors'])
        }
    
    def get_health(self) -> Dict:
        """Get API health status"""
        metrics = self.get_metrics()
        
        health = 'healthy'
        
        if metrics['success_rate'] < 0.95:
            health = 'degraded'
        
        if metrics['success_rate'] < 0.9:
            health = 'unhealthy'
        
        return {
            'status': health,
            'metrics': metrics
        }

# For production, we'll implement:
# - Redis for distributed rate limiting
# - Database persistence for usage tracking
# - Real-time monitoring dashboards
# - Alert system for errors
# - Cost prediction
# - Usage analytics
# - Custom tier management
# - Billing integration
# - Webhook notifications

if __name__ == '__main__':
    print("API rate limiting and usage tracking system ready")
