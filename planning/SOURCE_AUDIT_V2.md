# SOURCE AUDIT V2 — Repository Audit for the Fall 2026 Rebuild

**Date:** 2026-07-22/23 · **Trigger:** instructor's master prompt ("complete
course ecosystem": Week 1–16 architecture, milestones M0–M15, flipped classroom
with Student Research Leads, high-intensity controlled AI use, AI Research
Ledger, Purdue GenAI Studio roles, 37-chapter open book, replication +
multi-agent modules). · **Method:** three parallel repository audits (planning/
milestones; notebooks/template/guides; governance/site/scripts/history) +
verified external research. Supersedes nothing; complements
`planning/SOURCE_AUDIT.md` (the v1 seed audit). The v1 build is preserved at
git tag **`v1-compass-build`**.

---

## 1. What existed at audit time (the v1 build)

A complete, validated course (BUILD_STATUS: Phases A–F + revision pass,
2026-07-18; taxonomy adoption 2026-07-19; course redesign D13–D16 2026-07-20):

- **44-meeting MWF calendar** (42 in-person + 2 async), 8 phases, generated
  from `scripts/schedule_data/part1–4.py` → `planning/MEETING_SCHEDULE.{csv,md}`.
- **20 topic notebooks** nb00–nb19 (student committed; instructor gitignored,
  synced to the private `…_instructor` repo), built instructor-first from
  gitignored cell sources via `scripts/nbbuild.py`, all validator-green.
  84 Gemini prompt blocks + "After running, verify (the responsible-AI habit)"
  checklists; 69 Q&A blocks; 7 required active-learning moves per notebook;
  35-figure library.
- **24 milestone briefs** M00–M23 (`_research_project/2026Fall/`), each with a
  100-pt 4-band inline rubric on a fixed 5-virtue menu (compass alignment,
  evidence integrity, verification, uncertainty & limitations, craft) and
  hard-cap penalties; 13 `project/` protocol docs (poster storyboard/red-team/
  production, pitch/ULN/hard-questions/dress-rehearsal, reproducibility audit
  with partner cold-reproduction + signed attestation, post-conference
  redesign, evidence defense); cumulative final dossier + claim ledger.
- **Site**: Quarto → `docs/` → GitHub Pages; Home/Syllabus/Material/Schedule/
  Instructor; material/schedule/instructor pages generated; instructor page
  client-side encrypted post-render; dataset zip.
- **QA battery** (no unit tests; all local/hook-driven): validate_calendar /
  validate_coverage / validate_milestones / validate_notebooks /
  voice_lint_notebooks / voice_check_guides / audit_sources /
  update_schedule_badges --check.
- **Policies**: Ask → Verify → Document AI policy with a required per-deliverable
  disclosure block (`course_config.yaml ai_policy.ledger_required: true`);
  grading 15/30/20/20/5/10; revision policy; RDSS (free online) as primary
  text; `enrollment: 5`, `project_mode: individual`.

## 2. Decision registry status

D1–D11 are MGMT474-era seeds (D2/D3/D9 dropped, D10 superseded); the live
rulings at audit time were **D12** (inquiry compass, 2026-07-19), **D13**
(Friday studios + compression), **D14** (undergraduate voice), **D15**
(site split / dataset zip / instructor tab), **D16** (no fabricated citations)
— all 2026-07-20. New rulings D17–D21 (this rebuild) are recorded in
`_project_docs/DECISIONS.md`.

## 3. Conflicts between the master prompt and the v1 build — and the rulings

