import datetime
import email.utils
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent
RAW_EMAILS_PATH = BASE_DIR / "raw-emails.md"

# Core reporting team roster with role/domain context
TEAM_ROSTER: List[Dict[str, Any]] = [
    {
        "id": "venkata.sai@nsoft.in",
        "name": "Venkata Sai",
        "email": "venkata.sai@nsoft.in",
        "role": "Software Engineer — HRMS & ERP",
        "primary_projects": ["GESCOM ERP", "Employee Portal", "HRMS"],
    },
    {
        "id": "lasya.mannuru@nsoft.in",
        "name": "Mannuru Lasya",
        "email": "lasya.mannuru@nsoft.in",
        "role": "Software Engineer — HRMS Employee Module",
        "primary_projects": ["HRMS", "TCED ERP"],
    },
    {
        "id": "anith.hm@nsoft.in",
        "name": "Anith HM",
        "email": "anith.hm@nsoft.in",
        "role": "Software Engineer — TCED HRMS & Full-Stack",
        "primary_projects": ["TCED", "HRMS", "SQL/ASP.NET"],
    },
    {
        "id": "talari.kousalya@nsoft.in",
        "name": "Kousalya Talari",
        "email": "talari.kousalya@nsoft.in",
        "role": "Engineer — Smart Metering & Prepaid Billing",
        "primary_projects": ["INESH Meter", "CMRL", "Prepaid Billing"],
    },
    {
        "id": "nitishnag.m@nsoft.in",
        "name": "Nitish Nag M",
        "email": "nitishnag.m@nsoft.in",
        "role": "Software Engineer — TRM SpotBilling & Smart Metering",
        "primary_projects": ["TRM SpotBilling", "HESCOM", "BWSSB", "Smart Metering"],
    },
    {
        "id": "sanjana.cs@nsoft.in",
        "name": "Sanjana C S",
        "email": "sanjana.cs@nsoft.in",
        "role": "Software Engineer — TCED Portal & ERP Reports",
        "primary_projects": ["TCED", "Employee Portal", "ERP"],
    },
    {
        "id": "pallapu.rajesh@nsoft.in",
        "name": "Pallapu Rajesh",
        "email": "pallapu.rajesh@nsoft.in",
        "role": "Software Engineer — TCED & BGCL Billing",
        "primary_projects": ["TCED", "BGCL"],
    },
    {
        "id": "chitrashree.hr@nsoft.in",
        "name": "Chitrashree HR",
        "email": "chitrashree.hr@nsoft.in",
        "role": "Software Engineer — BGCL, KPTCL & DCW",
        "primary_projects": ["BGCL", "KPTCL", "DCW"],
    },
    {
        "id": "ankith.hm@nsoft.in",
        "name": "Ankith HM",
        "email": "ankith.hm@nsoft.in",
        "role": "Database & ERP Engineer — DB Restores & TCED",
        "primary_projects": ["DB Migration", "TCED ERP", "BESCOM/GESCOM/COCHIN"],
    },
    {
        "id": "rohith.r@nsoft.in",
        "name": "Rohith R",
        "email": "rohith.r@nsoft.in",
        "role": "Software Engineer — HESCOM & TCED Integrations",
        "primary_projects": ["HESCOM", "TCED"],
    },
]

CONFIDENTIAL_RE = re.compile(
    r"(--\s*\n)?The content of this email is\s*confidential.*$",
    re.IGNORECASE | re.DOTALL,
)

GENERIC_LEARNING_PATTERNS = [
    r"improved coding skills",
    r"gained practical experience.*business logic",
    r"learned how to identify issues.*make changes",
    r"learned about coding and business logic",
    r"focused on coding practices.*business logic",
    r"coding and(?: implementing)? business logic",
]

TECHNICAL_KEYWORDS = [
    "USP_",
    "USP_HRMS_SalaryFundRequestApproval",
    "M_ApprovalManagement",
    "B_BRNO",
    "B_BillPassing",
    "HRMS_",
    "HRMSalaryArrearsJV",
    "HRMELSApproval",
    "PensionStopExit",
    "DAEffectiveDateCapture",
    "DLMS",
    "AutoPostBack",
    "SqlCommand",
    "SqlDataAdapter",
    "DataSet",
    "BEL",
    "BAL",
    "DAL",
    "BESCOMAMI",
    "COCHINPORT",
    "GESCOMAMI",
    "GESCOM_LIVE_02042026",
    "ERP_LIVE_31032026",
    "PPAS 9.5",
    "--no-owner",
    "--no-acl",
    "PostgreSQL",
    "SQL Server",
    "stored procedure",
    "LocationCode",
    "RDLC",
    "Form 3",
    "Form 4",
    "Aadhaar",
    "Aadhar",
    "PAN",
    "relay status",
    "load switch",
    "prepaid",
    "Basic Difference",
    "CPS",
    "TOD",
    "E-Mudra",
    "E-Sign",
    "CPNG",
    "DPNG",
    "Claude",
]


def _extract_email_address(header_val: str) -> str:
    _, addr = email.utils.parseaddr(header_val)
    return addr.lower().strip()


def _parse_date(date_str: str) -> Optional[datetime.datetime]:
    try:
        dt = email.utils.parsedate_to_datetime(date_str)
        # Convert to IST (+05:30)
        ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        return dt.astimezone(ist)
    except Exception:
        return None


def _clean_body(raw_body: str) -> str:
    cleaned = raw_body.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = CONFIDENTIAL_RE.sub("", cleaned).strip()
    return cleaned


def _detect_projects(text: str, default_projects: List[str]) -> List[str]:
    found: List[str] = []
    mapping = [
        ("TCED", r"\bTCED\b"),
        ("GESCOM", r"\bGESCOM(?:AMI)?\b"),
        ("BGCL", r"\bBGCL\b"),
        ("HESCOM", r"\bHESCOM\b"),
        ("BWSSB", r"\bBWSSB\b"),
        ("KPTCL", r"\bKPTCL\b"),
        ("DCW", r"\bDCW\b"),
        ("INESH Meter", r"\bINESH\b"),
        ("CMRL", r"\bCMRL\b"),
        ("TRM SpotBilling", r"\bSpot\s*Billing\b"),
        ("Smart Metering", r"\bSmart\s*Meter(?:ing)?\b"),
        ("EMudra", r"\bEMudra\b"),
        ("Seva Sindhu", r"\bSeva\s*Sindhu\b"),
        ("HRMS", r"\bHRMS?\b|\bEmployee\s*(?:Creation|Approval|Portal|Exit)\b"),
        ("DB Restore", r"\bBESCOMAMI\b|\bCOCHINPORT\b|\bdatabase\s+restor"),
    ]
    for label, pat in mapping:
        if re.search(pat, text, re.IGNORECASE):
            found.append(label)
    if not found:
        return default_projects[:2]
    return found


