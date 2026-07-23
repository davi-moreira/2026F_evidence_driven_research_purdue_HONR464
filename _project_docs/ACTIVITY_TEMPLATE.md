# HONR 46400 Notebook Structure Template — v2 (canonical)

> **Canonical reference:** `notebooks/student/nb04_observational_descriptive_student.ipynb`
> (the Week 5 prototype, built in P2) is the reference implementation. Every
> weekly topic notebook (`notebooks/{instructor,student}/nbNN_topic_{instructor,student}.ipynb`)
> MUST follow this template. **One notebook per WEEK** (nb00–nb15), not per
> meeting — each notebook absorbs its week's Mon/Wed lectures (see
> `planning/COURSE_MASTER_PLAN.md` §2 and `scripts/notebooks_map.py`). The
> MGMT474 ML-isms (RANDOM_SEED=474, 60/20/20 splits, ISLP, seaborn) are gone by
> design — do not reintroduce them.

Validated by `scripts/validate_notebooks.py` (which reads the v2 notebook
registry in `scripts/notebooks_map.py`). **Instructor-FIRST workflow:** author
the gitignored cell source `_production_kit/nb_sources/nbNN_<slug>.py`, then
build with `python3 scripts/nbbuild.py NN` — this generates the
`*_instructor.ipynb`, executes it, strips every cell whose source contains
`INSTRUCTOR SOLUTION` to produce the student file, and runs this validator on the
pair. Never hand-edit a student `.ipynb`.

**The central discipline this template operationalizes.** AI is the student's
arm and research assistant, not their brain (`course_config.yaml ai_policy`). The
workflow is **Specify → Delegate → Interrogate → Inspect → Verify → Document →
Defend** (SDIIVDD), student-facing shorthand **Ask → Verify → Document**. Every
notebook makes the student commit their own answer first, delegate to AI under
tight control, interrogate and verify what comes back, log it in the AI Research
Ledger, and defend a bounded claim at the end.

---

## Required cells, in order

### 1. Header (markdown)

```markdown
# [Topic Title — no "Day N", no dates, no "Meeting M#"]

**Topic NN · N lecture(s)**

<hr>

# <center><a class="tocSkip"></center>
# <center>HONR 46400 — Evidence-Driven Research</center>
# <center>Professor: Davi Moreira</center>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/student/nbNN_topic_student.ipynb)

---
```

`**Topic NN · N lecture(s)**` states how many Mon/Wed lectures the week spans
(the async-only module says `async module`). The count is derived mechanically
by `lecture_labels()` in `scripts/notebooks_map.py` — never hand-invented.

### 2. Inquiry & Claim Boundary block (markdown) — REQUIRED, machine-checked

The course's operational spine (the inquiry compass — `planning/INQUIRY_MAP.md`).
State up front which compass position(s) the week emphasizes — **kind**
(descriptive / causal) and **reach** (data at hand / population / unseen cases) —
and the claim boundary it patrols. Weeks 5–9 additionally name the **design
pathway** (observational/experimental × descriptive/causal, or prediction).

```markdown
## 🧭 Inquiry & Claim Boundary

**Inquiry emphasis:** [description (descriptive · data at hand) |
generalization (descriptive · population) | prediction (descriptive · unseen
cases) | causal reasoning | all positions (framing/diagnosis/communication)]

**Design pathway (Weeks 5–9 only):** [observational descriptive | observational
causal | experimental descriptive | prediction | experimental causal]

| | |
|---|---|
| **A claim this topic PERMITS** | "[exact claim template]" |
| **A claim this topic does NOT permit** | "[exact overreach it forbids]" |

**Where this sits in the course:** [one sentence: which week, which milestone it
develops, what it builds on — no meeting numbers, no dates.]

*Provenance: [source-file or "fresh"] | [chapter/section] | [item] | [transformation]*
```

The provenance line follows `planning/SOURCE_AUDIT_V2.md` §7 (the v1→v2 reuse
map) and the evidence-integrity rule. Never invent chapters, declarations,
functions, or datasets.

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
shape so the reader can self-check.

### 5. Lecture openers and SRL cells (markdown) — machine-checked

Multi-lecture notebooks open EACH lecture with an explicit `# Lecture N` heading
cell (Lecture 1 right before section `## 1.`; later lectures after a horizontal
rule) — never meeting numbers, never dates, never italic boundary markers.

**Every lecture opens with a Student Research Lead puzzle cell.** From Week 2 on,
each Mon/Wed lecture is run by a Student Research Lead as a Socratic
investigation, not a summary (`course_config.yaml srl`; `planning/COURSE_MASTER_PLAN.md`
§3). The notebook seeds that opening with a puzzle the reader chews on before any
exposition or AI:

```markdown
### 🧩 Research Puzzle

*(Your Student Research Lead opens with this. Think it through and commit an
answer before we go further — no AI yet.)*

[A short, concrete puzzle whose resolution is the lecture's payoff. Speaks to
"you"; poses a genuine question; is answerable by reasoning, not lookup.]
```

One `### 🧩 Research Puzzle` per `# Lecture N`. Week 1's two launch lectures are
instructor-led; they still carry the puzzle cell (the instructor runs it).

### 6. Content sections (`## 1.`, `## 2.`, …) — narrative pattern + undergraduate voice

The narrative machinery (KEEP):
- Open analytical sections with a **"Why This Matters"** cell voiced by a named
  research-world stakeholder (thesis advisor, journal reviewer, IRB reviewer,
  skeptical peer, policy stakeholder) whose concern is a direct quote.
- **Narrative prose over bullets** in "Reading the evidence" cells.
- Inline Q&A: `> **A question that often comes up here:** *"<q>"*` + one flowing
  paragraph.
- One-sentence **section bridges** at each transition.

The undergraduate voice (ENFORCED — CLAUDE.md "Undergraduate-Friendly Voice"):
- **Em-dashes: ≤ 20 per notebook, ≤ 1 per markdown cell.** Prefer periods,
  commas, and bold lead-ins (`**Why this matters:**`, `**The catch:**`).
- **Every technical term**: bold term → one-sentence plain-language definition →
  concrete example, before the term is used again.