| # | Conflict | Ruling (Davi, 2026-07-22) |
|---|---|---|
| 1 | Week 5–9 topics: one week per DeclareDesign-library pathway vs compass-sequenced nb06–nb13 | **New prompt governs**: pathway weeks (obs-descriptive, obs-causal, exp-descriptive, prediction, exp-causal). Compass retained as the question-classification layer (see §5). |
| 2 | Milestones M0–M15 vs M00–M23 | **New prompt governs**: 16 packages M0–M15, new briefs + studio notebooks. |
| 3 | Mon/Wed pedagogy: flipped + Student Research Lead vs instructor-led | **Full SRL, every lecture** (launch week instructor-led; 25 lead slots = 5 per student at n=5). |
| 4 | Friday format: stand-up/sprint/red-team/submit vs recap/brief/work | New prompt's 4-section studio governs (milestone kickoff folded into the sprint opening). |
| 5 | AI-intensity components (prompt iteration, interrogation, competing roles, human-only checkpoint, exit defense, structured ledger) absent | Build all of them into template v2; **rewrite the Gemini prompts for the new material**. |
| 6 | Book: none vs 37 chapters | **Full 37-chapter book**, synchronized with the NEW notebooks + site; RDSS remains the theory text. |
| 7 | GenAI Studio absent | **Develop what is necessary** (roles, KB, Colab API PoC); Gemini stays primary in-notebook. |
| 8 | Thanksgiving async: peer replication/red-team vs self-robustness | New prompt governs: M13 = replication + red-team of a peer's anonymized package (due Sun Nov 29). |
| 9 | Wed Nov 18: class vs no class | New prompt governs: **no class Wed Nov 18** (calendar becomes 43 meetings). Flagged for final syllabus confirmation. |
| 10 | Robustness timing: before poster vs post-conference | New prompt governs: Week 10 = robustness/attack-the-analysis before the poster. |

## 4. What is preserved (infrastructure, policy, conventions)

- Instructor-first build pipeline, `INSTRUCTOR SOLUTION` markers, student
  placeholders, private-instructor-repo sync, Colab badges, `load_course_data()`.
- All six CLAUDE.md critical rules (voice/audience, undergraduate voice,
  evidence-integrity, responsible-AI documentation, uncertainty & limitations,
  lecture-labels-never-dates) and the voice/citation lint gates.
- Site machinery, generated-page discipline, instructor-page encryption,
  dataset-zip distribution (D15), SEED=464, no seaborn, escaping rules,
  emoji vocabulary, commit conventions, Commit-AND-Render rule.
- Rubric DNA (100-pt 4-band, 5-virtue menu, hard-cap penalties incl.
  missing-AI-disclosure → Craft 0).
- Generated session-guide mechanism (schedule data → builder scripts).

## 5. Conceptual reconciliation (why no taxonomy contradiction)

RDSS itself carries both layers. **Ch. 7** classifies *questions* (kind:
descriptive/causal × reach: data-at-hand/population/unseen) — the course's
inquiry compass, kept as the question-classification tool taught in Week 2 and
used in every declaration. **Ch. 14–19 (the design library)** organizes
*designs* by inquiry-kind × data-strategy: observational descriptive,
observational causal, experimental descriptive, experimental causal (+
complex), which is exactly the master prompt's Week 5–9 sequence, with
**prediction treated as its own answer objective** (generalization to unseen
observations — not forced into either grid), per both the prompt and the v1
nb12 design. The four-approach grid retired by D12 (description / statistical
inference / predictive modeling / causal reasoning) does **not** return.

## 6. Missing components the rebuild adds (gap list)

Student Research Lead system (0 prior references) · per-notebook AI Research
Partner briefing, prompt-modification requirement, AI-output interrogation,
competing AI roles, human-only checkpoints, exit defense · structured **AI
Research Ledger** artifact (v1 had the habit + disclosure block, no template)
· Purdue GenAI Studio anything (0 references) · multi-agent management module
(0 student-facing references) · peer anonymized replication/red-team activity
· research-note genre (v1 had 1-page brief + dossier) · course-authored book ·
CI (no `.github/`; every gate local).

## 7. Reuse map (v1 → v2)

