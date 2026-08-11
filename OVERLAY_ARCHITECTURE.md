# Ascension AI - Overlay Architecture

## Mission

Ascension AI is the **native intelligence layer** underneath all Ascension products. LifeOS, HomeOS, Sprout, FamilyOS, and Ascension AI itself are all **overlays** that consume, display, and act on the intelligence produced by this core AI.

## Core Principle

All products are overlays for the same intelligence:

```
Ascension AI (native intelligence core)
    ├── LifeOS (personal life operating system overlay)
    ├── HomeOS (household intelligence overlay)
    ├── Sprout (children/learning overlay)
    ├── FamilyOS (family enterprise overlay)
    └── Ascension AI (chat/API overlay)
```

## Product Overlays

### LifeOS
- **Scope**: Individual personal life
- **Data**: Quests, journal, streaks, 7 intelligence scores, identity, relationships
- **AP**: Ascension Partner serves the individual
- **AI Responsibilities**:
  - Generate daily quests based on energy state
  - Analyze journal entries
  - Calculate 7-domain intelligence scores
  - Provide proactive insights
  - Track streaks and XP
  - Support identity evolution

### HomeOS
- **Scope**: Household / co-parenting
- **Data**: Chores, shared resources, family schedules, home environment
- **AI Responsibilities**:
  - Coordinate household tasks
  - Manage shared schedules
  - Optimize home environment
  - Support co-parenting communication
  - Track shared goals

### Sprout
- **Scope**: Children / learning
- **Data**: Learning progress, skill development, growth milestones
- **AI Responsibilities**:
  - Create personalized learning paths
  - Generate age-appropriate content
  - Track development
  - Provide adaptive education
  - Support parent-child learning

### FamilyOS
- **Scope**: Family enterprise
- **Data**: Family relationships, businesses, shared finances, legacy
- **AI Responsibilities**:
  - Manage family relationships
  - Coordinate family businesses
  - Track generational goals
  - Support family decision-making
  - Preserve family knowledge

### Ascension AI
- **Scope**: Direct chat and API access
- **Data**: All user-permitted data across overlays
- **AI Responsibilities**:
  - Answer questions
  - Generate content
  - Execute tasks
  - Provide general intelligence
  - Surface capabilities from all other systems

## Data Flow

```
User Input / Sensor Data
    ↓
Product Overlay (LifeOS/HomeOS/Sprout/FamilyOS/AI)
    ↓
Vortex Connector
    ↓
Normalized Knowledge Object
    ↓
Ascension AI Intelligence Core
    ↓
Decision Physics
    ↓
CIE Surface Gate
    ↓
AP / Overlay Response
    ↓
User Action
    ↓
Outcome Tracking
    ↓
Improved Intelligence
```

## Replacement of Outside AI Providers

### Current Outside AI Providers Used by LifeOS
- OpenAI (via Polsia proxy) - quest gen, journal analysis, AI coach chat
- Other external AI services

### Replacement Gates
For each capability currently provided by outside AI, we must prove:
1. **Model loaded**: Native model is available and loadable
2. **Inference passes**: Model produces valid output
3. **Quality threshold**: Output meets minimum quality bar
4. **Latency acceptable**: Response time within practical window
5. **Context retention**: Multi-turn context maintained
6. **Safety compliance**: No leaks, hallucinations, or harmful output

### Replacement Status
See `scripts/replacement_contract_eval.py` for current evaluation.

**Current state**: All capabilities are architectural stubs. Outside AI fallback must remain enabled until each gate is proven with evidence.

## Shell-Specific Context

Each overlay sends only permission-scoped context to the AI core. The AI does not claim access to data not present in the request.

### Context Boundaries
- **LifeOS**: individual user data only
- **HomeOS**: household-level data with member permissions
- **Sprout**: child-specific data with parent consent
- **FamilyOS**: family enterprise data with role-based access
- **Ascension AI chat**: user-permitted cross-overlay data

## Integration Points

### From Overlays to AI
- Normalized knowledge objects
- Permission scopes
- Requested talent/intent
- User preferences
- Historical context

### From AI to Overlays
- Intelligence candidates
- Recommended actions
- Generated content
- Predictions and risks
- Explanations and confidence

## Enforcement

### Do Not Claim Active Until Proven
- A module file is not a proven capability
- A stub is not a replacement
- Only capabilities passing `replacement_contract_eval.py` can disable fallback

### Required Evidence
- Unit tests passing
- Live inference evidence
- Quality metrics
- Latency metrics
- User-facing verification
- Render deploy proof

## Next Steps

1. Train/load Ascension Candidate 3B (or larger)
2. Implement real inference for each capability
3. Run replacement contract evaluation
4. Provide evidence for each proven capability
5. Enable native-first routing for proven capabilities only
6. Keep outside fallback for unproven capabilities
7. Comment evidence in engineering coordination issue

