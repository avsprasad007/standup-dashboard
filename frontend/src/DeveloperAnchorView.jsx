import React, { useState, useEffect } from 'react';
import {
  Users,
  Target,
  Briefcase,
  Bot,
  GraduationCap,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ArrowRight,
  Copy,
  Check,
  Plus,
  Edit3,
  Save,
  RotateCcw,
  Layers,
  Terminal,
  Calendar,
  MessageSquare,
  ChevronRight,
  Zap,
  ShieldCheck,
  BookOpen,
  Award,
} from 'lucide-react';

const STATUS_BADGES = {
  done: {
    label: 'Done / Verified',
    dark: 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60',
    light: 'bg-emerald-50 text-emerald-800 border-emerald-300',
  },
  ready_for_deploy: {
    label: 'Ready for Deploy',
    dark: 'bg-sky-950/80 text-sky-300 border-sky-700/60',
    light: 'bg-sky-50 text-sky-800 border-sky-300',
  },
  in_progress: {
    label: 'Active Iteration',
    dark: 'bg-indigo-950/80 text-indigo-300 border-indigo-700/60',
    light: 'bg-indigo-50 text-indigo-800 border-indigo-300',
  },
  planned: {
    label: 'Planned Next',
    dark: 'bg-amber-950/80 text-amber-300 border-amber-700/60',
    light: 'bg-amber-50 text-amber-800 border-amber-300',
  },
  needs_iteration: {
    label: 'Needs Owner Sync',
    dark: 'bg-rose-950/80 text-rose-300 border-rose-700/60',
    light: 'bg-rose-50 text-rose-800 border-rose-300',
  },
};

function getInitials(name) {
  return (name || '')
    .split(/\s+/)
    .slice(0, 2)
    .map((w) => w[0])
    .join('')
    .toUpperCase();
}