| v1 asset | v2 destination |
|---|---|
| nb00 launchpad (AI hallucination demo, Meet Your Professor, Ask→Verify→Document) | nb00 Week 1 |
| nb01 curiosity→question; nb02 compass | nb01 Week 2 |
| nb03 sources/citation integrity/claim map | nb02 Week 3 |
| nb04 model&inquiry(DAG) + nb05 measurement + nb11 declare→diagnose→redesign | nb03 Week 4 (+ pathway weeks) |
| nb06 description + nb07 sampling + nb10 generalization/uncertainty/power | nb04 Week 5 |
| nb13 causal reasoning (identification, natural experiments) | nb05 Week 6 |
| nb07 assignment/ethics + bonilla_tillery survey experiment | nb06 Week 7 |
| nb12 prediction (leakage, baseline, split, metric) | nb07 Week 8 |
| nb13 experiments + foos_etal field experiment + nb09 estimators | nb08 Week 9 |
| nb17 robustness/sensitivity/claim ledger (async) | nb09 Week 10 + M13 |
| nb14 poster (storyboard/red-team/production; data-ink lecture) + poster protocols | nb10 Week 11 |
| nb15 communicating evidence (pitches, ULN, hot seat) + conference protocols | nb11 Week 12 |
| nb16 conference debrief + reflection protocols | nb12 Week 13 |
| reproducibility audit protocol + attestation (M20) | nb13 Week 14 + M13 |
| nb18 reproducibility/brief | nb14 Week 15 |
| nb19 evidence defense | nb15 Week 16 (defense strand) |
| 5 rdss datasets | pathway weeks (lapop+la_voter→nb04; cliningsmith→nb05; bonilla_tillery→nb06; foos_etal→nb08) |
| figure library, INQUIRY_DECLARATION, claim-ledger instrument, syllabus policies | carried forward |

## 8. External research (verified 2026-07-22)

**Purdue GenAI Studio** (official RCAC knowledge base, rcac.purdue.edu/knowledge/genaistudio):
custom models (base model + system prompt + attached Knowledge); RAG knowledge
bases (document upload, PostgreSQL vector backend) shareable via **groups**;
**multi-model comparison** in one chat; **OpenAI-compatible API** at
`https://genai.rcac.purdue.edu/api/chat/completions` (keys via Settings →
Account; Purdue SSO/CILogon). Open-source models only (LLaMA family; more by
ticket). **Not documented:** native agents, tools/pipelines, rate limits,
explicit student-eligibility terms. Course materials therefore use a six-level
taxonomy (prompted role → custom model → RAG assistant → sequential multi-role
workflow → autonomous agent → multi-agent orchestration) and implement GenAI
Studio only at levels 1–4. **Open item:** instructor verifies student access +
API-key availability before the semester.

**Sant'Anna** (`github.com/pedrohcgs/claude-code-my-workflow`, accessible):
adopted — plan-first specs, project memory, single-dimension specialist
reviewers, critic–fixer loops until dry, numeric quality gates, claim-provenance
cross-checks (≈ our claim ledger + traceability rule), AI-voice auditing
(≈ voice_lint), replication-package discipline, git safety. Modified — his
LaTeX/R/Stata toolchain is replaced by this repo's Python/Quarto/nbbuild gates.
Rejected — nothing of substance; the repo had convergently implemented most of it.

**Cunningham** (causalinf.substack.com posts 12, 24, 44, 51): **all four
paywalled** — per the evidence rule, no principles were invented from them. The
only public, verifiable fragments used: part 24's premise (validate analytical
code by comparing independent implementations, mindful that errors may be
correlated) informs the Week 16 correlated-errors lesson; MixtapeTools is a
fork of Sant'Anna's template.

**Calendar anchors** (purdue.edu/undergrad-research): Fall Expo 2026 = Nov
16–20, **posters Tue Nov 17** — matches the course's M-anchors (poster lock Fri
Nov 6; Expo Tue Nov 17). **DeclareDesign library** (book.declaredesign.org,
ch. 14–19): confirmed organized as observational/experimental ×
descriptive/causal + complex — the Week 5–9 backbone.

## 9. Risks carried into the rebuild

1. Book (37 chapters) is the largest scope item → sequenced last, with a
   book↔notebook sync validator.
2. GenAI Studio student access unverified → manual-UI fallback is a first-class
   path, not an afterthought.
3. Enrollment assumed ~5 → only schedule-data SRL slots change if it moves.
4. Autocommit Stop hook pushes tracked changes at turn end → keep the tree
   coherent; commit deliberately.
5. No CI → validators remain local; a lightweight Actions workflow is a
   recommended follow-up, not a course blocker.
6. Brightspace replication stays manual; URC abstract deadline still TBD
   (internal gate Fri Oct 9).
