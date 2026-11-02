import base64
import datetime
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import html2text
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_PATH = BASE_DIR / "credentials.json"
TOKEN_PATH = BASE_DIR / "token.json"
RAW_EMAILS_PATH = BASE_DIR / "raw-emails.md"

REDIRECT_URI = "http://localhost:8765/oauth2callback"
_PENDING_CODE_VERIFIER: Optional[str] = None

# Allow http://localhost for local OAuth2 development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def get_auth_status() -> Dict[str, Any]:
    """Return current OAuth configuration and authentication status."""
    has_credentials = CREDENTIALS_PATH.exists()
    has_token = TOKEN_PATH.exists()
    authenticated = False
    email_address = None
    error = None
    client_type = None

    if has_credentials:
        try:
            raw = json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))
            if "web" in raw:
                client_type = "web"
            elif "installed" in raw:
                client_type = "installed"
        except Exception:
            pass

    if has_token:
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
            if creds and creds.valid:
                authenticated = True
                service = build("gmail", "v1", credentials=creds)
                profile = service.users().getProfile(userId="me").execute()
                email_address = profile.get("emailAddress")
        except Exception as exc:
            error = str(exc)

    return {
        "has_credentials": has_credentials,
        "client_type": client_type,
        "redirect_uri": REDIRECT_URI,
        "has_token": has_token,
        "authenticated": authenticated,
        "email_address": email_address,
        "error": error,
        "credentials_path": str(CREDENTIALS_PATH),
        "raw_emails_path": str(RAW_EMAILS_PATH),
    }


def create_oauth_authorization_url() -> str:
    """Create the Google OAuth2 authorization URL using a fixed redirect URI."""
    global _PENDING_CODE_VERIFIER
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            f"credentials.json not found at {CREDENTIALS_PATH}. Please upload or place your credentials.json file first."
        )

    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_PATH),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    _PENDING_CODE_VERIFIER = getattr(flow, "code_verifier", None)
    return authorization_url


def finish_oauth_flow(full_callback_url: str) -> Dict[str, Any]:
    """Exchange the authorization code from the callback URL for OAuth tokens."""
    normalized_url = full_callback_url.replace("http://127.0.0.1:8765", "http://localhost:8765")
    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_PATH),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    if _PENDING_CODE_VERIFIER:
        flow.code_verifier = _PENDING_CODE_VERIFIER
    flow.fetch_token(authorization_response=normalized_url)
    creds = flow.credentials
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return get_auth_status()


def get_gmail_service():
    """Return an authenticated Gmail API service instance."""
    if not TOKEN_PATH.exists():
        raise PermissionError("Not authenticated with Gmail yet. Please connect your account first.")

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        else:
            raise PermissionError("Gmail token is invalid or expired. Please re-authenticate.")

    return build("gmail", "v1", credentials=creds)


def get_ingested_message_ids() -> Set[str]:
    """Parse raw-emails.md for <!-- gmail-id: ... --> markers."""
    if not RAW_EMAILS_PATH.exists():
        return set()
    content = RAW_EMAILS_PATH.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"<!--\s*gmail-id:\s*([a-zA-Z0-9_-]+)\s*-->", content))


def _decode_base64(data: str) -> str:
    if not data:
        return ""
    padded = data + "=" * (-len(data) % 4)
    raw_bytes = base64.urlsafe_b64decode(padded)
    return raw_bytes.decode("utf-8", errors="replace")


def _html_to_markdown(html_content: str) -> str:
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0
    converter.unicode_snob = True
    md = converter.handle(html_content)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md


def _extract_body_from_payload(payload: Dict[str, Any]) -> str:
    """Extract plain text or HTML-converted markdown from a Gmail message payload."""
    plain_parts: List[str] = []
    html_parts: List[str] = []

    def walk_parts(part: Dict[str, Any]):
        mime_type = part.get("mimeType", "")
        body_data = part.get("body", {}).get("data")
        parts = part.get("parts", [])

        if mime_type == "text/plain" and body_data:
            plain_parts.append(_decode_base64(body_data))
        elif mime_type == "text/html" and body_data:
            html_parts.append(_decode_base64(body_data))

        for subpart in parts:
            walk_parts(subpart)

    walk_parts(payload)

    if plain_parts:
        text = "\n\n".join(p.strip() for p in plain_parts if p.strip())
        if text:
            return re.sub(r"\n{3,}", "\n\n", text).strip()

    if html_parts:
        combined_html = "\n".join(html_parts)
        return _html_to_markdown(combined_html)

    return ""


