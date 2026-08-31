# Course Material Production Workflow (per week)

The end-to-end pipeline for producing **one week's unit** of HONR 46400: the topic
notebook (`nbNN`, one per week, `nb01`–`nb16`), its milestone brief, its session
guide, and the schedule rows that place it on the calendar. It generalizes the
sequence used across the v2 build (DECISIONS.md D17–D21) and is run once per week.

> This doc **sequences the whole pipeline**. The behavior-changing *quality gates*
> for each step — Instructor-First editing, the voice rule, evidence-integrity,
> render + commit — live in `CLAUDE.md`; this doc points to them, it does not
> restate them.

This is an **in-person MWF research course**, not the MGMT474 online ML course this
folder was seeded from. There are no recorded videos, no NotebookLM concept clips,
and no CV-first / test-set machinery. The unit of production is the **week**, and
its downstream artifacts are the **session guide** (how the instructor runs the
room) and the **milestone brief** (what the students build).

**Since D74 the week's notebook is itself collected.** Every student submits the
`nbNN` they worked in class, once a week, graded on completion under the 20%
**Lecture Notebooks** category. Nothing changes in how a notebook is produced, but
it is no longer only a teaching surface: what the reader writes in it is what gets
handed in, so authoring must leave visible room to write and must fit the 50
minutes. See "The weekly notebook is collected" below.

**The printed weekly quiz is retired for this edition (D58), not deleted.** No
quiz is produced, printed, administered, or scored this term, so quiz production
is not a step in the weekly pipeline below. The knowledge and the material are
kept: the banks and keys live under the gitignored `_quizzes/2026Fall/weekly/`,
the quiz builders stay in `scripts/`, and the option-length gate
`scripts/audit_answer_length.py` still guards any bank that is ever imported (the
dormant *MC Option-Length Parity* rule in `CLAUDE.md` states the thresholds).
Never delete a quiz file or a quiz script; a future edition turns the step back on.

---

## Where each artifact lives (and what is public)

| Artifact | Path | Git |
|---|---|---|
| Cell source (canonical for editing) | `_production_kit/nb_sources/nbNN_<slug>.py` | ignored (local) |
| Instructor notebook (built from source) | `notebooks/instructor/nbNN_<slug>_instructor.ipynb` | ignored (local) |
| **Student notebook (the deliverable, and now a collected artifact)** | `notebooks/student/nbNN_<slug>_student.ipynb` | **tracked / public** |
| Datasets + downloadable bundle | `notebooks/data/…`, `notebooks/data/data.zip` | tracked |
| Session guide | `session_guides/NN_session_guide.md` | ignored (generator tracked) |
| Milestone brief | `_research_project/2026Fall/milestone_NN_<slug>.md` | tracked |
| Schedule data (per meeting, incl. the lab-meeting reporter fields) | `scripts/schedule_data/partN.py` | tracked |
| Meeting schedule (generated) | `planning/MEETING_SCHEDULE.{csv,md}` | tracked |
| Public schedule page (generated) | `schedule.qmd` → `docs/` | tracked |
| Instructor tab (private-repo badges) | `instructor.qmd` → `docs/instructor.html` | tracked (ships openly, D35) |

Only the **student notebook**, the **datasets**, the **milestone briefs**, the
**planning docs**, and the **rendered `docs/`** are public. The cell source,
instructor notebooks, and session guides are instructor-facing and local-only
(gitignored); instructor notebooks reach the instructor via the **private repo**
(Phase E), never the public one.

---

## The pipeline

### Phase A — Notebook (the source of truth)

**A1. Edit the cell source FIRST.** Never edit a `notebooks/student/*.ipynb` or a
`notebooks/instructor/*.ipynb` directly. All authoring happens in the gitignored
`_production_kit/nb_sources/nbNN_<slug>.py`, which exports `CELLS: list[(kind,
source)]`. Solutions live here as `INSTRUCTOR SOLUTION` cells; the student file is
a mechanical, answer-stripped copy of the built instructor file.
*Gate: CLAUDE.md → Instructor-First Notebook Editing.*

