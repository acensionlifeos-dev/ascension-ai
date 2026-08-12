"""
Append canonical Ascension LifeOS capabilities to the Ascension AI registry only.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "src" / "services" / "capability-registry.ts"

NEW = [
    ("ascension_human_intelligence", "Ascension Human Intelligence", "intelligence", "Understand the human completely: identity, emotion, life flow, biometric, voice, behavior"),
    ("ascension_behavioral_intelligence", "Ascension Behavioral Intelligence", "intelligence", "Model procrastination, consistency, risk tolerance, follow-through, and motivation patterns"),
    ("ascension_astrology_intelligence", "Ascension Astrology Intelligence", "intelligence", "Symbolic astrological context as a supplement, never a deterministic prediction"),
    ("ascension_identity", "Ascension Identity", "intelligence", "Track and evolve the user's identity, values, roles, and self-concept"),
    ("ascension_life_flow", "Ascension Life Flow", "intelligence", "Model energy, schedule, recovery, and optimal execution windows"),
    ("ascension_biometric", "Ascension Biometric", "intelligence", "Read and act on HRV, sleep, recovery, and wearable signals"),
    ("ascension_voice_intelligence", "Ascension Voice Intelligence", "intelligence", "Voice-based interaction, tone, and voiceprint identity signals"),
    ("ascension_personality", "Ascension Personality", "intelligence", "Track personality layers, preferences, and decision style"),
    ("ascension_resource_intelligence", "Ascension Resource Intelligence", "intelligence", "Manage all resources: money, time, energy, skills, assets, credit, investments"),
    ("ascension_global_economics", "Ascension Global Economics", "finance", "Track macro signals: inflation, rates, employment, commodities, government incentives"),
    ("ascension_credit", "Ascension Credit", "finance", "Track credit score, debt ratio, and credit-optimizing actions"),
    ("ascension_assets", "Ascension Assets", "finance", "Track real estate, vehicles, collectibles, and illiquid assets"),
    ("ascension_opportunity_finance", "Ascension Opportunity Finance", "finance", "Find grants, scholarships, tax credits, refinancing, and rebates"),
    ("ascension_world_intelligence", "Ascension World Intelligence", "knowledge", "Understand the external world: environment, markets, government, science, tech"),
    ("ascension_environmental", "Ascension Environmental", "knowledge", "Track environmental, weather, pollen, AQI, and climate factors"),
    ("ascension_government", "Ascension Government", "knowledge", "Track government programs, policy, and regulatory impact"),
    ("ascension_politics", "Ascension Politics", "knowledge", "Track political context and civic opportunities"),
    ("ascension_relationship_intelligence", "Ascension Relationship Intelligence", "relationships", "Synthesize relationships, network, community, mentors, and influence"),
    ("ascension_network_vortex", "Ascension Network Vortex", "relationships", "Maintain the people graph: relationships, organizations, and community"),
    ("ascension_community", "Ascension Community", "relationships", "Track communities, groups, and local/global causes"),
    ("ascension_professional_network", "Ascension Professional Network", "career", "Track mentors, recruiters, collaborators, and career relationships"),
    ("ascension_mentors", "Ascension Mentors", "career", "Track mentors, coaches, advisors, and guidance relationships"),
    ("ascension_influence", "Ascension Influence", "business", "Track thought leadership, audience, and influence growth"),
    ("ascension_creation_intelligence", "Ascension Creation Intelligence", "creation", "Accelerate creation across business, media, product, software, knowledge, and creative studios"),
    ("ascension_business_studio", "Ascension Business Studio", "business", "Think like a founder: model, revenue, CAC, retention, operations, funding"),
    ("ascension_media_studio", "Ascension Media Studio", "creation", "Think like a publisher: consistency, audience, engagement, monetization"),
    ("ascension_product_studio", "Ascension Product Studio", "creation", "Think like an industrial designer and manufacturing advisor"),
    ("ascension_software_studio", "Ascension Software Studio", "creation", "Think like a software architect: architecture, tech debt, testing, deployment, security"),
    ("ascension_knowledge_studio", "Ascension Knowledge Studio", "knowledge", "Think like an educator, researcher, and author"),
    ("ascension_creative_studio", "Ascension Creative Studio", "creation", "Think like an art director, creative coach, and portfolio strategist"),
    ("ascension_creation_auditor", "Ascension Creation Auditor", "creation", "Continuous health audit for any project or studio"),
    ("ascension_roadmap_engine", "Ascension Roadmap Engine", "creation", "Build and track project roadmaps, milestones, and dependencies"),
    ("ascension_scorecards", "Ascension Scorecards", "business", "Idea maturity, execution momentum, validation, launch, and risk scorecards"),
    ("ascension_creation_transformation", "Ascension Creation Transformation", "creation", "Dream-to-reality transformation loop: observe, design, build, launch, scale"),
    ("ascension_opportunity_intelligence", "Ascension Opportunity Intelligence", "intelligence", "Synthesize all engines to find and prioritize opportunities"),
    ("ascension_decision_physics", "Ascension Decision Physics", "intelligence", "Observe, predict, simulate, decide, explain, and learn from outcomes"),
    ("ascension_adaptive_quest", "Ascension Adaptive Quest", "intelligence", "Calibrate quest difficulty and selection based on tri-baseline, life flow, and behavior"),
    ("ascension_cie", "Ascension CIE", "intelligence", "Conversation Intelligence Engine: score and gate all proactive AP messages"),
    ("ascension_age", "Ascension AGE", "intelligence", "Ascension Guide Engine: onboarding, feature unlocking, and readiness scoring"),
    ("ascension_personal_vortex", "Ascension Personal Vortex", "intelligence", "Everything about the user: identity, goals, behavior, history, preferences"),
    ("ascension_world_vortex", "Ascension World Vortex", "intelligence", "Everything external: markets, science, tech, politics, weather, news"),
    ("ascension_unified_vortex", "Ascension Unified Vortex", "intelligence", "Synthesize Personal, World, and Network Vortex into composite insights"),
    ("ascension_vortex_signals", "Ascension Vortex Signals", "intelligence", "Store and reason over signals from every engine and connected API"),
    ("ascension_calendar_intelligence", "Ascension Calendar Intelligence", "productivity", "Infer productivity windows, meeting density, key relationships, and burnout from calendar"),
    ("ascension_email_intelligence", "Ascension Email Intelligence", "productivity", "Infer communication network, opportunity signals, and subscription creep from email"),
    ("ascension_plaid_intelligence", "Ascension Plaid Intelligence", "finance", "Infer financial behavior, stress spending, and cash flow patterns from Plaid"),
    ("ascension_investment_intelligence", "Ascension Investment Intelligence", "finance", "Infer risk, diversification, contribution discipline, and retirement readiness"),
    ("ascension_crypto_intelligence", "Ascension Crypto Intelligence", "finance", "Track wallets, exchanges, staking, DeFi, and tax events"),
    ("ascension_health_intelligence", "Ascension Health Intelligence", "wellness", "Read HRV, sleep, recovery, and burnout signals from wearables"),
    ("ascension_location_intelligence", "Ascension Location Intelligence", "knowledge", "Infer routines, gym attendance, nature exposure, and home-away ratio"),
    ("ascension_spotify_intelligence", "Ascension Spotify Intelligence", "wellness", "Infer mood, energy, work style, and stress management from music"),
    ("ascension_linkedin_intelligence", "Ascension LinkedIn Intelligence", "career", "Infer career velocity, recruiter activity, and professional influence"),
    ("ascension_youtube_intelligence", "Ascension YouTube Intelligence", "knowledge", "Infer learning investment, topic depth, and research patterns"),
    ("ascension_tiktok_intelligence", "Ascension TikTok Intelligence", "creation", "Infer creator momentum, content discipline, and trend awareness"),
    ("ascension_github_intelligence", "Ascension GitHub Intelligence", "creation", "Infer coding consistency, technical growth, and architecture maturity"),
    ("ascension_weather_intelligence", "Ascension Weather Intelligence", "knowledge", "Infer mood/energy correlation and activity suitability from weather"),
    ("ascension_news_intelligence", "Ascension News Intelligence", "knowledge", "Infer industry opportunity, economic context, and regulatory impact"),
    ("ascension_question_engine", "Ascension Question Engine", "intelligence", "Ask one question at a time, track state, and adapt follow-ups"),
    ("ascension_vault", "Ascension Vault", "intelligence", "Permanent digital estate: AP can read, never write or delete"),
    ("ascension_living_memory", "Ascension Living Memory", "intelligence", "Active cognition: current goals, patterns, and recent interactions"),
    ("ascension_living_context", "Ascension Living Context", "intelligence", "Weekly pre-computed working memory snapshot for fast AP responses"),
    ("ascension_proactivity", "Ascension Proactivity", "intelligence", "Configure silent to always-on reaction levels"),
    ("ascension_workout", "Ascension Workout", "wellness", "Plan and adapt exercise routines and physical training"),
    ("ascension_body_profile", "Ascension Body Profile", "wellness", "Track body data, photos, weight, BMR, and TDEE"),
    ("ascension_document_intelligence", "Ascension Document Intelligence", "knowledge", "OCR, classify, extract, and persist structured data from uploaded documents"),
    ("ascension_legacy", "Ascension Legacy", "intelligence", "Plan contribution, generational impact, and long-term life legacy"),
    ("ascension_contribution", "Ascension Contribution", "intelligence", "Track giving, mentorship, community impact, and contribution goals"),
]


def main():
    text = REGISTRY.read_text(encoding="utf-8")
    old = "  }\n];"
    if old not in text:
        raise SystemExit("Could not find registry end marker")
    new_objects = []
    for i, (cid, name, category, desc) in enumerate(NEW):
        comma = "," if i < len(NEW) - 1 else ""
        new_objects.append(f"""  {{
    id: '{cid}',
    name: '{name}',
    category: '{category}',
    description: '{desc}',
    providers: ['ascension-native'],
    default_provider: 'ascension-native',
    cost_per_1k_tokens: 0,
    requires_tier: 'individual',
    executor: '{category}'
  }}{comma}""")
    replacement = "  }\n" + ",\n".join(new_objects) + "\n];"
    text = text.replace(old, replacement, 1)
    REGISTRY.write_text(text, encoding="utf-8")
    print(f"Appended {len(NEW)} capabilities to registry")


if __name__ == "__main__":
    main()