def parse_message_detail(msg: Dict[str, Any], ingested_ids: Optional[Set[str]] = None) -> Dict[str, Any]:
    """Convert a raw Gmail API message resource into a clean dictionary."""
    msg_id = msg.get("id", "")
    thread_id = msg.get("threadId", "")
    snippet = msg.get("snippet", "")
    internal_date_ms = int(msg.get("internalDate", "0"))
    dt = datetime.datetime.fromtimestamp(internal_date_ms / 1000.0, tz=datetime.timezone.utc).astimezone()

    payload = msg.get("payload", {})
    headers = {h["name"].lower(): h["value"] for h in payload.get("headers", []) if "name" in h and "value" in h}

    subject = headers.get("subject", "(No Subject)")
    sender = headers.get("from", "Unknown Sender")
    recipient = headers.get("to", "")
    cc = headers.get("cc", "")
    date_header = headers.get("date", dt.strftime("%Y-%m-%d %H:%M:%S %z"))
    labels = msg.get("labelIds", [])

    body = _extract_body_from_payload(payload)
    if not body:
        body = snippet

    return {
        "id": msg_id,
        "thread_id": thread_id,
        "subject": subject,
        "from": sender,
        "to": recipient,
        "cc": cc,
        "date": date_header,
        "iso_date": dt.strftime("%Y-%m-%d %H:%M"),
        "timestamp": internal_date_ms,
        "snippet": snippet,
        "labels": labels,
        "body": body,
        "ingested": (msg_id in ingested_ids) if ingested_ids is not None else False,
    }


def build_gmail_query(start_date: str, end_date: str, extra_query: str = "") -> str:
    """
    Build Gmail search query for a date range.
    start_date and end_date are YYYY-MM-DD strings.
    Note: Gmail's `before:` operator is exclusive of the date, so we add 1 day to end_date.
    """
    query_parts: List[str] = []
    if start_date:
        query_parts.append(f"after:{start_date.replace('-', '/')}")
    if end_date:
        end_dt = datetime.date.fromisoformat(end_date) + datetime.timedelta(days=1)
        query_parts.append(f"before:{end_dt.strftime('%Y/%m/%d')}")
    if extra_query and extra_query.strip():
        query_parts.append(f"({extra_query.strip()})")
    return " ".join(query_parts)


def fetch_emails(
    start_date: str,
    end_date: str,
    extra_query: str = "",
    max_results: int = 100,
) -> Dict[str, Any]:
    """Fetch messages matching the date range and optional Gmail query."""
    service = get_gmail_service()
    query = build_gmail_query(start_date, end_date, extra_query)
    ingested_ids = get_ingested_message_ids()

    response = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )
    message_refs = response.get("messages", [])

    emails: List[Dict[str, Any]] = []
    for ref in message_refs:
        msg_data = (
            service.users()
            .messages()
            .get(userId="me", id=ref["id"], format="full")
            .execute()
        )
        emails.append(parse_message_detail(msg_data, ingested_ids))

    emails.sort(key=lambda x: x["timestamp"], reverse=True)
    return {
        "query": query,
        "count": len(emails),
        "emails": emails,
    }


def format_email_as_markdown(email_item: Dict[str, Any]) -> str:
    """Format a parsed email dictionary as a Markdown section for raw-emails.md."""
    lines = [
        f"<!-- gmail-id: {email_item['id']} -->",
        f"## {email_item['subject']}",
        "",
        f"- **From:** {email_item['from']}",
        f"- **To:** {email_item['to']}",
    ]
    if email_item.get("cc"):
        lines.append(f"- **Cc:** {email_item['cc']}")
    lines.extend(
        [
            f"- **Date:** {email_item['date']}",
            f"- **Gmail ID:** `{email_item['id']}`",
            "",
            email_item.get("body", "").strip(),
            "",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def ingest_emails_to_markdown(
    message_ids: List[str],
    skip_duplicates: bool = True,
) -> Dict[str, Any]:
    """Fetch the specified Gmail message IDs and append them to raw-emails.md."""
    service = get_gmail_service()
    existing_ids = get_ingested_message_ids()

    added_count = 0
    skipped_count = 0
    blocks: List[str] = []

    for msg_id in message_ids:
        if skip_duplicates and msg_id in existing_ids:
            skipped_count += 1
            continue

        msg_data = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="full")
            .execute()
        )
        parsed = parse_message_detail(msg_data, existing_ids)
        blocks.append(format_email_as_markdown(parsed))
        existing_ids.add(msg_id)
        added_count += 1

    if blocks:
        if not RAW_EMAILS_PATH.exists() or RAW_EMAILS_PATH.stat().st_size == 0:
            header = "# Ingested Team Emails\n\n"
            RAW_EMAILS_PATH.write_text(header + "\n".join(blocks), encoding="utf-8")
        else:
            existing_text = RAW_EMAILS_PATH.read_text(encoding="utf-8", errors="replace")
            separator = "\n\n" if not existing_text.endswith("\n\n") else ""
            RAW_EMAILS_PATH.write_text(
                existing_text + separator + "\n".join(blocks),
                encoding="utf-8",
            )

    return {
        "added": added_count,
        "skipped": skipped_count,
        "total_ingested": len(existing_ids),
        "raw_emails_path": str(RAW_EMAILS_PATH),
    }