Every topic notebook must carry the blocks the template and the v2 rules require:

- the **Inquiry & Claim Boundary** block — the compass position (kind × reach) with
  its PERMITS / NOT rows (CLAUDE.md → Inquiry-Declaration Justification);
- an **AI Research Ledger** entry block — task delegated · tool · prompt · output
  summary · decision · verification method · remaining concern · responsible person
  (DECISIONS.md D21); every embedded AI prompt ends with an
  **"After running, verify:"** habit (the prompts are tool-generic since D30);
- a **Sources & Provenance** section with real, retrievable citations only
  (CLAUDE.md → Evidence-Integrity), and the setup discipline `SEED = 464`, no
  seaborn;
- per lecture, a `### 📣 Lab Meeting: Today's Reporter` brief right after
  `# Lecture N`, then the `### 🧩 Research Puzzle`, with the lecture's three
  questions in `### 🔎 Questions to Keep You Thinking` just past the puzzle (D74;
  `validate_notebooks.py` counts the first two per lecture). Do **not** author the
  `### 📣 My Report Plan` cell: `nbbuild.py` injects it beside every brief.

**A2. Build the notebook.** One command does the whole chain:

```bash
.venv/bin/python scripts/nbbuild.py nbNN
```

`nbbuild.py` writes `notebooks/instructor/nbNN_<slug>_instructor.ipynb` from the
source, **executes it end-to-end with nbclient** (kernel = repo `.venv`, cwd = repo
root, 300 s/cell — any raised error fails the build), **strips every `INSTRUCTOR
SOLUTION` cell** to generate the student file, runs `validate_notebooks.py` on the
pair, and refreshes the `schedule.qmd` badges. A `PostToolUse` hook additionally
runs `voice_lint_notebooks.py` whenever a student notebook is written.

**A3. Run the evidence gate.** Before the notebook is considered done:

```bash
.venv/bin/python scripts/audit_sources.py   # URL allowlist + verified-citation registry + fake-citation blocklist
```

### Phase B — Schedule (only if sequencing changed)

Skip this phase if the week's placement, driving questions, reporter assignment,
or milestone mapping did not change.

**B1. Edit the meeting data** in `scripts/schedule_data/partN.py`. This is where
each Mon/Wed lecture carries its **`srl_slot`** — since D74 the **lab-meeting
reporter slot** for that lecture — and its **`srl_focus`** (that lecture's puzzle
focus). The field keys keep their historical `srl_*` names for machine continuity
with the generators and the schedule page; what they now name is the reporter, not
a lead. The draw itself carries over unchanged from D69/D71 (25 slots, 6 students,
4 or 5 each), so do not re-draw. Fridays are studios and async meetings are
self-contained; both leave these fields empty (they are in `OPTIONAL_EMPTY`).

**B2. If the calendar backbone itself moved** (a date, day, or modality changed),
regenerate the verified backbone first — `build_meeting_schedule.py` validates
against it and will refuse to run on a mismatch:

```bash
python3 scripts/validate_calendar.py --emit-csv   # (re)write planning/CALENDAR_BACKBONE.csv
```

**B3. Rebuild the meeting schedule** (this is a **gate**, not just a generator):

```bash
python3 scripts/build_meeting_schedule.py         # writes MEETING_SCHEDULE.{csv,md}; non-zero exit on any invariant break
```

### Phase C — Session guide

Regenerate the instructor's run-of-show from the schedule (never hand-write it):

```bash
python3 scripts/build_session_guides.py
```

Guides are gitignored but the generator is tracked, so they are always reproducible.
Sessions are labeled by kind — "Lecture i of N", "Studio Friday", "Async module" —
with **no dates and no meeting numbers** (CLAUDE.md → Lecture Labels, Never Dates).
The printed run-of-show frames come from `course_config.yaml lab_meeting:`, which
D74 set to Monday **10 / 21 / 12 / 7** and Wednesday **10 / 20 / 12 / 8** (Friday's
studio stays **5 / 40 / 5**); each frame's first ten minutes are the lab meeting,
and each set still sums to 50.

