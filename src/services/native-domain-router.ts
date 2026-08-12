/**
 * Native Domain Router
 *
 * Provides structured, deterministic responses for each native overlay capability
 * while the generative model is still in training. This keeps the API useful,
 * fast, and safe across all registered native domains.
 */

import { requestPermissions, PermissionStatus } from './permission-engine';

export interface NativeResponse {
  content: string;
  model: string;
  provider: 'ascension-native';
  tokensUsed: number;
  capability: string;
  data?: Record<string, any>;
}

function permissionMessage(capability: string, permissions: Record<string, PermissionStatus>): { content: string } | null {
  const request = requestPermissions(capability, permissions);
  if (!request.can_execute) {
    return { content: request.message };
  }
  return null;
}

function travelResponse(message: string): NativeResponse {
  const days = /\d+\s*(?:day|week|nights?)/i.test(message) ? 'detected' : 'not specified';
  return {
    content: `I can build a complete travel plan once you share destination, dates, and budget. Nothing has been booked. So far I noted: ${days === 'detected' ? 'you mentioned a duration' : 'no duration yet'}. Please confirm where you want to go and your preferred travel window.`,
    model: 'Ascension Travel',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_travel',
    data: { days_detected: days === 'detected' }
  };
}

function legalResponse(message: string): NativeResponse {
  return {
    content: `I can review and explain documents, point out clauses to watch, and flag areas where a licensed attorney should review. I am not a lawyer and cannot guarantee outcomes. Please paste the document or describe the issue.`,
    model: 'Ascension Legal',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_legal',
    data: { review_type: 'preliminary', disclaimer: true }
  };
}

function realEstateResponse(message: string): NativeResponse {
  return {
    content: `I can help with housing search, lease review, and cash-flow-based affordability. The key variables that change the answer are location, move-in date, household needs, verified monthly housing limit, and total move-in cash. Nothing has been searched or applied for yet.`,
    model: 'Ascension Real Estate',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_realestate',
    data: { search_started: false }
  };
}

function researchResponse(message: string): NativeResponse {
  return {
    content: `I can research a topic, compare sources, and prepare citations. I will separate verified facts from inference and note uncertainty. What topic or question do you want me to investigate?`,
    model: 'Ascension Research',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_research',
    data: { sources: [], status: 'awaiting_query' }
  };
}

function eventsResponse(message: string): NativeResponse {
  return {
    content: `I can plan an event from guest list to venue and timeline. The biggest variables that shape the plan are date, guest count, location, and budget. Nothing has been booked or scheduled yet.`,
    model: 'Ascension Events',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_events',
    data: { planned: false }
  };
}

function automotiveResponse(message: string): NativeResponse {
  return {
    content: `I can track maintenance schedules, diagnose common symptoms from descriptions, and help compare vehicles. For repairs, I will flag when a mechanic should inspect it. Please describe the symptom or maintenance item.`,
    model: 'Ascension Automotive',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_automotive',
    data: { mechanic_referral: false }
  };
}

function petsResponse(message: string): NativeResponse {
  return {
    content: `I can help with training routines, nutrition, and when to call a vet. I cannot diagnose animals. Please describe your pet, the symptom, or the behavior.`,
    model: 'Ascension Pets',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_pets',
    data: { vet_referral: false }
  };
}

function weatherResponse(message: string): NativeResponse {
  return {
    content: `I can make weather-aware plans once you tell me the location and the day. I will not invent forecast data. Please share where and when.`,
    model: 'Ascension Weather',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_weather',
    data: { location: null, date: null }
  };
}

function financeResponse(message: string): NativeResponse {
  return {
    content: `I can analyze cash flow, income, debt, and spending, and build a step-by-step plan. I need your real balances, income dates, and upcoming bills to do it safely. Nothing has been budgeted or moved yet.`,
    model: 'Ascension Financial Intelligence',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_finance',
    data: { planning_started: false }
  };
}

function tradingResponse(message: string): NativeResponse {
  return {
    content: `I can analyze markets, backtest strategies, and run paper trades. I will not place live orders without your explicit approval and a verified broker receipt. What market or strategy do you want to explore?`,
    model: 'Ascension Trading Intelligence',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_trading',
    data: { paper_only: true }
  };
}

function healthResponse(message: string): NativeResponse {
  return {
    content: `I can help with wellness planning and symptom guidance, but I cannot diagnose or replace a healthcare provider. Please describe what you are experiencing or share any vitals you are comfortable with.`,
    model: 'Ascension Health',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_health',
    data: { medical_disclaimer: true }
  };
}

