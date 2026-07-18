# HONR 46400 Notebook Structure Template (canonical)

> **Canonical reference:** `notebooks/student/nb01_curiosity_to_question_student.ipynb`
> is the reference implementation once built. Every topic notebook
> (`notebooks/{instructor,student}/nbNN_topic_{instructor,student}.ipynb`) MUST
> follow this template. The MGMT474 ML-isms (RANDOM_SEED=474, 60/20/20 splits,
> ISLP, seaborn, Gemini-branding) are **gone by design** — do not reintroduce them.

Validated by `scripts/validate_notebooks.py`. One notebook per **topic**; each
absorbs all the MWF meetings its topic spans (see `planning/COURSE_MASTER_PLAN.md`
§5). Instructor-FIRST workflow: author `*_instructor.ipynb`, generate the student
file by stripping every cell whose source contains `INSTRUCTOR SOLUTION`
(`scripts/make_student.py`).

---

## Required cells, in order

### 1. Header (markdown)

```markdown
# [Topic Title — no "Day N", no dates]

<hr>

# <center><a class="tocSkip"></center>
# <center>HONR 46400 — Evidence-Driven Research</center>
# <center>Professor: Davi Moreira</center>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/student/nbNN_topic_student.ipynb)

---
```

### 2. Approach & Claim Boundary block (markdown) — REQUIRED, machine-checked

The course's operational spine. Every notebook states, up front, which of the
four approaches it emphasizes and the claim boundary it patrols:

```markdown
## 🧭 Approach & Claim Boundary

**Approach emphasis:** [description | statistical/observational inference |
predictive modeling | causal reasoning | all (framing/diagnosis/communication)]

| | |
|---|---|
| **A claim this topic PERMITS** | "[exact claim template]" |
| **A claim this topic does NOT permit** | "[exact overreach it forbids]" |

**Where this sits in the course:** [one sentence: which meetings, which milestone
it develops, what it builds on.]

*Provenance: [source-file or "fresh"] | [chapter/section] | [item] | [transformation]*
```

The provenance line follows `planning/SOURCE_AUDIT.md` §11 exactly. Never invent
chapters, declarations, functions, or datasets.

### 3. Learning objectives (markdown)