### Phase D — Milestone brief

**D1. Author/update the brief** at `_research_project/2026Fall/milestone_NN_<slug>.md`.
Milestones M1–M16 pair one-to-one with the weekly notebooks; the brief is what the
Friday studio kicks off and what the student submits into the Research Project
Dossier (with a cumulative AI Research Ledger appended, D21).

**D2. Validate the milestone system:**

```bash
python3 scripts/validate_milestones.py            # chain in PROJECT_MILESTONES.md vs. schedule + backbone; fixed anchors + due-date uniqueness
```

**D3. Replicate to Brightspace manually.** The brief is the source of truth; the
Brightspace assignment page is hand-copied from it. There is no generator for the
LMS side — keep the brief authoritative and the Brightspace page a faithful copy.

### Phase E — Sync instructor material, then publish

**E1. Push instructor material to the private repo** (the Instructor tab's backing
store):

```bash
bash scripts/sync_instructor_repo.sh              # notebooks/instructor/ + session_guides/ + notebooks/data/ → private repo
```

**E2. If a dataset changed,** regenerate the downloadable bundle before rendering:

```bash
.venv/bin/python scripts/make_dataset_zip.py      # rebuild notebooks/data/data.zip, then commit it
```

**E3. Render and publish** (CLAUDE.md → Commit AND Render Webpage — the project's
most common mistake is skipping the render):

```bash
git add notebooks/student/nbNN_*_student.ipynb <changed .qmd / schedule data / briefs>
git commit -m "feat: ..."
/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto render
git add docs/ && git commit -m "build: Render Quarto site"
git push origin main
```

Instructor-facing pages ship openly (D35 retired the page encryption); the
private instructor repo + GitHub auth is the protection. Always publish through
`quarto render`, never by hand-editing `docs/`.

---

## The weekly notebook is collected (D74)

The lecture notebook is a graded artifact, so the production pipeline now has a
consumer it did not have before: the student's own submission.

- **What is collected.** One notebook per week per student — the `nbNN` worked in
  class — due **11:59 PM on the Sunday that ends the studio week** (Week 16 closes
  Fri Dec 11). The dated list is `planning/LECTURE_NOTEBOOK_SCHEDULE.md`
  (generated); the machine spine is `course_config.yaml lecture_notebooks:`.
- **How it is graded.** Completion only: worked through and handed in. Never on
  whether the answers came out right, and never on how that student's live lab
  meeting report went. Credit `1.0` on time, `0.5` within seven days, `0`
  otherwise; `N = 16`, `d = 2`; the block is
  `20.0 × (sum of the highest 14 credits) / 14`.
- **Where it is submitted.** On the course platform, by hand, like the milestone
  briefs (Phase D3). There is no generator for the LMS side.
- **What that changes in Phase A.** Every writing move must leave a visible,
  fillable place in the notebook (the 📣 report-plan lines, the seven in-class
  moves, the 📒 ledger row per lecture), the required path must be completable
  inside the 50 minutes, and nothing below a lecture's `### ⏸` line — or behind a
  🏠 label — may ever be needed for the credit. The milestone studio notebooks
  (`msNN`) are unaffected: they arrive with their milestone, not under this
  category.

The lecture notebook is **not** a participation item and never carries
participation's ±0.9 contribution adjustment.

---

## The validator battery (what gates what)

