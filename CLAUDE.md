# HONR 46400 Evidence-Driven Research — AI Assistant Guide

This file documents the rules and workflows that change Claude's behavior in this
repository. Reference material lives in linked files — read those when relevant,
not by default.

## Project Mission

**HONR 46400 — SP: Evidence-Driven Research** ("How to Design, Analyze, Verify,
and Defend Empirical Research"), a semester-long Honors College seminar (Fall
2026, **Mon/Wed/Fri, 50 minutes, in person**, ~5 students, individual projects)
teaching honors students — **without assuming a quantitative or computing
background** — to run an original evidence-driven research project from
curiosity to a publicly defended claim. The course's defining message:

> **AI is your arm and your research assistant, not your brain.**

Students direct AI (their AI tools in Colab; Purdue GenAI Studio reviewer roles) through
the **Specify → Delegate → Interrogate → Inspect → Verify → Document → Defend**
workflow (everyday shorthand: **Ask → Verify → Document**), while keeping every
research decision — problem, question, design, measurement, ethics, claims,
uncertainty, defense — human. Deliverables: a poster presented at the **Purdue
Fall Undergraduate Research Expo (Tue Nov 17, 2026; poster locked Fri Nov 6,
5 PM)**, a replication + red-team report, a research note grown into a final
research chapter, an AI-management portfolio, and an oral evidence defense.

- **Instructor:** Professor Davi Moreira
- **Repository:** https://github.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464
- **Website:** https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/
- **Deployment:** Quarto → `docs/` → GitHub Pages
- **v1 build** (compass-sequenced 20-notebook course) preserved at git tag
  `v1-compass-build`; v1 sources archived in `_production_kit/nb_sources_v1/`
  and `_production_kit/schedule_data_v1/` (gitignored).

## See Also (Reference Files)

| File | When to read |
|---|---|
| `_project_docs/ACTIVITY_TEMPLATE.md` | Creating/restructuring a topic notebook — the machine-validated template |
| `_project_docs/DECISIONS.md` | Before proposing convention changes — D17–D22 govern the v2 build |
| `planning/COURSE_MASTER_PLAN.md` | Sequencing source of truth (16 weeks, nb01–nb16, M0–M15) |
| `planning/PROJECT_MILESTONES.md` | The milestone chain (dev meetings, presentations, due dates) |
| `planning/SOURCE_AUDIT_V2.md` | The rebuild audit: rulings, reuse map, GenAI Studio verification |
| `planning/MEETING_SCHEDULE.md` | Per-meeting detail (43 × 34; generated from `scripts/schedule_data/`) |
| `planning/INQUIRY_MAP.md` | The compass (questions) + design-pathway (designs) layers |
| `project/srl/` | Student Research Lead handbook, templates, rubric |
| `genai_studio/` | GenAI Studio role specs, KB strategy, Colab PoC |
| `CONVERSATION_LOG.md` | Project history and prior decisions |

**Canonical notebook reference:** `notebooks/student/nb05_observational_descriptive_student.ipynb`
(the v2 gold standard, built as the Phase-2 prototype) — match its formatting
exactly. Cell sources live in gitignored `_production_kit/nb_sources/nbNN_<slug>.py`;
edit the source, then rebuild with `.venv/bin/python scripts/nbbuild.py nbNN`.

---

## 🚨 CRITICAL RULE — Voice and Audience in Student-Facing Content  *(KEEP verbatim)*

The student activity is read **BY students**, not by instructors who then teach it.
Every sentence in a student-facing cell — including AI prompts and "After running,
verify" checklists — must be written **TO the student**, never ABOUT the student and
never TO the instructor.

1. Never write "students" as a third-party noun inside a student-facing cell.
   Rewrite in second person (`you`), neutral imperative, or first person.
2. AI prompts are scripts the student copies into the AI tool — they must sound like
   something a student would actually type.
3. No instructor-voice / facilitation language in student cells. That belongs only
   in `session_guides/NN_session_guide.md` (gitignored).
4. Session guides may reference students in third person in wrapper prose, but NOT
   inside blockquote read-aloud scripts (`> *"..."*`).

```bash
.venv/bin/python scripts/voice_lint_notebooks.py                      # all student notebooks; expect ✓ clean
python3 scripts/voice_check_guides.py session_guides/NN_session_guide.md
```

---