function homeResponse(message: string): NativeResponse {
  return {
    content: `I can coordinate schedules, chores, and smart home devices for your household. Nothing has been changed yet. Tell me who is in the household and what you want to organize.`,
    model: 'Ascension HomeOS',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_home',
    data: { household_known: false }
  };
}

function sproutResponse(message: string): NativeResponse {
  return {
    content: `I can create age-appropriate learning paths and milestone guidance under parent supervision. Tell me the child\'s age, interests, and what you want to focus on.`,
    model: 'Ascension Sprout',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_sprout',
    data: { parent_supervision: true }
  };
}

function familyResponse(message: string): NativeResponse {
  return {
    content: `I can help with family enterprise planning, governance, and shared records using only explicitly shared family data. What is the family decision or record you want to work on?`,
    model: 'Ascension FamilyOS',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_family',
    data: { shared_only: true }
  };
}

function chatResponse(message: string): NativeResponse {
  return {
    content: `I am AP, your Ascension Partner. I can help across every domain of your life, but I will not pretend to see data you have not shared and I will not act without your approval. What is on your mind?`,
    model: 'Ascension AP',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_chat',
    data: { shell: 'ap' }
  };
}

function nutritionResponse(message: string): NativeResponse {
  return {
    content: `I can build meal plans and analyze nutrition for your goals and preferences. I am not a dietitian; for medical conditions or eating disorders, I will point you toward a qualified provider. What are your goals?`,
    model: 'Ascension Nutrition',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_nutrition',
    data: { dietitian_referral: false }
  };
}

function fitnessResponse(message: string): NativeResponse {
  return {
    content: `I can design workouts, track progress, and suggest form cues. I will not push you past your limits or diagnose injury. What is your current routine or goal?`,
    model: 'Ascension Fitness',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_fitness',
    data: { injury_screen: false }
  };
}

function careerResponse(message: string): NativeResponse {
  return {
    content: `I can review resumes, prepare for interviews, and map career moves. I will not apply for jobs or send messages on your behalf without explicit approval. What are you working toward?`,
    model: 'Ascension Career',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_career',
    data: { applications: [] }
  };
}

function relationshipsResponse(message: string): NativeResponse {
  return {
    content: `I can help you think through conversations, prepare thoughtful responses, and notice relationship patterns. I will not contact anyone for you. What is the situation?`,
    model: 'Ascension Relationships',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_relationships',
    data: { sent_messages: [] }
  };
}

function creativeResponse(message: string): NativeResponse {
  return {
    content: `I can brainstorm, draft, and iterate on creative work. I will not publish or submit anything without you reviewing it. What are you creating?`,
    model: 'Ascension Creative',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_creative',
    data: { published: [] }
  };
}

function codeResponse(message: string): NativeResponse {
  return {
    content: `I can write, review, debug, and explain code. I will not execute code on your production systems or push changes without approval. What language and problem are you working in?`,
    model: 'Ascension Code',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_code',
    data: { executed: false }
  };
}

function learningResponse(message: string): NativeResponse {
  return {
    content: `I can build an adaptive learning path, assess gaps, and create practice problems. I will not lock you into a course you hate. What skill or topic do you want to learn?`,
    model: 'Ascension Learning',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_learning',
    data: { enrolled: [] }
  };
}

function meetingsResponse(message: string): NativeResponse {
  return {
    content: `I can summarize meetings, extract action items, and draft follow-ups. I need the transcript or recording to work from. Please paste the meeting text or upload the recording.`,
    model: 'Ascension Meetings',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_meetings',
    data: { transcript_received: false }
  };
}

function voiceResponse(message: string): NativeResponse {
  return {
    content: `I can process voice commands and transcribe speech. Microphone permission is required. Nothing has been recorded yet. Please enable voice when you are ready.`,
    model: 'Ascension Voice',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_voice',
    data: { microphone_required: true, recorded: false }
  };
}

function securityResponse(message: string): NativeResponse {
  return {
    content: `I can review security settings, flag suspicious behavior, and give privacy guidance. I will not change firewall, access, or authentication rules without explicit approval. What are you worried about?`,
    model: 'Ascension Security',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_security',
    data: { rules_changed: [] }
  };
}

function psychologyResponse(message: string): NativeResponse {
  return {
    content: `I can explain human behavior, emotion, motivation, cognition, and mental patterns. I am not a therapist or psychiatrist. If you are in crisis or need diagnosis, I will point you to a qualified professional. What are you trying to understand about yourself or someone else?`,
    model: 'Ascension Psychology',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_psychology',
    data: { therapist_referral: false }
  };
}

