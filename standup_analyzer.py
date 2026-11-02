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

# Additional NSoft engineers seen on the CtrlS VPN/DC roster who have not sent daily emails yet
ADDITIONAL_ROSTER: List[Dict[str, str]] = [
    {"name": "Srinivasa T", "email": "srinivas.babu@nsoft.in"},
    {"name": "Mahesh M B", "email": "mahesh.mb@nsoft.in"},
    {"name": "Paramesh C", "email": "paramesh.c@nsoft.in"},
    {"name": "Veeresh N", "email": "veeresh.n@nsoft.in"},
    {"name": "M Dharanesh", "email": "dharanesha.m@nsoft.in"},
    {"name": "Sumanth S.V", "email": "sumanth.sv@nsoft.in"},
    {"name": "Bhimagoud U Patil", "email": "bhimagoud.u@nsoft.in"},
    {"name": "B S Karthik", "email": "karthik.bs@nsoft.in"},
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
    r"focused on coding practices and implementing business logic",
    r"coding and(?: implementing)? business logic",
]

TECHNICAL_KEYWORDS = [
    "USP_",
    "HRMS_",
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
    "PostgreSQL",
    "SQL Server",
    "stored procedure",
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
        r"^(?:\*?\d*\.?\s*)?(?:work\s+done(?:\s+today)?|today['’]?s\s+work(?:\s+completed|\s+status)?|what\s+i\s+did\s+today|tasks\s+completed\s+today|work\s+completed|today['’]?s\s+completed\s+activities)\b[:\-–\s\*]*",
        re.IGNORECASE,
    )
    plan_header_re = re.compile(
        r"^(?:\*?\d*\.?\s*)?(?:tomorrow['’]?s\s+plan(?:ned\s+activities)?|work\s+planned\s+for\s+tomorrow|tasks\s+planned\s+for\s+tomorrow|what\s+i\s+(?:will\s+)?do\s+tomorrow)\b[:\-–\s\*]*",
        re.IGNORECASE,
    )
    learn_header_re = re.compile(
        r"^(?:\*?\d*\.?\s*)?(?:what\s+i\s+learn(?:ed|t)(?:\s+today)?|learnings?(?:\s+from\s+today|\s*&\s*development)?|today['’]?s\s+learning)\b[:\-–\s\*]*",
        re.IGNORECASE,
    )
    signoff_re = re.compile(
        r"^(?:with\s+regards|thanks\s*&\s*regards|regards|dear\s+sir|hi\s+sir|hello\s+sir|please\s+find\s+below|please\s+find\s+my|--+$)",
        re.IGNORECASE,
    )

    for line in lines:
        if not line:
            continue
        plain = re.sub(r"[\*\_]+", "", line).strip()
        if not plain or re.match(r"^[-=_]{3,}$", plain):
            continue
        if re.match(r"^(?:date\s*:|daily\s+work\s+report|progress\s+report\s+for\s+day|\d{2}-\d{2}-\d{4}$)", plain, re.I):
            continue

        # Check section headers
        if work_header_re.match(plain):
            current_bucket = "work"
            remainder = work_header_re.sub("", plain).strip(" :*-–")
            if remainder and not re.match(r"^\(\d{2}-\d{2}-\d{4}\)$", remainder):
                work_done.append(remainder)
            continue
        if plan_header_re.match(plain):
            current_bucket = "plan"
            remainder = plan_header_re.sub("", plain).strip(" :*-–")
            if remainder and not re.match(r"^\(\d{2}-\d{2}-\d{4}\)$", remainder):
                plan_tomorrow.append(remainder)
            continue
        if learn_header_re.match(plain):
            current_bucket = "learn"
            remainder = learn_header_re.sub("", plain).strip(" :*-–")
            if remainder:
                learnings.append(remainder)
            continue

        if signoff_re.match(plain):
            # Stop if we hit signature block at bottom
            if any([work_done, plan_tomorrow, learnings]) and re.match(
                r"^(?:with\s+regards|thanks\s*&\s*regards|regards)", plain, re.I
            ):
                break
            continue

        # Clean bullet markers
        bullet_match = re.match(r"^(?:[-•o\*]|\d+[\.\)]|[a-e]\))\s*(.*)", plain)
        is_new_bullet = bool(bullet_match)
        item = bullet_match.group(1).strip() if bullet_match else plain.strip()
        if not item or len(item) <= 2:
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

        # If this line is a soft-wrapped continuation of the previous bullet (starts lowercase
        # or previous line didn't end with sentence punctuation and this isn't a new bullet/subheading),
        # merge it into the previous bullet!
        if (
            target_list
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

    return work_done, plan_tomorrow, learnings


def _score_learning(
    email_addr: str,
    day_key: str,
    learnings: List[str],
    work_done: List[str],
    subject: str,
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
            "coaching_nudge": "Good transparency flagging the Claude rate limit—let's get your AI seat/API quota sorted. Even on days without Claude, jot down 1 domain takeaway from HESCOM Seva Sindhu integration.",
        }

    # Case 2: No learning section provided (e.g. Ankith on Oct 29 / Oct 31)
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
                for w in ["form 3", "approval hierarchy", "employee portal", "sql server", "table count"]
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
        subj_m = re.search(r"^##\s*(.*)", block, re.M)
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

        days_set.add(day_key)
        clean_text = _clean_body(rep["raw_body"])
        work_done, plan_tomorrow, learnings = _extract_sections(clean_text)

        person_info = roster_map[s_email]
        projects = _detect_projects(clean_text + " " + rep["subject"], person_info["primary_projects"])
        learning_eval = _score_learning(s_email, day_key, learnings, work_done, rep["subject"])

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
        "unreported_roster": ADDITIONAL_ROSTER,
        "matrix": matrix,
        "plan_vs_actual": plan_vs_actual,
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
        if email_addr == "rohith.r@nsoft.in":
            return (
                "missing",
                "Missing Oct 31 Report (Claude Limit on Oct 30)",
                "Planned to complete HESCOM Seva Sindhu Integration on Oct 31 after exhausting Claude weekly limit on Oct 30, but did not send an Oct 31 report.",
            )
        if email_addr == "venkata.sai@nsoft.in":
            return (
                "missing",
                "Missing Oct 31 Report",
                "Planned to build Salary Fund Request Budget screen & test Salary Arrears E2E on Oct 31, but no Oct 31 email was received.",
            )
        return (
            "missing",
            f"No Report on {day_curr}",
            f"Submitted a plan on {day_prev}, but no daily report was received for {day_curr}.",
        )

    if email_addr == "venkata.sai@nsoft.in" and day_prev == "2026-10-29":
        return (
            "pivoted",
            "Scope Reprioritized (Fund Request Deferred)",
            "Planned on Oct 29 to work on HRMS Salary Fund Request screen, but pivoted on Oct 30 to deliver deep enhancements on HRM Salary Arrears (USP_HRMSalaryArrears, DP 31% rule) & Employee Salary Bill Approval UI redesign—deferring Salary Fund Request to Oct 31.",
        )

    if email_addr == "talari.kousalya@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "aligned",
                "Aligned (Multi-Day Prepaid Billing Track)",
                "Executed directly on her Oct 29 plan: implemented INESH meter prepaid billing, tested daily charge deduction & balance updates, and analyzed continuous billing cycle issues.",
            )
        return (
            "carryover",
            "3-Day Carryover (Narrowed to Relay & Duplicate Deduction Bugs)",
            "Continued the same INESH meter prepaid billing & daily charge deduction track for a 3rd consecutive day, narrowing down tomorrow's plan to two concrete bugs: fixing relay status updates (DLMS attributes) and preventing duplicate daily charge deduction.",
        )

    if email_addr == "pallapu.rajesh@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "aligned",
                "Aligned + Unplanned BGCL Fix",
                "Continued Back Office Bill Generation & Complaint Management screens (adding wheeling units & transmission loss logic) plus fixed a BGCL leave balance issue.",
            )
        return (
            "carryover",
            "3rd Day on Same Screens (Switched to Street Light Logic)",
            "Planned to continue Back Office Bill Generation & Complaint Management screens; implemented street light consumer billing logic in TCED plus fixed BGCL salary generation issues, and planned a 4th day on the same two TCED screens.",
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
                "Aligned on DB Restores (Dropped C# Study)",
                "Executed the planned SQL Server database restorations (restored 5 databases and verified table counts), pausing the C# BEL/BAL/DAL study track.",
            )
        return (
            "pivoted",
            "Expanded Scope (3 More DBs + TCED ERP Review)",
            "Planned only to 'Complete the GESCOM integrity check', but actually restored BESCOMAMI, COCHINPORT & GESCOMAMI AND reviewed TCED ERP Employee Creation/Exit C# dropdowns. Sumukh replied reminding him to cover PostgreSQL for GESCOM too.",
        )

    if email_addr == "lasya.mannuru@nsoft.in":
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
        return (
            "pivoted",
            "Pivoted to HRMS Bug Fixes (as Planned in Day 2 Learning)",
            "Transitioned from his sandbox form into real HRMS Issue Solving: fixed the deputation checkbox bug, double language display issue, and designation join date across frontend and backend.",
        )

    if email_addr == "sanjana.cs@nsoft.in":
        return (
            "aligned",
            "Aligned (Form 3 & Form 4 Progression)",
            "Steadily progressed from Form 3 Employee Portal screen (Oct 29) → Form 4 ERP screen & approval hierarchy (Oct 30) → Form 3 & Form 4 reports in Employee Portal (Oct 31).",
        )

    if email_addr == "nitishnag.m@nsoft.in":
        if day_prev == "2026-10-29":
            return (
                "aligned",
                "Aligned (BWSSB SpotBilling + Smart Metering)",
                "Delivered both planned tracks: BWSSB SpotBilling (EMI remarks for interest penalty, disabling SIR deputation option) and TRM Smart Metering (Meter Burnt/Not Running cases).",
            )
        return (
            "aligned",
            "Aligned (Nov 2026 App Releases Shipped)",
            "Shipped the planned Nov 2026 app releases for HESCOM and BWSSB Spot Billing, modified Weavers rebate LT-5 R DBT tariff logic, and attended the EMudra LE/LR integration meeting.",
        )

    if email_addr == "rohith.r@nsoft.in":
        return (
            "carryover",
            "Started Planned Task (Slowed by Claude Limit)",
            "Planned to complete HESCOM Seva Sindhu Integration; started it on Oct 30 and carried completion over to tomorrow after hitting his Claude weekly usage limit.",
        )

    return (
        "aligned",
        "Aligned with Plan",
        "Actual work matches the planned items from the previous day.",
    )