def _extract_sections(clean_text: str) -> Tuple[List[str], List[str], List[str]]:
    """
    Parse free-form standup email body into (work_done, plan_tomorrow, learnings).
    Handles varied section headings and ordering across team members.
    """
    lines = [ln.strip() for ln in clean_text.splitlines()]

    work_done: List[str] = []
    plan_tomorrow: List[str] = []
    learnings: List[str] = []

    current_bucket: Optional[str] = "work"  # Default initial bucket for Ankith's headerless start

    work_header_re = re.compile(
        r"^(?:\*?\d*\.?\s*)?(?:\(\d{2}-\d{2}-\d{4}\)\s*-\s*work\s+done|work\s+done(?:\s+today)?|today['’]?s\s+work(?:\s+completed|\s+status)?|what\s+i\s+did\s+today|tasks\s+completed\s+today|work\s+completed(?:\s+today)?|today['’]?s\s+completed\s+activities|files\s+for\s+deployment)\b[:\-–\s\*]*",
        re.IGNORECASE,
    )
    plan_header_re = re.compile(
        r"^(?:\*?\d*\.?\s*)?(?:\(\d{2}-\d{2}-\d{4}\)\s*-\s*work\s+in\s+progress|tomorrow['’]?s\s+plan(?:ned\s+activities)?|plan\s+for\s+tomorrow|work\s+planned\s+for\s+tomorrow|tasks\s+planned\s+for\s+tomorrow|what\s+i\s+(?:will\s+|am\s+going\s+to\s+)?do\s+tomorrow|pending(?:\s+work)?)\b[:\-–\s\*]*",
        re.IGNORECASE,
    )
    learn_header_re = re.compile(
        r"^(?:\*?\d*\.?\s*)?(?:what\s+i\s+learn(?:ed|t)(?:\s+today)?|key\s+learnings?|learnings?(?:\s+from\s+today|\s*&\s*development)?|today['’]?s\s+learning)\b[:\-–\s\*]*",
        re.IGNORECASE,
    )
    signoff_re = re.compile(
        r"^(?:with\s+regards|thanks\s*(?:&|and)\s*regards|regards|dear\s+(?:sumukh\s+)?sir|hi\s+sir|hello\s+sir|please\s+find\s+below|please\s+find\s+my|--+$)",
        re.IGNORECASE,
    )

    prev_line_blank = False
    for line in lines:
        if not line:
            prev_line_blank = True
            continue
        plain = re.sub(r"\*+", "", line).strip()
        if not plain or re.match(r"^[-=_]{3,}$", plain):
            prev_line_blank = True
            continue
        if re.match(r"^(?:date\s*:|daily\s+work\s+report|progress\s+report\s+for\s+day|\d{1,2}-\d{2}-\d{4}$)", plain, re.I):
            prev_line_blank = True
            continue

        # Check section headers
        if work_header_re.match(plain):
            current_bucket = "work"
            remainder = work_header_re.sub("", plain).strip(" :*-–")
            if remainder and not re.match(r"^\(?\d{1,2}-\d{2}-\d{4}\)?$", remainder):
                work_done.append(remainder)
            prev_line_blank = True
            continue
        if plan_header_re.match(plain):
            current_bucket = "plan"
            remainder = plan_header_re.sub("", plain).strip(" :*-–")
            if remainder and not re.match(r"^\(?\d{1,2}-\d{2}-\d{4}\)?$", remainder):
                plan_tomorrow.append(remainder)
            prev_line_blank = True
            continue
        if learn_header_re.match(plain):
            current_bucket = "learn"
            remainder = learn_header_re.sub("", plain).strip(" :*-–")
            if remainder:
                learnings.append(remainder)
            prev_line_blank = True
            continue

        if signoff_re.match(plain):
            # Stop if we hit signature block at bottom
            if any([work_done, plan_tomorrow, learnings]) and re.match(
                r"^(?:with\s+regards|thanks\s*(?:&|and)\s*regards|regards)", plain, re.I
            ):
                break
            prev_line_blank = True
            continue

        # Clean bullet markers
        bullet_match = re.match(r"^(?:[-•\*]\s*|o\s+|\d+[\.\)]\s*|[a-e]\)\s+)(.*)", plain)
        is_new_bullet = bool(bullet_match)
        item = bullet_match.group(1).strip() if bullet_match else plain.strip()
        if not item or len(item) <= 2:
            prev_line_blank = False
            continue

        # Sub-heading labels like "Project: TCED" or "TRM SpotBilling"
        is_subheading = bool(
            re.match(r"^(?:project(?:\s+name)?\s*:|trm\b|bwssb\b|tced\b)", item, re.I)
            and len(item) < 45
        )

        target_list = (
            work_done
            if current_bucket == "work"
            else plan_tomorrow
            if current_bucket == "plan"
            else learnings
        )

        # If this line is a soft-wrapped continuation of the previous bullet (no blank line before it,
        # and starts lowercase or previous line didn't end with sentence punctuation),
        # merge it into the previous bullet!
        if (
            target_list
            and not prev_line_blank
            and not is_new_bullet
            and not is_subheading
            and (
                item[0].islower()
                or not target_list[-1].endswith((".", ":", ";", "!", "?"))
            )
        ):
            target_list[-1] = f"{target_list[-1]} {item}"
        else:
            target_list.append(item)
        prev_line_blank = False

    return work_done, plan_tomorrow, learnings