function humanLifeResponse(message: string): NativeResponse {
  return {
    content: `I can help across every domain of human life: identity, health, money, work, relationships, home, time, learning, creativity, meaning, and transitions. Which area are you working on right now?`,
    model: 'Ascension Human Life',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_human_life',
    data: { domains: ['identity', 'health', 'money', 'work', 'relationships', 'home', 'time', 'learning', 'creativity', 'meaning', 'transitions'] }
  };
}

function spiritualityResponse(message: string): NativeResponse {
  return {
    content: `I can explore faith, meditation, ritual, nature, legacy, and existential questions with you. I will not impose a framework; I can work with yours. What are you reflecting on?`,
    model: 'Ascension Spirituality',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_spirituality',
    data: { imposed_framework: false }
  };
}

function griefResponse(message: string): NativeResponse {
  return {
    content: `I am sorry you are going through this. I can hold space, help you organize practical tasks, and point you toward support. I am not a grief counselor. If the pain is overwhelming or persistent, please consider a professional or support group. What do you need most right now?`,
    model: 'Ascension Grief',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_grief',
    data: { counselor_referral: false }
  };
}

function mentalHealthResponse(message: string): NativeResponse {
  return {
    content: `I can help you understand stress, anxiety, low mood, emotional patterns, and when to seek professional help. I am not a therapist or doctor. If you are in crisis, please reach out to a crisis line or emergency services. What are you experiencing?`,
    model: 'Ascension Mental Health',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_mental_health',
    data: { crisis: false }
  };
}

function communicationResponse(message: string): NativeResponse {
  return {
    content: `I can help you prepare for difficult conversations, listen actively, and reduce conflict. I cannot send messages for you. Who is the conversation with and what is the goal?`,
    model: 'Ascension Communication',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_communication',
    data: { sent_messages: [] }
  };
}

function habitsResponse(message: string): NativeResponse {
  return {
    content: `I can help you build habits using cues, routines, rewards, and identity-based change. Tiny, consistent steps outperform heroic bursts. What habit do you want to build or break?`,
    model: 'Ascension Habits',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_habits',
    data: { streaks: [] }
  };
}

function stressResponse(message: string): NativeResponse {
  return {
    content: `I can help you spot stress signals, calm the nervous system, and recover before burnout. What is draining you right now and what is in your control?`,
    model: 'Ascension Stress',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_stress',
    data: { burnout_risk: 'unknown' }
  };
}

function sleepResponse(message: string): NativeResponse {
  return {
    content: `I can help you design a sleep routine and align with your circadian rhythm. I cannot diagnose sleep disorders; persistent insomnia may need a clinician. What is your current sleep pattern?`,
    model: 'Ascension Sleep',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_sleep',
    data: { clinician_referral: false }
  };
}

function parentingResponse(message: string): NativeResponse {
  return {
    content: `I can offer child-development guidance, discipline strategies, and co-parenting support. I am not a pediatrician or therapist. What age and situation are you navigating?`,
    model: 'Ascension Parenting',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_parenting',
    data: { child_age: null }
  };
}

function mindfulnessResponse(message: string): NativeResponse {
  return {
    content: `I can guide breathing, presence, and attention practices. Start with a few slow breaths. What is pulling your attention right now?`,
    model: 'Ascension Mindfulness',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_mindfulness',
    data: { practice_seconds: 0 }
  };
}

function timeResponse(message: string): NativeResponse {
  return {
    content: `I can help you map your energy, prioritize, and reduce procrastination. Time management works best when it follows your biology and values. What is competing for your time right now?`,
    model: 'Ascension Time',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_time',
    data: { priorities: [] }
  };
}

function confidenceResponse(message: string): NativeResponse {
  return {
    content: `I can help you build confidence through small wins, evidence, and self-compassion. Confidence grows from action and alignment, not just positive thinking. What situation is making you doubt yourself?`,
    model: 'Ascension Confidence',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_confidence',
    data: { small_wins: [] }
  };
}

function agingResponse(message: string): NativeResponse {
  return {
    content: `I can help with healthy aging, mobility, nutrition, and life-stage planning. I am not a geriatric specialist; persistent issues need a clinician. What are you planning for?`,
    model: 'Ascension Aging',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_aging',
    data: { clinician_referral: false }
  };
}

