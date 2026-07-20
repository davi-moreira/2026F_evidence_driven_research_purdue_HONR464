#!/usr/bin/env python3
"""build_session_guides.py — generate per-notebook session guides for the
instructor from planning/MEETING_SCHEDULE.csv.

One guide per topic notebook (session_guides/NN_session_guide.md, gitignored;
this generator is tracked so the guides are always reproducible). Each guide
covers every session its notebook absorbs (parsed from the schedule's
`other_material` column) and lays out, per session: the driving questions, the
claim boundary, a minute-by-minute run of show (parsed from `minute_dynamic`),
read-aloud openers, hands-on/practice moves, the milestone moment, instructor
prep, risks, and the exit ticket.

Sessions are labeled by kind (D13 — no dates, no meeting numbers anywhere):
"Lecture i of N" (Mon/Wed content), "Studio Friday" (recap + milestone kickoff
+ project work), or "Async module". Labels come from lecture_labels() in
notebooks_map.py; voice_check_guides.py fails any guide carrying a date.

Voice rule: read-aloud blockquotes must speak TO the class (voice_check_guides.py
audits every `> ` line). Any schedule text that mentions "students"/"the
instructor" is rendered as wrapper prose (instructor-facing), never blockquoted.

Usage: python3 scripts/build_session_guides.py   (then optionally
       python3 scripts/voice_check_guides.py session_guides/*.md)
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(REPO / "scripts"))
from notebooks_map import (NOTEBOOKS, student_filename, nb_of as nb_of_material,  # noqa: E402
                           session_kind, lecture_labels)

SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.csv"
OUT = REPO / "session_guides"

COLAB = ("https://colab.research.google.com/github/"
         "davi-moreira/2026F_evidence_driven_research_purdue_HONR464/"
         "blob/main/notebooks/student/{fname}")

# Same regexes as the voice checker — used to keep dirty lines OUT of blockquotes.
VOICE = [re.compile(r"\bstudents?\b", re.I), re.compile(r"\bthe instructor\b", re.I)]

COMPASS_CHEAT_SHEET = """\
## The compass, for the board (30-second redraw)

- **KIND** — descriptive (*what is / was?*) vs **causal** (*what would an
  intervention change?*) — RDSS ch. 7.
- **REACH** — the data at hand · a population beyond the data · cases not yet
  seen.
- **Positions:** Description (nb06) · Generalization (nb10) · Prediction (nb12)
  · Causal reasoning (nb13).
- **Crossings & licenses:** sample→population = sampling design + uncertainty
  (*silent upgrade* if unpaid) · observed→unseen = prediction-time honesty +
  held-out check (*leakage* if unpaid) · descriptive→causal = assignment /
  identification (*after-therefore-because* if unpaid).
- One-liner to repeat: **"You buy kind and reach with your data strategy, and
  you prove the purchase with diagnosis."**
"""


def clean(s: str) -> str:
    return (s or "").strip()


def voice_dirty(s: str) -> bool:
    return any(p.search(s) for p in VOICE)


def blockquote(s: str) -> str:
    """Blockquote a read-aloud line only if it passes the voice rule."""
    s = clean(s)
    if not s:
        return ""
    if voice_dirty(s):
        return f"*(instructor-facing — do not read verbatim)* {s}"
    return f'> *"{s}"*' if not s.startswith(">") else s


def run_of_show(minute_dynamic: str) -> list[str]:
    """Split the schedule's minute_dynamic into table rows."""
    segments = [seg.strip() for seg in minute_dynamic.split(";") if seg.strip()]
    rows = []
    for seg in segments:
        m = re.match(r"^(?:ASYNC[^:]*:\s*)?(\d+–\d+)\s*(.*)$", seg)
        if m:
            rows.append((m.group(1), m.group(2).strip(" .")))
        elif rows:  # continuation of the previous segment (no leading time range)
            t, prev = rows[-1]
            rows[-1] = (t, prev + " — " + seg.strip(" ."))
        else:
            rows.append(("", seg.strip(" .")))
    return rows


def nb_of(meeting: dict) -> int | None:
    return nb_of_material(meeting.get("other_material", ""))


def session_heading(m: dict, labels: dict[int, tuple[int, int, int]]) -> str:
    kind = session_kind(m)
    title = m["title"]
    for prefix in ("Studio Friday — ", "ASYNC — "):
        title = title.removeprefix(prefix)
    if kind == "async":
        return f"## Async module — {title}"
    if kind == "studio":
        return f"## Studio Friday — {title}"
    lab = labels.get(int(m["meeting"]))
    if lab:
        _nb, i, n = lab
        return f"## Lecture {i} of {n} — {title}"
    return f"## Lecture — {title}"


