import React, { useState, useEffect, useRef } from 'react';
import {
  Grid,
  GitCompare,
  Sparkles,
  Mail,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  MessageSquare,
  Copy,
  Check,
  RefreshCw,
  Eye,
  Calendar,
  Users,
  Code2,
  ArrowRight,
  Clock,
  Filter,
  ChevronDown,
  ChevronUp,
  Terminal,
  X,
  Sun,
  Moon,
  Search,
  Layers,
  Maximize2,
  Minimize2,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import ProductTrackerView from './ProductTrackerView.jsx';

const DAY_LABELS = {
  '2026-10-29': { short: 'Day 1 · Thu, Oct 29', date: '2026-10-29' },
  '2026-10-30': { short: 'Day 2 · Fri, Oct 30', date: '2026-10-30' },
  '2026-10-31': { short: 'Day 3 · Sat, Oct 31', date: '2026-10-31' },
};

function formatDayHeader(dayStr, idx) {
  if (DAY_LABELS[dayStr]) return DAY_LABELS[dayStr].short;
  return `Day ${idx + 1} · ${dayStr}`;
}

function getScoreStyles(score, isDark) {
  const styles = {
    green: isDark
      ? {
          badgeBg: 'bg-emerald-950/90 text-emerald-300 border-emerald-700/70',
          cardBorder: 'border-emerald-800/50 hover:border-emerald-500/80',
          cardBg: 'bg-slate-900/70 hover:bg-slate-900',
          headerStripe: 'bg-emerald-500',
          learnBox: 'bg-emerald-950/40 border-emerald-800/60 text-emerald-200',
          dot: 'bg-emerald-400',
        }
      : {
          badgeBg: 'bg-emerald-50 text-emerald-800 border-emerald-300',
          cardBorder: 'border-emerald-200 hover:border-emerald-500',
          cardBg: 'bg-white hover:bg-emerald-50/20 shadow-sm',
          headerStripe: 'bg-emerald-500',
          learnBox: 'bg-emerald-50/90 border-emerald-200 text-emerald-900',
          dot: 'bg-emerald-600',
        },
    amber: isDark
      ? {
          badgeBg: 'bg-amber-950/90 text-amber-300 border-amber-700/70',
          cardBorder: 'border-amber-800/50 hover:border-amber-500/80',
          cardBg: 'bg-slate-900/70 hover:bg-slate-900',
          headerStripe: 'bg-amber-500',
          learnBox: 'bg-amber-950/40 border-amber-800/60 text-amber-200',
          dot: 'bg-amber-400',
        }
      : {
          badgeBg: 'bg-amber-50 text-amber-800 border-amber-300',
          cardBorder: 'border-amber-200 hover:border-amber-500',
          cardBg: 'bg-white hover:bg-amber-50/20 shadow-sm',
          headerStripe: 'bg-amber-500',
          learnBox: 'bg-amber-50/90 border-amber-200 text-amber-900',
          dot: 'bg-amber-600',
        },
    red: isDark
      ? {
          badgeBg: 'bg-rose-950/90 text-rose-300 border-rose-700/70',
          cardBorder: 'border-rose-800/60 hover:border-rose-500/80',
          cardBg: 'bg-slate-900/70 hover:bg-slate-900',
          headerStripe: 'bg-rose-500',
          learnBox: 'bg-rose-950/40 border-rose-800/60 text-rose-200',
          dot: 'bg-rose-400',
        }
      : {
          badgeBg: 'bg-rose-50 text-rose-800 border-rose-300',
          cardBorder: 'border-rose-200 hover:border-rose-500',
          cardBg: 'bg-white hover:bg-rose-50/20 shadow-sm',
          headerStripe: 'bg-rose-500',
          learnBox: 'bg-rose-50/90 border-rose-200 text-rose-900',
          dot: 'bg-rose-600',
        },
  };
  return styles[score] || styles.green;
}

function getPvaStatusStyles(status, isDark) {
  const map = {
    aligned: {
      bg: isDark
        ? 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60'
        : 'bg-emerald-50 text-emerald-800 border-emerald-300',
      icon: CheckCircle2,
      label: 'Aligned',
    },
    carryover: {
      bg: isDark
        ? 'bg-sky-950/80 text-sky-300 border-sky-700/60'
        : 'bg-sky-50 text-sky-800 border-sky-300',
      icon: RefreshCw,
      label: 'Multi-Day Carryover',
    },
    pivoted: {
      bg: isDark
        ? 'bg-amber-950/80 text-amber-300 border-amber-700/60'
        : 'bg-amber-50 text-amber-800 border-amber-300',
      icon: AlertTriangle,
      label: 'Scope Pivot / Expanded',
    },
    missing: {
      bg: isDark
        ? 'bg-rose-950/80 text-rose-300 border-rose-700/60'
        : 'bg-rose-50 text-rose-800 border-rose-300',
      icon: XCircle,
      label: 'Missing Report',
    },
  };
  return map[status] || map.aligned;
}

export default function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('nsoft_standup_theme') || 'dark';
  });
  const isDark = theme === 'dark';

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
    localStorage.setItem('nsoft_standup_theme', theme);
  }, [theme, isDark]);

  const [currentRoute, setCurrentRoute] = useState(() =>
    window.location.pathname.startsWith('/project-tracker') ? '/project-tracker' : '/'
  );
  const isProjectTrackerPage = currentRoute === '/project-tracker';

  useEffect(() => {
    const onPopState = () => {
      setCurrentRoute(
        window.location.pathname.startsWith('/project-tracker') ? '/project-tracker' : '/'
      );
      setHoveredCell(null);
    };
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  const navigateTo = (path) => {
    window.history.pushState({}, '', path);
    setCurrentRoute(path);
    setHoveredCell(null);
  };

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('matrix'); // 'matrix' | 'pva' | 'learning' | 'ingest'

  // Filters & UX Controls for Matrix
  const [scoreFilter, setScoreFilter] = useState('all');
  const [projectFilter, setProjectFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [compactMode, setCompactMode] = useState(false);

  // Filters for Plan-vs-Actual
  const [pvaDayPair, setPvaDayPair] = useState('all');
  const [pvaStatusFilter, setPvaStatusFilter] = useState('all');

  // Filters for Learning Scorer
  const [learningFilter, setLearningFilter] = useState('all');

  // Hover, Pinned Cell & Engineer Journey Modal state
  const [hoveredCell, setHoveredCell] = useState(null);
  const [hoverPos, setHoverPos] = useState({ x: 0, y: 0 });
  const [pinnedCell, setPinnedCell] = useState(null);
  const [selectedPersonJourney, setSelectedPersonJourney] = useState(null);
  const [copiedId, setCopiedId] = useState(null);
  const hoverTimeoutRef = useRef(null);
  const searchInputRef = useRef(null);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/standup-dashboard');
      if (!res.ok) throw new Error('Failed to load standup analysis');
      const json = await res.json();
      setData(json);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  // Keyboard shortcuts: Esc closes modals, `/` focuses search, Left/Right steps days in pinned modal
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setPinnedCell(null);
        setSelectedPersonJourney(null);
        setHoveredCell(null);
      } else if (
        e.key === '/' &&
        document.activeElement?.tagName !== 'INPUT' &&
        document.activeElement?.tagName !== 'TEXTAREA'
      ) {
        e.preventDefault();
        searchInputRef.current?.focus();
      } else if (pinnedCell && data?.days) {
        const curIdx = data.days.indexOf(pinnedCell.day);
        if (e.key === 'ArrowRight' && curIdx < data.days.length - 1) {
          const nextCell = data.matrix[pinnedCell.person_email]?.[data.days[curIdx + 1]];
          if (nextCell) setPinnedCell(nextCell);
        } else if (e.key === 'ArrowLeft' && curIdx > 0) {
          const prevCell = data.matrix[pinnedCell.person_email]?.[data.days[curIdx - 1]];
          if (prevCell) setPinnedCell(prevCell);
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [pinnedCell, data]);

  const handleCopyText = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2200);
  };

  const handleCellMouseEnter = (e, cell) => {
    if (!cell) return;
    if (hoverTimeoutRef.current) clearTimeout(hoverTimeoutRef.current);
    const rect = e.currentTarget.getBoundingClientRect();
    const viewportW = window.innerWidth;
    const viewportH = window.innerHeight;

    let x = rect.right + 14;
    if (x + 480 > viewportW) {
      x = Math.max(16, rect.left - 494);
    }
    let y = Math.min(Math.max(16, rect.top - 10), viewportH - 480);

    setHoverPos({ x, y });
    setHoveredCell(cell);
  };

  const handleCellMouseLeave = () => {
    hoverTimeoutRef.current = setTimeout(() => {
      setHoveredCell(null);
    }, 140);
  };

  if (loading && !data) {
    return (
      <div
        className={`min-h-screen flex items-center justify-center ${
          isDark ? 'bg-slate-950 text-slate-200' : 'bg-slate-50 text-slate-800'
        }`}
      >
        <div className="flex flex-col items-center gap-3">
          <RefreshCw className="w-7 h-7 text-indigo-500 animate-spin" />
          <p className="text-sm font-medium opacity-80">Analyzing NSoft Team Standup Emails...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <div className="bg-rose-950/40 border border-rose-800 rounded-2xl p-6 max-w-md space-y-3">
          <div className="font-semibold text-base">Error Loading Standup Hub</div>
          <p className="text-xs opacity-80">{error}</p>
          <button
            onClick={fetchDashboard}
            className="px-4 py-2 rounded-lg bg-rose-600 text-white text-xs font-semibold"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const {
    days = [],
    people = [],
    matrix = {},
    plan_vs_actual = [],
    product_tracker = null,
    summary = {},
  } = data || {};

  const allProjects = Array.from(
    new Set(people.flatMap((p) => days.flatMap((d) => matrix[p.email]?.[d]?.projects || [])))
  ).sort();

  return (
    <div
      className={`min-h-screen flex flex-col transition-colors duration-150 ${
        isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'
      }`}
    >
      {/* Top Header & Executive Telemetry Bar */}
      <header
        className={`sticky top-0 z-30 border-b backdrop-blur-md ${
          isDark
            ? 'border-slate-800/90 bg-slate-950/95'
            : 'border-slate-200 bg-white/95 shadow-xs'
        }`}
      >
        <div className="max-w-[1600px] mx-auto px-6 py-3 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div
              className={`w-10 h-10 rounded-xl border flex items-center justify-center shadow-inner ${
                isDark
                  ? 'bg-gradient-to-br from-indigo-500/30 to-emerald-500/20 border-indigo-500/40 text-indigo-300'
                  : 'bg-gradient-to-br from-indigo-50 to-emerald-50 border-indigo-200 text-indigo-600'
              }`}
            >
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-base font-bold tracking-tight">
                  {isProjectTrackerPage
                    ? 'NSoft Product & Task Tracker'
                    : 'NSoft AI-Native Standup Intelligence Hub'}
                </h1>
                {/* Route Switcher between `/` and `/project-tracker` */}
                <div
                  className={`flex items-center rounded-xl p-0.5 border text-xs ${
                    isDark ? 'bg-slate-900 border-slate-800' : 'bg-slate-100 border-slate-200'
                  }`}
                >
                  <a
                    href="/"
                    onClick={(e) => {
                      e.preventDefault();
                      navigateTo('/');
                    }}
                    className={`px-2.5 py-1 rounded-lg font-semibold transition ${
                      !isProjectTrackerPage
                        ? 'bg-indigo-600 text-white shadow-xs'
                        : isDark
                        ? 'text-slate-400 hover:text-white'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    Standup Hub
                  </a>
                  <a
                    href="/project-tracker"
                    onClick={(e) => {
                      e.preventDefault();
                      navigateTo('/project-tracker');
                    }}
                    className={`px-2.5 py-1 rounded-lg font-semibold transition flex items-center gap-1 ${
                      isProjectTrackerPage
                        ? 'bg-indigo-600 text-white shadow-xs'
                        : isDark
                        ? 'text-slate-400 hover:text-white'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    <Layers className="w-3 h-3" />
                    <span>/project-tracker</span>
                  </a>
                </div>
              </div>
              <p className={`text-xs ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
                {isProjectTrackerPage
                  ? 'ClickUp-Style Portfolio Tracker · TRM · ERP · KPTCL · Infra & Security'
                  : 'Work Done · Plans for Tomorrow · Learnings Quality & Coaching Telemetry'}
              </p>
            </div>
          </div>

          {/* Search + KPI Pills + Theme Toggle */}
          <div className="flex flex-wrap items-center gap-2.5">
            {/* Global Search Bar */}
            <div className="relative">
              <Search
                className={`w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 ${
                  isDark ? 'text-slate-400' : 'text-slate-500'
                }`}
              />
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search person, table, project... (/)"
                className={`pl-8 pr-7 py-1.5 rounded-xl text-xs border w-56 focus:w-68 transition-all focus:outline-none ${
                  isDark
                    ? 'bg-slate-900 border-slate-800 text-slate-100 placeholder-slate-500 focus:border-indigo-500'
                    : 'bg-slate-100 border-slate-200 text-slate-900 placeholder-slate-400 focus:bg-white focus:border-indigo-500'
                }`}
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 cursor-pointer"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>

            <div
              className={`px-3 py-1.5 rounded-xl border flex items-center gap-2 text-xs ${
                isDark
                  ? 'bg-slate-900 border-slate-800 text-slate-300'
                  : 'bg-slate-100 border-slate-200 text-slate-700'
              }`}
            >
              <Users className="w-3.5 h-3.5 text-indigo-500" />
              <span>
                Sent:{' '}
                <strong className={isDark ? 'text-white' : 'text-slate-900'}>
                  {summary.submitted_reports}/{summary.expected_reports}
                </strong>
                <span className="text-emerald-500 font-semibold ml-1">
                  ({summary.submission_rate_pct}%)
                </span>
              </span>
            </div>

            <button
              onClick={() => {
                setActiveTab('learning');
                setLearningFilter('green');
              }}
              className={`px-3 py-1.5 rounded-xl border flex items-center gap-1.5 text-xs font-semibold transition cursor-pointer ${
                isDark
                  ? 'bg-emerald-950/50 hover:bg-emerald-950/80 border-emerald-800/60 text-emerald-200'
                  : 'bg-emerald-50 hover:bg-emerald-100 border-emerald-200 text-emerald-800'
              }`}
              title="Click to view Specific Technical Insights"
            >
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>{summary.green_learnings} Specific</span>
            </button>

            <button
              onClick={() => {
                setActiveTab('learning');
                setLearningFilter('amber');
              }}
              className={`px-3 py-1.5 rounded-xl border flex items-center gap-1.5 text-xs font-semibold transition cursor-pointer ${
                isDark
                  ? 'bg-amber-950/50 hover:bg-amber-950/80 border-amber-800/60 text-amber-200'
                  : 'bg-amber-50 hover:bg-amber-100 border-amber-200 text-amber-800'
              }`}
              title="Click to view Repeated Generic Boilerplate"
            >
              <span className="w-2 h-2 rounded-full bg-amber-500" />
              <span>{summary.amber_learnings} Boilerplate</span>
            </button>

            <button
              onClick={() => {
                setActiveTab('learning');
                setLearningFilter('red');
              }}
              className={`px-3 py-1.5 rounded-xl border flex items-center gap-1.5 text-xs font-semibold transition cursor-pointer ${
                isDark
                  ? 'bg-rose-950/50 hover:bg-rose-950/80 border-rose-800/60 text-rose-200'
                  : 'bg-rose-50 hover:bg-rose-100 border-rose-200 text-rose-800'
              }`}
              title="Click to view Blockers & Missing Sections"
            >
              <span className="w-2 h-2 rounded-full bg-rose-500" />
              <span>{summary.red_learnings} Blockers</span>
            </button>

            {/* Dark / Light Mode Toggle Button */}
            <button
              onClick={() => setTheme(isDark ? 'light' : 'dark')}
              className={`px-3 py-1.5 rounded-xl border flex items-center gap-1.5 text-xs font-semibold transition cursor-pointer ${
                isDark
                  ? 'bg-slate-900 hover:bg-slate-800 border-slate-700 text-amber-300'
                  : 'bg-slate-100 hover:bg-slate-200 border-slate-300 text-slate-800'
              }`}
              title={`Switch to ${isDark ? 'Light' : 'Dark'} Mode`}
            >
              {isDark ? (
                <>
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  <span>Light</span>
                </>
              ) : (
                <>
                  <Moon className="w-3.5 h-3.5 text-indigo-600" />
                  <span>Dark</span>
                </>
              )}
            </button>

            <button
              onClick={fetchDashboard}
              className={`p-2 rounded-xl border transition cursor-pointer ${
                isDark
                  ? 'bg-slate-900 hover:bg-slate-800 border-slate-800 text-slate-300'
                  : 'bg-slate-100 hover:bg-slate-200 border-slate-200 text-slate-700'
              }`}
              title="Refresh analysis from raw-emails.md"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Navigation Tabs (only shown on the Standup Hub `/` page) */}
        {!isProjectTrackerPage && (
          <div
            className={`max-w-[1600px] mx-auto px-6 flex items-center justify-between border-t ${
              isDark ? 'border-slate-900 bg-slate-950/60' : 'border-slate-200/80 bg-slate-50/70'
            }`}
          >
            <nav className="flex items-center gap-1 -mb-px overflow-x-auto">
              <TabButton
                isDark={isDark}
                active={activeTab === 'matrix'}
                onClick={() => setActiveTab('matrix')}
                icon={Grid}
                label="People × Days Matrix"
                badge={`${people.length} × ${days.length}`}
              />
              <TabButton
                isDark={isDark}
                active={activeTab === 'pva'}
                onClick={() => setActiveTab('pva')}
                icon={GitCompare}
                label="Plan-vs-Actual Tracker"
                badge="Yesterday's Plan → Today's Done"
              />
              <TabButton
                isDark={isDark}
                active={activeTab === 'learning'}
                onClick={() => setActiveTab('learning')}
                icon={Sparkles}
                label="Learning Quality Scorer & Coaching"
                badge={`${summary.green_learnings}G · ${summary.amber_learnings}A`}
              />
            </nav>

            <div
              className={`hidden xl:flex items-center gap-2 text-[11px] py-2 ${
                isDark ? 'text-slate-400' : 'text-slate-500'
              }`}
            >
              <Eye className="w-3.5 h-3.5 text-indigo-500" />
              <span>
                <strong>Hover</strong> any cell for raw email · <strong>Click cell</strong> to pin ·{' '}
                <strong>Click Engineer Name</strong> for 3-Day Journey
              </span>
            </div>
          </div>
        )}
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-[1600px] w-full mx-auto px-6 py-5">
        {isProjectTrackerPage ? (
          <ProductTrackerView
            isDark={isDark}
            productTracker={product_tracker}
            searchQuery={searchQuery}
            onInspectCell={(cell) => setPinnedCell(cell)}
          />
        ) : (
          <>
            {activeTab === 'matrix' && (
              <MatrixView
                isDark={isDark}
                days={days}
                people={people}
                matrix={matrix}
                scoreFilter={scoreFilter}
                setScoreFilter={setScoreFilter}
                projectFilter={projectFilter}
                setProjectFilter={setProjectFilter}
                searchQuery={searchQuery}
                compactMode={compactMode}
                setCompactMode={setCompactMode}
                allProjects={allProjects}
                onCellMouseEnter={handleCellMouseEnter}
                onCellMouseLeave={handleCellMouseLeave}
                onCellClick={(cell) => setPinnedCell(cell)}
                onSelectPersonJourney={(person) => setSelectedPersonJourney(person)}
              />
            )}

            {activeTab === 'pva' && (
              <PlanVsActualView
                isDark={isDark}
                days={days}
                planVsActual={plan_vs_actual}
                pvaDayPair={pvaDayPair}
                setPvaDayPair={setPvaDayPair}
                pvaStatusFilter={pvaStatusFilter}
                setPvaStatusFilter={setPvaStatusFilter}
                searchQuery={searchQuery}
                onInspectCell={(cell) => setPinnedCell(cell)}
                onCellMouseEnter={handleCellMouseEnter}
                onCellMouseLeave={handleCellMouseLeave}
              />
            )}

            {activeTab === 'learning' && (
              <LearningQualityView
                isDark={isDark}
                days={days}
                people={people}
                matrix={matrix}
                learningFilter={learningFilter}
                setLearningFilter={setLearningFilter}
                searchQuery={searchQuery}
                onInspectCell={(cell) => setPinnedCell(cell)}
                onCellMouseEnter={handleCellMouseEnter}
                onCellMouseLeave={handleCellMouseLeave}
                onCopyText={handleCopyText}
                copiedId={copiedId}
              />
            )}
          </>
        )}
      </main>

      {/* Floating Hover Raw-Email Popover */}
      {hoveredCell && !pinnedCell && !selectedPersonJourney && (
        <div
          style={{ left: `${hoverPos.x}px`, top: `${hoverPos.y}px` }}
          className={`fixed z-50 w-[480px] max-h-[460px] rounded-2xl shadow-2xl flex flex-col overflow-hidden pointer-events-none backdrop-blur-md border ${
            isDark
              ? 'bg-slate-900/98 border-indigo-500/60 text-slate-100 shadow-black/80'
              : 'bg-white/98 border-indigo-400 text-slate-900 shadow-slate-400/50'
          }`}
        >
          <div
            className={`px-4 py-2.5 border-b flex items-center justify-between ${
              isDark ? 'bg-slate-950 border-slate-800' : 'bg-indigo-50/70 border-indigo-100'
            }`}
          >
            <div className="flex items-center gap-2">
              <Terminal className="w-3.5 h-3.5 text-indigo-500" />
              <span className="text-xs font-bold">
                Raw Email · {hoveredCell.person_name} ({hoveredCell.day})
              </span>
            </div>
            <span
              className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                isDark
                  ? 'text-indigo-300 bg-indigo-950/70 border-indigo-800/60'
                  : 'text-indigo-700 bg-white border-indigo-200'
              }`}
            >
              Click cell to pin/scroll
            </span>
          </div>
          <div
            className={`px-4 py-2 border-b text-[11px] font-mono space-y-0.5 ${
              isDark
                ? 'bg-slate-900/90 border-slate-800/80 text-slate-300'
                : 'bg-slate-50 border-slate-200 text-slate-700'
            }`}
          >
            <div className="truncate">
              <span className="opacity-60">Subject:</span>{' '}
              <span className={!hoveredCell.has_subject ? 'text-rose-500 italic' : 'font-semibold'}>
                {hoveredCell.subject}
              </span>
            </div>
            <div className="truncate">
              <span className="opacity-60">Date:</span> {hoveredCell.date}
            </div>
            <div className="truncate">
              <span className="opacity-60">To:</span> {hoveredCell.to}
            </div>
          </div>
          <div className={`p-4 overflow-y-auto flex-1 ${isDark ? 'bg-slate-950/90' : 'bg-white'}`}>
            <pre
              className={`whitespace-pre-wrap font-mono text-[11px] leading-relaxed ${
                isDark ? 'text-slate-200' : 'text-slate-800'
              }`}
            >
              {hoveredCell.raw_body}
            </pre>
            {hoveredCell.manager_reply && (
              <div className="mt-3 pt-3 border-t border-indigo-500/30">
                <div className="text-[10px] font-bold uppercase tracking-wider text-indigo-500 mb-1">
                  Manager Reply ({hoveredCell.manager_reply.from} · {hoveredCell.manager_reply.date_short}):
                </div>
                <pre
                  className={`whitespace-pre-wrap font-mono text-[11px] p-2.5 rounded-lg border ${
                    isDark
                      ? 'text-indigo-200 bg-indigo-950/40 border-indigo-800/50'
                      : 'text-indigo-900 bg-indigo-50 border-indigo-200'
                  }`}
                >
                  {hoveredCell.manager_reply.body}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Pinned Cell Modal (with Left/Right Day Stepper) */}
      {pinnedCell && (
        <div
          className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-6"
          onClick={() => setPinnedCell(null)}
        >
          <div
            className={`border rounded-2xl max-w-4xl w-full max-h-[88vh] flex flex-col shadow-2xl overflow-hidden ${
              isDark ? 'bg-slate-900 border-slate-700 text-slate-100' : 'bg-white border-slate-300 text-slate-900'
            }`}
            onClick={(e) => e.stopPropagation()}
          >
            <div
              className={`px-6 py-4 border-b flex items-center justify-between ${
                isDark ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200'
              }`}
            >
              <div>
                <div className="flex items-center gap-2.5">
                  <h3 className="text-base font-bold">
                    {pinnedCell.person_name} — {pinnedCell.day}
                  </h3>
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
                      getScoreStyles(pinnedCell.learning_eval.score, isDark).badgeBg
                    }`}
                  >
                    {pinnedCell.learning_eval.badge}
                  </span>
                </div>
                <p className="text-xs opacity-60 font-mono mt-0.5">
                  Gmail ID: {pinnedCell.gmail_id} · {pinnedCell.date}
                </p>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[11px] opacity-60 hidden sm:inline mr-1">
                  Use ← / → keys to switch days
                </span>
                <button
                  onClick={() => setPinnedCell(null)}
                  className={`p-1.5 rounded-lg border cursor-pointer ${
                    isDark
                      ? 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-300'
                      : 'bg-white hover:bg-slate-100 border-slate-300 text-slate-700'
                  }`}
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left: Structured AI Analysis & Coaching */}
              <div className="space-y-4">
                <div
                  className={`p-4 rounded-xl border space-y-2.5 ${
                    isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-slate-50 border-slate-200'
                  }`}
                >
                  <div className="text-xs font-bold uppercase tracking-wider text-indigo-500">
                    AI Analysis &amp; Observations
                  </div>
                  <ul className="space-y-1.5 text-xs">
                    {pinnedCell.ai_analysis.map((note, idx) => (
                      <li key={idx} className="leading-relaxed">
                        {note}
                      </li>
                    ))}
                  </ul>
                  {pinnedCell.learning_eval.entities?.length > 0 && (
                    <div className="pt-2 flex flex-wrap gap-1.5">
                      {pinnedCell.learning_eval.entities.map((ent) => (
                        <span
                          key={ent}
                          className={`px-2 py-0.5 rounded border text-[11px] font-mono ${
                            isDark
                              ? 'bg-indigo-950/80 border-indigo-700/50 text-indigo-200'
                              : 'bg-indigo-50 border-indigo-200 text-indigo-800'
                          }`}
                        >
                          {ent}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {pinnedCell.learning_eval.coaching_nudge && (
                  <div
                    className={`p-4 rounded-xl border space-y-2 ${
                      isDark
                        ? 'bg-amber-950/30 border-amber-700/50 text-amber-100'
                        : 'bg-amber-50 border-amber-300 text-amber-950'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold uppercase tracking-wider text-amber-500">
                        Suggested Coaching Reply
                      </span>
                      <button
                        onClick={() =>
                          handleCopyText(
                            pinnedCell.learning_eval.coaching_nudge,
                            `modal-${pinnedCell.gmail_id}`
                          )
                        }
                        className="px-2.5 py-1 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs flex items-center gap-1.5 cursor-pointer"
                      >
                        {copiedId === `modal-${pinnedCell.gmail_id}` ? (
                          <>
                            <Check className="w-3.5 h-3.5" /> Copied!
                          </>
                        ) : (
                          <>
                            <Copy className="w-3.5 h-3.5" /> Copy Coaching Nudge
                          </>
                        )}
                      </button>
                    </div>
                    <p className="text-xs leading-relaxed italic">
                      "{pinnedCell.learning_eval.coaching_nudge}"
                    </p>
                  </div>
                )}

                <div
                  className={`p-4 rounded-xl border space-y-3 text-xs ${
                    isDark ? 'bg-slate-950/60 border-slate-800' : 'bg-slate-50 border-slate-200'
                  }`}
                >
                  <div>
                    <div className="font-bold opacity-60 uppercase text-[11px] mb-1">
                      Parsed Work Done ({pinnedCell.work_done.length})
                    </div>
                    <ul className="list-disc list-inside space-y-1">
                      {pinnedCell.work_done.map((w, i) => (
                        <li key={i}>{w}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <div className="font-bold opacity-60 uppercase text-[11px] mb-1">
                      Parsed Tomorrow's Plan ({pinnedCell.plan_tomorrow.length})
                    </div>
                    {pinnedCell.plan_tomorrow.length > 0 ? (
                      <ul className="list-disc list-inside space-y-1">
                        {pinnedCell.plan_tomorrow.map((p, i) => (
                          <li key={i}>{p}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-rose-500 italic">No plan section included in email.</p>
                    )}
                  </div>
                  <div>
                    <div className="font-bold opacity-60 uppercase text-[11px] mb-1">
                      Parsed Learnings ({pinnedCell.learnings.length})
                    </div>
                    {pinnedCell.learnings.length > 0 ? (
                      <ul className="list-disc list-inside space-y-1">
                        {pinnedCell.learnings.map((l, i) => (
                          <li key={i}>{l}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-rose-500 italic">No separate learnings section included.</p>
                    )}
                  </div>
                </div>
              </div>

              {/* Right: Raw Email Content As-Is */}
              <div
                className={`flex flex-col border rounded-xl overflow-hidden ${
                  isDark ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200'
                }`}
              >
                <div
                  className={`px-4 py-2.5 border-b flex items-center justify-between ${
                    isDark ? 'bg-slate-900 border-slate-800' : 'bg-slate-100 border-slate-200'
                  }`}
                >
                  <span className="text-xs font-semibold font-mono">
                    raw-emails.md (As-Is Content)
                  </span>
                  <button
                    onClick={() => handleCopyText(pinnedCell.raw_body, `raw-${pinnedCell.gmail_id}`)}
                    className={`px-2.5 py-1 rounded border text-xs flex items-center gap-1 cursor-pointer ${
                      isDark
                        ? 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-200'
                        : 'bg-white hover:bg-slate-50 border-slate-300 text-slate-700'
                    }`}
                  >
                    {copiedId === `raw-${pinnedCell.gmail_id}` ? (
                      <>
                        <Check className="w-3 h-3 text-emerald-500" /> Copied
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" /> Copy Raw
                      </>
                    )}
                  </button>
                </div>
                <pre className="p-4 whitespace-pre-wrap font-mono text-xs leading-relaxed overflow-y-auto flex-1">
                  {pinnedCell.raw_body}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Engineer 3-Day Journey Modal (when clicking an Engineer's Name) */}
      {selectedPersonJourney && (
        <div
          className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-6"
          onClick={() => setSelectedPersonJourney(null)}
        >
          <div
            className={`border rounded-2xl max-w-5xl w-full max-h-[88vh] flex flex-col shadow-2xl overflow-hidden ${
              isDark ? 'bg-slate-900 border-slate-700 text-slate-100' : 'bg-white border-slate-300 text-slate-900'
            }`}
            onClick={(e) => e.stopPropagation()}
          >
            <div
              className={`px-6 py-4 border-b flex items-center justify-between ${
                isDark ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200'
              }`}
            >
              <div>
                <h3 className="text-base font-bold">
                  {selectedPersonJourney.name} — 3-Day Engineering Progression
                </h3>
                <p className="text-xs opacity-60 font-mono">
                  {selectedPersonJourney.email} · {selectedPersonJourney.role}
                </p>
              </div>
              <button
                onClick={() => setSelectedPersonJourney(null)}
                className={`p-1.5 rounded-lg border cursor-pointer ${
                  isDark
                    ? 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-300'
                    : 'bg-white hover:bg-slate-100 border-slate-300 text-slate-700'
                }`}
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto grid grid-cols-1 md:grid-cols-3 gap-4">
              {days.map((d, idx) => {
                const cell = matrix[selectedPersonJourney.email]?.[d];
                if (!cell) {
                  return (
                    <div
                      key={d}
                      className="rounded-xl border border-dashed border-rose-500/40 p-4 flex flex-col items-center justify-center text-center"
                    >
                      <XCircle className="w-6 h-6 text-rose-500 mb-2" />
                      <div className="text-xs font-bold">{formatDayHeader(d, idx)}</div>
                      <p className="text-xs opacity-60 mt-1">No report submitted on this day.</p>
                    </div>
                  );
                }
                const st = getScoreStyles(cell.learning_eval.score, isDark);
                return (
                  <div
                    key={d}
                    className={`rounded-xl border p-4 space-y-3 flex flex-col justify-between ${st.cardBorder} ${st.cardBg}`}
                  >
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-indigo-500">
                          {formatDayHeader(d, idx)}
                        </span>
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${st.badgeBg}`}>
                          {cell.learning_eval.score.toUpperCase()}
                        </span>
                      </div>
                      <div>
                        <div className="text-[10px] font-bold uppercase opacity-60 mb-1">Work Done</div>
                        <ul className="list-disc list-inside text-xs space-y-1">
                          {cell.work_done.map((w, i) => (
                            <li key={i}>{w}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <div className="text-[10px] font-bold uppercase opacity-60 mb-1">Plan for Tomorrow</div>
                        <ul className="list-disc list-inside text-xs space-y-1 opacity-85">
                          {cell.plan_tomorrow.map((p, i) => (
                            <li key={i}>{p}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    <div className={`p-2.5 rounded-lg border text-xs ${st.learnBox}`}>
                      <div className="text-[10px] font-bold uppercase opacity-75 mb-0.5">Learning</div>
                      {cell.learnings.length > 0 ? cell.learnings.join(' ') : cell.learning_eval.reason}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function TabButton({ isDark, active, onClick, icon: Icon, label, badge }) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-3 text-xs font-semibold border-b-2 flex items-center gap-2 transition cursor-pointer ${
        active
          ? isDark
            ? 'border-indigo-500 text-white bg-indigo-950/30'
            : 'border-indigo-600 text-indigo-950 bg-indigo-50/70'
          : isDark
          ? 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
          : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
      }`}
    >
      <Icon className={`w-4 h-4 ${active ? 'text-indigo-500' : 'opacity-60'}`} />
      <span>{label}</span>
      {badge && (
        <span
          className={`px-2 py-0.5 rounded-full text-[10px] font-mono border ${
            active
              ? isDark
                ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30'
                : 'bg-indigo-100 text-indigo-800 border-indigo-200'
              : isDark
              ? 'bg-slate-900 text-slate-400 border-slate-800'
              : 'bg-slate-100 text-slate-600 border-slate-200'
          }`}
        >
          {badge}
        </span>
      )}
    </button>
  );
}

/* ============================================================================
   TAB 1: PEOPLE × DAYS MATRIX GRID VIEW
============================================================================ */
function MatrixView({
  isDark,
  days,
  people,
  matrix,
  scoreFilter,
  setScoreFilter,
  projectFilter,
  setProjectFilter,
  searchQuery,
  compactMode,
  setCompactMode,
  allProjects,
  onCellMouseEnter,
  onCellMouseLeave,
  onCellClick,
  onSelectPersonJourney,
}) {
  const q = searchQuery.trim().toLowerCase();

  return (
    <div className="space-y-4">
      {/* Filter & Density Bar */}
      <div
        className={`border rounded-2xl p-3.5 flex flex-wrap items-center justify-between gap-3 ${
          isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-semibold opacity-70 flex items-center gap-1.5 mr-1">
            <Filter className="w-3.5 h-3.5 text-indigo-500" /> Filter Cells:
          </span>
          {[
            { id: 'all', label: 'All Updates' },
            { id: 'green', label: '🟢 Specific Technical Insights' },
            { id: 'amber', label: '🟡 Generic Boilerplate' },
            { id: 'red', label: '🔴 Blockers / Missing Info' },
            { id: 'replied', label: '💬 Sumukh Replied / Nudged' },
          ].map((btn) => (
            <button
              key={btn.id}
              onClick={() => setScoreFilter(btn.id)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition cursor-pointer ${
                scoreFilter === btn.id
                  ? isDark
                    ? 'bg-indigo-600/25 border-indigo-500 text-white shadow-xs'
                    : 'bg-indigo-600 border-indigo-600 text-white shadow-xs'
                  : isDark
                  ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                  : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
              }`}
            >
              {btn.label}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          {/* Compact vs Detailed Density Toggle */}
          <button
            onClick={() => setCompactMode(!compactMode)}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium border flex items-center gap-1.5 cursor-pointer transition ${
              compactMode
                ? isDark
                  ? 'bg-indigo-950/70 border-indigo-500/60 text-indigo-200'
                  : 'bg-indigo-50 border-indigo-300 text-indigo-800'
                : isDark
                ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
            }`}
            title="Toggle between high-density overview and full bullet view"
          >
            {compactMode ? <Maximize2 className="w-3.5 h-3.5" /> : <Minimize2 className="w-3.5 h-3.5" />}
            <span>{compactMode ? 'Detailed View' : 'Compact View'}</span>
          </button>

          <div className="flex items-center gap-1.5">
            <select
              value={projectFilter}
              onChange={(e) => setProjectFilter(e.target.value)}
              className={`border rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:border-indigo-500 ${
                isDark
                  ? 'bg-slate-950 border-slate-800 text-slate-200'
                  : 'bg-slate-50 border-slate-200 text-slate-800'
              }`}
            >
              <option value="all">All Projects ({allProjects.length})</option>
              {allProjects.map((proj) => (
                <option key={proj} value={proj}>
                  {proj}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* People × Days Matrix Table */}
      <div
        className={`overflow-x-auto rounded-2xl border shadow-xl ${
          isDark ? 'border-slate-800 bg-slate-900/30' : 'border-slate-200 bg-white'
        }`}
      >
        <table className="w-full border-collapse table-fixed min-w-[1150px]">
          <thead>
            <tr
              className={`border-b text-left ${
                isDark ? 'bg-slate-900/95 border-slate-800' : 'bg-slate-100/90 border-slate-200'
              }`}
            >
              <th
                className={`w-[220px] py-3.5 px-4 text-xs font-bold uppercase tracking-wider border-r ${
                  isDark ? 'text-slate-300 border-slate-800' : 'text-slate-700 border-slate-200'
                }`}
              >
                Team Member ({people.length})
              </th>
              {days.map((dayStr, idx) => (
                <th
                  key={dayStr}
                  className={`py-3.5 px-4 text-xs font-bold uppercase tracking-wider border-r last:border-r-0 ${
                    isDark ? 'text-slate-200 border-slate-800' : 'text-slate-800 border-slate-200'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-2">
                      <Calendar className="w-3.5 h-3.5 text-indigo-500" />
                      {formatDayHeader(dayStr, idx)}
                    </span>
                    <span className="text-[11px] font-mono opacity-60 font-normal">
                      {people.filter((p) => Boolean(matrix[p.email]?.[dayStr])).length}/{people.length} sent
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className={`divide-y ${isDark ? 'divide-slate-800/80' : 'divide-slate-200'}`}>
            {people.map((person) => {
              const personCells = days.map((d) => matrix[person.email]?.[d] || null);

              if (
                projectFilter !== 'all' &&
                !personCells.some((c) => c && c.projects.includes(projectFilter))
              ) {
                return null;
              }

              if (q) {
                const personMatches =
                  person.name.toLowerCase().includes(q) ||
                  person.email.toLowerCase().includes(q) ||
                  person.role.toLowerCase().includes(q) ||
                  personCells.some(
                    (c) =>
                      c &&
                      (c.raw_body.toLowerCase().includes(q) ||
                        c.projects.some((pr) => pr.toLowerCase().includes(q)))
                  );
                if (!personMatches) return null;
              }

              const greenCount = personCells.filter((c) => c?.learning_eval?.score === 'green').length;
              const amberCount = personCells.filter((c) => c?.learning_eval?.score === 'amber').length;
              const sentCount = personCells.filter(Boolean).length;

              return (
                <tr
                  key={person.email}
                  className={`align-top ${isDark ? 'hover:bg-slate-900/20' : 'hover:bg-slate-50/60'}`}
                >
                  {/* Engineer Identity Cell */}
                  <td
                    onClick={() => onSelectPersonJourney(person)}
                    className={`p-4 border-r cursor-pointer transition ${
                      isDark
                        ? 'border-slate-800 bg-slate-950/60 hover:bg-slate-900/80'
                        : 'border-slate-200 bg-slate-50/70 hover:bg-indigo-50/40'
                    }`}
                    title="Click to view 3-Day Engineering Progression"
                  >
                    <div className="space-y-2">
                      <div>
                        <div className="font-bold text-sm flex items-center justify-between">
                          <span>{person.name}</span>
                          <ChevronRight className="w-3.5 h-3.5 opacity-40" />
                        </div>
                        <div className="text-[11px] opacity-60 font-mono truncate">{person.email}</div>
                        <div
                          className={`text-[11px] mt-1 leading-snug font-medium ${
                            isDark ? 'text-indigo-300/90' : 'text-indigo-700'
                          }`}
                        >
                          {person.role}
                        </div>
                      </div>

                      {!compactMode && (
                        <div className="flex flex-wrap gap-1 pt-1">
                          {person.primary_projects.map((proj) => (
                            <span
                              key={proj}
                              className={`px-2 py-0.5 rounded text-[10px] font-medium border ${
                                isDark
                                  ? 'bg-slate-900 text-slate-300 border-slate-800'
                                  : 'bg-white text-slate-700 border-slate-200'
                              }`}
                            >
                              {proj}
                            </span>
                          ))}
                        </div>
                      )}

                      <div
                        className={`pt-2 border-t flex items-center justify-between text-[11px] ${
                          isDark ? 'border-slate-800/80' : 'border-slate-200'
                        }`}
                      >
                        <span className="opacity-75">
                          Sent: <strong>{sentCount}/{days.length}</strong>
                        </span>
                        <div className="flex items-center gap-1">
                          {greenCount > 0 && (
                            <span
                              className={`px-1.5 py-0.5 rounded border text-[10px] font-semibold ${
                                isDark
                                  ? 'bg-emerald-950 text-emerald-300 border-emerald-800/60'
                                  : 'bg-emerald-50 text-emerald-800 border-emerald-200'
                              }`}
                            >
                              {greenCount}G
                            </span>
                          )}
                          {amberCount > 0 && (
                            <span
                              className={`px-1.5 py-0.5 rounded border text-[10px] font-semibold ${
                                isDark
                                  ? 'bg-amber-950 text-amber-300 border-amber-800/60'
                                  : 'bg-amber-50 text-amber-800 border-amber-200'
                              }`}
                            >
                              {amberCount}A
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </td>

                  {/* Day Cells */}
                  {days.map((dayStr) => {
                    const cell = matrix[person.email]?.[dayStr];
                    if (!cell) {
                      return (
                        <td
                          key={dayStr}
                          className={`p-3 border-r last:border-r-0 align-middle ${
                            isDark ? 'border-slate-800/70 bg-slate-950/30' : 'border-slate-200 bg-slate-50/40'
                          }`}
                        >
                          <div
                            className={`h-full ${
                              compactMode ? 'min-h-[84px]' : 'min-h-[180px]'
                            } rounded-xl border border-dashed border-rose-500/40 bg-rose-500/5 p-3 flex flex-col items-center justify-center text-center gap-1`}
                          >
                            <XCircle className="w-4 h-4 text-rose-500/80" />
                            <div className="text-xs font-semibold text-rose-500">No Report Received</div>
                            {!compactMode && (
                              <p className="text-[11px] opacity-60 max-w-[220px]">
                                {person.email === 'rohith.r@nsoft.in'
                                  ? 'Hit Claude weekly limit on Oct 30; did not send Oct 31 update.'
                                  : 'Did not submit a daily work update for this date.'}
                              </p>
                            )}
                          </div>
                        </td>
                      );
                    }

                    const score = cell.learning_eval.score;
                    const style = getScoreStyles(score, isDark);

                    const matchesFilter =
                      (scoreFilter === 'all' ||
                        (scoreFilter === 'replied' ? Boolean(cell.manager_reply) : score === scoreFilter)) &&
                      (projectFilter === 'all' || cell.projects.includes(projectFilter));

                    return (
                      <td
                        key={dayStr}
                        className={`p-3 border-r last:border-r-0 transition-opacity ${
                          isDark ? 'border-slate-800/70' : 'border-slate-200'
                        } ${matchesFilter ? 'opacity-100' : 'opacity-25'}`}
                      >
                        <div
                          onMouseEnter={(e) => onCellMouseEnter(e, cell)}
                          onMouseLeave={onCellMouseLeave}
                          onClick={() => onCellClick(cell)}
                          className={`rounded-xl border ${style.cardBorder} ${style.cardBg} transition-all cursor-pointer flex flex-col overflow-hidden`}
                        >
                          <div className={`h-1 w-full ${style.headerStripe}`} />

                          <div className="p-3 space-y-2.5">
                            {/* Header Row: Learning Quality Badge + Timestamp */}
                            <div className="flex items-center justify-between gap-1.5">
                              <span
                                className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border flex items-center gap-1.5 ${style.badgeBg}`}
                              >
                                <span className={`w-1.5 h-1.5 rounded-full ${style.dot}`} />
                                {cell.learning_eval.badge}
                              </span>
                              <span className="text-[10px] font-mono opacity-60 flex items-center gap-1 shrink-0">
                                <Clock className="w-3 h-3" />
                                {cell.time_short}
                              </span>
                            </div>

                            {/* Project & Warning Badges */}
                            <div className="flex flex-wrap items-center gap-1">
                              {cell.projects.map((proj) => (
                                <span
                                  key={proj}
                                  className={`px-1.5 py-0.5 rounded text-[10px] font-semibold border ${
                                    isDark
                                      ? 'bg-indigo-950/70 text-indigo-300 border-indigo-800/60'
                                      : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                                  }`}
                                >
                                  {proj}
                                </span>
                              ))}
                              {!cell.has_subject && (
                                <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-rose-500/15 text-rose-500 border border-rose-500/30">
                                  ⚠ Blank Subject
                                </span>
                              )}
                              {cell.submitted_late_note && (
                                <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-amber-500/15 text-amber-500 border border-amber-500/30">
                                  ⏰ Late / Revised
                                </span>
                              )}
                            </div>

                            {compactMode ? (
                              /* Compact Gist Mode */
                              <p className="text-xs line-clamp-2 leading-snug opacity-90">{cell.gist}</p>
                            ) : (
                              /* Detailed Mode */
                              <>
                                <div className="space-y-1">
                                  <div className="text-[10px] font-bold uppercase tracking-wider opacity-60">
                                    Work Done ({cell.work_done.length})
                                  </div>
                                  <ul className="space-y-1 text-xs leading-snug">
                                    {cell.work_done.slice(0, 3).map((item, idx) => (
                                      <li key={idx} className="line-clamp-2 flex items-start gap-1.5">
                                        <span className="text-indigo-500 font-bold mt-0.2">•</span>
                                        <span>{item}</span>
                                      </li>
                                    ))}
                                    {cell.work_done.length > 3 && (
                                      <li className="text-[11px] text-indigo-500 font-medium pl-3">
                                        +{cell.work_done.length - 3} more item(s)...
                                      </li>
                                    )}
                                  </ul>
                                </div>

                                <div
                                  className={`space-y-1 pt-1.5 border-t ${
                                    isDark ? 'border-slate-800/70' : 'border-slate-100'
                                  }`}
                                >
                                  <div className="text-[10px] font-bold uppercase tracking-wider opacity-60">
                                    Plan for Tomorrow
                                  </div>
                                  {cell.plan_tomorrow.length > 0 ? (
                                    <p className="text-[11px] opacity-85 line-clamp-2 leading-snug">
                                      → {cell.plan_tomorrow.join(' · ')}
                                    </p>
                                  ) : (
                                    <p className="text-[11px] text-rose-500 italic">
                                      ✕ Omitted Tomorrow's Plan
                                    </p>
                                  )}
                                </div>

                                <div className={`p-2 rounded-lg border text-[11px] leading-snug ${style.learnBox}`}>
                                  <div className="font-bold text-[10px] uppercase tracking-wider opacity-80 mb-0.5">
                                    Learning:
                                  </div>
                                  {cell.learnings.length > 0 ? (
                                    <div className="line-clamp-2">{cell.learnings.join(' ')}</div>
                                  ) : (
                                    <div className="italic">{cell.learning_eval.reason}</div>
                                  )}
                                </div>
                              </>
                            )}

                            {/* Entities & Manager Reply Footer */}
                            <div className="pt-0.5 space-y-1">
                              {!compactMode && cell.learning_eval.entities?.length > 0 && (
                                <div className="flex flex-wrap gap-1">
                                  {cell.learning_eval.entities.slice(0, 4).map((ent) => (
                                    <span
                                      key={ent}
                                      className={`px-1.5 py-0.5 rounded border text-[10px] font-mono ${
                                        isDark
                                          ? 'bg-slate-950 text-slate-300 border-slate-800'
                                          : 'bg-slate-100 text-slate-700 border-slate-200'
                                      }`}
                                    >
                                      {ent}
                                    </span>
                                  ))}
                                </div>
                              )}

                              {cell.manager_reply && (
                                <div
                                  className={`px-2 py-1 rounded text-[10px] font-medium flex items-center gap-1.5 border ${
                                    cell.manager_reply.body.toLowerCase() === 'noted'
                                      ? isDark
                                        ? 'bg-slate-950/90 text-slate-400 border-slate-800'
                                        : 'bg-slate-100 text-slate-600 border-slate-200'
                                      : isDark
                                      ? 'bg-indigo-950/80 text-indigo-200 border-indigo-700/70'
                                      : 'bg-indigo-50 text-indigo-900 border-indigo-200'
                                  }`}
                                >
                                  <MessageSquare className="w-3 h-3 shrink-0 text-indigo-500" />
                                  <span className="truncate">
                                    <strong>Sumukh:</strong> "{cell.manager_reply.body}"
                                  </span>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ============================================================================
   TAB 2: PLAN-VS-ACTUAL SIDE-BY-SIDE TRACKER
============================================================================ */
function PlanVsActualView({
  isDark,
  planVsActual,
  pvaDayPair,
  setPvaDayPair,
  pvaStatusFilter,
  setPvaStatusFilter,
  searchQuery,
  onInspectCell,
  onCellMouseEnter,
  onCellMouseLeave,
}) {
  const pairOptions = Array.from(new Set(planVsActual.map((item) => item.pair_label)));
  const q = searchQuery.trim().toLowerCase();

  const filtered = planVsActual.filter((item) => {
    if (pvaDayPair !== 'all' && item.pair_label !== pvaDayPair) return false;
    if (pvaStatusFilter !== 'all' && item.status !== pvaStatusFilter) return false;
    if (q) {
      const hay = `${item.person_name} ${item.commentary} ${item.planned_items.join(' ')} ${item.actual_items.join(' ')}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  const counts = {
    aligned: planVsActual.filter((i) => i.status === 'aligned').length,
    carryover: planVsActual.filter((i) => i.status === 'carryover').length,
    pivoted: planVsActual.filter((i) => i.status === 'pivoted').length,
    missing: planVsActual.filter((i) => i.status === 'missing').length,
  };

  return (
    <div className="space-y-4">
      <div
        className={`border rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4 ${
          isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-semibold opacity-70 mr-1">Day Transition:</span>
          <button
            onClick={() => setPvaDayPair('all')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition cursor-pointer ${
              pvaDayPair === 'all'
                ? 'bg-indigo-600 border-indigo-600 text-white'
                : isDark
                ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
            }`}
          >
            All Transitions ({planVsActual.length})
          </button>
          {pairOptions.map((label) => (
            <button
              key={label}
              onClick={() => setPvaDayPair(label)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition cursor-pointer ${
                pvaDayPair === label
                  ? 'bg-indigo-600 border-indigo-600 text-white'
                  : isDark
                  ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                  : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {[
            { id: 'all', label: 'All Statuses' },
            { id: 'aligned', label: `✓ Aligned (${counts.aligned})` },
            { id: 'carryover', label: `↻ Carryover (${counts.carryover})` },
            { id: 'pivoted', label: `⚡ Scope Pivot (${counts.pivoted})` },
            { id: 'missing', label: `✕ Missing Report (${counts.missing})` },
          ].map((st) => (
            <button
              key={st.id}
              onClick={() => setPvaStatusFilter(st.id)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition cursor-pointer ${
                pvaStatusFilter === st.id
                  ? isDark
                    ? 'bg-slate-800 border-indigo-400 text-white'
                    : 'bg-indigo-50 border-indigo-500 text-indigo-900 font-semibold'
                  : isDark
                  ? 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200'
                  : 'bg-slate-50 border-slate-200 text-slate-600 hover:text-slate-900'
              }`}
            >
              {st.label}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        {filtered.map((item) => {
          const st = getPvaStatusStyles(item.status, isDark);
          const StatusIcon = st.icon;

          return (
            <div
              key={item.id}
              className={`rounded-2xl border transition p-4 grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch ${
                isDark
                  ? 'border-slate-800 bg-slate-900/50 hover:border-slate-700'
                  : 'border-slate-200 bg-white hover:border-slate-300 shadow-xs'
              }`}
            >
              <div
                className={`lg:col-span-3 flex flex-col justify-between border-b lg:border-b-0 lg:border-r pb-3 lg:pb-0 lg:pr-4 ${
                  isDark ? 'border-slate-800/80' : 'border-slate-200'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-sm">{item.person_name}</span>
                    <span
                      className={`text-[11px] font-mono px-2 py-0.5 rounded border ${
                        isDark
                          ? 'text-indigo-300 bg-indigo-950/60 border-indigo-800/50'
                          : 'text-indigo-700 bg-indigo-50 border-indigo-200'
                      }`}
                    >
                      {item.day_prev.slice(5)} → {item.day_curr.slice(5)}
                    </span>
                  </div>
                  <div className="text-[11px] opacity-60 mt-0.5">{item.person_role}</div>

                  <div className="mt-3">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold border ${st.bg}`}
                    >
                      <StatusIcon className="w-3.5 h-3.5 shrink-0" />
                      <span>{item.badge}</span>
                    </span>
                  </div>
                </div>

                <div
                  className={`mt-3 pt-2 border-t text-xs leading-relaxed ${
                    isDark ? 'border-slate-800/60 text-slate-300' : 'border-slate-100 text-slate-700'
                  }`}
                >
                  <span className="text-indigo-500 font-semibold">AI Continuity Check: </span>
                  {item.commentary}
                </div>
              </div>

              {/* Yesterday's Plan */}
              <div
                onMouseEnter={(e) => item.prev_cell && onCellMouseEnter(e, item.prev_cell)}
                onMouseLeave={onCellMouseLeave}
                onClick={() => item.prev_cell && onInspectCell(item.prev_cell)}
                className={`lg:col-span-4 rounded-xl border p-3.5 flex flex-col justify-between cursor-pointer transition ${
                  isDark
                    ? 'bg-slate-950/70 border-slate-800/90 hover:border-indigo-500/50'
                    : 'bg-amber-50/30 border-slate-200 hover:border-amber-400'
                }`}
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-amber-500">
                      Yesterday's Plan ({item.day_prev})
                    </span>
                    {item.prev_cell && (
                      <span className="text-[10px] font-mono opacity-50">Hover for raw mail</span>
                    )}
                  </div>
                  {item.planned_items.length > 0 ? (
                    <ul className="space-y-1.5 text-xs leading-relaxed">
                      {item.planned_items.map((pl, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-amber-500 font-bold">→</span>
                          <span>{pl}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-xs text-rose-500 italic">No plan was stated on {item.day_prev}.</p>
                  )}
                </div>
              </div>

              {/* Arrow */}
              <div className="hidden lg:flex lg:col-span-1 items-center justify-center">
                <div
                  className={`w-9 h-9 rounded-full border flex items-center justify-center text-indigo-500 ${
                    isDark ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200'
                  }`}
                >
                  <ArrowRight className="w-4 h-4" />
                </div>
              </div>

              {/* Today's Actual Work Done */}
              <div
                onMouseEnter={(e) => item.curr_cell && onCellMouseEnter(e, item.curr_cell)}
                onMouseLeave={onCellMouseLeave}
                onClick={() => item.curr_cell && onInspectCell(item.curr_cell)}
                className={`lg:col-span-4 rounded-xl p-3.5 flex flex-col justify-between transition ${
                  item.curr_cell
                    ? isDark
                      ? 'bg-slate-950/70 border border-slate-800/90 cursor-pointer hover:border-emerald-500/50'
                      : 'bg-emerald-50/30 border border-slate-200 cursor-pointer hover:border-emerald-400'
                    : 'bg-rose-500/5 border border-dashed border-rose-500/40'
                }`}
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-500">
                      Today's Actual Work Done ({item.day_curr})
                    </span>
                    {item.curr_cell && (
                      <span className="text-[10px] font-mono opacity-50">Hover for raw mail</span>
                    )}
                  </div>
                  {item.actual_items.length > 0 ? (
                    <ul className="space-y-1.5 text-xs leading-relaxed">
                      {item.actual_items.map((act, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-emerald-500 font-bold">✓</span>
                          <span>{act}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <div className="py-4 text-center text-xs text-rose-500">
                      ✕ No standup report received for {item.day_curr}.
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ============================================================================
   TAB 3: LEARNING QUALITY SCORER & COACHING HUB
============================================================================ */
function LearningQualityView({
  isDark,
  days,
  people,
  matrix,
  learningFilter,
  setLearningFilter,
  searchQuery,
  onInspectCell,
  onCellMouseEnter,
  onCellMouseLeave,
  onCopyText,
  copiedId,
}) {
  const q = searchQuery.trim().toLowerCase();
  const allEntries = [];
  people.forEach((p) => {
    days.forEach((d) => {
      const cell = matrix[p.email]?.[d];
      if (cell) allEntries.push(cell);
    });
  });

  const filteredEntries = allEntries.filter((c) => {
    if (learningFilter !== 'all' && c.learning_eval.score !== learningFilter) return false;
    if (q) {
      const hay = `${c.person_name} ${c.learnings.join(' ')} ${c.learning_eval.reason} ${c.projects.join(' ')}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  return (
    <div className="space-y-5">
      <div
        className={`border rounded-2xl p-5 flex flex-wrap items-center justify-between gap-4 ${
          isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="max-w-2xl space-y-1">
          <h2 className="text-sm font-bold flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-500" />
            <span>Learning Quality Scorer &amp; 1-Click Coaching Hub</span>
          </h2>
          <p className="text-xs opacity-75 leading-relaxed">
            Automatically separates <strong className="text-emerald-500">Specific Technical Insights (Green)</strong>{' '}
            from <strong className="text-amber-500">Repeated Generic Boilerplate (Amber)</strong> and{' '}
            <strong className="text-rose-500">Tooling Blockers / Missing Sections (Red)</strong>, with tailored coaching prompts ready to copy.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {[
            { id: 'all', label: `All (${allEntries.length})` },
            {
              id: 'green',
              label: `🟢 Specific Technical Insights (${
                allEntries.filter((e) => e.learning_eval.score === 'green').length
              })`,
            },
            {
              id: 'amber',
              label: `🟡 Generic Boilerplate (${
                allEntries.filter((e) => e.learning_eval.score === 'amber').length
              })`,
            },
            {
              id: 'red',
              label: `🔴 Blockers / Missing (${
                allEntries.filter((e) => e.learning_eval.score === 'red').length
              })`,
            },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setLearningFilter(tab.id)}
              className={`px-3.5 py-2 rounded-xl text-xs font-semibold border transition cursor-pointer ${
                learningFilter === tab.id
                  ? 'bg-indigo-600 border-indigo-600 text-white'
                  : isDark
                  ? 'bg-slate-950 border-slate-800 text-slate-300 hover:bg-slate-800'
                  : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredEntries.map((cell) => {
          const score = cell.learning_eval.score;
          const style = getScoreStyles(score, isDark);

          return (
            <div
              key={cell.gmail_id}
              onMouseEnter={(e) => onCellMouseEnter(e, cell)}
              onMouseLeave={onCellMouseLeave}
              onClick={() => onInspectCell(cell)}
              className={`rounded-2xl border ${style.cardBorder} ${style.cardBg} p-4 flex flex-col justify-between gap-3 cursor-pointer transition`}
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-sm">{cell.person_name}</span>
                      <span className="text-xs font-mono opacity-60">{cell.day}</span>
                    </div>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {cell.projects.map((proj) => (
                        <span
                          key={proj}
                          className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${
                            isDark
                              ? 'bg-slate-950 text-indigo-300 border-slate-800'
                              : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                          }`}
                        >
                          {proj}
                        </span>
                      ))}
                    </div>
                  </div>
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${style.badgeBg}`}>
                    {cell.learning_eval.badge}
                  </span>
                </div>

                <div className={`p-3 rounded-xl border ${style.learnBox} space-y-1`}>
                  <div className="text-[10px] font-bold uppercase tracking-wider opacity-75">
                    What Engineer Wrote Under "Learnings":
                  </div>
                  {cell.learnings.length > 0 ? (
                    <p className="text-xs font-medium leading-relaxed">
                      "{cell.learnings.join(' ')}"
                    </p>
                  ) : (
                    <p className="text-xs italic">(No separate 'Learnings' section written in email)</p>
                  )}
                </div>

                <div className="text-xs opacity-85 leading-relaxed">
                  <strong>AI Evaluation: </strong>
                  {cell.learning_eval.reason}
                </div>

                {cell.learning_eval.entities?.length > 0 && (
                  <div className="flex flex-wrap items-center gap-1.5">
                    <Code2 className="w-3.5 h-3.5 text-indigo-500" />
                    {cell.learning_eval.entities.map((ent) => (
                      <span
                        key={ent}
                        className={`px-2 py-0.5 rounded border text-[11px] font-mono ${
                          isDark
                            ? 'bg-slate-950 border-slate-800 text-emerald-300'
                            : 'bg-emerald-50 border-emerald-200 text-emerald-800'
                        }`}
                      >
                        {ent}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {cell.learning_eval.coaching_nudge && (
                <div
                  onClick={(e) => e.stopPropagation()}
                  className={`pt-3 border-t flex items-center justify-between gap-3 ${
                    isDark ? 'border-slate-800/80' : 'border-slate-200'
                  }`}
                >
                  <p className="text-[11px] italic line-clamp-2 opacity-90">
                    💡 <strong>Nudge:</strong> "{cell.learning_eval.coaching_nudge}"
                  </p>
                  <button
                    onClick={() => onCopyText(cell.learning_eval.coaching_nudge, cell.gmail_id)}
                    className={`shrink-0 px-3 py-1.5 rounded-lg border text-xs font-semibold flex items-center gap-1.5 cursor-pointer ${
                      isDark
                        ? 'bg-amber-500/20 hover:bg-amber-500/30 border-amber-500/40 text-amber-200'
                        : 'bg-amber-100 hover:bg-amber-200 border-amber-300 text-amber-900'
                    }`}
                  >
                    {copiedId === cell.gmail_id ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-500" /> Copied
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" /> Copy Nudge
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ============================================================================
   TAB 4: GMAIL SYNC & RAW-EMAILS.MD INGESTION
============================================================================ */
function GmailIngestView({ isDark, onIngestComplete }) {
  const [status, setStatus] = useState(null);
  const [startDate, setStartDate] = useState(() => {
    const d = new Date();
    d.setDate(d.getDate() - 5);
    return d.toISOString().slice(0, 10);
  });
  const [endDate, setEndDate] = useState(() => new Date().toISOString().slice(0, 10));
  const [extraQuery, setExtraQuery] = useState('');
  const [emails, setEmails] = useState([]);
  const [selectedIds, setSelectedIds] = useState(new Set());
  const [fetching, setFetching] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    fetch('/api/status')
      .then((r) => r.json())
      .then(setStatus);
  }, []);

  const handleFetchEmails = async () => {
    setFetching(true);
    try {
      const params = new URLSearchParams({ start_date: startDate, end_date: endDate, q: extraQuery });
      const res = await fetch(`/api/emails?${params.toString()}`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed to fetch emails');
      setEmails(data.emails || []);
      setSelectedIds(new Set((data.emails || []).filter((e) => !e.ingested).map((e) => e.id)));
    } catch (err) {
      setToast({ type: 'error', text: err.message });
    } finally {
      setFetching(false);
    }
  };

  const handleIngest = async () => {
    if (selectedIds.size === 0) return;
    setIngesting(true);
    try {
      const res = await fetch('/api/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message_ids: Array.from(selectedIds),
          skip_duplicates: true,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Ingest failed');
      setToast({
        type: 'success',
        text: `Ingested ${data.added} new email(s) into raw-emails.md! Matrix refreshed.`,
      });
      await handleFetchEmails();
      if (onIngestComplete) onIngestComplete();
    } catch (err) {
      setToast({ type: 'error', text: err.message });
    } finally {
      setIngesting(false);
    }
  };

  return (
    <div className="space-y-4">
      <div
        className={`border rounded-2xl p-5 flex flex-wrap items-end justify-between gap-4 ${
          isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white border-slate-200 shadow-xs'
        }`}
      >
        <div className="flex flex-wrap items-end gap-3">
          <div>
            <label className="block text-[11px] uppercase font-semibold opacity-60 mb-1">Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className={`border rounded-xl px-3 py-1.5 text-xs ${
                isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-slate-50 border-slate-300 text-slate-900'
              }`}
            />
          </div>
          <div>
            <label className="block text-[11px] uppercase font-semibold opacity-60 mb-1">End Date</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className={`border rounded-xl px-3 py-1.5 text-xs ${
                isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-slate-50 border-slate-300 text-slate-900'
              }`}
            />
          </div>
          <div className="min-w-[240px]">
            <label className="block text-[11px] uppercase font-semibold opacity-60 mb-1">
              Optional Gmail Filter
            </label>
            <input
              type="text"
              value={extraQuery}
              onChange={(e) => setExtraQuery(e.target.value)}
              placeholder="e.g. Daily Work Report"
              className={`w-full border rounded-xl px-3 py-1.5 text-xs ${
                isDark ? 'bg-slate-950 border-slate-700 text-white' : 'bg-slate-50 border-slate-300 text-slate-900'
              }`}
            />
          </div>
          <button
            onClick={handleFetchEmails}
            disabled={fetching}
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold cursor-pointer"
          >
            {fetching ? 'Fetching from Gmail...' : 'Fetch Last 5 Days from Gmail'}
          </button>
        </div>

        <div className="flex items-center gap-3">
          {status && (
            <span className="text-xs opacity-75">
              Account: <strong className="text-emerald-500">{status.email_address || 'Not Connected'}</strong>
            </span>
          )}
          <button
            onClick={handleIngest}
            disabled={ingesting || selectedIds.size === 0}
            className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-white text-xs font-semibold cursor-pointer"
          >
            {ingesting ? 'Ingesting...' : `Ingest Selected (${selectedIds.size}) to raw-emails.md`}
          </button>
        </div>
      </div>

      {toast && (
        <div
          className={`p-3.5 rounded-xl border text-xs font-medium ${
            toast.type === 'error'
              ? 'bg-rose-500/15 border-rose-500/40 text-rose-500'
              : 'bg-emerald-500/15 border-emerald-500/40 text-emerald-500'
          }`}
        >
          {toast.text}
        </div>
      )}

      {emails.length > 0 && (
        <div
          className={`rounded-2xl border divide-y ${
            isDark
              ? 'border-slate-800 bg-slate-900/40 divide-slate-800'
              : 'border-slate-200 bg-white divide-slate-200'
          }`}
        >
          {emails.map((email) => (
            <label
              key={email.id}
              className={`p-3.5 flex items-start gap-3 cursor-pointer ${
                isDark ? 'hover:bg-slate-900/70' : 'hover:bg-slate-50'
              }`}
            >
              <input
                type="checkbox"
                checked={selectedIds.has(email.id)}
                onChange={() => {
                  const next = new Set(selectedIds);
                  if (next.has(email.id)) next.delete(email.id);
                  else next.add(email.id);
                  setSelectedIds(next);
                }}
                className="mt-1 rounded text-indigo-600"
              />
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-semibold">{email.subject}</span>
                  <span className="text-[11px] font-mono opacity-60">{email.iso_date}</span>
                </div>
                <div className="text-xs opacity-75">{email.from}</div>
                <div className="text-xs opacity-50 truncate mt-0.5">{email.snippet}</div>
              </div>
              {email.ingested && (
                <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/15 text-emerald-500 border border-emerald-500/30">
                  ✓ Ingested
                </span>
              )}
            </label>
          ))}
        </div>
      )}
    </div>
  );
}