export default function DeveloperAnchorView({
  isDark,
  developerPage,
  allPeople = [],
  days = [],
  onNavigateDeveloper,
  onInspectCell,
  onCopyText,
  copiedId,
}) {
  const slug = developerPage?.slug || '';
  const storageKey = `nsoft_dev_anchor_v1_${slug}`;

  // Interactive persisted state for two-way outcome iterations, sync notes, and personal learning goals
  const [outcomes, setOutcomes] = useState([]);
  const [syncNotes, setSyncNotes] = useState('');
  const [checkedGoals, setCheckedGoals] = useState({});
  const [customGoals, setCustomGoals] = useState([]);
  const [newGoalText, setNewGoalText] = useState('');
  const [editingOutcomeId, setEditingOutcomeId] = useState(null);
  const [addingOutcome, setAddingOutcome] = useState(false);
  const [newOutcomeDraft, setNewOutcomeDraft] = useState({
    track: '',
    v1_reported: '',
    v2_owner_sync: '',
    v3_business_outcome: '',
    status: 'in_progress',
  });

  useEffect(() => {
    if (!developerPage) return;
    const savedRaw = localStorage.getItem(storageKey);
    if (savedRaw) {
      try {
        const parsed = JSON.parse(savedRaw);
        setOutcomes(parsed.outcomes || developerPage.outcome_iterations || []);
        setSyncNotes(parsed.syncNotes || '');
        setCheckedGoals(parsed.checkedGoals || {});
        setCustomGoals(parsed.customGoals || []);
        return;
      } catch {
        // Fallback to default server payload
      }
    }
    setOutcomes(developerPage.outcome_iterations || []);
    setSyncNotes('');
    setCheckedGoals({});
    setCustomGoals([]);
  }, [slug, developerPage, storageKey]);

  const persistState = (nextOutcomes, nextNotes, nextChecked, nextCustomGoals) => {
    try {
      localStorage.setItem(
        storageKey,
        JSON.stringify({
          outcomes: nextOutcomes,
          syncNotes: nextNotes,
          checkedGoals: nextChecked,
          customGoals: nextCustomGoals,
        })
      );
    } catch {
      // Ignore storage quota errors
    }
  };

  if (!developerPage) return null;

  const {
    person,
    headline,
    product_spaces = [],
    utilities = [],
    telemetry = {},
    sync_owners = [],
    business_alignment = {},
    ai_agent_usage = {},
    learning_dimensions = {},
    pva_history = [],
    mapped_tasks = [],
    daily_reports = {},
  } = developerPage;

  const scores = learning_dimensions.scores || {
    technical_depth: 80,
    domain_mastery: 80,
    engineering_craft: 80,
    communication_ownership: 75,
  };
  const dimNotes = learning_dimensions.dimension_notes || {};
  const defaultGoals = learning_dimensions.growth_goals || [];
  const allGoals = [...defaultGoals, ...customGoals];

  const handleUpdateOutcomeField = (id, field, value) => {
    const next = outcomes.map((o) => (o.id === id ? { ...o, [field]: value } : o));
    setOutcomes(next);
    persistState(next, syncNotes, checkedGoals, customGoals);
  };

  const handleAddOutcome = () => {
    if (!newOutcomeDraft.track.trim()) return;
    const created = {
      id: `${slug}-out-${Date.now()}`,
      track: newOutcomeDraft.track.trim(),
      v1_reported: newOutcomeDraft.v1_reported.trim() || 'New workstream initiated in sync.',
      v2_owner_sync:
        newOutcomeDraft.v2_owner_sync.trim() ||
        'Define technical verification & edge-case contract between Developer and Module Lead.',
      v3_business_outcome:
        newOutcomeDraft.v3_business_outcome.trim() ||
        'Measurable production outcome aligned with utility SLA.',
      owners: [person.name, 'Sumukh Hegde', 'Prajwal D A', 'Prasad Amara'],
      status: newOutcomeDraft.status,
    };
    const next = [...outcomes, created];
    setOutcomes(next);
    persistState(next, syncNotes, checkedGoals, customGoals);
    setNewOutcomeDraft({
      track: '',
      v1_reported: '',
      v2_owner_sync: '',
      v3_business_outcome: '',
      status: 'in_progress',
    });
    setAddingOutcome(false);
  };

  const handleResetCharter = () => {
    localStorage.removeItem(storageKey);
    setOutcomes(developerPage.outcome_iterations || []);
    setSyncNotes('');
    setCheckedGoals({});
    setCustomGoals([]);
  };

  const handleToggleGoal = (idx) => {
    const next = { ...checkedGoals, [idx]: !checkedGoals[idx] };
    setCheckedGoals(next);
    persistState(outcomes, syncNotes, next, customGoals);
  };

  const handleAddCustomGoal = (e) => {
    e.preventDefault();
    if (!newGoalText.trim()) return;
    const nextCustom = [...customGoals, newGoalText.trim()];
    setCustomGoals(nextCustom);
    setNewGoalText('');
    persistState(outcomes, syncNotes, checkedGoals, nextCustom);
  };

  const buildSyncSummaryText = () => {
    const lines = [
      `# 1:1 Growth & Outcome Sync Anchor — ${person.name} (/${slug})`,
      `Role: ${person.role} | Focus: ${headline}`,
      `6-Day Telemetry: ${telemetry.days_reported}/${telemetry.total_days} Reports Sent (${telemetry.attendance_pct}%) | Learnings: ${telemetry.green_count}G · ${telemetry.amber_count}A · ${telemetry.red_count}R`,
      ``,
      `## 1. Two-Way Iterative Outcomes (Developer ↔ Sumukh ↔ Module Leads ↔ Prasad)`,
      ...outcomes.map(
        (o, idx) =>
          `${idx + 1}. [${(STATUS_BADGES[o.status]?.label || o.status).toUpperCase()}] ${o.track}\n   • v1 (Reported): ${o.v1_reported}\n   • v2 (Tech Sync): ${o.v2_owner_sync}\n   • v3 (Business Outcome): ${o.v3_business_outcome}`
      ),
      ``,
      `## 2. Business Alignment`,
      `Summary: ${business_alignment.strategic_summary || ''}`,
      ...(business_alignment.value_chains || []).map(
        (vc) => `- ${vc.deliverable} (${vc.client}): ${vc.business_impact} [KPI: ${vc.kpi}]`
      ),
      ``,
      `## 3. Deeper AI Agents Usage`,
      `Current: ${ai_agent_usage.current_stage} → Target: ${ai_agent_usage.target_stage}`,
      ...(ai_agent_usage.playbooks || []).map((pb) => `- Playbook: ${pb.title} — ${pb.context}`),
      ``,
      `## 4. Personal Learning Goals (All Dimensions)`,
      ...allGoals.map((g, i) => `- [${checkedGoals[i] ? 'x' : ' '}] ${g}`),
    ];
    if (syncNotes.trim()) {
      lines.push(``, `## Shared Discussion Notes & Next Actions`, syncNotes.trim());
    }
    return lines.join('\n');
  };

  return (
    <div className="space-y-6 pb-10">
      {/* =====================================================================
          TOP DEVELOPER SWITCHER BAR (`/<developer-slug>` Navigation)
      ===================================================================== */}
      <div
        className={`rounded-2xl border p-3.5 flex flex-wrap items-center justify-between gap-3 ${
          isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-[11px] font-bold uppercase tracking-wider opacity-60 mr-1.5 flex items-center gap-1.5">
            <Users className="w-3.5 h-3.5 text-indigo-500" /> Developer Anchor Pages:
          </span>
          {allPeople.map((p) => {
            const pSlug = p.slug || p.name.toLowerCase().replace(/\s+/g, '-');
            const isActive = pSlug === slug;
            return (
              <a
                key={p.email}
                href={`/${pSlug}`}
                onClick={(e) => {
                  e.preventDefault();
                  onNavigateDeveloper(`/${pSlug}`);
                }}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition flex items-center gap-1.5 ${
                  isActive
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm'
                    : isDark
                    ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800 hover:text-white'
                    : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                }`}
              >
                <span
                  className={`w-4 h-4 rounded-full text-[9px] font-bold flex items-center justify-center ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : isDark
                      ? 'bg-slate-800 text-indigo-300'
                      : 'bg-indigo-100 text-indigo-700'
                  }`}
                >
                  {getInitials(p.name)}
                </span>
                <span>{p.name.split(' ')[0]}</span>
              </a>
            );
          })}
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[11px] font-mono opacity-60 hidden xl:inline">
            URL: <strong>/{slug}</strong>
          </span>
          <button
            onClick={() => onCopyText(buildSyncSummaryText(), `sync-brief-${slug}`)}
            className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-xs"
          >
            {copiedId === `sync-brief-${slug}` ? (
              <>
                <Check className="w-3.5 h-3.5" />
                <span>Copied 1:1 Sync Charter!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy 1:1 Sync Charter</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* =====================================================================
          DEVELOPER HERO BANNER & 4-PILLAR TELEMETRY STRIP
      ===================================================================== */}
      <div
        className={`rounded-2xl border p-6 relative overflow-hidden ${
          isDark
            ? 'bg-gradient-to-br from-slate-900 via-slate-900/95 to-indigo-950/40 border-slate-800'
            : 'bg-gradient-to-br from-white via-slate-50/70 to-indigo-50/40 border-slate-200 shadow-sm'
        }`}
      >
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 text-white font-bold text-lg flex items-center justify-center shadow-lg shrink-0">
              {getInitials(person.name)}
            </div>
            <div className="space-y-1.5">
              <div className="flex flex-wrap items-center gap-2.5">
                <h2 className="text-xl font-bold tracking-tight">{person.name}</h2>
                <span
                  className={`px-2.5 py-0.5 rounded-full text-xs font-mono border ${
                    isDark
                      ? 'bg-indigo-950/80 text-indigo-300 border-indigo-700/60'
                      : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                  }`}
                >
                  /{slug}
                </span>
                <span className="text-xs font-mono opacity-60">{person.email}</span>
              </div>
              <p className="text-sm font-semibold text-indigo-500">{headline}</p>
              <div className="flex flex-wrap items-center gap-1.5 pt-1">
                {product_spaces.map((ps) => (
                  <span
                    key={ps}
                    className={`px-2 py-0.5 rounded-md text-[11px] font-bold border ${
                      isDark
                        ? 'bg-emerald-950/70 text-emerald-300 border-emerald-800/60'
                        : 'bg-emerald-50 text-emerald-800 border-emerald-200'
                    }`}
                  >
                    Product: {ps}
                  </span>
                ))}
                {utilities.map((u) => (
                  <span
                    key={u}
                    className={`px-2 py-0.5 rounded-md text-[11px] font-medium border ${
                      isDark
                        ? 'bg-slate-800/90 text-slate-300 border-slate-700'
                        : 'bg-white text-slate-700 border-slate-200'
                    }`}
                  >
                    {u}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* 4-Pillar Quick Scorecards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 shrink-0">
            <div
              className={`p-3 rounded-xl border ${
                isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-white border-slate-200'
              }`}
            >
              <div className="text-[10px] font-bold uppercase tracking-wider opacity-60">
                1. Two-Way Outcomes
              </div>
              <div className="text-lg font-bold mt-0.5 text-indigo-500">
                {outcomes.length} Tracks
              </div>
              <div className="text-[11px] opacity-70">{sync_owners.length} Sync Owners</div>
            </div>

            <div
              className={`p-3 rounded-xl border ${
                isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-white border-slate-200'
              }`}
            >
              <div className="text-[10px] font-bold uppercase tracking-wider opacity-60">
                2. Plan Continuity
              </div>
              <div className="text-lg font-bold mt-0.5 text-emerald-500">
                {telemetry.days_reported}/{telemetry.total_days} Days
              </div>
              <div className="text-[11px] opacity-70">
                {telemetry.aligned_transitions} Aligned · {telemetry.carryover_transitions} Carryover
              </div>
            </div>

            <div
              className={`p-3 rounded-xl border ${
                isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-white border-slate-200'
              }`}
            >
              <div className="text-[10px] font-bold uppercase tracking-wider opacity-60">
                3. AI Agent Stage
              </div>
              <div className="text-lg font-bold mt-0.5 text-purple-500">
                {(ai_agent_usage.current_stage || 'L2').split(':')[0]} →{' '}
                {(ai_agent_usage.target_stage || 'L3').split(':')[0]}
              </div>
              <div className="text-[11px] opacity-70">
                {(ai_agent_usage.playbooks || []).length} Custom Playbooks
              </div>
            </div>

            <div
              className={`p-3 rounded-xl border ${
                isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-white border-slate-200'
              }`}
            >
              <div className="text-[10px] font-bold uppercase tracking-wider opacity-60">
                4. Learning Signal
              </div>
              <div className="text-lg font-bold mt-0.5">
                <span className="text-emerald-500">{telemetry.green_count}G</span> ·{' '}
                <span className="text-amber-500">{telemetry.amber_count}A</span> ·{' '}
                <span className="text-rose-500">{telemetry.red_count}R</span>
              </div>
              <div className="text-[11px] opacity-70">4D Growth Rubric</div>
            </div>
          </div>
        </div>
      </div>

      {/* =====================================================================
          PILLAR 1: ITERATIVELY DEFINE OUTCOMES IN A TWO-WAY SYNC BETWEEN MULTIPLE OWNERS
      ===================================================================== */}
      <section
        className={`rounded-2xl border p-6 space-y-5 ${
          isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-wrap items-center justify-between gap-3 border-b pb-4 border-slate-500/20">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-500/15 border border-indigo-500/30 flex items-center justify-center text-indigo-500">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-500">
                  Pillar 1 · Multi-Owner Co-Design
                </span>
              </div>
              <h3 className="text-base font-bold">
                Iteratively Define Outcomes in a Two-Way Sync Between Multiple Owners
              </h3>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setAddingOutcome(!addingOutcome)}
              className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add Outcome Track</span>
            </button>
            <button
              onClick={handleResetCharter}
              className={`px-2.5 py-1.5 rounded-xl border text-xs flex items-center gap-1 cursor-pointer ${
                isDark
                  ? 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200'
                  : 'bg-slate-50 border-slate-200 text-slate-600 hover:text-slate-900'
              }`}
              title="Reset outcome edits to baseline"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          </div>
        </div>

        {/* Multi-Owner Sync Loop Strip */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {sync_owners.map((owner, idx) => (
            <div
              key={idx}
              className={`p-3.5 rounded-xl border flex flex-col justify-between ${
                isDark ? 'bg-slate-950/70 border-slate-800/90' : 'bg-slate-50/80 border-slate-200'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-bold">{owner.name}</span>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${
                      idx === 0
                        ? isDark
                          ? 'bg-indigo-950 text-indigo-300 border-indigo-800'
                          : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                        : isDark
                        ? 'bg-slate-900 text-slate-300 border-slate-700'
                        : 'bg-white text-slate-700 border-slate-200'
                    }`}
                  >
                    {owner.role}
                  </span>
                </div>
                <p className="text-xs opacity-80 mt-2 leading-relaxed">{owner.focus}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Add New Outcome Form */}
        {addingOutcome && (
          <div
            className={`p-4 rounded-xl border space-y-3 ${
              isDark ? 'bg-indigo-950/20 border-indigo-500/40' : 'bg-indigo-50/50 border-indigo-200'
            }`}
          >
            <div className="text-xs font-bold uppercase tracking-wider text-indigo-500">
              New Iterative Outcome Track
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <input
                type="text"
                value={newOutcomeDraft.track}
                onChange={(e) => setNewOutcomeDraft({ ...newOutcomeDraft, track: e.target.value })}
                placeholder="Outcome Track Title (e.g., Automated GESCOM Differential Restore Verification)"
                className={`px-3 py-2 rounded-lg border text-xs ${
                  isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                }`}
              />
              <select
                value={newOutcomeDraft.status}
                onChange={(e) => setNewOutcomeDraft({ ...newOutcomeDraft, status: e.target.value })}
                className={`px-3 py-2 rounded-lg border text-xs ${
                  isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                }`}
              >
                <option value="in_progress">Active Iteration</option>
                <option value="ready_for_deploy">Ready for Deploy</option>
                <option value="needs_iteration">Needs Owner Sync</option>
                <option value="planned">Planned Next</option>
                <option value="done">Done / Verified</option>
              </select>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <textarea
                rows={2}
                value={newOutcomeDraft.v1_reported}
                onChange={(e) =>
                  setNewOutcomeDraft({ ...newOutcomeDraft, v1_reported: e.target.value })
                }
                placeholder="Iteration 1: Developer's current reported task..."
                className={`p-2.5 rounded-lg border text-xs ${
                  isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                }`}
              />
              <textarea
                rows={2}
                value={newOutcomeDraft.v2_owner_sync}
                onChange={(e) =>
                  setNewOutcomeDraft({ ...newOutcomeDraft, v2_owner_sync: e.target.value })
                }
                placeholder="Iteration 2: Tech & Module Lead sync contract..."
                className={`p-2.5 rounded-lg border text-xs ${
                  isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                }`}
              />
              <textarea
                rows={2}
                value={newOutcomeDraft.v3_business_outcome}
                onChange={(e) =>
                  setNewOutcomeDraft({ ...newOutcomeDraft, v3_business_outcome: e.target.value })
                }
                placeholder="Iteration 3: Measurable business & utility outcome..."
                className={`p-2.5 rounded-lg border text-xs ${
                  isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                }`}
              />
            </div>
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setAddingOutcome(false)}
                className="px-3 py-1.5 rounded-lg text-xs opacity-70 hover:opacity-100 cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleAddOutcome}
                className="px-4 py-1.5 rounded-lg bg-indigo-600 text-white text-xs font-semibold cursor-pointer"
              >
                Save Outcome Track
              </button>
            </div>
          </div>
        )}

        {/* 3-Stage Iterative Outcome Evolution Cards */}
        <div className="space-y-4">
          {outcomes.map((out) => {
            const st = STATUS_BADGES[out.status] || STATUS_BADGES.in_progress;
            const isEditing = editingOutcomeId === out.id;

            return (
              <div
                key={out.id}
                className={`rounded-2xl border p-4 space-y-3.5 transition ${
                  isDark
                    ? 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                    : 'bg-white border-slate-200 shadow-2xs'
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="font-bold text-sm">{out.track}</span>
                    <select
                      value={out.status}
                      onChange={(e) => handleUpdateOutcomeField(out.id, 'status', e.target.value)}
                      className={`px-2.5 py-0.5 rounded-full text-[11px] font-semibold border cursor-pointer ${
                        isDark ? st.dark : st.light
                      }`}
                    >
                      {Object.entries(STATUS_BADGES).map(([k, v]) => (
                        <option key={k} value={k} className="bg-slate-900 text-white">
                          {v.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-1 text-[11px] opacity-70">
                      <span>Owners:</span>
                      {(out.owners || []).map((ow) => (
                        <span
                          key={ow}
                          className={`px-1.5 py-0.5 rounded text-[10px] font-medium border ${
                            isDark
                              ? 'bg-slate-900 border-slate-800 text-slate-300'
                              : 'bg-slate-100 border-slate-200 text-slate-700'
                          }`}
                        >
                          {ow.split(' ')[0]}
                        </span>
                      ))}
                    </div>
                    <button
                      onClick={() => setEditingOutcomeId(isEditing ? null : out.id)}
                      className={`px-2.5 py-1 rounded-lg border text-xs flex items-center gap-1 cursor-pointer ${
                        isEditing
                          ? 'bg-emerald-600 text-white border-emerald-500'
                          : isDark
                          ? 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-800'
                          : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                      }`}
                    >
                      {isEditing ? (
                        <>
                          <Save className="w-3 h-3" /> Done
                        </>
                      ) : (
                        <>
                          <Edit3 className="w-3 h-3" /> Edit Iteration
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* 3 Columns: Iteration 1 → Iteration 2 → Iteration 3 */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
                  {/* Iteration 1 */}
                  <div
                    className={`p-3.5 rounded-xl border ${
                      isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-slate-50/70 border-slate-200'
                    }`}
                  >
                    <div className="text-[10px] font-bold uppercase tracking-wider text-amber-500 mb-1">
                      Iteration 1 · Reported Task (Developer)
                    </div>
                    {isEditing ? (
                      <textarea
                        rows={3}
                        value={out.v1_reported}
                        onChange={(e) =>
                          handleUpdateOutcomeField(out.id, 'v1_reported', e.target.value)
                        }
                        className={`w-full p-2 rounded border text-xs ${
                          isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                        }`}
                      />
                    ) : (
                      <p className="text-xs leading-relaxed opacity-90">{out.v1_reported}</p>
                    )}
                  </div>

                  {/* Iteration 2 */}
                  <div
                    className={`p-3.5 rounded-xl border ${
                      isDark
                        ? 'bg-indigo-950/25 border-indigo-800/50'
                        : 'bg-indigo-50/40 border-indigo-200'
                    }`}
                  >
                    <div className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 mb-1">
                      Iteration 2 · Two-Way Tech Sync (Sumukh / Leads)
                    </div>
                    {isEditing ? (
                      <textarea
                        rows={3}
                        value={out.v2_owner_sync}
                        onChange={(e) =>
                          handleUpdateOutcomeField(out.id, 'v2_owner_sync', e.target.value)
                        }
                        className={`w-full p-2 rounded border text-xs ${
                          isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                        }`}
                      />
                    ) : (
                      <p className="text-xs leading-relaxed opacity-95">{out.v2_owner_sync}</p>
                    )}
                  </div>

                  {/* Iteration 3 */}
                  <div
                    className={`p-3.5 rounded-xl border ${
                      isDark
                        ? 'bg-emerald-950/25 border-emerald-800/50'
                        : 'bg-emerald-50/40 border-emerald-200'
                    }`}
                  >
                    <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-500 mb-1">
                      Iteration 3 · Agreed Business Outcome (Prasad / SLA)
                    </div>
                    {isEditing ? (
                      <textarea
                        rows={3}
                        value={out.v3_business_outcome}
                        onChange={(e) =>
                          handleUpdateOutcomeField(out.id, 'v3_business_outcome', e.target.value)
                        }
                        className={`w-full p-2 rounded border text-xs ${
                          isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                        }`}
                      />
                    ) : (
                      <p className="text-xs leading-relaxed font-medium">{out.v3_business_outcome}</p>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Live Discussion Scratchpad / Two-Way Sync Notes */}
        <div
          className={`p-4 rounded-xl border ${
            isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-slate-50 border-slate-200'
          }`}
        >
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs font-bold uppercase tracking-wider text-indigo-500 flex items-center gap-1.5">
              <MessageSquare className="w-3.5 h-3.5" /> Live 1:1 &amp; Multi-Owner Sync Notes (Auto-Saved Locally)
            </label>
            <span className="text-[11px] opacity-60">
              Included when you click "Copy 1:1 Sync Charter"
            </span>
          </div>
          <textarea
            rows={2}
            value={syncNotes}
            onChange={(e) => {
              setSyncNotes(e.target.value);
              persistState(outcomes, e.target.value, checkedGoals, customGoals);
            }}
            placeholder={`Capture decisions, blockers, or next-sprint commitments agreed with ${person.name}, Sumukh, Prajwal, Dharmaraj, and Prasad...`}
            className={`w-full p-3 rounded-lg border text-xs leading-relaxed focus:outline-none focus:border-indigo-500 ${
              isDark
                ? 'bg-slate-900 border-slate-800 text-slate-100 placeholder-slate-500'
                : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'
            }`}
          />
        </div>
      </section>

      {/* =====================================================================
          PILLAR 2: ALIGNMENT WITH BUSINESS & PLAN-VS-ACTUAL CONTINUITY
      ===================================================================== */}
      <section
        className={`rounded-2xl border p-6 space-y-5 ${
          isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-wrap items-center justify-between gap-3 border-b pb-4 border-slate-500/20">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-500">
              <Briefcase className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-500">
                Pillar 2 · Business &amp; Utility SLA Impact
              </span>
              <h3 className="text-base font-bold">
                Alignment with Business — Code-to-Customer Value &amp; Plan Continuity
              </h3>
            </div>
          </div>
        </div>

        <p className="text-xs leading-relaxed opacity-90">
          {business_alignment.strategic_summary}
        </p>

        {/* Code-to-Business Value Chain Table */}
        <div className="overflow-x-auto rounded-xl border border-slate-500/20">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr
                className={`border-b text-[11px] uppercase tracking-wider ${
                  isDark ? 'bg-slate-950/90 border-slate-800 text-slate-400' : 'bg-slate-100 border-slate-200 text-slate-600'
                }`}
              >
                <th className="py-2.5 px-4">Engineering Deliverable</th>
                <th className="py-2.5 px-4">Technical Artifact (Code / SQL / DLMS)</th>
                <th className="py-2.5 px-4">Utility / Client</th>
                <th className="py-2.5 px-4">Business &amp; Operational Impact</th>
                <th className="py-2.5 px-4">Target Outcome KPI</th>
              </tr>
            </thead>
            <tbody className={`divide-y ${isDark ? 'divide-slate-800' : 'divide-slate-200'}`}>
              {(business_alignment.value_chains || []).map((vc, i) => (
                <tr key={i} className={isDark ? 'hover:bg-slate-950/40' : 'hover:bg-slate-50'}>
                  <td className="py-3 px-4 font-bold">{vc.deliverable}</td>
                  <td className="py-3 px-4 font-mono text-[11px] text-indigo-400">{vc.artifact}</td>
                  <td className="py-3 px-4 font-semibold">{vc.client}</td>
                  <td className="py-3 px-4 leading-relaxed opacity-90">{vc.business_impact}</td>
                  <td className="py-3 px-4">
                    <span
                      className={`inline-block px-2.5 py-1 rounded-lg text-[11px] font-semibold border ${
                        isDark
                          ? 'bg-emerald-950/80 text-emerald-300 border-emerald-800/60'
                          : 'bg-emerald-50 text-emerald-800 border-emerald-200'
                      }`}
                    >
                      {vc.kpi}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* 5-Transition Plan-vs-Actual Continuity Strip */}
        <div className="space-y-2.5 pt-2">
          <div className="text-xs font-bold uppercase tracking-wider opacity-70">
            6-Day Plan-to-Actual Execution Continuity ({person.name})
          </div>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
            {pva_history.map((item) => {
              const badgeColor =
                item.status === 'aligned'
                  ? isDark
                    ? 'border-emerald-800/60 bg-emerald-950/30 text-emerald-300'
                    : 'border-emerald-200 bg-emerald-50 text-emerald-900'
                  : item.status === 'carryover'
                  ? isDark
                    ? 'border-sky-800/60 bg-sky-950/30 text-sky-300'
                    : 'border-sky-200 bg-sky-50 text-sky-900'
                  : item.status === 'pivoted'
                  ? isDark
                    ? 'border-amber-800/60 bg-amber-950/30 text-amber-300'
                    : 'border-amber-200 bg-amber-50 text-amber-900'
                  : isDark
                  ? 'border-rose-800/60 bg-rose-950/30 text-rose-300'
                  : 'border-rose-200 bg-rose-50 text-rose-900';

              return (
                <div
                  key={item.id}
                  onClick={() => item.curr_cell && onInspectCell(item.curr_cell)}
                  className={`p-3 rounded-xl border flex flex-col justify-between cursor-pointer transition hover:scale-[1.01] ${badgeColor}`}
                >
                  <div>
                    <div className="flex items-center justify-between text-[11px] font-mono opacity-80">
                      <span>
                        {item.day_prev.slice(5)} → {item.day_curr.slice(5)}
                      </span>
                      <span className="uppercase font-bold">{item.status}</span>
                    </div>
                    <div className="text-xs font-bold mt-1">{item.badge}</div>
                    <p className="text-[11px] opacity-85 mt-1.5 leading-relaxed line-clamp-4">
                      {item.commentary}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* =====================================================================
          PILLAR 3: DEEPER AI AGENTS' USAGE & ROLE-SPECIFIC PLAYBOOKS
      ===================================================================== */}
      <section
        className={`rounded-2xl border p-6 space-y-5 ${
          isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-wrap items-center justify-between gap-3 border-b pb-4 border-slate-500/20">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-400">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-purple-400">
                Pillar 3 · Agentic Engineering Leverage
              </span>
              <h3 className="text-base font-bold">
                Deeper AI Agents' Usage — Maturity Progression &amp; Copy-Ready Playbooks
              </h3>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span
              className={`px-3 py-1 rounded-full font-semibold border ${
                isDark
                  ? 'bg-slate-950 border-slate-800 text-slate-300'
                  : 'bg-slate-100 border-slate-200 text-slate-700'
              }`}
            >
              Today: <strong>{ai_agent_usage.current_stage}</strong>
            </span>
            <ArrowRight className="w-4 h-4 text-purple-400" />
            <span
              className={`px-3 py-1 rounded-full font-semibold border ${
                isDark
                  ? 'bg-purple-950/80 border-purple-700/60 text-purple-200'
                  : 'bg-purple-50 border-purple-200 text-purple-800'
              }`}
            >
              Target: <strong>{ai_agent_usage.target_stage}</strong>
            </span>
          </div>
        </div>

        <div
          className={`p-4 rounded-xl border text-xs leading-relaxed ${
            isDark
              ? 'bg-purple-950/20 border-purple-800/50 text-purple-100'
              : 'bg-purple-50/60 border-purple-200 text-purple-950'
          }`}
        >
          <span className="font-bold uppercase tracking-wider text-purple-400 mr-2">
            AI Telemetry Observation:
          </span>
          {ai_agent_usage.observation}
        </div>

        {/* Copyable Role-Specific AI Agent Playbooks */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {(ai_agent_usage.playbooks || []).map((pb, idx) => {
            const copyKey = `pb-${slug}-${idx}`;
            return (
              <div
                key={idx}
                className={`rounded-xl border p-4 flex flex-col justify-between space-y-3 ${
                  isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-slate-50 border-slate-200'
                }`}
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-bold flex items-center gap-1.5 text-indigo-400">
                      <Sparkles className="w-3.5 h-3.5" />
                      {pb.title}
                    </span>
                    <button
                      onClick={() => onCopyText(pb.prompt, copyKey)}
                      className="px-2.5 py-1 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-[11px] font-semibold flex items-center gap-1 cursor-pointer shrink-0"
                    >
                      {copiedId === copyKey ? (
                        <>
                          <Check className="w-3 h-3" /> Copied Prompt
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3" /> Copy Agent Prompt
                        </>
                      )}
                    </button>
                  </div>
                  <p className="text-[11px] opacity-75">{pb.context}</p>
                  <pre
                    className={`p-3 rounded-lg border font-mono text-[11px] whitespace-pre-wrap leading-relaxed ${
                      isDark
                        ? 'bg-slate-900 border-slate-800 text-slate-200'
                        : 'bg-white border-slate-200 text-slate-800'
                    }`}
                  >
                    {pb.prompt}
                  </pre>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* =====================================================================
          PILLAR 4: ENHANCED PERSONAL LEARNING FROM ALL DIMENSIONS
      ===================================================================== */}
      <section
        className={`rounded-2xl border p-6 space-y-5 ${
          isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-wrap items-center justify-between gap-3 border-b pb-4 border-slate-500/20">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-500">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-amber-500">
                Pillar 4 · 360° Engineering Growth
              </span>
              <h3 className="text-base font-bold">
                Enhanced Personal Learning from All Dimensions (Technical · Domain · Craft · Ownership)
              </h3>
            </div>
          </div>
        </div>

        {/* 4-Dimensional Learning Rubric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            {
              key: 'technical_depth',
              label: '1. Technical & Systems Depth',
              color: 'bg-indigo-500',
              text: 'text-indigo-400',
            },
            {
              key: 'domain_mastery',
              label: '2. Utility Domain Mastery',
              color: 'bg-emerald-500',
              text: 'text-emerald-400',
            },
            {
              key: 'engineering_craft',
              label: '3. Craft, Testing & Parity',
              color: 'bg-sky-500',
              text: 'text-sky-400',
            },
            {
              key: 'communication_ownership',
              label: '4. Communication & Signal',
              color: 'bg-amber-500',
              text: 'text-amber-400',
            },
          ].map((dim) => {
            const val = scores[dim.key] || 75;
            return (
              <div
                key={dim.key}
                className={`p-4 rounded-xl border space-y-2.5 ${
                  isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-slate-50 border-slate-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold">{dim.label}</span>
                  <span className={`text-sm font-mono font-bold ${dim.text}`}>{val}/100</span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-500/20 overflow-hidden">
                  <div className={`h-full rounded-full ${dim.color}`} style={{ width: `${val}%` }} />
                </div>
                <p className="text-xs opacity-80 leading-relaxed">{dimNotes[dim.key]}</p>
              </div>
            );
          })}
        </div>

        {/* Before vs. 10x Upgraded Learning Reflections + Next-Sprint Learning Commitments */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Left 7 Cols: Reflection Upgrade Examples */}
          <div className="lg:col-span-7 space-y-3">
            <div className="text-xs font-bold uppercase tracking-wider opacity-70">
              Standup Learning Upgrade — From Generic Activity to Architectural Insight
            </div>
            {(learning_dimensions.reflection_upgrades || []).map((ru, i) => (
              <div
                key={i}
                className={`p-4 rounded-xl border space-y-3 ${
                  isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-slate-50 border-slate-200'
                }`}
              >
                <div className="text-[11px] font-mono opacity-60"> Standup Date: {ru.day}</div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div
                    className={`p-3 rounded-lg border text-xs ${
                      isDark
                        ? 'bg-amber-950/20 border-amber-800/50 text-amber-200'
                        : 'bg-amber-50 border-amber-200 text-amber-900'
                    }`}
                  >
                    <div className="text-[10px] font-bold uppercase tracking-wider text-amber-500 mb-1">
                      What Was Written
                    </div>
                    "{ru.original}"
                  </div>
                  <div
                    className={`p-3 rounded-lg border text-xs ${
                      isDark
                        ? 'bg-emerald-950/25 border-emerald-800/60 text-emerald-200'
                        : 'bg-emerald-50 border-emerald-200 text-emerald-900'
                    }`}
                  >
                    <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-500 mb-1">
                      Multi-Dimensional Upgrade
                    </div>
                    "{ru.upgraded}"
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Right 5 Cols: Interactive Personal Growth Checklist */}
          <div
            className={`lg:col-span-5 p-4 rounded-xl border flex flex-col justify-between space-y-4 ${
              isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-slate-50 border-slate-200'
            }`}
          >
            <div className="space-y-3">
              <div className="text-xs font-bold uppercase tracking-wider text-amber-500">
                Agreed Personal Learning Commitments
              </div>
              <div className="space-y-2">
                {allGoals.map((g, idx) => (
                  <label
                    key={idx}
                    className={`p-2.5 rounded-lg border flex items-start gap-2.5 cursor-pointer text-xs leading-relaxed ${
                      checkedGoals[idx]
                        ? isDark
                          ? 'bg-emerald-950/30 border-emerald-800/50 line-through opacity-70'
                          : 'bg-emerald-50 border-emerald-200 line-through opacity-70'
                        : isDark
                        ? 'bg-slate-900 border-slate-800'
                        : 'bg-white border-slate-200'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={Boolean(checkedGoals[idx])}
                      onChange={() => handleToggleGoal(idx)}
                      className="mt-0.5 rounded text-indigo-600"
                    />
                    <span>{g}</span>
                  </label>
                ))}
              </div>
            </div>

            <form onSubmit={handleAddCustomGoal} className="flex gap-2">
              <input
                type="text"
                value={newGoalText}
                onChange={(e) => setNewGoalText(e.target.value)}
                placeholder="Add a personal learning goal..."
                className={`flex-1 px-3 py-1.5 rounded-lg border text-xs ${
                  isDark ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-300'
                }`}
              />
              <button
                type="submit"
                className="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs cursor-pointer"
              >
                Add
              </button>
            </form>
          </div>
        </div>

        {/* 6-Day Standup Archive Strip for this Developer */}
        <div className="pt-3 border-t border-slate-500/20 space-y-2.5">
          <div className="text-xs font-bold uppercase tracking-wider opacity-70">
            6-Day Standup Email Evidence ({person.name} — Click any day to inspect full raw email)
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-2.5">
            {days.map((d) => {
              const cell = daily_reports[d];
              if (!cell) {
                return (
                  <div
                    key={d}
                    className="p-3 rounded-xl border border-dashed border-rose-500/40 bg-rose-500/5 text-center flex flex-col justify-center"
                  >
                    <div className="text-xs font-mono font-bold text-rose-500">{d}</div>
                    <div className="text-[11px] opacity-60 mt-1">No Report Sent</div>
                  </div>
                );
              }
              return (
                <div
                  key={d}
                  onClick={() => onInspectCell(cell)}
                  className={`p-3 rounded-xl border cursor-pointer transition hover:border-indigo-500 ${
                    isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-white border-slate-200'
                  }`}
                >
                  <div className="flex items-center justify-between text-[11px] font-mono">
                    <span className="font-bold text-indigo-400">{d.slice(5)}</span>
                    <span
                      className={`px-1.5 py-0.2 rounded text-[10px] font-bold uppercase ${
                        cell.learning_eval.score === 'green'
                          ? 'text-emerald-400 bg-emerald-500/10'
                          : cell.learning_eval.score === 'amber'
                          ? 'text-amber-400 bg-amber-500/10'
                          : 'text-rose-400 bg-rose-500/10'
                      }`}
                    >
                      {cell.learning_eval.score}
                    </span>
                  </div>
                  <div className="text-xs font-semibold mt-1.5 line-clamp-2">{cell.gist}</div>
                  <div className="text-[10px] opacity-50 mt-1">{cell.time_short}</div>
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </div>
  );
}