- **Short-to-medium sentences** (~12–25 words), one idea each, always `you`.
- **No fourth-wall meta-references** ("fabricated for this exercise", "planted
  for verification") and **no fabricated citations anywhere** — verification
  exercises use real, retrievable sources.
- Markdown hygiene: escape `\$` and `\~`; emoji vocabulary ✓ ⚠️ 📝 💡 only (the
  section-marker emoji below are structural, not prose decoration).

### 7. The seven required active-learning moves (machine-checked)

Every ordinary notebook contains at least one of EACH, with the exact headings
below. The async-only module (nb13) embeds these inside its module flow.

| Move | Heading marker | What it is |
|---|---|---|
| Pre-run prediction | `### 🔮 Pause & Predict` | commit a written prediction BEFORE running the next cell; the following cell reveals |
| Runnable activity | `### 🛠️ Run the Study` (or `### 🛠️ Hands-On:` variant) | execute + modify real code on real data/simulation |
| Defended decision | `### ⚖️ Make a Design Choice` | choose between stated options and write a one-paragraph defense |
| Practice item | `### 📝 Practice` | short transfer drill (sorting, matching, repairing, classifying) |
| Interpretation task | `### 🔍 Reading the Evidence` | write what an output DOES and DOES NOT establish |
| Milestone transfer | `### 🎯 Project Transfer` | apply the topic to your own project/milestone, in the notebook |
| Exit defense | `### 🛡️ Exit Defense` | the closing move — see §9 |

Pacing rule: direct exposition ≤8 min per segment, <15 min total per lecture;
≥70% of class time active.

**Variants.** The communication/performance notebooks (nb10 poster criticism,
nb11 delivery, nb12 conference) may satisfy the runnable move with structured
criticism or delivery rounds instead of `### 🛠️ Run the Study` — the validator
exempts exactly those three from the runnable-move check, nothing else. The
async module (nb13) embeds all moves inside its self-paced flow and carries no
`### 🧩 Research Puzzle` (there is no Student Research Lead online).

### 8. The high-intensity AI-collaboration blocks (machine-checked)

AI is used constantly and under control. Each ordinary notebook carries **at
least one of each** required block below, marked with the exact heading. These
implement SDIIVDD around the notebook's real work.

| Block | Heading marker | What it is |
|---|---|---|
| Partner briefing | `### 🤝 AI Research Partner` | once near the top: how to task Gemini for THIS topic, what to never delegate, and the reminder to commit your own answer first |
| Gemini prompt + verify | `> 💡 **Gemini Prompt:**` (**≥3**) | a copy-paste prompt + an "After running, verify" checklist (see §8a) |
| Prompt modification | `### 🔁 Modify the Prompt` | change a supplied prompt yourself and predict how the output will change, then check |
| Output interrogation | `### 🔬 Interrogate the Output` | challenge the AI's response for errors, overreach, and fabricated citations; independently verify any code it produced before trusting a result |
| Human-only checkpoint | `### 🧑‍⚖️ Human-Only Checkpoint` | a decision made with AI set aside (one of the never-delegate decisions) |
| AI Research Ledger | `### 📒 AI Research Ledger` | log this notebook's AI use in the structured artifact (D21): task delegated · tool · prompt · output summary · decision · verification method · remaining concern · responsible student |

**Where useful (defined, not hard-required):**
- `### ⚔️ Competing AI Roles` — put two AI roles against each other (e.g.,
  proposer vs skeptic; the GenAI Studio reviewer bench at M5/M7/M9/M13) and
  adjudicate as the human.

### 8a. Gemini prompt + verification block (Ask → Verify → Document)

Every substantive code cell is preceded by a Gemini prompt (the setup cell and
trivial one-line prints are exempt). Prompts are scripts the reader copies into
Google Gemini, written exactly as they would type them (second person, never
about "students"). Each notebook carries **≥3** (machine-checked):

```markdown
> 💡 **Gemini Prompt:** "[prompt text — explain / critique / extend the next cell]"
>
> **After running, verify (the responsible-AI habit):**
> - [ ] Every source the AI cited exists — you retrieved it yourself.
> - [ ] [task-specific fact-check against the cell's actual output]
> - [ ] Log this use in your AI Research Ledger: task, tool, decision, verification.
```

### 8b. Question-driven frame + Q&A density (machine-checked)

Every `## N.` content section either has a question-phrased title or opens with a
bold **Guiding question:** line echoing the schedule's driving/secondary
questions. Every notebook carries **≥3** inline Q&A blocks
(`> **A question that often comes up here:** …`).

### 8c. Figures

External figures live in `notebooks/figures/` (committed; see its README for the
inspected-and-attributed inventory) and embed Colab-compatibly:

```markdown
<center><img src="https://raw.githubusercontent.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/main/notebooks/figures/FILE" width="70%"/></center>

*Caption in one sentence. (Attribution line from notebooks/figures/README.md.)*
```

Never embed a figure you have not looked at; never caption beyond what it shows.

### 9. Exit Defense (markdown) — the closing move, machine-checked

`### 🛡️ Exit Defense` replaces v1's Claim Ticket. It is the SDIIVDD **Defend**
step and the notebook's numbered exit. The reader states one claim they would put
their name on, its boundary, and how AI's contribution was verified:

```markdown
### 🛡️ Exit Defense

Defense #NN — write, in your own words:
1. **The claim I can defend:** [one bounded sentence].
2. **Its boundary:** what this evidence does NOT establish (name the compass
   position and any crossing you did or did not license).
3. **My uncertainty and limitations:** [one sentence].
4. **AI check:** what I delegated, and how I verified it before trusting it.
```

**Written vs spoken exits.** The Exit Defense is the notebook's WRITTEN closing
block. The class ALSO keeps its spoken exit ritual, the **Claim Ticket** read
aloud at the close of every meeting — that ritual lives in the session guides
(the schedule's `exit_ticket` field), not in the notebook. When a run-of-show
says "ledger + Claim Ticket", it means: complete the notebook's 📒 ledger row
and 🛡️ Exit Defense, then the spoken Claim Ticket closes the room.

### 10. Instructor-solution cells (stripped from the student file)

1. `### INSTRUCTOR SOLUTION — Exercise N` (markdown heading)
2. `# INSTRUCTOR SOLUTION` first line of solution code cells
3. `<!-- INSTRUCTOR SOLUTION -->` first line of solution markdown cells

Student placeholders that REMAIN: `### YOUR ANSWER HERE:` (markdown) and
`# YOUR SOLUTION HERE` (code). Solutions are **model exemplars** (a well-scoped
question, a worked justification, a verified analysis, a filled Ledger row) —
concept-level quality, not code golf. Instructor notebooks may also carry
`<!-- INSTRUCTOR SOLUTION -->`-prefixed facilitation notes (timing, common
stumbles, SRL coaching) — same marker, same strip.

### 11. Wrap-up (markdown)

`## N. Wrap-Up` — key takeaways as short narrative (not a bare list), one
blockquoted critical rule, and a warm bridge naming the next notebook and the
milestone it serves.

### 12. Provenance & bibliography (markdown)

`## N+1. Sources & Provenance` — the notebook's full provenance lines (one per
borrowed element), the dataset attribution line (if data used):
*"Dataset from the `rdss` package (Blair, Coppock & Humphreys, MIT License),
companion to* Research Design in the Social Sciences *(2023)."*, and the reading
citations (RDSS chapters at book.declaredesign.org; optional CB cases at
callingbullshit.org). Only verified sources — `scripts/audit_sources.py` and
`scripts/validate_coverage.py` cross-check citations against the verified
inventory.

### 13. Thank-you cell (markdown, final)

```markdown
<center>

Thank you!

</center>
```

---

## Voice rules (CLAUDE.md critical rule — zero tolerance)

Student-facing cells speak TO the reader (`you`), never ABOUT "students", never
to instructors. `scripts/voice_lint_notebooks.py` enforces: no `\bstudents?\b`,
no `the instructor`, no facilitation language (`have them`, `ask the class`, …)
in any student-notebook cell. Facilitation (including how the Student Research
Lead runs the puzzle) lives in instructor-only cells (marker-stripped) or the
session guide.

## Naming and placement

- Cell source (gitignored, canonical for editing): `_production_kit/nb_sources/nbNN_<slug>.py`
- Instructor (gitignored): `notebooks/instructor/nbNN_topic_instructor.ipynb`
- Student (committed): `notebooks/student/nbNN_topic_student.ipynb`
- Figures: `notebooks/figures/`; data: `notebooks/data/` (committed, attributed)
- Build one notebook end-to-end: `python3 scripts/nbbuild.py NN`
- After building, `scripts/update_schedule_badges.py` refreshes the Colab badge
  on `schedule.qmd` (also wired as a PostToolUse hook); sync instructor material
  with `scripts/sync_instructor_repo.sh`.

## Milestone studio notebooks (msNN) — reduced required set

Each milestone M0–M15 ships a light Friday studio notebook
`notebooks/student/msNN_<slug>_student.ipynb` (instructor version gitignored,
same markers). Required cells, in order — nothing else is mandatory:

1. Header: title, `**Milestone MN · studio notebook**`, Colab badge.
2. `## 🎯 Definition of Done` — the brief's definition of done + required
   evidence, restated to the reader.
3. `### 🤝 AI Research Partner` — what AI may help with in this sprint and what
   you must decide yourself.
4. `> 💡 **Gemini Prompt:**` (≥1) with the After-running-verify checklist —
   the sprint's AI assist.
5. `### 🗡️ Red-Team Exchange` — the peer + AI review protocol for this
   milestone (what to attack, what to log).
6. `### 📒 AI Research Ledger` — the sprint's ledger row(s).
7. `### ✅ Submission Checklist` — the brief's checklist + dossier update line.

## Validation rules — the machine-checked contract (validate_notebooks v2)

For every ORDINARY topic notebook (nb00–nb15 except as noted), the validator
asserts, by exact marker string:

| # | Check | Marker / rule | Threshold |
|---|---|---|---|
| 1 | Topic header | `**Topic NN · N lecture(s)**` or `**Topic NN · async module**` | =1, count matches `lecture_labels()` |
| 2 | Colab badge | `colab.research.google.com/github/...nbNN_..._student.ipynb` | =1 |
| 3 | Inquiry block | `## 🧭 Inquiry & Claim Boundary` with `**Inquiry emphasis:**`, `**Design pathway:**`, PERMITS + does-NOT-permit rows, `*Provenance:` | all present |
| 4 | Objectives | `## Learning Objectives` | =1 |
| 5 | Setup | `SEED = 464` + `default_rng`; `seaborn` absent notebook-wide | required |
| 6 | Lecture heads | `# Lecture i` per schedule; one `### 🧩 Research Puzzle` per lecture (exempt: nb13) | exact |
| 7 | Moves | `### 🔮 Pause & Predict`, `### ⚖️ Make a Design Choice`, `### 📝 Practice`, `### 🔍 Reading the Evidence`, `### 🎯 Project Transfer`, `### 🛡️ Exit Defense` | ≥1 each |
| 8 | Runnable move | `### 🛠️ Run the Study` or `### 🛠️ Hands-On:` | ≥1 (exempt: nb10, nb11, nb12) |
| 9 | Partner briefing | `### 🤝 AI Research Partner` | ≥1 |
| 10 | Gemini prompts | `> 💡 **Gemini Prompt:**` each followed by `**After running, verify` | ≥3 |
| 11 | Prompt modification | `### 🔁 Modify the Prompt` | ≥1 |
| 12 | Interrogation | `### 🔬 Interrogate the Output` | ≥1 |
| 13 | Human-only | `### 🧑‍⚖️ Human-Only Checkpoint` | ≥1 |
| 14 | Ledger | `### 📒 AI Research Ledger` | ≥1 |
| 15 | Q&A density | `> **A question that often comes up here:**` | ≥3 |
| 16 | Wrap + sources | `## N. Wrap-Up`, `## N+1. Sources & Provenance`, final thank-you cell | present, ordered |
| 17 | No leakage | `INSTRUCTOR SOLUTION` absent from the student file | =0 |

For every MILESTONE STUDIO notebook (msNN): checks 2, 5 (if code present), plus
`**Milestone MN · studio notebook**`, `## 🎯 Definition of Done`,
`### 🤝 AI Research Partner`, ≥1 Gemini prompt+verify, `### 🗡️ Red-Team
Exchange`, `### 📒 AI Research Ledger`, `### ✅ Submission Checklist`.

Voice, dates, em-dash budget, and citation integrity are enforced separately by
`voice_lint_notebooks.py` and `audit_sources.py`. The AI Research Ledger's
CONTENT quality is graded by rubric, not machine-checked.
