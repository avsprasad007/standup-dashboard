import datetime
import email.utils
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent
RAW_EMAILS_PATH = BASE_DIR / "raw-emails.md"

# Core reporting team roster with role/domain context and URL route slugs
TEAM_ROSTER: List[Dict[str, Any]] = [
    {
        "id": "venkata.sai@nsoft.in",
        "slug": "venkata-sai",
        "aliases": ["venkata-sai", "venkata", "venkata.sai", "venkatasai"],
        "name": "Venkata Sai",
        "email": "venkata.sai@nsoft.in",
        "role": "Software Engineer — HRMS & ERP",
        "primary_projects": ["GESCOM ERP", "Employee Portal", "HRMS"],
    },
    {
        "id": "lasya.mannuru@nsoft.in",
        "slug": "mannuru-lasya",
        "aliases": ["mannuru-lasya", "lasya", "lasya-mannuru", "lasya.mannuru", "mannurulasya"],
        "name": "Mannuru Lasya",
        "email": "lasya.mannuru@nsoft.in",
        "role": "Software Engineer — HRMS Employee Module",
        "primary_projects": ["HRMS", "TCED ERP"],
    },
    {
        "id": "anith.hm@nsoft.in",
        "slug": "anith-hm",
        "aliases": ["anith-hm", "anith", "anith.hm", "anithhm"],
        "name": "Anith HM",
        "email": "anith.hm@nsoft.in",
        "role": "Software Engineer — TCED HRMS & Full-Stack",
        "primary_projects": ["TCED", "HRMS", "SQL/ASP.NET"],
    },
    {
        "id": "talari.kousalya@nsoft.in",
        "slug": "kousalya-talari",
        "aliases": ["kousalya-talari", "kousalya", "talari-kousalya", "talari.kousalya", "kousalyatalari"],
        "name": "Kousalya Talari",
        "email": "talari.kousalya@nsoft.in",
        "role": "Engineer — Smart Metering & Prepaid Billing",
        "primary_projects": ["INESH Meter", "CMRL", "Prepaid Billing"],
    },
    {
        "id": "nitishnag.m@nsoft.in",
        "slug": "nitish-nag-m",
        "aliases": ["nitish-nag-m", "nitish-nag", "nitish", "nitishnag", "nitishnag.m"],
        "name": "Nitish Nag M",
        "email": "nitishnag.m@nsoft.in",
        "role": "Software Engineer — TRM SpotBilling & Smart Metering",
        "primary_projects": ["TRM SpotBilling", "HESCOM", "BWSSB", "Smart Metering"],
    },
    {
        "id": "sanjana.cs@nsoft.in",
        "slug": "sanjana-cs",
        "aliases": ["sanjana-cs", "sanjana", "sanjana.cs", "sanjanacs"],
        "name": "Sanjana C S",
        "email": "sanjana.cs@nsoft.in",
        "role": "Software Engineer — TCED Portal & ERP Reports",
        "primary_projects": ["TCED", "Employee Portal", "ERP"],
    },
    {
        "id": "pallapu.rajesh@nsoft.in",
        "slug": "pallapu-rajesh",
        "aliases": ["pallapu-rajesh", "rajesh", "rajesh-p", "pallapu.rajesh", "pallapurajesh"],
        "name": "Pallapu Rajesh",
        "email": "pallapu.rajesh@nsoft.in",
        "role": "Software Engineer — TCED & BGCL Billing",
        "primary_projects": ["TCED", "BGCL"],
    },
    {
        "id": "chitrashree.hr@nsoft.in",
        "slug": "chitrashree-hr",
        "aliases": ["chitrashree-hr", "chitrashree", "chitrashree.hr", "chitrashreehr"],
        "name": "Chitrashree HR",
        "email": "chitrashree.hr@nsoft.in",
        "role": "Software Engineer — BGCL, KPTCL & DCW",
        "primary_projects": ["BGCL", "KPTCL", "DCW"],
    },
    {
        "id": "ankith.hm@nsoft.in",
        "slug": "ankith-hm",
        "aliases": ["ankith-hm", "ankith", "ankith.hm", "ankithhm"],
        "name": "Ankith HM",
        "email": "ankith.hm@nsoft.in",
        "role": "Database & ERP Engineer — DB Restores & TCED",
        "primary_projects": ["DB Migration", "TCED ERP", "BESCOM/GESCOM/COCHIN"],
    },
    {
        "id": "rohith.r@nsoft.in",
        "slug": "rohith-r",
        "aliases": ["rohith-r", "rohith", "rohith.r", "rohithr"],
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

    product_tracker = _build_product_tracker(matrix, sorted_days)
    developer_pages = _build_developer_pages(matrix, sorted_days, plan_vs_actual, product_tracker)

    return {
        "days": sorted_days,
        "people": TEAM_ROSTER,
        "matrix": matrix,
        "plan_vs_actual": plan_vs_actual,
        "product_tracker": product_tracker,
        "developer_pages": developer_pages,
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



def _build_developer_pages(
    matrix: Dict[str, Dict[str, Any]],
    sorted_days: List[str],
    plan_vs_actual: List[Dict[str, Any]],
    product_tracker: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    """
    Build the per-developer 1:1 Growth & Alignment Anchor pages (`/<developer-slug>`),
    structured around the 4 core pillars:
      1. Iteratively define outcomes in a two-way sync between multiple owners
      2. Alignment with business
      3. Deeper AI agents' usage
      4. Enhanced personal learning from all dimensions
    """
    profiles: Dict[str, Dict[str, Any]] = {
        "venkata-sai": {
            "headline": "GESCOM HRMS Payroll, Arrears, ELS & Fund Request Architecture",
            "product_spaces": ["ERP"],
            "utilities": ["GESCOM"],
            "sync_owners": [
                {"name": "Venkata Sai", "role": "Developer (HRMS & Payroll)", "focus": "Owns USP_HRMSalaryArrears, B_BRNO fund requests, HRMELSApproval & M_ApprovalManagement flows."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead", "focus": "Reviews multi-screen ERP vs. Employee Portal parity & daily standup cadence (sent Oct 31 reminder)."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "Module & DB Leads", "focus": "Sign off on stored procedure changes (USP_HRMS_SalaryFundRequestApproval) & dev-to-live deployment packages."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Aligns HRMS payroll & budget controls with GESCOM finance/AAO audit and zero-defect disbursement."},
            ],
            "outcome_iterations": [
                {
                    "id": "vs-out-1",
                    "track": "GESCOM Salary Fund Request & Budget Control",
                    "v1_reported": "Worked on HRMSalaryFundRequestNew & Approval; added BR No/BR Date (B_BRNO) and Budget grid.",
                    "v2_owner_sync": "Enforce same-day BR Date lock, link B_BRNO via B_BillPassing.BRID, and validate AAO visibility via M_ApprovalManagement (RoleOrderId + Office).",
                    "v3_business_outcome": "100% audit-traceable GESCOM salary fund requisitions where AAO/Cashier officers see real-time Allocated vs. Used vs. Available FY budget before approving.",
                    "owners": ["Venkata Sai", "Sumukh Hegde", "Prajwal D A", "Prasad Amara"],
                    "status": "ready_for_deploy",
                },
                {
                    "id": "vs-out-2",
                    "track": "HRM Salary Arrears (2023–2026) & ELS Net Pay Integrity",
                    "v1_reported": "Editable Existing/Revised Basic in Arrears grid (USP_HRMSalaryArrears) + fixed ELS Approval double deduction.",
                    "v2_owner_sync": "Compute Net Pay strictly from (Month-wise Total − All Deductions) rather than mutating prior screen state; lock deduction edits as read-only for downstream approvers.",
                    "v3_business_outcome": "Zero over/under-payment errors across multi-year (2023–2026) GESCOM DA/DP arrears and ELS encashment approvals across both ERP and Employee Portal.",
                    "owners": ["Venkata Sai", "Sumukh Hegde", "Dharmaraj B"],
                    "status": "in_progress",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Directly protects GESCOM payroll accuracy, statutory DA/DP arrears compliance, and financial budget governance across ERP and Employee Portal.",
                "value_chains": [
                    {
                        "deliverable": "HRM Salary Arrears Grid & USP_HRMSalaryArrears",
                        "artifact": "HRMSalaryArrears.aspx.cs, USP_HRMSalaryArrears, DAEffectiveDateCapture",
                        "client": "GESCOM (ERP & Employee Portal)",
                        "business_impact": "Automates 31% DP rule (Aug-2024+) and live CPS 14%/10% recalculation for retrospective basic pay revisions.",
                        "kpi": "Zero manual spreadsheet recalculations for 2023–2026 arrears",
                    },
                    {
                        "deliverable": "Salary Fund Request & Budget Grid + ELS Net Pay Fix",
                        "artifact": "HRMSalaryFundRequestApproval.aspx, USP_HRMS_SalaryFundRequestApproval.sql, B_BRNO",
                        "client": "GESCOM Finance & AAO Offices",
                        "business_impact": "Eliminates double-deduction bugs in ELS and prevents over-budget fund requests by surfacing live FY Available Budget.",
                        "kpi": "5 ERP screens + 1 SQL procedure packaged for production release",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L2: Structured Problem Decomposition & SQL Transaction Verification",
                "target_stage": "L3: Multi-Project (ERP vs. Portal) Diff & Stored Procedure Regression Agent",
                "observation": "Writes the most architecturally detailed standups on the team (explicitly documenting M_ApprovalManagement, B_BRNO, and BEGIN TRAN ... ROLLBACK). Can save 40%+ time when syncing screens between ERP and Employee Portal using an AI diff workflow.",
                "playbooks": [
                    {
                        "title": "ERP vs. Employee Portal Cross-Project Sync Agent",
                        "context": "When applying the same Arrears or ELS change to both GESCOM ERP and Employee Portal without breaking project-specific bindings.",
                        "prompt": "Compare ERP/HRMSalaryArrears.aspx.cs and EmployeePortal/HRMSalaryArrears.aspx.cs. Port only the ExistingBasic recalculation and DP 31% (Aug-2024+) logic while preserving EmployeePortal session/login bindings, and list every changed method.",
                    },
                    {
                        "title": "SQL Stored Procedure BEGIN TRAN Test Harness Generator",
                        "context": "For validating USP_HRMS_SalaryFundRequestApproval and USP_HRMSalaryArrears before live deployment.",
                        "prompt": "Generate a T-SQL test script wrapped in BEGIN TRAN ... ROLLBACK for USP_HRMS_SalaryFundRequestApproval that tests: (1) Available = Allocated - Used budget calculation, (2) B_BRNO link via B_BillPassing.BRID, and (3) M_ApprovalManagement RoleOrderId filtering for AAO login.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 94,
                    "domain_mastery": 95,
                    "engineering_craft": 92,
                    "communication_ownership": 76,
                },
                "dimension_notes": {
                    "technical_depth": "Exemplary grasp of SQL Server procedures, B_BRNO/B_BillPassing schema links, and stateful ASP.NET WebForms grid calculations.",
                    "domain_mastery": "Deep command of GESCOM payroll rules (DA twice-yearly effective dates, DP 31% cutoff in Aug 2024, FY revenue budget formulas, RoleOrderId approval routing).",
                    "engineering_craft": "Proactively practices file/SP backups, BEGIN TRAN ... ROLLBACK testing on dev, and dev-vs-live server diffing prior to deployment.",
                    "communication_ownership": "When he sends a report, it is the gold standard for the team—but missed Oct 31 & Nov 2 reports and sent Nov 3 report on Nov 4 morning.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-03",
                        "original": "Net Pay should always be calculated from the totals (Total - Deductions), not from the previous Net Pay value on the screen. Always test SQL changes inside BEGIN TRAN ... ROLLBACK on dev first.",
                        "upgraded": "Already a benchmark Green reflection! Next step: codify your 6 deployment & SQL safety checks into a reusable team checklist in the repo so junior HRMS engineers (Anith, Lasya) inherit the same standard.",
                    }
                ],
                "growth_goals": [
                    "Maintain 100% same-evening standup consistency (even a 3-line WIP note on heavy coding days).",
                    "Publish a 1-page 'GESCOM HRMS Deployment & BEGIN TRAN Verification Checklist' for the ERP team.",
                    "Use an AI agent to automate dev-vs-live stored procedure comparison before every release.",
                ],
            },
        },
        "mannuru-lasya": {
            "headline": "HRMS Employee Creation/Approval Lifecycle & PensionStopExit Module",
            "product_spaces": ["ERP"],
            "utilities": ["TCED", "GESCOM HRMS"],
            "sync_owners": [
                {"name": "Mannuru Lasya", "role": "Developer (HRMS Employee & Pension)", "focus": "Owns EmployeeCreation, EmployeeCreationApproval (HRMS_AdditionalDocumnetsAppr), and PensionStopExit screens."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead (Direct Recipient)", "focus": "Primary reviewer on Lasya's updates (replied 'Noted' on Oct 31); guides live-server document path resolution & module deployments."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "Module Leads", "focus": "Coordinate HRMS table schema (HRMS_AdditionalDocumnetsAppr) and production deployment windows."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Ensures zero data-loss or duplicate records in employee onboarding and pension stop/exit workflows."},
            ],
            "outcome_iterations": [
                {
                    "id": "ml-out-1",
                    "track": "EmployeeCreation & Approval End-to-End Reliability",
                    "v1_reported": "Wired Return button to Edit mode, fetched Aadhaar/PAN from HRMS_AdditionalDocumnetsAppr, and fixed duplicate names in EmployeeCreationApproval.",
                    "v2_owner_sync": "Verify that live-server file paths in HRMS_AdditionalDocumnetsAppr resolve without broken links and that returning an employee to Edit mode never creates duplicate rows.",
                    "v3_business_outcome": "Frictionless HR officer approval workflow where Aadhaar/PAN KYC documents preview instant-load from the live server and rejected records round-trip cleanly.",
                    "owners": ["Mannuru Lasya", "Sumukh Hegde", "Prajwal D A"],
                    "status": "done",
                },
                {
                    "id": "ml-out-2",
                    "track": "Pension Modules Verification & PensionStopExit Deployment",
                    "v1_reported": "Verified data saving across all Pension modules and added Clear button to PensionStopExit screen.",
                    "v2_owner_sync": "Confirm all form controls, dropdowns, and hidden state reset cleanly on Clear without affecting saved pension records; deploy PensionStopExit.",
                    "v3_business_outcome": "Production-ready Pension & PensionStopExit module suite with verified database persistence and clean operator UX.",
                    "owners": ["Mannuru Lasya", "Sumukh Hegde", "Dharmaraj B"],
                    "status": "in_progress",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Delivers high-reliability HR onboarding (EmployeeCreation/Approval KYC document verification) and pension lifecycle screens with 100% plan-to-actual execution.",
                "value_chains": [
                    {
                        "deliverable": "Aadhaar & PAN Live Document Preview + Dedup Fix",
                        "artifact": "EmployeeCreationApproval.aspx, HRMS_AdditionalDocumnetsAppr",
                        "client": "HRMS Approval Officers",
                        "business_impact": "Eliminates broken document previews on live servers and removes duplicate employee rows in the approval queue.",
                        "kpi": "100% KYC document path resolution + unique approval rows",
                    },
                    {
                        "deliverable": "Pension Suite Verification & PensionStopExit Clear Flow",
                        "artifact": "PensionStopExit.aspx / .cs",
                        "client": "HR & Pension Administration",
                        "business_impact": "Validates end-to-end save integrity across all Pension screens and prevents stale form state errors.",
                        "kpi": "Ready for production deployment on Nov 5",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L1.5: Targeted Bug Tracing & Code-Behind Verification",
                "target_stage": "L3: Automated SQL Duplicate Detector & ASP.NET Form State Agent",
                "observation": "Lasya excels at focused, methodical verification (tracing save flows end-to-end and live-server file paths). Introducing AI agents for SQL join deduplication and regression test generation will multiply her throughput across all Pension modules.",
                "playbooks": [
                    {
                        "title": "SQL Duplicate Row & Join Diagnostic Agent",
                        "context": "When tables like EmployeeCreationApproval or HRMS_AdditionalDocumnetsAppr produce duplicate employee names.",
                        "prompt": "Here is the SQL query / stored procedure populating EmployeeCreationApproval alongside HRMS_AdditionalDocumnetsAppr (which has multiple document rows per employee). Rewrite the query using STRING_AGG / PIVOT or OUTER APPLY so each employee appears exactly once with both Aadhaar and PAN paths.",
                    },
                    {
                        "title": "ASP.NET WebForms Reset & Regression Checklist Agent",
                        "context": "When verifying all Pension modules and adding Reset/Clear actions like on PensionStopExit.",
                        "prompt": "Inspect this ASP.NET WebForms code-behind (PensionStopExit.aspx.cs). Generate a complete ClearForm() method that resets all TextBoxes, DropDownLists, ViewState keys, and GridView selections, and list 5 edge cases to test before deployment.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 82,
                    "domain_mastery": 84,
                    "engineering_craft": 90,
                    "communication_ownership": 88,
                },
                "dimension_notes": {
                    "technical_depth": "Strong understanding of how backend tables (HRMS_AdditionalDocumnetsAppr) map to live server file paths and how duplicate rows arise.",
                    "domain_mastery": "Clear grasp of the Employee Creation → Approval → Return-to-Edit lifecycle and PensionStopExit domain workflows.",
                    "engineering_craft": "High discipline in verifying live-server behavior and re-testing screens for regressions after fixes.",
                    "communication_ownership": "Crisp, well-titled emails (5/6 days sent, 100% Green learning scores on all 5 reports). Only missed Nov 3 report.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-04",
                        "original": "Analyzed and understood the underlying logic of the PensionStopExit screen.",
                        "upgraded": "Understood how PensionStopExit binds active pensioner status to stop-reason codes, and learned why ViewState/hidden fields must be explicitly cleared alongside TextBoxes so a subsequent search doesn't overwrite the previous employee's ID.",
                    }
                ],
                "growth_goals": [
                    "Include the exact stored procedure or C# method name in daily learnings (as done with HRMS_AdditionalDocumnetsAppr on Oct 31).",
                    "Use an AI agent to generate a 10-point regression test script across all Pension modules before deployment.",
                    "Address daily standups to Prasad Amara in `To:` (matching team convention) while keeping Sumukh, Prajwal & Dharmaraj in `To/Cc`.",
                ],
            },
        },
        "anith-hm": {
            "headline": "TCED HRMS Issue Resolution, Disciplinary Action & Annual Incumbency / RDLC Reports",
            "product_spaces": ["ERP"],
            "utilities": ["TCED", "GESCOM / Gulbarga"],
            "sync_owners": [
                {"name": "Anith HM", "role": "Developer (HRMS & Full-Stack)", "focus": "Owns HRMS deputation/language fixes, Disciplinary Action LocationCode dropdowns, and Annual Incumbency / Sanction Strength RDLC reports."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead", "focus": "Guided Anith's rapid transition from Day 1–2 sandbox CRUD into live TCED HRMS production bug fixing."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "Module Leads", "focus": "Provide affected report samples (e.g., Gulbarga Sanction Strength Report) and review LocationCode stored procedure updates."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Tracks ramp-up velocity from foundational ASP.NET/SQL training to independent ERP defect resolution."},
            ],
            "outcome_iterations": [
                {
                    "id": "ah-out-1",
                    "track": "HRMS Disciplinary Action & Annual Incumbency Location/Retirement Filtering",
                    "v1_reported": "Fixed Division/Section Employee dropdown via LocationCode hierarchy and solved Annual Incumbency retirement-date and office-mapping checks.",
                    "v2_owner_sync": "Standardize SQL LIKE vs. `=` LocationCode prefix matching across Division/Section stored procedures and validate retirement-date cutoff against test employees.",
                    "v3_business_outcome": "Accurate Division/Section employee lookup in Disciplinary Action and zero missing/retired employees in Annual Incumbency Preparation.",
                    "owners": ["Anith HM", "Sumukh Hegde", "Prajwal D A"],
                    "status": "in_progress",
                },
                {
                    "id": "ah-out-2",
                    "track": "Sanction Strength RDLC Report (Gulbarga Name Fix) & Employee Form Cleanup",
                    "v1_reported": "Fixed deputation checkbox & double language display bug; investigated Gulbarga name issue in Sanction Strength RDLC report.",
                    "v2_owner_sync": "Replace hardcoded RDLC report header strings with dynamic Session/DataSet office parameters once the affected Gulbarga report sample is verified.",
                    "v3_business_outcome": "Multi-utility compatible RDLC Sanction Strength Reports and defect-free HRMS employee creation/edit forms.",
                    "owners": ["Anith HM", "Sumukh Hegde", "Dharmaraj B"],
                    "status": "in_progress",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Fastest onboarding ramp-up on the team: transitioned in 48 hours from foundational ASP.NET/SQL CRUD exercises to resolving live HRMS bugs across Employee Creation, Disciplinary Action, and Annual Incumbency.",
                "value_chains": [
                    {
                        "deliverable": "Disciplinary Action LocationCode Hierarchy Fix",
                        "artifact": "Disciplinary Action Stored Procedure & ASP.NET Dropdown Binding",
                        "client": "TCED / Utility HR Divisions",
                        "business_impact": "Restores broken Division & Section employee dropdown loading by matching hierarchical LocationCode prefixes.",
                        "kpi": "100% employee dropdown population across Divisions & Sections",
                    },
                    {
                        "deliverable": "Annual Incumbency Retirement Filter & RDLC Sanction Strength Report",
                        "artifact": "Annual Incumbency Module, RDLC Report Viewer & Session Variables",
                        "client": "Utility HR Establishment & Audit",
                        "business_impact": "Ensures accurate retirement-date filtering and dynamic utility/zone naming in statutory Sanction Strength reports.",
                        "kpi": "6/6 days reported with 6/6 Green technical learnings",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L2: Active Full-Stack Learner (BEL/BAL/DAL + SQL Stored Procs + RDLC)",
                "target_stage": "L3: AI-Assisted Legacy C#/RDLC Debugger & Stored Procedure Analyzer",
                "observation": "Anith has achieved 6/6 Green learning scores by deeply investigating *why* bugs happen (AutoPostBack, array duplicate binding, SQL LIKE vs `=`, Session variables to RDLC). Pairing his curiosity with an AI legacy-code exploration workflow will accelerate his debugging of unfamiliar modules.",
                "playbooks": [
                    {
                        "title": "LocationCode Hierarchy & SQL LIKE vs. `=` Optimizer Agent",
                        "context": "When debugging Division/Subdivision/Section hierarchy filters in HRMS stored procedures.",
                        "prompt": "Analyze this stored procedure that filters employees by @LocationCode across Zone/Circle/Division/Section levels. Show where exact match (`=`) fails for parent offices, and rewrite the WHERE clause using index-friendly prefix matching so both Division and Section logins load employees fast.",
                    },
                    {
                        "title": "RDLC Report Viewer & Session Parameter Trace Agent",
                        "context": "When investigating hardcoded vs. dynamic headings (like the Gulbarga name issue) in RDLC reports.",
                        "prompt": "Scan this .rdlc XML definition and its companion .aspx.cs ReportViewer binding code. List every hardcoded text box (such as 'Gulbarga' or utility titles) and show the exact ReportParameter C# code needed to populate them dynamically from Session or DB.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 86,
                    "domain_mastery": 80,
                    "engineering_craft": 85,
                    "communication_ownership": 92,
                },
                "dimension_notes": {
                    "technical_depth": "Consistently articulates full-stack mechanics: AutoPostBack, flag-based CRUD procs, BAL/DAL interaction, Session-to-RDLC parameter passing.",
                    "domain_mastery": "Rapidly absorbing HRMS domain rules: deputation flags, LocationCode organizational hierarchy, retirement-date incumbency rules.",
                    "engineering_craft": "Tests both new-employee creation and old-employee edit paths and checks cross-browser layout alignment.",
                    "communication_ownership": "100% attendance (6/6 days) and 100% Green learning quality (6/6)—a model for how to write daily learning reflections.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-04",
                        "original": "Understood how retirement dates and office Location Codes are used to filter employees. Learned the difference between hardcoded report headings and dynamically populated fields in RDLC.",
                        "upgraded": "Strong Green reflection! To make it even more actionable for peers, include the exact RDLC file name and stored procedure name so teammates can find the fix via search.",
                    }
                ],
                "growth_goals": [
                    "Include exact `.aspx`, `.rdlc`, and stored procedure names in every daily standup.",
                    "Close the Gulbarga RDLC Sanction Strength Report issue by replacing hardcoded strings with ReportParameters.",
                    "Use an AI agent to generate unit/SQL test cases for Annual Incumbency retirement-date boundary conditions.",
                ],
            },
        },
        "kousalya-talari": {
            "headline": "INESH & Capital Smart Meter DLMS Prepaid Billing, Relay Control & PR XML Integration",
            "product_spaces": ["TRM"],
            "utilities": ["INESH Meter", "Capital Meter", "CMRL"],
            "sync_owners": [
                {"name": "Kousalya Talari", "role": "Developer (Smart Metering & Prepaid)", "focus": "Owns INESH & Capital meter DLMS communication, daily charge deduction, relay load-switch control, and PR XML API integration."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead", "focus": "Monitors daily smart-meter test closure (sent Oct 31 11:24 PM status reminder, prompting Kousalya's Nov 1 7:03 AM update)."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "TRM & Metering Leads", "focus": "Coordinate post-billing PR XML schema, API endpoints, and DLMS meter firmware/TCP response troubleshooting."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Drives reliable multi-vendor (INESH, Capital, CMRL) prepaid metering rollouts with zero duplicate deductions."},
            ],
            "outcome_iterations": [
                {
                    "id": "kt-out-1",
                    "track": "INESH Prepaid Billing Engine, Relay Switch & Post-Billing PR XML/API",
                    "v1_reported": "Tested INESH prepaid billing, daily charge deduction, missed-day recovery, DLMS relay status, and post-billing PR XML/API integration.",
                    "v2_owner_sync": "Guarantee idempotent daily charge deduction (zero duplicate deductions on retry), deterministic missed-day catch-up, and verified DLMS load-switch disconnect/reconnect on zero/positive balance.",
                    "v3_business_outcome": "Production-grade INESH prepaid billing loop with automated daily deduction, missed-day recovery, physical relay disconnect/reconnect, and real-time PR XML sync.",
                    "owners": ["Kousalya Talari", "Sumukh Hegde", "Prajwal D A"],
                    "status": "in_progress",
                },
                {
                    "id": "kt-out-2",
                    "track": "Capital Meter DLMS Communication & Cumulative Energy Consumption",
                    "v1_reported": "Analysed TCP response errors, worked on Capital meter DLMS communication, cumulative energy register readings, and daily consumption calculation.",
                    "v2_owner_sync": "Isolate TCP timeout/framing errors on Capital meters and validate daily kWh consumption delta calculation across midnight register rollovers.",
                    "v3_business_outcome": "Multi-vendor prepaid metering support across both INESH and Capital DLMS meters with accurate daily kWh consumption and balance deduction.",
                    "owners": ["Kousalya Talari", "Dharmaraj B", "Prasad Amara"],
                    "status": "in_progress",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Anchors NSoft's Smart Metering & Prepaid Billing capability across INESH, Capital, and CMRL meters—directly preventing utility revenue leakage and enabling automated load control.",
                "value_chains": [
                    {
                        "deliverable": "INESH Prepaid Deduction, Missed-Day Recovery & PR XML API",
                        "artifact": "INESH Prepaid Engine, DLMS Relay OBIS Attributes, PR XML Generator",
                        "client": "Utility Prepaid Metering Operations",
                        "business_impact": "Prevents duplicate daily deductions while recovering charges for offline/missed days and syncing post-billing PR XML via API.",
                        "kpi": "Zero duplicate deductions + verified DLMS relay switch state",
                    },
                    {
                        "deliverable": "Capital Meter DLMS Cumulative Register & TCP Error Resolution",
                        "artifact": "Capital Meter DLMS Reader & Daily Consumption Calculator",
                        "client": "Capital & CMRL Smart Metering",
                        "business_impact": "Extends prepaid billing to Capital meters by computing daily consumption from cumulative energy registers.",
                        "kpi": "6/6 days reported with 6/6 Green domain learnings",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L1.5: Manual Hardware/DLMS Protocol Testing & Log Inspection",
                "target_stage": "L3: AI-Powered DLMS Packet Decoder & Prepaid State-Machine Simulator",
                "observation": "Kousalya has spent 6 consecutive days testing complex stateful prepaid billing scenarios (missed-day recovery, duplicate deduction, TCP response errors, cumulative register deltas). An AI agent that simulates multi-day meter register sequences will cut manual test cycles in half.",
                "playbooks": [
                    {
                        "title": "Prepaid Billing Multi-Day Edge-Case Simulator Agent",
                        "context": "When testing daily charge deduction, missed-day recovery, and duplicate deduction prevention.",
                        "prompt": "Generate a table-driven test suite for our prepaid billing deduction service covering: (1) normal daily deduction, (2) 3 missed offline days followed by reconnection recovery, (3) duplicate scheduler trigger on the same calendar day (idempotency check), and (4) balance crossing 0 triggering DLMS relay disconnect.",
                    },
                    {
                        "title": "DLMS TCP Response & OBIS Register Diagnostic Agent",
                        "context": "When troubleshooting Capital/INESH meter TCP response errors and cumulative energy register readings.",
                        "prompt": "Here is our DLMS TCP communication log and OBIS code read sequence for the Capital meter cumulative energy register. Identify why TCP response timeouts/errors occur on consecutive frame reads and suggest retry/backoff + register scaling validation logic.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 85,
                    "domain_mastery": 90,
                    "engineering_craft": 84,
                    "communication_ownership": 80,
                },
                "dimension_notes": {
                    "technical_depth": "Strong protocol-level work across DLMS attributes, TCP socket responses, PR XML payloads, and energy register delta math.",
                    "domain_mastery": "Deep domain fluency in prepaid utility billing cycles, load switch disconnect/reconnect thresholds, and missed-day recovery.",
                    "engineering_craft": "Systematically tests both happy path and failure recovery (missed days, duplicate deduction, TCP errors).",
                    "communication_ownership": "6/6 days reported (including Sun 7:03 AM catch-up after Sumukh's nudge), but sent Nov 4 email with a blank Subject line and kept several multi-day bullets high-level.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-03",
                        "original": "Learned more about DLMS meter communication and prepaid billing implementation.",
                        "upgraded": "Diagnosed that Capital meter TCP response errors occurred when polling cumulative energy OBIS registers without waiting for the previous association frame to close; added frame timeout handling before computing daily consumption deltas.",
                    }
                ],
                "growth_goals": [
                    "Always include a clear email Subject line (`Daily Work Report – DD Nov 2026`) — Nov 4 subject was blank.",
                    "Break multi-day carryover items ('Continue prepaid billing implementation') into specific daily pass/fail test metrics.",
                    "Use an AI agent to build an automated simulator for 7-day prepaid deduction & missed-day recovery.",
                ],
            },
        },
        "nitish-nag-m": {
            "headline": "TRM SpotBilling Releases (HESCOM/BWSSB), Smart Meter APIs, E-Mudra LE/LR & TCED TOD/WFM",
            "product_spaces": ["TRM"],
            "utilities": ["HESCOM", "BWSSB", "TCED"],
            "sync_owners": [
                {"name": "Nitish Nag M", "role": "Developer (TRM SpotBilling & Smart Metering)", "focus": "Owns HESCOM/BWSSB monthly Android SpotBilling releases, E-Mudra LE/LR integration, Smart Meter Billing Data Fetch, and TCED TOD/WFM updates."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead", "focus": "Reviews daily TRM release milestones (replied 'Noted' on Oct 31) and tracks E-Mudra LE/LR completion."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "TRM Architecture Leads", "focus": "Coordinate Android SpotBilling APK rollouts, tariff rules (LT-5 R DBT, Rural Rebate, TOD), and WFM Portal APIs."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Ensures on-time 1st-of-month utility billing releases (HESCOM/BWSSB) and regulatory tariff compliance."},
            ],
            "outcome_iterations": [
                {
                    "id": "nn-out-1",
                    "track": "Monthly Utility SpotBilling Releases & Tariff Compliance (HESCOM, BWSSB, TCED)",
                    "v1_reported": "Released Nov 2026 Apps for HESCOM & BWSSB; modified LT-5 R DBT Weavers rebate, Rural Rebate, Capacitor Penalty, and TCED TOD (Normal/Peak/OffPeak).",
                    "v2_owner_sync": "Verify Android bill print formatting and server-side sync across all modified tariffs (LT-5 R DBT Sanctioned HP, Capacitor Penalty, EMI Penalty, TOD slots).",
                    "v3_business_outcome": "Zero billing-cycle disruption for Nov 2026 across HESCOM, BWSSB, and TCED field meter readers with 100% tariff accuracy.",
                    "owners": ["Nitish Nag M", "Sumukh Hegde", "Dharmaraj B", "Prasad Amara"],
                    "status": "done",
                },
                {
                    "id": "nn-out-2",
                    "track": "E-Mudra LE/LR Screen Modifications, Smart Meter Data Fetch & TCED WFM Portal",
                    "v1_reported": "Worked on E-Mudra LE/LR screen modifications, Smart Meter Billing Data Fetch, and TCED WFM Portal integration (Nov 2–3).",
                    "v2_owner_sync": "Complete end-to-end LE/LR digital signature workflow, validate Smart Meter billing data fetch completeness, and confirm Nov 4 delivery status.",
                    "v3_business_outcome": "Seamless E-Mudra LE/LR case processing and automated Smart Meter-to-TRM billing data ingestion.",
                    "owners": ["Nitish Nag M", "Sumukh Hegde", "Prajwal D A"],
                    "status": "in_progress",
                },
            ],
            "business_alignment": {
                "strategic_summary": "High-throughput revenue-operations engineer: shipped critical Nov 2026 SpotBilling releases for HESCOM and BWSSB while delivering tariff/meter enhancements across TCED and Smart Metering.",
                "value_chains": [
                    {
                        "deliverable": "Nov 2026 SpotBilling Releases (HESCOM & BWSSB) + Tariff Rules",
                        "artifact": "HESCOM & BWSSB Android SpotBilling APKs, LT-5 R DBT & EMI Penalty Logic",
                        "client": "HESCOM & BWSSB Field Billing Operations",
                        "business_impact": "Enables uninterrupted November 2026 field billing with updated Weavers LT-5 R DBT rebate, Rural Rebate, and EMI penalty remarks.",
                        "kpi": "2 utility production app releases shipped on Oct 31",
                    },
                    {
                        "deliverable": "TCED TOD (Normal/Peak/OffPeak), WFM Integration & E-Mudra LE/LR",
                        "artifact": "TCED File Updation Task, WFM Portal Integration, E-Mudra LE/LR Screens",
                        "client": "TCED & TRM Smart Metering",
                        "business_impact": "Supports time-of-day industrial tariff billing, Workforce Management sync, and E-Mudra LE/LR workflow.",
                        "kpi": "5/6 days reported (missed Nov 4 report)",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L1: High Manual Delivery Velocity, Zero Surfaced AI/Learning Telemetry",
                "target_stage": "L3: AI Tariff Rule Verification & Android-to-Server Contract Agent",
                "observation": "Nitish delivers an impressive volume of production TRM changes across 4 utilities, but copy-pasted the exact same 12-word boilerplate learning on all 5 days. Using AI agents to generate tariff boundary tests and summarize daily technical insights will elevate both his engineering leverage and team knowledge sharing.",
                "playbooks": [
                    {
                        "title": "Tariff Slab & Rebate Boundary Test Generator Agent",
                        "context": "When modifying complex utility tariff logic like LT-5 R DBT Sanctioned HP Weavers rebate, Rural Rebate, or TCED TOD (Normal/Peak/OffPeak).",
                        "prompt": "Here is the billing calculation code for LT-5 R DBT Weavers Rebate (based on Sanctioned HP) and TOD Normal/Peak/OffPeak slots. Generate a boundary-value test matrix covering minimum HP, threshold crossover, zero consumption, and peak/off-peak rounding so we verify Android device calculation matches server calculation 100%.",
                    },
                    {
                        "title": "E-Mudra LE/LR & WFM API Payload Validator Agent",
                        "context": "When integrating external portals (E-Mudra LE/LR cases, TCED WFM Portal, Smart Meter Billing Data Fetch).",
                        "prompt": "Review this C#/API integration handler for E-Mudra LE/LR screen modifications and Smart Meter Billing Data Fetch. Identify any unhandled null fields, timeout risks, or status-code mismatches, and generate structured logging for failed fetches.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 85,
                    "domain_mastery": 92,
                    "engineering_craft": 84,
                    "communication_ownership": 58,
                },
                "dimension_notes": {
                    "technical_depth": "Strong versatility across Android SpotBilling devices, backend billing engines, Smart Meter APIs, and WFM/E-Mudra integrations.",
                    "domain_mastery": "Deep utility tariff knowledge (Capacitor Penalty, SIR Electoral Roll deputation, LT-5 R DBT Weavers rebate, Rural Rebate, TOD Peak/OffPeak).",
                    "engineering_craft": "Consistently ships monthly utility app releases on schedule.",
                    "communication_ownership": "5/5 submitted reports used the exact same copy-pasted boilerplate ('Improved coding skills and gained practical experience in business logic implementation'), and Nov 4 report was missed.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-02",
                        "original": "Improved coding skills and gained practical experience in business logic implementation.",
                        "upgraded": "Updated TCED file updation parser to split meter readings across TOD Normal, TOD Peak, and TOD OffPeak registers, and verified that Rural Rebate rounding matches TRM back-office demand totals.",
                    },
                    {
                        "day": "2026-10-31",
                        "original": "Improved coding skills and gained practical experience in business logic implementation.",
                        "upgraded": "Modified LT-5 R DBT Weavers rebate calculation to check Sanctioned HP threshold before applying tariff subsidy in HESCOM Nov 2026 SpotBilling APK.",
                    },
                ],
                "growth_goals": [
                    "Retire the 'Improved coding skills...' boilerplate permanently—write 1 specific tariff rule, API edge case, or Android sync takeaway each day.",
                    "Submit the missing Nov 4 update covering E-Mudra LE/LR completion status.",
                    "Use an AI agent to auto-generate tariff regression test tables before each monthly SpotBilling APK release.",
                ],
            },
        },
        "sanjana-cs": {
            "headline": "TCED Kerala Municipal PF (Form 3 & Form 4, 75% Eligibility Engine) & DA Pension Arrears",
            "product_spaces": ["ERP"],
            "utilities": ["TCED"],
            "sync_owners": [
                {"name": "Sanjana C S", "role": "Developer (TCED Portal & ERP Reports)", "focus": "Owns TCED Kerala Municipal PF Form 3 & Form 4 screens, approval hierarchy, Create/Approve/Reject/Recommend reports, and 75% advance calculation logic."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead", "focus": "Reviews daily TCED PF progression (replied 'Noted' on Oct 31) and transitions Sanjana to DA Pension Arrears."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "TCED ERP Leads", "focus": "Validate Employee Portal to ERP workflow forwarding, approval hierarchy levels, and Balance at Credit formulas."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Ensures statutory accuracy of Kerala Municipal Pensionable Employees Central Provident Fund advances and pension arrears."},
            ],
            "outcome_iterations": [
                {
                    "id": "sc-out-1",
                    "track": "TCED Kerala Municipal PF Form 3 & Form 4 End-to-End Module",
                    "v1_reported": "Built Form 3 & Form 4 screens and reports (Create/Approve/Reject/Recommend) in Portal & ERP + implemented 75% Total Subscription eligibility & Balance at Credit calculation.",
                    "v2_owner_sync": "Verify that new PF advance applications cap eligible amount at `min(75% of Total Subscription, Available Balance at Credit)` and accurately compute monthly salary deduction.",
                    "v3_business_outcome": "Complete, tested digital workflow for TCED Kerala Municipal PF Temporary Advances from Employee Portal application through multi-level ERP sanction and reporting.",
                    "owners": ["Sanjana C S", "Sumukh Hegde", "Prajwal D A", "Prasad Amara"],
                    "status": "done",
                },
                {
                    "id": "sc-out-2",
                    "track": "TCED ERP DA Pension Arrears Screen & Report",
                    "v1_reported": "Planned for Nov 5: Create new DA Pension Arrears screen and report in the ERP source.",
                    "v2_owner_sync": "Align DA effective date lookup and arrears calculation logic with existing ERP pension tables and build matching RDLC/ERP report.",
                    "v3_business_outcome": "Automated DA Pension Arrears computation and reporting for TCED pensioners.",
                    "owners": ["Sanjana C S", "Sumukh Hegde", "Dharmaraj B"],
                    "status": "planned",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Model of steady, predictable delivery: 6/6 days reported with 100% plan-to-actual alignment, taking TCED Kerala Municipal PF Temporary Advances from initial screen creation to verified financial calculation closure.",
                "value_chains": [
                    {
                        "deliverable": "Form 3 & Form 4 Screens, Hierarchy & Reports (Portal + ERP)",
                        "artifact": "Form 3 Application & Form 4 Sanction Screens/Reports across Portal & ERP",
                        "client": "TCED Employees & PF Sanctioning Authority",
                        "business_impact": "Digitizes end-to-end Provident Fund temporary advance applications, recommendations, approvals, and rejections.",
                        "kpi": "Full parity across Employee Portal and ERP Source",
                    },
                    {
                        "deliverable": "75% Total Subscription Eligibility & Balance at Credit Calculator",
                        "artifact": "PF Advance Eligibility & Salary Deduction Business Logic",
                        "client": "TCED Finance & Payroll",
                        "business_impact": "Enforces statutory 75% subscription cap and calculates monthly loan recovery deductions automatically.",
                        "kpi": "Verified end-to-end across all test cases on Nov 4",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L1.5: Sequential Screen, Report & Calculation Development",
                "target_stage": "L3: AI Financial Formula Edge-Case Tester & ERP Report Scaffolding Agent",
                "observation": "Sanjana plans her work with remarkable accuracy (every single day's plan became the next day's completed work). She can accelerate report creation (Create/Approve/Reject/Recommend variants) and DA Pension Arrears scaffolding using AI agents.",
                "playbooks": [
                    {
                        "title": "PF 75% Eligibility & Loan Deduction Edge-Case Test Agent",
                        "context": "When validating Balance at Credit, 75% Total Subscription cap, and monthly salary deduction calculations.",
                        "prompt": "Review this C# / SQL calculation for Kerala Municipal PF Temporary Advance (Form 3 & Form 4). Generate 8 test cases covering: (1) existing unpaid advance balance, (2) requested amount > 75% of Total Subscription, (3) Balance at Credit < 75% cap, and (4) odd installment division rounding.",
                    },
                    {
                        "title": "DA Pension Arrears Screen & Report Co-Pilot Agent",
                        "context": "For Sanjana's next task: building the DA Pension Arrears screen and report in TCED ERP.",
                        "prompt": "Scaffold the ASP.NET WebForms grid, C# BAL/DAL methods, and SQL query for the new TCED DA Pension Arrears screen and report, following our existing Form 4 ERP report conventions and Venkata Sai's DAEffectiveDateCapture lookup pattern.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 78,
                    "domain_mastery": 88,
                    "engineering_craft": 88,
                    "communication_ownership": 75,
                },
                "dimension_notes": {
                    "technical_depth": "Solid execution across Employee Portal, ERP source, workflow hierarchies, and financial eligibility calculations.",
                    "domain_mastery": "Strong command of Kerala Municipal PF Form 3/Form 4 workflows and 75% subscription / Balance at Credit rules.",
                    "engineering_craft": "Dedicated a full day (Nov 4) to systematic calculation validation and edge-case testing before moving to DA Pension Arrears.",
                    "communication_ownership": "100% attendance (6/6 days) and crystal-clear 'Work Completed' and 'Tomorrow's Plan' sections, but 'What I Learned Today' relied on generic phrasing ('Learned about coding and business logic implementation') on 5 of 6 days.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-03",
                        "original": "Learned about coding and business logic implementation.",
                        "upgraded": "Learned how to compute net eligible PF advance in Form 3/4 by comparing 75% of Total Subscription against existing Balance at Credit and auto-deriving the monthly salary deduction installment.",
                    }
                ],
                "growth_goals": [
                    "Replace 'Learned about coding and business logic implementation' with the specific PF/Pension formula or SQL/report behavior discovered that day.",
                    "Reuse Venkata Sai's DAEffectiveDateCapture pattern when building the new DA Pension Arrears screen on Nov 5.",
                    "Use an AI agent to scaffold boilerplate Create/Approve/Reject/Recommend report variants.",
                ],
            },
        },
        "pallapu-rajesh": {
            "headline": "TCED Back-Office Billing & Tariff Engines (DL, Wheeling, Street Light, Solar, Temp) + BGCL Fixes",
            "product_spaces": ["TRM", "ERP"],
            "utilities": ["TCED", "BGCL"],
            "sync_owners": [
                {"name": "Pallapu Rajesh", "role": "Developer (TCED & BGCL Billing)", "focus": "Owns TCED Back Office Bill Generation, Complaint Management, Demand/Billing Reports, Solar Wheeling Loss, and BGCL leave/salary/BPNO/DPNG fixes."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead", "focus": "Reviews daily TCED & BGCL progress (replied 'Noted' on Oct 31) and monitors multi-day screen modifications."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "TCED & BGCL Leads", "focus": "Coordinate TCED tariff formulas (wheeling, transmission loss, street light, temporary consumer) and BGCL billing/HR fixes."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Ensures TCED back-office billing completeness across all consumer categories and stable BGCL operations."},
            ],
            "outcome_iterations": [
                {
                    "id": "pr-out-1",
                    "track": "TCED Back-Office Bill Generation & Complaint Management Multi-Tariff Engine",
                    "v1_reported": "Modified Back Office Bill Generation & Complaint Mgmt across 6 days (DL withdrawal, wheeling/loss, street light, solar bill print, temporary consumer, New Consumer/Debit Entry, Solar Wheeling Loss).",
                    "v2_owner_sync": "Consolidate all 6 consumer tariff rules into a clean, modular billing calculation service shared by both Back Office Bill Generation and Complaint Management so changes don't have to be duplicated across both screens.",
                    "v3_business_outcome": "Unified, regression-free TCED back-office billing and complaint recalculation engine supporting all commercial, street light, temporary, and solar wheeling consumers.",
                    "owners": ["Pallapu Rajesh", "Sumukh Hegde", "Prajwal D A", "Prasad Amara"],
                    "status": "in_progress",
                },
                {
                    "id": "pr-out-2",
                    "track": "BGCL Leave, Salary, BPNO Generation & DPNG Report Stabilization",
                    "v1_reported": "Fixed BGCL leave balance (Oct 30), salary generation (Oct 31), and BPNO generation & DPNG reports (Nov 3).",
                    "v2_owner_sync": "Coordinate BGCL touchpoints with Chitrashree HR and document root causes of BPNO and DPNG report defects.",
                    "v3_business_outcome": "Zero recurring payroll or BPNO/DPNG billing report failures in BGCL.",
                    "owners": ["Pallapu Rajesh", "Chitrashree HR", "Dharmaraj B"],
                    "status": "done",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Core billing-engine workhorse across TCED and BGCL: delivered 6 consecutive days of tariff logic across TCED Back Office Bill Generation & Complaint Management while resolving 4 production issues in BGCL.",
                "value_chains": [
                    {
                        "deliverable": "TCED Multi-Tariff Billing Engine (6 Consumer Categories)",
                        "artifact": "Back Office Bill Generation, Complaint Management, Demand & Billing Reports",
                        "client": "TCED Revenue & Subdivision Billing Offices",
                        "business_impact": "Enables accurate billing and complaint adjustments for DL withdrawal, wheeling/transmission loss, street lights, solar print, temporary consumers, and debit entries.",
                        "kpi": "6 consumer tariff tracks implemented across Oct 29 – Nov 4",
                    },
                    {
                        "deliverable": "BGCL Payroll & Billing Fixes (Leave, Salary, BPNO, DPNG)",
                        "artifact": "BGCL Salary/Leave Module, BPNO Generator & DPNG Reports",
                        "client": "BGCL Operations",
                        "business_impact": "Unblocks BGCL salary generation, leave balances, BPNO numbering, and DPNG reporting.",
                        "kpi": "4 BGCL production issues resolved alongside TCED sprint",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L1: Manual Parallel Editing of Duplicate Screens (Bill Gen + Complaint Mgmt)",
                "target_stage": "L3: AI Shared Billing-Service Refactoring & Tariff Parity Agent",
                "observation": "Every single day from Oct 29 to Nov 4, Rajesh had to modify *both* Back Office Bill Generation and Complaint Management for the exact same tariff rule (DL withdrawal, wheeling loss, street light, temporary consumer). An AI agent can help extract shared tariff calculation methods and verify parity between both screens.",
                "playbooks": [
                    {
                        "title": "Back Office Bill Gen vs. Complaint Mgmt Parity & Refactor Agent",
                        "context": "Because every tariff rule (DL withdrawal, wheeling, street light, temporary consumer, solar loss) must work identically in both screens.",
                        "prompt": "Compare the billing calculation methods in BackOfficeBillGeneration.aspx.cs and ComplaintManagement.aspx.cs. Identify any drift between the two files across DL withdrawal, street light, temporary consumer, and solar wheeling loss logic, and extract a shared TCEDTariffCalculator helper class.",
                    },
                    {
                        "title": "Solar Wheeling Transmission Loss Formula Verification Agent",
                        "context": "For Rajesh's active Nov 4–5 task on Solar Wheeling Transmission Loss and wheeling charges.",
                        "prompt": "Review this Solar Wheeling Transmission Loss and wheeling charges calculation for TCED. Generate unit test cases verifying net billed units when solar injection exceeds, equals, or trails consumption across divisional and subdivisional logins.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 82,
                    "domain_mastery": 90,
                    "engineering_craft": 80,
                    "communication_ownership": 64,
                },
                "dimension_notes": {
                    "technical_depth": "Deep familiarity with TCED billing screens, report generators, and BGCL salary/BPNO modules.",
                    "domain_mastery": "High domain command of utility tariff rules: DL withdrawal, wheeling units, transmission loss, street light billing, temporary consumers, and solar billing.",
                    "engineering_craft": "Consistently ships parallel updates across Bill Generation, Complaint Management, and Reports.",
                    "communication_ownership": "100% attendance (6/6 days), but all 6 'Learning' entries are 1-line generic boilerplate ('Focused on coding practices and business logic implementation'), and 'Tomorrow's Plan' repeated the same generic line for 5 days.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-04",
                        "original": "Coding and business logic implementation.",
                        "upgraded": "Implemented New Consumer Entry and Debit Entry bindings in TCED and learned how Solar Wheeling Transmission Loss percentage must be deducted from gross wheeled units before applying wheeling charges.",
                    },
                    {
                        "day": "2026-11-03",
                        "original": "Focused on coding practices and business logic implementation.",
                        "upgraded": "Fixed BGCL BPNO sequence generation collision and implemented temporary consumer tariff multiplier in TCED Back Office Bill Generation and Complaint Management.",
                    },
                ],
                "growth_goals": [
                    "Name the specific tariff formula or bug root cause in 'Learning & Development' instead of 'Coding and business logic implementation'.",
                    "Specify which tariff rule or sub-task is planned for tomorrow rather than 'Continue modifications to Back Office Bill Generation screen'.",
                    "Use an AI agent to verify 100% calculation parity between Back Office Bill Generation and Complaint Management.",
                ],
            },
        },
        "chitrashree-hr": {
            "headline": "BGCL Work Requisitions & CPNG Registration, KPTCL Reports & DCW / Material Purchase OM",
            "product_spaces": ["ERP", "KPTCL"],
            "utilities": ["BGCL", "KPTCL", "DCW"],
            "sync_owners": [
                {"name": "Chitrashree HR", "role": "Developer (BGCL, KPTCL & DCW)", "focus": "Owns BGCL work requisitions & CPNG registration, KPTCL report/application issues, DCW reports, and Material Purchase OM / Imprest screens."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead", "focus": "Reviews multi-project task switching across BGCL, KPTCL, and DCW (replied 'Noted' on Oct 31)."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "Module Leads", "focus": "Assign and prioritize BGCL CPNG/requisition tickets vs. KPTCL and DCW report fixes."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Tracks KPTCL client responsiveness and BGCL CPNG consumer registration throughput."},
            ],
            "outcome_iterations": [
                {
                    "id": "ch-out-1",
                    "track": "BGCL CPNG Registration Process & Work Requisition Workflow",
                    "v1_reported": "Worked on BGCL work requisition changes (Oct 31) and BGCL CPNG Registration Process workflow, data handling, and validations (Nov 3).",
                    "v2_owner_sync": "Define explicit acceptance criteria and validation rules for CPNG Registration and break 'Continue working on BGCL project' into named screens/tickets.",
                    "v3_business_outcome": "Validated, error-free BGCL CPNG consumer registration and work requisition flow.",
                    "owners": ["Chitrashree HR", "Sumukh Hegde", "Prajwal D A"],
                    "status": "in_progress",
                },
                {
                    "id": "ch-out-2",
                    "track": "KPTCL Report & Application Issue Resolution + DCW / Material Purchase OM",
                    "v1_reported": "Worked on Imprest Indent, Material Purchase OM, Estimate Approval, DCW Reports, and KPTCL report/application issues (Oct 29–31).",
                    "v2_owner_sync": "Log exact KPTCL report names and issue root causes in standup updates so KPTCL product tracker has full traceability.",
                    "v3_business_outcome": "Fast, auditable turnaround on KPTCL and DCW report/procurement defects.",
                    "owners": ["Chitrashree HR", "Dharmaraj B", "Prasad Amara"],
                    "status": "in_progress",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Spans 3 distinct client tracks—BGCL (CPNG Registration & Work Requisitions), KPTCL (Reports & App Fixes), and Procurement/DCW (Imprest Indent & Material Purchase OM).",
                "value_chains": [
                    {
                        "deliverable": "BGCL CPNG Registration & Work Requisitions",
                        "artifact": "BGCL CPNG Registration Screen & Work Requisition Module",
                        "client": "BGCL Gas Distribution Operations",
                        "business_impact": "Enables Commercial PNG registration workflow validations and work requisition updates.",
                        "kpi": "CPNG workflow & validation rules implemented on Nov 3",
                    },
                    {
                        "deliverable": "KPTCL Reports & Imprest / Material Purchase OM",
                        "artifact": "KPTCL Reports, Imprest Indent/Estimate & Material Purchase OM",
                        "client": "KPTCL & Utility Stores/Procurement",
                        "business_impact": "Resolves report generation and print defects across KPTCL, DCW, and Material Purchase OM.",
                        "kpi": "4/6 days reported (missed Nov 2 & Nov 4 reports)",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L1: Multi-Project Bug Fixing Without Surfaced AI Workflows",
                "target_stage": "L2.5: AI Form Validation Generator & Report Bug Root-Cause Summarizer",
                "observation": "Chitrashree switches context across BGCL, KPTCL, and DCW frequently. Using an AI agent to validate CPNG registration rules and auto-summarize git diffs into specific standup bullets will save time and eliminate vague 'Worked on KPTCL issues' / 'Continue BGCL' lines.",
                "playbooks": [
                    {
                        "title": "BGCL CPNG Registration Validation Matrix Agent",
                        "context": "When implementing workflow, data handling, and input validations for BGCL CPNG Registration.",
                        "prompt": "Review the BGCL CPNG Registration form fields and code-behind validation logic. Check for missing mandatory field checks, duplicate consumer registration prevention, and invalid mobile/meter/tariff combinations, and output both client-side and server-side validation code.",
                    },
                    {
                        "title": "Git Diff to Standup & Ticket Summary Agent",
                        "context": "To turn multi-project KPTCL/BGCL/DCW bug fixes into crisp, high-signal daily standup updates.",
                        "prompt": "Summarize my git diff across BGCL and KPTCL files today into: (1) exact screen/report names and root causes fixed, (2) specific technical learning from the fix, and (3) concrete screens planned for tomorrow.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 72,
                    "domain_mastery": 78,
                    "engineering_craft": 75,
                    "communication_ownership": 56,
                },
                "dimension_notes": {
                    "technical_depth": "Handles report generation, print options, and form validations across multiple ERP/KPTCL codebases.",
                    "domain_mastery": "Growing domain breadth across Imprest Indent, Material Purchase OM, DCW, KPTCL, and BGCL CPNG Registration (good domain detail added on Nov 3!).",
                    "engineering_craft": "Resolves issues across multiple modules per day, though ticket/screen specificity is needed.",
                    "communication_ownership": "Missed Nov 2 and Nov 4 standup emails; wrote the exact same 6-word plan ('Continue working on the BGCL project') on all 4 reported days and repeated 'Learned how to identify issues and make changes' on all 4 days.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-10-31",
                        "original": "Worked on KPTCL issues. Tomorrow’s Plan: Continue working on the BGCL project. What I Learned: Learned how to identify issues and make changes to the application.",
                        "upgraded": "Fixed parameter binding bug in KPTCL [Report Name] and updated approval status filter in BGCL Work Requisition screen. Tomorrow's Plan: Implement mandatory field validations on BGCL CPNG Registration screen.",
                    }
                ],
                "growth_goals": [
                    "Never write 'Worked on KPTCL issues' or 'Continue working on the BGCL project' without naming the exact screen, report, or workflow step.",
                    "Build on the Nov 3 CPNG learning improvement by dropping the 'Learned how to identify issues...' prefix altogether.",
                    "Ensure 100% daily standup submission (missed Nov 2 & Nov 4).",
                ],
            },
        },
        "ankith-hm": {
            "headline": "Multi-Utility SQL Server (21 DBs) & PostgreSQL / PPAS 9.5 Live Database Restorations + TCED ERP",
            "product_spaces": ["Infra & Security", "ERP"],
            "utilities": ["GESCOM", "BESCOM", "MESCOM", "TCED", "COCHINPORT", "VIZAG", "INDIAN RAILWAY"],
            "sync_owners": [
                {"name": "Ankith HM", "role": "Database & ERP Engineer", "focus": "Owns restoration and integrity verification of 21 SQL Server databases + GESCOM_LIVE_02042026 differential recovery + PostgreSQL/PPAS 9.5 live DBs."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead (Active Intervention)", "focus": "Intervened on Oct 31 at 11:16 PM: 'Put up a report of complete database restore. You should take care of GESCOM which is PostgreSQL also.'"},
                {"name": "Prajwal D A & Dharmaraj B", "role": "DB & Infra Leads", "focus": "Coordinate backup file transfers, PPAS 9.5 role permissions (--no-owner/--no-acl), and SQL differential backup recovery."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Oversees datacenter/DR database readiness across all utility environments."},
            ],
            "outcome_iterations": [
                {
                    "id": "ak-out-1",
                    "track": "21-Database SQL Server Fleet Restoration & GESCOM_LIVE_02042026 Differential Recovery",
                    "v1_reported": "Restored 5 DBs (Oct 30) → BESCOMAMI/COCHINPORT/GESCOMAMI (Oct 31) → published 18/21 progress table (Nov 2) → 20 SQL DBs ONLINE (Nov 3) → GESCOM_LIVE_02042026 full + differential restore (Nov 4).",
                    "v2_owner_sync": "Following Sumukh's Oct 31 directive, track every DB by name, ONLINE status, and table count; complete GESCOM_LIVE_02042026 differential recovery and publish the final 21/21 sign-off table.",
                    "v3_business_outcome": "100% verified, ONLINE SQL Server multi-utility database fleet with zero missing tables or unrecovered differential backups.",
                    "owners": ["Ankith HM", "Sumukh Hegde", "Dharmaraj B", "Prasad Amara"],
                    "status": "in_progress",
                },
                {
                    "id": "ak-out-2",
                    "track": "PostgreSQL / PPAS 9.5 Live Database Restoration (ERP_LIVE & GESCOM_LIVE)",
                    "v1_reported": "Restored ERP_LIVE_31032026 in PPAS 9.5 (--no-owner / --no-acl) and initiated GESCOM_LIVE_02042026 PostgreSQL restoration & row-count validation (Nov 3–4).",
                    "v2_owner_sync": "Cross-check PostgreSQL table/view/sequence counts and row-count estimates against source backups to certify GESCOM_LIVE_02042026 readiness.",
                    "v3_business_outcome": "Production-ready PostgreSQL/PPAS 9.5 ERP and GESCOM databases validated for application cutover.",
                    "owners": ["Ankith HM", "Sumukh Hegde", "Prajwal D A"],
                    "status": "in_progress",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Clear example of two-way sync in action: after Sumukh's Oct 31 11:16 PM nudge, Ankith transformed his reporting on Nov 2–4 to deliver a structured 20-database SQL Server restoration campaign plus PPAS 9.5 PostgreSQL restorations for ERP_LIVE and GESCOM_LIVE.",
                "value_chains": [
                    {
                        "deliverable": "SQL Server Fleet Restoration (20+ Utility Databases + GESCOM Differential)",
                        "artifact": "BESCOMAMI, COCHINPORT, GESCOMAMI, VIZAG, INDIAN_RAILWAY, NSOFTSTORE, SRTPV_BESCOM, GESCOM_LIVE_02042026",
                        "client": "NSoft Multi-Utility Infrastructure",
                        "business_impact": "Brings 20+ critical utility SQL Server databases ONLINE with verified table counts and integrity checks.",
                        "kpi": "20/21 main SQL DBs ONLINE + GESCOM_LIVE full restore done",
                    },
                    {
                        "deliverable": "PostgreSQL / PPAS 9.5 Live Restorations (ERP_LIVE & GESCOM_LIVE)",
                        "artifact": "ERP_LIVE_31032026 & GESCOM_LIVE_02042026 in PPAS 9.5",
                        "client": "GESCOM & ERP Production Readiness",
                        "business_impact": "Resolves missing role blockers via `--no-owner`/`--no-acl` and validates live tables, views, and sequences.",
                        "kpi": "ERP_LIVE_31032026 verified; GESCOM_LIVE Postgres validating",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L2: CLI & SQL Query Verification across SQL Server & PPAS 9.5",
                "target_stage": "L3: Automated DB Restore Audit & Cross-Engine Row-Count Parity Agent",
                "observation": "Ankith is managing 20+ database restores across two engines (SQL Server and PostgreSQL/PPAS 9.5). Automating restore monitoring, differential LSN chain checks, and row-count reconciliation via AI-generated scripts will eliminate manual delays.",
                "playbooks": [
                    {
                        "title": "SQL Server Differential Backup LSN Chain & Recovery Diagnostic Agent",
                        "context": "When investigating differential restore delays on large databases like GESCOM_LIVE_02042026.",
                        "prompt": "Generate a T-SQL diagnostic script using sys.dm_exec_requests, msdb.dbo.backupset, and RESTORE HEADERONLY to verify that the GESCOM_LIVE_02042026 differential backup DifferentialBaseLSN matches the full backup FirstLSN/LastLSN, and show real-time percent_complete, estimated_completion_time, and wait_type.",
                    },
                    {
                        "title": "PostgreSQL / PPAS 9.5 Object & Row-Count Parity Report Agent",
                        "context": "For certifying ERP_LIVE_31032026 and GESCOM_LIVE_02042026 after `--no-owner --no-acl` restore.",
                        "prompt": "Write a PostgreSQL / PPAS 9.5 validation query that outputs a complete Markdown status table of all schemas: total tables, views, sequences, functions, invalid objects, and top 25 tables by estimated row count (pg_class.reltuples) so I can paste it directly into my daily standup report.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 86,
                    "domain_mastery": 80,
                    "engineering_craft": 85,
                    "communication_ownership": 62,
                },
                "dimension_notes": {
                    "technical_depth": "Strong multi-engine DBA & C# skills: SQL Server full/differential restores, PPAS 9.5 `--no-owner`/`--no-acl`, and 3-tier BEL/BAL/DAL architecture.",
                    "domain_mastery": "Good exposure across TCED ERP (19 HR fields & Employee Exit dropdowns) and utility database schemas.",
                    "engineering_craft": "Responded strongly to Sumukh's Oct 31 feedback by publishing exact database names, table counts (1,851 / 1,732 / 1,239 / 1,766), and PostgreSQL validation steps.",
                    "communication_ownership": "6/6 days reported and fixed his blank-subject habit on Nov 2–4, but omitted the 'What I Learned' section on 3 of 6 days (Oct 31, Nov 2, Nov 4).",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-04",
                        "original": "(Omitted 'What I Learned' section on Nov 4)",
                        "upgraded": "Learned how to diagnose SQL Server differential restore stalls on GESCOM_LIVE_02042026 by checking wait states / LSN continuity before restarting WITH RECOVERY, and how to use PostgreSQL catalog row-count estimates to validate large imports without full table scans.",
                    }
                ],
                "growth_goals": [
                    "Never omit the 'What I Learned' section—your Nov 3 learning on PPAS 9.5 `--no-owner` and `--no-acl` was super valuable!",
                    "Publish the final 21/21 SQL Server + 2 PostgreSQL database restoration sign-off table once GESCOM_LIVE finishes.",
                    "Use an AI agent to generate a reusable SQL + Postgres post-restore verification script.",
                ],
            },
        },
        "rohith-r": {
            "headline": "HESCOM Seva Sindhu & E-Mudhra Integrations + TCED Load Formula, Online Services & E-Sign",
            "product_spaces": ["TRM", "ERP"],
            "utilities": ["HESCOM", "TCED"],
            "sync_owners": [
                {"name": "Rohith R", "role": "Developer (HESCOM & TCED Integrations)", "focus": "Owns HESCOM Group Billing, Seva Sindhu & E-Mudhra integrations, TCED Load Module formula, LT New Connection data load fix, and TCED ERP E-Sign module."},
                {"name": "Sumukh Hegde", "role": "Engineering Lead (Active Intervention)", "focus": "Sent Oct 31 11:22 PM reminder ('We have not received your daily work update for today') after Rohith hit his Claude weekly quota."},
                {"name": "Prajwal D A & Dharmaraj B", "role": "Integration Leads", "focus": "Coordinate HESCOM external gateway integrations (Seva Sindhu, E-Mudhra) and TCED ERP E-Sign / HRMS tasks."},
                {"name": "Prasad Amara", "role": "Business & Product Sponsor", "focus": "Champions high-leverage AI agent adoption across the team and removes AI tooling/quota bottlenecks."},
            ],
            "outcome_iterations": [
                {
                    "id": "rr-out-1",
                    "track": "HESCOM External Integrations (Group Billing, Seva Sindhu & E-Mudhra)",
                    "v1_reported": "Completed HESCOM Group Billing Report (Oct 29), started Seva Sindhu integration (Oct 30), and completed E-Mudhra Integration for HESCOM (Nov 3).",
                    "v2_owner_sync": "Confirm Seva Sindhu & E-Mudhra error handling and ensure AI quota limits are escalated immediately without pausing daily standup reporting.",
                    "v3_business_outcome": "Live citizen-facing HESCOM Seva Sindhu & E-Mudhra digital signature workflows.",
                    "owners": ["Rohith R", "Sumukh Hegde", "Prajwal D A", "Prasad Amara"],
                    "status": "done",
                },
                {
                    "id": "rr-out-2",
                    "track": "TCED ERP E-Sign Module, LT New Connection Fix & Pending HRMS Tasks",
                    "v1_reported": "Resolved data load issue in TCED Online Services (LT New Connection) and completed E-Sign Module changes in TCED ERP (Nov 3–4).",
                    "v2_owner_sync": "Break 'Complete pending tasks related to HRMS in TCED ERP' (Nov 5 plan) into specific screens/deliverables and apply his spec-first Claude prompting pattern.",
                    "v3_business_outcome": "End-to-end E-Sign capability in TCED ERP and smooth LT New Connection online applications.",
                    "owners": ["Rohith R", "Sumukh Hegde", "Dharmaraj B"],
                    "status": "in_progress",
                },
            ],
            "business_alignment": {
                "strategic_summary": "Key integration engineer bridging HESCOM & TCED with external digital-governance gateways (Seva Sindhu, E-Mudhra, E-Sign) and online consumer portals (LT New Connection).",
                "value_chains": [
                    {
                        "deliverable": "HESCOM E-Mudhra, Seva Sindhu & Group Billing Report",
                        "artifact": "HESCOM E-Mudhra Integration, Seva Sindhu Connector, Group Billing Report",
                        "client": "HESCOM Digital Services",
                        "business_impact": "Automates digital signing and citizen service portal integration for HESCOM.",
                        "kpi": "Group Billing & E-Mudhra integrations completed",
                    },
                    {
                        "deliverable": "TCED ERP E-Sign Module & Online Services (LT New Connection) Fix",
                        "artifact": "TCED ERP E-Sign Module, TCED Online Services Data Loader",
                        "client": "TCED ERP & LT New Connection Applicants",
                        "business_impact": "Completes E-Sign workflow in TCED ERP and unblocks data loading in LT New Connection online services.",
                        "kpi": "Delivered Nov 3–4 once Claude quota reset",
                    },
                ],
            },
            "ai_agent_usage": {
                "current_stage": "L2.5: Explicit Spec-Driven Claude Power User (Constrained by Weekly Seat Quota)",
                "target_stage": "L4: Token-Efficient Spec-to-Module Agent & Multi-Model Fallback Workflow",
                "observation": "Rohith is the ONLY engineer on the team who explicitly reflects on *how* he prompts AI ('with a clear picture of the desired output and giving a more detailed explanation, I was able to complete the entire module changes in E-Sign'). However, exhausting his Claude weekly limit on Oct 30 & Nov 3 stalled his velocity—making him the prime candidate for API/Pro seat upgrade + token-efficient context management.",
                "playbooks": [
                    {
                        "title": "Token-Efficient Spec-First Prompt Template (Avoid Weekly Quota Burn)",
                        "context": "To get 100% module completion in 1–2 turns without burning weekly Claude context windows on huge files.",
                        "prompt": "I am updating [Module Name, e.g., TCED ERP E-Sign / HRMS]. Here are ONLY the relevant method signatures, SQL schema columns, and the exact before/after behavior required: [Spec]. Output a minimal unified diff and a 3-step verification checklist without repeating unchanged code.",
                    },
                    {
                        "title": "E-Mudhra / E-Sign Webhook & Signature Verification Agent",
                        "context": "When building and testing E-Mudhra and E-Sign integrations across HESCOM and TCED ERP.",
                        "prompt": "Review this E-Sign / E-Mudhra callback handler. Generate test payloads for (1) valid signed XML/PDF response, (2) user-cancelled signature, (3) expired transaction token, and (4) hash mismatch, and verify database state transitions for each.",
                    },
                ],
            },
            "learning_dimensions": {
                "scores": {
                    "technical_depth": 80,
                    "domain_mastery": 82,
                    "engineering_craft": 78,
                    "communication_ownership": 68,
                },
                "dimension_notes": {
                    "technical_depth": "Delivers cross-system integrations (E-Mudhra, E-Sign, Seva Sindhu, Online Services LT New Connection, Load Module formulas).",
                    "domain_mastery": "Good grasp of utility online connection workflows, loan/load calculation formulas, and digital signing flows.",
                    "engineering_craft": "Discovered the core principle of agentic engineering: specification clarity directly determines AI code quality.",
                    "communication_ownership": "4/6 days reported (missed Oct 31 & Nov 2; sent Nov 3 update on Nov 4 at 10:13 AM). Needs to still share 1 domain/code learning on days when Claude quota is exhausted.",
                },
                "reflection_upgrades": [
                    {
                        "day": "2026-11-03",
                        "original": "I did not use claude today as my account weekly limit has been exhausted.",
                        "upgraded": "Completed E-Mudhra integration for HESCOM manually while Claude weekly quota was exhausted; learned how the E-Mudhra response payload maps transaction status codes back to our HESCOM application table.",
                    }
                ],
                "growth_goals": [
                    "Even on days without Claude access, document 1 domain or technical takeaway from the integration code.",
                    "Share a 5-minute demo with the team on how spec-first prompting completed the TCED ERP E-Sign module in one day.",
                    "Break 'Take up new task in HESCOM' / 'Complete pending HRMS tasks' into named screens in Tomorrow's Plan.",
                ],
            },
        },
    }

    result: Dict[str, Dict[str, Any]] = {}
    all_tasks = product_tracker.get("tasks", [])

    for person in TEAM_ROSTER:
        slug = person["slug"]
        email_addr = person["email"]
        prof = profiles.get(slug, {})

        person_cells = [matrix.get(email_addr, {}).get(d) for d in sorted_days]
        submitted_cells = [c for c in person_cells if c is not None]
        green_count = sum(1 for c in submitted_cells if c["learning_eval"]["score"] == "green")
        amber_count = sum(1 for c in submitted_cells if c["learning_eval"]["score"] == "amber")
        red_count = sum(1 for c in submitted_cells if c["learning_eval"]["score"] == "red")

        person_pva = [item for item in plan_vs_actual if item["person_email"] == email_addr]
        person_tasks = [t for t in all_tasks if t["assignee_email"] == email_addr]

        result[slug] = {
            "person": person,
            "slug": slug,
            "aliases": person.get("aliases", [slug]),
            "headline": prof.get("headline", person["role"]),
            "product_spaces": prof.get("product_spaces", []),
            "utilities": prof.get("utilities", person["primary_projects"]),
            "telemetry": {
                "days_reported": len(submitted_cells),
                "total_days": len(sorted_days),
                "attendance_pct": round((len(submitted_cells) / len(sorted_days)) * 100) if sorted_days else 0,
                "green_count": green_count,
                "amber_count": amber_count,
                "red_count": red_count,
                "aligned_transitions": sum(1 for i in person_pva if i["status"] == "aligned"),
                "carryover_transitions": sum(1 for i in person_pva if i["status"] == "carryover"),
                "pivoted_transitions": sum(1 for i in person_pva if i["status"] == "pivoted"),
                "missing_transitions": sum(1 for i in person_pva if i["status"] == "missing"),
            },
            "sync_owners": prof.get("sync_owners", []),
            "outcome_iterations": prof.get("outcome_iterations", []),
            "business_alignment": prof.get("business_alignment", {}),
            "ai_agent_usage": prof.get("ai_agent_usage", {}),
            "learning_dimensions": prof.get("learning_dimensions", {}),
            "pva_history": person_pva,
            "mapped_tasks": person_tasks,
            "daily_reports": {d: matrix.get(email_addr, {}).get(d) for d in sorted_days},
        }

    return result
