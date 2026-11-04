import React, { useState } from 'react';
import {
  Layers,
  Calendar,
  LayoutGrid,
  BarChart3,
  FileText,
  Sparkles,
  CheckCircle2,
  Clock,
  AlertTriangle,
  ArrowUpRight,
  ChevronDown,
  ChevronRight,
  User,
  Shield,
  Zap,
  Building2,
  Cpu,
  ListTodo,
  Filter,
} from 'lucide-react';

const PRODUCT_META = {
  TRM: {
    icon: Zap,
    accent: 'indigo',
    pillActive: 'bg-indigo-600 text-white border-indigo-500 shadow-sm',
    barBg: 'bg-gradient-to-r from-indigo-500 to-blue-500',
    badgeDark: 'bg-indigo-950/80 text-indigo-300 border-indigo-700/60',
    badgeLight: 'bg-indigo-50 text-indigo-700 border-indigo-200',
  },
  ERP: {
    icon: Building2,
    accent: 'emerald',
    pillActive: 'bg-emerald-600 text-white border-emerald-500 shadow-sm',
    barBg: 'bg-gradient-to-r from-emerald-500 to-teal-500',
    badgeDark: 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60',
    badgeLight: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  },
  KPTCL: {
    icon: Cpu,
    accent: 'amber',
    pillActive: 'bg-amber-500 text-slate-950 border-amber-400 shadow-sm',
    barBg: 'bg-gradient-to-r from-amber-500 to-orange-500',
    badgeDark: 'bg-amber-950/80 text-amber-300 border-amber-700/60',
    badgeLight: 'bg-amber-50 text-amber-800 border-amber-200',
  },
  'Infra & Security': {
    icon: Shield,
    accent: 'purple',
    pillActive: 'bg-purple-600 text-white border-purple-500 shadow-sm',
    barBg: 'bg-gradient-to-r from-purple-500 to-fuchsia-500',
    badgeDark: 'bg-purple-950/80 text-purple-300 border-purple-700/60',
    badgeLight: 'bg-purple-50 text-purple-700 border-purple-200',
  },
};

const STATUS_META = {
  done: {
    label: 'Done / Shipped',
    dot: 'bg-emerald-400',
    dark: 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60',
    light: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    barColor: 'from-emerald-500 to-teal-500',
  },
  in_progress: {
    label: 'In Progress',
    dot: 'bg-sky-400',
    dark: 'bg-sky-950/80 text-sky-300 border-sky-700/60',
    light: 'bg-sky-50 text-sky-800 border-sky-200',
    barColor: 'from-indigo-500 to-sky-500',
  },
  planned: {
    label: 'Planned Next',
    dot: 'bg-amber-400',
    dark: 'bg-amber-950/80 text-amber-300 border-amber-700/60',
    light: 'bg-amber-50 text-amber-800 border-amber-200',
    barColor: 'from-amber-500 to-orange-400',
  },
  blocked: {
    label: 'Needs Attention',
    dot: 'bg-rose-400',
    dark: 'bg-rose-950/90 text-rose-300 border-rose-700/70',
    light: 'bg-rose-50 text-rose-800 border-rose-300',
    barColor: 'from-rose-500 to-orange-500',
  },
};

const DAY_HEADERS = {
  '2026-10-29': { top: 'Oct 29', sub: 'Thu · D1' },
  '2026-10-30': { top: 'Oct 30', sub: 'Fri · D2' },
  '2026-10-31': { top: 'Oct 31', sub: 'Sat · D3' },
  '2026-11-02': { top: 'Nov 02', sub: 'Mon · D4' },
  '2026-11-03': { top: 'Nov 03', sub: 'Tue · D5' },
  '2026-11-04': { top: 'Nov 04', sub: 'Wed · D6' },
};

function getInitials(name) {
  return name
    .split(/\s+/)
    .slice(0, 2)
    .map((w) => w[0])
    .join('')
    .toUpperCase();
}

