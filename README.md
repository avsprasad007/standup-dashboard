# Team Emails — Gmail Ingestor

A local web application and Gmail OAuth2 ingestion pipeline that fetches emails from your Gmail account (defaulting to the **last 5 days**), lets you preview and select messages, and appends formatted Markdown into [`raw-emails.md`](./raw-emails.md) with automatic duplicate tracking.

## Quick Start

1. **Start the Web UI:**
   ```bash
   ./start.sh
   ```
   Open **http://127.0.0.1:8765** in your browser.

2. **Configure Gmail OAuth2 (`credentials.json`):**
   - Enable the [Gmail API in Google Cloud Console](https://console.cloud.google.com/apis/library/gmail.googleapis.com).
   - Create an **OAuth client ID** of type **Desktop app** under [Credentials](https://console.cloud.google.com/apis/credentials).
   - Either place the downloaded file at `/Users/avsprasad/Projects/team-emails/credentials.json` or upload/paste it directly inside the UI's **OAuth Settings** modal.
   - Click **Authenticate with Google** to authorize read-only Gmail access (`gmail.readonly`). Your token is stored locally in `token.json`.

3. **Filter, Select & Ingest:**
   - The UI defaults to the **Last 5 Days** (with quick toggles for Today, 5d, 7d, 14d, 30d, or custom Start/End dates, plus optional Gmail search syntax like `from:someone@domain.com` or `label:team`).
   - Preview any email on the right pane, check/uncheck the emails you want, and click **Ingest Selected to raw-emails.md**.
   - Already-ingested emails are tracked via `<!-- gmail-id: ... -->` markers in `raw-emails.md` so you never accidentally duplicate them.