| Script | Guards | When it runs |
|---|---|---|
| `validate_calendar.py` | the 43-meeting backbone (42 in-person + 1 async); `--emit-csv` rewrites `CALENDAR_BACKBONE.csv` | before any schedule change to the calendar |
| `build_meeting_schedule.py` | schedule data matches the backbone (row count, columns, date/day/modality, required fields) — **fails the build on mismatch** | every schedule regeneration |
| `validate_milestones.py` | M1–M16 present, dev-meetings precede due dates, fixed anchors, no shared due dates | after any milestone or schedule edit |
| `validate_notebooks.py` | template conformance: Inquiry & Claim Boundary block, provenance + Sources, the active-learning moves, one `📣 Lab Meeting` brief + one `🧩 Research Puzzle` per lecture, `SEED = 464`, no seaborn, no leaked `INSTRUCTOR SOLUTION`, markdown hygiene | inside `nbbuild.py` |
| `voice_lint_notebooks.py` | undergrad voice: em-dash budget, no "students" in student cells, no dates / "Meeting M#" (D13/D14) | inside `nbbuild.py` + `PostToolUse` hook |
| `audit_sources.py` | citation integrity: URL allowlist, verified-citation registry, fake-citation blocklist | before shipping any notebook |
| `update_schedule_badges.py --check` | `schedule.qmd` is not stale vs. the tracked student notebooks | before push |

---

## Dependency order — what must precede what

```
A  cell source ─► nbbuild (build → execute → strip → validate → badge) ─► audit_sources
                                                                              │
                  (if sequencing changed)                                     │
B  schedule_data/partN.py ─► [validate_calendar --emit-csv] ─► build_meeting_schedule (GATE)
                                                                              │
C                                          build_session_guides ◄────────────┤
                                                                              │
D  milestone brief ─► validate_milestones ─► (manual Brightspace copy)        │
                                                                              ▼
E  sync_instructor_repo.sh ─► [make_dataset_zip] ─► quarto render ─► commit docs/ ─► push
```

Phase A is always required. Phase B runs only when the week's placement, questions,
reporter assignment, or milestone mapping change. The schedule (B) must be current before
the session guides (C) are regenerated, because the guides are parsed from
`MEETING_SCHEDULE.csv`.

---

## Who does what

| Step | Claude can do it | Manual (instructor) |
|---|---|---|
| A1 author cell source | ✅ | review the compass declaration + solutions |
| A2 `nbbuild.py` build/execute/strip | ✅ | — |
| A3 `audit_sources.py` | ✅ | — |
| B schedule data + regenerate | ✅ | confirm the reporter draw |
| C `build_session_guides.py` | ✅ | — |
| D1 milestone brief | ✅ | approve scope |
| D3 Brightspace page | — | ✅ (copy from the brief) |
| E1 `sync_instructor_repo.sh` | ✅ (needs `gh` auth) | — |
| E3 render + commit + push | ✅ | — |

---

## Quality gates (apply at every relevant phase)

- **Instructor-first, always.** Edit the cell source; never touch a built `.ipynb`
  directly, and never let the student file drift from the instructor version.
- **Voice + evidence integrity.** `voice_lint_notebooks.py` clean, `audit_sources.py`
  clean; every AI use logged in the AI Research Ledger with a verification method.
- **Escape** `$`→`\$` and `~`→`\~` in all rendered markdown (notebooks, guides,
  briefs, `.qmd`) — `validate_notebooks.py` fails on unescaped `$<digit>`/`~<digit>`.
- **Render + commit `docs/` + push** after any `.qmd` / notebook / schedule / dataset
  change; the instructor page ships openly (D35 retired the page encryption) and the
  private instructor repo is what protects genuinely private material.
- Keep instructor-only artifacts (cell sources, instructor notebooks, session guides)
  **out of the public repo** — they are gitignored and reach the instructor via the
  private repo sync.

---

*Rewritten 2026-07-23 for the v2 course (DECISIONS.md D17–D21); replaces the
MGMT474-era video/NotebookLM/quiz pipeline; the weekly-quiz production step was
retired for this edition by D58, with the banks and builders kept. Updated
2026-08-31 for D74: the Student Research Lead became the ten-minute lab meeting
(retired in place — no SRL file or script is ever deleted), the MW frames became
10 / 21 / 12 / 7 and 10 / 20 / 12 / 8, and the weekly lecture notebook became a
collected 20% completion contract.*