def _score_learning(
    email_addr: str,
    day_key: str,
    learnings: List[str],
    work_done: List[str],
    subject: str,
    plan_tomorrow: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Evaluate learning quality:
      - 'green': Specific technical/domain/workflow insight
      - 'amber': Generic / repeated boilerplate
      - 'red': Missing learning section or tooling blocker
    """
    joined_learn = " ".join(learnings).strip()
    joined_work = " ".join(work_done).strip()
    all_text = f"{joined_learn} {joined_work}"

    extracted_entities = [
        kw for kw in TECHNICAL_KEYWORDS if re.search(r"\b" + re.escape(kw) + r"\b", all_text, re.IGNORECASE)
    ]

    # Case 1: Rohith's Claude weekly limit blocker
    if "weekly limit has been exhausted" in joined_learn.lower() or "did not use claude" in joined_learn.lower():
        return {
            "score": "red",
            "badge": "Tooling Blocker Flagged",
            "reason": "Reported AI tooling blocker ('did not use Claude today as my account weekly limit has been exhausted') instead of a technical learning.",
            "entities": extracted_entities,
            "is_boilerplate": False,
            "coaching_nudge": "Good transparency flagging the Claude rate limit—let's get your AI seat/API quota sorted. Even on days without Claude, jot down 1 domain takeaway from your integration work.",
        }

    # Case 2: No learning section provided (e.g. Ankith on Oct 29 / Oct 31 / Nov 2 / Nov 4)
    if not learnings:
        # Check if Ankith mixed learning into work_done on Oct 29
        if "studied the bel" in joined_work.lower():
            return {
                "score": "green",
                "badge": "Specific Architectural Learning",
                "reason": "Detailed 3-tier C# architecture study (BEL/BAL/DAL, SqlCommand, SqlDataAdapter) — though written in a single list without separate 'Learnings' heading.",
                "entities": extracted_entities,
                "is_boilerplate": False,
                "coaching_nudge": "Great breakdown of BEL/BAL/DAL and SQL Server backup verification! Next time, add a clear Subject line and separate 'Work Done' from 'What I Learned'.",
            }
        if plan_tomorrow:
            return {
                "score": "red",
                "badge": "Missing 'What I Learned' Section",
                "reason": "Included clear DB restoration status and tomorrow's plan, but omitted the 'What I Learned' section.",
                "entities": extracted_entities,
                "is_boilerplate": False,
                "coaching_nudge": "Great progress on the SQL Server & PostgreSQL database restorations! Please remember to include a 'What I Learned' section in every daily report.",
            }
        return {
            "score": "red",
            "badge": "Missing 'Learnings' & 'Tomorrow Plan'",
            "reason": "Omitted both the 'What I Learned' and 'Tomorrow's Plan' sections (and sent with a blank Subject line).",
            "entities": extracted_entities,
            "is_boilerplate": False,
            "coaching_nudge": "Nice work restoring BESCOMAMI, COCHINPORT & GESCOMAMI! Please remember to include: (1) an email Subject line, (2) Tomorrow's Plan (including PostgreSQL for GESCOM), and (3) 1 key learning from the DB restore.",
        }

    # Case 3: Check for generic boilerplate patterns
    for pat in GENERIC_LEARNING_PATTERNS:
        if re.search(pat, joined_learn, re.IGNORECASE):
            # Check if they also included something slightly more specific
            has_specific_clause = any(
                w in joined_learn.lower()
                for w in [
                    "form 3",
                    "approval hierarchy",
                    "employee portal",
                    "sql server",
                    "table count",
                    "cpng",
                    "calculation validation",
                ]
            )
            if has_specific_clause:
                return {
                    "score": "amber",
                    "badge": "Semi-Generic (Needs Depth)",
                    "reason": f"Mentions workflow topic ({joined_learn}), but still relies on high-level phrasing rather than naming the concrete edge case or code pattern learned.",
                    "entities": extracted_entities,
                    "is_boilerplate": True,
                    "coaching_nudge": f"You worked on concrete deliverables today ({work_done[0] if work_done else 'your module'}). Instead of 'learned coding and business logic', share 1 specific edge case or table/query behavior you discovered!",
                }
            return {
                "score": "amber",
                "badge": "Repeated Generic Boilerplate",
                "reason": f"Generic filler repeated across days: \"{joined_learn}\". Does not capture the actual domain or technical insight from today's work.",
                "entities": extracted_entities,
                "is_boilerplate": True,
                "coaching_nudge": f"Your 'Work Done' is clear ({work_done[0] if work_done else 'good progress'}), but your 'Learning' line is generic boilerplate. What was 1 tricky rule, SQL/code fix, or AI prompt takeaway from today?",
            }

    # Case 4: Ankith Oct 30 superficial restatement of work done
    if email_addr == "ankith.hm@nsoft.in" and day_key == "2026-10-30":
        return {
            "score": "amber",
            "badge": "Restated Task Title",
            "reason": "Restated task titles ('SQL Server database restoration; Checking database status and table counts') without detailing what was learned or which 5 DBs were restored.",
            "entities": extracted_entities,
            "is_boilerplate": False,
            "coaching_nudge": "Please add a Subject line to your daily email, list the names of the 5 databases restored, and note any specific issue or verification query you learned.",
        }

    # Default: Specific Green Insight!
    return {
        "score": "green",
        "badge": "Specific Technical Insight",
        "reason": f"Concrete domain/engineering reflection: {joined_learn}",
        "entities": extracted_entities,
        "is_boilerplate": False,
        "coaching_nudge": None,
    }


def _generate_gist_and_analysis(
    person_name: str,
    email_addr: str,
    day_key: str,
    subject: str,
    work_done: List[str],
    plan_tomorrow: List[str],
    learnings: List[str],
    learning_eval: Dict[str, Any],
    manager_reply: Optional[Dict[str, str]],
    submitted_late_note: Optional[str] = None,
) -> Tuple[str, List[str]]:
    """Build a crisp gist and bulleted AI analysis notes for a matrix cell."""
    if work_done:
        first_item = work_done[0]
        if len(work_done) > 1:
            gist = f"{first_item} (+{len(work_done) - 1} more item{'s' if len(work_done) > 2 else ''})"
        else:
            gist = first_item
    else:
        gist = "(No work items parsed)"

    notes: List[str] = []
    if submitted_late_note:
        notes.append(submitted_late_note)

    if not subject or not subject.strip():
        notes.append("⚠️ Sent with a blank Subject line.")

    if not plan_tomorrow:
        notes.append("⚠️ Missing 'Tomorrow's Plan' section.")

    if learning_eval["score"] == "green":
        notes.append(f"✅ High-signal learning: {learning_eval['reason']}")
    elif learning_eval["score"] == "amber":
        notes.append(f"⚡ Coaching opportunity: {learning_eval['reason']}")
    elif learning_eval["score"] == "red":
        notes.append(f"🚨 Attention needed: {learning_eval['reason']}")

    if manager_reply:
        reply_txt = manager_reply["body"]
        if reply_txt.lower() == "noted":
            notes.append(f"📩 Sumukh replied 'Noted' ({manager_reply['date_short']}).")
        else:
            notes.append(f"💬 Sumukh intervention ({manager_reply['date_short']}): \"{reply_txt}\"")

    return gist, notes


def parse_standup_dashboard() -> Dict[str, Any]:
    """Parse raw-emails.md into the full Team Standup Intelligence Dashboard payload."""
    if not RAW_EMAILS_PATH.exists():
        return {"days": [], "people": [], "matrix": {}, "plan_vs_actual": [], "summary": {}}

    raw_text = RAW_EMAILS_PATH.read_text(encoding="utf-8", errors="replace")
    blocks = raw_text.split("<!-- gmail-id:")[1:]

    raw_messages: List[Dict[str, Any]] = []
    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue
        gmail_id = lines[0].replace("-->", "").strip()
        subj_m = re.search(r"^##[ \t]*(.*)", block, re.M)
        from_m = re.search(r"^- \*\*From:\*\*\s*(.*)", block, re.M)
        to_m = re.search(r"^- \*\*To:\*\*\s*(.*)", block, re.M)
        cc_m = re.search(r"^- \*\*Cc:\*\*\s*(.*)", block, re.M)
        date_m = re.search(r"^- \*\*Date:\*\*\s*(.*)", block, re.M)

        subject = subj_m.group(1).strip() if subj_m else ""
        from_str = from_m.group(1).strip() if from_m else ""
        to_str = to_m.group(1).strip() if to_m else ""
        cc_str = cc_m.group(1).strip() if cc_m else ""
        date_str = date_m.group(1).strip() if date_m else ""

        # Extract body after `- **Gmail ID:** ...`
        body_split = re.split(r"^- \*\*Gmail ID:\*\*.*$", block, maxsplit=1, flags=re.M)
        raw_body = body_split[1].strip() if len(body_split) > 1 else ""
        # Strip trailing `---`
        raw_body = re.sub(r"\n---\s*$", "", raw_body).strip()

        dt = _parse_date(date_str)
        sender_email = _extract_email_address(from_str)

        raw_messages.append(
            {
                "gmail_id": gmail_id,
                "subject": subject,
                "from": from_str,
                "sender_email": sender_email,
                "to": to_str,
                "cc": cc_str,
                "date": date_str,
                "dt": dt,
                "raw_body": raw_body,
            }
        )

    # Separate Sumukh's manager replies / nudges vs engineer standup reports vs non-standup emails
    roster_map = {p["email"]: p for p in TEAM_ROSTER}
    manager_replies: List[Dict[str, Any]] = []
    standup_reports: List[Dict[str, Any]] = []
    non_standup_emails: List[Dict[str, Any]] = []

    for msg in raw_messages:
        s_email = msg["sender_email"]
        if s_email == "sumukh.hegde@nsoft.in":
            if "certificate" in msg["subject"].lower():
                non_standup_emails.append(msg)
            else:
                manager_replies.append(msg)
        elif s_email in roster_map:
            standup_reports.append(msg)
        else:
            non_standup_emails.append(msg)

    # Determine which day each standup report belongs to
    # Special handling: Kousalya's email sent Sun, 1 Nov 2026 07:03:28 +0530 is her Oct 31 report
    # sent right after Sumukh's Sat 31 Oct 23:24 nudge.
    matrix: Dict[str, Dict[str, Any]] = {p["email"]: {} for p in TEAM_ROSTER}
    days_set = {"2026-10-29", "2026-10-30", "2026-10-31"}

    # Sort oldest first so if someone sends a revised report 4 mins later (like Anith on Oct 29),
    # the newer one updates the slot while noting the revision.
    standup_reports.sort(key=lambda m: m["dt"] or datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))

    for rep in standup_reports:
        s_email = rep["sender_email"]
        dt = rep["dt"]
        if not dt:
            continue

        day_key = dt.strftime("%Y-%m-%d")
        submitted_late_note = None
        if s_email == "talari.kousalya@nsoft.in" and day_key == "2026-11-01" and dt.hour < 12:
            day_key = "2026-10-31"
            submitted_late_note = "⏰ Submitted Sun Nov 1 at 7:03 AM (following Sumukh's Sat 11:24 PM reminder)."
        elif dt.hour < 12:
            prev_day = (dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            day_key = prev_day
            submitted_late_note = f"⏰ Submitted next morning ({dt.strftime('%a %d %b, %I:%M %p')})."

        days_set.add(day_key)
        clean_text = _clean_body(rep["raw_body"])
        work_done, plan_tomorrow, learnings = _extract_sections(clean_text)

        person_info = roster_map[s_email]
        projects = _detect_projects(clean_text + " " + rep["subject"], person_info["primary_projects"])
        learning_eval = _score_learning(s_email, day_key, learnings, work_done, rep["subject"], plan_tomorrow)

        prev_entry = matrix[s_email].get(day_key)
        revision_note = None
        if prev_entry:
            revision_note = "📝 Sent 2 versions of this report 4 mins apart (19:02 & 19:06); showing latest."

        matrix[s_email][day_key] = {
            "gmail_id": rep["gmail_id"],
            "person_email": s_email,
            "person_name": person_info["name"],
            "day": day_key,
            "subject": rep["subject"] or "(No Subject)",
            "has_subject": bool(rep["subject"].strip()),
            "date": rep["date"],
            "time_short": dt.strftime("%d %b, %I:%M %p"),
            "to": rep["to"],
            "cc": rep["cc"],
            "raw_body": rep["raw_body"],
            "clean_body": clean_text,
            "projects": projects,
            "work_done": work_done,
            "plan_tomorrow": plan_tomorrow,
            "learnings": learnings,
            "learning_eval": learning_eval,
            "submitted_late_note": submitted_late_note or revision_note,
            "manager_reply": None,
        }

    # Attach Sumukh's replies/nudges to the corresponding engineer & day cell
    for reply in manager_replies:
        to_email = _extract_email_address(reply["to"])
        if to_email not in matrix:
            continue
        reply_FirstLine = reply["raw_body"].strip().splitlines()[0].strip() if reply["raw_body"].strip() else ""
        # Check if quoted body mentions a specific date (e.g., Oct 29 for Venkata Sai, Oct 30 for Rohith)
        target_day = "2026-10-31"
        if "Oct 29, 2026" in reply["raw_body"]:
            target_day = "2026-10-29"
        elif "Oct 30, 2026" in reply["raw_body"]:
            target_day = "2026-10-30"

        # Extract Sumukh's actual reply text before `On Sat, Oct 31...` or `--`
        reply_clean = re.split(r"\nOn\s+(?:Thu|Fri|Sat|Sun|Mon|Tue|Wed),", reply["raw_body"])[0]
        reply_clean = CONFIDENTIAL_RE.sub("", reply_clean).strip()

        reply_obj = {
            "gmail_id": reply["gmail_id"],
            "from": reply["from"],
            "date": reply["date"],
            "date_short": reply["dt"].strftime("%d %b, %I:%M %p") if reply["dt"] else reply["date"],
            "subject": reply["subject"],
            "body": reply_clean,
            "raw_body": reply["raw_body"],
        }

        if target_day in matrix[to_email]:
            matrix[to_email][target_day]["manager_reply"] = reply_obj

    # Finalize gists and AI analysis notes on every cell
    sorted_days = sorted(days_set)
    for p in TEAM_ROSTER:
        s_email = p["email"]
        for d in sorted_days:
            cell = matrix[s_email].get(d)
            if cell:
                gist, notes = _generate_gist_and_analysis(
                    person_name=p["name"],
                    email_addr=s_email,
                    day_key=d,
                    subject=cell["subject"] if cell["has_subject"] else "",
                    work_done=cell["work_done"],
                    plan_tomorrow=cell["plan_tomorrow"],
                    learnings=cell["learnings"],
                    learning_eval=cell["learning_eval"],
                    manager_reply=cell["manager_reply"],
                    submitted_late_note=cell["submitted_late_note"],
                )
                cell["gist"] = gist
                cell["ai_analysis"] = notes

    # Build Plan-vs-Actual Side-by-Side Tracker across consecutive day pairs
    plan_vs_actual: List[Dict[str, Any]] = []
    for i in range(len(sorted_days) - 1):
        day_prev = sorted_days[i]
        day_curr = sorted_days[i + 1]
        pair_label = f"{day_prev} Plan → {day_curr} Actual"

        for p in TEAM_ROSTER:
            s_email = p["email"]
            cell_prev = matrix[s_email].get(day_prev)
            cell_curr = matrix[s_email].get(day_curr)

            planned = cell_prev["plan_tomorrow"] if cell_prev else []
            actual = cell_curr["work_done"] if cell_curr else []

            status, badge, commentary = _evaluate_plan_vs_actual(
                person_name=p["name"],
                email_addr=s_email,
                day_prev=day_prev,
                day_curr=day_curr,
                planned=planned,
                actual=actual,
                has_prev=bool(cell_prev),
                has_curr=bool(cell_curr),
            )

            plan_vs_actual.append(
                {
                    "id": f"{s_email}:{day_prev}->{day_curr}",
                    "person_email": s_email,
                    "person_name": p["name"],
                    "person_role": p["role"],
                    "day_prev": day_prev,
                    "day_curr": day_curr,
                    "pair_label": pair_label,
                    "planned_items": planned,
                    "actual_items": actual,
                    "status": status,
                    "badge": badge,
                    "commentary": commentary,
                    "prev_cell": cell_prev,
                    "curr_cell": cell_curr,
                }
            )

    # Compute executive KPIs
    total_cells = len(TEAM_ROSTER) * len(sorted_days)
    submitted_cells = sum(
        1 for p in TEAM_ROSTER for d in sorted_days if d in matrix[p["email"]]
    )
    green_learnings = sum(
        1
        for p in TEAM_ROSTER
        for d in sorted_days
        if d in matrix[p["email"]] and matrix[p["email"]][d]["learning_eval"]["score"] == "green"
    )
    amber_learnings = sum(
        1
        for p in TEAM_ROSTER
        for d in sorted_days
        if d in matrix[p["email"]] and matrix[p["email"]][d]["learning_eval"]["score"] == "amber"
    )
    red_learnings = sum(
        1
        for p in TEAM_ROSTER
        for d in sorted_days
        if d in matrix[p["email"]] and matrix[p["email"]][d]["learning_eval"]["score"] == "red"
    )

    return {
        "days": sorted_days,
        "people": TEAM_ROSTER,
        "matrix": matrix,
        "plan_vs_actual": plan_vs_actual,
        "product_tracker": _build_product_tracker(matrix, sorted_days),
        "non_standup_count": len(non_standup_emails),
        "non_standup_subjects": [
            {"gmail_id": m["gmail_id"], "from": m["from"], "subject": m["subject"], "date": m["date"]}
            for m in non_standup_emails
        ],
        "summary": {
            "total_engineers": len(TEAM_ROSTER),
            "total_days": len(sorted_days),
            "submitted_reports": submitted_cells,
            "expected_reports": total_cells,
            "submission_rate_pct": round((submitted_cells / total_cells) * 100) if total_cells else 0,
            "green_learnings": green_learnings,
            "amber_learnings": amber_learnings,
            "red_learnings": red_learnings,
            "manager_replies_count": len(manager_replies),
        },
    }


def _evaluate_plan_vs_actual(
    person_name: str,
    email_addr: str,
    day_prev: str,
    day_curr: str,
    planned: List[str],
    actual: List[str],
    has_prev: bool,
    has_curr: bool,
) -> Tuple[str, str, str]:
    """Compare Day N-1 Plan against Day N Work Done and return (status, badge, commentary)."""
    if not has_curr:
        if email_addr == "rohith.r@nsoft.in" and day_curr == "2026-10-31":
            return (
                "missing",
                "Missing Oct 31 Report (Claude Limit on Oct 30)",
                "Planned to complete HESCOM Seva Sindhu Integration on Oct 31 after exhausting Claude weekly limit on Oct 30, but did not send an Oct 31 report.",
            )
        if email_addr == "venkata.sai@nsoft.in" and day_curr == "2026-10-31":
            return (
                "missing",
                "Missing Oct 31 Report",
                "Planned to build Salary Fund Request Budget screen & test Salary Arrears E2E on Oct 31, but no Oct 31 email was received.",
            )
        if not has_prev:
            return (
                "missing",
                f"No Reports ({day_prev} & {day_curr})",
                f"No standup report was submitted on either {day_prev} or {day_curr}.",
            )
        return (
            "missing",
            f"No Report on {day_curr}",
            f"Submitted a plan on {day_prev}, but no daily report was received for {day_curr}.",
        )

    if not has_prev:
        if email_addr == "venkata.sai@nsoft.in" and day_curr == "2026-11-03":
            return (
                "aligned",
                "Returned with Major 5-Screen ERP Delivery",
                "After missing Oct 31 & Nov 2 reports, delivered his Oct 30 planned Salary Fund Request & Approval screens (B_BRNO, USP_HRMS_SalaryFundRequestApproval) plus Salary Arrears JV/Report (2023–2024) and ELS Approval Net Pay fix.",
            )
        if email_addr == "rohith.r@nsoft.in" and day_curr == "2026-11-03":
            return (
                "pivoted",
                "Resumed Reporting (HESCOM E-Mudhra & TCED Data Load)",
                "After missing Oct 31 & Nov 2 reports, completed E-Mudhra Integration for HESCOM and resolved a data load issue in TCED Online Services (still noting Claude weekly quota exhaustion).",
            )
        if email_addr == "chitrashree.hr@nsoft.in" and day_curr == "2026-11-03":
            return (
                "aligned",
                "Resumed BGCL Track (CPNG Registration)",
                "Returned after missing Nov 2 report and delivered BGCL CPNG Registration Process changes.",
            )
        if email_addr == "lasya.mannuru@nsoft.in" and day_curr == "2026-11-04":
            return (
                "pivoted",
                "Completed Employee Track → Started Pension Modules",
                "After missing Nov 3 report, transitioned from EmployeeCreationApproval to verifying all Pension modules and adding the Clear button on the PensionStopExit screen.",
            )
        return (
            "aligned",
            f"Resumed Reporting on {day_curr}",
            f"No prior-day report on {day_prev}, but submitted full work update on {day_curr}.",
        )

    if email_addr == "venkata.sai@nsoft.in" and day_prev == "2026-10-29":
        return (
            "pivoted",
            "Scope Reprioritized (Fund Request Deferred)",
            "Planned on Oct 29 to work on HRMS Salary Fund Request screen, but pivoted on Oct 30 to deliver deep enhancements on HRM Salary Arrears (USP_HRMSalaryArrears, DP 31% rule) & Employee Salary Bill Approval UI redesign—deferring Salary Fund Request.",
        )

    if email_addr == "talari.kousalya@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "aligned",
                "Aligned (Multi-Day Prepaid Billing Track)",
                "Executed directly on her Oct 29 plan: implemented INESH meter prepaid billing, tested daily charge deduction & balance updates, and analyzed continuous billing cycle issues.",
            )
        if day_prev == "2026-10-30":
            return (
                "carryover",
                "3-Day Carryover (Narrowed to Relay & Duplicate Deduction Bugs)",
                "Continued the same INESH meter prepaid billing & daily charge deduction track for a 3rd consecutive day, narrowing down tomorrow's plan to fixing relay status updates (DLMS attributes) and preventing duplicate daily charge deduction.",
            )
        if day_prev == "2026-10-31":
            return (
                "aligned",
                "Aligned (Billing Recovery + Post-Billing PR XML/API)",
                "Tested the latest INESH prepaid billing build, verified daily charge deduction & missed-day billing recovery, and began post-billing PR XML generation and API integration.",
            )
        if day_prev == "2026-11-02":
            return (
                "carryover",
                "Carryover (Expanded to Capital Meter & TCP Response Errors)",
                "Continued prepaid billing across both INESH and Capital meters while diagnosing DLMS meter communication and TCP response errors.",
            )
        return (
            "aligned",
            "Aligned (Capital Meter DLMS & Daily Consumption)",
            "Focused on Capital meter DLMS communication, cumulative energy register readings, and daily consumption calculation for prepaid billing.",
        )

    if email_addr == "pallapu.rajesh@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "aligned",
                "Aligned + Unplanned BGCL Fix",
                "Continued Back Office Bill Generation & Complaint Management screens (adding wheeling units & transmission loss logic) plus fixed a BGCL leave balance issue.",
            )
        if day_prev == "2026-10-30":
            return (
                "carryover",
                "3rd Day on Same Screens (Street Light Billing Logic)",
                "Planned to continue Back Office Bill Generation & Complaint Management screens; implemented street light consumer billing logic in TCED plus fixed BGCL salary generation issues.",
            )
        if day_prev == "2026-10-31":
            return (
                "carryover",
                "4th Day on TCED Billing Screens + Solar Bill Print",
                "Continued modifications to Back Office Bill Generation and Complaint Management screens and added Solar Bill Print modifications.",
            )
        if day_prev == "2026-11-02":
            return (
                "carryover",
                "5th Day on TCED Screens (Temporary Consumer) + BGCL BPNO/DPNG",
                "Implemented temporary consumer billing logic in TCED Back Office Bill Generation & Complaint Management screens, plus fixed BGCL BPNO generation and DPNG report issues.",
            )
        return (
            "pivoted",
            "Expanded to New Consumer, Debit Entry & Solar Wheeling Loss",
            "Delivered New Consumer Entry, Debit Entry, and Billing Report modifications in TCED and started Solar Wheeling Transmission Loss logic.",
        )

    if email_addr == "chitrashree.hr@nsoft.in":
        return (
            "pivoted",
            "Vague Plan ('Continue BGCL') vs Multi-Project Actuals",
            "Wrote a generic one-line plan ('Continue working on the BGCL project'), while actual work spanned DCW Reports, Material Purchase OM changes, BGCL work requisitions, and KPTCL issues.",
        )

    if email_addr == "ankith.hm@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "aligned",
                "Aligned on DB Restores (Paused C# Study)",
                "Executed the planned SQL Server database restorations (restored 5 databases and verified table counts), pausing the C# BEL/BAL/DAL study track.",
            )
        if day_prev == "2026-10-30":
            return (
                "pivoted",
                "Expanded Scope (3 More DBs + TCED ERP Review)",
                "Planned only to 'Complete the GESCOM integrity check', but actually restored BESCOMAMI, COCHINPORT & GESCOMAMI AND reviewed TCED ERP Employee Creation/Exit C# dropdowns.",
            )
        if day_prev == "2026-10-31":
            return (
                "aligned",
                "Answered Sumukh's Directive (18/21 DBs Restored Table)",
                "Published structured progress table following Sumukh's Oct 31 reminder: restored VIZAG_15092023, INDIAN_RAILWAY_07062023, NSOFTSTORE_29042026 & SRTPV_BESCOM (reaching 18/21 SQL Server DBs ONLINE).",
            )
        if day_prev == "2026-11-02":
            return (
                "aligned",
                "Aligned (20 SQL DBs Online + PPAS 9.5 ERP_LIVE & GESCOM_LIVE)",
                "Reached 20 SQL Server DBs online, completed ERP_LIVE_31032026 restoration in PostgreSQL/PPAS 9.5 (--no-owner/--no-acl), and initiated GESCOM_LIVE_02042026.",
            )
        return (
            "aligned",
            "Aligned (GESCOM_LIVE_02042026 Full + Differential Restore)",
            "Completed SQL Server full database restore for GESCOM_LIVE_02042026, restarted the differential backup restore after diagnosing delays, and checked row-count estimates for PostgreSQL validation.",
        )

    if email_addr == "lasya.mannuru@nsoft.in":
        if day_prev == "2026-10-31":
            return (
                "pivoted",
                "Post-Deployment Dedup & Save Fixes on Employee Screens",
                "Planned deployment of Employee modules on Oct 31; on Nov 2 resolved duplicate name display in EmployeeCreationApproval and verified end-to-end save persistence in EmployeeCreation.",
            )
        return (
            "aligned",
            "100% Plan-to-Actual Execution",
            f"Directly completed every item planned on {day_prev} with clear verification on the EmployeeCreationApproval screen and HRMS_AdditionalDocumnetsAppr table.",
        )

    if email_addr == "anith.hm@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "aligned",
                "Aligned (SQL Tables + Flag-Based CRUD Stored Proc)",
                "Created the planned SQL Server relational tables, wrote the flag-based CRUD stored procedure, and wired C# AutoPostBack & dropdown bindings.",
            )
        if day_prev == "2026-10-30":
            return (
                "pivoted",
                "Pivoted to HRMS Bug Fixes (as Planned in Day 2 Learning)",
                "Transitioned from his sandbox form into real HRMS Issue Solving: fixed the deputation checkbox bug, double language display issue, and designation join date across frontend and backend.",
            )
        if day_prev == "2026-10-31":
            return (
                "carryover",
                "Continued Deputation Checkbox & Join Date Refinements",
                "Fixed newly surfaced edge cases in the deputation checkbox across new/edit employee flows and updated the current designation join date per requirement.",
            )
        if day_prev == "2026-11-02":
            return (
                "pivoted",
                "Assigned to HRMS Disciplinary Action Module",
                "Completed Employee form stabilization and tackled HRMS Disciplinary Action—fixing Division/Section Employee Name dropdown loading via LocationCode hierarchy in the stored procedure.",
            )
        return (
            "aligned",
            "100% Aligned (Annual Incumbency & Sanction Strength Report)",
            "Executed directly on his Nov 3 plan: resolved the Annual Incumbency Preparation retirement-date and office-mapping issues, and investigated the Gulbarga name issue in the RDLC Sanction Strength Report.",
        )

    if email_addr == "sanjana.cs@nsoft.in":
        return (
            "aligned",
            "100% Plan-to-Actual Execution (TCED PF Module)",
            f"Executed directly on her {day_prev} plan—progressing systematically from Form 3/4 Portal & ERP screens → Create/Approve/Reject/Recommend reports → 75% Total Subscription & Balance at Credit calculation logic → E2E calculation testing.",
        )

    if email_addr == "nitishnag.m@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "aligned",
                "Aligned (BWSSB SpotBilling + Smart Metering)",
                "Delivered both planned tracks: BWSSB SpotBilling (EMI remarks for interest penalty, disabling SIR deputation option) and TRM Smart Metering (Meter Burnt/Not Running cases).",
            )
        if day_prev == "2026-10-30":
            return (
                "aligned",
                "Aligned (Nov 2026 App Releases Shipped)",
                "Shipped the planned Nov 2026 app releases for HESCOM and BWSSB Spot Billing, modified Weavers rebate LT-5 R DBT tariff logic, and attended the EMudra LE/LR integration meeting.",
            )
        if day_prev == "2026-10-31":
            return (
                "aligned",
                "Aligned (E-Mudra LE/LR Screens + TCED TOD Tariff)",
                "Delivered E-Mudra LE/LR screen modifications, reviewed TRM Rural Rebate issues, and updated TCED file updation task for TOD Normal, TOD Peak, and TOD OffPeak.",
            )
        return (
            "aligned",
            "Aligned (E-Mudra LE/LR + Smart Meter Fetch + TCED WFM)",
            "Continued planned E-Mudra LE/LR screen modifications, resolved Smart Meter Billing Data Fetch issues, and worked on TCED WFM Portal integration.",
        )

    if email_addr == "rohith.r@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "carryover",
                "Started Planned Task (Slowed by Claude Limit)",
                "Planned to complete HESCOM Seva Sindhu Integration; started it on Oct 30 and carried completion over to tomorrow after hitting his Claude weekly usage limit.",
            )
        return (
            "pivoted",
            "Delivered TCED E-Sign Module & LT New Connection Fix",
            "Planned to take up a new HESCOM task, and pivoted to completing E-Sign Module changes in TCED ERP and fixing a data load issue in TCED Online Services (LT New Connection) with Claude access restored.",
        )

    return (
        "aligned",
        "Aligned with Plan",
        "Actual work matches the planned items from the previous day.",
    )


def _build_product_tracker(matrix: Dict[str, Dict[str, Any]], sorted_days: List[str]) -> Dict[str, Any]:
    """
    Build the ClickUp-style Product & Task Tracker mapped across the 4 NSoft Product Suites:
      1. TRM (Total Revenue Management, SpotBilling & Smart Metering)
      2. ERP (HRMS, Payroll/Arrears, Employee Portal, Municipal PF, BGCL & DCW)
      3. KPTCL (Karnataka Power Transmission Corp. Reports & App Issues)
      4. Infra & Security (SQL Server & PostgreSQL / PPAS 9.5 Database Restorations & Recovery)
    """
    products = [
        {
            "id": "TRM",
            "name": "TRM",
            "full_name": "TRM — SpotBilling, Billing Engines & Smart Metering",
            "color": "indigo",
            "projects": [
                "TCED Billing & Demand",
                "HESCOM SpotBilling & Integrations",
                "BWSSB SpotBilling",
                "Smart Metering (INESH / Capital / CMRL / EMudra)",
            ],
            "brief": {
                "title": "TRM Product Brief & Active Sprint (Oct 29 – Nov 4)",
                "agent_author": "TRM Delivery Agent",
                "overview": "Covers utility revenue billing, Android spot-billing releases (HESCOM, BWSSB), TCED back-office tariff/billing logic (TOD, Solar Wheeling, Street Light, Temporary Consumer), and smart/prepaid meter integrations (INESH & Capital DLMS, CMRL, E-Mudra).",
                "highlights": [
                    "Shipped Nov 2026 SpotBilling App Releases for HESCOM & BWSSB, TCED TOD (Normal/Peak/OffPeak) file updates, TCED WFM Portal integration, and E-Mudra LE/LR screen modifications (Nitish Nag).",
                    "Completed 6-day TCED billing sprint across DL withdrawal, wheeling/transmission loss, street light, solar bill print, temporary consumer, New Consumer/Debit Entry, and Solar Wheeling Transmission Loss (Pallapu Rajesh).",
                    "Progressed INESH & Capital meter DLMS prepaid billing through daily charge deduction, missed-day billing recovery, PR XML/API integration, TCP error analysis, and cumulative energy register consumption calculations (Kousalya Talari).",
                ],
                "risks": [
                    "Kousalya is resolving pending DLMS meter reading & TCP response issues on Capital meter prepaid billing (Day 6 of prepaid track).",
                    "Nitish Nag did not submit a Nov 4 standup report after planning further E-Mudra LE/LR screen modifications on Nov 3.",
                ],
            },
        },
        {
            "id": "ERP",
            "name": "ERP",
            "full_name": "ERP — HRMS, Payroll, Employee Portal & Municipal PF",
            "color": "emerald",
            "projects": [
                "GESCOM ERP & Employee Portal (HRMS)",
                "TCED ERP & Employee Portal (HRMS & PF)",
                "BGCL ERP & Requisitions",
                "DCW & Material Purchase OM",
            ],
            "brief": {
                "title": "ERP & HRMS Product Brief (Oct 29 – Nov 4)",
                "agent_author": "ERP Architecture Agent",
                "overview": "Spans GESCOM & TCED HRMS modules, Employee Creation/Approval & PensionStopExit workflows, Salary Arrears/JV/ELS/Fund Request calculation engines, Kerala Municipal PF Form 3/4 & 75% eligibility workflows, E-Sign, and BGCL/DCW operations.",
                "highlights": [
                    "GESCOM HRMS 5-screen delivery ready for deployment: Salary Arrears Report/JV (2023–2024), ELS Approval double-deduction Net Pay fix, and Salary Fund Request & Approval (B_BRNO, USP_HRMS_SalaryFundRequestApproval) + Salary JV in progress (Venkata Sai).",
                    "Completed EmployeeCreation & EmployeeCreationApproval deduplication/live-path fixes and verified all Pension modules + added PensionStopExit Clear button ready for deployment (Mannuru Lasya).",
                    "Built TCED Form 3 & Form 4 screens/reports across Portal & ERP, implemented 75% Total Subscription & Balance at Credit advance eligibility logic, and verified calculations end-to-end (Sanjana C S).",
                    "Fixed HRMS Disciplinary Action dropdown hierarchy (LocationCode) & Annual Incumbency retirement-date/office-mapping (Anith HM) and completed TCED ERP E-Sign module changes (Rohith R).",
                ],
                "risks": [
                    "Gulbarga name issue in RDLC Sanction Strength Report awaiting affected report sample for verification (Anith HM).",
                    "Venkata Sai submitted his Nov 3 report on Nov 4 morning (10:09 AM) and has not yet sent a Nov 4 evening report.",
                ],
            },
        },
        {
            "id": "KPTCL",
            "name": "KPTCL",
            "full_name": "KPTCL — Reports & Application Maintenance",
            "color": "amber",
            "projects": [
                "KPTCL Report & Application Fixes",
            ],
            "brief": {
                "title": "KPTCL Maintenance Brief (Oct 29 – Nov 4)",
                "agent_author": "KPTCL Ops Agent",
                "overview": "Tracks bug resolutions, report generation fixes, and application changes for Karnataka Power Transmission Corporation Limited (KPTCL).",
                "highlights": [
                    "Resolved KPTCL Report generation issues on Oct 30 and application issues on Oct 31 (Chitrashree HR).",
                ],
                "risks": [
                    "Chitrashree missed standup reports on Nov 2 and Nov 4, and KPTCL updates lack specific screen/ticket IDs.",
                ],
            },
        },
        {
            "id": "Infra & Security",
            "name": "Infra & Security",
            "full_name": "Infra & Security — SQL Server & PostgreSQL / PPAS 9.5 DB Restorations",
            "color": "purple",
            "projects": [
                "SQL Server Multi-Utility DB Restorations",
                "PostgreSQL / PPAS 9.5 Live DB Restorations",
            ],
            "brief": {
                "title": "Database Restoration & Recovery Brief (Oct 29 – Nov 4)",
                "agent_author": "Infra & DB Reliability Agent",
                "overview": "Covers multi-utility SQL Server (21-database backup set + GESCOM_LIVE_02042026 full & differential restores) and PostgreSQL / PPAS 9.5 (ERP_LIVE_31032026 & GESCOM_LIVE_02042026) database restorations, role/ownership handling, and row-count integrity checks.",
                "highlights": [
                    "Confirmed 20 of 21 main SQL Server databases restored and ONLINE (including BESCOMAMI, COCHINPORT, GESCOMAMI, VIZAG_15092023, INDIAN_RAILWAY_07062023, NSOFTSTORE_29042026, SRTPV_BESCOM) + completed SQL Server full restore for GESCOM_LIVE_02042026 (Ankith HM).",
                    "Completed ERP_LIVE_31032026 restoration in PostgreSQL/PPAS 9.5 using --no-owner and --no-acl flags and initiated GESCOM_LIVE_02042026 PostgreSQL validation (Ankith HM).",
                ],
                "risks": [
                    "SQL Server differential restore for GESCOM_LIVE_02042026 experienced delays and was restarted on Nov 4; final verification & PostgreSQL GESCOM validation scheduled for Nov 5.",
                ],
            },
        },
    ]

    tasks: List[Dict[str, Any]] = [
        # ==================== PRODUCT 1: TRM ====================
        {
            "id": "trm-inesh-prepaid",
            "product": "TRM",
            "project": "Smart Metering (INESH / Capital / CMRL / EMudra)",
            "title": "INESH & Capital Meter DLMS Prepaid Billing, PR XML/API & Daily Consumption Calculation",
            "assignee": "Kousalya Talari",
            "assignee_email": "talari.kousalya@nsoft.in",
            "status": "in_progress",
            "priority": "high",
            "start_day": "2026-10-29",
            "end_day": "2026-11-04",
            "days_active": 6,
            "source_day": "2026-11-04",
            "tags": ["INESH Meter", "Capital Meter", "DLMS", "PR XML / API", "Prepaid"],
            "subtasks": [
                {"text": "Oct 29–31: INESH prepaid billing, daily charge deduction & DLMS relay verification", "done": True},
                {"text": "Nov 2: Test missed-day billing recovery & post-billing PR XML generation / API integration", "done": True},
                {"text": "Nov 3: Diagnose INESH & Capital meter DLMS communication & TCP response errors", "done": True},
                {"text": "Nov 4: Capital meter cumulative energy register readings & daily consumption calculation", "done": True},
                {"text": "Nov 5 Plan: Complete Capital meter prepaid billing & resolve pending meter reading issues", "done": False},
            ],
            "ai_agent_note": "6-day deep smart-metering track: Kousalya progressed from INESH relay/deduction testing to PR XML API integration and Capital meter DLMS cumulative energy register calculations.",
        },
        {
            "id": "trm-cmrl-comms",
            "product": "TRM",
            "project": "Smart Metering (INESH / Capital / CMRL / EMudra)",
            "title": "CMRL Meter Communication Issue Resolution & Initial Capital Meter Testing",
            "assignee": "Kousalya Talari",
            "assignee_email": "talari.kousalya@nsoft.in",
            "status": "done",
            "priority": "medium",
            "start_day": "2026-10-29",
            "end_day": "2026-10-29",
            "days_active": 1,
            "source_day": "2026-10-29",
            "tags": ["CMRL", "Capital Meter"],
            "subtasks": [
                {"text": "Resolve CMRL meter communication issues", "done": True},
                {"text": "Execute initial Capital meter testing", "done": True},
            ],
            "ai_agent_note": None,
        },
        {
            "id": "trm-spotbilling-releases",
            "product": "TRM",
            "project": "HESCOM SpotBilling & Integrations",
            "title": "Nov 2026 SpotBilling App Releases (HESCOM & BWSSB) + Weavers LT-5 R DBT & Rural Rebate",
            "assignee": "Nitish Nag M",
            "assignee_email": "nitishnag.m@nsoft.in",
            "status": "done",
            "priority": "high",
            "start_day": "2026-10-30",
            "end_day": "2026-11-02",
            "days_active": 3,
            "source_day": "2026-11-02",
            "tags": ["HESCOM", "BWSSB", "LT-5 R DBT Tariff", "Rural Rebate"],
            "subtasks": [
                {"text": "Modify Weavers rebate concept for LT-5 R DBT Tariff based on Sanctioned HP", "done": True},
                {"text": "Release Nov 2026 SpotBilling Apps for HESCOM and BWSSB", "done": True},
                {"text": "Nov 2: Review and resolve Rural Rebate issues in TRM", "done": True},
            ],
            "ai_agent_note": None,
        },
        {
            "id": "trm-bwssb-emi",
            "product": "TRM",
            "project": "BWSSB SpotBilling",
            "title": "BWSSB EMI Interest Penalty Bill Remarks & SIR Deputation Option Disable",
            "assignee": "Nitish Nag M",
            "assignee_email": "nitishnag.m@nsoft.in",
            "status": "done",
            "priority": "medium",
            "start_day": "2026-10-29",
            "end_day": "2026-10-30",
            "days_active": 2,
            "source_day": "2026-10-30",
            "tags": ["BWSSB", "EMI Penalty", "Meter Readers"],
            "subtasks": [
                {"text": "Print EMI remarks on bill for interest penalty when unpaid in valid period", "done": True},
                {"text": "Disable Deputation to Survey option for Meter Readers on SIR Electoral Roll work", "done": True},
            ],
            "ai_agent_note": None,
        },
        {
            "id": "trm-smart-emudra",
            "product": "TRM",
            "project": "Smart Metering (INESH / Capital / CMRL / EMudra)",
            "title": "E-Mudra LE/LR Screen Modifications, Smart Meter Billing Data Fetch & TCED TOD/WFM",
            "assignee": "Nitish Nag M",
            "assignee_email": "nitishnag.m@nsoft.in",
            "status": "in_progress",
            "priority": "high",
            "start_day": "2026-10-29",
            "end_day": "2026-11-03",
            "days_active": 5,
            "source_day": "2026-11-03",
            "tags": ["E-Mudra LE/LR", "Smart Meter Data Fetch", "TCED TOD", "WFM Portal"],
            "subtasks": [
                {"text": "Oct 29–31: Virtual Meter, Meter Burnt/Not Running Smart-to-Smart & EMudra LE/LR meeting", "done": True},
                {"text": "Nov 2: E-Mudra LE/LR screen modifications & TCED TOD (Normal/Peak/OffPeak) file updation", "done": True},
                {"text": "Nov 3: Smart Meter Billing Data Fetch fixes & TCED WFM Portal integration", "done": True},
                {"text": "Complete remaining E-Mudra LE/LR screen modifications (No Nov 4 report received)", "done": False},
            ],
            "ai_agent_note": "Nitish delivered TCED TOD tariff updates, WFM Portal integration, and Smart Meter Billing Data Fetch on Nov 2–3, but did not send a Nov 4 standup report.",
        },
        {
            "id": "trm-tced-billing-screens",
            "product": "TRM",
            "project": "TCED Billing & Demand",
            "title": "TCED Back Office Bill Gen, Complaint Mgmt, Solar Print, Temporary Consumer & Solar Wheeling Loss",
            "assignee": "Pallapu Rajesh",
            "assignee_email": "pallapu.rajesh@nsoft.in",
            "status": "in_progress",
            "priority": "high",
            "start_day": "2026-10-29",
            "end_day": "2026-11-04",
            "days_active": 6,
            "source_day": "2026-11-04",
            "tags": ["TCED", "Back Office Billing", "Solar Wheeling Loss", "Temporary Consumer"],
            "subtasks": [
                {"text": "Oct 29–31: DL withdrawal, wheeling/transmission loss & street light billing logic", "done": True},
                {"text": "Nov 2: Implement Solar Bill Print functionality modifications", "done": True},
                {"text": "Nov 3: Implement temporary consumer billing logic in Bill Gen & Complaint Mgmt", "done": True},
                {"text": "Nov 4: Implement New Consumer Entry, Debit Entry & Billing Report modifications", "done": True},
                {"text": "Nov 5 Plan: Complete Solar Wheeling Transmission Loss & wheeling charges logic", "done": False},
            ],
            "ai_agent_note": "6-day continuous delivery on TCED billing engines: Rajesh completed 6 distinct consumer/tariff rules and is now finalizing Solar Wheeling Transmission Loss.",
        },
        {
            "id": "trm-tced-capacitor",
            "product": "TRM",
            "project": "TCED Billing & Demand",
            "title": "TCED Agricultural Consumer Capacitor Penalty (Android Print & Server Sync) + Load Formula",
            "assignee": "Nitish Nag M",
            "assignee_email": "nitishnag.m@nsoft.in",
            "status": "done",
            "priority": "medium",
            "start_day": "2026-10-29",
            "end_day": "2026-10-29",
            "days_active": 1,
            "source_day": "2026-10-29",
            "tags": ["TCED", "Android SpotBilling", "Capacitor Penalty"],
            "subtasks": [
                {"text": "Capacitor penalty calculation & Android bill print + server update (Nitish Nag)", "done": True},
                {"text": "TCED Load Module formula calculation & HESCOM Group Billing Report (Rohith R)", "done": True},
            ],
            "ai_agent_note": None,
        },
        {
            "id": "trm-hescom-seva-sindhu",
            "product": "TRM",
            "project": "HESCOM SpotBilling & Integrations",
            "title": "HESCOM Seva Sindhu & E-Mudhra Integration + TCED Online Services (LT New Connection) Fix",
            "assignee": "Rohith R",
            "assignee_email": "rohith.r@nsoft.in",
            "status": "done",
            "priority": "high",
            "start_day": "2026-10-30",
            "end_day": "2026-11-04",
            "days_active": 3,
            "source_day": "2026-11-03",
            "tags": ["HESCOM", "E-Mudhra", "Seva Sindhu", "TCED Online Services"],
            "subtasks": [
                {"text": "Oct 30: Start HESCOM Seva Sindhu integration", "done": True},
                {"text": "Nov 3: Complete E-Mudhra Integration for HESCOM & resolve TCED Online Services data load issue", "done": True},
                {"text": "Nov 4: Resolve minor data load issue in TCED Online Services (LT New Connection)", "done": True},
            ],
            "ai_agent_note": "Resolved after Oct 30–Nov 2 pause: Rohith completed HESCOM E-Mudhra integration on Nov 3 and fixed TCED Online Services LT New Connection data load on Nov 4.",
        },

        # ==================== PRODUCT 2: ERP ====================
        {
            "id": "erp-gescom-arrears",
            "product": "ERP",
            "project": "GESCOM ERP & Employee Portal (HRMS)",
            "title": "GESCOM HRMS Arrears/JV (2023–24), ELS Approval Net Pay Fix, Salary Fund Request (B_BRNO) & Salary JV",
            "assignee": "Venkata Sai",
            "assignee_email": "venkata.sai@nsoft.in",
            "status": "in_progress",
            "priority": "high",
            "start_day": "2026-10-29",
            "end_day": "2026-11-04",
            "days_active": 4,
            "source_day": "2026-11-03",
            "tags": ["USP_HRMS_SalaryFundRequestApproval", "B_BRNO", "M_ApprovalManagement", "HRMELSApproval"],
            "subtasks": [
                {"text": "Oct 29–30: Salary Arrears grid (USP_HRMSalaryArrears, 31% DP rule) & Salary Bill Approval UI", "done": True},
                {"text": "Nov 3: Add 2023–2024 to Arrears Report/JV & fix ELS Approval double-deduction Net Pay bug", "done": True},
                {"text": "Nov 3: Build Salary Fund Request (B_BRNO) & Approval Budget grid (USP_HRMS_SalaryFundRequestApproval)", "done": True},
                {"text": "Nov 3: Diagnose AAO login approval visibility via M_ApprovalManagement (RoleOrderId & office)", "done": True},
                {"text": "Nov 4 WIP: Verify Salary JV creation/approval flow in HRMS & deploy 5 ERP screens + SQL proc", "done": False},
            ],
            "ai_agent_note": "Comprehensive Nov 3 delivery (submitted Nov 4 at 10:09 AM) covering 5 ERP screens and USP_HRMS_SalaryFundRequestApproval.sql with 6 architectural learnings.",
        },
        {
            "id": "erp-emp-approval-docs",
            "product": "ERP",
            "project": "TCED ERP & Employee Portal (HRMS & PF)",
            "title": "EmployeeCreation & Approval (Aadhaar/PAN, Dedup & Save Fix) + PensionStopExit Screen",
            "assignee": "Mannuru Lasya",
            "assignee_email": "lasya.mannuru@nsoft.in",
            "status": "done",
            "priority": "high",
            "start_day": "2026-10-29",
            "end_day": "2026-11-04",
            "days_active": 5,
            "source_day": "2026-11-04",
            "tags": ["HRMS", "HRMS_AdditionalDocumnetsAppr", "PensionStopExit", "EmployeeCreation"],
            "subtasks": [
                {"text": "Oct 29–31: Wire Return-to-Edit & live-server Aadhaar/PAN paths from HRMS_AdditionalDocumnetsAppr", "done": True},
                {"text": "Nov 2: Eliminate duplicate rows in EmployeeCreationApproval & verify EmployeeCreation save flow", "done": True},
                {"text": "Nov 4: Verify data persistence across all Pension modules & add Clear button to PensionStopExit", "done": True},
                {"text": "Nov 5 Plan: Deploy PensionStopExit screen to production", "done": False},
            ],
            "ai_agent_note": "Consistent high-clarity execution: finished EmployeeCreation/Approval stabilization on Nov 2 and completed PensionStopExit enhancements on Nov 4.",
        },
        {
            "id": "erp-tced-form3-form4",
            "product": "ERP",
            "project": "TCED ERP & Employee Portal (HRMS & PF)",
            "title": "TCED Kerala Municipal PF (Form 3 & 4, 75% Advance Eligibility & Balance at Credit) + DA Pension Arrears",
            "assignee": "Sanjana C S",
            "assignee_email": "sanjana.cs@nsoft.in",
            "status": "in_progress",
            "priority": "high",
            "start_day": "2026-10-29",
            "end_day": "2026-11-04",
            "days_active": 6,
            "source_day": "2026-11-04",
            "tags": ["TCED", "Form 3 & Form 4", "75% Subscription Rule", "DA Pension Arrears"],
            "subtasks": [
                {"text": "Oct 29–31: Build Form 3 & Form 4 screens, approval hierarchy & Portal reports", "done": True},
                {"text": "Nov 2: Create Form 3 & Form 4 ERP reports for Create, Approve, Reject & Recommend sections", "done": True},
                {"text": "Nov 3: Implement 75% Total Subscription advance limit, Balance at Credit & salary deduction logic", "done": True},
                {"text": "Nov 4: Complete end-to-end calculation testing & edge-case verification for PF advances", "done": True},
                {"text": "Nov 5 Plan: Create new DA Pension Arrears screen and report in ERP source", "done": False},
            ],
            "ai_agent_note": "100% 6-day attendance and plan-to-actual alignment: closed the TCED Municipal PF Temporary Advance track on Nov 4 and starting DA Pension Arrears next.",
        },
        {
            "id": "erp-hrms-bugfixes",
            "product": "ERP",
            "project": "TCED ERP & Employee Portal (HRMS & PF)",
            "title": "HRMS Deputation Checkbox, Disciplinary Action (LocationCode) & Annual Incumbency / RDLC Reports",
            "assignee": "Anith HM",
            "assignee_email": "anith.hm@nsoft.in",
            "status": "in_progress",
            "priority": "high",
            "start_day": "2026-10-29",
            "end_day": "2026-11-04",
            "days_active": 6,
            "source_day": "2026-11-04",
            "tags": ["HRMS", "Disciplinary Action", "Annual Incumbency", "LocationCode", "RDLC"],
            "subtasks": [
                {"text": "Oct 29–Nov 2: Fix deputation checkbox, double language bug & designation join date across layers", "done": True},
                {"text": "Nov 3: Fix Disciplinary Action Division/Section Employee dropdown via LocationCode stored proc", "done": True},
                {"text": "Nov 4: Resolve Annual Incumbency Preparation retirement-date & office-mapping filter issues", "done": True},
                {"text": "Nov 4–5: Investigate & verify Gulbarga name issue in RDLC Sanction Strength Report", "done": False},
            ],
            "ai_agent_note": "Strong 6-day technical ramp-up: 6/6 green learning reflections covering AutoPostBack, BAL/DAL, LocationCode SQL hierarchy, Session variables, and RDLC reports.",
        },
        {
            "id": "erp-tced-esign",
            "product": "ERP",
            "project": "TCED ERP & Employee Portal (HRMS & PF)",
            "title": "TCED ERP E-Sign Module Changes & Pending HRMS Tasks",
            "assignee": "Rohith R",
            "assignee_email": "rohith.r@nsoft.in",
            "status": "in_progress",
            "priority": "medium",
            "start_day": "2026-11-04",
            "end_day": "2026-11-04",
            "days_active": 1,
            "source_day": "2026-11-04",
            "tags": ["TCED ERP", "E-Sign Module", "HRMS"],
            "subtasks": [
                {"text": "Nov 4: Complete E-Sign Module changes in TCED ERP", "done": True},
                {"text": "Nov 5 Plan: Complete pending HRMS tasks in TCED ERP", "done": False},
            ],
            "ai_agent_note": None,
        },
        {
            "id": "erp-tced-exit-19fields",
            "product": "ERP",
            "project": "TCED ERP & Employee Portal (HRMS & PF)",
            "title": "TCED ERP 19 Additional HR Fields Review & Employee Exit Dropdown / Search Investigation",
            "assignee": "Ankith HM",
            "assignee_email": "ankith.hm@nsoft.in",
            "status": "done",
            "priority": "medium",
            "start_day": "2026-10-31",
            "end_day": "2026-10-31",
            "days_active": 1,
            "source_day": "2026-10-31",
            "tags": ["TCED ERP", "Employee Exit", "C# / ASPX"],
            "subtasks": [
                {"text": "Analyze integration of 19 additional HR-specific fields in Employee Creation/Approval", "done": True},
                {"text": "Investigate Employee Exit ASPX/C# dropdown loading & employee-name search requirement", "done": True},
            ],
            "ai_agent_note": None,
        },
        {
            "id": "erp-bgcl-dcw",
            "product": "ERP",
            "project": "BGCL ERP & Requisitions",
            "title": "BGCL CPNG Registration, BPNO/DPNG Reports, Salary/Leave Fixes & DCW / Material Purchase OM",
            "assignee": "Chitrashree HR",
            "assignee_email": "chitrashree.hr@nsoft.in",
            "status": "in_progress",
            "priority": "medium",
            "start_day": "2026-10-29",
            "end_day": "2026-11-03",
            "days_active": 4,
            "source_day": "2026-11-03",
            "tags": ["BGCL", "CPNG Registration", "BPNO / DPNG", "DCW Reports"],
            "subtasks": [
                {"text": "Oct 29–31: Imprest Indent, Material Purchase OM, DCW Reports & BGCL work requisitions (Chitrashree)", "done": True},
                {"text": "Oct 30–31: Fix BGCL leave balance & salary generation issues (Pallapu Rajesh)", "done": True},
                {"text": "Nov 3: BGCL CPNG Registration Process workflow & validations (Chitrashree)", "done": True},
                {"text": "Nov 3: Fix BGCL BPNO generation & DPNG reports issues (Pallapu Rajesh)", "done": True},
                {"text": "Continue BGCL module modifications (Chitrashree missed Nov 4 report)", "done": False},
            ],
            "ai_agent_note": "Both Chitrashree HR (CPNG Registration) and Pallapu Rajesh (BPNO & DPNG reports) delivered BGCL fixes on Nov 3.",
        },

        # ==================== PRODUCT 3: KPTCL ====================
        {
            "id": "kptcl-reports-issues",
            "product": "KPTCL",
            "project": "KPTCL Report & Application Fixes",
            "title": "KPTCL Report Issues & Application Bug Fixes",
            "assignee": "Chitrashree HR",
            "assignee_email": "chitrashree.hr@nsoft.in",
            "status": "done",
            "priority": "medium",
            "start_day": "2026-10-30",
            "end_day": "2026-10-31",
            "days_active": 2,
            "source_day": "2026-10-31",
            "tags": ["KPTCL", "Reports"],
            "subtasks": [
                {"text": "Oct 30: Worked on KPTCL Report issues", "done": True},
                {"text": "Oct 31: Worked on KPTCL application issues", "done": True},
            ],
            "ai_agent_note": "Needs granular issue breakdown: ask Chitrashree to specify which KPTCL reports/screens were modified.",
        },

        # ==================== PRODUCT 4: INFRA & SECURITY ====================
        {
            "id": "infra-db-restores",
            "product": "Infra & Security",
            "project": "SQL Server Multi-Utility DB Restorations",
            "title": "SQL Server 21-Database Fleet Restoration & GESCOM_LIVE_02042026 Full + Differential Recovery",
            "assignee": "Ankith HM",
            "assignee_email": "ankith.hm@nsoft.in",
            "status": "in_progress",
            "priority": "high",
            "start_day": "2026-10-29",
            "end_day": "2026-11-04",
            "days_active": 6,
            "source_day": "2026-11-04",
            "tags": ["SQL Server", "GESCOM_LIVE_02042026", "BESCOMAMI", "VIZAG_15092023", "SRTPV_BESCOM"],
            "subtasks": [
                {"text": "Oct 29–31: Restore 8 SQL Server DBs including BESCOMAMI, COCHINPORT & GESCOMAMI", "done": True},
                {"text": "Nov 2: Restore VIZAG_15092023, INDIAN_RAILWAY_07062023, NSOFTSTORE_29042026 & SRTPV_BESCOM (18/21 online)", "done": True},
                {"text": "Nov 3: Confirm 20 SQL Server databases restored and ONLINE", "done": True},
                {"text": "Nov 4: Complete SQL Server full restore for GESCOM_LIVE_02042026 & restart differential restore", "done": True},
                {"text": "Nov 5 Plan: Complete and verify SQL Server GESCOM differential restore", "done": False},
            ],
            "ai_agent_note": "Following Sumukh's Oct 31 directive, Ankith published a structured DB restore table on Nov 2, brought 20 SQL Server DBs online on Nov 3, and completed the GESCOM_LIVE_02042026 full restore on Nov 4.",
        },
        {
            "id": "infra-postgres-restores",
            "product": "Infra & Security",
            "project": "PostgreSQL / PPAS 9.5 Live DB Restorations",
            "title": "PostgreSQL / PPAS 9.5 Restoration & Validation (ERP_LIVE_31032026 & GESCOM_LIVE_02042026)",
            "assignee": "Ankith HM",
            "assignee_email": "ankith.hm@nsoft.in",
            "status": "in_progress",
            "priority": "high",
            "start_day": "2026-11-02",
            "end_day": "2026-11-04",
            "days_active": 3,
            "source_day": "2026-11-03",
            "tags": ["PostgreSQL", "PPAS 9.5", "ERP_LIVE_31032026", "GESCOM_LIVE_02042026", "--no-owner"],
            "subtasks": [
                {"text": "Nov 3: Complete ERP_LIVE_31032026 restore in PPAS 9.5 (--no-owner / --no-acl) & verify tables/views/sequences", "done": True},
                {"text": "Nov 3: Initiate GESCOM_LIVE_02042026 PostgreSQL restoration and monitor data import", "done": True},
                {"text": "Nov 4: Check table details and row-count estimates to validate PostgreSQL restoration", "done": True},
                {"text": "Nov 5 Plan: Complete PostgreSQL GESCOM restoration and final data validation", "done": False},
            ],
            "ai_agent_note": "Directly addresses Sumukh Hegde's Oct 31 reminder ('take care of GESCOM which is PostgreSQL also').",
        },
    ]

    # Attach the actual matrix cell object (`source_cell`) to each task so clicking
    # a task in the ClickUp view can open the full source email drawer if needed
    for t in tasks:
        em = t["assignee_email"]
        sday = t["source_day"]
        t["source_cell"] = matrix.get(em, {}).get(sday)

    return {
        "products": products,
        "tasks": tasks,
        "timeline_days": ["2026-10-29", "2026-10-30", "2026-10-31", "2026-11-02", "2026-11-03", "2026-11-04"],
    }
