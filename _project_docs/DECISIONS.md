> **Registry status (2026-07-23).** D1–D11 are legacy seeds from MGMT474: D2/D3/D9
> are DROPPED for HONR 46400, D10 is superseded by D14, the rest survive only where
> restated below or in CLAUDE.md. D12–D16 are the 2026-07-19/20 HONR rulings; parts
> of D12 (sequencing) and D13 (Friday section format) are superseded by **D17**.
> D17–D21 (2026-07-22/23) govern the current v2 build. The full v1 build is
> preserved at git tag `v1-compass-build`.

# Course Design Decisions

This document records design decisions made during course development and the reasoning behind them. Decisions here are **load-bearing** — changing them requires deliberate review, not casual edits. New AI assistants and contributors should read this to understand WHY conventions exist before proposing changes.

---

## Decision 1: Flat Notebook Structure

**Decision:** All 21 notebooks live in `/notebooks/` (flat, not nested by week).

**Rationale:**
- Easier to link/reference (simple URLs).
- Clear sequential numbering (`nb00`–`nb20`).
- Students navigate linearly through days.
- GitHub displays flat lists better than nested directories.

---

## Decision 2: 60/20/20 Split for All Examples

**Decision:** Always use 60% train, 20% validation, 20% test.

**Rationale:**
- Consistency across all 21 notebooks.
- Students learn ONE splitting pattern.
- Sufficient validation data for tuning.
- Realistic test set size for course-scale datasets.

---

## Decision 3: `RANDOM_SEED = 474` Everywhere

**Decision:** All random operations use seed 474 (the course number, QM47400).

**Rationale:**
- Complete reproducibility — students get identical outputs.
- Easier to debug — same results every time.
- Course-specific seed (not the generic `42`).
- Memorable for students.

---

## Decision 4: Google Colab + Gemini (Not Local Jupyter)

**Decision:** Primary platform is Google Colab; AI assistance is Google Gemini.

**Rationale:**
- Zero setup for students (no installation issues).
- Consistent environment (same Python/library versions across all students).
- Built-in GPU access (for the deep-learning day).
- Gemini AI assistance integrated natively.
- Accessible from any device.

**Implication for notebook design:** Code must run in a fresh Colab runtime. No hardcoded local paths. Imports must be standard scientific-Python or pip-installable on first cell.

---

## Decision 5: Exclude Admin Materials from Git

**Decision:** `_adm_stuff/` is in `.gitignore`. Instructor notebooks (`*_instructor*.ipynb`) and `video_guides/` are also gitignored.

**Rationale:**
- Student privacy (contact info, accommodations).
- Sensitive data (grades, evaluations).
- Large files (homework solutions, zip archives).
- Public repo — cannot include private materials.
- Instructor solutions must not leak to students browsing the repo.

---

## Decision 6: Micro-Videos (≤12 min each)

**Decision:** All videos capped at 12 minutes maximum.

**Rationale:**
- Attention-span research suggests 10–15 min is optimal for instructional video.
- Mobile-friendly (students can watch on phone).
- Easy to re-watch specific topics.
- Forces concise, focused content.
- ~6 videos per day = ~1 hour total video, leaving time for hands-on notebook work.

---

## Decision 7: "PAUSE-AND-DO" (Not "Exercise" or "Assignment")

**Decision:** Use "PAUSE-AND-DO" terminology for the 10-minute in-notebook practice blocks.

**Rationale:**
- Clear action signal — pause the video, do this now.
- Distinguishes from graded assignments (which are separate).
- Emphasizes active learning over passive reading.
- 10-minute scope — not homework, not a project.
- Builds an engagement habit across all 21 notebooks.

---

## Decision 8: Instructor-First Notebook Editing Workflow

**Decision:** The instructor notebook (`nbNN_*_instructor.ipynb`) is the source of truth. The student notebook (`nbNN_*_student.ipynb`) is generated from it by copy-then-strip-`INSTRUCTOR SOLUTION`-cells.

**Rationale:**
- Single source of truth — solutions and student version cannot drift.
- Solutions live next to the prompts they answer (easier to maintain).
- Student notebook is generated, never hand-edited; this guarantees the student version is always derivable.
- Allows last-minute solution polish without re-writing the student version separately.

**Implication:** Every cell that should be excluded from the student version MUST contain the literal string `INSTRUCTOR SOLUTION`. The strip script keys on this marker. Unmarked solution cells leak into the student notebook.

---

## Decision 9: CV-First Evaluation, Test-Set Locked Until nb14

**Decision:** From `nb09` onward, all model-performance claims come from cross-validation. The test set (`X_test`, `y_test`) is locked — no model evaluation touches it until `nb14`'s "Opening the Locked Test Set" ceremony.

**Rationale:**
- The test-set-lock ceremony in nb14 is pedagogically central. If the test set is touched 30 times beforehand, the ceremony loses meaning.
- Cross-validation is the professionally honest evaluation method; the course teaches it as the spine.
- Students learn that "I peeked at the test set 30 times before reporting accuracy" is the most common subtle leak in industry.

**Exceptions:**
- `nb14` cell 33 only — the one authorized test-set opening.
- `nb18` Kaggle-submission demo — uses `X_test` to simulate predicting on a held-out CSV (production-pipeline pattern, not model evaluation).

**Implication:** Before every commit in `nb09`–`nb20`, run `scripts/audit_cv_first.py`. The only acceptable hits are the nb14/nb18 exceptions.

---

## Decision 10: Narrative Polish Pattern (nb08 Style)

**Decision:** Every student-notebook markdown cell follows the nb08 narrative style — named business stakeholder in "Why This Matters", flowing prose over bullet lists, inline `"A question that often comes up here"` Q&A blocks, explicit section bridges, warm wrap-ups bridging to the next notebook.

**Rationale:**
- Students read notebooks alone, often late at night. The voice must be encouraging and complete, not skeletal.
- Named stakeholders (HomeValue CFO, MedScreen chief medical officer) make business framing concrete instead of abstract.
- Inline Q&A pre-empts the most common confusions, reducing "I'm stuck and don't know what to ask" moments.
- The `"A question that often comes up here"` phrase is grep-findable for tooling and audits.

**Implication:** New markdown cells longer than ~150 words should be checked against the polish pattern before commit. See `CLAUDE.md` for the polish helper script and the audit checklist.

---

## Decision 11: MC Option-Length Parity in All Assessments

**Decision:** In every multiple-choice question (quizzes, midterm, any future exam), all options must sit in the same length-and-elaboration band: every option ≥ 60% of the question's longest option, and per bank the correct option is strictly longest in ≤ 40% of questions (target ~25%, chance). Distractors carry their own flawed-but-specific rationale at the correct option's elaboration and connector-word density.

**Rationale:**
- In 2026Summer, correct options were authored as full decisions-with-rationale while distractors stayed terse. Two students independently reported (extra-credit program, 2026-06-12) that "always pick the longest option" scored ~100%. Hypothesis tests confirmed it: correct-is-longest in 96% of quiz questions (250 analyzed) and 99.5% of midterm questions (210 analyzed) vs. 25% chance, p < 10⁻¹²³; the midterm's connector-word density showed the same cue.
- Length-balanced, equally-elaborated distractors restore the assessments' validity: the only way to eliminate an option is to recognize the misconception it encodes.

**Exceptions:** none. Numeric/label options satisfy the band by formatting all options in the same shape (e.g., `k = 2` / `k = 100`).

**Implication:** Before importing any quiz/exam CSV to Brightspace, run `python scripts/audit_answer_length.py --file <csv>` — PASS is mandatory. Authoring spec: `scripts/_distractor_rewrite_instructions.md`; per-bank rules embedded in `_quizzes/2026Summer/quiz_generation_plan.md` §4.5 and `_midterm_exam/2026Summer/midterm_generation_plan.md` §5.6. All 48 quiz CSVs and 14 midterm case CSVs were rewritten to this standard on 2026-06-12.

---

## Decision 12: Adopt the RDSS Taxonomy Outright — the Inquiry Compass (2026-07-19)

**Decision:** Retire the four-approach grid (description / statistical inference /
predictive modeling / causal reasoning) as the course's classification scheme and
adopt the book's own taxonomy: every research question is classified by **kind**
(descriptive vs causal inquiry, RDSS ch. 7) and **reach** (the data at hand / a
population beyond the data / cases not yet seen) — branded in course materials as
the **inquiry compass**. The four deep-dive modules survive as named compass
positions: Description (nb06, descriptive · data at hand), **Generalization**
(nb10, descriptive · population — renames "statistical/observational inference"),
Prediction (nb12, descriptive · unseen cases), Causal reasoning (nb13, causal
kind). MIDA + diagnosis remain the cross-cutting machinery.

**Rationale:**
- The old grid stood *beside* the textbook's taxonomy: students read RDSS ch. 7's
  two-family split while the course taught four families, with no student-facing
  reconciliation. Deriving the positions from kind × reach makes the course and
  its book one system.
- The claim-boundary drills survive stronger: every overclaim is now a **compass
  crossing without its license** — sample→population licensed by a sampling data
  strategy (violation: the silent upgrade), observed→unseen licensed by
  prediction-time honesty + held-out diagnosands (violation: leakage),
  descriptive→causal licensed by assignment/identification (violations:
  after-therefore-because, design mimicry). "You buy kind and reach with your
  data strategy, and you prove the purchase with diagnosis."
- Prediction gets an honest textbook home: nb12 authors the design-library entry
  RDSS stops short of — "Observational: predictive" — in the book's own
  declare-diagnose-redesign format (I = target for unseen units; leakage = a
  data-strategy violation; held-out performance = a diagnosand; baseline
  comparison = redesign).
- EDA is taught as the **explore → declare → confirm loop**, not a topic:
  upstream M-calibration (nb04), the named anchor (nb06), the §9.1.3
  whole-procedure rule (nb09), and ch. 22 pivoting/reconciliation (nb17).

**Implication:** `course_config.yaml` now carries `inquiry_framework:` (replacing
`approaches:`); `planning/INQUIRY_MAP.md` (renamed from QUANTITATIVE_APPROACH_MAP)
is canonical; the notebook template block is `## 🧭 Inquiry & Claim Boundary` with
`**Inquiry emphasis:**` (validator updated); the schedule column is `inquiry`
(renamed from `approach`); the student template is
`project/templates/INQUIRY_DECLARATION.md` with kind/reach checkboxes and a
crossing-licenses table; the CLAUDE.md critical rule is "Inquiry-Declaration
Justification". Notebook filenames (e.g., `nb02_four_approaches*`) were kept for
link stability — display titles changed everywhere.

---

## Decision 13: Friday Studios + Phase 1–2 Compression (2026-07-20)

**Decision:** Every Friday is a **studio**: ≈10 min topic recap + ≈10 min
instructor presentation of the next project milestone (from its Brightspace
brief) + ≈30 min supervised milestone/project work with rotating consults. No
new topic content on Fridays. Simultaneously, Phases 1–2 compress from 14
meetings to ~10: P1 = M1–M4 (nb00=1, nb01=2 lectures), P2 = M5–M11 (nb02–nb05
one lecture each), with Phase 2 content ending Wed Sep 16 (week 4). Freed slots
flow to Phase 3 (now M12–M22: nb06=1, nb07/nb09/nb10 two lectures each). nb08
becomes the async Friday-studio module (Oct 2, M05 work day). Every milestone is
kicked off on a Friday; three due dates moved (M00 Aug 26→Aug 28, M03 Sep
16→Sep 18, M05 Oct 7→Oct 2); hard anchors (M07 Oct 9/16, M12 Nov 6, M16 Nov 17,
M22 Dec 7/9, M23 Dec 11) unchanged.

**Rationale:** The prior calendar front-loaded question-formulation and
literature/measurement (32% of the semester) while layering milestone
presentations on top of new Friday content. A fixed weekly rhythm — learn
Mon/Wed, consolidate and build the project Fri — protects project time,
makes milestone expectations explicit, and moves students into the technical
phases (data, answer strategies, diagnosis) a week earlier.

**Implication:** `scripts/schedule_data/part1–4.py` rewritten; lecture labels
derived via `lecture_labels()` in `scripts/notebooks_map.py`; session guides and
notebooks reference lectures (never meetings or dates).

---

## Decision 14: Undergraduate-Friendly Voice (2026-07-20 — supersedes D10's punctuation habits)

**Decision:** Keep D10's narrative machinery (named-stakeholder "Why This
Matters" openers, "A question that often comes up here" Q&A blocks, prose over
bullets, bridges, warm wrap-ups) but enforce an undergraduate-friendly voice:
em-dashes ≤ 20 per notebook and ≤ 1 per markdown cell; every technical term
introduced as bold term → one-sentence plain definition → concrete example;
sentences ~12–25 words; second person throughout; no fourth-wall meta-references
about how the material was constructed.

**Rationale:** The built notebooks averaged ~2 em-dashes per markdown cell and
introduced compass/RDSS jargon without plain-language onboarding — reading as
AI-generated and taxing for honors students with no quantitative background.
MGMT474's student notebooks (the course's infra ancestor) demonstrate the
target: same pedagogy, restrained punctuation, term-definition-example rhythm.

**Implication:** `scripts/voice_lint_notebooks.py` gains an em-dash budget,
banned meta-phrases, and date-pattern checks; `_project_docs/ACTIVITY_TEMPLATE.md`
§5 rewritten; all 20 notebook sources rewritten and rebuilt.

---

## Decision 15: Material/Schedule Split, Dataset Zip, Password-Gated Instructor Tab (2026-07-20)

**Decision:** The site splits into **Material** (topic-indexed: notebook Colab
badge, dataset zip, readings — generated by `scripts/build_material_page.py`)
and **Schedule** (date-indexed calendar) tabs, QM670-style. All datasets live in
`notebooks/data/` and ship as one bundle `notebooks/data/honr46400_datasets.zip`
(regenerated by `scripts/make_dataset_zip.py`), linked from both pages. A new
**Instructor** tab is client-side encrypted (password held in gitignored
`_production_kit/page_password.txt` since D26,
`scripts/protect_instructor_page.py`, wired post-render) and lists Colab badges
pointing at the private repo
`davi-moreira/2026F_evidence_driven_research_purdue_HONR464_instructor`, synced
by `scripts/sync_instructor_repo.sh` from gitignored local material.

**Rationale:** Students need a stable topic-indexed resource catalog separate
from the calendar; a single zip is the offline data path; the instructor needs
the same one-click Colab access to solution notebooks without ever committing
them to the public repo. The page password is a courtesy lock — the private repo
plus GitHub auth is the real protection.

---

## Decision 16: Fabricated Citations Removed Course-Wide (2026-07-20)

**Decision:** The planted-fake-citation teaching device (previously nb00, nb03,
nb08, nb15) is removed entirely. Citation-verification skills are taught with
real, retrievable sources that students locate and confirm. `scripts/audit_sources.py`
now treats the former planted-fake names as a hard blocklist with no disclosure
exemption.

**Rationale:** The device required fourth-wall meta-asides ("fabricated for the
verification exercise") that undercut the course's own evidence-integrity spine
and read as AI-generated filler. Verifying real sources exercises the same
skill without shipping fakes in student material.

---

## Decision 17: Prompt-Architecture Rebuild — the v2 Course (2026-07-22, instructor ruling)

**Decision:** The instructor's Fall 2026 master prompt governs the course
architecture. The course is rebuilt as **16 weekly topics (nb00–nb15, one
notebook per week)** over a **43-meeting calendar** (41 in-person + 2 async;
NO class Wed Nov 18, the day after the Expo), with **milestones M0–M15**.
Weeks 5–9 follow the DeclareDesign design library (RDSS ch. 15–18): one week
each for observational descriptive, observational causal, experimental
descriptive, prediction, and experimental causal designs — prediction treated
as its own answer objective, never forced into either grid. The **inquiry
compass (RDSS ch. 7) is retained as the question-classification layer**
(taught Week 2, used in every declaration); the retired four-approach grid
does NOT return. Friday studios adopt the four-section format: stand-up /
milestone kickoff + AI sprint / peer + AI red-team / revise + submit.

**Rationale:** The instructor ruled (2026-07-22) that the new prompt's
architecture must govern and new material be developed. RDSS carries both
layers natively (ch. 7 for questions, ch. 14–19 for designs), so the compass
and the pathway weeks are one system, not competitors.

**Implication:** Supersedes D12's notebook sequencing (compass concepts and
claim-boundary machinery survive) and D13's Friday section format (the
studio-Friday principle — no new topic content on Fridays — survives). All 20
v1 notebooks, 24 v1 milestone briefs, and the 44-meeting schedule are replaced;
v1 is preserved at tag `v1-compass-build` and mined per
`planning/SOURCE_AUDIT_V2.md` §7.

---

## Decision 18: Flipped Classroom — the Student Research Lead System (2026-07-22)

**Decision:** Every Mon/Wed lecture from Week 2 onward is led by a **Student
Research Lead (SRL)** running a Socratic investigation (never a summary
presentation): a concrete puzzle first, prior beliefs elicited, commitment
before AI, directed Gemini use, human-vs-AI comparison, assumption probing,
revision, and a closing defense. 25 lead slots ÷ 5 students = 5 leads each,
assigned by rotation seats A–E in the schedule data. The 50-minute classes use
fixed four-section architectures (Mon 9/22/12/7; Wed 7/23/12/8) enforced by
the session-guide generator. SRL performance is graded on a rubric
(conceptual correctness, Socratic quality, assumption exposure, productive AI
use, AI interrogation, inclusion, time management, connection to research
decisions, handling uncertainty).

**Rationale:** The master prompt's central pedagogy; with a 5-person honors
seminar, frequent leading is feasible and rehearses exactly the skills the
Expo and the final defense assess.

**Implication:** `scripts/schedule_data/` carries `srl_slot` + `srl_focus`
per lecture; the SRL handbook/templates/rubric live in `project/srl/`;
Week 1's two lectures stay instructor-led to model the format.

---

## Decision 19: AI Stack — Gemini Primary, GenAI Studio Reviewer Bench (2026-07-22)

**Decision:** Google Gemini (in/alongside Colab) remains the embedded
in-notebook research assistant; all prompts are REWRITTEN for the v2 material.
**Purdue GenAI Studio** (genai.rcac.purdue.edu) is built out as the course's
reviewer bench: custom role models (base model + system prompt + course
knowledge base), shared via a course group, with required milestone
touchpoints (M5 Causal Identification Skeptic; M7 Prediction & Leakage
Auditor; M9 Poster Critic + Robustness & Sensitivity Reviewer; M13
Reproducibility Auditor) and an OpenAI-compatible-API Colab proof-of-concept
(Colab Secrets, never keys in code; manual-UI fallback is a first-class path).
Materials use the six-level taxonomy (prompted role → custom model → RAG
assistant → sequential multi-role workflow → autonomous agent → multi-agent
orchestration) and implement GenAI Studio only at levels 1–4 — it has NO
native agents and materials never claim otherwise.

**Rationale:** Rewriting 84 working Gemini prompts to a different primary tool
buys nothing; GenAI Studio's verified capabilities (custom models, RAG KBs,
groups, multi-model comparison, OpenAI-compatible API) map exactly onto the
reviewer-role pedagogy and the model-disagreement lessons.

**Implication:** Role specs + KB strategy + PoC live in `genai_studio/`;
student access must be verified by the instructor before the semester (open
item); the SDIIVDD discipline (Specify → Delegate → Interrogate → Inspect →
Verify → Document → Defend) becomes the course's full AI-collaboration loop
with Ask → Verify → Document as its everyday shorthand.

---

## Decision 20: The Course Book — 37 Chapters, Six Parts (2026-07-22)

