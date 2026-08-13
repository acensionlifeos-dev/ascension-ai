# Ascension Thesis Intelligence Contract

Ascension theses are living, inspectable syntheses of permissioned evidence. They are not hidden personality scores, diagnoses, destiny claims, or authority to act.

## Thesis layers

| Layer | Intelligence | Evidence boundary | Owner |
|---|---|---|---|
| Human Thesis | AP / LifeOS | One user's permission-scoped LifeOS evidence | The user |
| Sprout Growth Thesis | AP / Sprout | Child-centered evidence under a valid guardian authorization | The child, with authorized guardian controls |
| Home Thesis | NexusHome | Household facts and exact AP claims consented for NexusHome | Authorized household members |
| Family Thesis | NexusFamily / FamilyOS | FamilyOS facts and exact AP claims consented for NexusFamily | Authorized family governance |
| Global Product Thesis | Core / Founder controls | Minimum-size aggregate product analytics and cited public evidence | The B.E.I.N.G Group LLC authorized founder controls |

## AP-to-Nexus flow

1. AP builds a private Human Thesis from the authenticated user's context.
2. The user chooses exact thesis claims and their shared destination sections.
3. LifeOS records an explicit consent receipt.
4. `POST /v1/thesis/contribution` prepares a revocable, scope-limited packet. It never exports the raw Human Thesis.
5. NexusHome or NexusFamily validates and persists the packet.
6. `POST /v1/thesis` rebuilds the relevant shared thesis with sources, confidence, unknowns, conflicts, rejected contributions, and member coverage.

The Family Thesis is comprehensive only when every expected member has contributed, all expected sections have evidence, and no contradictions remain. Otherwise the API reports a partial thesis and identifies missing contributors or unresolved facts.

The Global Product Thesis never consumes any personal thesis or raw user row. Aggregate cohorts below the configured privacy threshold (never less than 20) are rejected. It may guide product improvements, partnerships, market research, funding, and company strategy, but every material decision requires founder review and the aggregate analytics use must be disclosed to users.

## Persistence and correction

Ascension AI is stateless at this boundary. The authenticated shell owns storage, consent, revocation, corrections, and audit receipts. Thesis IDs and claim IDs are stable hashes of the evidence packet so changed evidence produces a traceable revision. A thesis has no execution authority.

## Endpoints

- `POST /v1/thesis`: build `human`, `sprout`, `home`, or `family` thesis under its authorized shell.
- `POST /v1/thesis/contribution`: export exact Human Thesis claims to `nexus_home` or `nexus_family` after a validated consent receipt.
