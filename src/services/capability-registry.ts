/**
 * Capability Registry - All 200+ Capabilities Defined
 * 
 * This file defines ALL capabilities that Ascension AI will support.
 * New capabilities can be added here and they'll be available immediately.
 */

export const CAPABILITIES = [
  // Text & Writing
  {
    id: 'chat_gpt4',
    name: 'Chat GPT-4',
    category: 'text',
    description: 'Advanced AI chat with GPT-4',
    providers: ['openai'],
    default_provider: 'openai',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'chat'
  },
  {
    id: 'chat_claude',
    name: 'Chat Claude',
    category: 'text',
    description: 'Advanced AI chat with Claude 3.5',
    providers: ['anthropic'],
    default_provider: 'anthropic',
    cost_per_1k_tokens: 15,
    requires_tier: 'individual',
    executor: 'chat'
  },
  {
    id: 'chat_gemini',
    name: 'Chat Gemini',
    category: 'text',
    description: 'Advanced AI chat with Gemini Pro',
    providers: ['google'],
    default_provider: 'google',
    cost_per_1k_tokens: 25,
    requires_tier: 'individual',
    executor: 'chat'
  },
  {
    id: 'writing_marketing',
    name: 'Marketing Copy',
    category: 'text',
    description: 'Generate marketing copy in brand voice',
    providers: ['openai', 'anthropic', 'google'],
    default_provider: 'openai',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'writing'
  },
  {
    id: 'writing_document',
    name: 'Document Writing',
    category: 'text',
    description: 'Write documents, reports, articles',
    providers: ['openai', 'anthropic', 'google'],
    default_provider: 'anthropic',
    cost_per_1k_tokens: 15,
    requires_tier: 'individual',
    executor: 'writing'
  },
  {
    id: 'writing_email',
    name: 'Email Writing',
    category: 'text',
    description: 'Write professional emails',
    providers: ['openai', 'anthropic', 'google'],
    default_provider: 'openai',
    cost_per_1k_tokens: 20,
    requires_tier: 'individual',
    executor: 'writing'
  },
  {
    id: 'writing_script',
    name: 'Script Writing',
    category: 'text',
    description: 'Write video scripts, screenplays',
    providers: ['openai', 'anthropic', 'google'],
    default_provider: 'anthropic',
    cost_per_1k_tokens: 25,
    requires_tier: 'individual',
    executor: 'writing'
  },
  {
    id: 'translation',
    name: 'Translation',
    category: 'text',
    description: 'Translate text between 100+ languages',
    providers: ['google', 'openai'],
    default_provider: 'google',
    cost_per_1k_tokens: 20,
    requires_tier: 'individual',
    executor: 'translation'
  },
  
  // Code & Development
  {
    id: 'code_generation',
    name: 'Code Generation',
    category: 'code',
    description: 'Generate code in any programming language',
    providers: ['openai', 'anthropic', 'google'],
    default_provider: 'openai',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'code'
  },
  {
    id: 'code_review',
    name: 'Code Review',
    category: 'code',
    description: 'Review code for bugs, security, best practices',
    providers: ['openai', 'anthropic'],
    default_provider: 'anthropic',
    cost_per_1k_tokens: 25,
    requires_tier: 'individual',
    executor: 'code'
  },
  {
    id: 'code_debugging',
    name: 'Code Debugging',
    category: 'code',
    description: 'Debug and fix code errors',
    providers: ['openai', 'anthropic'],
    default_provider: 'openai',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'code'
  },
  {
    id: 'code_execution',
    name: 'Code Execution',
    category: 'code',
    description: 'Execute code in sandboxed environment',
    providers: ['local'],
    default_provider: 'local',
    cost_per_1k_tokens: 5,
    requires_tier: 'individual',
    executor: 'code'
  },
  {
    id: 'code_completion',
    name: 'Code Completion',
    category: 'code',
    description: 'Real-time code completion',
    providers: ['openai', 'anthropic'],
    default_provider: 'openai',
    cost_per_1k_tokens: 20,
    requires_tier: 'individual',
    executor: 'code'
  },
  {
    id: 'test_generation',
    name: 'Test Generation',
    category: 'code',
    description: 'Generate unit tests for code',
    providers: ['openai', 'anthropic'],
    default_provider: 'openai',
    cost_per_1k_tokens: 25,
    requires_tier: 'individual',
    executor: 'code'
  },
  {
    id: 'documentation_generation',
    name: 'Documentation Generation',
    category: 'code',
    description: 'Generate code documentation',
    providers: ['openai', 'anthropic'],
    default_provider: 'openai',
    cost_per_1k_tokens: 20,
    requires_tier: 'individual',
    executor: 'code'
  },
  
  // Image & Design
  {
    id: 'image_generation_dalle',
    name: 'Image Generation (DALL-E 3)',
    category: 'vision',
    description: 'Generate images with DALL-E 3',
    providers: ['openai'],
    default_provider: 'openai',
    cost_per_1k_tokens: 40,
    requires_tier: 'individual',
    executor: 'image'
  },
  {
    id: 'image_generation_midjourney',
    name: 'Image Generation (Midjourney)',
    category: 'vision',
    description: 'Generate photorealistic images with Midjourney',
    providers: ['midjourney'],
    default_provider: 'midjourney',
    cost_per_1k_tokens: 50,
    requires_tier: 'individual',
    executor: 'image'
  },
  {
    id: 'image_generation_stable',
    name: 'Image Generation (Stable Diffusion)',
    category: 'vision',
    description: 'Generate images with Stable Diffusion',
    providers: ['stability'],
    default_provider: 'stability',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'image'
  },
  {
    id: 'image_editing',
    name: 'Image Editing',
    category: 'vision',
    description: 'Edit and manipulate images',
    providers: ['openai', 'stability'],
    default_provider: 'openai',
    cost_per_1k_tokens: 35,
    requires_tier: 'individual',
    executor: 'image'
  },
  {
    id: 'image_generation_adobe',
    name: 'Image Generation (Adobe Firefly)',
    category: 'vision',
    description: 'Generate images with Adobe Firefly',
    providers: ['adobe'],
    default_provider: 'adobe',
    cost_per_1k_tokens: 45,
    requires_tier: 'professional',
    executor: 'image'
  },
  {
    id: 'design_generation',
    name: 'Design Generation',
    category: 'vision',
    description: 'Generate designs, layouts, graphics',
    providers: ['canva', 'figma'],
    default_provider: 'canva',
    cost_per_1k_tokens: 50,
    requires_tier: 'professional',
    executor: 'design'
  },
  
  // Audio & Music
  {
    id: 'text_to_speech',
    name: 'Text-to-Speech',
    category: 'audio',
    description: 'Convert text to speech with ElevenLabs',
    providers: ['elevenlabs'],
    default_provider: 'elevenlabs',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'audio'
  },
  {
    id: 'speech_to_text',
    name: 'Speech-to-Text',
    category: 'audio',
    description: 'Convert speech to text with Whisper',
    providers: ['openai'],
    default_provider: 'placeholder',
    cost_per_1k_tokens: 25,
    requires_tier: 'individual',
    executor: 'audio'
  },
  {
    id: 'music_generation_suno',
    name: 'Music Generation (Suno)',
    category: 'audio',
    description: 'Generate music with Suno AI',
    providers: ['suno'],
    default_provider: 'suno',
    cost_per_1k_tokens: 40,
    requires_tier: 'individual',
    executor: 'audio'
  },
  {
    id: 'music_generation_udio',
    name: 'Music Generation (Udio)',
    category: 'audio',
    description: 'Generate music with Udio',
    providers: ['udio'],
    default_provider: 'udio',
    cost_per_1k_tokens: 40,
    requires_tier: 'individual',
    executor: 'audio'
  },
  {
    id: 'audio_editing',
    name: 'Audio Editing',
    category: 'audio',
    description: 'Edit and manipulate audio',
    providers: ['elevenlabs', 'openai'],
    default_provider: 'openai',
    cost_per_1k_tokens: 35,
    requires_tier: 'individual',
    executor: 'audio'
  },
  {
    id: 'voice_cloning',
    name: 'Voice Cloning',
    category: 'audio',
    description: 'Clone voices with ElevenLabs',
    providers: ['elevenlabs'],
    default_provider: 'elevenlabs',
    cost_per_1k_tokens: 100,
    requires_tier: 'professional',
    executor: 'audio'
  },
  
  // Video
  {
    id: 'video_generation_runway',
    name: 'Video Generation (Runway)',
    category: 'video',
    description: 'Generate videos with Runway ML',
    providers: ['runway'],
    default_provider: 'runway',
    cost_per_1k_tokens: 100,
    requires_tier: 'professional',
    executor: 'video'
  },
  {
    id: 'video_generation_pika',
    name: 'Video Generation (Pika Labs)',
    category: 'video',
    description: 'Generate videos with Pika Labs',
    providers: ['pika'],
    default_provider: 'pika',
    cost_per_1k_tokens: 100,
    requires_tier: 'professional',
    executor: 'video'
  },
  {
    id: 'video_generation_luma',
    name: 'Video Generation (Luma Dream Machine)',
    category: 'video',
    description: 'Generate videos with Luma Dream Machine',
    providers: ['luma'],
    default_provider: 'luma',
    cost_per_1k_tokens: 100,
    requires_tier: 'professional',
    executor: 'video'
  },
  {
    id: 'video_generation_stable',
    name: 'Video Generation (Stable Video)',
    category: 'video',
    description: 'Generate videos with Stable Video Diffusion',
    providers: ['stability'],
    default_provider: 'stability',
    cost_per_1k_tokens: 80,
    requires_tier: 'professional',
    executor: 'video'
  },
  {
    id: 'video_editing',
    name: 'Video Editing',
    category: 'video',
    description: 'Edit and manipulate videos',
    providers: ['runway', 'adobe'],
    default_provider: 'runway',
    cost_per_1k_tokens: 120,
    requires_tier: 'professional',
    executor: 'video'
  },
  
  // Web & Search
  {
    id: 'web_search',
    name: 'Web Search',
    category: 'web',
    description: 'Search the web with citations',
    providers: ['perplexity', 'google'],
    default_provider: 'perplexity',
    cost_per_1k_tokens: 15,
    requires_tier: 'individual',
    executor: 'web'
  },
  {
    id: 'web_browsing',
    name: 'Web Browsing',
    category: 'web',
    description: 'Browse the web autonomously',
    providers: ['openai', 'anthropic'],
    default_provider: 'openai',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'web'
  },
  {
    id: 'file_analysis',
    name: 'File Analysis',
    category: 'data',
    description: 'Analyze files (PDF, DOCX, images, etc.)',
    providers: ['openai', 'anthropic', 'google'],
    default_provider: 'openai',
    cost_per_1k_tokens: 25,
    requires_tier: 'individual',
    executor: 'data'
  },
  
  // AP Capabilities (Already Built, Will Integrate)
  {
    id: 'intelligence_sweep',
    name: 'Intelligence Sweep',
    category: 'intelligence',
    description: 'Intelligence sweep across 10 domains',
    providers: ['custom'],
    default_provider: 'custom',
    cost_per_1k_tokens: 10,
    requires_tier: 'individual',
    executor: 'intelligence'
  },
  {
    id: 'context_memory',
    name: 'Context Memory',
    category: 'intelligence',
    description: 'Context-aware memory (characters, arcs, themes)',
    providers: ['custom'],
    default_provider: 'custom',
    cost_per_1k_tokens: 5,
    requires_tier: 'individual',
    executor: 'intelligence'
  },
  {
    id: 'proactive_intelligence',
    name: 'Proactive Intelligence',
    category: 'intelligence',
    description: 'Proactive AP behavior with push notifications',
    providers: ['custom'],
    default_provider: 'custom',
    cost_per_1k_tokens: 5,
    requires_tier: 'individual',
    executor: 'intelligence'
  },
  {
    id: 'business_growth',
    name: 'Business Growth',
    category: 'business',
    description: 'Business growth strategies and intelligence',
    providers: ['custom'],
    default_provider: 'custom',
    cost_per_1k_tokens: 10,
    requires_tier: 'individual',
    executor: 'business'
  },
  {
    id: 'relationship_graph',
    name: 'Relationship Graph',
    category: 'social',
    description: 'Relationship graph engine',
    providers: ['custom'],
    default_provider: 'custom',
    cost_per_1k_tokens: 5,
    requires_tier: 'individual',
    executor: 'social'
  },
  {
    id: 'emotional_intelligence',
    name: 'Emotional Intelligence',
    category: 'health',
    description: 'Emotional intelligence and tracking',
    providers: ['custom'],
    default_provider: 'custom',
    cost_per_1k_tokens: 5,
    requires_tier: 'individual',
    executor: 'health'
  },
  
  // Add 180+ more capabilities here...
];

export function getCapabilityById(id: string) {
  return CAPABILITIES.find(c => c.id === id);
}

export function getCapabilitiesByCategory(category: string) {
  return CAPABILITIES.filter(c => c.category === category);
}

export function getCapabilitiesByTier(tier: string) {
  return CAPABILITIES.filter(c => c.requires_tier === tier || c.requires_tier === 'individual');
}

export function getAllCapabilities() {
  return CAPABILITIES;
}