export default function ProductTrackerView({
  isDark,
  productTracker,
  searchQuery,
  onInspectCell,
}) {
  const [selectedProduct, setSelectedProduct] = useState('ALL'); // 'ALL' | 'TRM' | 'ERP' | 'KPTCL' | 'Infra & Security'
  const [subView, setSubView] = useState('gantt'); // 'gantt' | 'list' | 'board'
  const [statusFilter, setStatusFilter] = useState('all');
  const [expandedTaskIds, setExpandedTaskIds] = useState(new Set(['trm-inesh-prepaid', 'erp-gescom-arrears', 'infra-db-restores']));
  const [activeAgentTaskId, setActiveAgentTaskId] = useState('trm-inesh-prepaid');

  if (!productTracker) return null;
  const { products = [], tasks = [], timeline_days = [] } = productTracker;

  const q = (searchQuery || '').trim().toLowerCase();

  const filteredTasks = tasks.filter((t) => {
    if (selectedProduct !== 'ALL' && t.product !== selectedProduct) return false;
    if (statusFilter !== 'all' && t.status !== statusFilter) return false;
    if (q) {
      const hay = `${t.title} ${t.project} ${t.product} ${t.assignee} ${t.tags.join(' ')}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  const toggleExpandTask = (id) => {
    const next = new Set(expandedTaskIds);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setExpandedTaskIds(next);
  };

  // Pick product brief based on selectedProduct
  const activeBriefProduct =
    selectedProduct === 'ALL'
      ? {
          name: 'All NSoft Products (TRM · ERP · KPTCL · Infra & Security)',
          brief: {
            title: 'NSoft Engineering Portfolio Brief (Oct 29 – Nov 4)',
            agent_author: 'NSoft Portfolio Super Agent',
            overview:
              'Real-time synthesis of 18 engineering workstreams extracted from 6 days of team standups across TRM (SpotBilling & Smart Metering), ERP (GESCOM/TCED HRMS, Payroll, Municipal PF & BGCL), KPTCL, and Infra & Security (SQL Server & PostgreSQL / PPAS 9.5 DB Restorations).',
            highlights: [
              'TRM: Nov 2026 SpotBilling Apps shipped for HESCOM & BWSSB; TCED Billing updated across 6 tariff rules (DL, wheeling, street light, solar print, temporary consumer, solar wheeling loss); INESH & Capital DLMS prepaid meter billing & PR XML/API integrated.',
              'ERP: GESCOM HRMS 5-screen delivery (Arrears/JV 2023–24, ELS Approval Net Pay fix, Salary Fund Request B_BRNO & USP_HRMS_SalaryFundRequestApproval); TCED Form 3/4 & 75% advance calculation tested E2E; PensionStopExit & HRMS Disciplinary/Incumbency fixes completed.',
              'Infra & Security: 20/21 SQL Server databases restored ONLINE + GESCOM_LIVE_02042026 full restore completed + ERP_LIVE_31032026 restored in PostgreSQL/PPAS 9.5 (--no-owner/--no-acl).',
            ],
            risks: [
              'Infra: SQL Server differential restore for GESCOM_LIVE_02042026 restarted on Nov 4 after delays; PostgreSQL GESCOM validation continuing on Nov 5.',
              'Reporting Continuity: Nitish Nag M, Chitrashree HR, and Venkata Sai (sent Nov 3 update on Nov 4 morning) did not submit a Nov 4 evening report.',
            ],
          },
        }
      : products.find((p) => p.id === selectedProduct) || products[0];

  // Compute Assignee Bar Chart stats for the Dashboard widget
  const assigneeCounts = {};
  filteredTasks.forEach((t) => {
    const shortName = t.assignee.split(' ')[0];
    if (!assigneeCounts[shortName]) {
      assigneeCounts[shortName] = { name: shortName, fullName: t.assignee, count: 0, done: 0, subtasks: 0 };
    }
    assigneeCounts[shortName].count += 1;
    assigneeCounts[shortName].subtasks += t.subtasks?.length || 1;
    if (t.status === 'done') assigneeCounts[shortName].done += 1;
  });
  const assigneeBars = Object.values(assigneeCounts).sort((a, b) => b.subtasks - a.subtasks);
  const maxSubtasks = Math.max(1, ...assigneeBars.map((a) => a.subtasks));

  // Status counts for "Projects in Flight" widget
  const statusBreakdown = {
    done: filteredTasks.filter((t) => t.status === 'done').length,
    in_progress: filteredTasks.filter((t) => t.status === 'in_progress').length,
    planned: filteredTasks.filter((t) => t.status === 'planned').length,
    blocked: filteredTasks.filter((t) => t.status === 'blocked').length,
  };

  return (
    <div className="space-y-5">
      {/* ClickUp-Style Workspace Header: Product Switcher + Sub-View Tabs */}
      <div
        className={`rounded-2xl border p-4 space-y-3.5 ${
          isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        {/* Top Row: Product Space Selector Pills */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider opacity-60 mr-1 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-indigo-500" /> Product Spaces:
            </span>

            <button
              onClick={() => setSelectedProduct('ALL')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold border transition cursor-pointer flex items-center gap-2 ${
                selectedProduct === 'ALL'
                  ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm'
                  : isDark
                  ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                  : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
              }`}
            >
              <span>All Products</span>
              <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-black/20 font-mono">
                {tasks.length}
              </span>
            </button>

            {products.map((prod) => {
              const meta = PRODUCT_META[prod.id] || PRODUCT_META.TRM;
              const ProdIcon = meta.icon;
              const count = tasks.filter((t) => t.product === prod.id).length;
              const isSelected = selectedProduct === prod.id;

              return (
                <button
                  key={prod.id}
                  onClick={() => setSelectedProduct(prod.id)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-bold border transition cursor-pointer flex items-center gap-2 ${
                    isSelected
                      ? meta.pillActive
                      : isDark
                      ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                      : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <ProdIcon className="w-3.5 h-3.5" />
                  <span>{prod.name}</span>
                  <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-black/15 font-mono">
                    {count}
                  </span>
                </button>
              );
            })}
          </div>

          {/* ClickUp Sub-View Switcher (Gantt + Docs/Dashboard | List | Kanban Board) */}
          <div className="flex items-center gap-1.5">
            {[
              { id: 'gantt', label: 'Gantt & Brief Hub', icon: Calendar },
              { id: 'list', label: 'Task Hierarchy List', icon: ListTodo },
              { id: 'board', label: 'Kanban Board', icon: LayoutGrid },
            ].map((vw) => {
              const VIcon = vw.icon;
              return (
                <button
                  key={vw.id}
                  onClick={() => setSubView(vw.id)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold border flex items-center gap-1.5 transition cursor-pointer ${
                    subView === vw.id
                      ? isDark
                        ? 'bg-indigo-950/80 border-indigo-500 text-indigo-200'
                        : 'bg-indigo-50 border-indigo-500 text-indigo-900'
                      : isDark
                      ? 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200'
                      : 'bg-slate-50 border-slate-200 text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <VIcon className="w-3.5 h-3.5" />
                  <span>{vw.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Second Row: Project Mapping Pills + Status Filter */}
        <div
          className={`pt-2.5 border-t flex flex-wrap items-center justify-between gap-2 text-xs ${
            isDark ? 'border-slate-800/80' : 'border-slate-100'
          }`}
        >
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-[11px] opacity-60 font-medium mr-1">Mapped Projects:</span>
            {(selectedProduct === 'ALL'
              ? products.flatMap((p) => p.projects.map((pr) => ({ prod: p.id, name: pr })))
              : (products.find((p) => p.id === selectedProduct)?.projects || []).map((pr) => ({
                  prod: selectedProduct,
                  name: pr,
                }))
            ).map((item) => {
              const meta = PRODUCT_META[item.prod] || PRODUCT_META.TRM;
              return (
                <span
                  key={`${item.prod}-${item.name}`}
                  className={`px-2 py-0.5 rounded-md text-[11px] font-medium border ${
                    isDark ? meta.badgeDark : meta.badgeLight
                  }`}
                >
                  <strong>{item.prod}:</strong> {item.name}
                </span>
              );
            })}
          </div>

          <div className="flex items-center gap-1.5">
            {[
              { id: 'all', label: 'All' },
              { id: 'in_progress', label: 'In Progress' },
              { id: 'done', label: 'Done' },
              { id: 'planned', label: 'Planned' },
              { id: 'blocked', label: 'Needs Attention' },
            ].map((st) => (
              <button
                key={st.id}
                onClick={() => setStatusFilter(st.id)}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium border cursor-pointer ${
                  statusFilter === st.id
                    ? isDark
                      ? 'bg-slate-800 border-indigo-400 text-white'
                      : 'bg-slate-800 border-slate-800 text-white'
                    : isDark
                    ? 'bg-slate-950 border-slate-800 text-slate-400'
                    : 'bg-slate-50 border-slate-200 text-slate-600'
                }`}
              >
                {st.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* =====================================================================
          SUB-VIEW 1: CLICKUP GANTT TIMELINE + AI SUPER AGENT + DOCS & DASHBOARD
      ===================================================================== */}
      {subView === 'gantt' && (
        <div className="space-y-5">
          {/* Gantt Chart Card */}
          <div
            className={`rounded-2xl border overflow-hidden shadow-xl ${
              isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'
            }`}
          >
            {/* Gantt Top Bar */}
            <div
              className={`px-5 py-3 border-b flex items-center justify-between ${
                isDark ? 'bg-slate-900/90 border-slate-800' : 'bg-slate-50 border-slate-200'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <Calendar className="w-4 h-4 text-indigo-500" />
                <span className="text-xs font-bold uppercase tracking-wider">
                  Gantt Workstream Timeline — Oct 29 to Nov 4, 2026 ({timeline_days.length} Reporting Days)
                </span>
              </div>
              <div className="flex items-center gap-2 text-[11px] opacity-75">
                <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                <span>Click any purple ✨ icon on a bar to inspect the AI Super Agent blocker callout</span>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full border-collapse min-w-[1050px] table-fixed">
                <thead>
                  <tr
                    className={`border-b text-left text-xs ${
                      isDark ? 'bg-slate-950/70 border-slate-800' : 'bg-slate-100/70 border-slate-200'
                    }`}
                  >
                    <th
                      className={`w-[420px] py-3 px-4 font-bold uppercase tracking-wider border-r ${
                        isDark ? 'border-slate-800 text-slate-300' : 'border-slate-200 text-slate-700'
                      }`}
                    >
                      Product / Project / Workstream ({filteredTasks.length})
                    </th>
                    {timeline_days.map((d) => (
                      <th
                        key={d}
                        className={`py-2.5 px-3 text-center border-r last:border-r-0 ${
                          isDark ? 'border-slate-800/80' : 'border-slate-200'
                        }`}
                      >
                        <div className="font-bold text-xs">{DAY_HEADERS[d]?.top || d}</div>
                        <div className="text-[10px] font-mono opacity-60">{DAY_HEADERS[d]?.sub || ''}</div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className={`divide-y ${isDark ? 'divide-slate-800/70' : 'divide-slate-200'}`}>
                  {filteredTasks.map((task) => {
                    const pMeta = PRODUCT_META[task.product] || PRODUCT_META.TRM;
                    const sMeta = STATUS_META[task.status] || STATUS_META.in_progress;
                    const startIdx = Math.max(0, timeline_days.indexOf(task.start_day));
                    const endIdx = Math.max(startIdx, timeline_days.indexOf(task.end_day));
                    const spanCols = endIdx - startIdx + 1;
                    const doneSubtasks = (task.subtasks || []).filter((s) => s.done).length;
                    const totalSubtasks = (task.subtasks || []).length || 1;
                    const pct = Math.round((doneSubtasks / totalSubtasks) * 100);
                    const isAgentOpen = activeAgentTaskId === task.id && task.ai_agent_note;

                    return (
                      <React.Fragment key={task.id}>
                        <tr
                          onClick={() => task.source_cell && onInspectCell && onInspectCell(task.source_cell)}
                          className={`cursor-pointer transition ${
                            isDark ? 'hover:bg-slate-900/60' : 'hover:bg-indigo-50/30'
                          }`}
                        >
                          {/* Left Name Column */}
                          <td
                            className={`py-3 px-4 border-r ${
                              isDark ? 'border-slate-800' : 'border-slate-200'
                            }`}
                          >
                            <div className="flex items-start gap-2.5">
                              <span
                                className={`mt-0.5 px-2 py-0.5 rounded text-[10px] font-bold border shrink-0 ${
                                  isDark ? pMeta.badgeDark : pMeta.badgeLight
                                }`}
                              >
                                {task.product}
                              </span>
                              <div className="min-w-0 flex-1">
                                <div className="text-xs font-bold leading-snug truncate" title={task.title}>
                                  {task.title}
                                </div>
                                <div className="flex items-center gap-2 mt-1 text-[11px] opacity-70">
                                  <span className="truncate">{task.project}</span>
                                  <span>·</span>
                                  <span className="font-semibold text-indigo-400 shrink-0">
                                    {task.assignee}
                                  </span>
                                </div>
                              </div>
                            </div>
                          </td>

                          {/* Timeline Bar Columns */}
                          <td colSpan={timeline_days.length} className="p-0 relative h-14 align-middle">
                            {/* Vertical Day Grid Lines */}
                            <div
                              style={{
                                gridTemplateColumns: `repeat(${timeline_days.length}, minmax(0, 1fr))`,
                              }}
                              className="absolute inset-0 grid pointer-events-none"
                            >
                              {timeline_days.map((d) => (
                                <div
                                  key={d}
                                  className={`border-r last:border-r-0 ${
                                    isDark ? 'border-slate-800/50' : 'border-slate-100'
                                  }`}
                                />
                              ))}
                            </div>

                            {/* Gantt Bar Positioned Across Columns */}
                            <div className="relative z-10 px-2 flex items-center h-full">
                              <div
                                style={{
                                  marginLeft: `${(startIdx / timeline_days.length) * 100}%`,
                                  width: `${(spanCols / timeline_days.length) * 100}%`,
                                }}
                                className="flex items-center gap-2"
                              >
                                <div
                                  className={`h-8 w-full rounded-full bg-gradient-to-r ${sMeta.barColor} p-1 flex items-center justify-between shadow-md text-white text-[11px] font-semibold`}
                                >
                                  <div className="flex items-center gap-2 pl-2 truncate">
                                    <span className="w-5 h-5 rounded-full bg-black/25 flex items-center justify-center text-[10px] font-bold shrink-0">
                                      {getInitials(task.assignee)}
                                    </span>
                                    <span className="truncate">{sMeta.label}</span>
                                  </div>
                                  <div className="flex items-center gap-1.5 pr-2 shrink-0">
                                    <span className="text-[10px] font-mono bg-black/25 px-1.5 py-0.5 rounded-full">
                                      {doneSubtasks}/{totalSubtasks} ({pct}%)
                                    </span>
                                    {task.ai_agent_note && (
                                      <button
                                        onClick={(e) => {
                                          e.stopPropagation();
                                          setActiveAgentTaskId(isAgentOpen ? null : task.id);
                                        }}
                                        className="w-5 h-5 rounded-full bg-purple-900/90 hover:bg-purple-800 border border-purple-300/60 flex items-center justify-center text-purple-200 shadow cursor-pointer"
                                        title="Toggle Super Agent Insight"
                                      >
                                        <Sparkles className="w-3 h-3" />
                                      </button>
                                    )}
                                  </div>
                                </div>
                              </div>
                            </div>
                          </td>
                        </tr>

                        {/* ClickUp "Super Agent" Callout Row when active */}
                        {isAgentOpen && (
                          <tr className={isDark ? 'bg-purple-950/20' : 'bg-purple-50/60'}>
                            <td colSpan={timeline_days.length + 1} className="px-6 py-2.5">
                              <div className="flex items-center justify-between gap-4 rounded-xl bg-gradient-to-r from-purple-600/95 to-indigo-600/95 text-white px-4 py-2.5 shadow-lg">
                                <div className="flex items-center gap-3 text-xs">
                                  <div className="w-7 h-7 rounded-full bg-white/20 flex items-center justify-center shrink-0">
                                    <Sparkles className="w-4 h-4 text-amber-300" />
                                  </div>
                                  <div>
                                    <span className="font-bold text-purple-100 uppercase tracking-wider text-[10px] block">
                                      Super Agent · {task.product} Coordinator
                                    </span>
                                    <span className="font-medium">{task.ai_agent_note}</span>
                                  </div>
                                </div>
                                <button
                                  onClick={() => setActiveAgentTaskId(null)}
                                  className="text-xs text-purple-200 hover:text-white px-2 py-1 rounded bg-black/20 cursor-pointer shrink-0"
                                >
                                  Dismiss
                                </button>
                              </div>
                            </td>
                          </tr>
                        )}
                      </React.Fragment>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Bottom Split: ClickUp "Docs: AI Product Brief" (Left) + "Dashboard: By Assignee & In Flight" (Right) */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
            {/* Left 6 Cols: AI Product Brief (ClickUp Docs Card) */}
            <div
              className={`lg:col-span-6 rounded-2xl border p-6 space-y-4 shadow-lg ${
                isDark ? 'bg-slate-900/70 border-indigo-500/40' : 'bg-white border-indigo-200'
              }`}
            >
              <div className="flex items-center justify-between border-b pb-3 border-slate-500/20">
                <div className="flex items-center gap-2 text-xs font-bold text-indigo-500">
                  <FileText className="w-4 h-4" />
                  <span>Docs · AI Product Brief</span>
                </div>
                <span className="text-[11px] opacity-60 font-mono">
                  Synced from raw-emails.md
                </span>
              </div>

              <div>
                <h3 className="text-lg font-bold">{activeBriefProduct.brief.title}</h3>
                <div className="flex items-center gap-2 mt-1 text-xs opacity-75">
                  <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                  <span>{activeBriefProduct.brief.agent_author} · Live {timeline_days.length}-Day Synthesis</span>
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="text-xs font-bold uppercase tracking-wider opacity-60">
                  Product Overview
                </div>
                <p className="text-xs leading-relaxed opacity-90">
                  {activeBriefProduct.brief.overview}
                </p>
              </div>

              <div className="space-y-2">
                <div className="text-xs font-bold uppercase tracking-wider text-emerald-500">
                  Key Deliverables &amp; Highlights
                </div>
                <ul className="space-y-1.5 text-xs">
                  {activeBriefProduct.brief.highlights.map((hl, i) => (
                    <li key={i} className="flex items-start gap-2 leading-relaxed">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                      <span>{hl}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="space-y-2 pt-1">
                <div className="text-xs font-bold uppercase tracking-wider text-rose-500">
                  Active Risks &amp; Leadership Interventions
                </div>
                <ul className="space-y-1.5 text-xs">
                  {activeBriefProduct.brief.risks.map((rk, i) => (
                    <li key={i} className="flex items-start gap-2 leading-relaxed">
                      <AlertTriangle className="w-3.5 h-3.5 text-rose-500 shrink-0 mt-0.5" />
                      <span>{rk}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Right 6 Cols: ClickUp Dashboard Card (Tasks by Assignee + Workstreams in Flight) */}
            <div
              className={`lg:col-span-6 rounded-2xl border p-6 space-y-5 shadow-lg ${
                isDark ? 'bg-slate-900/70 border-purple-500/40' : 'bg-white border-purple-200'
              }`}
            >
              <div className="flex items-center justify-between border-b pb-3 border-slate-500/20">
                <div className="flex items-center gap-2 text-xs font-bold text-purple-500">
                  <BarChart3 className="w-4 h-4" />
                  <span>Dashboard · Engineering Telemetry</span>
                </div>
                <span className="text-[11px] font-mono opacity-60">
                  {selectedProduct === 'ALL' ? 'All 4 Products' : selectedProduct}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
                {/* Left Mini-Widget: Subtasks by Assignee Vertical Bar Chart */}
                <div className="space-y-3">
                  <div className="text-xs font-bold">Deliverables by Assignee</div>
                  <div className="h-44 flex items-end justify-between gap-2 pt-4 px-2 border-b border-slate-500/20">
                    {assigneeBars.slice(0, 7).map((bar, i) => {
                      const heightPct = Math.max(18, Math.round((bar.subtasks / maxSubtasks) * 100));
                      const gradients = [
                        'from-indigo-500 to-blue-400',
                        'from-purple-500 to-indigo-400',
                        'from-orange-500 to-amber-400',
                        'from-pink-500 to-rose-400',
                        'from-emerald-500 to-teal-400',
                        'from-sky-500 to-cyan-400',
                        'from-amber-500 to-yellow-400',
                      ];
                      return (
                        <div
                          key={bar.name}
                          className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end group"
                          title={`${bar.fullName}: ${bar.subtasks} subtasks across ${bar.count} workstreams`}
                        >
                          <span className="text-[10px] font-mono opacity-75">{bar.subtasks}</span>
                          <div
                            style={{ height: `${heightPct}%` }}
                            className={`w-full max-w-[28px] rounded-t-lg bg-gradient-to-t ${
                              gradients[i % gradients.length]
                            } transition-all group-hover:opacity-90`}
                          />
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex items-center justify-between gap-1 px-1">
                    {assigneeBars.slice(0, 7).map((bar) => (
                      <div
                        key={bar.name}
                        className="flex-1 text-center text-[10px] font-medium truncate opacity-75"
                      >
                        {bar.name}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Right Mini-Widget: Workstreams in Flight Breakdown */}
                <div className="space-y-3">
                  <div className="text-xs font-bold">Workstreams in Flight ({filteredTasks.length})</div>
                  <div className="space-y-2.5">
                    {[
                      {
                        key: 'in_progress',
                        label: 'In Progress (Multi-Day)',
                        count: statusBreakdown.in_progress,
                        color: 'bg-sky-500',
                      },
                      {
                        key: 'done',
                        label: 'Done / Shipped',
                        count: statusBreakdown.done,
                        color: 'bg-emerald-500',
                      },
                      {
                        key: 'planned',
                        label: 'Planned Next',
                        count: statusBreakdown.planned,
                        color: 'bg-amber-500',
                      },
                      {
                        key: 'blocked',
                        label: 'Needs Attention / Blocker',
                        count: statusBreakdown.blocked,
                        color: 'bg-rose-500',
                      },
                    ].map((row) => {
                      const pct = filteredTasks.length
                        ? Math.round((row.count / filteredTasks.length) * 100)
                        : 0;
                      return (
                        <div key={row.key} className="space-y-1">
                          <div className="flex items-center justify-between text-xs">
                            <span className="flex items-center gap-2">
                              <span className={`w-2.5 h-2.5 rounded-full ${row.color}`} />
                              <span>{row.label}</span>
                            </span>
                            <span className="font-mono font-bold">
                              {row.count} ({pct}%)
                            </span>
                          </div>
                          <div
                            className={`h-2 w-full rounded-full overflow-hidden ${
                              isDark ? 'bg-slate-800' : 'bg-slate-100'
                            }`}
                          >
                            <div
                              style={{ width: `${pct}%` }}
                              className={`h-full rounded-full ${row.color}`}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* =====================================================================
          SUB-VIEW 2: CLICKUP HIERARCHICAL TASK LIST (Product -> Project -> Subtasks)
      ===================================================================== */}
      {subView === 'list' && (
        <div className="space-y-4">
          {products
            .filter((p) => selectedProduct === 'ALL' || p.id === selectedProduct)
            .map((prod) => {
              const prodTasks = filteredTasks.filter((t) => t.product === prod.id);
              if (prodTasks.length === 0) return null;
              const pMeta = PRODUCT_META[prod.id] || PRODUCT_META.TRM;
              const ProdIcon = pMeta.icon;

              return (
                <div
                  key={prod.id}
                  className={`rounded-2xl border overflow-hidden ${
                    isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
                  }`}
                >
                  {/* Product Group Header */}
                  <div
                    className={`px-5 py-3 border-b flex items-center justify-between ${
                      isDark ? 'bg-slate-900 border-slate-800' : 'bg-slate-50 border-slate-200'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <ProdIcon className="w-4 h-4 text-indigo-500" />
                      <span className="font-bold text-sm">{prod.full_name}</span>
                      <span className="text-xs font-mono opacity-60">({prodTasks.length} workstreams)</span>
                    </div>
                  </div>

                  <div className={`divide-y ${isDark ? 'divide-slate-800/70' : 'divide-slate-200'}`}>
                    {prodTasks.map((task) => {
                      const sMeta = STATUS_META[task.status] || STATUS_META.in_progress;
                      const isExpanded = expandedTaskIds.has(task.id);

                      return (
                        <div key={task.id} className="p-4 space-y-2.5">
                          <div className="flex flex-wrap items-center justify-between gap-3">
                            <div className="flex items-start gap-2.5 flex-1 min-w-[280px]">
                              <button
                                onClick={() => toggleExpandTask(task.id)}
                                className="mt-0.5 p-1 rounded hover:bg-slate-500/10 cursor-pointer"
                              >
                                {isExpanded ? (
                                  <ChevronDown className="w-4 h-4" />
                                ) : (
                                  <ChevronRight className="w-4 h-4" />
                                )}
                              </button>
                              <div>
                                <div className="flex flex-wrap items-center gap-2">
                                  <span className="text-xs font-semibold text-indigo-400">
                                    [{task.project}]
                                  </span>
                                  <span
                                    onClick={() => task.source_cell && onInspectCell && onInspectCell(task.source_cell)}
                                    className="text-sm font-bold hover:underline cursor-pointer"
                                  >
                                    {task.title}
                                  </span>
                                </div>
                                <div className="flex flex-wrap items-center gap-1.5 mt-1">
                                  {task.tags.map((tg) => (
                                    <span
                                      key={tg}
                                      className={`px-2 py-0.5 rounded text-[10px] font-mono border ${
                                        isDark
                                          ? 'bg-slate-950 border-slate-800 text-slate-300'
                                          : 'bg-slate-100 border-slate-200 text-slate-700'
                                      }`}
                                    >
                                      {tg}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            </div>

                            <div className="flex items-center gap-3">
                              <span className="text-xs font-medium opacity-80">{task.assignee}</span>
                              <span className="text-[11px] font-mono opacity-60">
                                {task.days_active}d active
                              </span>
                              <span
                                className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${
                                  isDark ? sMeta.dark : sMeta.light
                                }`}
                              >
                                {sMeta.label}
                              </span>
                            </div>
                          </div>

                          {isExpanded && (
                            <div className="pl-8 space-y-2 pt-1">
                              <ul className="space-y-1.5 text-xs">
                                {task.subtasks.map((st, idx) => (
                                  <li key={idx} className="flex items-center gap-2">
                                    <span
                                      className={`w-4 h-4 rounded flex items-center justify-center text-[10px] font-bold ${
                                        st.done
                                          ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                                          : 'bg-amber-500/15 text-amber-400 border border-amber-500/40'
                                      }`}
                                    >
                                      {st.done ? '✓' : '→'}
                                    </span>
                                    <span className={st.done ? 'opacity-85' : 'font-semibold'}>
                                      {st.text}
                                    </span>
                                  </li>
                                ))}
                              </ul>
                              {task.ai_agent_note && (
                                <div className="p-2.5 rounded-xl bg-purple-500/10 border border-purple-500/30 text-xs flex items-center gap-2">
                                  <Sparkles className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                                  <span>
                                    <strong>Super Agent:</strong> {task.ai_agent_note}
                                  </span>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
        </div>
      )}

      {/* =====================================================================
          SUB-VIEW 3: CLICKUP KANBAN BOARD
      ===================================================================== */}
      {subView === 'board' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {['blocked', 'in_progress', 'planned', 'done'].map((stKey) => {
            const sMeta = STATUS_META[stKey];
            const colTasks = filteredTasks.filter((t) => t.status === stKey);

            return (
              <div
                key={stKey}
                className={`rounded-2xl border p-3.5 space-y-3 flex flex-col ${
                  isDark ? 'bg-slate-900/40 border-slate-800' : 'bg-slate-100/70 border-slate-200'
                }`}
              >
                <div className="flex items-center justify-between px-1">
                  <div className="flex items-center gap-2">
                    <span className={`w-2.5 h-2.5 rounded-full ${sMeta.dot}`} />
                    <span className="text-xs font-bold uppercase tracking-wider">{sMeta.label}</span>
                  </div>
                  <span className="text-xs font-mono opacity-60">{colTasks.length}</span>
                </div>

                <div className="space-y-3 flex-1">
                  {colTasks.map((task) => {
                    const pMeta = PRODUCT_META[task.product] || PRODUCT_META.TRM;
                    return (
                      <div
                        key={task.id}
                        onClick={() => task.source_cell && onInspectCell && onInspectCell(task.source_cell)}
                        className={`rounded-xl border p-3.5 space-y-2.5 cursor-pointer transition shadow-sm ${
                          isDark
                            ? 'bg-slate-950/90 border-slate-800 hover:border-indigo-500/60'
                            : 'bg-white border-slate-200 hover:border-indigo-400'
                        }`}
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                              isDark ? pMeta.badgeDark : pMeta.badgeLight
                            }`}
                          >
                            {task.product}
                          </span>
                          <span className="text-[10px] font-mono opacity-60">
                            {task.days_active}d active
                          </span>
                        </div>

                        <div className="text-xs font-bold leading-snug">{task.title}</div>
                        <div className="text-[11px] text-indigo-400 font-medium">{task.project}</div>

                        <div className="pt-2 border-t border-slate-500/20 flex items-center justify-between text-[11px]">
                          <span className="font-medium opacity-80">{task.assignee}</span>
                          <span className="font-mono text-[10px] opacity-60">
                            {(task.subtasks || []).filter((s) => s.done).length}/
                            {(task.subtasks || []).length} subtasks
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