def meeting_section(m: dict, labels: dict[int, tuple[int, int, int]]) -> str:
    lines = []
    lines.append(session_heading(m, labels))
    lines.append("")
    lines.append(f"*{m['modality']} · {m['unit']}*")
    lines.append("")
    lines.append(f"**Driving question:** {m['driving_question']}")
    if clean(m.get("secondary_questions")):
        lines.append(f"**Also in play:** {m['secondary_questions']}")
    lines.append("")
    lines.append(f"**Compass focus:** {m['inquiry']}")
    lines.append("")
    lines.append("| Claim boundary | |")
    lines.append("|---|---|")
    lines.append(f"| Permitted | {m['claim_permitted']} |")
    lines.append(f"| Not permitted | {m['claim_not_permitted']} |")
    lines.append("")
    if clean(m.get("rdss_reading")):
        lines.append(f"**Reading due:** {m['rdss_reading']}")
    if clean(m.get("cb_reading")):
        lines.append(f"**Optional (CB):** {m['cb_reading']}")
    lines.append(f"**Materials:** {m['other_material']}")
    if clean(m.get("dataset_simulation")) and m["dataset_simulation"].lower() != "none":
        lines.append(f"**Data / simulation:** {m['dataset_simulation']}")
    if clean(m.get("python_r_dependency")) and m["python_r_dependency"].lower() != "none":
        lines.append(f"**Computing:** {m['python_r_dependency']}")
    lines.append("")
    lines.append("### Run of show (50 min)")
    lines.append("")
    lines.append("| Min | Segment |")
    lines.append("|---|---|")
    for t, seg in run_of_show(m["minute_dynamic"]):
        seg = seg.replace("|", "\\|")
        lines.append(f"| {t} | {seg} |")
    lines.append("")
    lines.append("### Read-alouds")
    lines.append("")
    lines.append("Discussion opener:")
    lines.append(blockquote(m["discussion_prompt"]))
    lines.append("")
    lines.append("Exit ticket, read at the close:")
    lines.append(blockquote(m["exit_ticket"]))
    lines.append("")
    lines.append("### Hands-on & practice")
    lines.append("")
    lines.append(f"- **Hands-on:** {m['hands_on_activity']}")
    lines.append(f"- **Practice:** {m['practice']}")
    lines.append("")
    lines.append("### Milestone moment")
    lines.append("")
    lines.append(f"- **Milestone:** {m['milestone_developed']}")
    if clean(m.get("milestone_work_time")):
        lines.append(f"- **In-class work time:** {m['milestone_work_time']}")
    if clean(m.get("milestone_presentation_review")) and \
            m["milestone_presentation_review"].lower() not in ("none", "none (kickoff)"):
        lines.append(f"- **Presentation/review:** {m['milestone_presentation_review']}")
    lines.append(f"- **Project connection:** {m['project_connection']}")
    lines.append("")
    lines.append("### Before class")
    lines.append("")
    lines.append(f"- **Instructor prep:** {m['instructor_prep']}")
    lines.append(f"- **What they were asked to bring/do:** {m['student_prep']}")
    lines.append("")
    lines.append("### Risks & contingencies")
    lines.append("")
    lines.append(f"- {m['risks_contingency']}")
    lines.append("")
    lines.append("### Leaving class")
    lines.append("")
    lines.append(f"- **Artifact produced:** {m['student_artifact']}")
    lines.append(f"- **Homework / next milestone:** {m['homework_next_milestone']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    with SCHEDULE.open() as f:
        meetings = list(csv.DictReader(f))

    by_nb: dict[int, list[dict]] = {}
    for m in meetings:
        n = nb_of(m)
        if n is not None:
            by_nb.setdefault(n, []).append(m)

    labels = lecture_labels(meetings)

    OUT.mkdir(exist_ok=True)
    for n, (slug, title) in sorted(NOTEBOOKS.items()):
        ms = by_nb.get(n, [])
        if not ms:
            continue
        kinds = [session_kind(m) for m in ms]
        parts = []
        if kinds.count("lecture"):
            c = kinds.count("lecture")
            parts.append(f"{c} lecture{'s' if c > 1 else ''}")
        if kinds.count("studio"):
            c = kinds.count("studio")
            parts.append(f"{c} studio Friday{'s' if c > 1 else ''}")
        if kinds.count("async"):
            parts.append("1 async module" if kinds.count("async") == 1
                         else f"{kinds.count('async')} async modules")
        fname = student_filename(n)
        head = [
            f"# Session Guide — nb{n:02d} · {title}",
            "",
            f"*(Generated by `scripts/build_session_guides.py` from "
            f"`planning/MEETING_SCHEDULE.csv` — edit the schedule data and "
            f"regenerate; do not hand-edit. Gitignored; instructor-only.)*",
            "",
            f"**Sessions:** {' + '.join(parts)}",
            f"**Student notebook:** `notebooks/student/{fname}` · "
            f"[open in Colab]({COLAB.format(fname=fname)})",
            f"**Compass focus across the span:** "
            f"{' · '.join(dict.fromkeys(m['inquiry'] for m in ms))}",
            f"**Milestone arc:** "
            f"{' → '.join(dict.fromkeys(m['milestone_developed'] for m in ms))}",
            "",
            COMPASS_CHEAT_SHEET,
            "---",
            "",
        ]
        body = "\n---\n\n".join(meeting_section(m, labels) for m in ms)
        out = OUT / f"{n:02d}_session_guide.md"
        out.write_text("\n".join(head) + body)
        print(f"✓ wrote {out.relative_to(REPO)} ({len(ms)} session(s))")

    print(f"✓ {len(by_nb)} guides generated")


if __name__ == "__main__":
    main()
