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
  ChevronDown,
  Zap,
  ShieldCheck,
  BookOpen,
  Award,
  ExternalLink,
  FileText,
  Eye,
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

  // Active top-level sub-tab for progressive disclosure: 'outcomes' | 'growth'
  const [activeTab, setActiveTab] = useState('outcomes');

  // Interactive persisted state
  const [outcomes, setOutcomes] = useState([]);
  const [syncNotes, setSyncNotes] = useState('');
  const [checkedGoals, setCheckedGoals] = useState({});
  const [customGoals, setCustomGoals] = useState([]);
  const [newGoalText, setNewGoalText] = useState('');
  const [editingOutcomeId, setEditingOutcomeId] = useState(null);
  const [expandedOutcomeId, setExpandedOutcomeId] = useState(null);
  const [addingOutcome, setAddingOutcome] = useState(false);
  const [expandedPlaybookIdx, setExpandedPlaybookIdx] = useState(null);
  const [showEmailAudit, setShowEmailAudit] = useState(false);
  const [showSyncNotes, setShowSyncNotes] = useState(false);

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
        // Fallback to default
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
    setExpandedOutcomeId(created.id);
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
      `# 1:1 Growth & Outcome Sync Charter — ${person.name} (/${slug})`,
      `Role: ${person.role} | Focus: ${headline}`,
      `6-Day Telemetry: ${telemetry.days_reported}/${telemetry.total_days} Reports (${telemetry.attendance_pct}%) | Signal: ${telemetry.green_count}G · ${telemetry.amber_count}A · ${telemetry.red_count}R`,
      ``,
      `## 1. Active Outcomes (Two-Way Multi-Owner Sync)`,
      ...outcomes.map(
        (o, idx) =>
          `${idx + 1}. [${(STATUS_BADGES[o.status]?.label || o.status).toUpperCase()}] ${o.track}\n   • v1 (Reported): ${o.v1_reported}\n   • v2 (Tech Sync Contract): ${o.v2_owner_sync}\n   • v3 (Agreed Outcome & SLA): ${o.v3_business_outcome}`
      ),
      ``,
      `## 2. Business Alignment & Value Chain`,
      `Strategic Summary: ${business_alignment.strategic_summary || ''}`,
      ...(business_alignment.value_chains || []).map(
        (vc) => `- ${vc.deliverable} (${vc.client}): ${vc.business_impact} [KPI: ${vc.kpi}]`
      ),
      ``,
      `## 3. Deeper AI Agents Usage`,
      `Maturity: ${ai_agent_usage.current_stage} → ${ai_agent_usage.target_stage}`,
      ...(ai_agent_usage.playbooks || []).map((pb) => `- Playbook: ${pb.title} (${pb.context})`),
      ``,
      `## 4. Personal Learning & 4D Growth Goals`,
      ...allGoals.map((g, i) => `- [${checkedGoals[i] ? 'x' : ' '}] ${g}`),
    ];
    if (syncNotes.trim()) {
      lines.push(``, `## 1:1 Discussion Notes & Next Commitments`, syncNotes.trim());
    }
    return lines.join('\n');
  };

  return (
    <div className="space-y-4 pb-12 max-w-[1400px] mx-auto">
      {/* =====================================================================
          1. COMPACT DEVELOPER SWITCHER BAR (Glanceable Pill Carousel)
      ===================================================================== */}
      <div
        className={`rounded-2xl border px-3.5 py-2.5 flex items-center justify-between gap-3 ${
          isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex items-center gap-1.5 overflow-x-auto py-0.5">
          <span className="text-[11px] font-bold uppercase tracking-wider opacity-60 mr-1 flex items-center gap-1 shrink-0">
            <Users className="w-3.5 h-3.5 text-indigo-500" /> 1:1 Hubs:
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
                className={`px-2.5 py-1 rounded-xl text-xs font-semibold border transition flex items-center gap-1.5 shrink-0 ${
                  isActive
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-xs'
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

        <button
          onClick={() => onCopyText(buildSyncSummaryText(), `sync-brief-${slug}`)}
          className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-xs shrink-0"
          title="Export complete 1:1 charter to clipboard for Slack or email"
        >
          {copiedId === `sync-brief-${slug}` ? (
            <>
              <Check className="w-3.5 h-3.5" />
              <span>Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3.5 h-3.5" />
              <span>Copy 1:1 Charter</span>
            </>
          )}
        </button>
      </div>

      {/* =====================================================================
          2. STREAMLINED EXECUTIVE PROFILE HERO (Above the fold)
      ===================================================================== */}
      <div
        className={`rounded-2xl border p-5 ${
          isDark
            ? 'bg-slate-900/60 border-slate-800'
            : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 text-white font-bold text-base flex items-center justify-center shadow-md shrink-0">
              {getInitials(person.name)}
            </div>
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="text-lg font-bold tracking-tight">{person.name}</h2>
                <span
                  className={`px-2 py-0.5 rounded text-[11px] font-mono border ${
                    isDark
                      ? 'bg-indigo-950/70 text-indigo-300 border-indigo-700/50'
                      : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                  }`}
                >
                  /{slug}
                </span>
                <span className="text-xs opacity-60 font-mono hidden sm:inline">{person.email}</span>
              </div>
              <p className="text-xs text-indigo-500 font-semibold mt-0.5">{headline}</p>
              <div className="flex flex-wrap items-center gap-1.5 mt-1.5">
                {product_spaces.map((ps) => (
                  <span
                    key={ps}
                    className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                      isDark
                        ? 'bg-emerald-950/60 text-emerald-300 border-emerald-800/50'
                        : 'bg-emerald-50 text-emerald-800 border-emerald-200'
                    }`}
                  >
                    Product: {ps}
                  </span>
                ))}
                {utilities.map((u) => (
                  <span
                    key={u}
                    className={`px-2 py-0.5 rounded text-[10px] font-medium border ${
                      isDark
                        ? 'bg-slate-800 text-slate-300 border-slate-700'
                        : 'bg-slate-100 text-slate-700 border-slate-200'
                    }`}
                  >
                    {u}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* 3 Executive Metrics */}
          <div className="flex items-center gap-2.5 shrink-0">
            <div
              className={`px-3 py-2 rounded-xl border text-center min-w-[95px] ${
                isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-slate-50 border-slate-200'
              }`}
            >
              <div className="text-[10px] font-bold uppercase opacity-60">Standups</div>
              <div className="text-sm font-bold text-emerald-500 mt-0.5">
                {telemetry.days_reported}/{telemetry.total_days}
                <span className="text-[10px] font-normal opacity-70 ml-1">({telemetry.attendance_pct}%)</span>
              </div>
            </div>

            <div
              className={`px-3 py-2 rounded-xl border text-center min-w-[95px] ${
                isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-slate-50 border-slate-200'
              }`}
            >
              <div className="text-[10px] font-bold uppercase opacity-60">AI Stage</div>
              <div className="text-sm font-bold text-purple-400 mt-0.5">
                {(ai_agent_usage.current_stage || 'L2').split(':')[0]} →{' '}
                {(ai_agent_usage.target_stage || 'L3').split(':')[0]}
              </div>
            </div>

            <div
              className={`px-3 py-2 rounded-xl border text-center min-w-[95px] ${
                isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-slate-50 border-slate-200'
              }`}
            >
              <div className="text-[10px] font-bold uppercase opacity-60">Learnings</div>
              <div className="text-sm font-bold mt-0.5">
                <span className="text-emerald-500">{telemetry.green_count}G</span>
                <span className="text-amber-500 ml-1">{telemetry.amber_count}A</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* =====================================================================
          3. PROGRESSIVE DISCLOSURE SUB-TABS (Outcomes vs AI & Growth)
      ===================================================================== */}
      <div className="flex items-center justify-between border-b border-slate-500/20 px-1">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('outcomes')}
            className={`pb-2.5 px-3 text-xs font-bold border-b-2 transition flex items-center gap-2 cursor-pointer ${
              activeTab === 'outcomes'
                ? 'border-indigo-600 text-indigo-500'
                : 'border-transparent opacity-60 hover:opacity-100'
            }`}
          >
            <Target className="w-4 h-4" />
            <span>Outcomes &amp; Business Impact ({outcomes.length})</span>
          </button>
          <button
            onClick={() => setActiveTab('growth')}
            className={`pb-2.5 px-3 text-xs font-bold border-b-2 transition flex items-center gap-2 cursor-pointer ${
              activeTab === 'growth'
                ? 'border-indigo-600 text-indigo-500'
                : 'border-transparent opacity-60 hover:opacity-100'
            }`}
          >
            <Bot className="w-4 h-4" />
            <span>AI Leverage &amp; 4D Growth</span>
          </button>
        </div>

        <button
          onClick={() => setShowSyncNotes(!showSyncNotes)}
          className={`text-xs font-semibold pb-2.5 px-2 flex items-center gap-1.5 transition cursor-pointer ${
            showSyncNotes || syncNotes.trim()
              ? 'text-indigo-400 opacity-100 font-bold'
              : 'opacity-60 hover:opacity-100'
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          <span>Sync Notes {syncNotes.trim() ? '•' : ''}</span>
        </button>
      </div>

      {/* Collapsible 1:1 Scratchpad */}
      {showSyncNotes && (
        <div
          className={`p-4 rounded-2xl border space-y-2 transition ${
            isDark ? 'bg-slate-900/90 border-slate-800' : 'bg-slate-50 border-slate-200'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
              <MessageSquare className="w-3.5 h-3.5" /> 1:1 Discussion Decisions &amp; Commitments
            </span>
            <span className="text-[11px] opacity-60">Auto-saved to your browser</span>
          </div>
          <textarea
            rows={2}
            value={syncNotes}
            onChange={(e) => {
              setSyncNotes(e.target.value);
              persistState(outcomes, e.target.value, checkedGoals, customGoals);
            }}
            placeholder={`Jot notes from 1:1 sync with ${person.name}, Sumukh, and Prasad...`}
            className={`w-full p-2.5 rounded-xl border text-xs focus:outline-none focus:border-indigo-500 ${
              isDark ? 'bg-slate-950 border-slate-800 text-white' : 'bg-white border-slate-300'
            }`}
          />
        </div>
      )}

      {/* =====================================================================
          TAB 1: OUTCOMES & BUSINESS IMPACT
      ===================================================================== */}
      {activeTab === 'outcomes' && (
        <div className="space-y-4">
          {/* Active Outcomes Table / Cards */}
          <div
            className={`rounded-2xl border overflow-hidden ${
              isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
            }`}
          >
            <div className="p-4 border-b border-slate-500/15 flex flex-wrap items-center justify-between gap-3">
              <div>
                <h3 className="text-sm font-bold flex items-center gap-2">
                  <Target className="w-4 h-4 text-indigo-500" />
                  <span>Two-Way Iterative Outcomes</span>
                  <span className="text-xs opacity-60 font-normal">
                    (Click any stream to view 3-stage evolution)
                  </span>
                </h3>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setAddingOutcome(!addingOutcome)}
                  className="px-2.5 py-1 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1 cursor-pointer"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Add Outcome</span>
                </button>
                <button
                  onClick={handleResetCharter}
                  className={`px-2 py-1 rounded-xl border text-xs flex items-center gap-1 cursor-pointer opacity-70 hover:opacity-100 ${
                    isDark ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200'
                  }`}
                  title="Reset edits to baseline"
                >
                  <RotateCcw className="w-3 h-3" />
                </button>
              </div>
            </div>

            {/* Quick Add Form */}
            {addingOutcome && (
              <div
                className={`p-4 border-b space-y-3 ${
                  isDark ? 'bg-indigo-950/20 border-indigo-500/30' : 'bg-indigo-50/50 border-indigo-200'
                }`}
              >
                <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
                  New Outcome Stream
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                  <input
                    type="text"
                    value={newOutcomeDraft.track}
                    onChange={(e) => setNewOutcomeDraft({ ...newOutcomeDraft, track: e.target.value })}
                    placeholder="Track Title (e.g. Automated GESCOM Restore Verification)"
                    className={`px-3 py-1.5 rounded-lg border text-xs ${
                      isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                    }`}
                  />
                  <select
                    value={newOutcomeDraft.status}
                    onChange={(e) => setNewOutcomeDraft({ ...newOutcomeDraft, status: e.target.value })}
                    className={`px-3 py-1.5 rounded-lg border text-xs ${
                      isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                    }`}
                  >
                    <option value="in_progress">Active Iteration</option>
                    <option value="ready_for_deploy">Ready for Deploy</option>
                    <option value="needs_iteration">Needs Owner Sync</option>
                    <option value="done">Done / Verified</option>
                  </select>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5">
                  <textarea
                    rows={2}
                    value={newOutcomeDraft.v1_reported}
                    onChange={(e) => setNewOutcomeDraft({ ...newOutcomeDraft, v1_reported: e.target.value })}
                    placeholder="v1: Developer's reported task..."
                    className={`p-2 rounded-lg border text-xs ${
                      isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                    }`}
                  />
                  <textarea
                    rows={2}
                    value={newOutcomeDraft.v2_owner_sync}
                    onChange={(e) => setNewOutcomeDraft({ ...newOutcomeDraft, v2_owner_sync: e.target.value })}
                    placeholder="v2: Tech & Lead verification contract..."
                    className={`p-2 rounded-lg border text-xs ${
                      isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                    }`}
                  />
                  <textarea
                    rows={2}
                    value={newOutcomeDraft.v3_business_outcome}
                    onChange={(e) => setNewOutcomeDraft({ ...newOutcomeDraft, v3_business_outcome: e.target.value })}
                    placeholder="v3: Measurable business outcome & SLA..."
                    className={`p-2 rounded-lg border text-xs ${
                      isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                    }`}
                  />
                </div>
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => setAddingOutcome(false)}
                    className="px-3 py-1 text-xs opacity-70 hover:opacity-100 cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleAddOutcome}
                    className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold cursor-pointer"
                  >
                    Save Outcome
                  </button>
                </div>
              </div>
            )}

            {/* List of Outcomes with Progressive Disclosure */}
            <div className="divide-y divide-slate-500/10">
              {outcomes.map((out) => {
                const st = STATUS_BADGES[out.status] || STATUS_BADGES.in_progress;
                const isExpanded = expandedOutcomeId === out.id;
                const isEditing = editingOutcomeId === out.id;

                return (
                  <div key={out.id} className="p-4 transition hover:bg-slate-500/5">
                    {/* Compact Row */}
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div
                        className="flex-1 cursor-pointer select-none space-y-1"
                        onClick={() => setExpandedOutcomeId(isExpanded ? null : out.id)}
                      >
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-sm">{out.track}</span>
                          <span
                            className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${
                              isDark ? st.dark : st.light
                            }`}
                          >
                            {st.label}
                          </span>
                        </div>
                        <p className="text-xs opacity-80 line-clamp-1">
                          <strong>Outcome:</strong> {out.v3_business_outcome}
                        </p>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        <button
                          onClick={() => setEditingOutcomeId(isEditing ? null : out.id)}
                          className={`px-2.5 py-1 rounded-lg border text-xs flex items-center gap-1 cursor-pointer ${
                            isEditing
                              ? 'bg-emerald-600 text-white border-emerald-500'
                              : isDark
                              ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                              : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                          }`}
                        >
                          {isEditing ? (
                            <>
                              <Save className="w-3 h-3" /> Save
                            </>
                          ) : (
                            <>
                              <Edit3 className="w-3 h-3" /> Edit
                            </>
                          )}
                        </button>
                        <button
                          onClick={() => setExpandedOutcomeId(isExpanded ? null : out.id)}
                          className={`p-1.5 rounded-lg border text-xs cursor-pointer opacity-70 hover:opacity-100 ${
                            isDark ? 'border-slate-800' : 'border-slate-200'
                          }`}
                        >
                          <ChevronDown
                            className={`w-3.5 h-3.5 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                          />
                        </button>
                      </div>
                    </div>

                    {/* Expanded 3-Iteration Drilldown */}
                    {(isExpanded || isEditing) && (
                      <div className="mt-3.5 pt-3.5 border-t border-slate-500/15 space-y-3">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                          {/* Iteration 1 */}
                          <div
                            className={`p-3 rounded-xl border ${
                              isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-slate-50 border-slate-200'
                            }`}
                          >
                            <div className="text-[10px] font-bold uppercase tracking-wider text-amber-500 mb-1">
                              Iteration 1 · Reported Task (Dev)
                            </div>
                            {isEditing ? (
                              <textarea
                                rows={3}
                                value={out.v1_reported}
                                onChange={(e) => handleUpdateOutcomeField(out.id, 'v1_reported', e.target.value)}
                                className={`w-full p-2 rounded border text-xs ${
                                  isDark ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-300'
                                }`}
                              />
                            ) : (
                              <p className="text-xs leading-relaxed opacity-85">{out.v1_reported}</p>
                            )}
                          </div>

                          {/* Iteration 2 */}
                          <div
                            className={`p-3 rounded-xl border ${
                              isDark ? 'bg-indigo-950/30 border-indigo-800/50' : 'bg-indigo-50/50 border-indigo-200'
                            }`}
                          >
                            <div className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 mb-1">
                              Iteration 2 · Tech &amp; Verification Sync
                            </div>
                            {isEditing ? (
                              <textarea
                                rows={3}
                                value={out.v2_owner_sync}
                                onChange={(e) => handleUpdateOutcomeField(out.id, 'v2_owner_sync', e.target.value)}
                                className={`w-full p-2 rounded border text-xs ${
                                  isDark ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-300'
                                }`}
                              />
                            ) : (
                              <p className="text-xs leading-relaxed opacity-90">{out.v2_owner_sync}</p>
                            )}
                          </div>

                          {/* Iteration 3 */}
                          <div
                            className={`p-3 rounded-xl border ${
                              isDark ? 'bg-emerald-950/30 border-emerald-800/50' : 'bg-emerald-50/50 border-emerald-200'
                            }`}
                          >
                            <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-500 mb-1">
                              Iteration 3 · Agreed Business Outcome &amp; SLA
                            </div>
                            {isEditing ? (
                              <textarea
                                rows={3}
                                value={out.v3_business_outcome}
                                onChange={(e) => handleUpdateOutcomeField(out.id, 'v3_business_outcome', e.target.value)}
                                className={`w-full p-2 rounded border text-xs ${
                                  isDark ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-300'
                                }`}
                              />
                            ) : (
                              <p className="text-xs leading-relaxed font-medium">{out.v3_business_outcome}</p>
                            )}
                          </div>
                        </div>

                        {/* Status selector during editing */}
                        {isEditing && (
                          <div className="flex items-center gap-2 pt-1">
                            <span className="text-xs font-semibold opacity-70">Status:</span>
                            <select
                              value={out.status}
                              onChange={(e) => handleUpdateOutcomeField(out.id, 'status', e.target.value)}
                              className={`px-2.5 py-1 rounded-lg text-xs font-semibold border ${
                                isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-white border-slate-300'
                              }`}
                            >
                              {Object.entries(STATUS_BADGES).map(([k, v]) => (
                                <option key={k} value={k} className="bg-slate-900 text-white">
                                  {v.label}
                                </option>
                              ))}
                            </select>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Business & Client Value Chain (Condensed Clean Table) */}
          <div
            className={`rounded-2xl border p-4 space-y-3 ${
              isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
            }`}
          >
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-500 flex items-center gap-1.5">
                <Briefcase className="w-3.5 h-3.5" /> Code-to-Customer Value Chain
              </h3>
              <span className="text-[11px] opacity-60">Utility SLA &amp; Deliverable Impact</span>
            </div>

            <div className="overflow-x-auto rounded-xl border border-slate-500/20">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr
                    className={`border-b text-[11px] uppercase tracking-wider ${
                      isDark ? 'bg-slate-950/80 border-slate-800 text-slate-400' : 'bg-slate-100 border-slate-200 text-slate-600'
                    }`}
                  >
                    <th className="py-2 px-3">Deliverable</th>
                    <th className="py-2 px-3">Artifact</th>
                    <th className="py-2 px-3">Utility</th>
                    <th className="py-2 px-3">Operational Impact</th>
                    <th className="py-2 px-3">Target KPI</th>
                  </tr>
                </thead>
                <tbody className={`divide-y ${isDark ? 'divide-slate-800' : 'divide-slate-200'}`}>
                  {(business_alignment.value_chains || []).map((vc, i) => (
                    <tr key={i} className={isDark ? 'hover:bg-slate-950/40' : 'hover:bg-slate-50'}>
                      <td className="py-2.5 px-3 font-bold">{vc.deliverable}</td>
                      <td className="py-2.5 px-3 font-mono text-[11px] text-indigo-400">{vc.artifact}</td>
                      <td className="py-2.5 px-3 font-semibold">{vc.client}</td>
                      <td className="py-2.5 px-3 opacity-85 leading-relaxed">{vc.business_impact}</td>
                      <td className="py-2.5 px-3 font-semibold text-emerald-500">{vc.kpi}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* 6-Day Plan-vs-Actual Continuity Strip */}
          <div
            className={`rounded-2xl border p-4 space-y-2.5 ${
              isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
            }`}
          >
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold uppercase tracking-wider opacity-70">
                Plan-to-Actual Continuity (Yesterday's Plan → Today's Delivery)
              </span>
              <span className="text-[11px] opacity-60">Click card to inspect</span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-2.5">
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
                    className={`p-2.5 rounded-xl border flex flex-col justify-between cursor-pointer transition hover:scale-[1.01] ${badgeColor}`}
                  >
                    <div>
                      <div className="flex items-center justify-between text-[10px] font-mono opacity-75">
                        <span>{item.day_prev.slice(5)} → {item.day_curr.slice(5)}</span>
                        <span className="uppercase font-bold">{item.status}</span>
                      </div>
                      <div className="text-xs font-bold mt-1 truncate">{item.badge}</div>
                      <p className="text-[11px] opacity-80 mt-1 line-clamp-2 leading-snug">
                        {item.commentary}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* =====================================================================
          TAB 2: AI LEVERAGE & 4D PERSONAL GROWTH
      ===================================================================== */}
      {activeTab === 'growth' && (
        <div className="space-y-4">
          {/* AI Leverage Section */}
          <div
            className={`rounded-2xl border p-5 space-y-4 ${
              isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
            }`}
          >
            <div className="flex flex-wrap items-center justify-between gap-3 border-b pb-3 border-slate-500/15">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-400">
                  <Bot className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold">Agentic AI Leverage &amp; Playbooks</h3>
                  <p className="text-xs opacity-60">Grounded in actual standup telemetry</p>
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs">
                <span className="font-semibold opacity-70">Maturity:</span>
                <span
                  className={`px-2.5 py-0.5 rounded-full font-semibold border ${
                    isDark
                      ? 'bg-slate-950 border-slate-800 text-slate-300'
                      : 'bg-slate-100 border-slate-200 text-slate-700'
                  }`}
                >
                  {ai_agent_usage.current_stage}
                </span>
                <ArrowRight className="w-3.5 h-3.5 text-purple-400" />
                <span
                  className={`px-2.5 py-0.5 rounded-full font-semibold border ${
                    isDark
                      ? 'bg-purple-950/80 border-purple-700/60 text-purple-200'
                      : 'bg-purple-50 border-purple-200 text-purple-800'
                  }`}
                >
                  {ai_agent_usage.target_stage}
                </span>
              </div>
            </div>

            <p className="text-xs leading-relaxed opacity-90">
              <strong className="text-purple-400 uppercase tracking-wider text-[10px] mr-1">
                Telemetry Observation:
              </strong>
              {ai_agent_usage.observation}
            </p>

            {/* Compact Playbook Accordion Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
              {(ai_agent_usage.playbooks || []).map((pb, idx) => {
                const copyKey = `pb-${slug}-${idx}`;
                const isExpanded = expandedPlaybookIdx === idx;

                return (
                  <div
                    key={idx}
                    className={`rounded-xl border p-3.5 space-y-2.5 ${
                      isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-slate-50 border-slate-200'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs font-bold text-indigo-400 flex items-center gap-1.5">
                        <Sparkles className="w-3.5 h-3.5" />
                        {pb.title}
                      </span>
                      <button
                        onClick={() => onCopyText(pb.prompt, copyKey)}
                        className="px-2.5 py-1 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-[11px] font-semibold flex items-center gap-1 cursor-pointer shrink-0"
                      >
                        {copiedId === copyKey ? (
                          <>
                            <Check className="w-3 h-3" /> Copied
                          </>
                        ) : (
                          <>
                            <Copy className="w-3 h-3" /> Copy Prompt
                          </>
                        )}
                      </button>
                    </div>

                    <p className="text-[11px] opacity-80 leading-relaxed">{pb.context}</p>

                    <button
                      onClick={() => setExpandedPlaybookIdx(isExpanded ? null : idx)}
                      className="text-[11px] font-semibold text-purple-400 hover:underline flex items-center gap-1 cursor-pointer"
                    >
                      <span>{isExpanded ? 'Hide Agent Prompt' : 'View Agent Prompt Preview'}</span>
                      <ChevronDown
                        className={`w-3 h-3 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                      />
                    </button>

                    {isExpanded && (
                      <pre
                        className={`p-3 rounded-lg border font-mono text-[11px] whitespace-pre-wrap leading-relaxed max-h-56 overflow-y-auto ${
                          isDark
                            ? 'bg-slate-900 border-slate-800 text-slate-200'
                            : 'bg-white border-slate-200 text-slate-800'
                        }`}
                      >
                        {pb.prompt}
                      </pre>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* 4D Personal Growth Section */}
          <div
            className={`rounded-2xl border p-5 space-y-4 ${
              isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
            }`}
          >
            <div className="flex items-center justify-between border-b pb-3 border-slate-500/15">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-500">
                  <GraduationCap className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold">4D Personal Learning &amp; Commitments</h3>
                  <p className="text-xs opacity-60">Technical · Utility Domain · Craft &amp; Testing · Ownership</p>
                </div>
              </div>
            </div>

            {/* 4 Dimension Score Strip */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { key: 'technical_depth', label: '1. Technical Depth', color: 'bg-indigo-500' },
                { key: 'domain_mastery', label: '2. Utility Domain', color: 'bg-emerald-500' },
                { key: 'engineering_craft', label: '3. Craft & Testing', color: 'bg-sky-500' },
                { key: 'communication_ownership', label: '4. Ownership & Signal', color: 'bg-amber-500' },
              ].map((dim) => {
                const val = scores[dim.key] || 75;
                return (
                  <div
                    key={dim.key}
                    className={`p-3 rounded-xl border space-y-1.5 ${
                      isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-slate-50 border-slate-200'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold">{dim.label}</span>
                      <span className="font-mono font-bold opacity-80">{val}/100</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-slate-500/20 overflow-hidden">
                      <div className={`h-full rounded-full ${dim.color}`} style={{ width: `${val}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Growth Commitments Checklist */}
            <div
              className={`p-4 rounded-xl border space-y-3 ${
                isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-slate-50 border-slate-200'
              }`}
            >
              <div className="text-xs font-bold uppercase tracking-wider text-amber-500">
                Interactive Learning Commitments
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {allGoals.map((g, idx) => (
                  <label
                    key={idx}
                    className={`p-2 rounded-lg border flex items-start gap-2 cursor-pointer text-xs leading-snug transition ${
                      checkedGoals[idx]
                        ? isDark
                          ? 'bg-emerald-950/30 border-emerald-800/50 line-through opacity-60'
                          : 'bg-emerald-50 border-emerald-200 line-through opacity-60'
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

              <form onSubmit={handleAddCustomGoal} className="flex gap-2 pt-1">
                <input
                  type="text"
                  value={newGoalText}
                  onChange={(e) => setNewGoalText(e.target.value)}
                  placeholder="Add a custom learning commitment..."
                  className={`flex-1 px-3 py-1.5 rounded-lg border text-xs ${
                    isDark ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-300'
                  }`}
                />
                <button
                  type="submit"
                  className="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs cursor-pointer"
                >
                  Add Goal
                </button>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* =====================================================================
          4. COLLAPSIBLE BOTTOM DRAWER: STANDUP EMAIL EVIDENCE & AUDIT
      ===================================================================== */}
      <div
        className={`rounded-2xl border overflow-hidden transition ${
          isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <button
          onClick={() => setShowEmailAudit(!showEmailAudit)}
          className="w-full p-4 flex items-center justify-between text-left hover:bg-slate-500/5 cursor-pointer transition select-none"
        >
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-indigo-500" />
            <span className="text-xs font-bold uppercase tracking-wider opacity-80">
              6-Day Standup Email Audit &amp; Raw History ({person.name})
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] opacity-60">
              {showEmailAudit ? 'Collapse' : 'Expand 6 Reports'}
            </span>
            <ChevronDown
              className={`w-4 h-4 transition-transform ${showEmailAudit ? 'rotate-180' : ''}`}
            />
          </div>
        </button>

        {showEmailAudit && (
          <div className="p-4 border-t border-slate-500/15">
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
              {days.map((d) => {
                const cell = daily_reports[d];
                if (!cell) {
                  return (
                    <div
                      key={d}
                      className="p-3 rounded-xl border border-dashed border-rose-500/40 bg-rose-500/5 text-center flex flex-col justify-center"
                    >
                      <div className="text-xs font-mono font-bold text-rose-500">{d.slice(5)}</div>
                      <div className="text-[10px] opacity-60 mt-0.5">Missing</div>
                    </div>
                  );
                }
                return (
                  <div
                    key={d}
                    onClick={() => onInspectCell(cell)}
                    className={`p-3 rounded-xl border cursor-pointer transition hover:border-indigo-500 ${
                      isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-slate-50 border-slate-200'
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
        )}
      </div>
    </div>
  );
}