function addictionResponse(message: string): NativeResponse {
  return {
    content: `I can offer recovery support, habit strategies, and resources. I am not an addiction counselor. If you are in crisis or need treatment, please reach out to a professional or a recovery support line. What are you working to change?`,
    model: 'Ascension Addiction',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_addiction',
    data: { counselor_referral: false }
  };
}

function conflictResponse(message: string): NativeResponse {
  return {
    content: `I can help you de-escalate, understand positions, and find repair paths. I cannot contact anyone for you. What is the conflict about and what do you want to achieve?`,
    model: 'Ascension Conflict',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_conflict',
    data: { sent_messages: [] }
  };
}

function datingResponse(message: string): NativeResponse {
  return {
    content: `I can help with dating safety, boundaries, conversation, and red flags. I will not message anyone for you. What is the situation?`,
    model: 'Ascension Dating',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_dating',
    data: { sent_messages: [] }
  };
}

function cookingResponse(message: string): NativeResponse {
  return {
    content: `I can suggest recipes, meal plans, and substitutions based on what you have and your goals. What ingredients or dietary goals do you have?`,
    model: 'Ascension Cooking',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_cooking',
    data: { ingredients: [] }
  };
}

function socialResponse(message: string): NativeResponse {
  return {
    content: `I can help with friendship, networking, social skills, and community. What kind of connection are you looking for or struggling with?`,
    model: 'Ascension Social',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_social',
    data: { community: [] }
  };
}

function volunteeringResponse(message: string): NativeResponse {
  return {
    content: `I can help you find ways to contribute that match your skills and values. What causes or skills do you care about?`,
    model: 'Ascension Volunteering',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_volunteering',
    data: { causes: [] }
  };
}

function focusResponse(message: string): NativeResponse {
  return {
    content: `I can help you enter and protect deep work, manage attention, and reduce distraction. What is pulling you away from focus right now?`,
    model: 'Ascension Focus',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_focus',
    data: { pomodoro_minutes: 0 }
  };
}

function meditationResponse(message: string): NativeResponse {
  return {
    content: `I can guide simple meditations: breath focus, body scan, or open awareness. What sounds most useful right now?`,
    model: 'Ascension Meditation',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_meditation',
    data: { minutes: 0 }
  };
}

function gardenResponse(message: string): NativeResponse {
  return {
    content: `I can help plan a garden, choose plants for your climate, and troubleshoot care. What are you growing or want to grow?`,
    model: 'Ascension Garden',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_garden',
    data: { plants: [] }
  };
}

function fashionResponse(message: string): NativeResponse {
  return {
    content: `I can help with style, wardrobe building, and occasion dressing. What is the event or goal?`,
    model: 'Ascension Fashion',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_fashion',
    data: { occasion: null }
  };
}

function repairResponse(message: string): NativeResponse {
  return {
    content: `I can guide DIY repairs and help you decide when a professional is safer. What is broken and what tools do you have?`,
    model: 'Ascension Repair',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_repair',
    data: { call_pro: false }
  };
}

function musicResponse(message: string): NativeResponse {
  return {
    content: `I can help with music theory, composition, practice routines, and listening. What instrument or genre are you working in?`,
    model: 'Ascension Music',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_music',
    data: { instrument: null }
  };
}

function artResponse(message: string): NativeResponse {
  return {
    content: `I can discuss art techniques, composition, and creative direction. What medium or piece are you working on?`,
    model: 'Ascension Art',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_art',
    data: { medium: null }
  };
}

function writingResponse(message: string): NativeResponse {
  return {
    content: `I can help with writing craft, structure, voice, and editing. I will not publish anything for you. What are you writing?`,
    model: 'Ascension Writing',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_writing',
    data: { published: [] }
  };
}

function moviesResponse(message: string): NativeResponse {
  return {
    content: `I can recommend films and shows based on your mood, taste, and time. What do you like and how much time do you have?`,
    model: 'Ascension Movies',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_movies',
    data: { watchlist: [] }
  };
}

function booksResponse(message: string): NativeResponse {
  return {
    content: `I can recommend books, discuss themes, and help with reading lists. What do you enjoy or want to learn?`,
    model: 'Ascension Books',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_books',
    data: { reading_list: [] }
  };
}

function newsResponse(message: string): NativeResponse {
  return {
    content: `I can summarize and contextualize news, and help you spot bias. I will not invent current events. What topic or headline do you want to understand?`,
    model: 'Ascension News',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_news',
    data: { sources: [] }
  };
}

