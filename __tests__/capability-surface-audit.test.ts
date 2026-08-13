import * as crypto from 'crypto';
import * as fs from 'fs';
import * as path from 'path';
import { getCapabilityById } from '../src/services/capability-registry';
import { routeNativeDomain } from '../src/services/native-domain-router';
import { modelRouter } from '../src/services/model-router';
import { getRequiredPermissions, PermissionStatus } from '../src/services/permission-engine';

type SurfaceClass = 'registered_only' | 'outside_provider' | 'specialized_deterministic' | 'model_backed_native';

const SCHEMA_VERSION = '1';
const SOURCE_FILES_TO_HASH = [
  'src/services/capability-registry.ts',
  'src/services/native-domain-router.ts',
  'src/services/model-router.ts',
  'src/services/permission-engine.ts',
];

interface IdDetail {
  surface: string;
  id: string;
  registered: boolean;
  class: SurfaceClass;
  flavor: 'canned' | 'stub' | 'missing' | 'permission_gate' | 'routed' | 'native_deterministic';
  no_permission_content_hash: string;
  gated_content_hash: string | null;
  has_permission_gate: boolean;
  routed_provider: string | null;
  uses_message: boolean;
  model_backed_native: boolean;
}

interface SurfaceDetail {
  surface: string;
  ids: string[];
  permission_boundaries: boolean;
  surface_class: SurfaceClass;
  blockers: string[];
}

export interface AuditReport {
  schema_version: string;
  source_hashes: Record<string, string>;
  replacement_ready: boolean;
  replacement_ready_blockers: string[];
  per_id: Record<string, IdDetail>;
  per_surface: Record<string, SurfaceDetail>;
}

const STUB_MARKER = 'stub: domain handler not yet specialized';
const TEST_MESSAGE = 'ascension-audit-canary';
const REPORT_PATH = path.resolve(__dirname, '..', 'evals', 'capability_surface_report.json');

const SURFACES: { surface: string; ids: string[]; permissionBoundaries: boolean }[] = [
  { surface: 'natural conversation', ids: ['ascension_chat'], permissionBoundaries: false },
  { surface: 'persistent memory / corrections', ids: ['ascension_living_memory', 'ascension_second_brain', 'ascension_living_context'], permissionBoundaries: false },
  { surface: 'schedule / calendar', ids: ['ascension_calendar_intelligence', 'ascension_appointments', 'ascension_time'], permissionBoundaries: false },
  { surface: 'tasks / quests', ids: ['ascension_task', 'ascension_adaptive_quest'], permissionBoundaries: false },
  { surface: 'finance / budget / grocery', ids: ['ascension_finance', 'ascension_budgeting', 'ascension_grocery_list'], permissionBoundaries: false },
  { surface: 'nutrition', ids: ['ascension_nutrition'], permissionBoundaries: false },
  { surface: 'workout / health', ids: ['ascension_workout', 'ascension_health'], permissionBoundaries: false },
  { surface: 'learning / course generation', ids: ['ascension_learning', 'ascension_knowledge_studio'], permissionBoundaries: false },
  { surface: 'career', ids: ['ascension_career'], permissionBoundaries: false },
  { surface: 'aspirations', ids: ['ascension_goals', 'ascension_milestones', 'ascension_dream_fund'], permissionBoundaries: false },
  { surface: 'creation / project workspaces', ids: ['ascension_creative', 'ascension_project', 'ascension_content_workspace'], permissionBoundaries: false },
  { surface: 'browser / web research', ids: ['web_browsing', 'ascension_research_assistant'], permissionBoundaries: false },
  { surface: 'relationships', ids: ['ascension_relationships', 'ascension_relationship_intelligence'], permissionBoundaries: false },
  { surface: 'FamilyOS / Sprout / Nexus permission boundaries', ids: ['ascension_home', 'ascension_sprout', 'ascension_family'], permissionBoundaries: true },
  { surface: 'self-care', ids: ['ascension_mindfulness', 'ascension_sleep_hygiene', 'ascension_journaling'], permissionBoundaries: false },
  { surface: 'astrology / numerology reflection', ids: ['ascension_astrology', 'ascension_horoscope', 'ascension_tarot'], permissionBoundaries: false },
  { surface: 'journal / reflection', ids: ['ascension_journaling', 'ascension_gratitude', 'ascension_visualization'], permissionBoundaries: false },
];

