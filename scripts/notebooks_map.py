"""notebooks_map.py — the single registry of the 20 topic notebooks.

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

# nb number -> (file slug, short site title)
NOTEBOOKS = {
    0:  ("nb00_launchpad", "Launchpad: How do we know? Colab + Ask → Verify → Document"),
    1:  ("nb01_curiosity_to_question", "Curiosity → gap → problem → answerable question"),
    2:  ("nb02_four_approaches", "The inquiry compass: classify the question by kind + reach"),
    3:  ("nb03_sources_claims", "Real sources, citation integrity, and the claim map"),
    4:  ("nb04_model_inquiry", "Model & Inquiry (MIDA I): worlds, potential outcomes, DAGs"),
    5:  ("nb05_measurement", "Measurement & operationalization: concept → construct → indicator"),
    6:  ("nb06_description", "Description deep dive: honest summaries & visualization"),
    7:  ("nb07_data_strategy", "Data strategy (MIDA II): sampling, assignment, ethics"),
    8:  ("nb08_async_claim_diagnosis", "Async module: diagnose a misleading claim (milestone work day)"),
    9:  ("nb09_answer_strategy", "Answer strategy (MIDA III): estimators & regression"),
    10: ("nb10_inference", "Generalization deep dive: uncertainty, reach, power"),
    11: ("nb11_declare_diagnose_redesign", "Declare → Diagnose → Redesign: the design engine"),
    12: ("nb12_prediction", "Prediction deep dive: target, baseline, split, metric, leakage"),
    13: ("nb13_causal", "Causal reasoning deep dive: counterfactuals & identification"),
    14: ("nb14_poster", "Poster: storyboard, red-team, final production"),
    15: ("nb15_communicating_evidence", "Communicating evidence: pitches, uncertainty, rehearsal"),
    16: ("nb16_debrief_redesign", "Conference debrief → feedback-to-redesign"),
    17: ("nb17_async_poster_to_dossier", "Async module: poster-to-dossier — sensitivity & claim ledger"),
    18: ("nb18_reproducibility_brief", "Reproducibility audit + research brief"),
    19: ("nb19_evidence_defense", "Evidence Defense + synthesis"),
}

REPO_SLUG = "davi-moreira/2026F_evidence_driven_research_purdue_HONR464"


def student_filename(n: int) -> str:
    return f"{NOTEBOOKS[n][0]}_student.ipynb"


def instructor_filename(n: int) -> str:
    return f"{NOTEBOOKS[n][0]}_instructor.ipynb"


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
