/**
 * Capability Registry - All 200+ Capabilities Defined
 * 
 * This file defines ALL capabilities that Aerynza AI will support.
 * New capabilities can be added here and they'll be available immediately.
 */

export const CAPABILITIES = [
  {
    id: 'chat_gpt4',
    name: 'Chat GPT-4',
    category: 'text',
    description: 'Advanced AI chat with GPT-4',
    providers: ['openai'],
    default_provider: 'openai',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'chat',
    related_capabilities: [
    'chat_claude',
    'chat_gemini',
    'writing_marketing',
    'writing_document',
    'writing_email'
  ],
    context: 'Triggers: user asks about Chat GPT-4, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_claude, chat_gemini, writing_marketing, writing_document, writing_email. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'chat',
    related_capabilities: [
    'chat_gpt4',
    'chat_gemini',
    'writing_marketing',
    'writing_document',
    'writing_email'
  ],
    context: 'Triggers: user asks about Chat Claude, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_gpt4, chat_gemini, writing_marketing, writing_document, writing_email. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'chat',
    related_capabilities: [
    'chat_gpt4',
    'chat_claude',
    'writing_marketing',
    'writing_document',
    'writing_email'
  ],
    context: 'Triggers: user asks about Chat Gemini, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_gpt4, chat_claude, writing_marketing, writing_document, writing_email. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'writing',
    related_capabilities: [
    'chat_gpt4',
    'chat_claude',
    'chat_gemini',
    'writing_document',
    'writing_email'
  ],
    context: 'Triggers: user asks about Marketing Copy, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_gpt4, chat_claude, chat_gemini, writing_document, writing_email. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'writing',
    related_capabilities: [
    'chat_gpt4',
    'chat_claude',
    'chat_gemini',
    'writing_marketing',
    'writing_email'
  ],
    context: 'Triggers: user asks about Document Writing, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_gpt4, chat_claude, chat_gemini, writing_marketing, writing_email. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'writing',
    related_capabilities: [
    'chat_gpt4',
    'chat_claude',
    'chat_gemini',
    'writing_marketing',
    'writing_document'
  ],
    context: 'Triggers: user asks about Email Writing, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_gpt4, chat_claude, chat_gemini, writing_marketing, writing_document. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'writing',
    related_capabilities: [
    'chat_gpt4',
    'chat_claude',
    'chat_gemini',
    'writing_marketing',
    'writing_document'
  ],
    context: 'Triggers: user asks about Script Writing, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_gpt4, chat_claude, chat_gemini, writing_marketing, writing_document. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'translation',
    related_capabilities: [
    'chat_gpt4',
    'chat_claude',
    'chat_gemini',
    'writing_marketing',
    'writing_document'
  ],
    context: 'Triggers: user asks about Translation, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_gpt4, chat_claude, chat_gemini, writing_marketing, writing_document. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'code_generation',
    name: 'Code Generation',
    category: 'code',
    description: 'Generate code in any programming language',
    providers: ['openai', 'anthropic', 'google'],
    default_provider: 'openai',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'code',
    related_capabilities: [
    'code_review',
    'code_debugging',
    'code_execution',
    'code_completion',
    'test_generation'
  ],
    context: 'Triggers: user asks about Code Generation, starts a code-domain quest, or needs a decision in this area. Cross-references: code_review, code_debugging, code_execution, code_completion, test_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'code',
    related_capabilities: [
    'code_generation',
    'code_debugging',
    'code_execution',
    'code_completion',
    'test_generation'
  ],
    context: 'Triggers: user asks about Code Review, starts a code-domain quest, or needs a decision in this area. Cross-references: code_generation, code_debugging, code_execution, code_completion, test_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'code',
    related_capabilities: [
    'code_generation',
    'code_review',
    'code_execution',
    'code_completion',
    'test_generation'
  ],
    context: 'Triggers: user asks about Code Debugging, starts a code-domain quest, or needs a decision in this area. Cross-references: code_generation, code_review, code_execution, code_completion, test_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'code',
    related_capabilities: [
    'code_generation',
    'code_review',
    'code_debugging',
    'code_completion',
    'test_generation'
  ],
    context: 'Triggers: user asks about Code Execution, starts a code-domain quest, or needs a decision in this area. Cross-references: code_generation, code_review, code_debugging, code_completion, test_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'code',
    related_capabilities: [
    'code_generation',
    'code_review',
    'code_debugging',
    'code_execution',
    'test_generation'
  ],
    context: 'Triggers: user asks about Code Completion, starts a code-domain quest, or needs a decision in this area. Cross-references: code_generation, code_review, code_debugging, code_execution, test_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'code',
    related_capabilities: [
    'code_generation',
    'code_review',
    'code_debugging',
    'code_execution',
    'code_completion'
  ],
    context: 'Triggers: user asks about Test Generation, starts a code-domain quest, or needs a decision in this area. Cross-references: code_generation, code_review, code_debugging, code_execution, code_completion. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'code',
    related_capabilities: [
    'code_generation',
    'code_review',
    'code_debugging',
    'code_execution',
    'code_completion'
  ],
    context: 'Triggers: user asks about Documentation Generation, starts a code-domain quest, or needs a decision in this area. Cross-references: code_generation, code_review, code_debugging, code_execution, code_completion. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'image_generation_dalle',
    name: 'Image Generation (DALL-E 3)',
    category: 'vision',
    description: 'Generate images with DALL-E 3',
    providers: ['openai'],
    default_provider: 'openai',
    cost_per_1k_tokens: 40,
    requires_tier: 'individual',
    executor: 'image',
    related_capabilities: [
    'image_generation_midjourney',
    'image_generation_stable',
    'image_editing',
    'image_generation_adobe',
    'design_generation'
  ],
    context: 'Triggers: user asks about Image Generation (DALL-E 3), starts a vision-domain quest, or needs a decision in this area. Cross-references: image_generation_midjourney, image_generation_stable, image_editing, image_generation_adobe, design_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'image',
    related_capabilities: [
    'image_generation_dalle',
    'image_generation_stable',
    'image_editing',
    'image_generation_adobe',
    'design_generation'
  ],
    context: 'Triggers: user asks about Image Generation (Midjourney), starts a vision-domain quest, or needs a decision in this area. Cross-references: image_generation_dalle, image_generation_stable, image_editing, image_generation_adobe, design_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'image',
    related_capabilities: [
    'image_generation_dalle',
    'image_generation_midjourney',
    'image_editing',
    'image_generation_adobe',
    'design_generation'
  ],
    context: 'Triggers: user asks about Image Generation (Stable Diffusion), starts a vision-domain quest, or needs a decision in this area. Cross-references: image_generation_dalle, image_generation_midjourney, image_editing, image_generation_adobe, design_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'image',
    related_capabilities: [
    'image_generation_dalle',
    'image_generation_midjourney',
    'image_generation_stable',
    'image_generation_adobe',
    'design_generation'
  ],
    context: 'Triggers: user asks about Image Editing, starts a vision-domain quest, or needs a decision in this area. Cross-references: image_generation_dalle, image_generation_midjourney, image_generation_stable, image_generation_adobe, design_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'image',
    related_capabilities: [
    'image_generation_dalle',
    'image_generation_midjourney',
    'image_generation_stable',
    'image_editing',
    'design_generation'
  ],
    context: 'Triggers: user asks about Image Generation (Adobe Firefly), starts a vision-domain quest, or needs a decision in this area. Cross-references: image_generation_dalle, image_generation_midjourney, image_generation_stable, image_editing, design_generation. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'design',
    related_capabilities: [
    'image_generation_dalle',
    'image_generation_midjourney',
    'image_generation_stable',
    'image_editing',
    'image_generation_adobe'
  ],
    context: 'Triggers: user asks about Design Generation, starts a vision-domain quest, or needs a decision in this area. Cross-references: image_generation_dalle, image_generation_midjourney, image_generation_stable, image_editing, image_generation_adobe. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'text_to_speech',
    name: 'Text-to-Speech',
    category: 'audio',
    description: 'Convert text to speech with ElevenLabs',
    providers: ['elevenlabs'],
    default_provider: 'elevenlabs',
    cost_per_1k_tokens: 30,
    requires_tier: 'individual',
    executor: 'audio',
    related_capabilities: [
    'speech_to_text',
    'music_generation_suno',
    'music_generation_udio',
    'audio_editing',
    'voice_cloning'
  ],
    context: 'Triggers: user asks about Text-to-Speech, starts a audio-domain quest, or needs a decision in this area. Cross-references: speech_to_text, music_generation_suno, music_generation_udio, audio_editing, voice_cloning. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'speech_to_text',
    name: 'Speech-to-Text',
    category: 'audio',
    description: 'Convert speech to text with Whisper',
    providers: ['openai'],
    default_provider: 'openai',
    cost_per_1k_tokens: 25,
    requires_tier: 'individual',
    executor: 'audio',
    related_capabilities: [
    'text_to_speech',
    'music_generation_suno',
    'music_generation_udio',
    'audio_editing',
    'voice_cloning'
  ],
    context: 'Triggers: user asks about Speech-to-Text, starts a audio-domain quest, or needs a decision in this area. Cross-references: text_to_speech, music_generation_suno, music_generation_udio, audio_editing, voice_cloning. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'audio',
    related_capabilities: [
    'text_to_speech',
    'speech_to_text',
    'music_generation_udio',
    'audio_editing',
    'voice_cloning'
  ],
    context: 'Triggers: user asks about Music Generation (Suno), starts a audio-domain quest, or needs a decision in this area. Cross-references: text_to_speech, speech_to_text, music_generation_udio, audio_editing, voice_cloning. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'audio',
    related_capabilities: [
    'text_to_speech',
    'speech_to_text',
    'music_generation_suno',
    'audio_editing',
    'voice_cloning'
  ],
    context: 'Triggers: user asks about Music Generation (Udio), starts a audio-domain quest, or needs a decision in this area. Cross-references: text_to_speech, speech_to_text, music_generation_suno, audio_editing, voice_cloning. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'audio',
    related_capabilities: [
    'text_to_speech',
    'speech_to_text',
    'music_generation_suno',
    'music_generation_udio',
    'voice_cloning'
  ],
    context: 'Triggers: user asks about Audio Editing, starts a audio-domain quest, or needs a decision in this area. Cross-references: text_to_speech, speech_to_text, music_generation_suno, music_generation_udio, voice_cloning. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'audio',
    related_capabilities: [
    'text_to_speech',
    'speech_to_text',
    'music_generation_suno',
    'music_generation_udio',
    'audio_editing'
  ],
    context: 'Triggers: user asks about Voice Cloning, starts a audio-domain quest, or needs a decision in this area. Cross-references: text_to_speech, speech_to_text, music_generation_suno, music_generation_udio, audio_editing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'video_generation_runway',
    name: 'Video Generation (Runway)',
    category: 'video',
    description: 'Generate videos with Runway ML',
    providers: ['runway'],
    default_provider: 'runway',
    cost_per_1k_tokens: 100,
    requires_tier: 'professional',
    executor: 'video',
    related_capabilities: [
    'video_generation_pika',
    'video_generation_luma',
    'video_generation_stable',
    'video_editing'
  ],
    context: 'Triggers: user asks about Video Generation (Runway), starts a video-domain quest, or needs a decision in this area. Cross-references: video_generation_pika, video_generation_luma, video_generation_stable, video_editing. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'video',
    related_capabilities: [
    'video_generation_runway',
    'video_generation_luma',
    'video_generation_stable',
    'video_editing'
  ],
    context: 'Triggers: user asks about Video Generation (Pika Labs), starts a video-domain quest, or needs a decision in this area. Cross-references: video_generation_runway, video_generation_luma, video_generation_stable, video_editing. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'video',
    related_capabilities: [
    'video_generation_runway',
    'video_generation_pika',
    'video_generation_stable',
    'video_editing'
  ],
    context: 'Triggers: user asks about Video Generation (Luma Dream Machine), starts a video-domain quest, or needs a decision in this area. Cross-references: video_generation_runway, video_generation_pika, video_generation_stable, video_editing. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'video',
    related_capabilities: [
    'video_generation_runway',
    'video_generation_pika',
    'video_generation_luma',
    'video_editing'
  ],
    context: 'Triggers: user asks about Video Generation (Stable Video), starts a video-domain quest, or needs a decision in this area. Cross-references: video_generation_runway, video_generation_pika, video_generation_luma, video_editing. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'video',
    related_capabilities: [
    'video_generation_runway',
    'video_generation_pika',
    'video_generation_luma',
    'video_generation_stable'
  ],
    context: 'Triggers: user asks about Video Editing, starts a video-domain quest, or needs a decision in this area. Cross-references: video_generation_runway, video_generation_pika, video_generation_luma, video_generation_stable. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'web_search',
    name: 'Web Search',
    category: 'web',
    description: 'Search the web with citations',
    providers: ['perplexity', 'google'],
    default_provider: 'perplexity',
    cost_per_1k_tokens: 15,
    requires_tier: 'individual',
    executor: 'web',
    related_capabilities: [
    'web_browsing'
  ],
    context: 'Triggers: user asks about Web Search, starts a web-domain quest, or needs a decision in this area. Cross-references: web_browsing. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'web',
    related_capabilities: [
    'web_search'
  ],
    context: 'Triggers: user asks about Web Browsing, starts a web-domain quest, or needs a decision in this area. Cross-references: web_search. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'data',
    related_capabilities: [
    'ascension_chat'
  ],
    context: 'Triggers: user asks about File Analysis, starts a data-domain quest, or needs a decision in this area. Cross-references: ascension_chat. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'intelligence_sweep',
    name: 'Intelligence Sweep',
    category: 'intelligence',
    description: 'Intelligence sweep across 10 domains',
    providers: ['custom'],
    default_provider: 'custom',
    cost_per_1k_tokens: 10,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator',
    'ascension_user_profile'
  ],
    context: 'Triggers: user asks about Intelligence Sweep, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator, ascension_user_profile. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator',
    'ascension_user_profile'
  ],
    context: 'Triggers: user asks about Context Memory, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator, ascension_user_profile. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'ascension_second_brain',
    'ascension_life_orchestrator',
    'ascension_user_profile'
  ],
    context: 'Triggers: user asks about Proactive Intelligence, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, ascension_second_brain, ascension_life_orchestrator, ascension_user_profile. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'business',
    related_capabilities: [
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales',
    'ascension_brand'
  ],
    context: 'Triggers: user asks about Business Growth, starts a business-domain quest, or needs a decision in this area. Cross-references: ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales, ascension_brand. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'social',
    related_capabilities: [
    'ascension_facebook',
    'ascension_reddit',
    'ascension_discord'
  ],
    context: 'Triggers: user asks about Relationship Graph, starts a social-domain quest, or needs a decision in this area. Cross-references: ascension_facebook, ascension_reddit, ascension_discord. Use with permission-scoped context and a receipt for any action.'
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
    executor: 'health',
    related_capabilities: [
    'ascension_health',
    'ascension_nutrition',
    'ascension_fitness',
    'ascension_sleep',
    'ascension_aging'
  ],
    context: 'Triggers: user asks about Emotional Intelligence, starts a health-domain quest, or needs a decision in this area. Cross-references: ascension_health, ascension_nutrition, ascension_fitness, ascension_sleep, ascension_aging. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_chat',
    name: 'Aerynza Native Chat',
    category: 'text',
    description: 'General chat powered by native Aerynza AI core',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'chat',
    related_capabilities: [
    'chat_gpt4',
    'chat_claude',
    'chat_gemini',
    'writing_marketing',
    'writing_document'
  ],
    context: 'Triggers: user asks about Native Chat, starts a text-domain quest, or needs a decision in this area. Cross-references: chat_gpt4, chat_claude, chat_gemini, writing_marketing, writing_document. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_home',
    name: 'Aerynza HomeOS',
    category: 'home',
    description: 'Household and co-parenting coordination',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive',
    'ascension_pets'
  ],
    context: 'Triggers: user asks about HomeOS, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_travel, ascension_realestate, ascension_events, ascension_automotive, ascension_pets. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sprout',
    name: 'Aerynza Sprout',
    category: 'sprout',
    description: 'Child development and learning paths',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sprout',
    related_capabilities: [
    'ascension_chat'
  ],
    context: 'Triggers: user asks about Sprout, starts a sprout-domain quest, or needs a decision in this area. Cross-references: ascension_chat. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_family',
    name: 'Aerynza FamilyOS',
    category: 'family',
    description: 'Family enterprise, tree, and governance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'family',
    related_capabilities: [
    'ascension_family_sync',
    'ascension_family_abroad',
    'ascension_child_development'
  ],
    context: 'Triggers: user asks about FamilyOS, starts a family-domain quest, or needs a decision in this area. Cross-references: ascension_family_sync, ascension_family_abroad, ascension_child_development. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_health',
    name: 'Aerynza Health',
    category: 'health',
    description: 'Health, wellness, and symptom guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'health',
    related_capabilities: [
    'emotional_intelligence',
    'ascension_nutrition',
    'ascension_fitness',
    'ascension_sleep',
    'ascension_aging'
  ],
    context: 'Triggers: user asks about Health, starts a health-domain quest, or needs a decision in this area. Cross-references: emotional_intelligence, ascension_nutrition, ascension_fitness, ascension_sleep, ascension_aging. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_finance',
    name: 'Aerynza Financial Intelligence',
    category: 'finance',
    description: 'Financial analysis, planning, and opportunity finding',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance',
    'ascension_daytrading'
  ],
    context: 'Triggers: user asks about Financial Intelligence, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_trading, ascension_investing, ascension_taxes, ascension_insurance, ascension_daytrading. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_trading',
    name: 'Aerynza Trading Intelligence',
    category: 'finance',
    description: 'Multi-market analysis, backtesting, and paper trading',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance',
    'ascension_daytrading'
  ],
    context: 'Triggers: user asks about Trading Intelligence, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_investing, ascension_taxes, ascension_insurance, ascension_daytrading. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_prediction_markets',
    name: 'Aerynza Prediction Market Intelligence',
    category: 'finance',
    description: 'Research live prediction markets, compare implied odds with sourced evidence, and prepare risk-bounded paper positions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_trading',
    'ascension_finance',
    'ascension_risk_budget',
    'ascension_money_flip',
    'ascension_research_assistant'
  ],
    context: 'Triggers: user asks about Polymarket, prediction markets, market odds, or event probabilities. Compare current market-implied probability with reputable supporting and contrary evidence, resolution rules, time, and liquidity. Express a probability range and uncertainty. Research and paper planning are allowed; no guarantee or real order without jurisdiction checks, explicit approval, wallet signature, and a provider receipt.'
  },
  {
    id: 'ascension_vision',
    name: 'Aerynza Vision',
    category: 'vision',
    description: 'Camera and environmental understanding',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'vision',
    related_capabilities: [
    'image_generation_dalle',
    'image_generation_midjourney',
    'image_generation_stable',
    'image_editing',
    'image_generation_adobe'
  ],
    context: 'Triggers: user asks about Vision, starts a vision-domain quest, or needs a decision in this area. Cross-references: image_generation_dalle, image_generation_midjourney, image_generation_stable, image_editing, image_generation_adobe. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_legal',
    name: 'Aerynza Legal Assistant',
    category: 'documents',
    description: 'Document review, contract analysis, and legal guidance flags',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'documents',
    related_capabilities: [
    'ascension_chat'
  ],
    context: 'Triggers: user asks about Legal Assistant, starts a documents-domain quest, or needs a decision in this area. Cross-references: ascension_chat. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_travel',
    name: 'Aerynza Travel',
    category: 'home',
    description: 'Trip planning, flight search, and itinerary preparation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive',
    'ascension_pets'
  ],
    context: 'Triggers: user asks about Travel, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_realestate, ascension_events, ascension_automotive, ascension_pets. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_realestate',
    name: 'Aerynza Real Estate',
    category: 'home',
    description: 'Housing search, lease review, and property analysis',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_events',
    'ascension_automotive',
    'ascension_pets'
  ],
    context: 'Triggers: user asks about Real Estate, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_events, ascension_automotive, ascension_pets. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_research',
    name: 'Aerynza Research',
    category: 'research',
    description: 'Deep research with source comparison and citation preparation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'research',
    related_capabilities: [
    'ascension_news',
    'ascension_reviews'
  ],
    context: 'Triggers: user asks about Research, starts a research-domain quest, or needs a decision in this area. Cross-references: ascension_news, ascension_reviews. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_events',
    name: 'Aerynza Events',
    category: 'home',
    description: 'Event planning, coordination, and logistics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_automotive',
    'ascension_pets'
  ],
    context: 'Triggers: user asks about Events, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_automotive, ascension_pets. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_automotive',
    name: 'Aerynza Automotive',
    category: 'home',
    description: 'Vehicle maintenance, diagnostics, and buying guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_pets'
  ],
    context: 'Triggers: user asks about Automotive, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_pets. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_pets',
    name: 'Aerynza Pets',
    category: 'home',
    description: 'Pet care, health, training, and nutrition guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Pets, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_weather',
    name: 'Aerynza Weather',
    category: 'environment',
    description: 'Weather-aware planning and safety recommendations',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'environment',
    related_capabilities: [
    'ascension_environment'
  ],
    context: 'Triggers: user asks about Weather, starts a environment-domain quest, or needs a decision in this area. Cross-references: ascension_environment. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_nutrition',
    name: 'Aerynza Nutrition',
    category: 'health',
    description: 'Meal planning, nutrition analysis, and dietary guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'health',
    related_capabilities: [
    'emotional_intelligence',
    'ascension_health',
    'ascension_fitness',
    'ascension_sleep',
    'ascension_aging'
  ],
    context: 'Triggers: user asks about Nutrition, starts a health-domain quest, or needs a decision in this area. Cross-references: emotional_intelligence, ascension_health, ascension_fitness, ascension_sleep, ascension_aging. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fitness',
    name: 'Aerynza Fitness',
    category: 'health',
    description: 'Workout plans, form guidance, and progress tracking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'health',
    related_capabilities: [
    'emotional_intelligence',
    'ascension_health',
    'ascension_nutrition',
    'ascension_sleep',
    'ascension_aging'
  ],
    context: 'Triggers: user asks about Fitness, starts a health-domain quest, or needs a decision in this area. Cross-references: emotional_intelligence, ascension_health, ascension_nutrition, ascension_sleep, ascension_aging. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_career',
    name: 'Aerynza Career',
    category: 'career',
    description: 'Resume review, job matching, and career planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'career',
    related_capabilities: [
    'ascension_professional_network',
    'ascension_mentors',
    'ascension_linkedin_intelligence'
  ],
    context: 'Triggers: user asks about Career, starts a career-domain quest, or needs a decision in this area. Cross-references: ascension_professional_network, ascension_mentors, ascension_linkedin_intelligence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_relationships',
    name: 'Aerynza Relationships',
    category: 'relationships',
    description: 'Communication support, follow-up prep, and relationship context',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy',
    'ascension_charisma'
  ],
    context: 'Triggers: user asks about Relationships, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_dating, ascension_social, ascension_rapport, ascension_empathy, ascension_charisma. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_creative',
    name: 'Aerynza Creative',
    category: 'creation',
    description: 'Writing, music, art, and content generation planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance',
    'ascension_photography'
  ],
    context: 'Triggers: user asks about Creative, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_music, ascension_art, ascension_writing, ascension_dance, ascension_photography. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_code',
    name: 'Aerynza Code',
    category: 'code',
    description: 'Code generation, review, debugging, and architecture planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'code',
    related_capabilities: [
    'code_generation',
    'code_review',
    'code_debugging',
    'code_execution',
    'code_completion'
  ],
    context: 'Triggers: user asks about Code, starts a code-domain quest, or needs a decision in this area. Cross-references: code_generation, code_review, code_debugging, code_execution, code_completion. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_learning',
    name: 'Aerynza Learning',
    category: 'learning',
    description: 'Adaptive skill paths, practice generation, and concept explanation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'learning',
    related_capabilities: [
    'ascension_chat'
  ],
    context: 'Triggers: user asks about Learning, starts a learning-domain quest, or needs a decision in this area. Cross-references: ascension_chat. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_meetings',
    name: 'Aerynza Meetings',
    category: 'productivity',
    description: 'Meeting transcription, summaries, and action-item extraction',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'productivity',
    related_capabilities: [
    'ascension_time',
    'ascension_focus',
    'ascension_calendar_intelligence',
    'ascension_email_intelligence'
  ],
    context: 'Triggers: user asks about Meetings, starts a productivity-domain quest, or needs a decision in this area. Cross-references: ascension_time, ascension_focus, ascension_calendar_intelligence, ascension_email_intelligence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_voice',
    name: 'Aerynza Voice',
    category: 'voice',
    description: 'Voice commands, transcription, and speech-driven control',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'voice',
    related_capabilities: [
    'ascension_chat'
  ],
    context: 'Triggers: user asks about Voice, starts a voice-domain quest, or needs a decision in this area. Cross-references: ascension_chat. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_security',
    name: 'Aerynza Security',
    category: 'security',
    description: 'Security analysis, threat flags, and privacy guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'security',
    related_capabilities: [
    'ascension_chat'
  ],
    context: 'Triggers: user asks about Security, starts a security-domain quest, or needs a decision in this area. Cross-references: ascension_chat. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_psychology',
    name: 'Aerynza Psychology',
    category: 'psychology',
    description: 'Human behavior, emotion, motivation, cognition, and mental health guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'psychology',
    related_capabilities: [
    'ascension_mental_health',
    'ascension_communication',
    'ascension_habits',
    'ascension_stress',
    'ascension_confidence'
  ],
    context: 'Triggers: user asks about Psychology, starts a psychology-domain quest, or needs a decision in this area. Cross-references: ascension_mental_health, ascension_communication, ascension_habits, ascension_stress, ascension_confidence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_human_life',
    name: 'Aerynza Human Life',
    category: 'human_life',
    description: 'Comprehensive guidance across identity, health, money, relationships, home, time, learning, creativity, meaning, and transitions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'human_life',
    related_capabilities: [
    'ascension_grief'
  ],
    context: 'Triggers: user asks about Human Life, starts a human_life-domain quest, or needs a decision in this area. Cross-references: ascension_grief. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_spirituality',
    name: 'Aerynza Spirituality',
    category: 'spirituality',
    description: 'Faith, meaning, meditation, ritual, nature, legacy, and existential exploration',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism',
    'ascension_christianity'
  ],
    context: 'Triggers: user asks about Spirituality, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism, ascension_christianity. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_grief',
    name: 'Aerynza Grief',
    category: 'human_life',
    description: 'Loss, bereavement, transition, and emotional support',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'human_life',
    related_capabilities: [
    'ascension_human_life'
  ],
    context: 'Triggers: user asks about Grief, starts a human_life-domain quest, or needs a decision in this area. Cross-references: ascension_human_life. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mental_health',
    name: 'Aerynza Mental Health',
    category: 'psychology',
    description: 'Stress, anxiety, mood, therapy navigation, and emotional regulation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'psychology',
    related_capabilities: [
    'ascension_psychology',
    'ascension_communication',
    'ascension_habits',
    'ascension_stress',
    'ascension_confidence'
  ],
    context: 'Triggers: user asks about Mental Health, starts a psychology-domain quest, or needs a decision in this area. Cross-references: ascension_psychology, ascension_communication, ascension_habits, ascension_stress, ascension_confidence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_communication',
    name: 'Aerynza Communication',
    category: 'psychology',
    description: 'Difficult conversations, feedback, listening, and conflict resolution',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'psychology',
    related_capabilities: [
    'ascension_psychology',
    'ascension_mental_health',
    'ascension_habits',
    'ascension_stress',
    'ascension_confidence'
  ],
    context: 'Triggers: user asks about Communication, starts a psychology-domain quest, or needs a decision in this area. Cross-references: ascension_psychology, ascension_mental_health, ascension_habits, ascension_stress, ascension_confidence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_habits',
    name: 'Aerynza Habits',
    category: 'psychology',
    description: 'Habit formation, behavior change, cue-routine-reward loops, and identity-based change',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'psychology',
    related_capabilities: [
    'ascension_psychology',
    'ascension_mental_health',
    'ascension_communication',
    'ascension_stress',
    'ascension_confidence'
  ],
    context: 'Triggers: user asks about Habits, starts a psychology-domain quest, or needs a decision in this area. Cross-references: ascension_psychology, ascension_mental_health, ascension_communication, ascension_stress, ascension_confidence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_stress',
    name: 'Aerynza Stress',
    category: 'psychology',
    description: 'Stress recognition, regulation, recovery, and burnout prevention',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'psychology',
    related_capabilities: [
    'ascension_psychology',
    'ascension_mental_health',
    'ascension_communication',
    'ascension_habits',
    'ascension_confidence'
  ],
    context: 'Triggers: user asks about Stress, starts a psychology-domain quest, or needs a decision in this area. Cross-references: ascension_psychology, ascension_mental_health, ascension_communication, ascension_habits, ascension_confidence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sleep',
    name: 'Aerynza Sleep',
    category: 'health',
    description: 'Sleep hygiene, circadian rhythm, and recovery planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'health',
    related_capabilities: [
    'emotional_intelligence',
    'ascension_health',
    'ascension_nutrition',
    'ascension_fitness',
    'ascension_aging'
  ],
    context: 'Triggers: user asks about Sleep, starts a health-domain quest, or needs a decision in this area. Cross-references: emotional_intelligence, ascension_health, ascension_nutrition, ascension_fitness, ascension_aging. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_parenting',
    name: 'Aerynza Parenting',
    category: 'home',
    description: 'Child development, discipline, co-parenting, and parent support',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Parenting, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mindfulness',
    name: 'Aerynza Mindfulness',
    category: 'spirituality',
    description: 'Presence, meditation, breathing, and attention training',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism',
    'ascension_christianity'
  ],
    context: 'Triggers: user asks about Mindfulness, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_meditation, ascension_buddhism, ascension_hinduism, ascension_christianity. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_time',
    name: 'Aerynza Time',
    category: 'productivity',
    description: 'Time management, energy mapping, priorities, and anti-procrastination',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'productivity',
    related_capabilities: [
    'ascension_meetings',
    'ascension_focus',
    'ascension_calendar_intelligence',
    'ascension_email_intelligence'
  ],
    context: 'Triggers: user asks about Time, starts a productivity-domain quest, or needs a decision in this area. Cross-references: ascension_meetings, ascension_focus, ascension_calendar_intelligence, ascension_email_intelligence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_confidence',
    name: 'Aerynza Confidence',
    category: 'psychology',
    description: 'Self-efficacy, confidence building, and self-doubt navigation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'psychology',
    related_capabilities: [
    'ascension_psychology',
    'ascension_mental_health',
    'ascension_communication',
    'ascension_habits',
    'ascension_stress'
  ],
    context: 'Triggers: user asks about Confidence, starts a psychology-domain quest, or needs a decision in this area. Cross-references: ascension_psychology, ascension_mental_health, ascension_communication, ascension_habits, ascension_stress. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_aging',
    name: 'Aerynza Aging',
    category: 'health',
    description: 'Healthy aging, longevity, and life-stage adaptation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'health',
    related_capabilities: [
    'emotional_intelligence',
    'ascension_health',
    'ascension_nutrition',
    'ascension_fitness',
    'ascension_sleep'
  ],
    context: 'Triggers: user asks about Aging, starts a health-domain quest, or needs a decision in this area. Cross-references: emotional_intelligence, ascension_health, ascension_nutrition, ascension_fitness, ascension_sleep. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_addiction',
    name: 'Aerynza Addiction',
    category: 'psychology',
    description: 'Substance and behavioral addiction support, recovery, and professional referrals',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'psychology',
    related_capabilities: [
    'ascension_psychology',
    'ascension_mental_health',
    'ascension_communication',
    'ascension_habits',
    'ascension_stress'
  ],
    context: 'Triggers: user asks about Addiction, starts a psychology-domain quest, or needs a decision in this area. Cross-references: ascension_psychology, ascension_mental_health, ascension_communication, ascension_habits, ascension_stress. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_conflict',
    name: 'Aerynza Conflict',
    category: 'psychology',
    description: 'Dispute resolution, de-escalation, and repair strategies',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'psychology',
    related_capabilities: [
    'ascension_psychology',
    'ascension_mental_health',
    'ascension_communication',
    'ascension_habits',
    'ascension_stress'
  ],
    context: 'Triggers: user asks about Conflict, starts a psychology-domain quest, or needs a decision in this area. Cross-references: ascension_psychology, ascension_mental_health, ascension_communication, ascension_habits, ascension_stress. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_dating',
    name: 'Aerynza Dating',
    category: 'relationships',
    description: 'Dating strategy, safety, boundaries, and communication',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy',
    'ascension_charisma'
  ],
    context: 'Triggers: user asks about Dating, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_social, ascension_rapport, ascension_empathy, ascension_charisma. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cooking',
    name: 'Aerynza Cooking',
    category: 'home',
    description: 'Meal planning, recipes, and kitchen guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Cooking, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_social',
    name: 'Aerynza Social',
    category: 'relationships',
    description: 'Friendship, networking, social skills, and community',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_rapport',
    'ascension_empathy',
    'ascension_charisma'
  ],
    context: 'Triggers: user asks about Social, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_rapport, ascension_empathy, ascension_charisma. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_volunteering',
    name: 'Aerynza Volunteering',
    category: 'community',
    description: 'Service, volunteering, and community contribution matching',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'community',
    related_capabilities: [
    'ascension_activism'
  ],
    context: 'Triggers: user asks about Volunteering, starts a community-domain quest, or needs a decision in this area. Cross-references: ascension_activism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_focus',
    name: 'Aerynza Focus',
    category: 'productivity',
    description: 'Deep work, attention management, and distraction reduction',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'productivity',
    related_capabilities: [
    'ascension_meetings',
    'ascension_time',
    'ascension_calendar_intelligence',
    'ascension_email_intelligence'
  ],
    context: 'Triggers: user asks about Focus, starts a productivity-domain quest, or needs a decision in this area. Cross-references: ascension_meetings, ascension_time, ascension_calendar_intelligence, ascension_email_intelligence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_meditation',
    name: 'Aerynza Meditation',
    category: 'spirituality',
    description: 'Guided meditation, body scans, and contemplative practices',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_buddhism',
    'ascension_hinduism',
    'ascension_christianity'
  ],
    context: 'Triggers: user asks about Meditation, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_buddhism, ascension_hinduism, ascension_christianity. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_garden',
    name: 'Aerynza Garden',
    category: 'home',
    description: 'Garden planning, plant care, and growing guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Garden, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fashion',
    name: 'Aerynza Fashion',
    category: 'lifestyle',
    description: 'Style, wardrobe, and occasion-appropriate dressing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'lifestyle',
    related_capabilities: [
    'ascension_shopping',
    'ascension_auction',
    'ascension_collector',
    'ascension_antiques',
    'ascension_stamps'
  ],
    context: 'Triggers: user asks about Fashion, starts a lifestyle-domain quest, or needs a decision in this area. Cross-references: ascension_shopping, ascension_auction, ascension_collector, ascension_antiques, ascension_stamps. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_repair',
    name: 'Aerynza Repair',
    category: 'home',
    description: 'DIY repairs, maintenance, and when-to-call-a-pro guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Repair, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_music',
    name: 'Aerynza Music',
    category: 'creation',
    description: 'Music theory, composition, practice, and listening guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_art',
    'ascension_writing',
    'ascension_dance',
    'ascension_photography'
  ],
    context: 'Triggers: user asks about Music, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_art, ascension_writing, ascension_dance, ascension_photography. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_art',
    name: 'Aerynza Art',
    category: 'creation',
    description: 'Art techniques, critiques, and creative direction',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_writing',
    'ascension_dance',
    'ascension_photography'
  ],
    context: 'Triggers: user asks about Art, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_writing, ascension_dance, ascension_photography. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_writing',
    name: 'Aerynza Writing',
    category: 'creation',
    description: 'Writing craft, editing, voice, and storytelling',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_dance',
    'ascension_photography'
  ],
    context: 'Triggers: user asks about Writing, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_dance, ascension_photography. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_movies',
    name: 'Aerynza Movies',
    category: 'entertainment',
    description: 'Film and TV recommendations, analysis, and watch planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope',
    'ascension_astrology'
  ],
    context: 'Triggers: user asks about Movies, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_books, ascension_sports, ascension_games, ascension_horoscope, ascension_astrology. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_books',
    name: 'Aerynza Books',
    category: 'entertainment',
    description: 'Book recommendations, analysis, and reading planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope',
    'ascension_astrology'
  ],
    context: 'Triggers: user asks about Books, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_sports, ascension_games, ascension_horoscope, ascension_astrology. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_news',
    name: 'Aerynza News',
    category: 'research',
    description: 'News curation, bias awareness, and summary synthesis',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'research',
    related_capabilities: [
    'ascension_research',
    'ascension_reviews'
  ],
    context: 'Triggers: user asks about News, starts a research-domain quest, or needs a decision in this area. Cross-references: ascension_research, ascension_reviews. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sports',
    name: 'Aerynza Sports',
    category: 'entertainment',
    description: 'Sports analysis, training, and fan engagement',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_games',
    'ascension_horoscope',
    'ascension_astrology'
  ],
    context: 'Triggers: user asks about Sports, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_games, ascension_horoscope, ascension_astrology. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_games',
    name: 'Aerynza Games',
    category: 'entertainment',
    description: 'Game recommendations, strategy, and design discussion',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_horoscope',
    'ascension_astrology'
  ],
    context: 'Triggers: user asks about Games, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_horoscope, ascension_astrology. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_shopping',
    name: 'Aerynza Shopping',
    category: 'lifestyle',
    description: 'Product research, comparison, and value-based buying',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'lifestyle',
    related_capabilities: [
    'ascension_fashion',
    'ascension_auction',
    'ascension_collector',
    'ascension_antiques',
    'ascension_stamps'
  ],
    context: 'Triggers: user asks about Shopping, starts a lifestyle-domain quest, or needs a decision in this area. Cross-references: ascension_fashion, ascension_auction, ascension_collector, ascension_antiques, ascension_stamps. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_investing',
    name: 'Aerynza Investing',
    category: 'finance',
    description: 'Portfolio thinking, asset allocation, and long-term investing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_taxes',
    'ascension_insurance',
    'ascension_daytrading'
  ],
    context: 'Triggers: user asks about Investing, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_taxes, ascension_insurance, ascension_daytrading. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_taxes',
    name: 'Aerynza Taxes',
    category: 'finance',
    description: 'Tax organization, deduction discovery, and preparer coordination',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_insurance',
    'ascension_daytrading'
  ],
    context: 'Triggers: user asks about Taxes, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_insurance, ascension_daytrading. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_insurance',
    name: 'Aerynza Insurance',
    category: 'finance',
    description: 'Insurance review, comparison, and gap analysis',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_daytrading'
  ],
    context: 'Triggers: user asks about Insurance, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_daytrading. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_moving',
    name: 'Aerynza Moving',
    category: 'home',
    description: 'Relocation planning, checklists, and logistics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Moving, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cleaning',
    name: 'Aerynza Cleaning',
    category: 'home',
    description: 'Cleaning routines, schedules, and product guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Cleaning, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_philosophy',
    name: 'Aerynza Philosophy',
    category: 'knowledge',
    description: 'Philosophical questions, schools of thought, and ethical reasoning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language',
    'ascension_culture'
  ],
    context: 'Triggers: user asks about Philosophy, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_history, ascension_science, ascension_math, ascension_language, ascension_culture. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_history',
    name: 'Aerynza History',
    category: 'knowledge',
    description: 'Historical context, events, and lessons',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_science',
    'ascension_math',
    'ascension_language',
    'ascension_culture'
  ],
    context: 'Triggers: user asks about History, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_science, ascension_math, ascension_language, ascension_culture. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_science',
    name: 'Aerynza Science',
    category: 'knowledge',
    description: 'Scientific concepts, literacy, and exploration',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_math',
    'ascension_language',
    'ascension_culture'
  ],
    context: 'Triggers: user asks about Science, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_math, ascension_language, ascension_culture. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_math',
    name: 'Aerynza Math',
    category: 'knowledge',
    description: 'Math explanation, problem-solving, and tutoring',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_language',
    'ascension_culture'
  ],
    context: 'Triggers: user asks about Math, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_language, ascension_culture. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_language',
    name: 'Aerynza Language',
    category: 'knowledge',
    description: 'Language learning, translation, and conversation practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_culture'
  ],
    context: 'Triggers: user asks about Language, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_culture. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_culture',
    name: 'Aerynza Culture',
    category: 'knowledge',
    description: 'Cultural understanding, etiquette, and context',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Culture, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_ethics',
    name: 'Aerynza Ethics',
    category: 'knowledge',
    description: 'Moral reasoning, dilemma navigation, and values clarification',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Ethics, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_environment',
    name: 'Aerynza Environment',
    category: 'environment',
    description: 'Sustainability, climate, and ecological action planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'environment',
    related_capabilities: [
    'ascension_weather'
  ],
    context: 'Triggers: user asks about Environment, starts a environment-domain quest, or needs a decision in this area. Cross-references: ascension_weather. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_activism',
    name: 'Aerynza Activism',
    category: 'community',
    description: 'Civic action, advocacy, and community organizing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'community',
    related_capabilities: [
    'ascension_volunteering'
  ],
    context: 'Triggers: user asks about Activism, starts a community-domain quest, or needs a decision in this area. Cross-references: ascension_volunteering. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_project',
    name: 'Aerynza Project',
    category: 'work',
    description: 'Project planning, milestones, and delivery tracking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume',
    'ascension_negotiation'
  ],
    context: 'Triggers: user asks about Project, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_task, ascension_remote, ascension_interview, ascension_resume, ascension_negotiation. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_task',
    name: 'Aerynza Task',
    category: 'work',
    description: 'Task breakdown, prioritization, and execution support',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume',
    'ascension_negotiation'
  ],
    context: 'Triggers: user asks about Task, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_remote, ascension_interview, ascension_resume, ascension_negotiation. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_remote',
    name: 'Aerynza Remote',
    category: 'work',
    description: 'Remote work setup, routines, and collaboration',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_interview',
    'ascension_resume',
    'ascension_negotiation'
  ],
    context: 'Triggers: user asks about Remote, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_interview, ascension_resume, ascension_negotiation. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_interview',
    name: 'Aerynza Interview',
    category: 'work',
    description: 'Interview preparation and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_resume',
    'ascension_negotiation'
  ],
    context: 'Triggers: user asks about Interview, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_resume, ascension_negotiation. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_resume',
    name: 'Aerynza Resume',
    category: 'work',
    description: 'Resume and cover letter review',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_negotiation'
  ],
    context: 'Triggers: user asks about Resume, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_negotiation. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_negotiation',
    name: 'Aerynza Negotiation',
    category: 'work',
    description: 'Salary, contract, and negotiation strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Negotiation, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_networking',
    name: 'Aerynza Networking',
    category: 'work',
    description: 'Professional networking and relationship building',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Networking, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_leadership',
    name: 'Aerynza Leadership',
    category: 'work',
    description: 'Leadership, management, and team guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Leadership, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_team',
    name: 'Aerynza Team',
    category: 'work',
    description: 'Team dynamics, conflict, and collaboration',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Team, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_feedback',
    name: 'Aerynza Feedback',
    category: 'work',
    description: 'Giving and receiving feedback effectively',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Feedback, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_yoga',
    name: 'Aerynza Yoga',
    category: 'wellness',
    description: 'Yoga poses, sequences, and practice guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking',
    'ascension_climbing'
  ],
    context: 'Triggers: user asks about Yoga, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_running, ascension_swimming, ascension_cycling, ascension_hiking, ascension_climbing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_running',
    name: 'Aerynza Running',
    category: 'wellness',
    description: 'Running plans, form, and training progression',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking',
    'ascension_climbing'
  ],
    context: 'Triggers: user asks about Running, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_swimming, ascension_cycling, ascension_hiking, ascension_climbing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_swimming',
    name: 'Aerynza Swimming',
    category: 'wellness',
    description: 'Swim technique, workouts, and training',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_cycling',
    'ascension_hiking',
    'ascension_climbing'
  ],
    context: 'Triggers: user asks about Swimming, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_cycling, ascension_hiking, ascension_climbing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cycling',
    name: 'Aerynza Cycling',
    category: 'wellness',
    description: 'Cycling routes, training, and equipment',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_hiking',
    'ascension_climbing'
  ],
    context: 'Triggers: user asks about Cycling, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_hiking, ascension_climbing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_hiking',
    name: 'Aerynza Hiking',
    category: 'wellness',
    description: 'Hiking preparation, trails, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_climbing'
  ],
    context: 'Triggers: user asks about Hiking, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_climbing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_climbing',
    name: 'Aerynza Climbing',
    category: 'wellness',
    description: 'Climbing technique, training, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Climbing, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_martialarts',
    promoted: false,
    name: 'Aerynza Martial Arts',
    category: 'wellness',
    description: 'Martial arts style guidance, drills, and conditioning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Martial Arts, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_skincare',
    name: 'Aerynza Skincare',
    category: 'wellness',
    description: 'Skincare routines, ingredients, and concerns',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Skincare, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_ergonomics',
    name: 'Aerynza Ergonomics',
    category: 'wellness',
    description: 'Desk, posture, and workspace ergonomics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Ergonomics, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_firstaid',
    name: 'Aerynza First Aid',
    category: 'wellness',
    description: 'First aid guidance and when to seek care',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about First Aid, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_dance',
    name: 'Aerynza Dance',
    category: 'creation',
    description: 'Dance styles, choreography, and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_photography'
  ],
    context: 'Triggers: user asks about Dance, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_photography. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_photography',
    name: 'Aerynza Photography',
    category: 'creation',
    description: 'Photography technique, composition, and editing guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Photography, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_filmmaking',
    name: 'Aerynza Filmmaking',
    category: 'creation',
    description: 'Film, video, and content production guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Filmmaking, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_podcast',
    name: 'Aerynza Podcast',
    category: 'creation',
    description: 'Podcast planning, production, and distribution guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Podcast, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_design',
    name: 'Aerynza Design',
    category: 'creation',
    description: 'Graphic, UX, and visual design guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Design, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_interior_design',
    name: 'Aerynza Interior Design',
    category: 'home',
    description: 'Interior layout, color, and decor planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Interior Design, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_craft',
    name: 'Aerynza Craft',
    category: 'creation',
    description: 'Crafts, DIY, and maker project guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Craft, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_baking',
    name: 'Aerynza Baking',
    category: 'home',
    description: 'Baking recipes, technique, and troubleshooting',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Baking, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mixology',
    name: 'Aerynza Mixology',
    category: 'home',
    description: 'Cocktail, mocktail, and beverage guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Mixology, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_etiquette',
    name: 'Aerynza Etiquette',
    category: 'knowledge',
    description: 'Etiquette, manners, and social situation guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Etiquette, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_wedding',
    name: 'Aerynza Wedding',
    category: 'life_events',
    description: 'Wedding planning, timeline, and etiquette',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_birthday',
    'ascension_party',
    'ascension_holiday',
    'ascension_gift',
    'ascension_funeral'
  ],
    context: 'Triggers: user asks about Wedding, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_birthday, ascension_party, ascension_holiday, ascension_gift, ascension_funeral. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_birthday',
    name: 'Aerynza Birthday',
    category: 'life_events',
    description: 'Birthday planning, themes, and gift ideas',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_party',
    'ascension_holiday',
    'ascension_gift',
    'ascension_funeral'
  ],
    context: 'Triggers: user asks about Birthday, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_party, ascension_holiday, ascension_gift, ascension_funeral. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_party',
    name: 'Aerynza Party',
    category: 'life_events',
    description: 'Party planning, guest lists, and logistics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_birthday',
    'ascension_holiday',
    'ascension_gift',
    'ascension_funeral'
  ],
    context: 'Triggers: user asks about Party, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_birthday, ascension_holiday, ascension_gift, ascension_funeral. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_holiday',
    name: 'Aerynza Holiday',
    category: 'life_events',
    description: 'Holiday planning, traditions, and travel',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_birthday',
    'ascension_party',
    'ascension_gift',
    'ascension_funeral'
  ],
    context: 'Triggers: user asks about Holiday, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_birthday, ascension_party, ascension_gift, ascension_funeral. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_gift',
    name: 'Aerynza Gift',
    category: 'life_events',
    description: 'Gift ideas, wrapping, and giving guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_birthday',
    'ascension_party',
    'ascension_holiday',
    'ascension_funeral'
  ],
    context: 'Triggers: user asks about Gift, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_birthday, ascension_party, ascension_holiday, ascension_funeral. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_funeral',
    name: 'Aerynza Funeral',
    category: 'life_events',
    description: 'Funeral planning, grief, and memorial support',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_birthday',
    'ascension_party',
    'ascension_holiday',
    'ascension_gift'
  ],
    context: 'Triggers: user asks about Funeral, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_birthday, ascension_party, ascension_holiday, ascension_gift. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_babyshower',
    name: 'Aerynza Baby Shower',
    category: 'life_events',
    description: 'Baby shower planning and registry guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_birthday',
    'ascension_party',
    'ascension_holiday',
    'ascension_gift'
  ],
    context: 'Triggers: user asks about Baby Shower, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_birthday, ascension_party, ascension_holiday, ascension_gift. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_graduation',
    name: 'Aerynza Graduation',
    category: 'life_events',
    description: 'Graduation planning, gifts, and next steps',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_birthday',
    'ascension_party',
    'ascension_holiday',
    'ascension_gift'
  ],
    context: 'Triggers: user asks about Graduation, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_birthday, ascension_party, ascension_holiday, ascension_gift. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_retirement',
    name: 'Aerynza Retirement',
    category: 'life_events',
    description: 'Retirement planning, lifestyle, and transitions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_birthday',
    'ascension_party',
    'ascension_holiday',
    'ascension_gift'
  ],
    context: 'Triggers: user asks about Retirement, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_birthday, ascension_party, ascension_holiday, ascension_gift. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_anniversary',
    name: 'Aerynza Anniversary',
    category: 'life_events',
    description: 'Anniversary celebration and gift ideas',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'life_events',
    related_capabilities: [
    'ascension_wedding',
    'ascension_birthday',
    'ascension_party',
    'ascension_holiday',
    'ascension_gift'
  ],
    context: 'Triggers: user asks about Anniversary, starts a life_events-domain quest, or needs a decision in this area. Cross-references: ascension_wedding, ascension_birthday, ascension_party, ascension_holiday, ascension_gift. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_homework',
    name: 'Aerynza Homework',
    category: 'education',
    description: 'Homework help, explanation, and study guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_tutor',
    'ascension_school',
    'ascension_college',
    'ascension_scholarship',
    'ascension_exam'
  ],
    context: 'Triggers: user asks about Homework, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_tutor, ascension_school, ascension_college, ascension_scholarship, ascension_exam. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tutor',
    name: 'Aerynza Tutor',
    category: 'education',
    description: 'One-on-one tutoring across subjects',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_school',
    'ascension_college',
    'ascension_scholarship',
    'ascension_exam'
  ],
    context: 'Triggers: user asks about Tutor, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_school, ascension_college, ascension_scholarship, ascension_exam. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_school',
    name: 'Aerynza School',
    category: 'education',
    description: 'School selection, applications, and planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_tutor',
    'ascension_college',
    'ascension_scholarship',
    'ascension_exam'
  ],
    context: 'Triggers: user asks about School, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_tutor, ascension_college, ascension_scholarship, ascension_exam. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_college',
    name: 'Aerynza College',
    category: 'education',
    description: 'College search, applications, and planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_tutor',
    'ascension_school',
    'ascension_scholarship',
    'ascension_exam'
  ],
    context: 'Triggers: user asks about College, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_tutor, ascension_school, ascension_scholarship, ascension_exam. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_scholarship',
    name: 'Aerynza Scholarship',
    category: 'education',
    description: 'Scholarship search and application support',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_tutor',
    'ascension_school',
    'ascension_college',
    'ascension_exam'
  ],
    context: 'Triggers: user asks about Scholarship, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_tutor, ascension_school, ascension_college, ascension_exam. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_exam',
    name: 'Aerynza Exam',
    category: 'education',
    description: 'Exam preparation, strategy, and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_tutor',
    'ascension_school',
    'ascension_college',
    'ascension_scholarship'
  ],
    context: 'Triggers: user asks about Exam, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_tutor, ascension_school, ascension_college, ascension_scholarship. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_studyskills',
    name: 'Aerynza Study Skills',
    category: 'education',
    description: 'Study habits, note-taking, and retention',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_tutor',
    'ascension_school',
    'ascension_college',
    'ascension_scholarship'
  ],
    context: 'Triggers: user asks about Study Skills, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_tutor, ascension_school, ascension_college, ascension_scholarship. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_memorization',
    name: 'Aerynza Memorization',
    category: 'education',
    description: 'Memory techniques and spaced repetition',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_tutor',
    'ascension_school',
    'ascension_college',
    'ascension_scholarship'
  ],
    context: 'Triggers: user asks about Memorization, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_tutor, ascension_school, ascension_college, ascension_scholarship. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_presentation',
    name: 'Aerynza Presentation',
    category: 'education',
    description: 'Presentations, slides, and public speaking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_tutor',
    'ascension_school',
    'ascension_college',
    'ascension_scholarship'
  ],
    context: 'Triggers: user asks about Presentation, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_tutor, ascension_school, ascension_college, ascension_scholarship. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_teaching',
    name: 'Aerynza Teaching',
    category: 'education',
    description: 'Teaching methods, lesson planning, and assessment',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'education',
    related_capabilities: [
    'ascension_homework',
    'ascension_tutor',
    'ascension_school',
    'ascension_college',
    'ascension_scholarship'
  ],
    context: 'Triggers: user asks about Teaching, starts a education-domain quest, or needs a decision in this area. Cross-references: ascension_homework, ascension_tutor, ascension_school, ascension_college, ascension_scholarship. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_devops',
    name: 'Aerynza DevOps',
    category: 'engineering',
    description: 'DevOps practices, pipelines, and infrastructure',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing',
    'ascension_cicd'
  ],
    context: 'Triggers: user asks about DevOps, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_cloud, ascension_databases, ascension_security_tech, ascension_testing, ascension_cicd. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cloud',
    name: 'Aerynza Cloud',
    category: 'engineering',
    description: 'Cloud architecture, services, and cost guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing',
    'ascension_cicd'
  ],
    context: 'Triggers: user asks about Cloud, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_databases, ascension_security_tech, ascension_testing, ascension_cicd. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_databases',
    name: 'Aerynza Databases',
    category: 'engineering',
    description: 'Database design, queries, and optimization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_security_tech',
    'ascension_testing',
    'ascension_cicd'
  ],
    context: 'Triggers: user asks about Databases, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_security_tech, ascension_testing, ascension_cicd. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_security_tech',
    name: 'Aerynza Security Tech',
    category: 'engineering',
    description: 'Application and infrastructure security guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_testing',
    'ascension_cicd'
  ],
    context: 'Triggers: user asks about Security Tech, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_testing, ascension_cicd. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_testing',
    name: 'Aerynza Testing',
    category: 'engineering',
    description: 'Test strategy, automation, and quality assurance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_cicd'
  ],
    context: 'Triggers: user asks about Testing, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_security_tech, ascension_cicd. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cicd',
    name: 'Aerynza CI/CD',
    category: 'engineering',
    description: 'Continuous integration and delivery guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing'
  ],
    context: 'Triggers: user asks about CI/CD, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_security_tech, ascension_testing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_monitoring',
    name: 'Aerynza Monitoring',
    category: 'engineering',
    description: 'Observability, logging, and alerting',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing'
  ],
    context: 'Triggers: user asks about Monitoring, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_security_tech, ascension_testing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_api',
    name: 'Aerynza API',
    category: 'engineering',
    description: 'API design, versioning, and documentation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing'
  ],
    context: 'Triggers: user asks about API, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_security_tech, ascension_testing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_microservices',
    name: 'Aerynza Microservices',
    category: 'engineering',
    description: 'Microservices architecture and tradeoffs',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing'
  ],
    context: 'Triggers: user asks about Microservices, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_security_tech, ascension_testing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_blockchain',
    name: 'Aerynza Blockchain',
    category: 'engineering',
    description: 'Blockchain concepts, smart contracts, and crypto basics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing'
  ],
    context: 'Triggers: user asks about Blockchain, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_security_tech, ascension_testing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_walking',
    name: 'Aerynza Walking',
    category: 'wellness',
    description: 'Walking plans, routes, and fitness integration',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Walking, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_stretching',
    name: 'Aerynza Stretching',
    category: 'wellness',
    description: 'Stretching routines, mobility, and flexibility',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Stretching, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_recovery',
    name: 'Aerynza Recovery',
    category: 'wellness',
    description: 'Rest, recovery, and regeneration planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Recovery, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_supplements',
    name: 'Aerynza Supplements',
    category: 'wellness',
    description: 'Supplement information and when to consult a clinician',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Supplements, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_allergies',
    name: 'Aerynza Allergies',
    category: 'wellness',
    description: 'Allergy awareness, triggers, and management',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Allergies, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_chronic',
    name: 'Aerynza Chronic',
    category: 'wellness',
    description: 'Chronic condition support and self-management guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Chronic, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_disability',
    name: 'Aerynza Disability',
    category: 'wellness',
    description: 'Disability support, accommodations, and resources',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Disability, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_pregnancy',
    name: 'Aerynza Pregnancy',
    category: 'wellness',
    description: 'Pregnancy planning, questions, and resource guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Pregnancy, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_childbirth',
    name: 'Aerynza Childbirth',
    category: 'wellness',
    description: 'Childbirth preparation and birth plan support',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Childbirth, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_postpartum',
    name: 'Aerynza Postpartum',
    category: 'wellness',
    description: 'Postpartum support, recovery, and newborn adjustment',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Postpartum, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_packing',
    name: 'Aerynza Packing',
    category: 'home',
    description: 'Packing lists and travel preparation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Packing, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_commute',
    name: 'Aerynza Commute',
    category: 'home',
    description: 'Commute planning, routes, and optimization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Commute, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_laundry',
    name: 'Aerynza Laundry',
    category: 'home',
    description: 'Laundry routines, stains, and care',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Laundry, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_organizing',
    name: 'Aerynza Organizing',
    category: 'home',
    description: 'Organization systems and decluttering',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Organizing, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_storage',
    name: 'Aerynza Storage',
    category: 'home',
    description: 'Storage solutions and space planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Storage, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_decor',
    name: 'Aerynza Decor',
    category: 'home',
    description: 'Decor choices, themes, and styling',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Decor, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_lighting',
    name: 'Aerynza Lighting',
    category: 'home',
    description: 'Lighting design, bulbs, and ambiance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Lighting, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sound',
    name: 'Aerynza Sound',
    category: 'home',
    description: 'Sound, acoustics, and noise management',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Sound, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_smell',
    name: 'Aerynza Smell',
    category: 'home',
    description: 'Scent, air quality, and fragrance guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Smell, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_balcony',
    name: 'Aerynza Balcony',
    category: 'home',
    description: 'Balcony, patio, and small outdoor space use',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Balcony, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_will',
    name: 'Aerynza Will',
    category: 'legal',
    description: 'Will planning and estate introduction',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_trust',
    'ascension_prenup',
    'ascension_divorce',
    'ascension_custody',
    'ascension_adoption'
  ],
    context: 'Triggers: user asks about Will, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_trust, ascension_prenup, ascension_divorce, ascension_custody, ascension_adoption. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_trust',
    name: 'Aerynza Trust',
    category: 'legal',
    description: 'Trust basics and estate planning guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_prenup',
    'ascension_divorce',
    'ascension_custody',
    'ascension_adoption'
  ],
    context: 'Triggers: user asks about Trust, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_prenup, ascension_divorce, ascension_custody, ascension_adoption. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_prenup',
    name: 'Aerynza Prenup',
    category: 'legal',
    description: 'Prenuptial agreement information and attorney referral',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_trust',
    'ascension_divorce',
    'ascension_custody',
    'ascension_adoption'
  ],
    context: 'Triggers: user asks about Prenup, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_trust, ascension_divorce, ascension_custody, ascension_adoption. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_divorce',
    name: 'Aerynza Divorce',
    category: 'legal',
    description: 'Divorce information and resource guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_trust',
    'ascension_prenup',
    'ascension_custody',
    'ascension_adoption'
  ],
    context: 'Triggers: user asks about Divorce, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_trust, ascension_prenup, ascension_custody, ascension_adoption. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_custody',
    name: 'Aerynza Custody',
    category: 'legal',
    description: 'Child custody information and co-parenting resources',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_trust',
    'ascension_prenup',
    'ascension_divorce',
    'ascension_adoption'
  ],
    context: 'Triggers: user asks about Custody, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_trust, ascension_prenup, ascension_divorce, ascension_adoption. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_adoption',
    name: 'Aerynza Adoption',
    category: 'legal',
    description: 'Adoption information, steps, and resources',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_trust',
    'ascension_prenup',
    'ascension_divorce',
    'ascension_custody'
  ],
    context: 'Triggers: user asks about Adoption, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_trust, ascension_prenup, ascension_divorce, ascension_custody. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_immigration',
    name: 'Aerynza Immigration',
    category: 'legal',
    description: 'Immigration path overview and document organization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_trust',
    'ascension_prenup',
    'ascension_divorce',
    'ascension_custody'
  ],
    context: 'Triggers: user asks about Immigration, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_trust, ascension_prenup, ascension_divorce, ascension_custody. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_contracts',
    name: 'Aerynza Contracts',
    category: 'legal',
    description: 'Contract review preparation and plain-language explanations',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_trust',
    'ascension_prenup',
    'ascension_divorce',
    'ascension_custody'
  ],
    context: 'Triggers: user asks about Contracts, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_trust, ascension_prenup, ascension_divorce, ascension_custody. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tenant',
    name: 'Aerynza Tenant',
    category: 'legal',
    description: 'Tenant rights, leases, and rental issues',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_trust',
    'ascension_prenup',
    'ascension_divorce',
    'ascension_custody'
  ],
    context: 'Triggers: user asks about Tenant, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_trust, ascension_prenup, ascension_divorce, ascension_custody. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_landlord',
    name: 'Aerynza Landlord',
    category: 'legal',
    description: 'Landlord responsibilities, leases, and tenant issues',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'legal',
    related_capabilities: [
    'ascension_will',
    'ascension_trust',
    'ascension_prenup',
    'ascension_divorce',
    'ascension_custody'
  ],
    context: 'Triggers: user asks about Landlord, starts a legal-domain quest, or needs a decision in this area. Cross-references: ascension_will, ascension_trust, ascension_prenup, ascension_divorce, ascension_custody. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_startup',
    name: 'Aerynza Startup',
    category: 'business',
    description: 'Startup ideation, validation, and early operations',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales',
    'ascension_brand'
  ],
    context: 'Triggers: user asks about Startup, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_business_plan, ascension_marketing, ascension_sales, ascension_brand. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_business_plan',
    name: 'Aerynza Business Plan',
    category: 'business',
    description: 'Business plan drafting and review',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_marketing',
    'ascension_sales',
    'ascension_brand'
  ],
    context: 'Triggers: user asks about Business Plan, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_marketing, ascension_sales, ascension_brand. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_marketing',
    name: 'Aerynza Marketing',
    category: 'business',
    description: 'Marketing strategy, channels, and campaigns',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_sales',
    'ascension_brand'
  ],
    context: 'Triggers: user asks about Marketing, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_sales, ascension_brand. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sales',
    name: 'Aerynza Sales',
    category: 'business',
    description: 'Sales process, outreach, and closing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_brand'
  ],
    context: 'Triggers: user asks about Sales, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_brand. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_brand',
    name: 'Aerynza Brand',
    category: 'business',
    description: 'Brand positioning, voice, and identity',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Brand, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_customer_service',
    name: 'Aerynza Customer Service',
    category: 'business',
    description: 'Customer service, support, and retention',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Customer Service, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_hr',
    name: 'Aerynza HR',
    category: 'business',
    description: 'Hiring, onboarding, and employee relations',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about HR, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fundraising',
    name: 'Aerynza Fundraising',
    category: 'business',
    description: 'Fundraising, investors, and grant seeking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Fundraising, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_pitch',
    name: 'Aerynza Pitch',
    category: 'business',
    description: 'Pitch deck and investor presentation practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Pitch, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_partnerships',
    name: 'Aerynza Partnerships',
    category: 'business',
    description: 'Partnership, alliance, and deal strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Partnerships, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_car_buying',
    name: 'Aerynza Car Buying',
    category: 'automotive',
    description: 'Car buying, negotiation, and research',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'automotive',
    related_capabilities: [
    'ascension_car_maintenance',
    'ascension_motorcycle',
    'ascension_bicycle',
    'ascension_boat',
    'ascension_rv'
  ],
    context: 'Triggers: user asks about Car Buying, starts a automotive-domain quest, or needs a decision in this area. Cross-references: ascension_car_maintenance, ascension_motorcycle, ascension_bicycle, ascension_boat, ascension_rv. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_car_maintenance',
    name: 'Aerynza Car Maintenance',
    category: 'automotive',
    description: 'Car maintenance, service schedules, and troubleshooting',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'automotive',
    related_capabilities: [
    'ascension_car_buying',
    'ascension_motorcycle',
    'ascension_bicycle',
    'ascension_boat',
    'ascension_rv'
  ],
    context: 'Triggers: user asks about Car Maintenance, starts a automotive-domain quest, or needs a decision in this area. Cross-references: ascension_car_buying, ascension_motorcycle, ascension_bicycle, ascension_boat, ascension_rv. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_motorcycle',
    name: 'Aerynza Motorcycle',
    category: 'automotive',
    description: 'Motorcycle riding, gear, and maintenance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'automotive',
    related_capabilities: [
    'ascension_car_buying',
    'ascension_car_maintenance',
    'ascension_bicycle',
    'ascension_boat',
    'ascension_rv'
  ],
    context: 'Triggers: user asks about Motorcycle, starts a automotive-domain quest, or needs a decision in this area. Cross-references: ascension_car_buying, ascension_car_maintenance, ascension_bicycle, ascension_boat, ascension_rv. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_bicycle',
    name: 'Aerynza Bicycle',
    category: 'automotive',
    description: 'Bicycle selection, maintenance, and riding',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'automotive',
    related_capabilities: [
    'ascension_car_buying',
    'ascension_car_maintenance',
    'ascension_motorcycle',
    'ascension_boat',
    'ascension_rv'
  ],
    context: 'Triggers: user asks about Bicycle, starts a automotive-domain quest, or needs a decision in this area. Cross-references: ascension_car_buying, ascension_car_maintenance, ascension_motorcycle, ascension_boat, ascension_rv. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_boat',
    name: 'Aerynza Boat',
    category: 'automotive',
    description: 'Boating basics, safety, and maintenance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'automotive',
    related_capabilities: [
    'ascension_car_buying',
    'ascension_car_maintenance',
    'ascension_motorcycle',
    'ascension_bicycle',
    'ascension_rv'
  ],
    context: 'Triggers: user asks about Boat, starts a automotive-domain quest, or needs a decision in this area. Cross-references: ascension_car_buying, ascension_car_maintenance, ascension_motorcycle, ascension_bicycle, ascension_rv. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_rv',
    name: 'Aerynza RV',
    category: 'automotive',
    description: 'RV travel, maintenance, and trip planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'automotive',
    related_capabilities: [
    'ascension_car_buying',
    'ascension_car_maintenance',
    'ascension_motorcycle',
    'ascension_bicycle',
    'ascension_boat'
  ],
    context: 'Triggers: user asks about RV, starts a automotive-domain quest, or needs a decision in this area. Cross-references: ascension_car_buying, ascension_car_maintenance, ascension_motorcycle, ascension_bicycle, ascension_boat. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_electric_vehicle',
    name: 'Aerynza Electric Vehicle',
    category: 'automotive',
    description: 'EV selection, charging, and ownership',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'automotive',
    related_capabilities: [
    'ascension_car_buying',
    'ascension_car_maintenance',
    'ascension_motorcycle',
    'ascension_bicycle',
    'ascension_boat'
  ],
    context: 'Triggers: user asks about Electric Vehicle, starts a automotive-domain quest, or needs a decision in this area. Cross-references: ascension_car_buying, ascension_car_maintenance, ascension_motorcycle, ascension_bicycle, ascension_boat. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_public_transit',
    name: 'Aerynza Public Transit',
    category: 'travel',
    description: 'Public transit navigation, schedules, and tips',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'travel',
    related_capabilities: [
    'ascension_rideshare',
    'ascension_flight',
    'ascension_travel_insurance'
  ],
    context: 'Triggers: user asks about Public Transit, starts a travel-domain quest, or needs a decision in this area. Cross-references: ascension_rideshare, ascension_flight, ascension_travel_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_rideshare',
    name: 'Aerynza Rideshare',
    category: 'travel',
    description: 'Rideshare, taxi, and driver guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'travel',
    related_capabilities: [
    'ascension_public_transit',
    'ascension_flight',
    'ascension_travel_insurance'
  ],
    context: 'Triggers: user asks about Rideshare, starts a travel-domain quest, or needs a decision in this area. Cross-references: ascension_public_transit, ascension_flight, ascension_travel_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_flight',
    name: 'Aerynza Flight',
    category: 'travel',
    description: 'Flight booking, airports, and travel strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'travel',
    related_capabilities: [
    'ascension_public_transit',
    'ascension_rideshare',
    'ascension_travel_insurance'
  ],
    context: 'Triggers: user asks about Flight, starts a travel-domain quest, or needs a decision in this area. Cross-references: ascension_public_transit, ascension_rideshare, ascension_travel_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cricket',
    name: 'Aerynza Cricket',
    category: 'sports',
    description: 'Cricket rules, strategy, and fan questions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_basketball',
    'ascension_football',
    'ascension_baseball',
    'ascension_soccer',
    'ascension_tennis'
  ],
    context: 'Triggers: user asks about Cricket, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_basketball, ascension_football, ascension_baseball, ascension_soccer, ascension_tennis. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_basketball',
    name: 'Aerynza Basketball',
    category: 'sports',
    description: 'Basketball strategy, training, and analysis',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_football',
    'ascension_baseball',
    'ascension_soccer',
    'ascension_tennis'
  ],
    context: 'Triggers: user asks about Basketball, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_football, ascension_baseball, ascension_soccer, ascension_tennis. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_football',
    name: 'Aerynza Football',
    category: 'sports',
    description: 'Football strategy, training, and analysis',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_basketball',
    'ascension_baseball',
    'ascension_soccer',
    'ascension_tennis'
  ],
    context: 'Triggers: user asks about Football, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_basketball, ascension_baseball, ascension_soccer, ascension_tennis. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_baseball',
    name: 'Aerynza Baseball',
    category: 'sports',
    description: 'Baseball rules, strategy, and analysis',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_basketball',
    'ascension_football',
    'ascension_soccer',
    'ascension_tennis'
  ],
    context: 'Triggers: user asks about Baseball, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_basketball, ascension_football, ascension_soccer, ascension_tennis. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_soccer',
    name: 'Aerynza Soccer',
    category: 'sports',
    description: 'Soccer tactics, training, and fan questions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_basketball',
    'ascension_football',
    'ascension_baseball',
    'ascension_tennis'
  ],
    context: 'Triggers: user asks about Soccer, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_basketball, ascension_football, ascension_baseball, ascension_tennis. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tennis',
    name: 'Aerynza Tennis',
    category: 'sports',
    description: 'Tennis technique, training, and matches',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_basketball',
    'ascension_football',
    'ascension_baseball',
    'ascension_soccer'
  ],
    context: 'Triggers: user asks about Tennis, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_basketball, ascension_football, ascension_baseball, ascension_soccer. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_golf',
    name: 'Aerynza Golf',
    category: 'sports',
    description: 'Golf swing, course strategy, and equipment',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_basketball',
    'ascension_football',
    'ascension_baseball',
    'ascension_soccer'
  ],
    context: 'Triggers: user asks about Golf, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_basketball, ascension_football, ascension_baseball, ascension_soccer. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_hockey',
    name: 'Aerynza Hockey',
    category: 'sports',
    description: 'Hockey rules, strategy, and training',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_basketball',
    'ascension_football',
    'ascension_baseball',
    'ascension_soccer'
  ],
    context: 'Triggers: user asks about Hockey, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_basketball, ascension_football, ascension_baseball, ascension_soccer. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_esports',
    name: 'Aerynza Esports',
    category: 'sports',
    description: 'Esports games, teams, and strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_basketball',
    'ascension_football',
    'ascension_baseball',
    'ascension_soccer'
  ],
    context: 'Triggers: user asks about Esports, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_basketball, ascension_football, ascension_baseball, ascension_soccer. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fantasy',
    name: 'Aerynza Fantasy',
    category: 'sports',
    description: 'Fantasy sports draft, lineup, and strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'sports',
    related_capabilities: [
    'ascension_cricket',
    'ascension_basketball',
    'ascension_football',
    'ascension_baseball',
    'ascension_soccer'
  ],
    context: 'Triggers: user asks about Fantasy, starts a sports-domain quest, or needs a decision in this area. Cross-references: ascension_cricket, ascension_basketball, ascension_football, ascension_baseball, ascension_soccer. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_horoscope',
    name: 'Aerynza Horoscope',
    category: 'entertainment',
    description: 'Horoscope, astrology, and personal sign guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_astrology'
  ],
    context: 'Triggers: user asks about Horoscope, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_astrology. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_astrology',
    name: 'Aerynza Astrology',
    category: 'entertainment',
    description: 'Astrology chart basics and sign compatibility',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Astrology, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tarot',
    name: 'Aerynza Tarot',
    category: 'entertainment',
    description: 'Tarot card meanings and reflective readings',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Tarot, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tattoo',
    name: 'Aerynza Tattoo',
    category: 'style',
    description: 'Tattoo ideas, styles, and aftercare',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch',
    'ascension_shoes'
  ],
    context: 'Triggers: user asks about Tattoo, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_piercing, ascension_perfume, ascension_jewelry, ascension_watch, ascension_shoes. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_piercing',
    name: 'Aerynza Piercing',
    category: 'style',
    description: 'Piercing types, care, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch',
    'ascension_shoes'
  ],
    context: 'Triggers: user asks about Piercing, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_perfume, ascension_jewelry, ascension_watch, ascension_shoes. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_perfume',
    name: 'Aerynza Perfume',
    category: 'style',
    description: 'Fragrance, perfume, and scent guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_jewelry',
    'ascension_watch',
    'ascension_shoes'
  ],
    context: 'Triggers: user asks about Perfume, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_jewelry, ascension_watch, ascension_shoes. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_jewelry',
    name: 'Aerynza Jewelry',
    category: 'style',
    description: 'Jewelry selection, care, and occasion matching',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_watch',
    'ascension_shoes'
  ],
    context: 'Triggers: user asks about Jewelry, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_watch, ascension_shoes. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_watch',
    name: 'Aerynza Watch',
    category: 'style',
    description: 'Watch selection, care, and collection guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_shoes'
  ],
    context: 'Triggers: user asks about Watch, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_jewelry, ascension_shoes. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_shoes',
    name: 'Aerynza Shoes',
    category: 'style',
    description: 'Shoe selection, fit, and care',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch'
  ],
    context: 'Triggers: user asks about Shoes, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_jewelry, ascension_watch. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_bag',
    name: 'Aerynza Bag',
    category: 'style',
    description: 'Bag and luggage selection and care',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch'
  ],
    context: 'Triggers: user asks about Bag, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_jewelry, ascension_watch. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_wallet',
    name: 'Aerynza Wallet',
    category: 'style',
    description: 'Wallet selection and organization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch'
  ],
    context: 'Triggers: user asks about Wallet, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_jewelry, ascension_watch. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sunglasses',
    name: 'Aerynza Sunglasses',
    category: 'style',
    description: 'Sunglasses, UV protection, and style',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch'
  ],
    context: 'Triggers: user asks about Sunglasses, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_jewelry, ascension_watch. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_haircut',
    name: 'Aerynza Haircut',
    category: 'style',
    description: 'Haircut styles, face shape, and maintenance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch'
  ],
    context: 'Triggers: user asks about Haircut, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_jewelry, ascension_watch. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_beard',
    name: 'Aerynza Beard',
    category: 'style',
    description: 'Beard styles, growth, and grooming',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch'
  ],
    context: 'Triggers: user asks about Beard, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_jewelry, ascension_watch. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_makeup',
    name: 'Aerynza Makeup',
    category: 'style',
    description: 'Makeup techniques, products, and looks',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'style',
    related_capabilities: [
    'ascension_tattoo',
    'ascension_piercing',
    'ascension_perfume',
    'ascension_jewelry',
    'ascension_watch'
  ],
    context: 'Triggers: user asks about Makeup, starts a style-domain quest, or needs a decision in this area. Cross-references: ascension_tattoo, ascension_piercing, ascension_perfume, ascension_jewelry, ascension_watch. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_camping',
    name: 'Aerynza Camping',
    category: 'wellness',
    description: 'Camping gear, sites, and outdoor skills',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Camping, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fishing',
    name: 'Aerynza Fishing',
    category: 'wellness',
    description: 'Fishing techniques, gear, and locations',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Fishing, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_hunting',
    promoted: false,
    name: 'Aerynza Hunting',
    category: 'wellness',
    description: 'Hunting safety, gear, and ethics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Hunting, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_shooting',
    promoted: false,
    name: 'Aerynza Shooting',
    category: 'wellness',
    description: 'Firearm safety, range practice, and training',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Shooting, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_archery',
    promoted: false,
    name: 'Aerynza Archery',
    category: 'wellness',
    description: 'Archery technique, gear, and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Archery, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fencing',
    promoted: false,
    name: 'Aerynza Fencing',
    category: 'wellness',
    description: 'Fencing styles, gear, and training',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Fencing, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_boxing',
    promoted: false,
    name: 'Aerynza Boxing',
    category: 'wellness',
    description: 'Boxing technique, training, and conditioning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Boxing, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_wrestling',
    promoted: false,
    name: 'Aerynza Wrestling',
    category: 'wellness',
    description: 'Wrestling styles, training, and technique',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Wrestling, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_gymnastics',
    name: 'Aerynza Gymnastics',
    category: 'wellness',
    description: 'Gymnastics skills, training, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Gymnastics, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_skateboarding',
    name: 'Aerynza Skateboarding',
    category: 'wellness',
    description: 'Skateboarding tricks, gear, and spots',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Skateboarding, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_surfing',
    name: 'Aerynza Surfing',
    category: 'wellness',
    description: 'Surfing technique, waves, and board selection',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Surfing, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_skiing',
    name: 'Aerynza Skiing',
    category: 'wellness',
    description: 'Skiing technique, gear, and resorts',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Skiing, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_snowboarding',
    name: 'Aerynza Snowboarding',
    category: 'wellness',
    description: 'Snowboarding technique, gear, and resorts',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Snowboarding, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_ice_skating',
    name: 'Aerynza Ice Skating',
    category: 'wellness',
    description: 'Ice skating technique, gear, and rinks',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Ice Skating, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_roller_skating',
    name: 'Aerynza Roller Skating',
    category: 'wellness',
    description: 'Roller skating technique, gear, and spots',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Roller Skating, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_magic',
    name: 'Aerynza Magic',
    category: 'entertainment',
    description: 'Magic tricks, sleight of hand, and performance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Magic, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_comedy',
    name: 'Aerynza Comedy',
    category: 'entertainment',
    description: 'Comedy writing, timing, and performance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Comedy, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_jokes',
    name: 'Aerynza Jokes',
    category: 'entertainment',
    description: 'Joke writing, setups, and punchlines',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Jokes, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_riddles',
    name: 'Aerynza Riddles',
    category: 'entertainment',
    description: 'Riddles, brain teasers, and lateral thinking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Riddles, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_puzzles',
    name: 'Aerynza Puzzles',
    category: 'entertainment',
    description: 'Puzzles, logic, and problem-solving games',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Puzzles, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_standup',
    name: 'Aerynza Standup',
    category: 'entertainment',
    description: 'Stand-up comedy writing and performance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Standup, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_poetry',
    name: 'Aerynza Poetry',
    category: 'creation',
    description: 'Poetry forms, technique, and writing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Poetry, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_lyrics',
    name: 'Aerynza Lyrics',
    category: 'creation',
    description: 'Lyric writing, rhyme, and song structure',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Lyrics, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_storytelling',
    name: 'Aerynza Storytelling',
    category: 'creation',
    description: 'Story structure, narrative, and oral telling',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Storytelling, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fanfiction',
    name: 'Aerynza Fanfiction',
    category: 'creation',
    description: 'Fanfiction writing, tropes, and platforms',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Fanfiction, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cosplay',
    name: 'Aerynza Cosplay',
    category: 'entertainment',
    description: 'Cosplay design, construction, and events',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Cosplay, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_roleplay',
    name: 'Aerynza Roleplay',
    category: 'entertainment',
    description: 'Roleplay genres, character creation, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Roleplay, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_reviews',
    name: 'Aerynza Reviews',
    category: 'research',
    description: 'Product, media, and service review writing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'research',
    related_capabilities: [
    'ascension_research',
    'ascension_news'
  ],
    context: 'Triggers: user asks about Reviews, starts a research-domain quest, or needs a decision in this area. Cross-references: ascension_research, ascension_news. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_trivia',
    name: 'Aerynza Trivia',
    category: 'entertainment',
    description: 'Trivia facts, hosting, and categories',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Trivia, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_boardgames',
    name: 'Aerynza Board Games',
    category: 'entertainment',
    description: 'Board game rules, strategy, and recommendations',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Board Games, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_streaming',
    name: 'Aerynza Streaming',
    category: 'creation',
    description: 'Live streaming setup, platforms, and growth',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Streaming, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_youtube',
    name: 'Aerynza YouTube',
    category: 'creation',
    description: 'YouTube content, SEO, and channel growth',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about YouTube, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tiktok',
    name: 'Aerynza TikTok',
    category: 'creation',
    description: 'TikTok content, trends, and strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about TikTok, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_instagram',
    name: 'Aerynza Instagram',
    category: 'creation',
    description: 'Instagram content, reels, and growth',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Instagram, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_twitter',
    name: 'Aerynza Twitter',
    category: 'creation',
    description: 'Twitter/X content, threads, and engagement',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Twitter, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_linkedin',
    name: 'Aerynza LinkedIn',
    category: 'work',
    description: 'LinkedIn profile, content, and networking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about LinkedIn, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_facebook',
    name: 'Aerynza Facebook',
    category: 'social',
    description: 'Facebook groups, pages, and events',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'social',
    related_capabilities: [
    'relationship_graph',
    'ascension_reddit',
    'ascension_discord'
  ],
    context: 'Triggers: user asks about Facebook, starts a social-domain quest, or needs a decision in this area. Cross-references: relationship_graph, ascension_reddit, ascension_discord. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_reddit',
    name: 'Aerynza Reddit',
    category: 'social',
    description: 'Reddit communities, posts, and etiquette',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'social',
    related_capabilities: [
    'relationship_graph',
    'ascension_facebook',
    'ascension_discord'
  ],
    context: 'Triggers: user asks about Reddit, starts a social-domain quest, or needs a decision in this area. Cross-references: relationship_graph, ascension_facebook, ascension_discord. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_discord',
    name: 'Aerynza Discord',
    category: 'social',
    description: 'Discord servers, roles, and moderation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'social',
    related_capabilities: [
    'relationship_graph',
    'ascension_facebook',
    'ascension_reddit'
  ],
    context: 'Triggers: user asks about Discord, starts a social-domain quest, or needs a decision in this area. Cross-references: relationship_graph, ascension_facebook, ascension_reddit. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_slack',
    name: 'Aerynza Slack',
    category: 'work',
    description: 'Slack workspace, channels, and bots',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Slack, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_teams',
    name: 'Aerynza Teams',
    category: 'work',
    description: 'Microsoft Teams meetings and collaboration',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Teams, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_zoom',
    name: 'Aerynza Zoom',
    category: 'work',
    description: 'Zoom meetings, webinars, and setup',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Zoom, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_meet',
    name: 'Aerynza Meet',
    category: 'work',
    description: 'Google Meet calls and settings',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Meet, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_webex',
    name: 'Aerynza Webex',
    category: 'work',
    description: 'Webex meetings and setup',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'work',
    related_capabilities: [
    'ascension_project',
    'ascension_task',
    'ascension_remote',
    'ascension_interview',
    'ascension_resume'
  ],
    context: 'Triggers: user asks about Webex, starts a work-domain quest, or needs a decision in this area. Cross-references: ascension_project, ascension_task, ascension_remote, ascension_interview, ascension_resume. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_obs',
    name: 'Aerynza OBS',
    category: 'creation',
    description: 'OBS Studio setup, scenes, and streaming',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about OBS, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_chess',
    name: 'Aerynza Chess',
    category: 'entertainment',
    description: 'Chess openings, tactics, and strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Chess, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_poker',
    name: 'Aerynza Poker',
    category: 'entertainment',
    description: 'Poker strategy, odds, and bankroll',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Poker, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_blackjack',
    name: 'Aerynza Blackjack',
    category: 'entertainment',
    description: 'Blackjack strategy and odds',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Blackjack, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_betting',
    name: 'Aerynza Betting',
    category: 'entertainment',
    description: 'Sports betting, odds, and risk management',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Betting, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_lottery',
    name: 'Aerynza Lottery',
    category: 'entertainment',
    description: 'Lottery odds and expectation guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Lottery, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_auction',
    name: 'Aerynza Auction',
    category: 'lifestyle',
    description: 'Auction bidding, valuation, and strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'lifestyle',
    related_capabilities: [
    'ascension_fashion',
    'ascension_shopping',
    'ascension_collector',
    'ascension_antiques',
    'ascension_stamps'
  ],
    context: 'Triggers: user asks about Auction, starts a lifestyle-domain quest, or needs a decision in this area. Cross-references: ascension_fashion, ascension_shopping, ascension_collector, ascension_antiques, ascension_stamps. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_collector',
    name: 'Aerynza Collector',
    category: 'lifestyle',
    description: 'Collecting strategy, valuation, and curation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'lifestyle',
    related_capabilities: [
    'ascension_fashion',
    'ascension_shopping',
    'ascension_auction',
    'ascension_antiques',
    'ascension_stamps'
  ],
    context: 'Triggers: user asks about Collector, starts a lifestyle-domain quest, or needs a decision in this area. Cross-references: ascension_fashion, ascension_shopping, ascension_auction, ascension_antiques, ascension_stamps. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_antiques',
    name: 'Aerynza Antiques',
    category: 'lifestyle',
    description: 'Antique identification, value, and care',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'lifestyle',
    related_capabilities: [
    'ascension_fashion',
    'ascension_shopping',
    'ascension_auction',
    'ascension_collector',
    'ascension_stamps'
  ],
    context: 'Triggers: user asks about Antiques, starts a lifestyle-domain quest, or needs a decision in this area. Cross-references: ascension_fashion, ascension_shopping, ascension_auction, ascension_collector, ascension_stamps. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_stamps',
    name: 'Aerynza Stamps',
    category: 'lifestyle',
    description: 'Stamp collecting and valuation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'lifestyle',
    related_capabilities: [
    'ascension_fashion',
    'ascension_shopping',
    'ascension_auction',
    'ascension_collector',
    'ascension_antiques'
  ],
    context: 'Triggers: user asks about Stamps, starts a lifestyle-domain quest, or needs a decision in this area. Cross-references: ascension_fashion, ascension_shopping, ascension_auction, ascension_collector, ascension_antiques. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_coins',
    name: 'Aerynza Coins',
    category: 'lifestyle',
    description: 'Coin collecting and numismatics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'lifestyle',
    related_capabilities: [
    'ascension_fashion',
    'ascension_shopping',
    'ascension_auction',
    'ascension_collector',
    'ascension_antiques'
  ],
    context: 'Triggers: user asks about Coins, starts a lifestyle-domain quest, or needs a decision in this area. Cross-references: ascension_fashion, ascension_shopping, ascension_auction, ascension_collector, ascension_antiques. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_comics',
    name: 'Aerynza Comics',
    category: 'entertainment',
    description: 'Comic books, grading, and collecting',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Comics, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_trading_cards',
    name: 'Aerynza Trading Cards',
    category: 'entertainment',
    description: 'Trading cards, value, and protection',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Trading Cards, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_vinyl',
    name: 'Aerynza Vinyl',
    category: 'lifestyle',
    description: 'Vinyl records, collecting, and care',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'lifestyle',
    related_capabilities: [
    'ascension_fashion',
    'ascension_shopping',
    'ascension_auction',
    'ascension_collector',
    'ascension_antiques'
  ],
    context: 'Triggers: user asks about Vinyl, starts a lifestyle-domain quest, or needs a decision in this area. Cross-references: ascension_fashion, ascension_shopping, ascension_auction, ascension_collector, ascension_antiques. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_concerts',
    name: 'Aerynza Concerts',
    category: 'entertainment',
    description: 'Concert planning, tickets, and etiquette',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Concerts, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_festivals',
    name: 'Aerynza Festivals',
    category: 'entertainment',
    description: 'Festival planning, packing, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Festivals, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_karaoke',
    name: 'Aerynza Karaoke',
    category: 'entertainment',
    description: 'Karaoke song choice, setup, and fun',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Karaoke, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_casino',
    name: 'Aerynza Casino',
    category: 'entertainment',
    description: 'Casino game odds, strategy, and risk awareness',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Casino, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sports_betting',
    name: 'Aerynza Sports Betting',
    category: 'entertainment',
    description: 'Sports betting strategy and risk management',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about Sports Betting, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_daytrading',
    name: 'Aerynza Day Trading',
    category: 'finance',
    description: 'Day trading strategy, risk, and psychology',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Day Trading, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_swingtrading',
    name: 'Aerynza Swing Trading',
    category: 'finance',
    description: 'Swing trading setups and position management',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Swing Trading, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_forex',
    name: 'Aerynza Forex',
    category: 'finance',
    description: 'Forex basics, pairs, and risk',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Forex, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_crypto',
    name: 'Aerynza Crypto',
    category: 'finance',
    description: 'Cryptocurrency basics, custody, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Crypto, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_nfts',
    name: 'Aerynza NFTs',
    category: 'finance',
    description: 'NFTs, marketplaces, and valuation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about NFTs, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mining',
    name: 'Aerynza Mining',
    category: 'engineering',
    description: 'Crypto mining hardware and profitability',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing'
  ],
    context: 'Triggers: user asks about Mining, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_security_tech, ascension_testing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_staking',
    name: 'Aerynza Staking',
    category: 'finance',
    description: 'Staking, yields, and validator selection',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Staking, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_defi',
    name: 'Aerynza DeFi',
    category: 'finance',
    description: 'DeFi protocols, yields, and risks',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about DeFi, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_dao',
    name: 'Aerynza DAO',
    category: 'finance',
    description: 'DAO governance and participation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about DAO, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_airdrop',
    name: 'Aerynza Airdrop',
    category: 'finance',
    description: 'Airdrop farming, safety, and taxes',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Airdrop, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_presale',
    name: 'Aerynza Presale',
    category: 'finance',
    description: 'Presale research, red flags, and allocation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Presale, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_whitelist',
    name: 'Aerynza Whitelist',
    category: 'finance',
    description: 'Whitelist registration and security',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Whitelist, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_nodes',
    name: 'Aerynza Nodes',
    category: 'engineering',
    description: 'Blockchain nodes, setup, and maintenance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
    'ascension_devops',
    'ascension_cloud',
    'ascension_databases',
    'ascension_security_tech',
    'ascension_testing'
  ],
    context: 'Triggers: user asks about Nodes, starts a engineering-domain quest, or needs a decision in this area. Cross-references: ascension_devops, ascension_cloud, ascension_databases, ascension_security_tech, ascension_testing. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_3d_printing',
    name: 'Aerynza 3D Printing',
    category: 'creation',
    description: '3D printing, slicing, and materials',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about 3D Printing, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_laser_cutting',
    name: 'Aerynza Laser Cutting',
    category: 'creation',
    description: 'Laser cutting, engraving, and design',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Laser Cutting, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cnc',
    name: 'Aerynza CNC',
    category: 'creation',
    description: 'CNC machining, tooling, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about CNC, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_woodworking',
    name: 'Aerynza Woodworking',
    category: 'creation',
    description: 'Woodworking projects, tools, and joinery',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Woodworking, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_metalworking',
    name: 'Aerynza Metalworking',
    category: 'creation',
    description: 'Metalworking tools, forging, and finishing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Metalworking, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_welding',
    name: 'Aerynza Welding',
    category: 'creation',
    description: 'Welding processes, safety, and certification',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Welding, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_soldering',
    name: 'Aerynza Soldering',
    category: 'creation',
    description: 'Soldering, desoldering, and circuit repair',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Soldering, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_electronics',
    name: 'Aerynza Electronics',
    category: 'creation',
    description: 'Electronics basics, circuits, and components',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Electronics, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_arduino',
    name: 'Aerynza Arduino',
    category: 'creation',
    description: 'Arduino projects, sensors, and code',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Arduino, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_raspberry_pi',
    name: 'Aerynza Raspberry Pi',
    category: 'creation',
    description: 'Raspberry Pi projects, OS, and hardware',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Raspberry Pi, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_robotics',
    name: 'Aerynza Robotics',
    category: 'creation',
    description: 'Robotics kits, programming, and projects',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Robotics, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_drones',
    name: 'Aerynza Drones',
    category: 'creation',
    description: 'Drones, flying, regulations, and repairs',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Drones, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_rc',
    name: 'Aerynza RC',
    category: 'entertainment',
    description: 'RC cars, planes, boats, and maintenance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'entertainment',
    related_capabilities: [
    'ascension_movies',
    'ascension_books',
    'ascension_sports',
    'ascension_games',
    'ascension_horoscope'
  ],
    context: 'Triggers: user asks about RC, starts a entertainment-domain quest, or needs a decision in this area. Cross-references: ascension_movies, ascension_books, ascension_sports, ascension_games, ascension_horoscope. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_ham_radio',
    name: 'Aerynza Ham Radio',
    category: 'creation',
    description: 'Ham radio, licensing, and operation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Ham Radio, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_astronomy',
    name: 'Aerynza Astronomy',
    category: 'knowledge',
    description: 'Astronomy, stargazing, and equipment',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Astronomy, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_photography_gear',
    name: 'Aerynza Photography Gear',
    category: 'creation',
    description: 'Cameras, lenses, and photography equipment',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Photography Gear, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_video_editing',
    name: 'Aerynza Video Editing',
    category: 'creation',
    description: 'Video editing, software, and workflow',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Video Editing, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_color_grading',
    name: 'Aerynza Color Grading',
    category: 'creation',
    description: 'Color grading, LUTs, and look development',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Color Grading, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sound_design',
    name: 'Aerynza Sound Design',
    category: 'creation',
    description: 'Sound design, Foley, and audio libraries',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Sound Design, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mixing',
    name: 'Aerynza Mixing',
    category: 'creation',
    description: 'Audio mixing, levels, and balance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Mixing, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mastering',
    name: 'Aerynza Mastering',
    category: 'creation',
    description: 'Audio mastering, loudness, and delivery',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Mastering, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_voiceover',
    name: 'Aerynza Voiceover',
    category: 'creation',
    description: 'Voiceover recording, performance, and equipment',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Voiceover, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_podcast_production',
    name: 'Aerynza Podcast Production',
    category: 'creation',
    description: 'Podcast production, editing, and publishing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Podcast Production, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_youtube_seo',
    name: 'Aerynza YouTube SEO',
    category: 'creation',
    description: 'YouTube SEO, titles, and thumbnails',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about YouTube SEO, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_thumbnail',
    name: 'Aerynza Thumbnail',
    category: 'creation',
    description: 'Thumbnail design, text, and contrast',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Thumbnail, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_branding',
    name: 'Aerynza Branding',
    category: 'creation',
    description: 'Brand identity, voice, and assets',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Branding, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_merchandise',
    name: 'Aerynza Merchandise',
    category: 'business',
    description: 'Merch design, production, and sales',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Merchandise, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_crowdfunding',
    name: 'Aerynza Crowdfunding',
    category: 'business',
    description: 'Crowdfunding campaigns, rewards, and promotion',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Crowdfunding, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_patreon',
    name: 'Aerynza Patreon',
    category: 'business',
    description: 'Patreon tiers, rewards, and growth',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Patreon, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sponsorships',
    name: 'Aerynza Sponsorships',
    category: 'business',
    description: 'Sponsorship outreach and deal terms',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Sponsorships, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_affiliate',
    name: 'Aerynza Affiliate',
    category: 'business',
    description: 'Affiliate marketing, links, and commissions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Affiliate, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_ecommerce',
    name: 'Aerynza Ecommerce',
    category: 'business',
    description: 'Ecommerce strategy, platforms, and operations',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Ecommerce, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_shopify',
    name: 'Aerynza Shopify',
    category: 'business',
    description: 'Shopify store setup, apps, and optimization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Shopify, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_woocommerce',
    name: 'Aerynza WooCommerce',
    category: 'business',
    description: 'WooCommerce setup, plugins, and payments',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about WooCommerce, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_amazon',
    name: 'Aerynza Amazon',
    category: 'business',
    description: 'Amazon selling, FBA, and listings',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Amazon, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_ebay',
    name: 'Aerynza eBay',
    category: 'business',
    description: 'eBay selling, auctions, and shipping',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about eBay, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_etsy',
    name: 'Aerynza Etsy',
    category: 'business',
    description: 'Etsy listings, SEO, and shop management',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Etsy, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_dropshipping',
    name: 'Aerynza Dropshipping',
    category: 'business',
    description: 'Dropshipping suppliers, products, and risks',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Dropshipping, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_print_on_demand',
    name: 'Aerynza Print On Demand',
    category: 'business',
    description: 'Print on demand products and suppliers',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Print On Demand, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fulfillment',
    name: 'Aerynza Fulfillment',
    category: 'business',
    description: 'Order fulfillment, 3PL, and warehousing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Fulfillment, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_inventory',
    name: 'Aerynza Inventory',
    category: 'business',
    description: 'Inventory tracking, forecasting, and management',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Inventory, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_pos',
    name: 'Aerynza POS',
    category: 'business',
    description: 'Point of sale systems and setup',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about POS, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_import',
    name: 'Aerynza Import',
    category: 'business',
    description: 'Importing goods, suppliers, and customs',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Import, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_export',
    name: 'Aerynza Export',
    category: 'business',
    description: 'Exporting goods, compliance, and markets',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Export, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tariffs',
    name: 'Aerynza Tariffs',
    category: 'business',
    description: 'Tariffs, duties, and trade compliance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Tariffs, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_shipping',
    name: 'Aerynza Shipping',
    category: 'business',
    description: 'Shipping carriers, rates, and packaging',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Shipping, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_customer_support',
    name: 'Aerynza Customer Support',
    category: 'business',
    description: 'Customer support, tickets, and responses',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Customer Support, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_helpdesk',
    name: 'Aerynza Helpdesk',
    category: 'business',
    description: 'Helpdesk organization, priorities, and SLAs',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Helpdesk, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_ticketing',
    name: 'Aerynza Ticketing',
    category: 'business',
    description: 'Ticket creation, routing, and resolution',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Ticketing, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_live_chat',
    name: 'Aerynza Live Chat',
    category: 'business',
    description: 'Live chat scripts, routing, and handoff',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Live Chat, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_chatbot',
    name: 'Aerynza Chatbot',
    category: 'business',
    description: 'Chatbot design, flows, and fallback',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Chatbot, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_knowledge_base',
    name: 'Aerynza Knowledge Base',
    category: 'business',
    description: 'Knowledge base articles, search, and updates',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Knowledge Base, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_faq',
    name: 'Aerynza FAQ',
    category: 'business',
    description: 'FAQ generation, maintenance, and answers',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about FAQ, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_onboarding',
    name: 'Aerynza Onboarding',
    category: 'business',
    description: 'Customer and employee onboarding flows',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Onboarding, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_retention',
    name: 'Aerynza Retention',
    category: 'business',
    description: 'Customer retention strategies and signals',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Retention, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_churn',
    name: 'Aerynza Churn',
    category: 'business',
    description: 'Churn analysis and prevention',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Churn, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_upsell',
    name: 'Aerynza Upsell',
    category: 'business',
    description: 'Upsell recommendations and timing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Upsell, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cross_sell',
    name: 'Aerynza Cross Sell',
    category: 'business',
    description: 'Cross-sell pairing and messaging',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Cross Sell, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_loyalty',
    name: 'Aerynza Loyalty',
    category: 'business',
    description: 'Loyalty programs, points, and rewards',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Loyalty, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_referral',
    name: 'Aerynza Referral',
    category: 'business',
    description: 'Referral program design and tracking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Referral, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_reputation',
    name: 'Aerynza Reputation',
    category: 'business',
    description: 'Online reputation monitoring and response',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Reputation, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_accounting',
    name: 'Aerynza Accounting',
    category: 'finance',
    description: 'Accounting principles, bookkeeping, and reports',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Accounting, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_bookkeeping',
    name: 'Aerynza Bookkeeping',
    category: 'finance',
    description: 'Bookkeeping entries, ledgers, and reconciliation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Bookkeeping, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_invoicing',
    name: 'Aerynza Invoicing',
    category: 'finance',
    description: 'Invoice creation, terms, and collection',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Invoicing, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_payroll',
    name: 'Aerynza Payroll',
    category: 'finance',
    description: 'Payroll processing, taxes, and compliance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Payroll, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_budgeting',
    name: 'Aerynza Budgeting',
    category: 'finance',
    description: 'Budget creation, tracking, and variance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Budgeting, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_expenses',
    name: 'Aerynza Expenses',
    category: 'finance',
    description: 'Expense tracking, reimbursement, and policies',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Expenses, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_business_taxes',
    name: 'Aerynza Business Taxes',
    category: 'finance',
    description: 'Business tax planning, deductions, and filing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Business Taxes, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_audit',
    name: 'Aerynza Audit',
    category: 'finance',
    description: 'Audit preparation, documentation, and response',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Audit, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_compliance',
    name: 'Aerynza Compliance',
    category: 'business',
    description: 'Regulatory compliance, policies, and controls',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Compliance, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_grants',
    name: 'Aerynza Grants',
    category: 'business',
    description: 'Grant research, applications, and reporting',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Grants, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_loans',
    name: 'Aerynza Loans',
    category: 'finance',
    description: 'Loan types, terms, and applications',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Loans, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_credit',
    name: 'Aerynza Credit',
    category: 'finance',
    description: 'Credit cards, lines, and management',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Credit, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_debt',
    name: 'Aerynza Debt',
    category: 'finance',
    description: 'Debt payoff, consolidation, and strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Debt, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_credit_score',
    name: 'Aerynza Credit Score',
    category: 'finance',
    description: 'Credit score building and repair',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Credit Score, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mortgage',
    name: 'Aerynza Mortgage',
    category: 'finance',
    description: 'Mortgage types, rates, and refinancing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Mortgage, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_insurance_review',
    name: 'Aerynza Insurance Review',
    category: 'finance',
    description: 'Insurance policy review and coverage gaps',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Insurance Review, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_policy_review',
    name: 'Aerynza Policy Review',
    category: 'finance',
    description: 'Policy terms, exclusions, and renewals',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Policy Review, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_deductible',
    name: 'Aerynza Deductible',
    category: 'finance',
    description: 'Deductible strategy and tradeoffs',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Deductible, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_premium',
    name: 'Aerynza Premium',
    category: 'finance',
    description: 'Premium pricing, payment, and discounts',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Premium, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_hsa',
    name: 'Aerynza HSA',
    category: 'finance',
    description: 'Health Savings Accounts and strategy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about HSA, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fsa',
    name: 'Aerynza FSA',
    category: 'finance',
    description: 'Flexible Spending Accounts and planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about FSA, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_benefits',
    name: 'Aerynza Benefits',
    category: 'business',
    description: 'Employee benefits packages and selection',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Benefits, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_open_enrollment',
    name: 'Aerynza Open Enrollment',
    category: 'business',
    description: 'Open enrollment choices and deadlines',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Open Enrollment, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_workers_comp',
    name: 'Aerynza Workers Comp',
    category: 'business',
    description: 'Workers compensation basics and claims',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Workers Comp, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_liability_insurance',
    name: 'Aerynza Liability Insurance',
    category: 'finance',
    description: 'Liability insurance types and limits',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Liability Insurance, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_umbrella_insurance',
    name: 'Aerynza Umbrella Insurance',
    category: 'finance',
    description: 'Umbrella policy limits and use cases',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Umbrella Insurance, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_flood_insurance',
    name: 'Aerynza Flood Insurance',
    category: 'finance',
    description: 'Flood insurance, zones, and claims',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Flood Insurance, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_earthquake_insurance',
    name: 'Aerynza Earthquake Insurance',
    category: 'finance',
    description: 'Earthquake coverage and risk',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Earthquake Insurance, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_pet_insurance',
    name: 'Aerynza Pet Insurance',
    category: 'finance',
    description: 'Pet insurance plans and claims',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Pet Insurance, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_travel_insurance',
    name: 'Aerynza Travel Insurance',
    category: 'travel',
    description: 'Travel insurance coverage and claims',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'travel',
    related_capabilities: [
    'ascension_public_transit',
    'ascension_rideshare',
    'ascension_flight'
  ],
    context: 'Triggers: user asks about Travel Insurance, starts a travel-domain quest, or needs a decision in this area. Cross-references: ascension_public_transit, ascension_rideshare, ascension_flight. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_gardening',
    name: 'Aerynza Gardening',
    category: 'home',
    description: 'Garden planning, planting, and care',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Gardening, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_landscaping',
    name: 'Aerynza Landscaping',
    category: 'home',
    description: 'Landscape design, plants, and maintenance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Landscaping, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_lawn_care',
    name: 'Aerynza Lawn Care',
    category: 'home',
    description: 'Lawn care, mowing, and fertilization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Lawn Care, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_composting',
    name: 'Aerynza Composting',
    category: 'home',
    description: 'Composting methods, balance, and use',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Composting, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_hydroponics',
    name: 'Aerynza Hydroponics',
    category: 'home',
    description: 'Hydroponic systems, nutrients, and crops',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Hydroponics, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_aquaponics',
    name: 'Aerynza Aquaponics',
    category: 'home',
    description: 'Aquaponics systems, fish, and plants',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Aquaponics, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fermentation',
    name: 'Aerynza Fermentation',
    category: 'home',
    description: 'Fermentation, pickles, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Fermentation, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_preserving',
    name: 'Aerynza Preserving',
    category: 'home',
    description: 'Food preservation, canning, and drying',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Preserving, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_canning',
    name: 'Aerynza Canning',
    category: 'home',
    description: 'Canning methods, safety, and storage',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Canning, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_smoking',
    name: 'Aerynza Smoking',
    category: 'cooking',
    description: 'Smoking meats, woods, and temperatures',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_bbq',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_bread_making',
    'ascension_sourdough'
  ],
    context: 'Triggers: user asks about Smoking, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_bbq, ascension_grilling, ascension_pizza, ascension_bread_making, ascension_sourdough. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_bbq',
    name: 'Aerynza BBQ',
    category: 'cooking',
    description: 'BBQ styles, rubs, and techniques',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_bread_making',
    'ascension_sourdough'
  ],
    context: 'Triggers: user asks about BBQ, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_grilling, ascension_pizza, ascension_bread_making, ascension_sourdough. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_grilling',
    name: 'Aerynza Grilling',
    category: 'cooking',
    description: 'Grilling techniques, heat, and timing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_pizza',
    'ascension_bread_making',
    'ascension_sourdough'
  ],
    context: 'Triggers: user asks about Grilling, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_pizza, ascension_bread_making, ascension_sourdough. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_pizza',
    name: 'Aerynza Pizza',
    category: 'cooking',
    description: 'Pizza dough, sauce, and oven setup',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_grilling',
    'ascension_bread_making',
    'ascension_sourdough'
  ],
    context: 'Triggers: user asks about Pizza, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_grilling, ascension_bread_making, ascension_sourdough. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_bread_making',
    name: 'Aerynza Bread Making',
    category: 'cooking',
    description: 'Bread formulas, kneading, and baking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_sourdough'
  ],
    context: 'Triggers: user asks about Bread Making, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_grilling, ascension_pizza, ascension_sourdough. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sourdough',
    name: 'Aerynza Sourdough',
    category: 'cooking',
    description: 'Sourdough starter, fermentation, and baking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_bread_making'
  ],
    context: 'Triggers: user asks about Sourdough, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_grilling, ascension_pizza, ascension_bread_making. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_meal_prep',
    name: 'Aerynza Meal Prep',
    category: 'nutrition',
    description: 'Meal prep, containers, and storage',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'nutrition',
    related_capabilities: [
    'ascension_batch_cooking',
    'ascension_freezer_meals',
    'ascension_juicing',
    'ascension_smoothies',
    'ascension_protein'
  ],
    context: 'Triggers: user asks about Meal Prep, starts a nutrition-domain quest, or needs a decision in this area. Cross-references: ascension_batch_cooking, ascension_freezer_meals, ascension_juicing, ascension_smoothies, ascension_protein. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_batch_cooking',
    name: 'Aerynza Batch Cooking',
    category: 'nutrition',
    description: 'Batch cooking plans and reheating',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'nutrition',
    related_capabilities: [
    'ascension_meal_prep',
    'ascension_freezer_meals',
    'ascension_juicing',
    'ascension_smoothies',
    'ascension_protein'
  ],
    context: 'Triggers: user asks about Batch Cooking, starts a nutrition-domain quest, or needs a decision in this area. Cross-references: ascension_meal_prep, ascension_freezer_meals, ascension_juicing, ascension_smoothies, ascension_protein. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_freezer_meals',
    name: 'Aerynza Freezer Meals',
    category: 'nutrition',
    description: 'Freezer meal recipes and storage',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'nutrition',
    related_capabilities: [
    'ascension_meal_prep',
    'ascension_batch_cooking',
    'ascension_juicing',
    'ascension_smoothies',
    'ascension_protein'
  ],
    context: 'Triggers: user asks about Freezer Meals, starts a nutrition-domain quest, or needs a decision in this area. Cross-references: ascension_meal_prep, ascension_batch_cooking, ascension_juicing, ascension_smoothies, ascension_protein. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_slow_cooker',
    name: 'Aerynza Slow Cooker',
    category: 'cooking',
    description: 'Slow cooker recipes and timing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_bread_making'
  ],
    context: 'Triggers: user asks about Slow Cooker, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_grilling, ascension_pizza, ascension_bread_making. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_pressure_cooker',
    name: 'Aerynza Pressure Cooker',
    category: 'cooking',
    description: 'Pressure cooker safety and recipes',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_bread_making'
  ],
    context: 'Triggers: user asks about Pressure Cooker, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_grilling, ascension_pizza, ascension_bread_making. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_air_fryer',
    name: 'Aerynza Air Fryer',
    category: 'cooking',
    description: 'Air fryer recipes, timing, and conversions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_bread_making'
  ],
    context: 'Triggers: user asks about Air Fryer, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_grilling, ascension_pizza, ascension_bread_making. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sous_vide',
    name: 'Aerynza Sous Vide',
    category: 'cooking',
    description: 'Sous vide temperatures, times, and searing',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_bread_making'
  ],
    context: 'Triggers: user asks about Sous Vide, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_grilling, ascension_pizza, ascension_bread_making. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_dehydrator',
    name: 'Aerynza Dehydrator',
    category: 'cooking',
    description: 'Dehydrator recipes and storage',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'cooking',
    related_capabilities: [
    'ascension_smoking',
    'ascension_bbq',
    'ascension_grilling',
    'ascension_pizza',
    'ascension_bread_making'
  ],
    context: 'Triggers: user asks about Dehydrator, starts a cooking-domain quest, or needs a decision in this area. Cross-references: ascension_smoking, ascension_bbq, ascension_grilling, ascension_pizza, ascension_bread_making. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_juicing',
    name: 'Aerynza Juicing',
    category: 'nutrition',
    description: 'Juicing recipes, produce, and cleanup',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'nutrition',
    related_capabilities: [
    'ascension_meal_prep',
    'ascension_batch_cooking',
    'ascension_freezer_meals',
    'ascension_smoothies',
    'ascension_protein'
  ],
    context: 'Triggers: user asks about Juicing, starts a nutrition-domain quest, or needs a decision in this area. Cross-references: ascension_meal_prep, ascension_batch_cooking, ascension_freezer_meals, ascension_smoothies, ascension_protein. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_smoothies',
    name: 'Aerynza Smoothies',
    category: 'nutrition',
    description: 'Smoothie blends, protein, and macros',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'nutrition',
    related_capabilities: [
    'ascension_meal_prep',
    'ascension_batch_cooking',
    'ascension_freezer_meals',
    'ascension_juicing',
    'ascension_protein'
  ],
    context: 'Triggers: user asks about Smoothies, starts a nutrition-domain quest, or needs a decision in this area. Cross-references: ascension_meal_prep, ascension_batch_cooking, ascension_freezer_meals, ascension_juicing, ascension_protein. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_protein',
    name: 'Aerynza Protein',
    category: 'nutrition',
    description: 'Protein sources, timing, and targets',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'nutrition',
    related_capabilities: [
    'ascension_meal_prep',
    'ascension_batch_cooking',
    'ascension_freezer_meals',
    'ascension_juicing',
    'ascension_smoothies'
  ],
    context: 'Triggers: user asks about Protein, starts a nutrition-domain quest, or needs a decision in this area. Cross-references: ascension_meal_prep, ascension_batch_cooking, ascension_freezer_meals, ascension_juicing, ascension_smoothies. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_supplements_stack',
    name: 'Aerynza Supplements Stack',
    category: 'nutrition',
    description: 'Supplement stacking, timing, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'nutrition',
    related_capabilities: [
    'ascension_meal_prep',
    'ascension_batch_cooking',
    'ascension_freezer_meals',
    'ascension_juicing',
    'ascension_smoothies'
  ],
    context: 'Triggers: user asks about Supplements Stack, starts a nutrition-domain quest, or needs a decision in this area. Cross-references: ascension_meal_prep, ascension_batch_cooking, ascension_freezer_meals, ascension_juicing, ascension_smoothies. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_pre_workout',
    name: 'Aerynza Pre Workout',
    category: 'fitness',
    description: 'Pre-workout nutrition, timing, and ingredients',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'fitness',
    related_capabilities: [
    'ascension_post_workout'
  ],
    context: 'Triggers: user asks about Pre Workout, starts a fitness-domain quest, or needs a decision in this area. Cross-references: ascension_post_workout. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_post_workout',
    name: 'Aerynza Post Workout',
    category: 'fitness',
    description: 'Post-workout nutrition and recovery',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'fitness',
    related_capabilities: [
    'ascension_pre_workout'
  ],
    context: 'Triggers: user asks about Post Workout, starts a fitness-domain quest, or needs a decision in this area. Cross-references: ascension_pre_workout. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_meal_planning',
    name: 'Aerynza Meal Planning',
    category: 'nutrition',
    description: 'Weekly meal plans, balance, and shopping',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'nutrition',
    related_capabilities: [
    'ascension_meal_prep',
    'ascension_batch_cooking',
    'ascension_freezer_meals',
    'ascension_juicing',
    'ascension_smoothies'
  ],
    context: 'Triggers: user asks about Meal Planning, starts a nutrition-domain quest, or needs a decision in this area. Cross-references: ascension_meal_prep, ascension_batch_cooking, ascension_freezer_meals, ascension_juicing, ascension_smoothies. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_grocery_list',
    name: 'Aerynza Grocery List',
    category: 'home',
    description: 'Grocery list creation, pantry check, and budget',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Grocery List, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_meditation_guided',
    name: 'Aerynza Meditation Guided',
    category: 'wellness',
    description: 'Guided meditation and relaxation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Meditation Guided, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_breathing',
    name: 'Aerynza Breathing',
    category: 'wellness',
    description: 'Breathing exercises and techniques',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Breathing, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cold_exposure',
    name: 'Aerynza Cold Exposure',
    category: 'wellness',
    description: 'Cold exposure, showers, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Cold Exposure, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_heat_exposure',
    name: 'Aerynza Heat Exposure',
    category: 'wellness',
    description: 'Sauna, hot bath, and heat safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Heat Exposure, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sauna',
    name: 'Aerynza Sauna',
    category: 'wellness',
    description: 'Sauna protocols, hydration, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Sauna, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_ice_bath',
    name: 'Aerynza Ice Bath',
    category: 'wellness',
    description: 'Ice bath setup, duration, and safety',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Ice Bath, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sleep_hygiene',
    name: 'Aerynza Sleep Hygiene',
    category: 'wellness',
    description: 'Sleep routines, environment, and habits',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Sleep Hygiene, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_nap',
    name: 'Aerynza Nap',
    category: 'wellness',
    description: 'Nap length, timing, and recovery',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Nap, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_circadian',
    name: 'Aerynza Circadian',
    category: 'wellness',
    description: 'Circadian rhythm, light, and schedule',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Circadian, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_journaling',
    name: 'Aerynza Journaling',
    category: 'wellness',
    description: 'Journaling prompts, habits, and review',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Journaling, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_gratitude',
    name: 'Aerynza Gratitude',
    category: 'wellness',
    description: 'Gratitude practice and reflection',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Gratitude, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_affirmations',
    name: 'Aerynza Affirmations',
    category: 'wellness',
    description: 'Affirmations, wording, and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Affirmations, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_visualization',
    name: 'Aerynza Visualization',
    category: 'wellness',
    description: 'Visualization techniques and mental rehearsal',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Visualization, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mindset',
    name: 'Aerynza Mindset',
    category: 'wellness',
    description: 'Mindset coaching and reframes',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Mindset, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_resilience',
    name: 'Aerynza Resilience',
    category: 'wellness',
    description: 'Resilience building and stress recovery',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Resilience, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_growth_mindset',
    name: 'Aerynza Growth Mindset',
    category: 'wellness',
    description: 'Growth mindset and learning attitude',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Growth Mindset, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_stoicism',
    name: 'Aerynza Stoicism',
    category: 'wellness',
    description: 'Stoic principles and daily practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Stoicism, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_buddhism',
    name: 'Aerynza Buddhism',
    category: 'spirituality',
    description: 'Buddhist concepts, practice, and meditation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_hinduism',
    'ascension_christianity'
  ],
    context: 'Triggers: user asks about Buddhism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_hinduism, ascension_christianity. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_hinduism',
    name: 'Aerynza Hinduism',
    category: 'spirituality',
    description: 'Hindu philosophy, texts, and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_christianity'
  ],
    context: 'Triggers: user asks about Hinduism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_christianity. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_christianity',
    name: 'Aerynza Christianity',
    category: 'spirituality',
    description: 'Christian beliefs, practice, and study',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Christianity, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_islam',
    name: 'Aerynza Islam',
    category: 'spirituality',
    description: 'Islamic beliefs, practice, and study',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Islam, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_judaism',
    name: 'Aerynza Judaism',
    category: 'spirituality',
    description: 'Jewish beliefs, practice, and study',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Judaism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_taoism',
    name: 'Aerynza Taoism',
    category: 'spirituality',
    description: 'Taoist philosophy and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Taoism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_confucianism',
    name: 'Aerynza Confucianism',
    category: 'spirituality',
    description: 'Confucian values and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Confucianism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_shinto',
    name: 'Aerynza Shinto',
    category: 'spirituality',
    description: 'Shinto practice, kami, and shrines',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Shinto, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_sikhism',
    name: 'Aerynza Sikhism',
    category: 'spirituality',
    description: 'Sikh beliefs, practice, and study',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Sikhism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_jainism',
    name: 'Aerynza Jainism',
    category: 'spirituality',
    description: 'Jain beliefs and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Jainism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_bahai',
    name: 'Aerynza Baha i',
    category: 'spirituality',
    description: 'Baha i principles and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Baha i, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_paganism',
    name: 'Aerynza Paganism',
    category: 'spirituality',
    description: 'Pagan paths, seasons, and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Paganism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_wicca',
    name: 'Aerynza Wicca',
    category: 'spirituality',
    description: 'Wiccan practice, sabbats, and ethics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Wicca, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_druidry',
    name: 'Aerynza Druidry',
    category: 'spirituality',
    description: 'Druidry, nature, and ritual',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Druidry, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_native_spirituality',
    name: 'Aerynza Native Spirituality',
    category: 'spirituality',
    description: 'Indigenous spiritual practices and respect',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Native Spirituality, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_shamanism',
    name: 'Aerynza Shamanism',
    category: 'spirituality',
    description: 'Shamanic journeying and practice',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spirituality',
    related_capabilities: [
    'ascension_spirituality',
    'ascension_mindfulness',
    'ascension_meditation',
    'ascension_buddhism',
    'ascension_hinduism'
  ],
    context: 'Triggers: user asks about Shamanism, starts a spirituality-domain quest, or needs a decision in this area. Cross-references: ascension_spirituality, ascension_mindfulness, ascension_meditation, ascension_buddhism, ascension_hinduism. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_logic',
    name: 'Aerynza Logic',
    category: 'knowledge',
    description: 'Logic, reasoning, and fallacies',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Logic, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_critical_thinking',
    name: 'Aerynza Critical Thinking',
    category: 'knowledge',
    description: 'Critical thinking and evaluation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Critical Thinking, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_argumentation',
    name: 'Aerynza Argumentation',
    category: 'knowledge',
    description: 'Argument structure and evidence',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Argumentation, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fallacies',
    name: 'Aerynza Fallacies',
    category: 'knowledge',
    description: 'Logical fallacies and spotting them',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Fallacies, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_debate',
    name: 'Aerynza Debate',
    category: 'knowledge',
    description: 'Debate formats, prep, and rebuttal',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Debate, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_persuasion',
    name: 'Aerynza Persuasion',
    category: 'knowledge',
    description: 'Persuasion principles and ethics',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Persuasion, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_rapport',
    name: 'Aerynza Rapport',
    category: 'relationships',
    description: 'Building rapport and trust',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_empathy',
    'ascension_charisma'
  ],
    context: 'Triggers: user asks about Rapport, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_empathy, ascension_charisma. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_empathy',
    name: 'Aerynza Empathy',
    category: 'relationships',
    description: 'Empathy, listening, and response',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_charisma'
  ],
    context: 'Triggers: user asks about Empathy, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_charisma. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_charisma',
    name: 'Aerynza Charisma',
    category: 'relationships',
    description: 'Charisma, presence, and influence',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy'
  ],
    context: 'Triggers: user asks about Charisma, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_empathy. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_confidence_building',
    name: 'Aerynza Confidence Building',
    category: 'wellness',
    description: 'Confidence building and self-efficacy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Confidence Building, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_assertiveness',
    name: 'Aerynza Assertiveness',
    category: 'relationships',
    description: 'Assertive communication and boundaries',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy'
  ],
    context: 'Triggers: user asks about Assertiveness, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_empathy. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_boundaries',
    name: 'Aerynza Boundaries',
    category: 'relationships',
    description: 'Personal boundaries and maintenance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy'
  ],
    context: 'Triggers: user asks about Boundaries, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_empathy. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_conflict_resolution',
    name: 'Aerynza Conflict Resolution',
    category: 'relationships',
    description: 'Conflict resolution and mediation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy'
  ],
    context: 'Triggers: user asks about Conflict Resolution, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_empathy. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_active_listening',
    name: 'Aerynza Active Listening',
    category: 'relationships',
    description: 'Active listening and reflective response',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy'
  ],
    context: 'Triggers: user asks about Active Listening, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_empathy. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_wallet_automation',
    name: 'Aerynza Wallet Automation',
    category: 'finance',
    description: 'Connect a wallet and run automated financial strategies',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Wallet Automation, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_fast_turn',
    name: 'Aerynza Fast Turn',
    category: 'finance',
    description: 'Fast capital multiplication strategies with explicit risk warnings',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Fast Turn, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_income_split',
    name: 'Aerynza Income Split',
    category: 'finance',
    description: 'Split direct deposits into spending, savings, bills, quick investment, long-term investment, and dream board buckets',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Income Split, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_inventor_lab',
    name: 'Aerynza Inventor Lab',
    category: 'creation',
    description: 'Co-inventor and lab partner for product design, prototyping, and experiments',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Inventor Lab, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_hardware_prototyping',
    name: 'Aerynza Hardware Prototyping',
    category: 'creation',
    description: 'Step-by-step hardware build plans, materials, models, and cost-efficient methods',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Hardware Prototyping, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_youtube_automation',
    name: 'Aerynza YouTube Automation',
    category: 'creation',
    description: 'Build and automate a YouTube channel including uploads, SEO, and monetization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about YouTube Automation, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tiktok_automation',
    name: 'Aerynza TikTok Automation',
    category: 'creation',
    description: 'Build and automate a TikTok account including uploads, trends, and monetization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about TikTok Automation, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_amsr_studio',
    name: 'Aerynza AMSR Studio',
    category: 'creation',
    description: 'Create and automate AMSR content, videos, and channel growth',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about AMSR Studio, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_affiliate_automation',
    name: 'Aerynza Affiliate Automation',
    category: 'business',
    description: 'Automate affiliate program discovery, application, and revenue tracking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Affiliate Automation, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_streaming_channel',
    name: 'Aerynza Streaming Channel',
    category: 'creation',
    description: 'Build a live streaming channel, schedule, overlays, and audience growth',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Streaming Channel, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_streaming_moderator',
    name: 'Aerynza Streaming Moderator',
    category: 'creation',
    description: 'Live moderation, chat engagement, and safety for streaming sessions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Streaming Moderator, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_overlay_design',
    name: 'Aerynza Overlay Design',
    category: 'creation',
    description: 'Design cool overlays, alerts, and scenes for live streams',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Overlay Design, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_research_assistant',
    name: 'Aerynza Research Assistant',
    category: 'knowledge',
    description: 'Best research and design assistant on the planet for facts, patents, and experiments',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Research Assistant, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_design_assistant',
    name: 'Aerynza Design Assistant',
    category: 'creation',
    description: 'Best design assistant for products, experiences, and interfaces',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Design Assistant, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_crowdfunding_product',
    name: 'Aerynza Crowdfunding Product',
    category: 'business',
    description: 'Plan and run crowdfunding campaigns for inventions and products',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Crowdfunding Product, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_dream_fund',
    name: 'Aerynza Dream Fund',
    category: 'finance',
    description: 'Track aspirations and dream board goals with automated savings and milestone planning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Dream Fund, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_content_workspace',
    name: 'Aerynza Content Workspace',
    category: 'business',
    description: 'Create and organize workspaces for content projects, channels, and campaigns',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Content Workspace, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_content_analytics',
    name: 'Aerynza Content Analytics',
    category: 'business',
    description: 'Wire analytics for content, streams, and social accounts to track performance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Content Analytics, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_growth_tracker',
    name: 'Aerynza Growth Tracker',
    category: 'business',
    description: 'Track followers, views, subscribers, and growth metrics across platforms',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Growth Tracker, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_revenue_tracker',
    name: 'Aerynza Revenue Tracker',
    category: 'finance',
    description: 'Track ad, affiliate, sponsorship, and product revenue from content and streams',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Revenue Tracker, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_content_calendar',
    name: 'Aerynza Content Calendar',
    category: 'business',
    description: 'Plan and schedule content releases, streams, and campaigns across platforms',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Content Calendar, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_solution_engine',
    name: 'Aerynza Solution Engine',
    category: 'knowledge',
    description: 'Invent custom solutions for any goal with constraints, permissions, and a build path',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Solution Engine, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_invention_engine',
    name: 'Aerynza Invention Engine',
    category: 'creation',
    description: 'Invent products, services, and experiences from scratch with materials, cost, and steps',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Invention Engine, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_video_types',
    name: 'Aerynza Video Types',
    category: 'creation',
    description: 'Recommend the right video formats for any channel, niche, and monetization goal',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Video Types, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_channel_types',
    name: 'Aerynza Channel Types',
    category: 'business',
    description: 'Recommend channel types and services for any audience, income, and cash situation',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Channel Types, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cash_strategy',
    name: 'Aerynza Cash Strategy',
    category: 'finance',
    description: 'Invent cash solutions for any budget, timeline, and risk level',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Cash Strategy, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_zero_capital',
    name: 'Aerynza Zero Capital',
    category: 'finance',
    description: 'Build income and solutions when starting with no money',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Zero Capital, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_micro_launch',
    name: 'Aerynza Micro Launch',
    category: 'business',
    description: 'Launch a product, channel, or service with a tiny budget and fast feedback loop',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Micro Launch, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_service_designer',
    name: 'Aerynza Service Designer',
    category: 'business',
    description: 'Design a service offering, pricing, and delivery path for any skill or audience',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Service Designer, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_idea_validator',
    name: 'Aerynza Idea Validator',
    category: 'knowledge',
    description: 'Quickly validate an idea, market, and first move before building',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Idea Validator, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_build_path',
    name: 'Aerynza Build Path',
    category: 'creation',
    description: 'Generate a step-by-step build path for any invention, project, or channel',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Build Path, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_compound_engine',
    name: 'Aerynza Compound Engine',
    category: 'finance',
    description: 'Build a reinvestment and compounding plan for any small starting amount and time horizon with explicit risk warnings',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Compound Engine, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_72h_sprint',
    name: 'Aerynza 72h Sprint',
    category: 'finance',
    description: 'Design a high-activity 72-hour income or growth sprint with realistic targets and legal methods',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about 72h Sprint, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_risk_budget',
    name: 'Aerynza Risk Budget',
    category: 'finance',
    description: 'Set a risk budget for fast-turn experiments so survival money is never at risk',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Risk Budget, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_gig_sprint',
    name: 'Aerynza Gig Sprint',
    category: 'finance',
    description: 'Map the fastest gig and task income for a small amount in a short window',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Gig Sprint, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_money_flip',
    name: 'Aerynza Money Flip',
    category: 'finance',
    description: 'Plug in any amount and get a custom flip plan with realistic target, timeline, and risk warning',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Money Flip, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_second_brain',
    name: 'Aerynza Second Brain',
    category: 'intelligence',
    description: 'Personal knowledge engine that captures, connects, and retrieves everything the user shares',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_life_orchestrator',
    'ascension_user_profile'
  ],
    context: 'Triggers: user asks about Second Brain, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_life_orchestrator, ascension_user_profile. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_life_orchestrator',
    name: 'Aerynza Life Orchestrator',
    category: 'intelligence',
    description: 'Coordinate the full stack of life domains: work, family, health, home, finance, and creativity',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_user_profile'
  ],
    context: 'Triggers: user asks about Life Orchestrator, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_user_profile. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_user_profile',
    name: 'Aerynza User Profile',
    category: 'intelligence',
    description: 'Maintain a living profile of the user: goals, skills, schedule, people, and preferences',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about User Profile, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_family_profile',
    name: 'Aerynza Family Profile',
    category: 'intelligence',
    description: 'Maintain a living profile of the household and extended family with permission boundaries',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'family',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Family Profile, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_context_engine',
    name: 'Aerynza Context Engine',
    category: 'intelligence',
    description: 'Share permissioned context across AP, Nexus, HomeOS, and Sprout shells',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Context Engine, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_shell_orchestrator',
    name: 'Aerynza Shell Orchestrator',
    category: 'intelligence',
    description: 'Route tasks and insights between AP, Nexus, HomeOS, Sprout, and product shells',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Shell Orchestrator, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_knowledge_graph',
    name: 'Aerynza Knowledge Graph',
    category: 'intelligence',
    description: 'Connect people, places, projects, goals, and events into a queryable knowledge graph',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Knowledge Graph, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_proactive_engine',
    name: 'Aerynza Proactive Engine',
    category: 'intelligence',
    description: 'Surface reminders, opportunities, and next steps before the user asks',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Proactive Engine, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_appointments',
    name: 'Aerynza Appointments',
    category: 'home',
    description: 'Track, schedule, and prepare for appointments across health, work, family, and services',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Appointments, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_maintenance',
    name: 'Aerynza Maintenance',
    category: 'home',
    description: 'Track home, vehicle, health, and device maintenance schedules with reminders',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Maintenance, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_family_sync',
    name: 'Aerynza Family Sync',
    category: 'family',
    description: 'Sync schedules, tasks, and updates across household and extended family members',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'family',
    executor: 'family',
    related_capabilities: [
    'ascension_family',
    'ascension_family_abroad',
    'ascension_child_development'
  ],
    context: 'Triggers: user asks about Family Sync, starts a family-domain quest, or needs a decision in this area. Cross-references: ascension_family, ascension_family_abroad, ascension_child_development. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_family_abroad',
    name: 'Aerynza Family Abroad',
    category: 'family',
    description: 'Support coordination, calls, gifts, visits, and updates for family living abroad',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'family',
    executor: 'family',
    related_capabilities: [
    'ascension_family',
    'ascension_family_sync',
    'ascension_child_development'
  ],
    context: 'Triggers: user asks about Family Abroad, starts a family-domain quest, or needs a decision in this area. Cross-references: ascension_family, ascension_family_sync, ascension_child_development. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_household_sync',
    name: 'Aerynza Household Sync',
    category: 'home',
    description: 'Sync chores, shopping, meals, and routines across the household',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Household Sync, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_life_admin',
    name: 'Aerynza Life Admin',
    category: 'home',
    description: 'Manage paperwork, renewals, deadlines, and bureaucratic tasks for the user and family',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Life Admin, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_creative_manager',
    name: 'Aerynza Creative Manager',
    category: 'creation',
    description: 'Track projects, ideas, assets, and releases across all creative pursuits',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Creative Manager, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_business_manager',
    name: 'Aerynza Business Manager',
    category: 'business',
    description: 'Track leads, revenue, tasks, and operations across businesses and side projects',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'business',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Business Manager, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_child_development',
    name: 'Aerynza Child Development',
    category: 'family',
    description: 'Track developmental milestones, learning, and activities for each child',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'family',
    executor: 'family',
    related_capabilities: [
    'ascension_family',
    'ascension_family_sync',
    'ascension_family_abroad'
  ],
    context: 'Triggers: user asks about Child Development, starts a family-domain quest, or needs a decision in this area. Cross-references: ascension_family, ascension_family_sync, ascension_family_abroad. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_goals',
    name: 'Aerynza Goals',
    category: 'wellness',
    description: 'Set, track, and break down goals across every life domain with milestones and reviews',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Goals, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_milestones',
    name: 'Aerynza Milestones',
    category: 'wellness',
    description: 'Track milestones, celebrations, and progress across personal and family life',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Milestones, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_routine',
    name: 'Aerynza Routine',
    category: 'home',
    description: 'Design, sync, and adapt daily, weekly, and seasonal routines for the user and household',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'home',
    related_capabilities: [
    'ascension_home',
    'ascension_travel',
    'ascension_realestate',
    'ascension_events',
    'ascension_automotive'
  ],
    context: 'Triggers: user asks about Routine, starts a home-domain quest, or needs a decision in this area. Cross-references: ascension_home, ascension_travel, ascension_realestate, ascension_events, ascension_automotive. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_human_intelligence',
    name: 'Aerynza Human Intelligence',
    category: 'intelligence',
    description: 'Understand the human completely: identity, emotion, life flow, biometric, voice, behavior',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Human Intelligence, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_behavioral_intelligence',
    name: 'Aerynza Behavioral Intelligence',
    category: 'intelligence',
    description: 'Model procrastination, consistency, risk tolerance, follow-through, and motivation patterns',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Behavioral Intelligence, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_astrology_intelligence',
    name: 'Aerynza Astrology Intelligence',
    category: 'intelligence',
    description: 'Symbolic astrological context as a supplement, never a deterministic prediction',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Astrology Intelligence, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_identity',
    name: 'Aerynza Identity',
    category: 'intelligence',
    description: 'Track and evolve the user',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Identity, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_life_flow',
    name: 'Aerynza Life Flow',
    category: 'intelligence',
    description: 'Model energy, schedule, recovery, and optimal execution windows',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Life Flow, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_biometric',
    name: 'Aerynza Biometric',
    category: 'intelligence',
    description: 'Read and act on HRV, sleep, recovery, and wearable signals',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Biometric, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_voice_intelligence',
    name: 'Aerynza Voice Intelligence',
    category: 'intelligence',
    description: 'Voice-based interaction, tone, and voiceprint identity signals',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Voice Intelligence, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_personality',
    name: 'Aerynza Personality',
    category: 'intelligence',
    description: 'Track personality layers, preferences, and decision style',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Personality, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_resource_intelligence',
    name: 'Aerynza Resource Intelligence',
    category: 'intelligence',
    description: 'Manage all resources: money, time, energy, skills, assets, credit, investments',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Resource Intelligence, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_global_economics',
    name: 'Aerynza Global Economics',
    category: 'finance',
    description: 'Track macro signals: inflation, rates, employment, commodities, government incentives',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Global Economics, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_assets',
    name: 'Aerynza Assets',
    category: 'finance',
    description: 'Track real estate, vehicles, collectibles, and illiquid assets',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Assets, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_opportunity_finance',
    name: 'Aerynza Opportunity Finance',
    category: 'finance',
    description: 'Find grants, scholarships, tax credits, refinancing, and rebates',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Opportunity Finance, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_world_intelligence',
    name: 'Aerynza World Intelligence',
    category: 'knowledge',
    description: 'Understand the external world: environment, markets, government, science, tech',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about World Intelligence, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_environmental',
    name: 'Aerynza Environmental',
    category: 'knowledge',
    description: 'Track environmental, weather, pollen, AQI, and climate factors',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Environmental, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_government',
    name: 'Aerynza Government',
    category: 'knowledge',
    description: 'Track government programs, policy, and regulatory impact',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Government, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_politics',
    name: 'Aerynza Politics',
    category: 'knowledge',
    description: 'Track political context and civic opportunities',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Politics, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_relationship_intelligence',
    name: 'Aerynza Relationship Intelligence',
    category: 'relationships',
    description: 'Synthesize relationships, network, community, mentors, and influence',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy'
  ],
    context: 'Triggers: user asks about Relationship Intelligence, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_empathy. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_network_vortex',
    name: 'Aerynza Network Vortex',
    category: 'relationships',
    description: 'Maintain the people graph: relationships, organizations, and community',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy'
  ],
    context: 'Triggers: user asks about Network Vortex, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_empathy. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_community',
    name: 'Aerynza Community',
    category: 'relationships',
    description: 'Track communities, groups, and local/global causes',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'relationships',
    related_capabilities: [
    'ascension_relationships',
    'ascension_dating',
    'ascension_social',
    'ascension_rapport',
    'ascension_empathy'
  ],
    context: 'Triggers: user asks about Community, starts a relationships-domain quest, or needs a decision in this area. Cross-references: ascension_relationships, ascension_dating, ascension_social, ascension_rapport, ascension_empathy. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_professional_network',
    name: 'Aerynza Professional Network',
    category: 'career',
    description: 'Track mentors, recruiters, collaborators, and career relationships',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'career',
    related_capabilities: [
    'ascension_career',
    'ascension_mentors',
    'ascension_linkedin_intelligence'
  ],
    context: 'Triggers: user asks about Professional Network, starts a career-domain quest, or needs a decision in this area. Cross-references: ascension_career, ascension_mentors, ascension_linkedin_intelligence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_mentors',
    name: 'Aerynza Mentors',
    category: 'career',
    description: 'Track mentors, coaches, advisors, and guidance relationships',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'career',
    related_capabilities: [
    'ascension_career',
    'ascension_professional_network',
    'ascension_linkedin_intelligence'
  ],
    context: 'Triggers: user asks about Mentors, starts a career-domain quest, or needs a decision in this area. Cross-references: ascension_career, ascension_professional_network, ascension_linkedin_intelligence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_influence',
    name: 'Aerynza Influence',
    category: 'business',
    description: 'Track thought leadership, audience, and influence growth',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Influence, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_creation_intelligence',
    name: 'Aerynza Creation Intelligence',
    category: 'creation',
    description: 'Accelerate creation across business, media, product, software, knowledge, and creative studios',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Creation Intelligence, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_business_studio',
    name: 'Aerynza Business Studio',
    category: 'business',
    description: 'Think like a founder: model, revenue, CAC, retention, operations, funding',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Business Studio, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_media_studio',
    name: 'Aerynza Media Studio',
    category: 'creation',
    description: 'Think like a publisher: consistency, audience, engagement, monetization',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Media Studio, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_product_studio',
    name: 'Aerynza Product Studio',
    category: 'creation',
    description: 'Think like an industrial designer and manufacturing advisor',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Product Studio, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_software_studio',
    name: 'Aerynza Software Studio',
    category: 'creation',
    description: 'Think like a software architect: architecture, tech debt, testing, deployment, security',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Software Studio, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_knowledge_studio',
    name: 'Aerynza Knowledge Studio',
    category: 'knowledge',
    description: 'Think like an educator, researcher, and author',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Knowledge Studio, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_creative_studio',
    name: 'Aerynza Creative Studio',
    category: 'creation',
    description: 'Think like an art director, creative coach, and portfolio strategist',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Creative Studio, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_creation_auditor',
    name: 'Aerynza Creation Auditor',
    category: 'creation',
    description: 'Continuous health audit for any project or studio',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Creation Auditor, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_roadmap_engine',
    name: 'Aerynza Roadmap Engine',
    category: 'creation',
    description: 'Build and track project roadmaps, milestones, and dependencies',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Roadmap Engine, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_scorecards',
    name: 'Aerynza Scorecards',
    category: 'business',
    description: 'Idea maturity, execution momentum, validation, launch, and risk scorecards',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'business',
    related_capabilities: [
    'business_growth',
    'ascension_startup',
    'ascension_business_plan',
    'ascension_marketing',
    'ascension_sales'
  ],
    context: 'Triggers: user asks about Scorecards, starts a business-domain quest, or needs a decision in this area. Cross-references: business_growth, ascension_startup, ascension_business_plan, ascension_marketing, ascension_sales. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_creation_transformation',
    name: 'Aerynza Creation Transformation',
    category: 'creation',
    description: 'Dream-to-reality transformation loop: observe, design, build, launch, scale',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about Creation Transformation, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_opportunity_intelligence',
    name: 'Aerynza Opportunity Intelligence',
    category: 'intelligence',
    description: 'Synthesize all engines to find and prioritize opportunities',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Opportunity Intelligence, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_decision_physics',
    name: 'Aerynza Decision Physics',
    category: 'intelligence',
    description: 'Observe, predict, simulate, decide, explain, and learn from outcomes',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Decision Physics, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_adaptive_quest',
    name: 'Aerynza Adaptive Quest',
    category: 'intelligence',
    description: 'Calibrate quest difficulty and selection based on tri-baseline, life flow, and behavior',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Adaptive Quest, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_cie',
    name: 'Aerynza CIE',
    category: 'intelligence',
    description: 'Conversation Intelligence Engine: score and gate all proactive AP messages',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about CIE, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_age',
    name: 'Aerynza AGE',
    category: 'intelligence',
    description: 'Aerynza Guide Engine: onboarding, feature unlocking, and readiness scoring',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about AGE, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_personal_vortex',
    name: 'Aerynza Personal Vortex',
    category: 'intelligence',
    description: 'Everything about the user: identity, goals, behavior, history, preferences',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Personal Vortex, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_world_vortex',
    name: 'Aerynza World Vortex',
    category: 'intelligence',
    description: 'Everything external: markets, science, tech, politics, weather, news',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about World Vortex, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_unified_vortex',
    name: 'Aerynza Unified Vortex',
    category: 'intelligence',
    description: 'Synthesize Personal, World, and Network Vortex into composite insights',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Unified Vortex, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_vortex_signals',
    name: 'Aerynza Vortex Signals',
    category: 'intelligence',
    description: 'Store and reason over signals from every engine and connected API',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Vortex Signals, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_calendar_intelligence',
    name: 'Aerynza Calendar Intelligence',
    category: 'productivity',
    description: 'Infer productivity windows, meeting density, key relationships, and burnout from calendar',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'productivity',
    related_capabilities: [
    'ascension_meetings',
    'ascension_time',
    'ascension_focus',
    'ascension_email_intelligence'
  ],
    context: 'Triggers: user asks about Calendar Intelligence, starts a productivity-domain quest, or needs a decision in this area. Cross-references: ascension_meetings, ascension_time, ascension_focus, ascension_email_intelligence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_email_intelligence',
    name: 'Aerynza Email Intelligence',
    category: 'productivity',
    description: 'Infer communication network, opportunity signals, and subscription creep from email',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'productivity',
    related_capabilities: [
    'ascension_meetings',
    'ascension_time',
    'ascension_focus',
    'ascension_calendar_intelligence'
  ],
    context: 'Triggers: user asks about Email Intelligence, starts a productivity-domain quest, or needs a decision in this area. Cross-references: ascension_meetings, ascension_time, ascension_focus, ascension_calendar_intelligence. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_plaid_intelligence',
    name: 'Aerynza Plaid Intelligence',
    category: 'finance',
    description: 'Infer financial behavior, stress spending, and cash flow patterns from Plaid',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Plaid Intelligence, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_investment_intelligence',
    name: 'Aerynza Investment Intelligence',
    category: 'finance',
    description: 'Infer risk, diversification, contribution discipline, and retirement readiness',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Investment Intelligence, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_crypto_intelligence',
    name: 'Aerynza Crypto Intelligence',
    category: 'finance',
    description: 'Track wallets, exchanges, staking, DeFi, and tax events',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'finance',
    related_capabilities: [
    'ascension_finance',
    'ascension_trading',
    'ascension_investing',
    'ascension_taxes',
    'ascension_insurance'
  ],
    context: 'Triggers: user asks about Crypto Intelligence, starts a finance-domain quest, or needs a decision in this area. Cross-references: ascension_finance, ascension_trading, ascension_investing, ascension_taxes, ascension_insurance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_health_intelligence',
    name: 'Aerynza Health Intelligence',
    category: 'wellness',
    description: 'Read HRV, sleep, recovery, and burnout signals from wearables',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Health Intelligence, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_location_intelligence',
    name: 'Aerynza Location Intelligence',
    category: 'knowledge',
    description: 'Infer routines, gym attendance, nature exposure, and home-away ratio',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Location Intelligence, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_spotify_intelligence',
    name: 'Aerynza Spotify Intelligence',
    category: 'wellness',
    description: 'Infer mood, energy, work style, and stress management from music',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Spotify Intelligence, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_linkedin_intelligence',
    name: 'Aerynza LinkedIn Intelligence',
    category: 'career',
    description: 'Infer career velocity, recruiter activity, and professional influence',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'career',
    related_capabilities: [
    'ascension_career',
    'ascension_professional_network',
    'ascension_mentors'
  ],
    context: 'Triggers: user asks about LinkedIn Intelligence, starts a career-domain quest, or needs a decision in this area. Cross-references: ascension_career, ascension_professional_network, ascension_mentors. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_youtube_intelligence',
    name: 'Aerynza YouTube Intelligence',
    category: 'knowledge',
    description: 'Infer learning investment, topic depth, and research patterns',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about YouTube Intelligence, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_tiktok_intelligence',
    name: 'Aerynza TikTok Intelligence',
    category: 'creation',
    description: 'Infer creator momentum, content discipline, and trend awareness',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about TikTok Intelligence, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_github_intelligence',
    name: 'Aerynza GitHub Intelligence',
    category: 'creation',
    description: 'Infer coding consistency, technical growth, and architecture maturity',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'creation',
    related_capabilities: [
    'ascension_creative',
    'ascension_music',
    'ascension_art',
    'ascension_writing',
    'ascension_dance'
  ],
    context: 'Triggers: user asks about GitHub Intelligence, starts a creation-domain quest, or needs a decision in this area. Cross-references: ascension_creative, ascension_music, ascension_art, ascension_writing, ascension_dance. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_weather_intelligence',
    name: 'Aerynza Weather Intelligence',
    category: 'knowledge',
    description: 'Infer mood/energy correlation and activity suitability from weather',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Weather Intelligence, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_news_intelligence',
    name: 'Aerynza News Intelligence',
    category: 'knowledge',
    description: 'Infer industry opportunity, economic context, and regulatory impact',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about News Intelligence, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_question_engine',
    name: 'Aerynza Question Engine',
    category: 'intelligence',
    description: 'Ask one question at a time, track state, and adapt follow-ups',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Question Engine, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_vault',
    name: 'Aerynza Vault',
    category: 'intelligence',
    description: 'Permanent digital estate: AP can read, never write or delete',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Vault, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_living_memory',
    name: 'Aerynza Living Memory',
    category: 'intelligence',
    description: 'Active cognition: current goals, patterns, and recent interactions',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Living Memory, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_living_context',
    name: 'Aerynza Living Context',
    category: 'intelligence',
    description: 'Weekly pre-computed working memory snapshot for fast AP responses',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Living Context, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_proactivity',
    name: 'Aerynza Proactivity',
    category: 'intelligence',
    description: 'Configure silent to always-on reaction levels',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Proactivity, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_workout',
    name: 'Aerynza Workout',
    category: 'wellness',
    description: 'Plan and adapt exercise routines and physical training',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Workout, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_body_profile',
    name: 'Aerynza Body Profile',
    category: 'wellness',
    description: 'Track body data, photos, weight, BMR, and TDEE',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'wellness',
    related_capabilities: [
    'ascension_yoga',
    'ascension_running',
    'ascension_swimming',
    'ascension_cycling',
    'ascension_hiking'
  ],
    context: 'Triggers: user asks about Body Profile, starts a wellness-domain quest, or needs a decision in this area. Cross-references: ascension_yoga, ascension_running, ascension_swimming, ascension_cycling, ascension_hiking. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_document_intelligence',
    name: 'Aerynza Document Intelligence',
    category: 'knowledge',
    description: 'OCR, classify, extract, and persist structured data from uploaded documents',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'knowledge',
    related_capabilities: [
    'ascension_philosophy',
    'ascension_history',
    'ascension_science',
    'ascension_math',
    'ascension_language'
  ],
    context: 'Triggers: user asks about Document Intelligence, starts a knowledge-domain quest, or needs a decision in this area. Cross-references: ascension_philosophy, ascension_history, ascension_science, ascension_math, ascension_language. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_legacy',
    name: 'Aerynza Legacy',
    category: 'intelligence',
    description: 'Plan contribution, generational impact, and long-term life legacy',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Legacy, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ascension_contribution',
    name: 'Aerynza Contribution',
    category: 'intelligence',
    description: 'Track giving, mentorship, community impact, and contribution goals',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'intelligence',
    related_capabilities: [
    'intelligence_sweep',
    'context_memory',
    'proactive_intelligence',
    'ascension_second_brain',
    'ascension_life_orchestrator'
  ],
    context: 'Triggers: user asks about Contribution, starts a intelligence-domain quest, or needs a decision in this area. Cross-references: intelligence_sweep, context_memory, proactive_intelligence, ascension_second_brain, ascension_life_orchestrator. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'phone_os',
    promoted: false,
    name: 'Phone OS',
    category: 'engineering',
    description: 'Design, scaffold, and build a custom mobile operating system for ARM or x86 phone hardware',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'phone_drivers',
      'phone_flash',
      'phone_recovery',
      'ascension_build_path',
      'ascension_solution_engine',
      'ascension_invention_engine',
      'ascension_second_brain'
    ],
    context: 'Triggers: user asks about building a phone OS, replacing Android/iOS, or creating a custom mobile operating system. Cross-references: phone_drivers, phone_flash, phone_recovery, ascension_build_path, ascension_solution_engine, ascension_invention_engine, ascension_second_brain. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'phone_drivers',
    promoted: false,
    name: 'Phone Driver Layer',
    category: 'engineering',
    description: 'Generate, wire, and validate USB, fastboot, ADB, display, touch, radio, and SoC drivers for a phone OS',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'phone_os',
      'phone_flash',
      'phone_recovery',
      'ascension_build_path',
      'ascension_code_generator',
      'ascension_hardware_interface'
    ],
    context: 'Triggers: user needs phone drivers, USB stack, touch/screen drivers, radio drivers, or SoC support. Cross-references: phone_os, phone_flash, phone_recovery, ascension_build_path, ascension_code_generator, ascension_hardware_interface. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'phone_flash',
    promoted: false,
    name: 'Phone Flash',
    category: 'engineering',
    description: 'Prepare a flashable OS image, verify compatibility, and flash it to a phone connected over USB',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'phone_os',
      'phone_drivers',
      'phone_recovery',
      'ascension_build_path',
      'ascension_device_control',
      'ascension_risk_budget'
    ],
    context: 'Triggers: user asks to flash an OS to a phone over USB, rewrite phone firmware, or install a custom ROM. Cross-references: phone_os, phone_drivers, phone_recovery, ascension_build_path, ascension_device_control, ascension_risk_budget. Requires explicit device.flash permission and a receipt before writing anything to the device.'
  },
  {
    id: 'phone_recovery',
    promoted: false,
    name: 'Phone Recovery',
    category: 'engineering',
    description: 'Design recovery, bootloader, and fail-safe images for phone OS updates and brick recovery',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'phone_os',
      'phone_drivers',
      'phone_flash',
      'ascension_build_path',
      'ascension_experiment_design',
      'ascension_risk_budget'
    ],
    context: 'Triggers: user asks about recovery mode, bootloader, brick recovery, or safe images for phone OS. Cross-references: phone_os, phone_drivers, phone_flash, ascension_build_path, ascension_experiment_design, ascension_risk_budget. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'universal_os',
    promoted: false,
    name: 'Universal OS',
    category: 'engineering',
    description: 'Design a unified operating system that can target phones, laptops, desktops, and smart devices from one code base',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'phone_os',
      'laptop_os',
      'desktop_os',
      'smart_device_os',
      'device_drivers',
      'device_flash',
      'ip_guard'
    ],
    context: 'Triggers: user asks about a universal OS, one OS for every device, or building an operating system for laptops, desktops, phones, and smart devices. Cross-references: phone_os, laptop_os, desktop_os, smart_device_os, device_drivers, device_flash, ip_guard. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'laptop_os',
    promoted: false,
    name: 'Laptop OS',
    category: 'engineering',
    description: 'Port or build the universal OS for laptop form factors: x86/ARM64, power management, keyboard, trackpad, display, and docking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'universal_os',
      'device_drivers',
      'device_flash',
      'ip_guard'
    ],
    context: 'Triggers: user asks about a laptop OS, notebook OS, or running Aerynza OS on a laptop. Cross-references: universal_os, device_drivers, device_flash, ip_guard. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'desktop_os',
    promoted: false,
    name: 'Desktop OS',
    category: 'engineering',
    description: 'Port or build the universal OS for desktop towers and all-in-ones: multi-monitor, GPU, peripherals, storage, and networking',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'universal_os',
      'laptop_os',
      'device_drivers',
      'device_flash',
      'ip_guard'
    ],
    context: 'Triggers: user asks about a desktop OS, tower OS, or running Aerynza OS on a desktop. Cross-references: universal_os, laptop_os, device_drivers, device_flash, ip_guard. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'smart_device_os',
    promoted: false,
    name: 'Smart Device OS',
    category: 'engineering',
    description: 'Port or build the universal OS for smart home, wearables, IoT, and embedded devices',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'universal_os',
      'device_drivers',
      'device_flash',
      'ip_guard'
    ],
    context: 'Triggers: user asks about smart home OS, wearable OS, IoT OS, or embedded device OS. Cross-references: universal_os, device_drivers, device_flash, ip_guard. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'device_drivers',
    promoted: false,
    name: 'Universal Device Drivers',
    category: 'engineering',
    description: 'Generate and organize a shared driver layer that works across phones, laptops, desktops, and smart devices',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'universal_os',
      'phone_drivers',
      'phone_os',
      'laptop_os',
      'desktop_os',
      'smart_device_os',
      'ip_guard'
    ],
    context: 'Triggers: user asks about drivers for multiple device types, shared HAL, or universal device support. Cross-references: universal_os, phone_drivers, phone_os, laptop_os, desktop_os, smart_device_os, ip_guard. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'device_flash',
    promoted: false,
    name: 'Universal Device Flash',
    category: 'engineering',
    description: 'Prepare and flash the universal OS onto any connected phone, laptop, desktop, or smart device over USB or network',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'universal_os',
      'laptop_os',
      'desktop_os',
      'smart_device_os',
      'phone_flash',
      'ip_guard'
    ],
    context: 'Triggers: user asks to flash an OS to a laptop, desktop, smart device, or any hardware. Cross-references: universal_os, laptop_os, desktop_os, smart_device_os, phone_flash, ip_guard. Requires explicit device.flash permission and a verified receipt before writing to any device.'
  },
  {
    id: 'ip_guard',
    promoted: false,
    name: 'IP Guard',
    category: 'engineering',
    description: 'Protect Aerynza intellectual property in source code, models, designs, and binaries through licensing, watermarking, and access control',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'universal_os',
      'device_drivers',
      'device_flash',
      'code_guardian'
    ],
    context: 'Triggers: user asks about protecting IP, licensing an OS, watermarking binaries, or access control for proprietary source. Cross-references: universal_os, device_drivers, device_flash, code_guardian. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'code_guardian',
    promoted: false,
    name: 'Code Guardian',
    category: 'engineering',
    description: 'Audit, sign, encrypt, and vault Aerynza source code and artifacts to prevent unauthorized exfiltration or tampering',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'engineering',
    related_capabilities: [
      'ip_guard',
      'universal_os',
      'ascension_second_brain',
      'ascension_knowledge_vault'
    ],
    context: 'Triggers: user asks about source code vault, code signing, encryption, or leak prevention for proprietary code. Cross-references: ip_guard, universal_os, ascension_second_brain, ascension_knowledge_vault. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ar_assistant',
    promoted: false,
    name: 'AR Assistant',
    category: 'spatial',
    description: 'A Jarvis-level AR companion that walks with the user in the real world, sees what they see, and gives context-aware guidance',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_environment_scan',
      'ar_object_recognition',
      'ar_navigation',
      'ar_realtime_translate',
      'ar_people_recognition',
      'ar_context_feed',
      'ar_proactive_data',
      'ar_safety_alert',
      'ar_memory_anchor'
    ],
    context: 'Triggers: user asks about AR glasses, walking AI, real-world assistant, spatial companion, or Jarvis in public. Cross-references: ar_environment_scan, ar_object_recognition, ar_navigation, ar_realtime_translate, ar_people_recognition, ar_context_feed, ar_proactive_data, ar_safety_alert, ar_memory_anchor. Use with permission-scoped context and a receipt for any action.'
  },
  {
    id: 'ar_environment_scan',
    promoted: false,
    name: 'AR Environment Scan',
    category: 'spatial',
    description: 'Build and maintain a real-time 3D map of the user\'s surroundings for safe AR interaction',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_object_recognition',
      'ar_safety_alert',
      'ar_memory_anchor',
      'ascension_vision'
    ],
    context: 'Triggers: user asks about scanning a room, mapping surroundings, spatial mesh, or obstacle detection. Cross-references: ar_assistant, ar_object_recognition, ar_safety_alert, ar_memory_anchor, ascension_vision. Requires camera.read, location.read, and ar.read permissions.'
  },
  {
    id: 'ar_object_recognition',
    promoted: false,
    name: 'AR Object Recognition',
    category: 'spatial',
    description: 'Identify objects, labels, prices, ingredients, and hazards in the user\'s field of view',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_environment_scan',
      'ar_context_feed',
      'ar_proactive_data',
      'ascension_vision'
    ],
    context: 'Triggers: user asks what something is, read a label, identify an object, or scan ingredients. Cross-references: ar_assistant, ar_environment_scan, ar_context_feed, ar_proactive_data, ascension_vision. Requires camera.read and ar.read permissions.'
  },
  {
    id: 'ar_navigation',
    promoted: false,
    name: 'AR Navigation',
    category: 'spatial',
    description: 'Overlay walking, driving, and indoor directions directly into the user\'s view',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_environment_scan',
      'ar_context_feed',
      'ascension_location_intelligence',
      'ascension_appointments'
    ],
    context: 'Triggers: user asks for walking directions, indoor navigation, or AR arrows to a destination. Cross-references: ar_assistant, ar_environment_scan, ar_context_feed, ascension_location_intelligence, ascension_appointments. Requires location.read, camera.read, and ar.overlay permissions.'
  },
  {
    id: 'ar_realtime_translate',
    promoted: false,
    name: 'AR Real-Time Translate',
    category: 'spatial',
    description: 'Translate signs, menus, conversations, and text the user sees in real time through AR',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_object_recognition',
      'ar_context_feed',
      'translation',
      'ascension_voice_intelligence'
    ],
    context: 'Triggers: user asks to translate a sign, menu, or conversation through AR glasses. Cross-references: ar_assistant, ar_object_recognition, ar_context_feed, translation, ascension_voice_intelligence. Requires camera.read, microphone.read, and ar.overlay permissions.'
  },
  {
    id: 'ar_people_recognition',
    promoted: false,
    name: 'AR People Recognition',
    category: 'spatial',
    description: 'Recognize known contacts, read name tags, and give social context about people in view',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_context_feed',
      'ascension_personal_vortex',
      'ascension_network_vortex',
      'ascension_identity'
    ],
    context: 'Triggers: user asks who someone is, remember a face, or get context on a contact. Cross-references: ar_assistant, ar_context_feed, ascension_personal_vortex, ascension_network_vortex, ascension_identity. Requires ar.read and an explicit privacy setting. Does not identify strangers without consent.'
  },
  {
    id: 'ar_context_feed',
    promoted: false,
    name: 'AR Context Feed',
    category: 'spatial',
    description: 'Stream relevant, glanceable information to the user based on what they are looking at and where they are',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_object_recognition',
      'ar_navigation',
      'ar_realtime_translate',
      'ascension_living_context',
      'ascension_proactive_engine'
    ],
    context: 'Triggers: user asks for heads-up display, AR overlay info, glanceable data, or context about a place. Cross-references: ar_assistant, ar_object_recognition, ar_navigation, ar_realtime_translate, ascension_living_context, ascension_proactive_engine. Requires camera.read, location.read, and ar.overlay permissions.'
  },
  {
    id: 'ar_proactive_data',
    promoted: false,
    name: 'AR Proactive Data',
    category: 'spatial',
    description: 'Anticipate what the user needs next and feed it without being asked while in AR mode',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_context_feed',
      'ar_safety_alert',
      'ascension_proactive_engine',
      'ascension_living_context'
    ],
    context: 'Triggers: user enables proactive AR or asks AP to look ahead. Cross-references: ar_assistant, ar_context_feed, ar_safety_alert, ascension_proactive_engine, ascension_living_context. Requires explicit opt-in, camera.read, location.read, and ar.overlay permissions. Respects bystander privacy and never proactively identifies strangers.'
  },
  {
    id: 'ar_safety_alert',
    promoted: false,
    name: 'AR Safety Alert',
    category: 'spatial',
    description: 'Warn the user about physical hazards, traffic, obstacles, and unsafe conditions in AR',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_environment_scan',
      'ar_object_recognition',
      'ascension_health_intelligence',
      'ascension_location_intelligence'
    ],
    context: 'Triggers: user asks for safety warnings, obstacle detection, traffic alerts, or hazard overlay. Cross-references: ar_assistant, ar_environment_scan, ar_object_recognition, ascension_health_intelligence, ascension_location_intelligence. Requires camera.read and ar.read permissions.'
  },
  {
    id: 'ar_memory_anchor',
    promoted: false,
    name: 'AR Memory Anchor',
    category: 'spatial',
    description: 'Tag places, objects, and moments in the real world so AP can recall context later',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: 'spatial',
    related_capabilities: [
      'ar_assistant',
      'ar_environment_scan',
      'ascension_second_brain',
      'ascension_living_memory',
      'ascension_living_context'
    ],
    context: 'Triggers: user asks to remember where something is, save a location, or anchor an object. Cross-references: ar_assistant, ar_environment_scan, ascension_second_brain, ascension_living_memory, ascension_living_context. Requires camera.read, location.read, and ar.write permissions. Stores anchors locally unless user opts into cloud backup.'
  }
];
const CAPABILITY_MAP = new Map(CAPABILITIES.map(c => [c.id, c]));

export function getCapabilityById(id: string) {
  return CAPABILITY_MAP.get(id);
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

export function getPromotedCapabilities() {
  return CAPABILITIES.filter(c => c.promoted !== false);
}