## 🚨 CRITICAL RULE — Undergraduate-Friendly Voice  *(D14; unchanged)*

Notebooks are read by honors undergraduates with **no quantitative background**.
The narrative machinery stays; the prose must read like a person, not a model.

**Keep (the pedagogy):** named research-world stakeholders opening "Why This
Matters" cells; narrative prose over bullet lists; inline Q&A blocks
(`> **A question that often comes up here:** …`); section bridges and warm
wrap-ups bridging to the next week.

**Enforce (machine-checked by `scripts/voice_lint_notebooks.py`):**
1. **Em-dash budget: ≤ 20 per notebook, ≤ 1 per markdown cell.**
2. **Every technical term:** bold term → one-sentence plain-language definition
   → concrete example, before reuse.
3. **Short-to-medium sentences** (~12–25 words), one idea each, second person.
4. **No fourth-wall meta-references** about how the material was constructed.
5. **No fabricated citations anywhere** (D16).

---

## 🚨 CRITICAL RULE — Evidence-Integrity & Results-Verification  *(unchanged)*

1. **Every empirical claim traces to a real, retrievable source.** If a claim
   came from an AI tool, the underlying source is independently located and
   confirmed to exist.
2. **Every result is verified before it is reported** — recomputed,
   triangulated, or spot-checked, and the check is recorded.
3. **Decisions are documented, not just outcomes.**
4. **No planted-fake citations, even as a teaching device** (D16); hallucination
   demos catch LIVE AI output, never planted text.

```bash
.venv/bin/python scripts/audit_sources.py
```

---

## 🚨 CRITICAL RULE — The AI Research Ledger & SDIIVDD  *(D21 — replaces "Responsible-AI-Use Documentation")*

Every deliverable and every notebook session appends to the student's **AI
Research Ledger** (fields: task delegated · tool used · prompt · output summary
· decision · verification method · remaining concern · responsible researcher).
Embedded AI prompts carry an **"After running, verify:"** checklist ending with
a ledger line. Every notebook also contains: an AI Research Partner briefing,
an initial human commitment BEFORE consulting AI, at least one required prompt
modification, an AI-output interrogation, a **Human-Only Checkpoint** (no AI),
and an **Exit Defense**. A missing ledger entry scores the rubric's Craft
criterion 0 and returns the submission. The claim ledger (what the research
asserts) is a separate instrument from the AI Research Ledger (what AI did and
how it was checked).

---

## 🚨 CRITICAL RULE — Inquiry-Declaration Justification  *(updated for the two layers)*

Questions are classified on the **inquiry compass** (RDSS ch. 7): **kind**
(descriptive vs causal) × **reach** (data at hand / population / unseen).
Designs are classified on the **library pathways** (RDSS ch. 15–18):
observational/experimental × descriptive/causal, plus **prediction as its own
answer objective** (never forced into either grid; experimental assignment does
NOT automatically imply a causal inquiry). Whenever a student declares, the
deliverable must state at a conceptual level: (1) why kind + reach fit the
question's words, (2) which crossing licenses the design holds (sampling →
population; prediction-time honesty + held-out check → unseen; assignment /
identification → causal) and hence what the answer can and cannot establish,
and (3) key limitations and uncertainty. Canonical: `planning/INQUIRY_MAP.md`;
machine core: `course_config.yaml inquiry_framework:`. Never reintroduce the
retired four-approach grid vocabulary (D12).

---

## 🚨 CRITICAL RULE — Uncertainty & Limitations in Communication  *(unchanged)*

Findings are never communicated as certainties. Every written report and oral
defense states the uncertainty around its claims and the limitations of its
evidence and method. A results statement with no uncertainty/limitations framing
is a defect.

---

## 🚨 CRITICAL RULE — Lecture Labels, Never Dates  *(D13 rule; unchanged mechanics)*

Notebooks and session guides carry **no calendar dates and no "Meeting M#"
references** — position is expressed as `**Topic NN · N lecture(s)**` headers
and explicit `# Lecture 1` / `# Lecture 2` heading cells, derived mechanically
from `lecture_labels()` in `scripts/notebooks_map.py` (computed from
`planning/MEETING_SCHEDULE.csv`). Dates live ONLY on `schedule.qmd` and in
milestone briefs (`_research_project/2026Fall/`).

---

## 🚨 CRITICAL RULE — The Flipped Classroom & 50-Minute Architectures  *(D17/D18, amended D22)*

