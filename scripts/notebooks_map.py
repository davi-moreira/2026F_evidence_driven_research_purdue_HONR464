"""notebooks_map.py — the single registry of the 16 weekly topic notebooks.

Slug + site title per notebook, plus the shared schedule-derived helpers
(`nb_of`, `session_kind`, `lecture_labels`) that the schedule generator, badge
updater, session-guide builder, and validators all use. Meeting spans and
milestones are derived from planning/MEETING_SCHEDULE.csv (the
`other_material` column carries the nbNN reference for every meeting); this
file fixes filenames, display titles, and the lecture-numbering convention
(D13: "Topic NN · Lecture i of N", derived mechanically, never hand-kept).
"""

import csv
import re
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_SCHEDULE_CSV = _REPO / "planning" / "MEETING_SCHEDULE.csv"

NB_RE = re.compile(r"nb(\d\d)")

# nb number -> (file slug, short site title). One notebook per WEEK (v2).
NOTEBOOKS = {
    0:  ("nb00_ai_arm_not_brain", "Research in the age of AI: your arm, your RA — not your brain"),
    1:  ("nb01_curiosity_to_problem", "From curiosity to a research problem: descriptive, predictive, causal"),
    2:  ("nb02_research_builds_on_research", "Research builds on research: verified evidence + real gaps"),
    3:  ("nb03_anatomy_of_design", "The anatomy of a research design: MIDA + declare → diagnose → redesign"),
    4:  ("nb04_observational_descriptive", "Observational descriptive research"),
    5:  ("nb05_observational_causal", "Observational causal research"),
    6:  ("nb06_experimental_descriptive", "Experimental descriptive research"),
    7:  ("nb07_prediction", "Prediction: generalizing to unseen cases"),
    8:  ("nb08_experimental_causal", "Experimental causal research"),
    9:  ("nb09_attack_the_analysis", "Share the research + attack the analysis"),
    10: ("nb10_poster_criticism_lock", "Poster criticism + final poster lock"),
    11: ("nb11_poster_delivery", "Poster delivery: pitches, uncertainty, difficult questions"),
    12: ("nb12_conference", "Final conference preparation, presentation + reflection"),
    13: ("nb13_replication_redteam", "Async module: replication + red-team of a peer's package"),
    14: ("nb14_poster_to_research_note", "From poster to research note"),
    15: ("nb15_managing_ai_agents", "Managing multiple AI agents + the final defense"),
}

REPO_SLUG = "davi-moreira/2026F_evidence_driven_research_purdue_HONR464"

# Milestone studio notebooks (msNN) — the light Friday-studio companions to the
# M0–M15 milestone briefs (ACTIVITY_TEMPLATE.md, "Milestone studio notebooks"
# final section). Keyed by milestone id. These carry the reduced required set,
# no schedule badge, and no per-lecture structure. Built ad hoc as each milestone
# package ships; not every id is present until P4 completes.
MS_NOTEBOOKS = {
    0:  ("ms00_research_ai_baseline", "M0 studio — research and AI baseline"),
    1:  ("ms01_research_opportunity_landscape", "M1 studio — research opportunity landscape"),
    2:  ("ms02_verified_evidence_map", "M2 studio — verified evidence and contribution map"),
    3:  ("ms03_research_charter_mida", "M3 studio — research charter and MIDA declaration"),
    4:  ("ms04_observational_descriptive_audit",
        "M4 studio — observational descriptive design audit"),
    5:  ("ms05_causal_identification", "M5 studio — causal identification or boundary (async)"),
    6:  ("ms06_experimental_measurement_protocol", "M6 studio — experimental measurement protocol + abstract gate"),
    7:  ("ms07_declared_analysis_protocol", "M7 studio — declared analysis protocol"),
    8:  ("ms08_minimum_viable_analysis", "M8 studio — minimum viable analysis"),
    9:  ("ms09_poster_draft_research_audit", "M9 studio — poster draft 1 and research audit"),
    10: ("ms10_final_poster_lock", "M10 studio — final poster lock (terminal)"),
    11: ("ms11_presentation_package", "M11 studio — presentation package + mock symposium"),
    12: ("ms12_conference_reflection", "M12 studio — conference reflection and criticism portfolio"),
    13: ("ms13_replication_redteam", "M13 module — replication and red-team (async)"),
    14: ("ms14_research_note_capsule", "M14 studio — research note and reproducibility capsule"),
    15: ("ms15_final_chapter_portfolio", "M15 studio — final chapter, portfolio + ceremony (terminal)"),
}


def student_filename(n: int) -> str:
    return f"{NOTEBOOKS[n][0]}_student.ipynb"


def instructor_filename(n: int) -> str:
    return f"{NOTEBOOKS[n][0]}_instructor.ipynb"


def ms_student_filename(n: int) -> str:
    return f"{MS_NOTEBOOKS[n][0]}_student.ipynb"


def ms_instructor_filename(n: int) -> str:
    return f"{MS_NOTEBOOKS[n][0]}_instructor.ipynb"


def colab_badge(n: int) -> str:
    url = (f"https://colab.research.google.com/github/{REPO_SLUG}/"
           f"blob/main/notebooks/student/{student_filename(n)}")
    return (f"[![Open In Colab](https://colab.research.google.com/assets/"
            f"colab-badge.svg)]({url}){{target=\"_blank\"}}")


# --- schedule-derived helpers (D13 lecture numbering) -----------------------

def nb_of(other_material: str) -> int | None:
    """First nbNN token in a schedule row's other_material = owning notebook."""
    m = NB_RE.search(other_material or "")
    return int(m.group(1)) if m else None


def session_kind(row: dict) -> str:
    """'async' | 'studio' | 'lecture' for a MEETING_SCHEDULE.csv row.

    Fridays are studios (recap + milestone kickoff + project work, no new
    content); async meetings are self-contained modules; Mon/Wed are lectures.
    """
    if row["modality"] == "async-online":
        return "async"
    if row["day"] == "Fri":
        return "studio"
    return "lecture"


def load_schedule_rows() -> list[dict]:
    with open(_SCHEDULE_CSV, newline="") as f:
        return list(csv.DictReader(f))


def lecture_labels(rows: list[dict] | None = None) -> dict[int, tuple[int, int, int]]:
    """meeting number -> (nb, i, N) over lecture-kind meetings.

    Grouped by notebook (not consecutive runs), so a topic's lectures number
    consecutively across intervening studio Fridays. Studio and async rows get
    no label — they borrow the topic's identity, not a lecture number.
    """
    rows = load_schedule_rows() if rows is None else rows
    per_nb: dict[int, list[int]] = {}
    for r in rows:
        if session_kind(r) != "lecture":
            continue
        n = nb_of(r["other_material"])
        if n is None:
            continue
        per_nb.setdefault(n, []).append(int(r["meeting"]))
    labels: dict[int, tuple[int, int, int]] = {}
    for n, ms in per_nb.items():
        for i, mtg in enumerate(sorted(ms), start=1):
            labels[mtg] = (n, i, len(ms))
    return labels


def lecture_count(n: int, rows: list[dict] | None = None) -> int:
    """Number of Mon/Wed lectures topic nb<n> spans (0 = async-only module)."""
    labels = lecture_labels(rows)
    return max((N for (nb, _i, N) in labels.values() if nb == n), default=0)