**Decision:** Build the full 37-chapter open-access Quarto book ("Evidence-
Driven Research: How to Design, Analyze, Verify, and Defend Empirical
Research") in `book/`, rendered into `docs/book/` with a site Book tab.
Chapters synchronize with the v2 notebooks + site (Part I ↔ nb00; II ↔
nb01–03; III ↔ nb04–08; IV ↔ nb07–09 + cross-cutting; V ↔ nb10–12; VI ↔
nb13–15), each carrying: the research decision, conceptual explanation, a
STEM worked example, a Colab lab link, recommended AI prompts, a "Do not
delegate" box, an AI failure case, a verification lab, project transfer, and
a defend-your-decision activity. RDSS remains the assigned theory text.

**Rationale:** Instructor ruling (2026-07-22): full book, synchronized with
the new notebooks and site. Building it AFTER the notebooks stabilize keeps
one source of truth; `scripts/validate_book_sync.py` enforces chapter↔notebook
links both ways.

---

## Decision 21: The AI Research Ledger (2026-07-22)

**Decision:** The v1 "AI-use ledger" habit and per-deliverable disclosure
block are unified into ONE structured artifact: the **AI Research Ledger**,
with fixed fields (task delegated · tool used · prompt · output summary ·
decision · verification method · remaining concern · responsible researcher).
Every notebook carries a ledger-entry block; every milestone submission
appends to the student's cumulative ledger inside the Research Project
Dossier. The claim ledger (claims, evidence, verification, boundaries)
remains a DISTINCT instrument: the claim ledger tracks what the research
asserts; the AI Research Ledger tracks what AI did and how it was checked.
Missing ledger entries keep the v1 penalty: the rubric's Craft criterion
scores 0 and the submission is returned.

**Rationale:** One named artifact, taught on day 1 and audited at every
milestone, turns the responsible-AI-use rule from a habit into a graded,
inspectable record — and gives the M13 red-team and M15 portfolio their
primary source.

---

## Decision 22: Week-aligned numbering, quiz-first Fridays, notebook-embedded SRL briefs, confirmed assessment (2026-07-27)

**Decision:** Instructor ruling, seven parts.
1. **Renumbering:** the weekly topic notebooks run `nb01`–`nb16` so the week
   number always equals the notebook number (formerly `nb00`–`nb15`; files,
   registry keys, Topic NN headers, book links, and planning docs all shifted;
   milestones keep M0–M15 and studio notebooks keep ms00–ms15).
2. **SRL assignment:** lead slots are randomly assigned at the start of the
   semester — the seat A–E rotation is retired. No student-facing "five times"
   promise; no five-day SRL-page release.
3. **SRL briefs:** each lecture's SRL guidance is a STUDENT-VISIBLE
   `### 🎤 SRL Lead Brief` cell opening that lecture in its notebook (after
   `# Lecture N`, before the 🧩 Research Puzzle). The old instructor-only "SRL
   page" cells are retired. Briefs must be simple to follow, and must leave
   explicit room for the lead's own staging ("the brief is a floor, not a
   ceiling"). The voice linter allow-lists the exact role name
   "Student Research Lead"/"Student-led" (proper noun, not third-person voice).
   The SRL guide is also a course-book appendix (`book/srl.qmd`).
4. **Friday studios are quiz-first:** 0–10 weekly multiple-choice topic quiz
   (printed, solo, graded) · 10–15 stand-up · 15–32 milestone kickoff +
   AI-supported sprint · 32–42 peer + AI red-team review · 42–50 revise,
   ledger, submit. Quiz masters + keys + D2L banks: `_quizzes/2026Fall/weekly/`
   (gate: `scripts/audit_answer_length.py --file`).
5. **Assessment (confirmed):** Lecture Notebook Completion 10 · Quizzes 20 ·
   SRL performance 20 · Final Project Milestones 20 · Final Project 20 ·
   Research artifact (paper/chapter/note) 10.
6. **Course book:** retitled "Evidence-Driven Research in AI-era: How to
   Design, Analyze, Verify, and Defend"; presented as a work in progress under
   development across the semester.
7. **Site:** course description replaced verbatim (no bold); learning outcomes
   mirror it; the AI-tagline blockquote, async/no-class bullets, midterm/exam
   sentence, revision-policy block, and Milestone Chain section are off the
   home/syllabus pages — the milestone chain and weekly architecture now live
   in nb01 Lecture 1 (dateless; dates stay on Schedule). The tagline drops its
   em dash: "your arm, your RA, not your brain."

**Rationale:** Instructor review of the v2 build (2026-07-27): align numbering
with weeks for student legibility; make the SRL system simpler, public, and
creative; add weekly retrieval practice with a graded quiz; settle grading
weights; de-clutter the public pages while keeping operational detail in the
first notebook, the book appendix, and the schedule.

---

## Decision 23: EDRAI book-first loop, agnostic book, translations, notebook de-cluttering (2026-07-27)

**Decision:** Instructor ruling, second review round.
1. **EDRAI.** The course book's acronym is **EDRAI** (*Evidence-Driven Research
   in AI-era: How to Design, Analyze, Verify, and Defend*). Reading model:
   **EDRAI chapters are the required reading; the matching RDSS chapters are
   recommended** — EDRAI exists to translate RDSS to the econ/STEM/business
   undergraduate audience. Every chapter carries a Reading box naming its RDSS
   companions, and a verification-section callout stating: **AI can review AI,
   but the last decision is always human.** The Book tab opens in a new tab.
2. **The book-first loop.** Going forward: (a) notebook content must reflect
   the book; (b) the instructor manually reviews and updates the book; (c) the
   assistant then articulates and incorporates those reviews across the course
   material (notebooks, guides, site); (d) the book stays
   **institution-agnostic** (usable by instructors/students outside Purdue —
   generic "course platform", "AI reviewer bench", "your research conference"
   phrasing in chapter bodies; Purdue specifics only as parentheticals).
3. **Translations.** EDRAI ships in Brazilian Portuguese (`book-pt/` →
   `docs/book-pt`) and Spanish (`book-es/` → `docs/book-es`). The English
   edition is the source of truth; translations are regenerated from it after
   EN edits. Render all three books on any book change.
4. **Notebook de-cluttering.** The vacuous "all positions (…)" inquiry-emphasis
   tags and the pipe-separated build-provenance metadata lines are retired from
   student-facing cells (validator updated; the end-of-notebook Sources &
   Provenance section stays). The course's opening claim standard is now: "An
   AI tool generated this, the source exists, and I read, confirmed, and
   criticized the underlying argument or technique before using it."
5. **nb01 welcome.** The first notebook opens Lecture 1 with the professor's
   introduction (bio, Palmeiras, Carnaval de Olinda; images in
   `images/professor/`), mirroring the MGMT305 opening-lecture format.
6. **Syllabus de-policying.** The late-policy line and the Poster & Conference
   and Reproducibility policy sections are removed from the syllabus page
   (reproducibility remains enforced through milestones and notebooks).

**Rationale:** Instructor review 2026-07-27 (second round): make the book the
reviewable center of the course with a clear propagation loop, open it to
audiences beyond Purdue (including PT-BR/ES readers), tighten the student
notebooks to content that serves the reader, and raise the claim standard from
"the source exists" to "I read, confirmed, and criticized it."

---

## Decision 24: EDR|AI — the self-contained manual (2026-07-27, third review round)

**Decision:** Instructor ruling.
1. **Title/brand:** the book is **EDR|AI — Evidence-Driven Research in the Age
   of AI** (subtitle: How to Design, Analyze, Verify, and Defend) in all three
   languages; the site tab reads "Book: EDR|AI" and opens in a new tab.
2. **Self-contained manual:** chapter bodies carry NO course furniture
   (milestones, studios, quizzes, rubrics, "this course"). The three closing
   sections (Verification laboratory · Project transfer · Defend your
   decision) are replaced by ONE final **"It is your turn"** section per
   chapter; the 37 sections chain into a complete research project and a draft
   research artifact by the end of the book. Sync-validator element set
   updated accordingly.
3. **Domains:** worked examples come from econ, political science, business,
   and biology, at undergraduate level, in a friendly first-person-researcher
   register (the ch. 2 "run the assay… that part is mine" passage is the
   exemplar).
4. **The AI loop:** the book teaches AI use as a LOOP (prompt → output →
   interrogate → refine → run again; agentic tools run loops autonomously),
   formally introduced in ch. 3 with SDIIVDD as the checklist that governs
   every cycle; chs. 19–20 and 35–36 build on it.
5. **Apparatus:** in-chapter Reading boxes retired; the verification guide is
   now a book APPENDIX (book/verification-guide.qmd, from
   ai_resources/verification_guide.md) and all chapter links point at it; new
   appendices: About the Author; Part I opens with an overview page + mermaid
   diagram of the book's arc; Part I retitled 'Research when AI does
   "everything"'; every book page carries a language switcher (EN · PT-BR ·
   ES) via include-before-body.
6. **nb01:** an explicit ⚙️ Setup section (setup + readiness + AI Research
   Partner) precedes Lecture 1; Lecture 1 is the orientation lecture
   (professor intro with updated title line — Quantitative Methods Department,
   Director of the Daniels Undergraduate Business Honors Program — student
   intros, course at a glance, weekly rhythm + milestone chain, grading,
   materials/logistics, questions), with the SRL Lead Brief and Research
   Puzzle moved after orientation.

**Rationale:** make EDR|AI a book that stands entirely on its own — a manual
any student anywhere can follow to a finished, defensible research artifact —
while the course wraps around it, not the other way round.

## Decision 25: Book/course separation — companion notebooks, For Instructors, book-anchored milestones (2026-07-28, fourth review round)

**Decision:** Instructor ruling. The book and the course are DIFFERENT
artifacts, coupled only through the book-first loop.

1. **The book owns its notebooks:** every chapter has its own companion Colab
   notebook (`notebooks/book/chNN_<slug>.ipynb`, plus `pt/` and `es/`
   editions), generated from the chapter sources by
   `scripts/build_book_notebooks.py` (rerun after any chapter edit). The
   chapter badge opens the companion notebook — a reader runs the chapter's
   code and completes its "It is your turn" section there, with no course.
   Each chapter's "Colab laboratory" section introduces the companion notebook
   first, then names the classroom lab (course notebook nbNN) as
   companion-course material with an inline Colab link.
2. **The course refers to the book:** (a) readings — EDR|AI chapters required,
   RDSS recommended (unchanged); (b) course notebooks derive from the book's
   chapters (lecture structure/dynamics unchanged); (c) every milestone brief
   M0–M15 carries a "Book Anchor — It Is Your Turn" section + submission-table
   row: students complete and submit the anchored chapters' "It is your turn"
   sections (milestone NN anchors the chapters whose primary lab is
   nb(NN+1); the 16 anchors partition all 37 chapters).
3. **For Instructors appendix** (`for-instructors.qmd`, all three editions):
   presents the companion course and makes its material available — the
   two-artifacts model, the weekly SRL/studio architecture, the milestone
   chain, and a table of all 16 course labs with their chapters and Colab
   links.
4. **Front matter:** About the Author moves from the appendices to directly
   AFTER the Preface (unnumbered page); book author is "Davi Moreira" (no
   title); new preface/description blurb — "an open research manual for
   undergraduates who aspire to produce high-quality research with scientific
   impact…" (domains list and "A work in progress" dropped from the blurb; the
   in-preface work-in-progress callout stays).
5. **Validator:** `validate_book_sync.py` now also requires each chapter to
   link its companion notebook, the For-instructors appendix to exist in all
   three editions and link all 16 labs, and PT/ES chapters to link their
   localized companions.

**Rationale:** a reader anywhere can complete the whole manual from the
chapter badges alone, while the course consumes the book (readings, derived
labs, milestone-collected "It is your turn" chains) and the book presents the
course to instructors — separation with an explicit, validated interface.

## Decision 26: Locked instructor area, IYT rubrics, review banners, seeded simulations (2026-07-28, fifth review round)

**Decision:** Instructor ruling.
1. **The For-Instructors appendix is password-locked** in all three editions:
   `protect_instructor_page.py` (now a multi-page registry) AES-GCM-encrypts
   `docs/book*/for-instructors.html` at each book's post-render, alongside the
   site's `docs/instructor.html`; the gate page tells visitors to request the
   password by email (dcordeir@purdue.edu). The password is NEVER released:
   it now lives ONLY in gitignored `_production_kit/page_password.txt` (or env
   `HONR_INSTRUCTOR_PASSWORD`); the script has no default, and the literal was
   scrubbed from all committed docs. (Caveat recorded: the old literal exists
   in public git history from the pre-D26 era; rotating it is Davi's call.)
2. **Every "It is your turn" section has a grading rubric**, generated by
   `build_book_notebooks.py`: one 0/1/2 row per step (criterion = the step's
   first sentence) plus a standing craft-and-verification row. Released in
   BOTH places: a rubric cell in the chapter's companion notebook (students
   see exactly what is graded) and `<edition>/_iyt-rubrics.qmd`, included at
   the end of the locked For-Instructors appendix for grading.
3. **Under-development banners:** while the book is in development, every
   chapter opens with a localized `.review-pending` warning callout. The
   registry `planning/BOOK_REVIEW_STATUS.yml` tracks per-chapter review; when
   Davi reports a chapter reviewed, flip its flag, run
   `scripts/update_chapter_review_banners.py` (idempotent, all three
   editions), and re-render.
4. **Seeded visual simulations (standing content rule):** whenever possible,
   chapters embed code that generates a seeded (SEED=464) simulation visually
   presenting the concept — code block + pre-generated figure in the chapter
   (figures built offline by `scripts/build_book_sim_figures.py` with
   localized labels; no render-time execution), automatically flowing into
   the companion notebook as runnable cells. First tranche shipped: ch11
   (random vs convenience sampling), ch14 (overfitting, train vs holdout),
   ch15 (randomization distribution). Extend chapter-by-chapter as the
   review advances.
5. **Book publication funding:** tracked as course task issue #17 in the
   private companion repo (Innovation Hub AI-in-Teaching grants as best fit;
   Libraries/Press, Honors College, Daniels School as parallel routes).

**Rationale:** give the course-facing half of the book real (if courteous)
access control with graded instruments inside it; make the development status
honest to readers and trackable for review; and make the book's concepts
visible, not just stated — reproducibly, in the reader's own hands.

## Decision 27: Book polish — switcher, Part I figure, author page, notebook header spec (2026-07-28, sixth review round)

**Decision:** Instructor ruling.
1. **Language switcher** rebuilt as pill buttons (bordered, hover state,
   active edition filled dark and non-clickable); one `_lang-switcher.html`
   copied identically to the three editions.
2. **Part I figure**: the mermaid flowchart is retired; the overview page
   embeds a designed monochrome figure (cover aesthetic) generated by
   `scripts/build_book_part1_figure.py` → `<edition>/images/part1_arc.png`,
   localized ×3.
3. **part1-overview carries the under-development banner** like every
   chapter: `update_chapter_review_banners.py` gained an EXTRA_PAGES list and
   the registry a `part1_overview` key.
4. **Author page enriched** from davi-moreira.github.io: applied-data-science
   span, prior appointments (UFPE; visiting at Emory and UC San Diego GPS),
   2017 best Brazilian PolSci/IR dissertation prize, what he does at Purdue
   now; ×3 editions.
5. **Companion-notebook header spec**: EDR|AI logo (site URL, width 300)
   above the title · "Authored by Davi Moreira" linking to the book ·
   companion line · links · the one rule. The sentence "It belongs to the
   book, not to any course…" is REMOVED, and the standing rule is: **no
   artifact-boundary meta-commentary in reader-facing content** (never tell
   readers what an artifact is NOT part of).
6. **Badge caption fix**: chapter badges rewritten to
   `[![](badge){fig-alt="Open In Colab"}](url)` so Pandoc's implicit-figure
   rule stops printing a stray "Open In Colab" caption under the badge (×111).
7. **Preface shows the book**: `images/edrai_book.png` (3D mockup) embedded
   after the work-in-progress callout ×3; the flat cover
   (`edrai_cover.png`) remains the Quarto cover-image.

**Rationale:** presentation polish round — the book should look like the
object on its own cover: designed, consistent, and free of generator
artifacts.

## Decision 28: The book voice policy + preface restructure (2026-07-29, seventh review round)

**Decision:** Instructor ruling.
1. **Voice policy:** the book must never read as AI-generated. The policy is
   `_project_docs/BOOK_VOICE_POLICY.md`, adapted for the undergraduate
   audience from the "rewrite-introduction" style guide
   (github.com/mgaldino/agents-workflow). The book's teaching devices
   (second person, stakeholder openers, Q&A blocks, bold term → definition →
   example) STAY; the tells go: contrast-formula defaults, pivot-word
   accumulation, typographic emphasis, default triads/symmetry, generic
   smart phrases, vague upgrade words, synthetic endings, filler, inserted
   transitions, empty compression. Mechanical subset enforced by
   `scripts/voice_lint_book.py` (per-language tell lists; warnings by
   default, `--strict` on newly written prose; baseline: 129/129 files
   clean). New prose is drafted under the policy; existing chapters are
   swept as Davi reviews them (banner workflow); PT/ES follow EN.
2. **Enrollment language banned:** never state that a reader "does not need
   to be enrolled in a course"; frame the book positively as a self-learning
   resource instead. All existing instances swept (preface ×3, For
   Instructors ×3).
3. **Preface restructured ×3:** opening (what the book is, the one message,
   six parts + RDSS) → **For students** (chapter anatomy, companion
   notebooks, the It-is-your-turn chain, self-learning) → **For
   instructors** (condensed pointer to the locked appendix, password by
   email) → **Languages**. The `description:` blurb was REMOVED from the
   three `_quarto.yml` (it rendered as duplicate text at the top of the main
   page).
4. **Main page image** (reaffirmed from the 8701499 fix): the cover slot
   shows `edrai_book.png` only; `edrai_cover.png` is unused on the page.

**Rationale:** the book's credibility depends on sounding like its author;
a policy plus a linter makes that testable instead of aspirational, and the
preface now speaks to each of its two readers directly.

## Decision 29: One brand — the site follows the book; logo in every notebook; AI-image disclosure (2026-07-29)

**Decision:** Instructor ruling.
1. **The course site matches the book's aesthetics**: sidebar logo replaced
   with the EDR|AI wordmark (`images/edrai_logo.png`); the Purdue-gold link
   and sidebar colors retired from `styles.css` in favor of the book's look
   (cosmo defaults, neutral `#f4f4f3` sidebar, ink accents).
2. **The EDR|AI wordmark opens every notebook**: `nbbuild.py` now prepends a
   generated logo cell to every built notebook (topics and studios,
   instructor and student), so sources stay logo-free and the brand changes
   in one place; the same cell was injected once into all existing built
   notebooks. The book's companion notebooks already carried it (D27).
3. **AI-image disclosure**: a small muted note under the book image on the
   main page, ×3 editions, saying the image is AI-generated and provisional
   while the book is under development.

**Rationale:** one visual identity across book, site, and notebooks, and
honest labeling of generated artwork — the book practices the disclosure it
teaches.

## Decision 30: AI-generic voice, agentic-era framing, Friday 10/5/30/5, nb01 restructure (2026-07-29, eighth review round)

**Decision:** Instructor ruling, 18 items.
1. **Syllabus:** EDR|AI listed before RDSS; translations described as "AI
   generated"; the milestone-collection sentence dropped from the book bullet.
2. **Friday studio rearchitected:** four sections, 10 quiz / 5 stand-up /
   30 milestone kickoff + AI-supported sprint / 5 revision-ledger-submission.
   The peer + AI red-team block is RETIRED; the kickoff line is now "your
   instructor presents the milestone in the course Brightspace page, then you
   work on it with your AI assistant." Students WORK ON milestones at the
   studio (no weekly presentations). "No new topic content, ever" loses the
   ", ever". Applied in course_config.yaml, schedule_data part1–4
   (timelines retimed 15–45/45–50, red-team segments excised), regenerated
   MEETING_SCHEDULE + session guides, CLAUDE.md.