**Every Mon/Wed lecture from Week 2 is led by a Student Research Lead (SRL)**
running a Socratic investigation. Slots are **randomly assigned at the start of
the semester** (no rotation, no seats). Each lecture's **SRL Lead Brief** is a
STUDENT-VISIBLE `### 🎤 SRL Lead Brief` cell that opens that lecture in its
notebook (right after `# Lecture N`, before the 🧩 Research Puzzle); leads prep
from one week ahead and submit a preparation script/notebook two days ahead.
Briefs must stay simple to follow and explicitly leave room for the lead's own
staging. Fixed section frames, enforced by the session-guide generator
(sums = 50):

- **Monday:** 0–9 SRL research puzzle · 9–31 guided AI research-partner
  investigation · 31–43 human verification + instructor formalization ·
  43–50 decision & defense (ledger + Claim Ticket).
- **Wednesday:** 0–7 SRL retrieval & challenge · 7–30 intensive applied AI
  laboratory · 30–42 peer defense + adversarial questioning · 42–50 project
  transfer (ledger + Claim Ticket).
- **Friday studio (no new topic content):** 0–10 weekly multiple-choice topic
  quiz (printed; `_quizzes/2026Fall/weekly/`) · 10–15 research stand-up ·
  15–45 milestone kickoff (presented from the course Brightspace page) +
  AI-supported work with the student's AI assistant · 45–50 revise, update
  ledger + dossier, submit (Claim Ticket). The Friday red-team block was
  RETIRED (D30); students WORK ON milestones at the studio (no weekly
  presentations).

Week 1's two lectures are instructor-led to model the format. SRL materials:
`project/srl/` + the course-book appendix `book/srl.qmd`; the milestone chain
and weekly-architecture orientation live in nb01 Lecture 1 (not on the
syllabus).

---

## 🚨 CRITICAL RULE — Dataset Distribution  *(D15; unchanged)*

`notebooks/data/` is the single canonical dataset folder; everything ships in
`notebooks/data/honr46400_datasets.zip`, linked from Material and Schedule.
After any dataset change:

```bash
.venv/bin/python scripts/make_dataset_zip.py
```

Notebooks load data via `load_course_data()` (GitHub raw first, local fallback).

---

## 🚨 CRITICAL RULE — The EDR|AI Book-First Loop  *(D20, amended D23/D24/D25/D26)*

The course book is **EDR|AI** (*Evidence-Driven Research in the Age of AI*;
`book/`, 37 chapters + Part I overview; front matter: Preface then About the
Author; appendices: SRL, Verification Guide, For Instructors; rendered to
`docs/book/`; book author is "Davi Moreira", no title). The loop:

1. **Book and course are DIFFERENT artifacts (D25).** The book owns its
   notebooks: every chapter's badge opens its OWN companion Colab notebook
   (`notebooks/book/chNN_<slug>.ipynb` + `pt/`/`es/`), generated by
   `scripts/build_book_notebooks.py` — rerun it after ANY chapter edit. The
   chapter's "Colab laboratory" section introduces the companion notebook,
   then names its primary course lab (nbNN) as companion-course material. The
   **For Instructors** appendix presents and links all course material; it is
   **password-locked** (D26): each book render's post-render encrypts
   `docs/book*/for-instructors.html`; the password lives ONLY in gitignored
   `_production_kit/page_password.txt` (or env `HONR_INSTRUCTOR_PASSWORD`),
   is requested by email, and must NEVER appear in committed files. The
   generator also derives each chapter's **"It is your turn" RUBRIC** (D26):
   a rubric cell in the companion notebook + `<edition>/_iyt-rubrics.qmd`
   included in the locked appendix — never hand-edit those files.
