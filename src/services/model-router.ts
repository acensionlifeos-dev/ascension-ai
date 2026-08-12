/**
 * Model Router - Routes to Best Provider Based on Capability
 * 
 * This router can route to ANY provider: OpenAI, Anthropic, Google, Midjourney, ElevenLabs, etc.
 * It selects the best provider based on capability, tier, and availability.
 */

import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';
// import { GoogleGenerativeAI } from '@google/generative-ai';
import { getCapabilityById } from './capability-registry';
import { responseCache } from './response-cache';

export interface ModelConfig {
  provider: 'openai' | 'anthropic' | 'google' | 'midjourney' | 'elevenlabs' | 'suno' | 'runway' | 'luma' | 'stability' | 'ascension-native' | 'custom';
  model: string;
  apiKey: string;
}

export interface RoutingDecision {
  provider: string;
  model: string;
  reason: string;
  estimatedCost: number;
}

class ModelRouter {
  private openai: OpenAI | null = null;
  private anthropic: Anthropic | null = null;

  private getOpenAI(): OpenAI | null {
    if (!this.openai && process.env.OPENAI_API_KEY) {
      this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    }
    return this.openai;
  }

  private getAnthropic(): Anthropic | null {
    if (!this.anthropic && process.env.ANTHROPIC_API_KEY) {
      this.anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
    }
    return this.anthropic;
  }

  /**
   * Route to best provider for a capability
   */
  async route(capabilityId: string, userTier: string = 'individual'): Promise<RoutingDecision> {
    const capability = getCapabilityById(capabilityId);
    
    if (!capability) {
      throw new Error(`Capability ${capabilityId} not found`);
    }
    
    // Check if user tier has access
    if (capability.requires_tier === 'enterprise' && userTier !== 'enterprise') {
      throw new Error(`Capability ${capabilityId} requires enterprise tier`);
    }
    
    // Check if default provider is available
    const defaultProvider = capability.default_provider;
    const providerAvailable = this.isProviderAvailable(defaultProvider);
    
    if (providerAvailable) {
      return {
        provider: defaultProvider,
        model: this.getModelForProvider(defaultProvider, capability),
        reason: 'Default provider available',
        estimatedCost: capability.cost_per_1k_tokens
      };
    }
    
    // Try alternative providers
    for (const provider of capability.providers) {
      if (this.isProviderAvailable(provider)) {
        return {
          provider,
          model: this.getModelForProvider(provider, capability),
          reason: `Default provider unavailable, using ${provider}`,
          estimatedCost: capability.cost_per_1k_tokens
        };
      }
    }
    
    throw new Error(`No available provider for capability ${capabilityId}`);
  }
  
  /**
   * Check if provider is available
   */
  private isProviderAvailable(provider: string): boolean {
    switch (provider) {
      case 'openai':
        return this.getOpenAI() !== null;
      case 'anthropic':
        return this.getAnthropic() !== null;
      // case 'google':
      //   return this.google !== null;
      case 'midjourney':
        return process.env.MIDJOURNEY_API_KEY !== undefined;
      case 'elevenlabs':
        return process.env.ELEVENLABS_API_KEY !== undefined;
      case 'suno':
        return process.env.SUNO_API_KEY !== undefined;
      case 'runway':
        return process.env.RUNWAY_API_KEY !== undefined;
      case 'luma':
        return process.env.LUMA_API_KEY !== undefined;
      case 'stability':
        return process.env.STABILITY_API_KEY !== undefined;
      case 'ascension-native':
        return process.env.ASCENSION_NATIVE_ENABLED === 'true';
      case 'custom':
        return true; // Custom providers always available
      default:
        return false;
    }
  }
  
  /**
   * Get model name for provider
   */
  private getModelForProvider(provider: string, capability: any): string {
    switch (provider) {
      case 'openai':
        return this.getOpenAIModel(capability);
      case 'anthropic':
        return this.getAnthropicModel(capability);
      // case 'google':
      //   return this.getGoogleModel(capability);
      case 'midjourney':
        return 'midjourney-v6';
      case 'elevenlabs':
        return 'eleven-multilingual-v2';
      case 'suno':
        return 'suno-v3';
      case 'runway':
        return 'runway-gen3';
      case 'luma':
        return 'luma-dream-machine';
      case 'stability':
        return 'stable-diffusion-xl';
      case 'ascension-native':
        return 'Ascension Candidate 3B';
      case 'custom':
        return 'custom-model';
      default:
        return 'default';
    }
  }
  