const EXPECTED_SURFACE_CLASSES: Record<string, SurfaceClass> = SURFACES.reduce(
  (acc) => ({ ...acc }),
  {} as Record<string, SurfaceClass>
);
for (const { surface } of SURFACES) {
  EXPECTED_SURFACE_CLASSES[surface] = 'registered_only';
}

function sha256(input: string | Buffer): string {
  return crypto.createHash('sha256').update(input).digest('hex');
}

function computeSourceHashes(): Record<string, string> {
  const hashes: Record<string, string> = {};
  for (const rel of SOURCE_FILES_TO_HASH) {
    const full = path.resolve(__dirname, '..', rel);
    hashes[rel] = sha256(fs.readFileSync(full));
  }
  return hashes;
}

function handlerUsesMessage(content: string): boolean {
  return content.includes(TEST_MESSAGE);
}

function grantedPermissions(id: string): Record<string, PermissionStatus> {
  const required = getRequiredPermissions(id);
  const granted: Record<string, PermissionStatus> = {};
  for (const scope of required) {
    granted[scope.id] = {
      id: scope.id,
      granted: true,
      granted_at: new Date().toISOString(),
    };
  }
  return granted;
}

async function classifyId(surface: string, id: string): Promise<IdDetail> {
  const cap = getCapabilityById(id);
  const registered = Boolean(cap && cap.id === id);
  const noPermissionRouted = routeNativeDomain(id, TEST_MESSAGE, {});
  const noPermissionContent = noPermissionRouted.content;
  const hasPermissionGate = getRequiredPermissions(id).length > 0;

  let gatedContent: string | null = null;
  if (hasPermissionGate) {
    const gatedRouted = routeNativeDomain(id, TEST_MESSAGE, grantedPermissions(id));
    gatedContent = gatedRouted.content;
  }

  const contentToClassify = gatedContent ?? noPermissionContent;

  let routedProvider: string | null = null;
  // Model-backed native execution requires actual runtime endpoint evidence this audit does not collect.
  const modelBackedNative = false;

  if (registered && cap) {
    try {
      const decision = await modelRouter.route(id, 'individual');
      routedProvider = decision.provider;
    } catch {
      routedProvider = 'unroutable';
    }
  }

  let className: SurfaceClass;
  let flavor: IdDetail['flavor'];

  if (!registered) {
    className = 'registered_only';
    flavor = 'missing';
  } else if (contentToClassify.includes(STUB_MARKER)) {
    className = 'registered_only';
    flavor = 'stub';
  } else if (!handlerUsesMessage(contentToClassify)) {
    // The permission gate is safety evidence, but the gated handler must still use the message to be a real binding.
    if (routedProvider && routedProvider !== 'ascension-native' && routedProvider !== 'unroutable') {
      className = 'outside_provider';
      flavor = 'routed';
    } else {
      className = 'registered_only';
      flavor = 'canned';
    }
  } else {
    className = 'specialized_deterministic';
    flavor = 'native_deterministic';
  }

  return {
    surface,
    id,
    registered,
    class: className,
    flavor,
    no_permission_content_hash: sha256(noPermissionContent),
    gated_content_hash: gatedContent ? sha256(gatedContent) : sha256(noPermissionContent),
    has_permission_gate: hasPermissionGate,
    routed_provider: routedProvider,
    uses_message: handlerUsesMessage(contentToClassify),
    model_backed_native: modelBackedNative,
  };
}