2. **Development banners + seeded simulations (D26).** Every chapter carries
   a `.review-pending` warning banner until Davi reviews it (the Part I
   overview page too — `part1_overview` in the registry): the registry is
   `planning/BOOK_REVIEW_STATUS.yml`; when he reports a chapter reviewed,
   flip its flag, run `scripts/update_chapter_review_banners.py`, re-render.
   Companion-notebook header spec (D27): logo → title → "Authored by Davi
   Moreira" (links to the book) → companion line → links → the one rule.
   NEVER add artifact-boundary meta-commentary to reader-facing content
   (no "this belongs to X, not Y" sentences). Chapter badges use
   `[![](badge){fig-alt="Open In Colab"}](url)` — the empty alt suppresses
   Pandoc's implicit-figure caption; keep that form. Part I figure:
   `scripts/build_book_part1_figure.py` (mermaid retired).
   Whenever possible, chapters embed **seeded (SEED=464) simulation code that
   visually presents the concept**: the chapter shows the code AND the
   pre-generated figure (`scripts/build_book_sim_figures.py`, localized
   labels, offline — no render-time execution); keep the chapter block and
   the script in sync, and the code flows into the companion notebook
   automatically. Shipped so far: ch11, ch14, ch15 — extend as chapters are
   reviewed. ALL book prose follows `_project_docs/BOOK_VOICE_POLICY.md`
   (D28: must never read as AI-generated; teaching devices stay, the tells
   go; never say a reader "does not need to be enrolled" — frame
   self-learning positively). Lint: `scripts/voice_lint_book.py`
   (`--strict` on newly written prose).
3. **Notebook content must reflect the book** — course notebooks derive from
   the chapters; every notebook's wrap-up names its chapters; never edit a
   chapter's design content without checking its notebook (and vice versa).
   Every milestone brief M0–M15 carries a **Book Anchor**: students submit the
   anchored chapters' "It is your turn" sections (milestone NN ↔ nb(NN+1)'s
   chapters; the 16 anchors partition all 37 chapters).
4. **The instructor manually reviews and updates the book**; the assistant then
   articulates and incorporates those reviews across the course material
   (notebooks, guides, site).
5. **The book is institution-agnostic** (used outside Purdue): chapter bodies
   say "your course platform", "AI reviewer bench", "your research conference";
   Purdue specifics appear only as parentheticals (the For Instructors appendix
   is where the companion course is presented). Reading model: EDR|AI chapters
   REQUIRED, matching RDSS chapters RECOMMENDED (stated on the Material page
   and preface — the in-chapter Reading boxes were retired, D24).
   The book is a SELF-CONTAINED MANUAL: every chapter ends with an
   **"It is your turn"** section, and the 37 sections chain into a complete
   research project/paper by the end (no course-milestone language in chapter
   bodies). Domains for examples: econ, political science, business, biology.
   The "AI can review AI — but the last decision is human" rule lives in the
   Verification Guide appendix and wherever chapters verify.
6. **Translations:** `book-pt/` (PT-BR) and `book-es/` (ES) are generated from
   the English edition (the source of truth) and must be resynchronized after
   any EN chapter edit. Render all three books on any book change:

```bash
.venv/bin/python scripts/build_book_notebooks.py          # 111 companion notebooks + rubrics
.venv/bin/python scripts/update_chapter_review_banners.py # banners from BOOK_REVIEW_STATUS.yml
.venv/bin/python scripts/build_book_sim_figures.py        # seeded sim figures (if sims changed)
.venv/bin/python scripts/voice_lint_book.py               # BOOK_VOICE_POLICY tells (D28)
.venv/bin/python scripts/validate_book_sync.py            # chapter↔notebook links, both directions
quarto render book/ && quarto render book-pt/ && quarto render book-es/  # AFTER the site render
```

---

## 🚨 CRITICAL WORKFLOW — Instructor-First Notebook Editing  *(hard rule — no exceptions)*

**ANY request to "work on a notebook" means: edit the instructor side first; the
student notebook is only ever a mechanical, answer-stripped copy.** Never edit a
`notebooks/student/*.ipynb` directly.

ALWAYS edit the cell source `_production_kit/nb_sources/nbNN_<slug>.py` (gitignored)
FIRST, then rebuild: `.venv/bin/python scripts/nbbuild.py nbNN` — regenerates the
instructor notebook, executes it with nbclient, strips `INSTRUCTOR SOLUTION`
cells into the student file, runs the template/voice validators, and refreshes
the schedule badge.

- Markers: `### INSTRUCTOR SOLUTION — Exercise N`, `# INSTRUCTOR SOLUTION`,
  `<!-- INSTRUCTOR SOLUTION -->`. Student placeholders: `### YOUR ANSWER HERE:`,
  `# YOUR SOLUTION HERE`.
- Only `notebooks/student/*_student.ipynb` is committed; instructor notebooks and
  `_production_kit/` are gitignored.