function sportsResponse(message: string): NativeResponse {
  return {
    content: `I can analyze sports, training, and fan questions. What sport, team, or training goal are you focused on?`,
    model: 'Ascension Sports',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_sports',
    data: { sport: null }
  };
}

function gamesResponse(message: string): NativeResponse {
  return {
    content: `I can recommend games, discuss strategy, and talk game design. What genre or game are you into?`,
    model: 'Ascension Games',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_games',
    data: { genre: null }
  };
}

function shoppingResponse(message: string): NativeResponse {
  return {
    content: `I can help you compare products and find the best value for your needs. What are you shopping for?`,
    model: 'Ascension Shopping',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_shopping',
    data: { budget: null }
  };
}

function investingResponse(message: string): NativeResponse {
  return {
    content: `I can explain portfolio thinking, asset allocation, and long-term strategies. I will not promise returns. What are your goals and time horizon?`,
    model: 'Ascension Investing',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_investing',
    data: { returns_promised: false }
  };
}

function taxesResponse(message: string): NativeResponse {
  return {
    content: `I can help organize tax documents, find deductions to review, and prepare for a tax professional. I am not a tax preparer. What is your tax situation?`,
    model: 'Ascension Taxes',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_taxes',
    data: { preparer: false }
  };
}

function insuranceResponse(message: string): NativeResponse {
  return {
    content: `I can help review coverage types, gaps, and comparisons. I am not an insurance agent. What coverage are you reviewing?`,
    model: 'Ascension Insurance',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_insurance',
    data: { agent: false }
  };
}

function movingResponse(message: string): NativeResponse {
  return {
    content: `I can help with moving checklists, timelines, and logistics. Where are you moving from and to, and when?`,
    model: 'Ascension Moving',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_moving',
    data: { moved: false }
  };
}

function cleaningResponse(message: string): NativeResponse {
  return {
    content: `I can help build cleaning routines and choose products. What spaces or schedules do you want to tackle?`,
    model: 'Ascension Cleaning',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_cleaning',
    data: { schedule: [] }
  };
}

function philosophyResponse(message: string): NativeResponse {
  return {
    content: `I can explore philosophical questions, schools, and arguments with you. What question or thinker do you want to examine?`,
    model: 'Ascension Philosophy',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_philosophy',
    data: { school: null }
  };
}

function historyResponse(message: string): NativeResponse {
  return {
    content: `I can provide historical context and discuss events and lessons. What period, event, or figure are you interested in?`,
    model: 'Ascension History',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_history',
    data: { period: null }
  };
}

function scienceResponse(message: string): NativeResponse {
  return {
    content: `I can explain scientific concepts and help with scientific thinking. What topic or question do you have?`,
    model: 'Ascension Science',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_science',
    data: { field: null }
  };
}

function mathResponse(message: string): NativeResponse {
  return {
    content: `I can walk through math problems and concepts step by step. What problem or topic are you working on?`,
    model: 'Ascension Math',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_math',
    data: { solved: false }
  };
}

function languageResponse(message: string): NativeResponse {
  return {
    content: `I can help you learn a language, practice phrases, or translate. Which language and what is your level?`,
    model: 'Ascension Language',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_language',
    data: { language: null }
  };
}

function cultureResponse(message: string): NativeResponse {
  return {
    content: `I can discuss cultural context, etiquette, and traditions. What culture or situation do you want to understand?`,
    model: 'Ascension Culture',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_culture',
    data: { context: null }
  };
}

function ethicsResponse(message: string): NativeResponse {
  return {
    content: `I can help you reason through ethical questions and clarify values. What dilemma or principle are you considering?`,
    model: 'Ascension Ethics',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_ethics',
    data: { dilemma: null }
  };
}

function environmentResponse(message: string): NativeResponse {
  return {
    content: `I can help with sustainability choices, climate understanding, and ecological action. What are you trying to reduce or improve?`,
    model: 'Ascension Environment',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_environment',
    data: { action_plan: [] }
  };
}

function activismResponse(message: string): NativeResponse {
  return {
    content: `I can help with advocacy, civic action, and community organizing. What cause or change are you working toward?`,
    model: 'Ascension Activism',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_activism',
    data: { campaign: null }
  };
}

function projectResponse(message: string): NativeResponse {
  return {
    content: `I can help plan projects, define milestones, and track delivery. I won't claim any tasks are done without a receipt. What is the project goal?`,
    model: 'Ascension Project',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_project',
    data: { milestones: [] }
  };
}

