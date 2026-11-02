# NSoft AI Standup Intelligence Hub & Product Tracker

An AI-native engineering standup & product portfolio dashboard built with **React + Vite + Tailwind CSS** (frontend) and **FastAPI** (optional local parser/Gmail ingestor backend).

## Running on Any Machine (Frontend Only — Zero Python / Gmail Setup Needed)

The repository includes the pre-parsed dataset ([`frontend/public/standup-dashboard.json`](./frontend/public/standup-dashboard.json)) generated from [`raw-emails.md`](./raw-emails.md). You can clone and run the frontend with just **Node.js**:

```bash
git clone https://github.com/avsprasad007/standup-dashboard.git
cd standup-dashboard/frontend
npm install
npm run dev
```

Then open:
- **http://localhost:5173/** — **Standup Intelligence Hub** (People × Days Matrix, Plan-vs-Actual Tracker, Learning Quality Scorer & Coaching Nudges)
- **http://localhost:5173/project-tracker** — **ClickUp-Style Product & Task Tracker** (`TRM`, `ERP`, `KPTCL`, `Infra & Security` Gantt, AI Product Briefs, Kanban & Telemetry)

---

## Optional: Running with Live `raw-emails.md` Parser (Python Backend)

If you edit [`raw-emails.md`](./raw-emails.md) or want to ingest new emails from Gmail later, start the Python backend (still **does not require** `credentials.json` unless you actively trigger Gmail OAuth):

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8765 --reload
```