- Badges key off git-tracked student files (`scripts/update_schedule_badges.py`).
- **After building, sync the private instructor repo:**
  `scripts/sync_instructor_repo.sh` (backs the password-gated Instructor tab;
  the page password (gitignored `_production_kit/page_password.txt`; request
  by email, never committed) is a courtesy lock — the private repo is the real
  protection).

---

## 🚨 CRITICAL WORKFLOW — Sync Session Guides and Planning Docs

Session guides are GENERATED: edit `scripts/schedule_data/part1–4.py` →
`.venv/bin/python scripts/build_meeting_schedule.py` →
`.venv/bin/python scripts/build_session_guides.py`. Never hand-edit
`planning/MEETING_SCHEDULE.{csv,md}` or `session_guides/*.md`. Significant
sequencing changes also update `planning/COURSE_MASTER_PLAN.md`.

---

## 🚨 CRITICAL WORKFLOW — Commit AND Render Webpage  *(KEEP verbatim)*

Every content change → `quarto render` → commit `docs/` → push. GitHub Pages serves
`docs/`; skipping the render leaves the site stale (the project's most common
mistake).

```bash
git add <changed .qmd or activity>
git commit -m "feat: ..."
/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto render
git add docs/ && git commit -m "build: Render Quarto site"
git push origin main
```

Site pages: `index` / `syllabus` (hand-edited), `material.qmd` + `instructor.qmd`
(generated by `scripts/build_material_page.py`), `schedule.qmd` (generated by
`scripts/update_schedule_badges.py`), the book (rendered from `book/`). The
post-render step encrypts `docs/instructor.html` — never commit an unencrypted
instructor page. Do not hand-edit generated pages.

---

## 🚨 OPTIONAL RULE — MC Option-Length Parity  *(dormant; only if MC quizzes are used)*

If auto-graded MC quizzes are introduced: every option ≥ 60% of the longest
option's length; correct option strictly longest in ≤ 40% of a bank;
`python3 scripts/audit_answer_length.py --file <csv>` must PASS before import.

---

## Style Guidelines

| Setting | Value |
|---|---|
| Money in markdown cells | Always escape: `\$50,000` |
| Tildes in markdown cells | Always escape: `\~30 sources` |
| Emoji vocabulary | `✓` success, `⚠️` warning, `📝` exercise, `💡` insight |

> `SEED = 464` via `np.random.default_rng(SEED)` in every setup cell; all
> simulations deterministic. No seaborn. Python 3.11-compatible; libraries:
> numpy, pandas, matplotlib, scipy, statsmodels, scikit-learn, networkx.

## Naming and Commit Conventions

- Student notebooks (committed): `notebooks/student/nbNN_topic_student.ipynb`
  (nb01–nb16, one per week); milestone studio notebooks `msNN_topic_student.ipynb`.
- Instructor notebooks (gitignored): `notebooks/instructor/…_instructor.ipynb`
- Cell sources (gitignored, canonical for editing): `_production_kit/nb_sources/`
- Milestone briefs: `_research_project/2026Fall/milestone_NN_<slug>.md` (M0–M15)
- Commit messages: `<type>: <subject>` (feat|fix|docs|chore|build|refactor) with a
  trailing `Co-Authored-By:` line. Stage specific files — never `git add .`.

---

