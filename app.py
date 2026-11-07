import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from gmail_service import (
    CREDENTIALS_PATH,
    RAW_EMAILS_PATH,
    TOKEN_PATH,
    create_oauth_authorization_url,
    fetch_emails,
    finish_oauth_flow,
    get_auth_status,
    ingest_emails_to_markdown,
)
from standup_analyzer import parse_standup_dashboard

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"
FRONTEND_PUBLIC_DIR = BASE_DIR / "frontend" / "public"

app = FastAPI(title="Team Emails Gmail Ingestor & AI Standup Hub")


class IngestRequest(BaseModel):
    message_ids: List[str]
    skip_duplicates: bool = True


class CredentialsPayload(BaseModel):
    json_content: str


@app.get("/api/status")
def api_status():
    return get_auth_status()


@app.post("/api/credentials/upload")
async def upload_credentials(file: UploadFile = File(...)):
    try:
        raw = await file.read()
        parsed = json.loads(raw.decode("utf-8"))
        if "installed" not in parsed and "web" not in parsed:
            raise ValueError("Invalid Google OAuth credentials JSON: expected 'installed' or 'web' key.")
        CREDENTIALS_PATH.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
        return get_auth_status()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/credentials/paste")
def paste_credentials(payload: CredentialsPayload):
    try:
        parsed = json.loads(payload.json_content)
        if "installed" not in parsed and "web" not in parsed:
            raise ValueError("Invalid Google OAuth credentials JSON: expected 'installed' or 'web' key.")
        CREDENTIALS_PATH.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
        return get_auth_status()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/auth/connect")
def api_connect():
    try:
        auth_url = create_oauth_authorization_url()
        return {"auth_url": auth_url}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/oauth2callback")
def oauth2callback(request: Request):
    try:
        finish_oauth_flow(str(request.url))
        return RedirectResponse(url="http://localhost:8765/?connected=1")
    except Exception as exc:
        return HTMLResponse(
            content=f"""
            <html>
              <body style="background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:40px;">
                <h2 style="color:#f43f5e;">OAuth Callback Error</h2>
                <pre style="background:#1e293b;padding:16px;border-radius:8px;">{exc}</pre>
                <p><a href="http://localhost:8765" style="color:#818cf8;">← Return to Team Emails Ingestor</a></p>
              </body>
            </html>
            """,
            status_code=400,
        )


@app.post("/api/auth/disconnect")
def api_disconnect():
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
    return get_auth_status()


@app.get("/api/emails")
def api_list_emails(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD"),
    q: str = Query("", description="Optional Gmail search filter"),
    max_results: int = Query(100, ge=1, le=500),
):
    try:
        return fetch_emails(
            start_date=start_date,
            end_date=end_date,
            extra_query=q,
            max_results=max_results,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/ingest")
def api_ingest(req: IngestRequest):
    if not req.message_ids:
        raise HTTPException(status_code=400, detail="No message IDs selected for ingestion.")
    try:
        res = ingest_emails_to_markdown(
            message_ids=req.message_ids,
            skip_duplicates=req.skip_duplicates,
        )
        if FRONTEND_PUBLIC_DIR.exists():
            dashboard_data = parse_standup_dashboard()
            (FRONTEND_PUBLIC_DIR / "standup-dashboard.json").write_text(
                json.dumps(dashboard_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        return res
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/standup-dashboard")
def api_standup_dashboard():
    try:
        return parse_standup_dashboard()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/raw-emails")
def api_get_raw_emails():
    content = ""
    if RAW_EMAILS_PATH.exists():
        content = RAW_EMAILS_PATH.read_text(encoding="utf-8", errors="replace")
    return {
        "path": str(RAW_EMAILS_PATH),
        "size_bytes": len(content.encode("utf-8")),
        "content": content,
    }


@app.delete("/api/raw-emails")
def api_clear_raw_emails():
    RAW_EMAILS_PATH.write_text("", encoding="utf-8")
    return {"status": "cleared", "path": str(RAW_EMAILS_PATH)}


if (FRONTEND_DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST_DIR / "assets")), name="assets")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/standup-dashboard.json")
def serve_static_snapshot():
    if (FRONTEND_DIST_DIR / "standup-dashboard.json").exists():
        return FileResponse(str(FRONTEND_DIST_DIR / "standup-dashboard.json"))
    if (FRONTEND_PUBLIC_DIR / "standup-dashboard.json").exists():
        return FileResponse(str(FRONTEND_PUBLIC_DIR / "standup-dashboard.json"))
    return parse_standup_dashboard()


@app.get("/")
@app.get("/project-tracker")
@app.get("/{developer_slug}")
def serve_index(developer_slug: str = ""):
    if (FRONTEND_DIST_DIR / "index.html").exists():
        return FileResponse(str(FRONTEND_DIST_DIR / "index.html"))
    return FileResponse(str(STATIC_DIR / "index.html"))