3. **AI-generic voice (student-facing):** notebooks never name a specific
   AI product; "Gemini" swept to AI-partner phrasing across all 32 notebook
   sources (416 mentions) and 5 book chapters ×3 editions (ch19/27/28/33/34;
   ch31's concrete disclosure examples deliberately keep the tool name). The
   template element is renamed **"AI Prompt"** (validator +
   ACTIVITY_TEMPLATE.md updated). CLAUDE.md mission/Monday lines genericized.
4. **Agentic-era framing (standing rule):** AI is more than a chatbot;
   asking AI/agents to DO things is encouraged, while review, curation, and
   the final decision stay human. Touchpoints added: preface ¶2 ×3, nb01
   partner cell, companion-notebook how-to bullet ×3 languages. ch03 already
   taught the agentic loop (D24). **Brainstorming** is named as a partner
   role (nb01 + ch03 ×3).
5. **nb01:** Inquiry & Claim Boundary panel now explains its own parts
   (Inquiry emphasis / Design pathway / claim table); the five design
   pathways are named wherever referenced; M0 is "worked on", not presented;
   the AI Research Partner cell moved directly before the Research Puzzle;
   the never-delegate list links book ch. 4; every code cell has an
   expectation lead-in and a "Reading the output" cell (with the seeded
   numbers verified against execution).
6. **Code-cell narration (standing rule, D30):** every code chunk in course
   and book notebooks is preceded by what it is expected to do and followed
   by a "Reading the output" explanation. Implemented: nb01 (exemplar) + the
   companion-notebook generator (all 111). Remaining course notebooks
   (nb02–nb16, studios) get it as Davi's review advances.

**Deferred, flagged for Davi:** milestone briefs still say "you present a
3-minute walkthrough" (presentation model retired?); the
milestone_presentation_review fields in schedule_data still describe
present+review Fridays; GenAI Studio reviewer touchpoints at M7/M9 lost
their Friday home (M5/M13 live in async modules); the syllabus still lists
the four required GenAI Studio reviews (M5, M7, M9, M13).

**D30 addendum (2026-07-29, same day): deferred items a–d resolved by
extending the same policy.** (a) All 16 milestone briefs: cadence is now
kickoff → develop → submit → revise; studio-presentation parentheticals and
"Presentation"/"Clinic" spec rows replaced by **Studio work** rows; walkthrough
phrasing removed from rubric cells; red-teaming YOUR OWN work (and M13's
replication + red-team identity) kept; briefs are AI-generic (Gemini swept).
(b) schedule_data: all "M# presented:" values → "worked at the studio and
submitted"; "(presented + submitted/due)" → "(worked + …)"; guide label is now
**Studio work / review**; schedule + guides regenerated. (c)+(d) GenAI Studio
reviewer roles are **recommended everywhere, required nowhere** (syllabus,
home page, briefs M5/M7/M9/M13, schedule fields, notebook sources nb10/nb14/
ms09/ms13 — rebuilt). Lecture-block activities that are real course
components (Evidence Defenses, poster gallery walks, hot-seat rounds, the
Expo) are unchanged. The home page's Course Materials and AI Tools blocks
were resynchronized with the syllabus (book first, AI-generated translations,
companion notebooks, GenAI recommended).

## Decision 31: nb01 = orientation + Colab exercise; M5 goes live; attendance/participation split (2026-07-29, ninth review round)

**Decision:** Instructor ruling, 10 items.
1. **nb01 Lecture 1 is orientation only, ending at Questions.** Everything
   from the Research Puzzle to the end of Lecture 1 is now a submitted
   exercise ("Your First Colab Mission") that doubles as Colab training:
   run/edit/add cells, with three **🧱 Build it** tasks (add your own text and
   code cells) and an explicit submit instruction. The AI Research Partner
   section sits after Materials and Logistics; Materials and Logistics is
   fully hyperlinked; the SRL brief links the book's SRL appendix and states
   the swap policy (swap weeks allowed, notify the instructor one week
   ahead); "research seminar, not a statistics survey" and "all code is
   provided" dropped; briefs/rubrics/deadlines sentence simplified to
   Brightspace.
2. **The Course at a Glance teaches what students LEARN**: the working
   structure of contemporary scientific research (question → design →
   evidence along the pathways → verification → uncertainty → public
   defense) with AI agents inside it — added to nb01 and the For-Instructors
   appendix ×3 (which also drops its stale red-team Friday sentence).
3. **M5 is no longer async.** Friday Oct 2 is a regular in-person studio:
   calendar invariant is now 43 = 42 in-person + 1 async
   (validate_calendar updated; the async note removed);
   meeting 17 rewritten to the 10/5/30/5 frame; m05 brief, nb06, ms05,
   registry title, nb01 chain, and planning docs de-asynced. M13's
   Thanksgiving async module stays.
4. **Grading split:** Lecture Notebook Completion (10%) becomes
   **Attendance 1%** (iClicker, 85% target) + **Participation 9%** (rubric:
   notebook completion, feedback surveys, in-class activities) — in
   course_config.yaml, the syllabus, and nb01.

## Decision 32: One visible lecture framework — seven active-voice moves, per lecture (2026-07-29, tenth review round)

**Decision:** Instructor ruling.
1. **The MW lecture architecture nb01 presents is now visible in every topic
   notebook** (nb02–nb16): nbbuild injects a 🗺️ "Today's frame" cell after
   every `# Lecture N` heading — Monday (9/22/12/7) for Lecture 1, Wednesday
   (7/23/12/8) for Lecture 2, a day-neutral frame for single-lecture
   notebooks; nb01 and the async module are exempt.
2. **The seven moves are renamed in active voice** and required IN EVERY
   LECTURE: 🔮 Predict First (was Pause & Predict) · 🛠️ Run the Study
   ("Hands-On" variants → "Run It Live") · 🔍 Read the Evidence · ⚖️ Make a
   Design Choice · 📝 Practice · 🎯 Take It to Your Project (was Project
   Transfer) · 🛡️ Defend Your Decision (was Exit Defense). The 33 missing
   per-lecture instances were authored (uniform ritual closers anchored to
   "today's research decision" + bespoke cells for nb04-L2 Read, nb10-L2 and
   nb16-L2 Practice). `validate_notebooks.py` enforces all seven per lecture.
3. **The book matches**: the SRL appendix (×3 editions) presents the same
   four blocks and names the seven moves; nb01's Mon/Wed cells name them too.

**Rationale:** students get one identical, visible framework for what to do
in every lecture; leads inherit structure instead of inventing it.

## Decision 33: All seven moves INSIDE the 50-minute frame — the homework tail retired (2026-07-29, eleventh review round)

**Decision:** Instructor ruling ("do not overwhelm my students with homework;
fit all moves inside the MW lecture structures").

1. **Placement.** Every one of the seven moves, plus the lecture's 📒 AI
   Research Ledger row, runs INSIDE the 50-minute lecture and sits ABOVE that
   lecture's `### ⏸` line. Monday's blocks now host: 🧩+🔮 (block 1), 🛠️
   (block 2), 🔍 + a spoken 📝 drill + ⚖️ (block 3), 🎯 + 🛡️ + 📒 (block 4).
   Wednesday's: 🧩 + a spoken 📝 retrieval drill of Monday's decision rule +
   🔮 (block 1), 🛠️ with 🔁/🔬 folded into the lab's iterative control
   (block 2), 🧑‍⚖️ + ⚖️ + peer defense (block 3), 🎯 + 🛡️ + 📒 (block 4).
   Block boundaries and minute splits are unchanged (D22).
2. **In-class weight.** 📝 runs aloud (writing optional); ⚖️ is one committed
   written line defended aloud (full paragraph = optional depth); 🎯 is one
   sentence (deep transfer lives at the Friday studio and in the book's "It
   is your turn" chain); 🛡️ keeps its short ritual form, completed by the
   ledger row and the spoken Claim Ticket.
3. **The ⏸ cell changed meaning**: "Optional depth from here", placed after
   the closing moves; everything below it (and every 🏠-labeled prompt) is
   enrichment, never required — the required homework tail is retired.
   Wednesday's old full-length 📝 drill lives on below the line as optional
   depth. 🏠 labels now read "Optional depth."
4. **Machinery.** nbbuild frames rewritten (Wednesday finally names 🔍; both
   days name all seven + 📒 and the ⏸ rule; day-neutral and nb13 conference
   variants); validate_notebooks enforces placement per lecture (moves + 📒
   above ⏸; 🔁/🔬/🧑‍⚖️ above a ⏸ notebook-wide); ACTIVITY_TEMPLATE §7/P3
   updated; all 25 lectures transformed and rebuilt; nb01's week-structure
   cells and the book SRL appendix (×3) updated to match.
5. **Exemptions.** nb01 (orientation), nb14 (async), and nb13 (conference
   week): below nb13's ⏸ is the CONFERENCE PATH (Expo fieldwork + reflection
   studio → M12), kept as own-time work with its own frame cell wording.
   Editorial calls made in the sweep: nb11-L2's Final-Lock section and
   nb12-L2's mock-symposium briefing moved into class; nb04-L1's genie-test
   section, nb08's ##4 model-checks deep dive, and similar depth sections
   became optional; nb09-L1's 📝 gained an inline power definition.

**Rationale:** the required path now fits the room. Depth is preserved but
opt-in; milestone-level transfer keeps its Friday/It-is-your-turn home; and
the visible frame finally tells the truth about when each move happens.

## Decision 34: The D33 evaluation rulings — alignment sweep, validator hardening, and the Wednesday accuracy lock (2026-07-30, twelfth review round)

**Decision:** Instructor-directed evaluation of the D33 build (course task #18),
run through two independent reviews (a Claude specialist review committed as
`LECTURE_STRUCTURE_REVIEW.md`, then an OpenAI Codex critique that recomputed
its counts and audited the repository; artifacts in gitignored
`_adm/codex_reviews/2026-07-30_d33-mw-lecture-structure/`). Rulings applied:

1. **§9① — the demoted arcs stay optional, and assessment aligns to the
   required path.** nb07's list experiment and nb10's placebo/leave-one-out
   arc remain below the ⏸ line (nb07's required §2 survey experiment already
   executes the experimental-descriptive signature; D30 forbids moving new
   teaching to Friday). Everything that still REQUIRED them was realigned:
   week07 quiz Q5 replaced with a survey-experiment measurement item; the
   M18/M26 schedule fields (minute_dynamic, hands_on_activity,
   student_artifact, instructor_prep, risks_contingency, dataset_simulation)
   no longer demand the optional cells; nb10's required 📝 item F became
   self-contained (week10 Q4 is licensed by it and stays); nb08 hoisted a
   compact cross-validation + distribution-shift probe above the ⏸ into the
   verdict section (one provided code cell), which licenses week08 Q4/Q5 and
   the M7 boundary language — the full five-check laboratory stays optional
   (now §7). "Moves to homework" contingency phrasing retired from the
   schedule data.
2. **§9② — one live prompt per lecture, machine-checked.** nb03-L1's
   seed-source snowball prompt demoted to 🏠 (rewrite + prediction stay
   required; running it is optional). nb03 keeps TWO in-class exchanges (the
   live chain-chase + the gap-attack), per the template's standing exception;
   the validator caps required (non-🏠) prompts above the ⏸ at 1 per governed
   lecture (nb03: 2), with the 🏠 label required in the SAME cell as the
   prompt. Label standardized to `**🏠 Optional depth.**` everywhere (12
   stale "Homework depth" strings purged; nb13 keeps its conference-path
   labels).
3. **§9③ — the frame names both optional markers.** All three generated
   frames now close: "🏠-marked items and everything below the ⏸ line are
   optional depth."
4. **The notebook close is never optional.** `nbbuild.py` normalizes the ⏸
   region at build: the ⏸ cell text is standardized, and each notebook's
   Wrap-Up → Sources & Provenance → thank-you is hoisted ABOVE the final
   ⏸ line, so the close and the provenance record sit on the required path
   (nb13 exempt — its below-⏸ is the conference path, not optional depth).
   Section numbers renumbered to read sequentially above the line (nb02,
   nb04, nb07, nb08, nb12, nb16); optional tails carry the last numbers.
5. **Validator hardening.** `validate_notebooks.py` now requires exactly one
   `### ⏸` HEADING per governed lecture (the old character count let prose
   mentions satisfy it, and a missing heading made the placement checks pass
   vacuously); requires Wrap-Up and Sources above the final ⏸; enforces the
   one-live-prompt cap; and bans the retired homework-depth label.
6. **The Wednesday accuracy lock (from the specialist review, resized by the
   Codex critique).** Wednesday block 3 keeps its D22 boundaries (30–42) and
   gains an internal split: 30–38 peer defense + adversarial questioning,
   38–42 SRL synthesis + instructor accuracy lock — the lead states the
   room's conclusion and its uncertainty, and the instructor corrects any
   claim that survived challenge but is wrong before it can enter a ledger.
   Applied to all 13 ordinary Wednesdays in the schedule data (the
   compressed Evidence-Defense Wednesday keeps its full 30–42; Week 1's
   instructor-led Wednesday models the move); session-guide generator keeps
   sub-range labels visible; SRL handbook, prep template, intervention
   protocol, implementation guide, and the book SRL appendix ×3 updated.
7. **Rejected from the specialist review** (per the Codex critique, verified
   against the repository): the 7/20/15/8 Wednesday retime (breaks D22), the
   four-heading collapse and Mon/Wed unification (heading count is not
   transition count; implementation far larger than claimed), and the fixed
   Weeks 2–5/6–11/12–16 guidance-fading schedule (expertise reversal does not
   license calendar fading; safeguards never fade). Write-then-speak 📝 and
   the ⚖️ "I chose X over Y because Z" grammar remain candidates to pilot in
   the room, not pre-semester rewrites. Stale operational docs reconciled
   (instructor guide: quiz-first 10/5/30/5 Friday, random SRL slots, SRL 20%,
   AI-generic voice).

**Rationale:** both reviews agreed the pedagogy holds; the defects that
mattered were contract defects — material promised as optional was still
assessed or scheduled as required, and enforcement had blind spots. The
sweep makes "above the ⏸ line" a true statement of what is required, makes
the validator able to notice when it stops being true, and buys Wednesday a
consolidation moment without reopening D22. Feasibility in the room (block-4
timing, Wednesday block 2) remains to be observed in Weeks 1–2, not assumed.

**Same-day addendum (the weight propagation + the instrument).** The D33
in-class weights were propagated into the closing prompts themselves: the 14
heavy 🎯 cells (all Wednesday closes + nb02-L1, nb03-L1, nb08-L1, nb12-L1)
now ask for ONE in-class sentence, with the milestone spine compacted into a
labeled Friday-studio preview and the answer cell reduced to one field; the
13 heavy 🛡️ cells now run the four-field ritual at one line per field, each
keeping its lecture-specific boundary hint. Measured on the rebuilt
notebooks: required 🎯 prose 135 → 73 mean words with 0/24 lectures carrying
numbered required tasks (was 14/24); 🛡️ 81 → 53. nb11's two 🎯 cells stay as
built — they capture in-room gallery/defense output, which IS that block's
work. The feasibility instrument now exists as
`_project_docs/D33_EVALUATION_PROTOCOL.md`: four dry-run cases (nb03, nb08,
an ordinary Monday, an ordinary Wednesday), a boundary-and-move timing sheet,
an AI-latency field, six predeclared pass criteria, an observer form, ledger
audits, and the first-two-weeks review rule with its cut order (Wednesday
block 2 first; the ⏸/🏠 pilots next; the accuracy lock lengthens before any
frame moves; D22 reopens only on two failed levers in both weeks).

## Decision 35: EDR|AI Architecture v0 — the independence axiom, 39 lessons, 12 practice stations, and the design freeze (2026-07-30, book design evaluation)

**Decision:** Instructor ruling on the EDR|AI book design evaluation (course
task #20), run through two independent ultra-effort OpenAI Codex reviews and
two Claude analyses. The full chain is recorded on the private task as Records
1–6; session artifacts in gitignored
`_adm/codex_reviews/2026-07-30_book-project-design-review/` and
`_adm/codex_reviews/2026-07-30_book-native-redesign-proposal/`.

Both reviews converged: the book's content inventory is sound, but **37
identically equipped chapters are the wrong unit for the practice apparatus**,
and several flagship methods examples teach invalid analysis. Chapter review is
FROZEN until Architecture v1.

1. **The independence axiom (binding).** EDR|AI is an independent,
   self-contained research manual. It must work for a reader at any
   institution, on any calendar (semester, quarter, trimester, none), in any of
   its three languages, with no course attached. HONR 46400 is its first
   adopter, not its skeleton. Course structures — 16 weeks, nb01–nb16,
   milestones M0–M15, the Purdue Expo, SRL machinery, weekly quizzes — may
   constrain ONLY the adoption crosswalk in the For Instructors appendix, never
   the book's spine, and never a chapter body. A machine leakage scan enforces
   this (Phase 2).

2. **Two grains, 39 lessons.** Chapters are *lessons* (reading units); the full
   pedagogical apparatus lives at *stations* (practice units). Two lessons are
   added where both reviews found load-bearing gaps: **uncertainty foundations**
   (estimand → estimator → sampling/randomization distribution → standard
   error/interval → dependence) placed BEFORE ch10, which needs it for its own
   bias/variance/power discussion; and **research ethics and data governance**
   (competent-authority determination, permissions, privacy, de-identification,
   AI data-exposure rules) after ch10. Total 39. The "37 chapters" branding is
   retired rather than merging useful lessons to preserve numerology.

3. **Architecture v0 — 12 versioned practice stations (PROVISIONAL).** Adopted
   from the Codex round-2 counter-proposal. Current chapter numbers are trace
   labels only; production uses immutable semantic lesson IDs.

   | Station | Lessons | Defensible checkpoint |
   |---|---|---|
   | 1. Govern the work | ch1–4 | Responsibility statement, AI/data-handling rules, AI ledger, early red-flag screen |
   | 2. Frame the inquiry | ch5–6 | Objective, units/outcomes/conditions, target/reach, provisional claim boundary |
   | 3. Ground it in verified evidence | ch7–8 | Evidence registry, search log, evidence map; explicit revision of Station 2 |
   | 4. Declare and diagnose provisionally | ch9 → uncertainty foundations → ch10 → ethics/governance | MIDA/Contract v0, diagnosands, permission status, redesign record |
   | 5. Develop the pathway | route hub + ch11–15; ch16 optional complex overlay | Objective × target/reach × data-strategy × warrant declaration; Contract v1 |
   | 6. Govern data and measurement | ch17–18 | Provenance, management, measurement, route-specific permission recheck |
   | 7. Produce a reproducible first analysis | ch19–20 | Route-specific result with uncertainty, restart-and-run-all, environment and claim–output checks |
   | 8. Stress-test and adjudicate | ch21–24 | Robustness, negative-test, diagnostic, adversarial-review, adjudication record |
   | 9. Write, bound, and disclose | ch25–26 + ch31 + rewritten ch33 | Stand-alone research note/report draft, claim–evidence table, AI disclosure |
   | 10. Adapt and defend | ch27–30 as genre branches | One chosen adaptation (poster, talk, brief, other) + defense rehearsal; not yet public release |
   | 11. Reproduce and package | ch32 + ch34 | Independent cold run and reusable package |
   | 12. Release and direct the next cycle | rewritten ch37; ch35–36 optional advanced | Release audit, final dossier, stopping rule, next-study agenda |

   **Versioned, not irreversible.** Checkpoints produce numbered versions with
   reasons, never locked passes — anything else contradicts the book's own
   Declare → Diagnose → Redesign method. Station 4 produces Contract v0 plus a
   permission status; route diagnosis, measurement, permissions, and
   realized-data changes each generate a later version.

   **Four persistent rails** cross every station: ethics/permissions/data
   exposure · evidence, provenance, reproducibility · AI activity, verification,
   human decisions · uncertainty, claim boundary, revision history.

   **The Research Dossier CONTAINS the Contract, it does not equal it.**
   Components: Design Declaration/Contract versions · Evidence Registry ·
   permissions record · data/measurement documentation · analysis/claim ledger ·
   AI ledger · communication artifacts · reproducibility package · revision
   history.

   **Route model — four independent dimensions**, never three conflated ones:
   objective/inquiry; target and reach; data strategy; identification /
   generalization / validation warrant. A currently unidentified causal
   question remains CAUSAL. The five pathway forms of the design layer are
   preserved (observational descriptive · observational causal · experimental
   descriptive · prediction · experimental causal); ch16 is a cross-cutting
   complex-design overlay, not a sixth pathway. Station 5 runs a route hub with
   recognition practice across all forms, full dossier work on the selected
   branch, and one deliberate contrast case.

   **Reproduce before you publish.** Restart-and-run-all, environment capture,
   and claim-to-output agreement belong to the Station 7 first-analysis
   checkpoint; the author's pre-release self-reproduction gates public release
   (Station 11); later peer reproduction is a distinct exercise.

   **A rubric cannot authorize research.** The Station 4 checkpoint is
   "document required determinations and permissions", with states `cleared` ·
   `formal determination required` · `pending` · `not authorized/stop`. No
   collecting, acquiring, linking, transferring, or uploading restricted,
   identifiable, or proprietary real data until the status is documented; safe
   public or synthetic feasibility work is permitted meanwhile.

   v0 is **provisional by design**. It becomes Architecture v1 only after the
   Phase-3 prototypes and cold pilots pass (see `BOOK_DESIGN_ACCEPTANCE.md`).

4. **Retired claims and apparatus.** D24's "the 37 It-is-your-turn sections
   chain into a complete project" is retired — the chain does not produce a
   complete artifact; the accumulation promise moves to the 12 station
   checkpoints, and chapter IYT becomes short practice feeding them. D25(1)'s
   per-chapter companion notebooks are replaced by per-station workbooks
   (physical file count stays provisional until the Station 5/10 prototypes —
   generated-file count is not a maintenance measure). D26's auto-derived
   first-sentence rubrics are retired in favor of authored analytic rubrics with
   stable criterion IDs, route/genre addenda, and exemplar pairs, stored in
   `planning/BOOK_ASSESSMENTS.yml`. D26's seeded-simulation rule and the
   review-banner workflow are unchanged. Non-computational stations are called
   **workbooks**, not laboratories.

5. **F7 — the instructor lock is retired.** A password recoverable from public
   git history still opened all four committed pages, so the encryption was
   theater. The adoption guide, crosswalk, and rubrics are published openly; the
   **private instructor repo** — already "the real protection" — holds
   everything genuinely private (solutions, keys, quiz banks). The post-render
   encryption step and the password file are removed.

6. **Secondary dispositions.** The SRL appendix (`book/srl.qmd`) leaves the
   general appendices in all three editions — it is course machinery, and the
   course keeps its own canonical copy at `project/srl/`. The 111 legacy
   compatibility notebooks are SKIPPED: the book is weeks old, banner-flagged on
   every chapter, and unannounced, so no external reader is known to depend on
   those paths; HTML paths stay stable and semantic lesson IDs are adopted now.
   The review registry is confirmed accurate — nothing is reviewed yet.

7. **The phase plan.** Phase 0: this decision + `BOOK_DESIGN_ACCEPTANCE.md`.
   Phase 1 (independent of architecture, release blockers): the F2/F3 methods
   corrections, the F9 factual fixes, the F7 lock retirement. Phase 2:
   `BOOK_ARCHITECTURE.yml` (immutable lesson IDs, station assignments),
   `COURSE_BOOK_CROSSWALK.yml` (the 16-row map, machine-verified against
   `MEETING_SCHEDULE.csv` and the milestone briefs), `BOOK_ASSESSMENTS.yml`
   skeleton, and rewritten generator/validator with course-leakage scan and
   prerequisite-timing check — this MUST precede inserting the two new lessons,
   or the renumbering desync bites. Phase 3: build the two new lessons and EN
   prototypes of Stations 4, 5, 7, and 10/11; run the cold note-only solo path;
   then freeze v1 and amend D24–D26 and CLAUDE.md. Phase 4: remaining station
   workbooks, authored rubrics + exemplars, de-coursing the chapter bodies
   (Part VI retitle, ch33/ch37 rewrites), citations apparatus, locale
   regeneration. **Chapter review resumes only after the v1 freeze.**

8. **Trimmed from the Codex round-2 list** (right in principle, oversized for a
   one-maintainer project at this stage): the 111 legacy shims (item 6); full
   WCAG 2.2 AA assistive-technology QA across three languages — basic
   accessibility folds into the acceptance criteria and the workbook generator,
   full testing waits until v1 so it does not test throwaway artifacts; and the
   exemplar-provenance BUILD GATES — the registry fields are adopted from day
   one, but failing builds on "unexplained culture-specific adaptation" waits
   until exemplar translations exist.

9. **The next Codex review targets the Phase-3 prototypes**, not another paper
   proposal. Both verdicts said the whole evaluation chain lacked real
   artifacts and cold pilots; a third round on prose would repeat that gap.

**Rationale:** the evaluation found the book promising a complete, self-contained
route it does not deliver, teaching several methods incorrectly, shipping 33
"laboratories" that contain only a scratch cell, and grading with rubrics
truncated to a step's first sentence. The architecture that produced those
defects is the per-chapter uniform kit; the fix is to separate reading grain
from practice grain, put the apparatus where the research decisions actually
cluster, and validate the result on real artifacts before freezing it. The
independence axiom is what keeps the fix from importing Purdue's calendar into
a manual meant for any reader anywhere. Timing: none of this blocks the Fall
2026 launch — the course notebooks are separate artifacts and the early
milestone anchors are identical under both architectures.

## Decision 36: Translation deferred to project end; autonomous completion of Phases 1–4 (2026-07-31)

**Decision (Davi's directive, this date):**

1. **PT/ES translation is FROZEN until the end of the D35 build.** English is
   the only edition edited and rendered through Phases 1–4. The PT/ES books
   stay online, and every PT/ES page carries a prominent development notice
   (injected via each edition's `_lang-switcher.html` include) stating that
   the translation is under development and that the English edition is the
   version of reference, with a link to it. Language buttons remain on every
   page in all editions; a reader who clicks Português or Español lands on a
   page carrying the notice. Once Phase-3 insertions make the EN structure
   diverge, the PT/ES buttons on EN pages route to the PT/ES index rather
   than the per-page counterpart.
2. **Every deferred item is logged in `planning/TRANSLATION_BACKLOG.md`**,
   created by this decision — including the round-4 PT/ES ch14 errors, the
   never-crossed ch21/ch22, the PT/ES preface bounded-claim fix, and the
   round-4-required human PT/ES methods review. This amends D23's
   resynchronize-on-every-edit rule for the duration of the build. The 6.2
   release blocker transfers to the backlog unchanged: translations still may
   not ship *as current* before syncing — the per-page notice is what makes
   the interim state honest.
3. **Autonomous completion mandate:** the assistant executes Phases 1–4
   end-to-end without stopping for approval, running the two-role Codex loop
   (mirror-mode partner + adversarial critique, xhigh; ultra only on Davi's
   explicit word) on every substantive unit. Davi reviews the finished
   English artifact manually at the end.
4. **Course readings update from the machine-verified crosswalk** (Phase 2,
   re-run after the Phase-3 lessons land). Topics change only if the
   validator proves a change necessary, and every such change is logged for
   Davi's review.
5. **Endpoint and order:** Phases 1–4 complete in English → hand-off → Davi's
   manual review → translation, performed once, after the review settles the
   text.

**Rationale:** four adversarial review rounds showed that every English change
forces a PT/ES propagation whose fidelity no English-substring scanner can
certify (rounds 3–4), tripling work-in-progress while the architecture
redesign is still moving the text. Freezing translation until the text stops
moving removes triple maintenance during Phases 2–4, and matches round 4's own
requirement of a human methods reader per language — which is only worth
staging once, on settled prose.

## Decision 37: Architecture v1 FROZEN — the two grains are real, chapter review reopens (2026-08-01)

**Decision.** EDR|AI Architecture is frozen at **v1**. The structural questions
D35 left provisional are settled and machine-enforced, so the shape of the book
stops moving and **chapter review reopens** (D35's freeze is lifted).

**What v1 fixes, all validator-enforced:**

1. **Two grains, both real.** 39 lessons (reading) and 12 practice stations
   (doing). Stations exist as generated pages and workbooks with authored
   practice content, versioned checkpoints, the four rails in station-specific
   form, and authored rubrics. The preface teaches the distinction and every
   lesson points to the station its work feeds.
2. **Identity is immutable and proven.** Lesson ids, `url_path`, and companion
   paths survive insertion — demonstrated twice in the live repository by
   activating the two new lessons, with every projection (briefs, BOOK_MAP,
   material page, companions, TOC) regenerating itself. `identity_epoch`
   enforces it: a rename or URL move fails the build.
3. **One validated loader.** Every book consumer reads
   `scripts/book_manifest.py`; nothing derives identity from a filename
   prefix or a display number; orphan artifacts are rejected in both
   directions.
4. **Institution-agnostic bodies.** The A2 leakage scan reports zero and is a
   HARD GATE. The lesson-to-lab mapping lives in the For Instructors appendix
   as a generated table.
5. **The two load-bearing lessons ship**: uncertainty foundations (before
   ch10, which needed it) and research ethics and data governance.

**What v1 does NOT claim.** Acceptance test A1 was RUN on 2026-08-01 and
returned **No**: a solo reader reaches a defensible plan, not an original
empirical claim. The three causes are recorded and fixed
(`planning/BOOK_DESIGN_ACCEPTANCE.md`), including the architectural gap the
pilot exposed — nothing acquired data, so Station 6 now opens with an
acquisition route keyed to permission status. P1 stays BOUNDED and the preface
says what the book actually delivers. Freezing the architecture is not
claiming the promise; it is fixing the shape so the remaining work is content,
not structure.

**Open, tracked, not blocking the freeze:** station workbooks still need worked
examples, starter data, and faded scaffolds (A4); route/genre rubric addenda
and exemplar pairs are unauthored (A6, and exemplars need real consented
student work); Part VI's retitle; PT/ES remain frozen under D36 with their
backlog; prediction's book-wide classification still needs Davi's ruling.

## Decision 38: The Twelve Studios become the book — amended Option 1, "Studio" naming, the practice-first chapter template, real bibliography (2026-08-03)

**Ruling (Davi).** Implement the structure loop's final recommendation
(`planning/BOOK_STRUCTURE_OPTIONS.md`): the twelve practice units become the
book's twelve navigational parts. Four modifications rule the implementation:

1. **"Studio", not "Station."** The reader-facing word is **Studio**
   everywhere (pages, pointers, preface, workbooks, proposal). The machine
   layer keeps the immutable `station` ids and YAML keys — display is derived,
   identity never moves (A10). Studio pages live at
   `book/studios/studioNN-<id>.html`; the old `stations/stationNN-*.html`
   URLs stay alive via per-page aliases.
2. **The chapter template turns practice-first.** The standalone
   "Recommended AI prompts" section is retired — every AI prompt attaches to
   the exercise/practice step it serves inside "It is your turn". "The Colab
   laboratory" section is removed; its companion-notebook introduction folds
   into "It is your turn" (the section Davi prefers). **Worked examples must
   come with data and evidence** — a seeded code block or named real dataset
   generating the numbers the prose quotes, plus a citation to real published
   material.
3. **A real reference apparatus.** Chapters carry in-text citations to real,
   independently retrieved published material (`book/references.bib`);
   every entry is opened before it is cited; unverifiable candidates queue,
   never ship.
4. **The T&F proposal follows the book.** The filled proposal DOCX's ToC +
   abstracts section is regenerated to the twelve-Studio structure; Davi's
   manually reviewed sections before it are preserved untouched.

**Mechanics shipped with this ruling:** `scripts/build_book_toc.py` generates
the `chapters:` block of `book/_quarto.yml` from the manifest (the last
hand-maintained ordering source closes); the TOC and studio pages are
PROJECTION-level validator checks (stale ones fail the run but never withhold
the lock — the N2 deadlock class); two lessons re-rank into their studio
(`ai-disclosure` 310→262, `poster-to-note` 330→264 — the only two order moves,
both enacting D35's dossier-first adjudication); `poster-to-note` becomes
`role: core` retitled "From Dossier to Research Note" (url_path immutable);
studio openers carry the `#checkpoint` anchor and each studio's last lesson
routes the reader back to it; lesson pointers are role-aware (core / branch
pathway or genre / optional overlay); the six former parts survive as
non-navigational arcs on the "How this book is organized" front page
(repurposed part1-overview.qmd, same URL). Display numbers 29–35 relabel;
projections regenerate mechanically. PT/ES stay frozen (D36) and now also
diverge structurally — the translation pass will regenerate their TOCs from
the same manifest.

**D38 implementation record (2026-08-03).** All four parts shipped:
(A) the Studio migration — generated TOC, `book/studios/` with aliases,
`#checkpoint` anchors, role-aware pointers, two re-ranks, ch33 core;
(B) the practice-first template across all 39 chapters — prompts attached to
their IYT steps (mapping from a Codex partner run; 3 duplicates dropped),
"The Colab laboratory" folded into "It is your turn"; (C) 108 verified
citations from 67 new bibliography entries, each independently resolved
before inclusion (93 direct, 14 via Crossref, Belmont via archival copies);
(D) 39/39 worked examples now carry seeded data AND published evidence, with
`DATA_PENDING`/`EVIDENCE_PENDING` empty and enforcing. Where code and prose
disagreed, the prose was corrected to the executed output. The T&F proposal
DOCX was regenerated from the ToC heading down (12 studios, renumbered
abstracts); every paragraph above that heading is byte-identical to Davi's
reviewed text, machine-verified.

## Decision 40: Milestone chapters close every studio; new-tab links; titled bibliographies (2026-08-03)

**Ruling (Davi).** Three directives, all book-side:

1. **Book hyperlinks always open in a new tab.** Implemented as
   `book/_page-behavior.html` (include-after-body): every link in the page
   BODY gets `target="_blank" rel="noopener"`; navigation chrome (sidebar,
   TOC, breadcrumbs, next/previous) and same-page anchors keep native
   behavior, so the book never navigates away from the reader's place. The
   include also demotes the citeproc-generated bibliography heading to h2.
2. **Chapter bibliographies live in a titled section.**
   `reference-section-title: Bibliography` in `book/_quarto.yml`: chapters
   that cite get a "Bibliography" section above their reference list;
   pages without citations get none.
3. **The studio "checkpoint" becomes a Milestone chapter.** Each studio is
   now TWO generated pages: the OPENER anticipates the milestone (the
   authored `milestone_reason`, what it produces, the `hands_forward`
   chain sentence, and a per-lesson list of the piece each lesson's "It is
   your turn" hands the milestone) and keeps route/acquisition guidance
   plus the legacy `#checkpoint` anchor; the **Milestone chapter**
   (`book/studios/milestoneNN-<id>.qmd`, unnumbered, LAST in its part)
   carries the details — "What you bring" checklist, practice steps
   (`#milestone`), the version-not-a-pass rule, the four rails, "Where
   this milestone sits" (the 12-milestone chain ending in the released
   research artifact), revisit, the authored rubric, and the workbook
   badge. Reader-facing titles are artifact-first ("Milestone 2: Your
   question, declared").

**Scaffold guarantee.** BOOK_STATIONS.yml gains four authored fields per
station — `milestone_title`, `milestone_reason`, `hands_forward`,
`contributions` (lesson id → the IYT piece it hands the milestone; 39
lines authored from the actual IYT steps) — and the architecture validator
gains a scaffold gate: an active lesson with no contribution entry, or a
contribution naming a lesson outside the studio, fails the build. The
milestone chain (1→12) is generated on every milestone page and stated in
the preface and the organization page.

**Mechanics.** `build_station_pages.py` emits opener + milestone chapter +
workbook (workbooks retitled "Milestone N", same immutable paths);
`build_book_toc.py` appends each milestone chapter to its part;
`build_station_pointers.py` routes each studio's last lesson to
`milestoneNN-<id>.qmd#milestone` and rewords the core pointer; rubric
texts in BOOK_ASSESSMENTS.yml resworded station/checkpoint →
studio/milestone (ids untouched); the A2 leakage rule `course-milestones`
narrowed to course-CODED forms (`milestone M4`, `M4 brief`,
`milestone_04`) since bare "Milestone N" is now book vocabulary; the For
Instructors appendix disambiguates book Milestones 1–12 from course
milestones M0–M15; PT/ES replay steps logged in TRANSLATION_BACKLOG.md
items 12–13. Identity untouched: station ids, lesson urls, and workbook
paths are unchanged; old `#checkpoint` deep links land on the opener's
anticipation section.

**Process.** Built through the two-role Codex loop: a mirror-mode partner
run (gpt-5.6-sol, xhigh, read-only) ran the same assignment in parallel;
its material is merged with attribution in
`_adm/codex_collab/2026-08-03_studio-milestones-links-bib/`. The partner
merge adopted the link-accessibility layer, the native external baseline,
and three integrity repairs (Studio 4's measurement inversion — Contract
v0 carries a provisional operationalization, measurement is assessed in
Studio 6; Studio 11's solo-proxy label; Studio 12's stale-run gate). The
review round (same model/effort, `review --base e9eb85a`) returned four
findings, all confirmed and applied: the stale-run gate widened to any
package change, the milestone checklist made role-aware (branch/optional
pieces bind only when their condition holds), the solo proxy aligned with
Studio 11's produces and rubric, and a visible new-tab cue added beside
the assistive note. Declined partner recommendations (recorded for Davi):
"References" as section title with a per-chapter static include; rank-free
milestone URLs and un-numbered milestone titles; the per-lesson IYT gap
list, manifest-level milestone identity, `_iyt-rubrics` retirement, and
the release-bundle final-artifact definition stay queued for the chapter
review.

## Decision 41: Option 2 — the studio-first route-selective semester (2026-08-03, ruled; structural phase shipped 2026-08-04)

**Ruling (Davi).** The course adopts **Option 2** of
`planning/COURSE_REFRAME_OPTIONS.md` (studio-first, route-selective), updated
for the post-D40 book. The course is conditioned on the book, never the
reverse; the book does not change. (No D39 exists — the number was reserved
by the options memo and the book took D40 first; the gap is deliberate.)

**What the ruling fixes:**

1. **The weekly spine is the Studio arc.** W1–W4 = Studios 1–4; **W5 is the
   route hub** (Studio 5): all five pathway lessons anchor there as
   `route-required` — each student reads their OWN route plus one
   instructor-assigned contrast, class runs a five-route jigsaw with
   advocate roles independent of project routes, and
   `hybrid-complex-designs` binds only when the design has stages (the
   course's blanket adopt-optional-as-required policy bends for
   route-conditional lessons). W6=S6, W7–8=S7 (build / clean-restart
   verify), W9=S8, W10=S9, W11–13=S10 (poster / defense / public test),
   W14–15=S11 (+S9 close), W16=S12.
2. **The three repairs are binding**: pathway declared at M4; the bounded
   research-note v0 (M9) exists BEFORE poster adaptation; author
   self-reproduction AND a release preflight gate the Nov 6 poster lock
   (two blocking gates on the M10 row).
3. **The D40 naming bridge.** Course milestones M0–M15 stay the
   submission/Brightspace ids and each presents a **book Milestone
   version**: M6+M7 are versions 1–2 of Book Milestone 7, M10–M12 versions
   1–3 of Book Milestone 10, M13+M14 versions 1–2 of Book Milestone 11,
   M14 also closes Book Milestone 9 (v2). "Course milestone M#" and "Book
   Milestone N" are never abbreviated to a bare shared "Milestone N" in
   course surfaces. The bridge is machine-readable: crosswalk schema 1.1's
   `book_milestones:` blocks (+ `route_selection:`,
   `supporting_gate_milestones:`), validated per row.
4. **Checkpoint semantics**: a checkpoint FIRES once (first version) and
   later submissions are `revisit` events. M12/nb13 is a legal
   **revisit-only calendar container** (the Expo week presents no new
   lesson); `validate_book_sync.py` check 3 now requires ≥1 assignment of
   any purpose per notebook, and the For Instructors adoption table lists
   revisit-only labs explicitly.
5. **Identity is untouched**: calendar, 50-minute frames (D22/D33/D34),
   assessment weights (1/9/20/20/20/20/10), notebook slugs and student
   filenames (permanent compatibility ids), brief filenames, lesson and
   station ids, book URLs. Notebook display titles change only when their
   content is rebuilt.

**Structural phase (shipped with this record):** crosswalk rewritten
(39-lesson bijection: pathway lessons 5+1 → M4; data-provenance +
measurement → M5 with the D40 Contract-operationalization revisit;
ai-as-programmer → M6; ai-analytical-assistant → M7; the four stress-test
lessons → M8; the four Studio 9 lessons incl. poster-to-note + ai-disclosure
→ M9; difficult-questions → M11; research-packages alone anchors M14);
BOOK_STATIONS.yml joined the crosswalk lock; schema-1.1 validation added;
briefs' Book Anchors, BOOK_MAP, the For Instructors adoption table, and the
Material/Instructor pages regenerated; course_config v3 (weeks, milestone
titles, pathways at W5, GenAI touchpoints remapped M4/M7/M10/M13);
PROJECT_MILESTONES chain retitled with the Book Milestone column;
COURSE_MASTER_PLAN v3 (§2 studio table, §4 route hub, §7 attendance/
participation split, §8 post-D40 book description); M1's broken M2 link
fixed. Process: two-role Codex loop — mirror-mode partner blueprint +
diff review (gpt-5.6-sol, xhigh, read-only), artifacts in
`_adm/codex_collab/2026-08-03_option2-implementation/`.

**Content phase (tracked, before the Aug 24 launch):** (B) milestone-brief
prose rebuild M3–M15 (titles/artifacts/rubrics; retitle only, never
re-slug) + quiz banks W5–W12 + GenAI role spec re-anchoring + SRL briefs;
(C) `scripts/schedule_data/` meeting rewrite (m12–m43 semantic fields, all
34 columns) + regenerated schedule/guides + `update_schedule_badges.py`
milestone-label handling + nb05–nb16 source rebuild via
`_production_kit/nb_sources/` with display titles updated at cutover;
(D) Synthetic Colleague infrastructure (persona templates, per-studio
generation workflow, audit rubric, Case 464), per the memo's device
section. Declined from the partner run (recorded): staging the crosswalk
as an inactive candidate until notebook cutover — Davi ordered
implementation; the transition is disclosed here and in the crosswalk
header instead. Deferred validator hardening: `validate_coverage.py`
exactly-one-nb-token rule; lock validator-version rejection in
`require_lock()`.

**D41 review-round record (2026-08-04).** The Codex diff review
(gpt-5.6-sol, xhigh, read-only; verdict in
`_adm/codex_collab/2026-08-03_option2-implementation/review_verdict.md`)
returned do-not-ship with six findings — a session auto-commit had shipped
the structural phase mid-review as `a3faef8`; this corrective commit applies
every confirmed finding: (1) the naming bridge is now GENERATED — 
`build_milestone_anchors.py` renders a marked Book-Milestone-bridge block
into every brief (book Milestone number/title/version from the crosswalk +
BOOK_STATIONS, route-conditional reading on M4, revisit and gate lines, and
a D41 rebuild note), and all sixteen briefs are retitled "Course milestone
MN — <D41 title>" so bare "Milestone N" stays book vocabulary; (2) the
Material page, adoption table, and every brief carry an explicit
rebuild-in-progress notice until the nb05–nb16 content cutover, replacing
the false "derived from" claims; (3) schema-1.1 validation is a real state
machine (bridge↔event agreement both directions, checkpoint fires exactly
once, revisit only after its checkpoint, route policy tied to
route-required rows, first-read ⇒ home anchor, typed gate booleans,
schema_version enforced; VALIDATOR_VERSION 1.1) — all ten corruption
fixtures, including the review's seven, are caught; (4) Book Milestone 11
corrected: M13 is peer cold-run PRACTICE preceding version 1, M14's
checkpoint is v1; (5) `taught_in`, the reading-model fields, the master
plan's Week-7 sentence, and the kickoff reviewer set (M4/M7/M10/M13) no
longer contradict the route policy, and the stale "37 It is your turn
sections" sentence is fixed in all sixteen briefs; (6) `require_lock()`
verifies the COMPLETE locked manifest set (assessments + leakage policy
included). Queued counter-proposals for Phase B: structured
version/status fields instead of free-form version_label; one typed loader
generating the milestone registry, PROJECT table, brief bridges, and
adoption labels; separating lesson ownership / student assignment /
version contribution, which `home_anchor` currently overloads.

**D41 content-phase completion record (2026-08-04).** Phases B, C, and D
are COMPLETE and the transition state is closed. Shipped through the
two-role Codex loop (a 1,620-line mirror-mode content blueprint —
redistribution maps with cell-level reuse, eight full draft meeting dicts,
forty draft quiz items, the cutover sequence — merged with an independent
Claude track and executed by coordinated subagents, every artifact
machine-gated): (B) all 16 briefs carry the studio-first artifacts; quiz
banks W5–W12 rebuilt + the missing week06 created, all parity-gated, keys
teaching the guarded formulations with misconceptions as distractors only;
the five-touchpoint GenAI bench (M4/M7/M8/M10/M13 — the old M9 pairing
split); SRL-adjacent protocols re-anchored. (C) `scripts/schedule_data/`
parts 1–4 fully studio-first (43 meetings × 34 fields; colleague beats per
the kit cadence; naming bridges in every milestone field); ALL 16 course
notebooks rebuilt or adapted (nb05 route hub with five verified route
cards; nb06 governance; nb07/nb08 the build/verify pair; nb09 stress-test
with the pre-registration card; nb10 the bounded-note week; nb11 gates;
nb12 pitch; nb13 revisit-only public test; nb14 practice-not-checkpoint
cold run; nb15 note-v1+package; nb16 release audit) plus all 16 ms studio
sources; display titles cut over (nb14 keeps the "Async module" prefix the
async validator keys on); the three rebuild notices removed and every
projection regenerated; instructor repo synced (32 notebooks, 16 guides).
(D) the Synthetic Colleague kit: public `project/colleague/` (README with
sourced learning-science claims, 7-move audit protocol, 4-row rubric,
synopsis form with generic-case/withdrawal/retention consent, Case 464)
and the private generation kit (error menus for all 12 studios keyed to
the misconception manifest, generation workflow with pre-release
verification, persona template, Case 464 key); syllabus disclosure inside
Participation. Full validator suite green (architecture, sync, milestones,
calendar, adoption, anchors, book map, badges, misconceptions local,
citation audit, voice ×16). Session-limit interruption mid-build was
recovered by state assessment + targeted repair (nb12's corrupted cell,
one voice violation) + one relaunch. Remaining known work: the Codex
review round over the content diff (in flight at this record); GenAI role
spec deep rewrite and SRL handbook refresh remain adequate-but-unpolished;
first live generation of the five colleague personas happens when student
synopses arrive (Week 2).

**D41 review-round record — content phases (2026-08-04).** The closing
Codex review (gpt-5.6-sol, xhigh, read-only; verdict in
`_adm/codex_collab/2026-08-04_d41-content-phases/review_verdict.md`)
returned do-not-ship with nine confirmed findings; all nine are applied:
(1) the consolidated quiz ANSWER_KEY regenerated wholesale from the weekly
key files (it had kept pre-cutover questions for W5/W8/W10) and its
week-6-async header error fixed; (2) nb05's three methods defects repaired
— the Hajj card relabeled as the intention-to-treat effect of WINNING the
lottery (the file has no attendance variable; the pilgrimage's own effect
needs IV), the Bonilla card stripped of its equivalence-from-failure-to-
reject verdict ("did not detect a frame effect of this size" replaces
"frame-STABLE"; the frames are named as a real intervention used to
measure), and the retrieval prompt's "unfound in a minute = fabricated"
replaced with unresolved-as-status; (3) the audit cadence made REAL: ten
scored beats now scheduled (W2-W6, W8-W11, W16 Wednesdays; Studio 1 is the
modeled Case 464, Studio 11 is graded through M13 itself) and every surface
says best 8 of 10; (4) required GenAI touchpoints say "required" on the
schedule surfaces and the instructor guide's table carries the five current
roles; (5) M4's reading burden made route-conditional on both graded
surfaces and W5's meeting openers aligned to the notebook; (6) nb09's
primary panel split — unadjusted marginal contrast alone, covariate-
adjusted contrasts in their own labeled panel, the "does the target
quantity change?" gate added; (7) nb10's claim ladder replaced with the
kind-x-reach claim-license matrix and results ordering re-anchored to the
predeclared primary (interval width demoted to one input); (8) M7 requires
two independent re-derivations with a pre-declared tolerance and route-
conditional precommitment language; M9's poster content brief is an
ungraded handoff to M10 kickoff (note-first made operational); (9)
`validate_coverage.py`'s pipe-parser fixed (structural " | ", so "EDR|AI"
is content) and the gate is GREEN for the first time this build — the
earlier completion record's "full validator suite green" claim was wrong
by omission of this gate, corrected here. Queued counter-proposals: one
typed registry for audit events/touchpoints/artifact lists; route/estimand
cards for teaching cases; canonical structured quiz items rendering both
bank and key.

## Decision 42: References sections; Studio 10 venue contracts; Studio 12 closes mode-neutral with its agent lessons kept (2026-08-04)

**Ruling (Davi).** Three directives: (1) the chapter bibliography section is
titled **References**, not Bibliography; (2) Studio 10 must honestly serve
formats beyond the poster; (3) the Studio 12 lessons-vs-description mismatch
is evaluated and resolved whichever way is better for the book, with a
stated preference for keeping something about AI agents.

**1. References.** `reference-section-title: References` (amends D40's
Bibliography choice). Toolchain fact, verified twice: Pandoc keeps the
section id `#bibliography` whatever the visible title, so no anchors moved;
the demotion include now keys on the stable `div#refs` container, which
also survives the future localized titles (Referências / Referencias —
TRANSLATION_BACKLOG item 13 updated).

**2. Studio 10 — the venue contract is the universal scaffold.** No new
lesson; all four lesson classifications unchanged. The studio's authored
content now opens with a **venue contract** (audience, medium, limits,
required elements, accessibility, submission rule, question channel) and a
**content map** locating claim, evidence, boundary, uncertainty, and
disclosure; a format table routes poster / live talk / talk-with-slides /
written brief / other through the existing lessons, transferring named
techniques rather than whole lessons. The guide renders on the opener, the
milestone chapter, and the workbook (the practice references it). Practice
steps: contract → content map → build with trace → test in the format's
actual mode → rehearse (written questions when the venue has no live ones).
Rubric criterion 5 resynced with diagnostic 0/1/2 levels. Chapter touch-ups:
ch27 names what travels with a figure vs what is poster-only; ch28 separates
the audit's universal spine from poster procedure; ch29 adds the
slides-serve-the-spoken-spine paragraph; ch30 is de-postered and admits
written questions. Poster-criticism's milestone contribution returned to an
honest poster-only condition — the milestone, not the lesson, owns the
general audit.

**3. Studio 12 — lessons kept, description made true.** Ruled direction:
keep the two optional agent lessons in place (they need a mature draft, so
earlier placement fails; ch37 consumes their outputs; moving them would
ripple through station ranks, TOC, and the M15 bridge for no content gain)
and make the studio genuinely mode-neutral. The confirmed defect the
partner run exposed: ch37's core IYT required a multi-agent portfolio
(loop decomposition, conflict + override, independence check) that a
reader who correctly skips the optional lessons cannot produce. Now: the
practice records a **review mode** (no AI / one assistant / several
loops) and attaches only the evidence that mode produces; ch37's portfolio
step is producible in all three modes; ch35's setup is conditional; ch36
diagnoses a load-bearing pair whether it agrees or disagrees. The release
audit marks items clear / pending / **blocking**, the decision is release
or **withhold pending a named repair** (a valid final version under D35's
version-not-pass rule), the dossier carries a manifest, and a
package-current-with-cold-run blocking gate joined the rubric. The
milestone chain sentence on every page now ends on the decision ("whether
your finished research artifact leaves your hands"), not a promised
"released and defended". The studio's framing closes the ch01 thesis:
zero, one, or many tools — the release standard does not change.

**Machine layer.** `build_station_pages.py` renders `genre_guide` on all
three studio surfaces and the decision-honest chain; the architecture
validator requires route/genre chooser guides wherever a studio has
route/genre-branch lessons. Course ripple: zero briefs changed (titles
stable); BOOK_STATIONS/ASSESSMENTS re-locked.

**Process.** Two-role Codex loop (gpt-5.6-sol, xhigh, read-only): mirror
partner run merged with attribution
(`_adm/codex_collab/2026-08-04_refs-studio10-studio12/`) — Codex-only
contributions: the stable-id toolchain fact, the venue-contract scaffold,
the ch37 impossibility, the guide-placement gap, the withhold semantics;
Claude-only: the References implementation, thesis-closure framing, course
ripple check. Declined/queued: a dedicated policy-brief lesson (generic
venue-contract path suffices until Davi wants the genre taught in depth);
ch37 retitle to "Release Audit and the Next Study" (kept the
AI-management-portfolio identity the course deliverable depends on;
mode-adaptive wording achieves the same coherence); strict criterion-5 ↔
produces machine-sync (texts legitimately diverge in explanatory tails).
Diff review round (same model/effort, `review --base a6389a7`): three
findings, all confirmed and applied — ch37's IYT now tells the no-AI mode
to skip the prompts, run the checks manually, and close the ledger with
the scope line; ch36's closing step logs the pair, diagnosis, and check,
with an override only when one occurred; and the transfer notes restore
the interval-OR-caveat formulation (uncertainty shown where the design
licenses it) instead of demanding intervals on every quantitative
visual, in ch27, ch29, and the Studio 10 contribution line.

## Decision 43: The research-first on-ramp — curiosity before the tools, kits before the milestones (2026-08-04)

**Ruling (Davi).** Implement `planning/BOOK_OPENING_OPTIONS.md`'s
recommendation (Option 4) and its adjustments 1, 3, 4, and 5; adjustment 2
(the author-review gate) stays with Davi, to start after this lands. Also:
update the Studio 1 and Studio 2 content in the filled T&F/CRC proposal.
The experienced sequence is now: **human curiosity → ledger and rules →
verified AI assistance → formal research question.**

**The on-ramp.** Studio 1's opener and workbook open with a human-only
**opening move** (authored `opening_move` field; generator renders it as
"Start without a tool"): four handwritten lines — what you want to
understand, why it matters, your starting belief, and the evidence that
would revise it — with a hard no-AI stop. Studio 1 is retitled **"Begin
the research and govern the work"** (display only; id, rank, URLs
unchanged). Ch1 bridges from the committed curiosity and widens it; the
preface leads research-first; the organization figure is rebuilt as the
research road (curiosity capsule → six stages → a DECISION endpoint that
honors D42's release-or-withhold, four rails beneath). Course side: the
Week-1 units and master plan carry the new title, and nb01 visibly
creates the ledger before its first prompt (instructor repo synced). The
first-AI invariant — human commitment → ledger opened → AI prompt →
independent check → ledger row — is now explicit on every surface.

**Practice kits (A4 tranche, Studios 1–4).** Authored `practice_kit`
fields (worked example · half-finished faded task · starter · verification
check) render into the four studio workbooks, threaded on the book's own
restaurant-prices running example from ch1; completeness is
validator-enforced. The partner run's alternative kit thread (Indianapolis
hot-days, NCEI) is recorded as a candidate for the analysis studios.

**Tiered opening.** Each Studio 1 lesson keeps ONE core AI cycle (ch1
locate-and-verify sources — the citation catch; ch2 the boundary
red-team; ch3 the SDIIVDD delegation; ch4 list-every-claim-to-verify, the
partner run's argued flip); the other eight prompts carry an *Optional
depth* label. M0 requires the Book Milestone 1 checklist's named
contributions, not prompt count, in both the submission row and the Book
Anchor intro.

**Instruments and positioning.** `planning/COLD_TEST_PROTOCOLS.md`: the
45–60-minute first-mile protocol (hard prompt-before-ledger gate,
five-move reconstruction, numerator reporting, IRB determination flag)
and the second-A1-pilot frame (unaffiliated reader, book-only,
no-permission route, claim-or-evidence-based-withhold pass; toys never
lift A1). `planning/RDSS_COVERAGE_MATRIX.md`: the
adopted/adapted/omitted/EDR|AI-original map; the preface now says EDR|AI
"draws its design framework from" RDSS (MIDA, declare-diagnose-redesign),
a companion and on-ramp, never a translation. CAUGHT for Davi: official
RDSS ch. 4 is the DeclareDesign/R quickstart, so `READING_MAP.md`'s
"RDSS ch. 4 §literature" citation conflicts with the official contents
and needs his correction.

**The proposal DOCX.** Studio 1 and Studio 2 passages inserted after the
Part I/II headers; the structure preamble names the twelve Studios and
Milestone chapters; ch1/ch5 abstracts carry the research-first opening
(backup saved beside the file). FLAGGED for Davi: the FILLED proposal's
ToC is still the six-part structure frozen Aug 1 — it never received the
twelve-studio regeneration D38's record describes; regenerating it is a
decision, not done silently.

**Process.** Two-role Codex loop (gpt-5.6-sol, xhigh, read-only): mirror
partner drafts merged with attribution
(`_adm/codex_collab/2026-08-04_d43-implementation/`); kept over
counter-proposals: the restaurant-prices kit thread (continuity) and
ch2's boundary red-team as core. PT/ES: replay entries only (D36). Diff
review round (same model/effort): five findings, all confirmed and
applied — the S3 faded task now audits LIVE AI output instead of implying
a planted citation (D16); the S2 worked example's reach is bounded to the
retrievable panel (no silent upgrade toward the group, per INQUIRY_MAP);
the S4 redesign stops pretending a fixed panel removes price-dependent
survival and narrows the estimand instead; the workbook opening-move cell
asks for all four lines with a field template; and the cold-test protocol
gains participant data management (IDs, redaction, consent for quotes and
photos, approved storage, deletion date) required before recruitment.

## Decision 44: Front-matter numbering; the arc made experiential; publication-ready Studio 10; Studio 12 as the agentic special topic (2026-08-05)

**Ruling (Davi).** Four directives: (1) "How this book is organized" must
not be enumerated — only Studios and lessons carry numbers; (2) the D43
arc must be PRESENTED inside Studios 1–2 and their lessons, with AI
brainstorming licensed as a structured way to push the curiosity toward
its later formalization; (3) Studio 10 must cover formats beyond the
poster — the goal is an artifact ready for publication and/or
presentation (paper, seminar, talk, poster, other); (4) Studio 12 becomes
a special topic whose core is advanced AI and agentic-AI research
practice, with the organization figure and prose reviewed afterward.

**1. Numbering.** The organization page is H1 `{.unnumbered}` front
matter. Side effect deliberately banked: Quarto's chapter numbers now
equal the manifest's Lesson N labels (chapter 1 = Lesson 1; the old
off-by-one is gone). The banner updater re-anchors on an H1 when a page
has no YAML (partner-run catch).

**2. The arc, experienced.** Studio 1's milestone_reason narrates the
four beats (curiosity → ledger and rules → verified AI assistance →
formal question) and Studio 2's closes them; ch5/ch6 bridges anchor
their beats. ch1 gains the licensed **structured brainstorm** after the
ledger: a divergence-partner prompt (five stretching questions,
NEW-labeled introductions, no ranking, no choosing, no novelty claims,
no citations) with an audit verify note; ch5's widening prompt gains the
same kept-or-rejected trail. The first-AI invariant holds; the brainstorm
is licensed, not required. Partner counter-proposal recorded: placing the
first brainstorm in Lesson 5 instead (the memo's decision trail into
Milestone 2) — declined for ch1 placement per Davi's "push their
curiosity … later formalize".

**3. Studio 10 = "Prepare to publish or present."** Retitled (display
only). The milestone produces the artifact itself, ready to submit or
deliver: the format guide's first-class rows are paper/research note
(developed from the Studio 9 note), seminar/conference talk (the pitches
spine expanded; ch29 teaches the expansion), short pitch, poster, other;
a transformation-memo step (what expands, compresses, moves, becomes
visual or spoken) precedes the content map; milestone retitled "Your
artifact, ready to publish or present" (course briefs re-bridged
mechanically). Course stays poster-focused (D41).

**4. Studio 12 = "Special topic: agentic AI, release, and the next
cycle."** ch35/36 flip to role: core (the milestone checklist now lists
their products as prerequisites; course M15 already required them, so
book and course align). The closing review runs as a directed team with
**capability honesty**: declare who chooses each next step — you, a
fixed script, or an agent that plans and calls tools — and never call a
manually sequenced chat autonomous (GenAI Studio supports human-sequenced
workflows; agentic execution waits on a verified platform). ch35/37 IYT
recentered on the team record; the no-backfill rule stands; the release
audit, dossier, stopping rule, and release-or-withhold decision remain
the milestone's practice with the blocking gates intact. M15 integrity
repairs: the manufactured-override advice replaced by an
independent-check drill; the crosswalk version label "released artifact"
corrected to "release decision and next-cycle record". QUEUED for Davi:
the advanced agentic authoring tranche (workflow-vs-agent lesson content,
planner/replanner loops, tool-using agents with permissions and
receipts, layered guardrails, observability, a risk-based role menu) —
substantive new chapter material, scheduled, never smuggled into
contribution language.

**Figure and prose.** Road stages 5–6 relabeled ("write and bound, ready
the artifact"; "reproduce, package; agentic review, decide"); the
organization page opens and closes on the release DECISION, matching
D42's withhold semantics; PT/ES labels staged (D36 replay).

**Process.** Two-role Codex loop (gpt-5.6-sol, xhigh, read-only): mirror
partner merged with attribution
(`_adm/codex_collab/2026-08-05_d44-opening-s10-s12/`). Declined and
recorded: Lesson-5-first brainstorm; "Special topic: Agentic-AI research
practice" as the S12 title; the ch37 retitle (course deliverable
anchor). Diff review round (same model/effort): three findings, all
confirmed and applied — the banner updater's H1 branch no longer crashes
on reinsertion (used the computed anchor; path regression-tested); Studio
12's purpose line is capability-honest ("agentic where your tools truly
plan and act, human-sequenced otherwise"); and the road figure's alt text
was resynchronized with its visible labels.

## Decision 45: The flip — the book opens with your curiosity (2026-08-05)

**Ruling (Davi), overruling D43's Option-4 middle path and parts of D44.**
Studios 1 and 2 are FLIPPED so the studio-and-lesson reading order itself
realizes the arc *human curiosity → ledger and rules → verified AI
assistance → formal research question*, with fluid transitions and an
engaging undergraduate narrative; the curiosity opening is grounded in the
Einstein scientific-discovery framework as presented by the Google
DeepMind position paper "LLMs can't jump" (Zahavy 2026); and AI is allowed
at EVERY step of the book — the reader keeps the final decision, and for
brainstorming in particular AI must be usable from the first page, before
the ledger formally exists (relaxing D43's ledger-before-prompt invariant
by ruling; the pre-ledger exchange keeps a simple receipt that becomes the
ledger's first row, marked retrospective). Also ruled: Studio 10's D44
identity must reach its chapters, and every studio's lessons must visibly
connect to the studio's proposal.

**Structure (identity preserved).** Station `frame-the-inquiry` takes rank
1, retitled "Begin with your curiosity", holding `curiosity-to-problem`
(ch5, rank 5 → the book's Lesson/Chapter 1) with NEW checkpoint
`curiosity-committed-v0` and milestone "Your curiosity, committed".
Station `govern-the-work` takes rank 2, retitled "Govern the work and
declare your question", holding ch1–ch4 plus `question-kinds` (station
move, D38 precedent) as the arc-closing lesson; checkpoint
`question-declared-v0` moved with it (the station now carries both
checkpoints, presented sequentially) and the milestone is "Your rules and
your question". Studio/milestone page URLs moved with the ranks; legacy
URLs alias-redirect both directions (generator `LEGACY_RANKS`). Rubrics:
the curiosity checkpoint got authored criteria; governance criterion 5
covers both artifacts plus a dedicated declaration criterion.

**Content.** ch5 rebuilt as the opening lesson: the Zahavy/Einstein
discovery cycle (cited, attributed as a position, never a capability
theorem), abduction, AI as divergence partner from page one (the
structured brainstorm with NEW-labeling lives here), the four-move funnel
that STOPS at the research problem — units, outcomes, conditions, kind,
and reach belong to ch6's formal declaration, which now owns a field-card
"formal declaration" section and closes the arc as Studio 2's last
lesson. ch1 opens downstream of the jump, receives the brainstorm receipt
retrospectively into the fresh ledger, and runs the first verified
delegation on the reader's own problem. Six authored transition sentences
join ch5→1→2→3→4→6→7. Preface, organization page, and road figure follow
("Studio 1: begin with your curiosity").

**Studio 10 chapters** now route by format: ch27 opens on venue viewing
conditions (paper/talk/poster) with the poster as the scan-path case;
ch28 declares the gallery walk and print lock poster procedure (a
manuscript cold read and a timed rehearsal are not gallery walks); ch29
is "Research Pitches, Talks, and Seminars" with the
not-one-artifact-at-different-speeds decision; ch30's decision block is
channel-aware (live, reviewer report, editor query, written response).

**Alignment sweep (12 studios, applied):** ch8 closes by revising or
defending the declared question against the map; ch9/uncertainty
foundations say "before you inspect outcome-bearing fields", honest for
existing-data projects; ch16 says primary-pathway-plus-contrast, not "all
four"; ch17 keeps the contract provisional; ch20 closes with the
milestone's restart/environment/trace checks; ch31's bridge stands on the
claim table; ch32 labels the author's cold restart a solo proxy; ch33
stops presuming the Studio 11 capsule; ch37's no-AI bypass removed (the
honest minimum mode is one assistant playing the review roles — D44's
core ruling). Studio 8 needed nothing.

**Course.** Crosswalk re-mapped: M0 = ch5, `frame-the-inquiry`,
curiosity checkpoint (its authored curiosity-map substance fit the flip
naturally); M1 = ch1–4 + ch6, both governance checkpoints; W1/W2 units,
master plan, and M0/M1 submission rows re-anchored; bridges regenerated.
FLAGGED follow-on, not done: the nb01/nb02 SOURCE content rebuild (their
instructional identities are still the pre-flip sequence; generated
course surfaces carry the D41 rebuild-in-progress notice).

**Process.** Two-role Codex loop (gpt-5.6-sol, xhigh, read-only): the
mirror partner VERIFIED the structural design, contributed the ch5/ch1/
ch6 narrative drafts, the transitions, the S10 routing, and the sweep's
fix list, and caught a duplicate-numbering defect and a jump-attribution
overreach ("no tool can" → Zahavy's argued position) in the base. Merged
with attribution (`_adm/codex_collab/2026-08-05_d45-flip-s1s2/`). Diff
review round (same model/effort): five findings, all confirmed and
applied — the For Instructors adoption table and BOOK_MAP regenerated
(two freshness gates the pipeline had missed); M0's checklist, purpose,
and chapter references reconciled with the curiosity milestone (a
version-zero commitment, not "nothing is a commitment"); ch5's step-5
prompt and closing verification made problem-level (no field card before
Studio 2); the cold-test protocol re-scoped to the ruled flow (receipted
brainstorm before the ledger; retrospective first row; new hard gate: no
tool-chosen problem, no receipt-less exchange); and the legacy
`/stations/stationNN-*` URLs from before the flip now alias-redirect
alongside the studio ones.

## Decision 46: Studio 2 rebalanced — the declaration gets its own lesson (2026-08-05)

**Ruling (Davi).** Studio 2 carried four governance lessons against one
question lesson. Rebalance it, connect the two purposes, rename freely,
rewrite as needed — and do not be lazy.

**Structure.** A new core lesson, **"Declare Your Research Question"**
(`declare-your-question`, rank 62, semantic source and URL — the
D37-proven insertion path), closes the studio. It takes the
formal-declaration material D45 had stuffed into ch6 and performs the
declaration as GOVERNED WRITING: the field card first (freezing the
human decisions), then AI-drafted candidate wordings under a
**show-what-changed** discipline (every differing word accounted for, no
new topics, the tool never chooses), the boundary pair, the stranger
test, and a dated version zero. Its seeded worked example proves "the
sentence chooses the rows" (one simulated menu world; wording A counts
listed entree prices, wording B counts what a student pays; two different
growth numbers); its AI failure case is declaration-level silent scope
change. ch6 returns to its compass identity and is retitled **"Choose
Your Question's Kind and Reach"** (the old title presented prediction as
a third kind, against the inquiry framework). The studio is retitled
**"Set your rules, shape your question"**, its steps interleave rule
beats and question beats, and its milestone_reason states the connection:
the rules are not a preface to the question; they govern how it is
written.

**Threading.** ch2's delegation map covers the declaration work
(candidate wordings delegable; kind, reach, and boundary never); ch3's
SDIIVDD run targets a claim the reader's starting belief makes; ch4's
ownership statement starts with the question's words. Contributions
rewritten to carry the thread; the practice kit's faded task now plants
an AI candidate wording that silently adds a population, which the reader
must reject with a written reason. Assessment progressions corrected:
objective, setting_time, and claim_boundary are defined by the
declaration lesson.

**Course.** Crosswalk M1 anchors the new lesson (home anchor; six
lessons at W2 — the partner run measured the load at ~11.6k words before
the insertion and specified load controls: staged reading, ch6 + the
declaration treated as one two-stage question lab, M1 graded as one
integrated artifact, never six notebook submissions). M1's display title
is "Your Rules and Your Question" (slug immutable) in the brief, master
plan, and course_config; briefs, adoption table, BOOK_MAP, TOC,
pointers, companions, schedule, and guides regenerated; displays after
rank 62 shift by one. RECORDED for the flagged course-content phase
(with nb01/nb02 from D45): the M1 brief's hand-authored body, the nb02
source, and the W2 quiz/SRL rebalance.

**Declined, recorded:** Codex's ch2/ch4 retitles ("Decide What AI May
Do", "Put Your Name on the Work") — the research-director and ownership
vocabulary anchors course material; its full alternative chapter draft
(equivalent coverage; mine was validator-clean first).

**Process.** Two-role Codex loop (gpt-5.6-sol, xhigh, read-only): the
partner adopted the structure with guardrails (ch6 and the new lesson
own different decisions; no duplicated field-card work; load-neutral in
practice) and contributed the retitle package, the contribution thread,
the reject-drill faded task, and the progression moves. Merged with
attribution (`_adm/codex_collab/2026-08-05_d46-studio2-balance/`). Diff
review round (same model/effort): five findings, all confirmed and
applied — ch6's new decision block had named prediction a third KIND
(fixed: descriptive or causal, prediction as its own compass position);
the worked example now computes the comparison its sentence asserts (a
retrieved overall-index benchmark in the code) and wording B is labeled
as what its rows measure; the declaration gains a required
uncertainty-and-limitations step (IYT, studio step, contribution, and
rubric criterion); the wording prompt carries the full field card so
show-what-changed can actually be enforced; and the canonical lesson
counts (CLAUDE.md, COURSE_MASTER_PLAN partition) now say 40.

## Decision 47: The completeness pass — every workbook developed, the chain explicit, every path drawn (2026-08-06)

**Ruling (Davi).** Assuming the book's goal — anyone, especially an
undergraduate, finishes with a fully developed research artifact after
completing every "It is your turn" and every studio milestone — ensure:
(1) IYT material and companion notebooks are fully developed and aligned
with their studio milestone; (2) all milestone material, especially the
workbook notebooks, is complete and fully developed; (3) completing all
milestones delivers what the book promises; (4) a figure presents every
path through the book, in "How this book is organized", matching the
existing figure's standard.

**Workbooks (A4 complete, 12/12).** Practice kits authored for Studios
5–12, continuing the restaurant-prices thread down the whole road: route
declaration with a causal-contrast drill (S5), provenance + measurement
(S6), declared-analysis result with seeded starter CODE (S7), pre-listed
robustness grid (S8), claim-evidence rows with a trace-or-cut drill
(S9), venue contract with a real mode test (S10), the five-part capsule
with the solo-proxy label (S11), and a capability-honest closing review
whose worked example WITHHOLDS pending a named repair (S12). Simulated
teaching records are labeled as such.

**Alignment (the partner audit, applied).** The 12-studio IYT ↔
contribution ↔ milestone audit found most alignments exact; every
confirmed repair shipped — highlights: ch5 dates the opening lines as
version zero; ch3 records a check's outcome even when nothing changed;
S3 carries the revised declaration; S4's MIDA carries every Contract v0
field; S5's prediction contrast is a real drill and its milestone
carries the bounded skip rule (primary + ONE contrast, resolving the
route-guide/checklist contradiction); ch17 closes with acquisition,
data-management, and the realized permission recheck; ch20's
contribution carries the restart/environment/trace closes; ch33 now
assembles the FULL stand-alone note (methods, results with uncertainty,
discussion, references, disclosure, package pointer); ch29 expands to
venue length; S11 assembles-then-runs and freezes a dated manifest;
ch35 declares each role's capability.

**The chain, explicit.** Every milestone's "What you bring" opens with a
generated carry-forward line naming the previous milestone's artifact as
an input, and authored `bring_note` rules bound the skip logic (S5) and
name the format inputs (S10). Completing the twelve milestones now
demonstrably assembles: the bounded note (M9) → the publication- or
presentation-ready artifact (M10) → the reproducible package (M11) → the
release-or-withhold decision with dossier and next-study agenda (M12).

**The all-paths figure.** `part1_paths.png`, generated beside the road
figure in the same monochrome standard: one spine (Studios 1–4), the
five-way pathway branch at Studio 5 with the optional overlay, the
rejoin (6–9), the four-way format branch at Studio 10, the close on YOUR
ARTIFACT. A new "Choose your path" section presents it: five pathways
in, four formats out, twenty end-to-end roads, one spine.

**QUEUED (tracked, not silently claimed):** route-specific Studio 7
analysis variants — the five A1 pilot paths need worked analysis
recipes beyond the observational-descriptive thread; a content tranche
for Davi to schedule. The second A1 pilot (D43 protocol) remains the
evidence standard for lifting the preface's bounded promise.

**Process.** Two-role Codex loop (gpt-5.6-sol, xhigh, read-only): the
partner's audit table and promise-chain findings were merged with my
kit authoring and figure implementation; its `receives:`/`bring_rule:`
design was adopted as the generated carry-forward + `bring_note`
mechanism. Attribution in
`_adm/codex_collab/2026-08-06_d47-completeness/`. Diff review round
(same model/effort): three findings, all confirmed and applied — the
Studio 7 starter now lands as a REAL executable code cell in the
workbook (generator splits fenced starters; the cell was executed as a
test), ch3's document step records the check's outcome either way (an
agreeing check no longer makes the workflow impossible), and Studio 5's
contrast rule names its own selection (any other route the reader
chooses) instead of pointing at a mapping the route guide never had.

---

## D48 — The plagiarism and attribution pass (2026-08-05)

**Ruling.** Davi asked for an audit of the book's plagiarism exposure,
especially where EDR|AI incorporates and "translates" the approach published
in RDSS (Blair, Coppock & Humphreys, *Research Design in the Social
Sciences*), with findings presented BEFORE any edit. After reviewing them he
ruled: apply everything necessary, replace the copied figures with our own
drawn in the house style of the "How this book is organized" figure, and have
Codex review the result.

**What the audit found.** Two independent tracks (a Codex research-integrity
audit in mirror mode and my own close-text comparison against RDSS pages
fetched verbatim) agree: **there is no verbatim or near-verbatim RDSS prose
anywhere in `book/*.qmd`.** The book's expression is its own. The real
exposure was attribution and licensing, in five kinds:

1. **A positioning statement that contradicted D43.** `references.bib` called
   RDSS "the theory text EDR|AI translates". The preface says the opposite,
   correctly. Now: "EDR|AI draws on and adapts its research-design framework."
2. **Two close conceptual paraphrases** at the openers of ch11 and ch13,
   tracking RDSS's distinctive framing of the observational-descriptive and
   experimental-descriptive pathways with no citation in either chapter.
3. **Framework use without point-of-use credit.** MIDA was introduced as
   "this book calls them MIDA"; "diagnosand", a term its authors coined, was
   used as assumed vocabulary; the pathway chapters and the Studio 4 pages
   taught an adapted design library with no local credit. A preface nod does
   not cover independently linkable pages.
4. **Citation-accuracy defects.** The *Science* surprise essay's authors were
   wrong in the bibliography (Michael Petroff / Molly King, for **Casey**
   Petroff and **Gary** King); ch31 attributed the book's own
   verification-disclosure rule to ICMJE, which requires only tool and
   purpose; ch27's screen-reader claim rested on a color-vision paper rather
   than WCAG; ch11 taught the four sampling groups as strictly nested, which
   a sampling frame is not.
5. **Licensing.** Eighteen exact RDSS figure conversions were committed to a
   public repository, and the repo's only license was MIT pointed at
   everything, with no statement covering book prose or third-party material.

**What was applied.** Point-of-use credit at every first teaching surface
(ch9, ch10, ch11, ch12, ch13, ch15, ch16, Studio 1, Studio 4 on both its
opener and its milestone step); the two paraphrases reworded to name and cite
the pathway they follow; ch14 now says plainly that prediction is EDR|AI's
own fifth pathway, extending rather than adapting RDSS's library, and
uncertainty-foundations carries the inquiry/estimand lineage sentence. Two
definitions were widened for fidelity, not just credit: a data strategy
includes **measurement** (stated outright in the 2019 article: "Measurement
techniques are also a part of data strategies"), and an answer strategy
includes **uncertainty and interpretation** (the 2019 article demonstrates the
uncertainty outputs; RDSS 2023 is where cleaning, estimation, interpretation,
and uncertainty are explicitly enumerated). The narrower versions were teaching
less than the labels promise. "Diagnosands" left the Studio 4
produces line and the Milestone 4 rubric in favour of the book's own plain
language (bias, wobble, and how often it would detect), with the coinage
credited where ch10 actually teaches it. Bibliography: authors corrected with
DOI added, plus two verified new records — `blair2019declaring` (APSR 113(3),
838–859, **CC BY 4.0**, the article that introduces both MIDA and diagnosands)
and `w3c2024wcag22`.

**The figures: the book draws its own.** The 18 `rdss_fig_*.png` files were
deleted. Attribution in a README is not permission, and the MIT license on the
`rdss` R package does not establish redistribution rights for converted book
figures. Nothing referenced them (their assignments pointed at v1 notebooks,
retired at tag `v1-compass-build`). In their place,
`scripts/build_book_concept_figures.py` generates three diagrams in the
monochrome house style of `build_book_part1_figure.py`, localized per edition
and frozen-edition aware: **`mida_map.png`** (ch9 — the four parts split into
what you assert on paper and what you run, with the alignment check as a
dashed arrow), **`diagnose_loop.png`** (ch10 — declare, diagnose, redesign,
with the honest call sitting outside the loop), and **`sampling_groups.png`**
(ch11 — the four groups drawn honestly, the frame overlapping rather than
nesting inside the accessible population). The standing rule, restored in
`planning/SOURCE_AUDIT.md` §8: re-implement, never embed.

**The datasets: the MIT notice now travels with the copies.** A live exposure
neither the preface nor the audit brief anticipated: the five CSVs in
`notebooks/data/` are redistributed from the MIT-licensed `rdss` package, and
MIT requires its notice to accompany every copy. Prose credit alone does not
satisfy it. `notebooks/data/LICENSE-rdss.txt` now reproduces the upstream
notice verbatim (YEAR 2021; Graeme Blair, Alexander Coppock, and Macartan
Humphreys, verified on CRAN) and `make_dataset_zip.py` ships it inside
`honr46400_datasets.zip`.

**Rights.** `LICENSE` now separates three kinds of material: code and
infrastructure under MIT; book and course text under the author's copyright,
all rights reserved; third-party quotations, figures, and datasets excluded
and governed by their own sources. **The all-rights-reserved default for the
text is a placeholder Davi can loosen** (a Creative Commons option was
offered); it forfeits nothing in the meantime.

**Verification discipline.** Every new bibliography claim was opened before it
was written. The 2019 APSR PDF was retrieved and read rather than trusted:
it confirmed the page range, the CC BY 4.0 licence, that the article
introduces both MIDA and "diagnosands", and — usefully — that measurement
belongs to the data strategy, which is what the ch9 fidelity fix now teaches.
Codex's proposed WCAG record carried the wrong year (2023); the published
Recommendation is dated 12 December 2024, and the record says so. Two Codex
claims that could not be verified (the pages and licence of the 2019 article
from the landing page alone) were verified from the PDF rather than repeated
on trust.

**Not applied.** Nothing was deferred silently. Codex's optional
Ask-Verify-Document clarification was judged unnecessary: the book presents
the mnemonic as its own habit, which it is, and its NIST citation supports the
underlying guidance.

**Process.** Codex partner audit (gpt-5.6-sol, xhigh, read-only, web enabled)
in mirror mode, merged with my own close-text track; artifacts and the merged
findings report in `_adm/codex_collab/2026-08-06_d48-plagiarism-audit/`.
PT/ES replay logged as TRANSLATION_BACKLOG item 20 (D36 freeze holds; the
figure script already carries PT and ES labels).

**Review round (same day).** Codex reviewed the pass as a research-integrity
specialist (gpt-5.6-sol, xhigh, read-only) and cleared the three new figures as
independent expression, but not the pass as a whole. Twelve findings, all
applied. Eight were errors in my own new text: Jasper Cooper was made an author
of the 2023 book (he coauthored the 2019 article only); the diagnosand
etymology ran backwards; MIDA was asserted as a universal rather than a named
framework; RDSS's subtitle was printed wrong; the MIDA figure's row labels
implied D and A are execution rather than declaration; the sampling figure put
"ineligible units" inside the target population and drew duplicates as a
region; ch11 blamed its causal limit on the absence of assignment, which is
also true of the observational-causal pathway; and ch5 called a student's
expected answer a measure of what the project taught anyone, where the Science
essay's gap is audience-level. Four were surfaces the first pass never reached:
`index.qmd` still said the book "translates RDSS" and called it an "open text";
Studio 5's route table, nb04, and nb05 taught borrowed vocabulary uncredited;
the LICENSE did not separate notebook code cells from notebook prose cells; and
WCAG's normative scope is web content, not printed boards.

**The lint (Codex's counter-proposal, adopted in part).** Codex argued that
scattered prose edits regress because studio pages and notebooks are generated
and drift silently, and proposed a rights-and-lineage manifest as the source of
truth with a lint over it. The full manifest is a project-sized task and is
queued below; the lint is not, so it shipped:
`scripts/audit_attribution.py` fails if any public teaching surface uses
**MIDA** or **diagnosand** without naming its source in the same file. It found
three companion notebooks on its first run, all fixed at the chapter source.

**QUEUED for Davi (flagged, not silently resolved).**
1. **The upstream data rights chain.** The `rdss` package's MIT licence covers
   the packaging, not each original investigator's authorization to
   redistribute their study data publicly, and the package documentation limits
   the LAPOP-derived resample to teaching use. `notebooks/data/README.md` and
   `planning/SOURCE_AUDIT.md` §8 now say exactly that instead of claiming the
   question is settled. Resolving it means a per-file manifest (archive/DOI,
   owner, licence or permission, allowed transformations, hash against the
   source archive), or replacing files with openly licensed or synthetic
   equivalents.
2. **The book's licence choice.** All-rights-reserved-but-free-to-read is a
   placeholder. A deliberate Creative Commons licence (CC BY, or CC BY-NC if
   commercial reuse is the worry) is available whenever Davi wants it.
3. **The Palmeiras crest** on the author page has no documented brand-use
   basis. Left in place because it is Davi's own bio page and his call.
4. **The rights-and-lineage manifest** covering every framework, dataset,
   quotation, and image.
5. A full near-verbatim comparison against the entire Princeton text remains
   **UNVERIFIED**; both passes checked changed passages, known RDSS surfaces,
   and repository assets, not every sentence against a licensed corpus.

## Decision 49: One Studio per week — the course realigned to the 40-lesson book (2026-08-05)

**Ruling (Davi).** Three directives:

1. **Update the course to the book's new version, structure, and design.**
   The book moved past the D41 alignment: 40 lessons (D46 added
   `declare-your-question`), Studio 1 is now the reader's curiosity alone
   (D45's flip), Studio 2 absorbed the question lessons, Studio 10 became
   venue-neutral and publication-ready (D42/D44), Studio 12 is the agentic
   special topic (D44), every workbook is developed (D47), and attribution
   is governed (D48).
2. **Every lecture from Week 1 Wednesday to the last lecture of Week 16 is
   updated and rewritten as needed.** Week 1 Monday stays the
   instructor-led orientation and is the only lecture exempt.
3. **One Studio per week.** Monday and Wednesday teach that Studio's
   LESSONS together with their "It is your turn" work; **Friday IS that
   Studio's MILESTONE.** The exceptions are Week 1 and the date-driven
   weeks.

**The mapping this produces — Studios 1–12 on Weeks 1–12.** It is not an
accident that this fits: the fixed dates land exactly where the book
already wants them.

| Wk | Studio | Course M | Book M | The fixed date it carries |
|---|---|---|---|---|
| 1 | S1 Frame the inquiry | M0 | 1 | Mon = orientation (exempt) |
| 2 | S2 Govern the work | M1 | 2 | — |
| 3 | S3 Ground in evidence | M2 | 3 | short week (Labor Day) |
| 4 | S4 Declare and diagnose | M3 | 4 | — |
| 5 | S5 Develop the pathway | M4 | 5 | — |
| 6 | S6 Govern data and measurement | M5 | 6 | — |
| 7 | S7 First reproducible analysis | M6 | 7 | **URC abstract gate, Fri Oct 9** |
| 8 | S8 Stress-test and adjudicate | M7 | 8 | short week (October break) |
| 9 | S9 Write, bound, disclose | M8 | 9 | — |
| 10 | S10 Adapt and defend | M9 | 10 | — |
| 11 | S11 Reproduce and package | M10 | 11 | **poster lock, Fri Nov 6, TERMINAL** |
| 12 | S12 Release and next cycle | M11 | 12 | — |
| 13 | *(revisits)* public test | M12 | 10 v2 | **Expo, Tue Nov 17** |
| 14 | *(practice)* peer cold run | M13 | 11 practice | **async, Mon Nov 23** |
| 15 | *(revisits)* note v1 + package | M14 | 9 v2 + 11 v2 | — |
| 16 | *(revisits)* defenses + release | M15 | 12 v2 | **terminal, Fri Dec 11** |

**Why the fixed dates fall right.** The URC abstract needs a result, and
Studio 7 produces the first one (Week 7 Friday = Oct 9). The poster lock
needs reproduced numbers, and Studio 11 is the reproduction gate — so the
numbers that lock onto the poster on Nov 6 are the numbers that just
reproduced from a clean package. And Studio 12's release audit sits the
week BEFORE the Expo, which makes the Expo the release rather than a
rehearsal: you audit release before you release. The four post-studio
weeks then do what only they can — the public test, the peer cold run
(on someone else's package, since your own already exists), the revision
that adjudicates both streams of evidence, and the defense.

**Course policy recorded in the crosswalk, never inferred from the book:**
the five pathway lessons stay route-required (own route + one assigned
contrast; hybrid only for staged designs), and BOTH Studio 10 genre
branches are required because this course's venue contract mandates a
poster (the Expo) and an oral evidence defense.

**Load, stated honestly.** Two weeks carry more than their meetings do
comfortably: Week 2 teaches six lessons in two lectures (Monday takes the
four governance lessons as one arc, Wednesday the two question lessons),
and Week 8 teaches four lessons in ONE lecture because October break
removes its Monday. Week 8's lecture teaches the spine that unifies the
four — pre-list, run commensurable panels, read a negative test against
the null reference spread, adjudicate every flag against a real check —
and the four chapters carry their depth through their IYT sections. This
is the price of one-studio-per-week and it is recorded, not hidden.

**Identity untouched:** the calendar, the 50-minute frames (D22/D33/D34),
assessment weights, notebook slugs and filenames, course milestone ids
M0–M15, lesson and station ids, and every book URL. Display titles and
artifact specs change; identifiers never do.

**Merged from the partner run (adopted).** The independent Codex design
converged on the same week↔Studio map, which is itself evidence the
mapping is right, and caught one real gap: the poster lock and the Expo
each change a book artifact materially, so both now carry bridges instead
of changing it silently. Book Milestone 10 runs v1 (artifact ready, M9) →
v2 (the locked print edition, M10) → v3 (publicly presented, M12), and
Book Milestone 12 runs v1 (the release decision, M11) → v2 (released, with
what the public test returned, M12) → v3 (the final release, M15).

**Process.** Built through the two-role Codex loop plus multi-agent
orchestration: a mirror-mode Codex design partner ran the same assignment
independently while a 16-agent workflow wrote one teaching spec per week
and a semester-coherence critic audited them together; implementation ran
as further workflows over the briefs, the schedule, and the notebooks;
a Codex review round closes the build. Artifacts in
`_adm/codex_collab/2026-08-05_d49-one-studio-per-week/`.

**D49 implementation and review record (2026-08-06).** The realignment
shipped in full and both review legs are applied.

**Built:** the machine layer (crosswalk rewritten as a 40-lesson bijection
with twelve checkpoints firing once and the exception weeks carrying
revisits; config v4; milestone chain and master plan v4); all 16 milestone
briefs rewritten to their studios' `produces`; **all 16 course notebooks
and all 16 studio notebooks rebuilt**, every one executed clean and
validated; all 43 meeting dictionaries and the 16 generated session
guides; the 15 weekly quiz banks re-scoped and parity-gated; the colleague
cadence re-derived (studio N = week N, so the ten scored audits are simply
Weeks 2–6 and 8–12, Week 1 modeled and Week 7 an unscored preview).

**Orchestration.** A mirror-mode Codex design partner ran the same
assignment independently and converged on the identical week↔Studio map —
then caught a gap worth the whole run: the Nov 6 lock and the Expo each
materially change a book artifact but carried no bridge, so those
artifacts would have changed silently. Book Milestone 10 now versions
v1 (artifact ready, M9) → v2 (locked print edition, M10) → v3 (publicly
presented, M12), and Book Milestone 12 v1 (release decision, M11) → v2
(released, M12) → v3 (final, M15). Implementation ran as six workflows:
16 week specs plus a semester-coherence critic, 16 briefs, three notebook
waves, the schedule, the studio notebooks and quizzes, and two fix passes.

**The semester critic found seven defects**, all applied: eleven scored
colleague audits scheduled against a ten-audit rule (ruled and derived
once, with a standing rule never to hand-number an audit again); Week 14
still telling students their package work lay ahead when D49 has them
building it in Week 11; Week 13's Milestone version labels contradicting
the crosswalk on a criterion every station rubric grades; the `foos_etal`
example re-revealing the same surprise across five weeks (one owner per
beat now); the preliminary-edition label graded in Week 11 but taught
nowhere (it belongs to Studio 10's venue genre); and Book Milestone 10 v2
having no home in the lock week.

**The Codex review round returned fix-forward with eight findings**, all
applied. The five that mattered: Week 8's quiz and workbook collapsed a
negative CONTROL into a permutation-style null pile and called an
inside-the-spread reading a "clean pass" — both prohibited by the
misconception manifest, and invisible to the gate because quiz banks are
gitignored and the phrasing evaded the regex (the two checks are now
taught and assessed as different objects, with a bounded verdict replacing
"clean pass" here and in the Week 8 lecture notebook); the M7 workbook
stated the commensurability rule and then pooled sample and measurement
changes into one spread panel; Week 8's Friday could not fit its work, so
Wednesday now ends with a frozen unrun scaffold and Friday executes and
adjudicates only, with pending recorded honestly as pending; the M10 gate
code compared every poster number against one shared value and demanded an
inferential bound on all of them, so two estimates could never both pass;
and the Reproducibility Auditor was mandatory at M10 in the schedule while
the registry, brief, and workbook never required it — removed, since no AI
reviewer can make an author's own rerun independent, and kept required at
M13 where the package is someone else's.

**A gate that had stopped gating.** The misconception self-test deletes a
required correction from every surface and demands the scan fail, but it
mutated raw file text while the scanner reads normalized notebook JSON, so
a phrase that wrapped across notebook source lines survived the deletion
probe. The probe now mutates per cell on the joined source, and the full
self-test passes again.

**Left for Davi, deliberately not changed:** `book/part4-credible-evidence/22-diagnostics-and-negative-tests.qmd`
uses the same "clean pass" wording for a negative test. The passage teaches
the correct rule (read against the spread, never exact zero) and the
wording is a nuance, but the book is fixed under D49 and frozen for chapter
review under D35, so the call is his.

**Standing after the build:** all validators green — 16 student + 16
instructor + 16 studio notebooks structurally valid and voice-clean, the
misconception gate clean and self-proving, citation integrity clean across
16 notebooks and 41 chapters, book architecture and sync consistent at 40
lessons, coverage clean across 43 meetings, calendar invariants holding,
and the milestone system consistent with every fixed date anchored.

---

## D50 — The conference block: milestone renumbering and the post-conference studios (2026-08-22)

**Decision.** The course milestone track is renumbered **M0–M15 → M1–M17**, and
Studios 11 and 12 move from Weeks 11–12 to Weeks 15–16. Weeks 11–14 become the
**conference block**. Concretely:

1. **M1–M10 present Book Milestones 1–10 one-to-one and in order.** The old
   off-by-one (course M(n) presented Book Milestone (n+1)) is gone. The course
   is 1-based like the book.
2. **Weeks 11–14 anchor no new lesson.** They carry Book Milestone 10 forward as
   versions 2, 3, and 4, and they exist to turn the Studio 10 artifact into a
   printed poster that has already survived criticism, then to deliver it:
   - **M11 Poster first draft** — due AT CLASS on the Week-11 Wednesday, because
     the structured four-reviewer round runs in that same session.
   - **M12 Peer review submission** — the four review surveys, completion-graded.
   - **M13 Final poster lock** — **Sunday, November 8, 11:59 PM, TERMINAL**.
   - **M14 Go-public package** — audience analysis, three timed pitches
     (30 s ≤75 w · 90 s ≤200 w · 2 min ≤300 w), poster-integration outline,
     question strategy, and the public invitation post.
   - **M15 Conference reflection** — the coded audience tally and its
     adjudication, due Sunday, November 29.
3. **Studios 11 and 12 run POST-conference on Weeks 15–16, in the STANDARD
   frame**: Monday and Wednesday teach the studio's lessons with their "It is
   your turn" work, and Friday IS that studio's milestone. **M16** presents Book
   Milestone 11 (and carries the research note revised after public criticism);
   **M17** presents Book Milestone 12 and closes the course, terminal.
4. **The peer cold run moves in-class.** The Thanksgiving asynchronous
   replication module is retired. On the Week-15 Wednesday a colleague runs your
   capsule from your written instructions alone while you run theirs, and Friday
   is the repair block. Handing packages across a table beats doing it alone over
   a holiday, and it makes the reproduction failure visible in the room.
5. **Calendar.** Friday, November 20 becomes **asynchronous** (post-Expo
   audience-data capture), joining Monday, November 23 (in-person 42 → 41,
   async 1 → 2; total stays 43). `poster_deadline` moves from 2026-11-06 to
   **2026-11-08**, matched to QM 47400's lock so both courses print on one run.

**Rationale.**

- **Packaging and release do not gate poster development.** Book Milestones 11
  and 12 are about reproducing and releasing a finished result. Under D49 they
  sat between the last studio and the Expo, which spent two of the four
  pre-conference weeks on work the poster does not need, and left no room to
  criticise the poster before it locked.
- **The new order is more faithful to the book, not less.** Book Milestone 12 is
  "release and next cycle", and release genuinely comes after the public test:
  what the room returns is part of what you release. The book's twelve Studios
  keep their own order; the course inserts a conference block between Studio 10
  and Studio 11. The independence axiom (D35) is untouched — the book's spine
  was never renumbered to suit the course.
- **Peer criticism before the lock.** Four readers who did not confer are four
  checks. A defect found in class costs an evening; the same defect found at the
  Expo costs the claim.
- **The print window.** Locking Sunday night gives a full working week to print
  and hand posters back, so the Week-12 Friday studio and the Week-13 Monday
  dress rehearsal both run on the real printed board.

**Imported from QM 47400** (both courses present at the same URC Expo): the
draft-abstract milestone (M6), the **conference application with its
proof-of-submission PDF** (M7, which the course previously lacked entirely), the
poster first draft on a shared template and rubric, the timed-pitch
specification with word ceilings, the invitation post, the structured peer-review
instrument, and the proof-of-presentation photograph. QM 47400's own poster
deadline moved from Tue Nov 10 to Sun Nov 8 in the same pass.

**Not imported:** the group contract, the intra-group peer evaluation, the
two-round instructor/TA meeting schedule-and-confirm cycle (all group-project
machinery; HONR 46400 projects are individual), and Poster-to-Product.

**Mechanics.**
- `course_config.yaml` — calendar, the 17-milestone map, `weeks` with `also_due`,
  GenAI Studio touchpoints repositioned (Poster Critic moves to the DRAFT, M11,
  where criticism can still change the poster).
- `planning/COURSE_BOOK_CROSSWALK.yml` — 17 rows; new `also_nb:` field for a
  milestone that spans two calendar weeks (M15 covers Weeks 13–14).
- `scripts/schedule_data/part3.py`, `part4.py` — meetings 29–43 rebuilt; the
  Studio 11 and Studio 12 lecture records were RELOCATED rather than rewritten.
- Validators updated: `validate_milestones.py` (17 milestones, new anchors),
  `validate_book_architecture.py` (M1..M17; the nb column is no longer a
  partition), `validate_book_sync.py` (`also_nb`), `validate_session_readings.py`
  (a studio's calendar week is READ from the crosswalk, never assumed equal to
  its rank), `validate_calendar.py` (two async labels, the Nov 8 lock).
- Notebooks: nb11 and nb12 are new conference-block notebooks; the Studio 11 and
  Studio 12 notebooks became nb15 and nb16. The D49 revision and close notebooks
  are archived at `_production_kit/nb_sources_d49_retired/`.
- Briefs: 10 renamed +1, three new (M11, M12, M14), four repurposed, two archived
  under `_research_project/2026Fall/_retired_d50/`.

**Superseded:** D49's "Studios 1–12 on Weeks 1–12" for Weeks 11–16 only. Weeks
1–10 are untouched, and the D49 shape still governs them.

---

## D51 — QM474 Final Project grading adopted for individual HONR projects (2026-08-22)

**Decision.** HONR 46400 adopts the operative Fall 2026 QM474 Final Project
proportions — **30 / 20 / 10 / 20 / 20** — while preserving this course's five
individual projects. The standalone **Research artifact
(paper/chapter/note) 10%** course category is retired and its ten course points
move into **Final Project**, which rises **20% → 30%**. The top-level assessment
contract is now Attendance 1% · Participation 9% · Quizzes 20% · Student
Research Lead performance 20% · Final Project Milestones 20% · Final Project
30% = **100%**.

**Reference adjudication.** QM474's current canonical project reference, source
syllabus, rendered syllabus, and Brightspace reconciliation agree on five
components: Milestone Deliverables 30% · Peer Evaluation 20% · Peer Review 10%
· Conference Poster Presentation 20% · Instructor/TA Evaluation 20%. Its older
40/20/40 summary is stale and is not imported.

**The individual-project mapping.** HONR keeps QM474's five proportions, but
maps the functions to work this course already requires:

| QM474 component | HONR 46400 equivalent | Share of Final Project | Course points |
|---|---|---:|---:|
| Milestone Deliverables | **Final Research Artifact and Milestone Synthesis** — the final paper, chapter, or research note | 30% | 9 |
| Peer Evaluation | **Individual Research Process and AI-Management Portfolio** — accountability demonstrated by the student's own ledger, checks, conflicts, and overrides | 20% | 6 |
| Peer Review | **Peer Review** — structured reviews of classmates' posters and a record of how criticism was used | 10% | 3 |
| Conference Poster Presentation | **Poster and Expo Presentation** — the individual locked poster and required public presentation | 20% | 6 |
| Instructor/TA Evaluation | **Instructor Evaluation and Evidence Defense** — the instructor evaluates integrative command of the final dossier through the individual oral defense | 20% | 6 |
| | **Total** | **100%** | **30** |

The first slot does not repeat M1–M17: HONR's developmental submissions remain
a separate 20% top-level category, so the 30% project slot evaluates their
integrated final scholarly artifact. Under the exact QM proportions, the final
paper/chapter/note is directly worth 9 course points rather than the former 10;
the entire former 10-point category still enters Final Project, and the fifths
redistribute one point across the other terminal evidence.

**Scoring determinism.** Each Final Project grade item produces an independent
0–100 score: the M17 Final Research Artifact rubric; the M17 Individual Research
Process and AI-Management Portfolio rubric; the M12 Final Project Peer Review
rubric; `0.70 ×` the M13 poster-quality score plus `0.30 ×` the M15 live Expo
presentation score; and the instructor-scored Evidence Defense Protocol rubric.
M12/M13/M15/M17 milestone scores remain process scores and are not inputs to
those Final Project calculations. The `70/30` split is an HONR operational
ruling inside QM474's imported 20% Poster Presentation slot: the persistent,
auditable poster carries the majority and public explanation/question handling
remains material.

**What does not transfer.** No group contract, intra-group peer evaluation,
teammate score adjustment, group meeting cycle, or Poster-to-Product assessment
is created. HONR's peer review remains cross-project criticism performed by each
student. No TA is assumed.

**Participation wording.** The public syllabus paragraph is exactly:
`Participation includes feedback surveys, lecture-notebook completion, and other constructive contributions to the course.`
This does not abolish the colleague audits; they remain one possible constructive
contribution rather than a separately promised syllabus subcategory.

**Implication.** `course_config.yaml`, `syllabus.qmd`,
`planning/ASSESSMENT_ARCHITECTURE.md`, `planning/COURSE_MASTER_PLAN.md`, the
Brightspace generator and its ignored output, nb01's grading table, and the
M13/M15/M16/M17 grading language must remain synchronized. D22/D31/D41 remain
historical records; D51 supersedes their assessment-weight statements only.

---

## D52 — One Final Project with QM474's same five component items (2026-08-23)

**Decision.** This decision explicitly supersedes **D51's grading design**.
HONR 46400 no longer splits project grading between a 20% Final Project
Milestones category and a 30% Final Project category. Those two categories merge
into exactly one top-level **Final Project worth 50%**. The full course contract
is Attendance 1% · Participation 9% · Quizzes 20% · Student Research Lead
performance 20% · Final Project 50% = **100%**.

**The five items are not translated or renamed.** The Fall 2026 QM474 public
`../../../predictive_analytics/2026F_predictive_analytics_QM474/syllabus.qmd`
supplies the exact labels; its canonical project reference
(`_final_project/2026F/final_project_milestone_reference.md` in the QM474
repository) confirms the internal shares while abbreviating the last two labels:

| Final Project item | Share of Final Project | Course points |
|---|---:|---:|
| **Milestone Deliverables** | 30% | 15 |
| **Peer Evaluation** | 20% | 10 |
| **Peer Review** | 10% | 5 |
| **Poster Presentation at the Purdue Undergraduate Research Conference** | 20% | 10 |
| **Instructor/TA Evaluation** | 20% | 10 |
| **Total** | **100%** | **50** |

This supersedes D51's functional substitutions: Final Research Artifact and
Milestone Synthesis is not a component name; Individual Research Process and
AI-Management Portfolio does not replace Peer Evaluation; Poster and Expo
Presentation does not replace the conference-presentation item; and Instructor
Evaluation and Evidence Defense does not replace Instructor/TA Evaluation.
The paper, portfolio, poster rubric, and defense remain graded evidence inside
the five named items.

**Project mode.** Individual work is the default. Students may complete a group
project only with instructor approval before shared work begins. With the
five-student enrollment, at most one group of two or three may be approved.
Approval must
preserve at least three active projects so every student can review at least two
other live projects. It must also permit a Peer Evaluation plan with two
observers per individual researcher and a nonempty submission set for every
student. It does not change the five items or their weights. Shared artifacts
receive common rubric-row scores; all explicitly individual performances and
records remain individually scored, so milestone scores may differ only through
those individual rows.

**Peer Evaluation remains actual peer evaluation.** For an approved group, each
member confidentially evaluates every teammate, with no self-rating, following
QM474's mechanics. For an individual project, the instructor assigns two project
peers early enough to observe scheduled studio work, milestone checks,
reproduction work, and defenses; those classmates confidentially evaluate the
researcher's observable preparation, research contribution, communication,
dependability, and reciprocal support. Peer Evaluation is per student and is
separate from Peer Review, which scores each student's structured criticism of
other projects. Every student receives a nonempty set of evaluations to submit;
the classmates a student rates need not be the classmates who rate that student.

The HONR Peer Evaluation conversion is explicit because QM474 does not publish a
1–5-to-percentage formula: `received_rating_score = min(100, 100 × mean received
rating / 3)` and `item score = 0.80 × received_rating_score + submission points`.
Complete required evaluations with usable comments earn 20 submission points;
non-submission earns 0 submission points and therefore reduces only the
non-submitter. A missing rating is omitted from the intended recipient's mean.
If evaluator non-submission leaves no valid received rating after instructor
follow-up, the intended recipient receives the neutral 80-point received-rating
portion (equivalent to a mean rating of 3); no substitute evaluator is added
after the observation period. Any moderation of strategic ratings is
documented.

**Deterministic scoring.** Milestone Deliverables is the equal-weight mean of
the seventeen M1–M17 scores. Every student completes Peer Review. Poster
Presentation at the Purdue Undergraduate Research Conference is `0.70 ×` M13
poster quality + `0.30 ×` the student's M15 live presentation; a group shares
only the poster-quality subscore. Instructor/TA Evaluation is `0.50 ×` M17 Final
Research Artifact + `0.25 ×` M17 AI-management portfolio + `0.25 ×` individual
Evidence Defense; a group shares only the final-artifact subscore. The
instructor records the last item if no TA is assigned.

**No duplicate raw scores.** M12, M13, M15, and M17 remain milestones inside
Milestone Deliverables, but their milestone rubrics score process, timeliness,
versioning, and response. Their distinct terminal rubrics feed Peer Review,
Poster Presentation at the Purdue Undergraduate Research Conference, or
Instructor/TA Evaluation. No raw rubric score is copied into two component
calculations.

**Participation wording remains locked.** The public syllabus paragraph is
exactly: `Participation includes feedback surveys, lecture-notebook completion, and other constructive contributions to the course.`

**Supersession boundary.** D52 supersedes D51's top-level weights, five renamed
components, individual-only assumption, and scoring formulas. D51 remains in the
record as the superseded decision. D22/D31 retain their historical force except
where their assessment-weight statements conflict with D52; D50's calendar and
milestone dates are unchanged.

---

## D53 — The Final Project syllabus text is QM474's, adopted verbatim (2026-08-23)

**Decision.** The public syllabus section `### Final Project (50%)` is now the Fall 2026
QM 47400 Final Project section **copied word for word**, with only the changes listed
below. D53 changes **no weight, no component name, and no scoring rule** — D52 remains
the governing grading decision in full. What changes is *where the operational detail
lives* and *how the syllabus reads*.

**Instruction.** Davi, 2026-08-23: "replace the Final Project section in the course
webpage syllabus (and all syllabus related material) with exactly the same text we use
for the qm474 course - except by the percentages." When asked how literal the copy
should be, he chose verbatim plus the minimum edits needed to keep the text from being
false for HONR, and chose to move the operational machinery out of the syllabus.

**Source of truth.** `predictive_analytics/2026F_predictive_analytics_QM474/syllabus.qmd`,
the `### Final Project (35%)` section and its five numbered items.

**The six permitted deviations — the complete list.** Any other difference is a defect.

| # | QM 47400 | HONR 46400 | Why |
|---|---|---|---|
| 1 | `### Final Project (35%)` | `### Final Project (50%)` | the percentage; HONR's Final Project is 50% under D52 |
| 2 | "In groups, students will complete a practical predictive analytics project" | "Students will complete a practical evidence-driven research project", followed by the individual-default / approved-group sentence | HONR is individual-by-default (D52), and the subject is not predictive analytics |
| 3 | item 2, "productive teamwork" | "productive research work" | "teamwork" is false for a solo researcher |
| 4 | item 3, "Each group will review … other teams' posters" | "Each student will review … the other projects' posters" | no teams by default |
| 5 | item 4, "due date indicated in the syllabus" | "due date indicated in the course schedule" | D13 confines dates to `schedule.qmd` |
| 6 | item 5, "your instructor and the TA will evaluate" | "your instructor will evaluate" | HONR has no TA (D52: "The instructor records the last item if no TA is assigned.") |

The five internal shares — 30 / 20 / 10 / 20 / 20 — are **identical in both courses**, so
despite the instruction's wording there was nothing to change inside the list.

**Sentences adopted from QM474 after verifying they are true for HONR.** Each was checked
against the calendar before being kept, not assumed:

- *"We will not hold our usual class immediately following the Poster Presentation."*
  True. The Expo is Tue 2026-11-17; HONR meets Mon Nov 16 and then **skips Wed Nov 18**,
  resuming Fri Nov 20 asynchronously.
- *"printed and distributed during a dedicated Poster Presentation Preparation class."*
  True. Meeting 34, Fri 2026-11-13 — "the printed poster arrives: rehearse on the real
  thing."
- *"submitted by the due date indicated in the course schedule."* True. The terminal
  poster lock is Sun 2026-11-08, 11:59 PM (M13), a print run shared with QM 47400.
- *"A poster template and assessment rubric will be shared."* The rubric exists. **The
  template does not.** D53 converts a known content gap into a public syllabus promise;
  it is due by M11 on Wed 2026-11-04 and is tracked as workstream L3 on the private
  course tracker.

**Where the removed machinery went.** The syllabus previously carried the component
table with its share-of-course column, the four per-component scoring formulas, the
project-mode rules, and the Peer Evaluation conversion. All of it moves to
`_research_project/2026Fall/final_project_grading_and_project_modes.md` — the "comprehensive
set of project guidelines" the new text promises, published to Brightspace — and to
`brightspace/gradebook_spec.md`. **Nothing is repealed.** The syllabus governs the
weights; the guidelines document governs the operational detail.

**Implication.** `syllabus.qmd`, `planning/ASSESSMENT_ARCHITECTURE.md`,
`_research_project/2026Fall/final_project_grading_and_project_modes.md`,
`scripts/build_brightspace_kit.py`, nb01's grading cell, and the instructor operations
docs must stay synchronized. The standalone conference-URL line that used to follow the
grading scale was deleted as a duplicate — item 4 now carries that URL.

**Supersession boundary.** D53 supersedes only the *syllabus prose* of D52's Final
Project section. D52's weights, component names, scoring formulas, project-mode rules,
and Peer Evaluation mechanics all stand unchanged. D51 remains superseded. D50's
calendar is unchanged.

---

## D54 — M17 is retired: the last Friday is the course reflection session (2026-08-23)

**Decision.** The course runs **M1–M16**. There is no course milestone M17. The last
Friday of the semester is the **course reflection session**, so there is no studio slot
for an M17 submission, and nothing in the course sets M17: not the schedule, not the
gradebook, not the handout PDFs, not the milestone mean. Week 16 is unchanged as
teaching: Monday and Wednesday still teach Studio 12's lessons through nb16.

**Instruction.** Davi, 2026-08-23: "make sure to record that we will not have m17 as we
will use the last friday for reflection, so no need to set it in the course anywhere
even knowing we have the material."

**The material is kept, and simply unassigned.** Retiring a milestone is not deleting
its content. These survive, unassigned:

- `_research_project/2026Fall/_retired_d54/milestone_17_release_and_final_chapter.md`
  (archived under the `_retired_*` convention D50 established)
- `book/studios/milestone12-release-next-cycle.qmd`, the book's own Milestone 12, which
  the book keeps in full: **no course milestone now presents Book Milestone 12**
- `notebooks/student/nb16_release_next_cycle_student.ipynb`, which still teaches
  Week 16 with its milestone framing removed
- `notebooks/student/_retired_d54/ms11_presentation_package_student.ipynb` and
  `notebooks/student/_retired_d54/ms15_final_chapter_portfolio_student.ipynb` — BOTH
  held M17's release-audit / final-chapter / portfolio material. `ms11`'s entry in
  `scripts/notebooks_map.py` claimed it was "M14 studio — the go-public package",
  which was simply wrong: its content is M17's. **M11, M12 and M14 have no studio
  notebook and never did**, which the map's bad label had been hiding.
- the authored course-additions section for M17, parked under `retired:` in
  `_research_project/milestone_course_additions.yml` in case a later edition revives it

**What the reading chain does NOT lose.** The Week-16 row stays in
`planning/COURSE_BOOK_CROSSWALK.yml` with its `assignments:` intact, because Week 16
still teaches `managing-ai-agents`, `conflicting-agents` and `final-portfolio`, and
each is that lesson's **home anchor**. Removing the row would break the home-anchor
partition, drop three chapters out of `planning/READING_FEEDBACK_SCHEDULE.md`, and fail
`validate_book_architecture.py`. The crosswalk answers *what Week 16 teaches*; it does
not answer *what the course collects*.

The row therefore survives but **loses its milestone identity**: it is now
`milestone: null`, so no consumer can print "M17" from it, and it declares
`teaches_station: release-next-cycle` so the session-reading validator can still map
Studio 12 to Week 16 without a graded checkpoint. Four scripts learned to skip
milestone-less rows: `milestone_map.py`, `build_milestone_anchors.py`,
`validate_book_architecture.py` and `validate_session_readings.py`. The row's
`book_milestones:` bridge is now empty and its station event is `introduce`, not
`checkpoint` — `release-audit-v1` is deliberately never reached, which
`validate_book_architecture.py` reports as its standing Phase-4 warning.

**One declaration, every consumer.** The live chain is the `milestones:` table in
`course_config.yaml`. `scripts/milestone_map.py` reads it through `live_milestones()`,
and both course-facing consumers inherit the retirement from that single edit:

| Consumer | Effect |
|---|---|
| `scripts/build_handout_pdfs.py` | 16 milestone PDFs, not 17. No M17 handout is produced. |
| `scripts/update_schedule_badges.py` | the three Week-16 rows print "No milestone" instead of a Book Milestone link. The suppression is no longer hardcoded to the string "M17". |

A milestone dropped from `course_config.yaml` therefore disappears from the PDFs and
from the schedule at the same moment, with no second list to remember.

**Grading.** `milestone_deliverables` becomes the equally weighted mean of the
**M1–M16** scores. No weight anywhere changes: Final Project stays 50%, and its five
QM474 component names and 30/20/10/20/20 shares are untouched, so D52 and D53 stand.

**Grading, resolved.** Davi ruled the three open questions the same day, in session:

1. **Instructor/TA Evaluation is scored from the final poster submission.** Davi's
   words: "the final poster submission." `course_config.yaml` and
   `_research_project/2026Fall/final_project_grading_and_project_modes.md` both now
   read: 100% instructor evaluation of the poster locked at **M13**, judged as
   research communication (traceable argument, reproducible results, uncertainty and
   limitations at the claim, verified sources, honest AI disclosure) — a different
   judgement from the **Poster Presentation** component, which scores poster quality
   against the M13 rubric plus the live Expo delivery.
2. **The final research chapter and the AI-management portfolio are dropped from all
   student-facing material.** Davi chose "Drop both". The Project Mission line in
   `syllabus.qmd` now ends the course at the reproducible package, the bounded
   research note, and the written reflection. Both instruments survive only in
   `_retired_d54/`.
3. **The last Friday's reflection is graded as its own light deliverable**, sitting
   outside the milestone mean. It is collected under **Participation (9%)**, which
   keeps every published weight intact and adds no sixth Final Project component, so
   D52 and D53 are untouched. `syllabus.qmd` §Participation and
   `course_config.yaml assessment:` both say so.

⚠ **Still open — the Evidence Defense.** With Instructor/TA Evaluation moved to the
poster, the individual oral Evidence Defense carries **no grade weight**. It is still
scheduled as in-class practice in the Week 15 and Week 16 Wednesday peer-defence
blocks, and the Project Mission still names "an oral evidence defense" as a course
deliverable. Davi has not been asked whether the defense should stay as ungraded
practice, be folded into a graded component, or be retired outright. Until he rules,
it stays in the schedule as practice.

⚠ **Worth a look — the poster now drives two components.** M13's poster supplies 70%
of Poster Presentation (20% of the project) *and* 100% of Instructor/TA Evaluation
(20%), so a single artifact now determines 34 of the project's 100 points. That is a
direct consequence of ruling 1 and is recorded here so it is a choice on the record
rather than an accident.

**Supersession boundary.** D54 supersedes only D50's milestone *count*: the chain is
M1–M16, not M1–M17. D50's conference block, its renumbering of M1–M10 onto Book
Milestones 1–10, and its Weeks 15–16 post-conference studios all stand. D52's weights
and component names stand. D53's syllabus prose stands.

---

## D55 — every milestone is due the Sunday after its Friday studio (2026-08-23)

**Decision.** A milestone is **worked at its Friday studio and due that Sunday at
11:59 PM**. The Friday studio is unchanged as the working session; what moves is the
deadline, off the studio's own evening and onto the end of the weekend.

**Instruction.** Davi, 2026-08-23: "make sure that all milestones due dates on friday
will be updated to sunday right after it."

**The shift, milestone by milestone.**

| Was | Now |
|---|---|
| M1 Fri Aug 28 | **Sun Aug 30** |
| M2 Fri Sep 4 | **Sun Sep 6** |
| M3 Fri Sep 11 | **Sun Sep 13** |
| M4 Fri Sep 18 | **Sun Sep 20** |
| M5 Fri Sep 25 | **Sun Sep 27** |
| M6 Fri Oct 2 | **Sun Oct 4** (carries the URC draft abstract) |
| M7 Fri Oct 9 | **Sun Oct 11** (carries the URC application + proof) |
| M8 Fri Oct 16 | **Sun Oct 18** |
| M9 Fri Oct 23 | **Sun Oct 25** |
| M10 Fri Oct 30 | **Sun Nov 1** |
| M14 Fri Nov 13, 5:00 PM | **Sun Nov 15, 11:59 PM** |
| M16 Fri Dec 4 | **Sun Dec 6** |

**Three deadlines deliberately do NOT move**, because the conference block depends on
their weekday position and Davi ruled each one:

- **M11** stays **Wed Nov 4, at class**. It was never a Friday deadline.
- **M12** stays **Fri Nov 6, 5:00 PM**. Its Sunday-after is Nov 8, which is the
  terminal poster lock: peer criticism has to reach authors *before* the lock, and
  `validate_milestones.py` hard-fails on two milestones sharing a due date. Davi's
  call: keep Friday.
- **M13** is already **Sun Nov 8, 11:59 PM**, terminal, and shares QM 47400's print
  run. **M15** is already **Sun Nov 29**.

**M14 was a judgement call and Davi took it.** Moving it to Sun Nov 15 leaves the
invitation post about 36 hours of lead time before the Tue Nov 17 Expo. He chose the
Sunday anyway; the tightened lead time is on the record.

**What changed in the tree.** `course_config.yaml milestones:` is the source of truth
and every consumer follows it. Also updated by hand, because they carry the dates in
prose: the chain table and notes in `planning/PROJECT_MILESTONES.md`; the `Due:` line
and the studio-work rubric row of each brief in `_research_project/2026Fall/`; the
fixed anchors and success line in `scripts/validate_milestones.py`; the
`milestone_developed` fields and the Friday closes in `scripts/schedule_data/part1–4.py`;
and nb01's week-architecture cell, which now says a milestone "is due that Sunday at
11:59 PM" without printing a calendar date (D13 still forbids dates in notebooks).

**Stale antecedents this cleared.** Chasing the dates surfaced four D50 leftovers,
all fixed: M15's post-release note pointed at a "release audit at M17, four days
before the Expo" that no milestone created (it now points at the **M13 lock**, nine
days before, which is genuinely the pre-Expo release decision); the Week-13 dress
rehearsal listed "M17 submitted" as student prep (now **M14**); nb01 said the poster
"locks the Friday before" the Expo (it locks on a Sunday, more than a week before);
and nb16 closed with "next comes the public test" although Week 16 is after it.

**Not the deadline, the work.** The studio itself is unchanged: milestones are still
built in the room, not at midnight. Brief prose that said "submitted the same day" or
"submit at studio close" now says "submitted by Sunday", and the Friday close still
says submit — the Sunday is a deadline, not an instruction to wait.

## D56 — One `data.zip`, the Calling Bullshit reference dropped, and the no-class days made visible (2026-08-23)

Three separate rulings, taken together because they touch the same generators.

**1. The student dataset bundle is `notebooks/data/data.zip`.** It supersedes
`honr46400_datasets.zip` (D15, D48) and is the single bundle for BOTH the course and
the book. Membership is unchanged — the five `rdss` CSVs, `README.md`, and the MIT
notice `LICENSE-rdss.txt`, which still ships inside every copy (D48 stands). Two
things did change:

- **The archive stores its members under `notebooks/data/`.** That is the first path
  `load_course_data()` falls back to, so a student who unzips the bundle in the
  directory they run from can execute every notebook offline with no edit. This
  closes `planning/AUDIT_FIXLIST.md` item L7, open since the v2 build.
- **`.gitignore` now negates `docs/notebooks/data/data.zip` as well.** Without that
  second negation the rendered copy was ignored, never committed, and never
  published: the old bundle's Pages URL returned **404 for the whole life of the
  repo**, so every "all datasets (.zip)" link on the Material page was dead. The new
  URL is verified live.

The Schedule page now carries the download link, which it never did despite CLAUDE.md
and the data README both claiming it. The frozen PT/ES editions still name the old
file and are logged in `planning/TRANSLATION_BACKLOG.md` (D36).

**2. Bergstrom & West, *Calling Bullshit*, is dropped from the entire course.** Not
demoted — removed. The `cb_reading` column is gone from the schedule schema, so
`planning/MEETING_SCHEDULE.csv` is now **43 × 34**, and with it went the label, the
`OPTIONAL_EMPTY` exemption, the session-guide emitter, the schedule-row emitter, the
`validate_coverage.py` gate, the `callingbullshit.org` entry in `audit_sources.py`'s
domain allowlist, the `Bergstrom.{0,20}West` entry in its verified-citation registry,
`course_config.yaml sources.secondary_book`, and the reference itself from four
notebook sources, the schedule footer, and seven planning documents. Order matters:
the two `audit_sources.py` entries must be deleted LAST, after the notebooks are
rebuilt, or the citation gate fails on its own material. Historical audit records
(`planning/AUDIT_FIXLIST.md`, `planning/FINAL_REPORT_V2.md`) keep their mentions;
they are point-in-time records, not live references.

**3. The five no-class MWF days are printed, not silently skipped.** `Mon Sep 7`
(Labor Day), `Mon Oct 12` (October Break), `Wed Nov 18` (the day after the Expo),
`Wed Nov 25` and `Fri Nov 27` (Thanksgiving) carry no meeting number, so
`planning/MEETING_SCHEDULE.csv` has no row for them and every printed calendar used
to jump straight past them. They now appear on the Schedule page, in the schedule
`.docx`, in the syllabus `.docx`, and in the Brightspace weekly units — which also
stopped announcing "the three meetings" over as few as one. The wording lives once,
in `scripts/validate_calendar.py PUBLIC_NO_CLASS_LABEL`, next to the `HOLIDAYS` set
it must agree with; every printed surface reads it from there. A break day takes its
Week from a meeting in the **same calendar week**, which is the only rule that files
Fri Nov 27 under the Thanksgiving week rather than the week starting three days later.

Two deadlines were landing ON closed days — SRL slots 03 and 12 had their preparation
scripts due on Labor Day and on October Break. `scripts/assign_srl_slots.py` and
`scripts/build_participation_schedules.py` now step the "two days ahead" deadline back
to the previous day the class actually meets (Fri Sep 4 and Fri Oct 9).

**The Schedule page is held to 65,535 characters** and had grown to 76,654 bytes. It
is now ~62.7 KB, and `scripts/update_schedule_badges.py` FAILS if a render breaches
the ceiling, so it cannot silently regress. What paid for it, all in generators and
none of it costing a student any information: the page turns off the Quarto features
it does not use (`toc`, `anchor-sections`); the Notebook column is a text link rather
than the badge image (the Material page keeps the image); one script sets the
new-tab behaviour instead of 186 inline attributes; the table's CSS moved to
`styles.css`; Week and Studio are bold from CSS; a Studio's full title is spelled out
on its week's first row and shortened on the repeats; and a reading cell that repeats
chapters the same week already linked above NAMES them (`Ch. 40 *(linked above)*`)
instead of relisting the links. That last one is deliberately exact: an earlier draft
said "this week's chapters", which would have told a Week-16 student to submit three
chapters' *It is your turn* sections when only one is due.

`code-copy` and `code-annotations` are off **site-wide** rather than on the schedule
page alone, because a page-level override forked a second 498 KB bootstrap bundle
into `docs/` for one page. No page on this site carries a code block.