**Version:** 5.9 — eighth instructor review round (2026-07-29, DECISIONS.md
D30): AI-generic student-facing voice (Gemini retired from notebooks + 5
chapters; template element renamed "AI Prompt"); agentic-era framing +
brainstorming as a partner role; Friday studio = 10/5/30/5 with the
red-team block RETIRED and milestones WORKED ON (not presented); nb01
restructured (panel explainer, pathways named, partner cell before the
puzzle, book-ch4 never-delegate link, per-code-cell expectation +
"Reading the output" narration — standing rule, exemplar nb01 +
companion generator); syllabus book-first + AI-generated translations.
(5.8 — same-day addendum (2026-07-29, DECISIONS.md D29): one
brand — site sidebar carries the EDR|AI wordmark and the book's neutral
palette (gold retired from styles.css); `nbbuild.py` prepends a generated
logo cell to every built notebook (injected once into existing ones);
AI-image disclosure note under the book image on the main page ×3.
(5.7 — seventh instructor review round (2026-07-29, DECISIONS.md
D28): BOOK_VOICE_POLICY (book must never read as AI-generated; adapted from
mgaldino's rewrite-introduction style guide for the undergrad audience) +
`voice_lint_book.py`; enrollment language banned (self-learning framing
instead); preface restructured ×3 with For students / For instructors /
Languages sections; `description:` blurb removed from the three book
`_quarto.yml`. (5.6 — sixth instructor review round (2026-07-28, DECISIONS.md
D27): pill-button language switcher; designed Part I figure
(`build_book_part1_figure.py`, mermaid retired); part1-overview joins the
banner registry; enriched author page ×3; companion-notebook header spec
(logo + "Authored by Davi Moreira" + no artifact-boundary meta-commentary
rule); badge implicit-figure caption fix ×111; 3D book mockup in the
preface ×3. (5.5 — fifth instructor review round (2026-07-28, DECISIONS.md
D26): For-Instructors appendix password-locked in all three editions
(post-render encryption; password only in gitignored
`_production_kit/page_password.txt`, requested by email, scrubbed from all
committed docs); auto-derived **"It is your turn" rubrics** in every companion
notebook + the locked appendix (`_iyt-rubrics.qmd`); under-development
banners on all 37 chapters driven by `planning/BOOK_REVIEW_STATUS.yml` +
`update_chapter_review_banners.py`; standing seeded-simulation content rule
with first tranche ch11/ch14/ch15 (`build_book_sim_figures.py`); book-funding
search tracked as private course task #17. (5.4 — fourth instructor review
round (2026-07-28, DECISIONS.md
D25): book/course SEPARATION — every chapter gets its OWN companion Colab
notebook (`notebooks/book/`, EN/PT/ES, built by
`scripts/build_book_notebooks.py`; chapter badges repointed; "Colab
laboratory" sections re-anchored); new **For Instructors** appendix (×3
editions) presenting the companion course; milestone briefs M0–M15 carry Book
Anchors collecting the chapters' "It is your turn" sections (submission-table
row added); About the Author moved to right after the Preface; author "Davi
Moreira"; new preface/description blurb ("undergraduates who aspire to produce
high-quality research with scientific impact"); validator extended (companion
links, For-Instructors coverage, localized companions). (5.3 — third
instructor review round (2026-07-27,
D24): the book becomes **EDR|AI — Evidence-Driven Research in the Age of AI**,
a SELF-CONTAINED MANUAL: per-chapter "It is your turn" sections chaining into a
full research artifact (Verification lab / Project transfer / Defend sections
retired; Reading boxes retired; sync-validator elements updated); domains econ
/ political science / business / biology; the AI loop taught from ch. 3;
per-page language switcher; Part I overview page with diagram; appendices:
SRL, Verification Guide, About the Author; site tab "Book: EDR|AI" (new tab);
nb01 = orientation Lecture 1 with ⚙️ Setup section and updated bio. (5.2 —
second instructor review round (2026-07-27,
D23): EDR|AI (then 'EDRAI') acronym + book-first loop (notebooks reflect the book; instructor
reviews the book; assistant propagates; institution-agnostic body), EDR|AI
required / RDSS recommended reading model, PT-BR + ES book translations
(book-pt/, book-es/ — EN is source of truth), AI-reviews-AI-human-decides
callouts, provenance metadata lines + "all positions" tags retired from
notebooks, upgraded claim standard, professor intro opening nb01, syllabus
de-policying. (5.1 — first instructor review round (2026-07-27, D22):
week-aligned numbering nb01–nb16, random SRL slots with notebook-embedded
student-visible SRL Lead Briefs, quiz-first Fridays (10-min printed MC quiz;
`_quizzes/2026Fall/weekly/`), confirmed assessment weights, course book
retitled (now EDR|AI, D24) (work in progress) with the SRL
appendix. (5.0 = v2 prompt-architecture rebuild 2026-07-22/23, D17–D21: 16
weekly topics, milestones M0–M15, SRL flipped classroom, AI Research Ledger +
SDIIVDD, GenAI Studio reviewer bench, 37-chapter course book, 43-meeting
calendar; 4.0 = 2026-07-20 course redesign D13–D16; 3.0 = RDSS inquiry compass
2026-07-19; 2.0 = v1 build complete; 1.0 = seeded from MGMT474 infra.)))))))))
**Maintained by:** Professor Davi Moreira + AI Assistants
