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
    1:  ("nb01_ai_arm_not_brain", "Studio 1: Frame the inquiry — from curiosity to a research problem"),
    2:  ("nb02_curiosity_to_problem", "Studio 2: Govern the work — your rules and your question"),
    3:  ("nb03_research_builds_on_research", "Studio 3: Ground it in verified evidence"),
    4:  ("nb04_anatomy_of_design", "Studio 4: Declare and diagnose provisionally"),
    5:  ("nb05_observational_descriptive", "Studio 5: Develop the pathway — the route hub"),
    6:  ("nb06_observational_causal", "Studio 6: Govern data and measurement"),
    7:  ("nb07_experimental_descriptive", "Studio 7: Produce a reproducible first analysis"),
    8:  ("nb08_prediction", "Studio 8: Stress-test and adjudicate"),
    9:  ("nb09_experimental_causal", "Studio 9: Write, bound, and disclose"),
    10: ("nb10_attack_the_analysis", "Studio 10: Adapt and defend — the venue contract and the artifact"),
    11: ("nb11_poster_production_review", "Poster production and peer review"),
    12: ("nb12_presentation_preparation", "Presentation preparation: the pitch, the hard questions, the invitation"),
    13: ("nb13_conference", "The public test: dress rehearsal and the Expo"),
    14: ("nb14_replication_redteam", "Async module: reflection on what the public test returned"),
    15: ("nb15_reproduce_and_package", "Studio 11: Reproduce and package"),
    16: ("nb16_release_next_cycle", "Studio 12: Release and direct the next cycle"),
}

REPO_SLUG = "davi-moreira/2026F_evidence_driven_research_purdue_HONR464"

# Milestone studio notebooks (msNN) — the light Friday-studio companions to the
# M1–M17 milestone briefs (ACTIVITY_TEMPLATE.md, "Milestone studio notebooks"
# final section). Keyed by milestone id. These carry the reduced required set,
# no schedule badge, and no per-lecture structure. Built ad hoc as each milestone
# package ships; not every id is present until P4 completes.
MS_NOTEBOOKS = {
    0:  ("ms00_research_ai_baseline", "M1 studio — curiosity committed and the research problem"),
    1:  ("ms01_research_opportunity_landscape", "M2 studio — your rules and your question"),
    2:  ("ms02_verified_evidence_map", "M3 studio — verified evidence and contribution map"),
    3:  ("ms03_research_charter_mida", "M4 studio — Research Contract v0 and permission determination"),
    4:  ("ms04_observational_descriptive_audit",
        "M5 studio — pathway declaration and mandated contrast"),
    5:  ("ms05_causal_identification", "M6 studio — data and measurement governance"),
    6:  ("ms06_experimental_measurement_protocol", "M7 studio — first reproducible analysis + conference application"),
    7:  ("ms07_declared_analysis_protocol", "M8 studio — robustness audit"),
    8:  ("ms08_minimum_viable_analysis", "M9 studio — bounded research note and claim-evidence table"),
    9:  ("ms09_poster_draft_research_audit", "M10 studio — venue contract and the publication-ready artifact"),
    10: ("ms10_final_poster_lock", "M13 studio — the final poster lock (terminal)"),
    11: ("ms11_presentation_package", "M14 studio — the go-public package"),
    12: ("ms12_conference_reflection", "M15 studio — conference reflection"),
    13: ("ms13_replication_redteam", "M16 support — the peer cold run"),
    14: ("ms14_research_note_capsule", "M16 studio — reproducible package and the peer cold run"),
    15: ("ms15_final_chapter_portfolio", "M17 studio — release, final chapter, and portfolio (terminal)"),
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
