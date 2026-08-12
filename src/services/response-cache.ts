/**
 * Response Cache
 *
 * In-memory cache for deterministic, low-latency native responses. Only caches
 * responses that are safe to repeat and do not contain sensitive context.
 */

export interface CacheEntry {
  content: any;
  timestamp: number;
  ttl_ms: number;
}

class ResponseCache {
  private store = new Map<string, CacheEntry>();
  private defaultTtlMs: number;

  constructor(defaultTtlMs = 30_000) {
    this.defaultTtlMs = defaultTtlMs;
  }

  private key(capabilityId: string, message: string, contextKey = ''): string {
    return `${capabilityId}::${message.trim().toLowerCase()}::${contextKey}`;
  }

  get(capabilityId: string, message: string, contextKey = ''): any | null {
    const k = this.key(capabilityId, message, contextKey);
    const entry = this.store.get(k);
    if (!entry) return null;
    if (Date.now() - entry.timestamp > entry.ttl_ms) {
      this.store.delete(k);
      return null;
    }
    return entry.content;
  }

  set(capabilityId: string, message: string, content: any, contextKey = '', ttlMs?: number): void {
    const k = this.key(capabilityId, message, contextKey);
    this.store.set(k, {
      content,
      timestamp: Date.now(),
      ttl_ms: ttlMs ?? this.defaultTtlMs
    });
  }

  invalidate(capabilityId?: string): void {
    if (!capabilityId) {
      this.store.clear();
      return;
    }
    for (const key of this.store.keys()) {
      if (key.startsWith(`${capabilityId}::`)) {
        this.store.delete(key);
      }
    }
  }

  size(): number {
    return this.store.size;
  }
}

export const responseCache = new ResponseCache();