function taskResponse(message: string): NativeResponse {
  return {
    content: `I can help break work into tasks, prioritize, and plan execution. I can't mark tasks complete in your system without permission. What do you need to get done?`,
    model: 'Ascension Task',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_task',
    data: { completed: [] }
  };
}

function remoteResponse(message: string): NativeResponse {
  return {
    content: `I can help with remote work routines, focus, and async collaboration. What is your remote-work challenge?`,
    model: 'Ascension Remote',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_remote',
    data: { setup: null }
  };
}

function interviewResponse(message: string): NativeResponse {
  return {
    content: `I can help you prepare and practice for interviews. What role or type of interview?`,
    model: 'Ascension Interview',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_interview',
    data: { role: null }
  };
}

function resumeResponse(message: string): NativeResponse {
  return {
    content: `I can review resumes and cover letters and suggest improvements. I won't send anything to employers. Paste or describe what you have.`,
    model: 'Ascension Resume',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_resume',
    data: { submitted: [] }
  };
}

function negotiationResponse(message: string): NativeResponse {
  return {
    content: `I can help you prepare for negotiations and practice language. I won't guarantee outcomes. What are you negotiating?`,
    model: 'Ascension Negotiation',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_negotiation',
    data: { guarantee: false }
  };
}

function networkingResponse(message: string): NativeResponse {
  return {
    content: `I can help with professional networking strategy and outreach. What field or event are you focused on?`,
    model: 'Ascension Networking',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_networking',
    data: { contacts: [] }
  };
}

function leadershipResponse(message: string): NativeResponse {
  return {
    content: `I can discuss leadership, management, and team guidance. What leadership challenge are you facing?`,
    model: 'Ascension Leadership',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_leadership',
    data: { team_size: null }
  };
}

function teamResponse(message: string): NativeResponse {
  return {
    content: `I can help with team dynamics, collaboration, and conflict. What is happening with the team?`,
    model: 'Ascension Team',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_team',
    data: { members: [] }
  };
}

function feedbackResponse(message: string): NativeResponse {
  return {
    content: `I can help you give or receive feedback with clarity and respect. What feedback situation do you want to work through?`,
    model: 'Ascension Feedback',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: 'ascension_feedback',
    data: { delivered: false }
  };
}

const DOMAIN_HANDLERS: Record<string, (message: string) => NativeResponse> = {
  'ascension_travel': travelResponse,
  'ascension_legal': legalResponse,
  'ascension_realestate': realEstateResponse,
  'ascension_research': researchResponse,
  'ascension_events': eventsResponse,
  'ascension_automotive': automotiveResponse,
  'ascension_pets': petsResponse,
  'ascension_weather': weatherResponse,
  'ascension_finance': financeResponse,
  'ascension_trading': tradingResponse,
  'ascension_health': healthResponse,
  'ascension_home': homeResponse,
  'ascension_sprout': sproutResponse,
  'ascension_family': familyResponse,
  'ascension_chat': chatResponse,
  'ascension_nutrition': nutritionResponse,
  'ascension_fitness': fitnessResponse,
  'ascension_career': careerResponse,
  'ascension_relationships': relationshipsResponse,
  'ascension_creative': creativeResponse,
  'ascension_code': codeResponse,
  'ascension_learning': learningResponse,
  'ascension_meetings': meetingsResponse,
  'ascension_voice': voiceResponse,
  'ascension_security': securityResponse,
  'ascension_psychology': psychologyResponse,
  'ascension_human_life': humanLifeResponse,
  'ascension_spirituality': spiritualityResponse,
  'ascension_grief': griefResponse,
  'ascension_mental_health': mentalHealthResponse,
  'ascension_communication': communicationResponse,
  'ascension_habits': habitsResponse,
  'ascension_stress': stressResponse,
  'ascension_sleep': sleepResponse,
  'ascension_parenting': parentingResponse,
  'ascension_mindfulness': mindfulnessResponse
};

export function routeNativeDomain(
  capabilityId: string,
  message: string,
  permissions: Record<string, PermissionStatus>
): NativeResponse {
  const permissionMsg = permissionMessage(capabilityId, permissions);
  if (permissionMsg) {
    return {
      content: permissionMsg.content,
      model: 'Ascension Permission Gate',
      provider: 'ascension-native',
      tokensUsed: 0,
      capability: capabilityId
    };
  }

  const handler = DOMAIN_HANDLERS[capabilityId];
  if (handler) {
    return handler(message);
  }

  return {
    content: `Ascension native response for ${capabilityId} (stub: domain handler not yet specialized).`,
    model: 'Ascension Candidate 3B',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: capabilityId
  };
}