`By the end of this notebook, you will be able to:` + 4–6 numbered, verb-first
objectives. The last objective is ALWAYS a milestone/project transfer ("apply X
to your own project's …").

### 4. Setup (code) — deterministic, Colab-first, fallback-loading

```python
# Setup — run this cell first.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
pd.set_option("display.precision", 3)
plt.rcParams["figure.figsize"] = (9, 5)

SEED = 464  # course number — keeps every simulation reproducible
rng = np.random.default_rng(SEED)

# Data loads: GitHub raw URL first (works in Colab), local repo path as fallback.
DATA_URL = ("https://raw.githubusercontent.com/davi-moreira/"
            "2026F_evidence_driven_research_purdue_HONR464/main/notebooks/data/")

def load_course_data(filename):
    """Load a course dataset from GitHub, falling back to the local repo copy."""
    try:
        return pd.read_csv(DATA_URL + filename)
    except Exception:
        from pathlib import Path
        local = Path("notebooks/data") / filename
        if not local.exists():
            local = Path("../data") / filename
        return pd.read_csv(local)

print("✓ Setup complete — seed", SEED)
```

Rules: **no seaborn**; scipy/statsmodels/sklearn/networkx imported only in the
notebooks that use them; every stochastic cell uses `rng` (or a seeded
`train_test_split`); every data cell prints a `✓ Loaded …` confirmation with
shape so students can self-check.

### 5. Content sections (`## 1.`, `## 2.`, …) with the narrative pattern

- Open analytical sections with a **"Why This Matters"** cell voiced by a named
  research-world stakeholder (thesis advisor, journal reviewer, IRB reviewer,
  skeptical peer, policy stakeholder) whose concern is a direct quote.
- **Narrative prose over bullets** in "Reading the evidence" cells.
- Inline Q&A: `> **A question that often comes up here:** *"<q>"*` + one flowing
  paragraph.
- One-sentence **section bridges** at each transition.
- Markdown hygiene: escape `\$` and `\~`; emoji vocabulary ✓ ⚠️ 📝 💡 only.

### 6. The seven required active-learning moves (machine-checked)

Every ordinary notebook contains at least one of EACH, clearly marked with the
exact headings below (nb08/nb17, the async modules, additionally embed their
exit ticket inside the module flow):

| Move | Heading marker | What it is |
|---|---|---|
| Pre-run prediction | `### 🔮 Pause & Predict` | students commit a written prediction BEFORE running the next cell; the cell after reveals |
| Runnable activity | `### 🛠️ Run the Study` (or `### 🛠️ Hands-On:` variant) | students execute + modify real code on real data/simulation |
| Defended decision | `### ⚖️ Make a Design Choice` | students choose between stated options and write a one-paragraph defense |
| Practice item | `### 📝 Practice` | short transfer drill (sorting, matching, repairing, classifying) |
| Interpretation task | `### 🔍 Reading the Evidence` | students write what an output DOES and DOES NOT establish |
| Milestone transfer | `### 🎯 Project Transfer` | students apply the topic to their own project/milestone, in the notebook |
| Exit ticket | `### 🎟️ Claim Ticket` | the closing claim-boundary exit ticket (numbered #NN per meeting) |

Pacing rule (brief): direct exposition ≤8 min per segment, <15 min total per
meeting; ≥70% of class time active. Multi-meeting notebooks mark meeting
boundaries with a horizontal rule + `*(Meeting M# picks up here.)*`.

### 7. AI prompt + verification block (Ask → Verify → Document)

AI prompts are scripts the student copies into their AI tool — written exactly
as a student would type them (second person never breaks):

```markdown
> 💡 **AI Prompt (copy into your AI assistant):** "[prompt text]"
>
> **After running, verify (the responsible-AI habit):**
> - [ ] Every source the AI cited exists — you retrieved it yourself.
> - [ ] [task-specific fact-check]
> - [ ] Log this use in your AI ledger: tool, task, verification.
```

### 8. Instructor-solution cells (stripped from the student file)

1. `### INSTRUCTOR SOLUTION — Exercise N` (markdown heading)
2. `# INSTRUCTOR SOLUTION` first line of solution code cells
3. `<!-- INSTRUCTOR SOLUTION -->` first line of solution markdown cells

Student placeholders that REMAIN: `### YOUR ANSWER HERE:` (markdown) and
`# YOUR SOLUTION HERE` (code). Solutions are **model exemplars** (a well-scoped
question, a worked justification, a verified analysis) — concept-level quality,
not code golf. Instructor notebooks may also carry
`<!-- INSTRUCTOR SOLUTION -->`-prefixed facilitation notes (timing, common
stumbles) — same marker, same strip.

### 9. Wrap-up (markdown)

`## N. Wrap-Up` — key takeaways as short narrative (not a bare list), one
blockquoted critical rule, and a warm bridge naming the next notebook and the
milestone it serves.

### 10. Provenance & bibliography (markdown)

`## N+1. Sources & Provenance` — the notebook's full provenance lines (one per
borrowed element), the dataset attribution line (if data used):
*"Dataset from the `rdss` package (Blair, Coppock & Humphreys, MIT License),
companion to* Research Design in the Social Sciences *(2023)."*, and the reading
citations (RDSS chapters at book.declaredesign.org; optional CB cases at
callingbullshit.org). Only verified sources — `scripts/validate_coverage.py`
cross-checks chapters against the verified inventory.

### 11. Thank-you cell (markdown, final)

```markdown
<center>

Thank you!

</center>
```

---

## Voice rules (CLAUDE.md critical rule — zero tolerance)

Student-facing cells speak TO the student (`you`), never ABOUT "students", never
to instructors. `scripts/voice_lint_notebooks.py` enforces:
no `\bstudents?\b`, no `the instructor`, no facilitation language
(`have them`, `ask the class`, …) in any student-notebook cell. Facilitation
lives in instructor-only cells (marker-stripped) or session guides.

## Naming and placement

- Instructor (gitignored): `notebooks/instructor/nbNN_topic_instructor.ipynb`
- Student (committed): `notebooks/student/nbNN_topic_student.ipynb`
- Figures: `notebooks/figures/`; data: `notebooks/data/` (committed, attributed)
- Generation: `python3 scripts/make_student.py notebooks/instructor/nbNN_*.ipynb`
- After each student notebook: `python3 scripts/update_schedule_badges.py`
  refreshes its Colab badge on `schedule.qmd` (also wired as a PostToolUse hook).