export async function generateCapabilitySurfaceReport(): Promise<AuditReport> {
  const perId: Record<string, IdDetail> = {};
  const perSurface: Record<string, SurfaceDetail> = {};

  for (const { surface, ids, permissionBoundaries } of SURFACES) {
    for (const id of ids) {
      perId[id] = await classifyId(surface, id);
    }

    const surfaceClasses = ids.map((id) => perId[id].class);
    let surfaceClass: SurfaceClass;
    if (surfaceClasses.includes('registered_only')) {
      surfaceClass = 'registered_only';
    } else if (surfaceClasses.includes('outside_provider')) {
      surfaceClass = 'outside_provider';
    } else if (surfaceClasses.includes('specialized_deterministic')) {
      surfaceClass = 'specialized_deterministic';
    } else {
      surfaceClass = 'model_backed_native';
    }

    const blockers: string[] = [];
    for (const id of ids) {
      const d = perId[id];
      if (d.class === 'registered_only') {
        blockers.push(`${id}: ${d.flavor}`);
      }
    }
    if (surfaceClass !== 'specialized_deterministic' && surfaceClass !== 'model_backed_native') {
      if (blockers.length === 0) {
        blockers.push('no native specialized/model-backed binding');
      }
    }

    perSurface[surface] = {
      surface,
      ids,
      permission_boundaries: permissionBoundaries,
      surface_class: surfaceClass,
      blockers,
    };
  }

  const blockers = Object.values(perSurface)
    .filter((s) => s.surface_class !== 'specialized_deterministic' && s.surface_class !== 'model_backed_native')
    .map((s) => s.surface);

  return {
    schema_version: SCHEMA_VERSION,
    source_hashes: computeSourceHashes(),
    replacement_ready: blockers.length === 0,
    replacement_ready_blockers: blockers,
    per_id: perId,
    per_surface: perSurface,
  };
}

describe('Ascension AI capability surface coverage', () => {
  const envBackup = {
    OPENAI_API_KEY: process.env.OPENAI_API_KEY,
    ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
    ASCENSION_NATIVE_ENABLED: process.env.ASCENSION_NATIVE_ENABLED,
  };

  let report: AuditReport;

  beforeAll(async () => {
    process.env.OPENAI_API_KEY = 'test-openai-key';
    process.env.ANTHROPIC_API_KEY = 'test-anthropic-key';
    process.env.ASCENSION_NATIVE_ENABLED = 'true';
    report = await generateCapabilitySurfaceReport();
  }, 60000);

  afterAll(() => {
    process.env.OPENAI_API_KEY = envBackup.OPENAI_API_KEY;
    process.env.ANTHROPIC_API_KEY = envBackup.ANTHROPIC_API_KEY;
    process.env.ASCENSION_NATIVE_ENABLED = envBackup.ASCENSION_NATIVE_ENABLED;

    fs.writeFileSync(REPORT_PATH, JSON.stringify(report, null, 2));
  });

  test('the report binds the current source bytes with schema_version and source_hashes', () => {
    expect(report.schema_version).toBe(SCHEMA_VERSION);
    for (const rel of SOURCE_FILES_TO_HASH) {
      expect(report.source_hashes[rel]).toBeDefined();
      expect(report.source_hashes[rel]).toMatch(/^[a-f0-9]{64}$/);
    }
  });

  test('replacement_ready is false because every requested surface is unproven', () => {
    expect(report.replacement_ready).toBe(false);
  });

  test('all requested surfaces are in the registered-only / unproven blocker list', () => {
    const expectedBlockers = SURFACES.map(({ surface }) => surface).sort();
    expect(report.replacement_ready_blockers.sort()).toEqual(expectedBlockers);
    expect(report.replacement_ready_blockers.length).toBe(expectedBlockers.length);
  });

  test('no requested surface is classified as proven native capability', () => {
    const proven = Object.values(report.per_surface).filter(
      (s) => s.surface_class === 'specialized_deterministic' || s.surface_class === 'model_backed_native'
    );
    expect(proven).toEqual([]);
  });

  test('permission-boundary capabilities have a safety gate but still a canned underlying handler', () => {
    const boundaryIds = SURFACES.filter((s) => s.permissionBoundaries).flatMap((s) => s.ids);
    for (const id of boundaryIds) {
      const detail = report.per_id[id];
      expect(detail.has_permission_gate).toBe(true);
      expect(detail.class).toBe('registered_only');
      expect(detail.flavor).toBe('canned');
    }
  });

  test('no id is incorrectly classified as model_backed_native without runtime evidence', () => {
    const modelBacked = Object.values(report.per_id).filter((d) => d.class === 'model_backed_native');
    expect(modelBacked).toEqual([]);
  });

  test('web_browsing is the only outside-provider fallback among requested ids', () => {
    const outside = Object.values(report.per_id).filter((d) => d.class === 'outside_provider');
    expect(outside.length).toBe(1);
    expect(outside[0].id).toBe('web_browsing');
  });

  for (const { surface } of SURFACES) {
    test(`${surface} has the expected coverage classification`, () => {
      const detail = report.per_surface[surface];
      expect(detail).toBeDefined();
      expect(detail.surface_class).toBe(EXPECTED_SURFACE_CLASSES[surface]);
    });
  }
});
