"""notebooks_map.py — the single registry of the 20 topic notebooks.

Slug + site title per notebook. Meeting spans and milestones are derived from
planning/MEETING_SCHEDULE.csv (the `other_material` column carries the nbNN
reference for every meeting); this file only fixes filenames and display titles
so the schedule generator, badge updater, and validators agree.
"""

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
    8:  ("nb08_async_claim_diagnosis", "Async: diagnose a misleading claim"),
    9:  ("nb09_answer_strategy", "Answer strategy (MIDA III): estimators & regression"),
    10: ("nb10_inference", "Generalization deep dive: uncertainty, reach, power"),
    11: ("nb11_declare_diagnose_redesign", "Declare → Diagnose → Redesign: the design engine"),
    12: ("nb12_prediction", "Prediction deep dive: target, baseline, split, metric, leakage"),
    13: ("nb13_causal", "Causal reasoning deep dive: counterfactuals & identification"),
    14: ("nb14_poster", "Poster: storyboard, red-team, final production"),
    15: ("nb15_communicating_evidence", "Communicating evidence: pitches, uncertainty, rehearsal"),
    16: ("nb16_debrief_redesign", "Conference debrief → feedback-to-redesign"),
    17: ("nb17_async_poster_to_dossier", "Async: poster-to-dossier — sensitivity & claim ledger"),
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