  private getOpenAIModel(capability: any): string {
    switch (capability.category) {
      case 'text':
        return 'gpt-4-turbo-preview';
      case 'code':
        return 'gpt-4-turbo-preview';
      case 'vision':
        return 'gpt-4-vision-preview';
      case 'audio':
        return 'whisper-1';
      default:
        return 'gpt-4-turbo-preview';
    }
  }
  
  private getAnthropicModel(capability: any): string {
    switch (capability.category) {
      case 'text':
        return 'claude-3-5-sonnet-20241022';
      case 'code':
        return 'claude-3-5-sonnet-20241022';
      case 'vision':
        return 'claude-3-5-sonnet-20241022';
      default:
        return 'claude-3-5-sonnet-20241022';
    }
  }
  
  // private getGoogleModel(capability: any): string {
  //   switch (capability.category) {
  //     case 'text':
  //       return 'gemini-1.5-pro';
  //     case 'code':
  //       return 'gemini-1.5-pro';
  //     case 'vision':
  //       return 'gemini-1.5-pro-vision';
  //     default:
  //       return 'gemini-1.5-pro';
  //   }
  // }
  
  /**
   * Execute request through routed provider
   */
  async execute(routingDecision: RoutingDecision, request: any): Promise<any> {
    switch (routingDecision.provider) {
      case 'openai':
        return this.executeOpenAI(routingDecision, request);
      case 'anthropic':
        return this.executeAnthropic(routingDecision, request);
      case 'ascension-native':
        return this.executeAscensionNative(routingDecision, request);
      // case 'google':
      //   return this.executeGoogle(routingDecision, request);
      default:
        throw new Error(`Provider ${routingDecision.provider} not yet implemented`);
    }
  }
  
  private async executeOpenAI(routingDecision: RoutingDecision, request: any): Promise<any> {
    const openai = this.getOpenAI();
    if (!openai) throw new Error('OpenAI not initialized');
    
    const response = await openai.chat.completions.create({
      model: routingDecision.model,
      messages: request.messages || [],
      max_tokens: request.max_tokens || 2048,
      temperature: request.temperature || 0.7
    });
    
    return {
      content: response.choices[0].message.content,
      model: routingDecision.model,
      provider: 'openai',
      tokensUsed: response.usage?.total_tokens || 0
    };
  }
  
  private async executeAnthropic(routingDecision: RoutingDecision, request: any): Promise<any> {
    const anthropic = this.getAnthropic();
    if (!anthropic) throw new Error('Anthropic not initialized');
    
    const response = await anthropic.messages.create({
      model: routingDecision.model,
      max_tokens: request.max_tokens || 2048,
      messages: request.messages || []
    });
    
    return {
      content: response.content[0].text,
      model: routingDecision.model,
      provider: 'anthropic',
      tokensUsed: response.usage?.input_tokens + response.usage?.output_tokens || 0
    };
  }
  
  private async executeAscensionNative(routingDecision: RoutingDecision, request: any): Promise<any> {
    // Route to the native Python core via internal endpoint or local model
    const nativeEndpoint = process.env.ASCENSION_NATIVE_URL || 'http://localhost:8000/chat';
    const capability = request.capability || 'ascension_chat';
    const lastMessage = (request.messages || []).slice(-1)[0]?.content || '';
    
    // Fast-path: in-memory cache for identical, short, non-sensitive prompts
    if (lastMessage && lastMessage.length < 500) {
      const cached = responseCache.get(capability, lastMessage);
      if (cached) {
        return { ...cached, cached: true };
      }
    }
    
    try {
      const response = await fetch(nativeEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: request.messages || [],
          temperature: request.temperature ?? 0.7,
          max_tokens: request.max_tokens || 2048,
          capability: request.capability
        })
      });
      
      if (!response.ok) {
        throw new Error(`Native runtime returned ${response.status}`);
      }
      
      const data: any = await response.json();
      const result = {
        content: data.content,
        model: routingDecision.model,
        provider: 'ascension-native',
        tokensUsed: data.tokensUsed || 0
      };
      
      if (lastMessage && lastMessage.length < 500) {
        responseCache.set(capability, lastMessage, result);
      }
      
      return result;
    } catch (error) {
      // Fallback to first-pass deterministic response if native runtime is unavailable
      return {
        content: `Ascension native response for ${routingDecision.model} (stub: native model not loaded yet).`,
        model: routingDecision.model,
        provider: 'ascension-native',
        tokensUsed: 0,
        fallback: true
      };
    }
  }
}

export const modelRouter = new ModelRouter();
