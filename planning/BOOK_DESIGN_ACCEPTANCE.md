# BOOK_DESIGN_ACCEPTANCE — what EDR|AI promises, and how we test it (D35)

**Architecture version:** v1 (FROZEN 2026-08-01 — see D37)
**Status:** chapter review OPEN; the structure is stable
**Governing decision:** `_project_docs/DECISIONS.md` D35
**Evaluation record:** private task #20, Records 1–6

This file is the contract between what the book claims and what we have
verified. A promise may not appear in reader-facing text until its acceptance
test passes. Architecture v0 becomes v1 only when every P1 gate below is green.

---

## 1. The promises

Each promise is stated as the book would state it to a reader, with its current
status. `BOUNDED` means the promise is currently written in weakened form
because its test has not passed.

| # | Promise | Status | Gate |
|---|---|---|---|
| P1 | A reader with no quantitative background can go from curiosity to a defensible, written empirical claim using this book alone. | **BOUNDED — A1 RUN 2026-08-01, RESULT NO** (see below); the preface says "a guided path", names what the reader needs, and states plainly where other people are required | A1 |
| P2 | The book works with no course, no institution, no calendar, no peers, and no conference attached. | **PASSES A2** — de-coursing sweep 2026-08-01 cleared all 41 hits; A2 is now a HARD GATE (planted-leakage probe fails the build). ch33 derives the note from the dossier, ch37 opens on a release audit, SRL is out. Part VI retitle remains | A2, A3 |
| P3 | Every practice unit contains real work: a worked example, faded practice, an executable or structured task, and a verification test. | **PARTIAL** — the practice grain now exists (12 station pages + workbooks, generated from the manifest, each with its checkpoint and authored rubric). The cold pilot confirms workbooks still lack worked examples, starter data, and faded scaffolds | A4 |
| P4 | Every methods claim the book teaches is correct at the level it is taught. | **PASSES A5** — Phase 1 closed 2026-07-31 after six adversarial rounds; 12 misconceptions carry executable positive/boundary/converse cases, and the gate runs on every scan | A5 |
| P5 | Assessment criteria represent what is actually being learned, across all five pathway forms and all communication genres. | **PARTIAL** — 60 authored criteria across the 12 checkpoints, with criterion-specific 0/1/2 descriptors and blocking permission gates, replace the truncated auto-derived rubrics. Route/genre addenda and exemplar pairs remain unauthored | A6 |
| P6 | A reader never undertakes data work they are not authorized to do, and never exposes restricted data to an AI service. | **PASSES A7** — the ethics and data-governance lesson ships: four permission states, a three-question determination, six misconception cases, a seeded re-identification demonstration, AI-exposure rules with incident response, and a no-permission route for unaffiliated readers | A7 |
| P7 | No claim is published before its computation has been regenerated from its own files in a clean environment. | **MISSING** — the lifecycle publishes at Station 10 and reproduces at Station 11 only if the gate is added | A8 |
| P8 | The three editions say the same thing, and every factual claim is retrievable. | **BOUNDED BY D36** — EN carries a verified `references.bib` (every entry read, none asserted from an AI summary) and the F9 errors are fixed; PT/ES are deliberately frozen behind per-page notices, with all deferred work ledgered in TRANSLATION_BACKLOG.md | A9 |
| P9 | Chapter identity, URLs, and citations survive the insertion of new lessons. | **PASSES A10** — proven twice in the live repo: inserting two lessons preserved every id, url_path, and companion path while the projections regenerated themselves. identity_epoch enforced; a rename or URL move fails the build | A10 |
| P10 | The book is usable solo, on a modest device, without paid AI. | **PARTIAL, now specified** — the preface states what the reader needs, gives a no-AI path, and names where other people are genuinely required; the cold pilot found and fixed the peer-check and AI-access stalls. Remaining solo gaps are listed under A1 | A11 |

---

## 2. The acceptance tests

Priority marks what must pass before the **v1 freeze** (P1) versus before
**general release / announcement** (P2).

### A1 — Cold end-to-end pilots · P1

Run complete projects using only the public book — no instructor, no course
materials, no private help. Minimum set, one project each:

1. observational descriptive
2. prediction
3. experimental descriptive
4. observational causal, **currently unidentified** (must stay causal, never be
   relabeled descriptive)
5. note-only communication, solo, no peers and no conference

**Pass:** each pilot reaches a written research note containing methods,
results with stated uncertainty, discussion, claim boundary, references, and a
reproducibility package — without the reader having to invent apparatus the
book failed to supply. Every point where the reader stalls is logged as a
defect against the station that should have carried them.

**Until it passes:** the preface, `index.qmd` ×3, and For Instructors state the
bounded form of P1.

### A2 — Course-leakage scan · P1 · machine

An allowlist-based scanner rejects, anywhere outside `for-instructors.qmd` and
the crosswalk data: `notebooks/student`, `nbNN`, Expo, SRL, Student Research
Lead, milestone, M0–M15, weekly quiz, conference week, Purdue (except as an
explicit parenthetical), Brightspace, studio, semester week numbers.

**Pass:** zero hits in all three editions' chapter bodies, appendices (except
For Instructors), and station workbooks. Runs in `validate_book_sync.py`.

### A3 — Independence walkthrough · P1

A reader profile with **no** conference, **no** peers, **no** course, and **no**
graded portfolio can name, for every station, what they produce and why. Poster,
pitch, brief, and oral defense appear as genre branches of one core artifact,
never as the required sequence.

**Pass:** Part VI carries a medium-neutral title; ch33 derives the note from the
dossier, not from a poster; ch37 is a medium-neutral release audit; `srl.qmd` is
no longer a general appendix; no chapter body links a course lab.

### A4 — Station-kit completeness · P1 · machine + human

Every station workbook contains, and a semantic validator verifies the presence
of: one fully worked example with expected output · starter data or a seeded
generator · one faded-scaffold completion task · route variants where the
station branches · one explicit verification test · the dossier checkpoint ·
the authored rubric.

**Pass:** the validator fails on a workbook whose only code cell is generated
scaffolding. Fresh-Colab smoke test executes every computational workbook end to
end from a clean runtime.

### A5 — Methods-correctness counterexamples · P1 · executable

Each confirmed F2/F3 defect gets an executable counterexample plus a concept
check the reader must pass:

| Defect | Counterexample must show |
|---|---|
| Compass relabeling | A causal question with confounded observational data classifies as "causal target; currently unidentified" — never descriptive |
| ch10 bias | Signed mean error, not average distance; power undefined without a test and alpha |
| ch14 leakage | Nested selection versus reused-holdout selection produce different, and differently honest, performance estimates; time-ordered splits for temporal data |
| ch15 attrition | Complete-case contrast under treatment-affected retention is not an effect "among stayers" |
| ch18 reliability | Splitting respondents measures sampling variation; split-half reliability splits ITEMS |
| ch21 robustness | Same-sign specification curves can share one bias; a specification spread is not an uncertainty interval; every version must test the same substantive claim, dots in one panel must be commensurable, and no version may condition on a post-treatment outcome |
| ch22 negative tests | Repeated samples under a valid null produce nonzero estimates; "exact zero" is the wrong criterion; a pass reduces concern only as far as the check was sensitive, and no simulated band is a decision rule |
| ch32 LOCF | Death is post-treatment; the estimand and its assumptions must be declared, and the spread is not an honest range |

**Pass (strengthened 2026-07-30, per the Batch-A review):** for each defect, the
counterexample set must contain, seeded (SEED = 464):

1. a **positive case** demonstrating the defect;
2. a **boundary case** where the superficial warning sign is present but the
   defect is absent (e.g., differential retention unrelated to outcomes → little
   bias);
3. a **converse case** where the warning sign is absent but the defect is present
   (e.g., equal retention rates with opposite outcome selection → large bias);
4. **numerical assertions** tied to the declared estimand (the plotted "truth"
   must equal the quantity computed from the generated potential outcomes, never
   a hard-coded number the DGP only approximates);
5. a **concept check with an expected answer**, so a wrong learner reading is
   detectable;
6. **propagation searches**: the rejected phrases greped across book chapters,
   canonical notebook sources (`_production_kit/nb_sources/`), configuration
   (`course_config.yaml`, generators), and both translations.

One vivid counterexample demonstrates that a failure can happen; only the
boundary and converse cases establish WHICH feature causes it, and only the
propagation search makes the correction durable.

**Amendment (2026-07-30, from the B/C review).** The earlier "all specifications
must share an estimand" wording was itself too strict and helped produce a ch21
overshoot: legitimate multiverse analysis does vary operationalizations. The rule
is now four-part — (1) a common substantive claim; (2) commensurable quantities
within a plotted panel; (3) explicit stratification into labeled panels when
population, outcome definition, or scale changes; (4) exclusion or separate
treatment of groups defined by a post-treatment outcome. Stricter where causal
meaning is at stake, less falsely rigid where it is not.

**Implemented (2026-07-30).** `planning/MISCONCEPTION_MANIFEST.yml` +
`scripts/validate_misconceptions.py`, running in CI. Eleven misconceptions, 28
literal rejected phrases, and **regex claim-families** so a paraphrase cannot
drift through: literal matching only catches the wording already fixed, which is
not how a misconception returns. `--self-test` asserts both directions — every
drift sentence is caught, every legitimate phrasing is permitted — because a
validator that cannot fail is not a gate, and one that fails wrongly is worse.

**Hardened (2026-07-31, from the round-4 audit).** Twelve misconceptions now
carry the A5 schema fields (estimand · counterexample · concept_check),
enforced by the manifest schema check. The self-test runs against an ISOLATED
SNAPSHOT (a round-4 interruption had leaked fixture text into published ch22
— the test now cannot touch a real file), asserts each mutation is caught by
its OWN id at the probe path, and runs 11 adversarial **allow-reversals**
(every `allow:` span must carry its refutation; a bare quotation span had
been shown to launder an endorsement). Public CI states honestly that it
certifies tracked public surfaces only; `--local` scans the gitignored
canonical sources and instructor notebooks plus generation freshness, and is
wired into `scripts/nbbuild.py` (every build) and
`scripts/sync_instructor_repo.sh` (every private sync) — the two points where
canonical content moves. The numbers evaluator enumerates every numeric
component of ch14/ch15/ch22 including alt text and both endpoints of every
range, with numpy/matplotlib pinned in CI. On its first hardened run the
gate found a stale nb12-era instructor notebook still carrying "the only
honest test" and 20 orphaned v1 sources, one already damaged by a
wrong-target sweep — all removed against a verified archive.

Evidence it works: on first run it caught 7 live remnants that manual greps had
missed (including `nb06` and `nb12`, which no review had flagged); a line-wrap
bug in the matcher then hid 2 more, one of them a regression introduced minutes
earlier when a ch21 rewrite deleted the very term it was teaching; and adding the
regex families caught 3 further genuine instances that had survived two full
review rounds, including ch15's failure case still asserting the contrast
"describes only the healthier patients who remained."

**Executable manifest (required before Phase 1 is declared complete).** A5 is not
met by prose. Each defect needs one row in an executable manifest carrying: the
declared estimand, the positive case, the boundary case, the converse case, the
expected numbers with tolerances, the concept-check answer key, and the propagation
allowlist. The check must FAIL when a rejected phrase is deliberately reinserted
into a canonical source — that test is the point, since the B/C round passed prose
review while the same misconceptions survived in `nb08`, `nb10`, `ch20`, `ch23`,
`ms09`, `ms13`, `nb14`, and the generated rubrics. Propagation searches run across
chapter bodies AND prompts, canonical notebook sources, generated notebooks,
rubrics, configuration, and both translations.

**Known Phase-1 → Phase-3 dependency (recorded 2026-07-30).** Correcting ch10's
power definition required naming a **statistical test** and its **threshold**, and
correcting its diagnosand list required naming **coverage**. Verified by search:
ch10 is now the FIRST place in the book where testing vocabulary appears, and
nothing before it teaches tests, thresholds, or intervals. Phase 1 bridges this
inline with bold-term definitions plus a forward pointer, which is the minimum
honest fix. The real repair is the **uncertainty-foundations lesson placed before
ch10** (D35 §2) — exactly the prerequisite inversion the round-2 review identified.
When that lesson lands, revisit ch10's inline glosses and delete what it now
supplies. Until then, ch10 carries a load its predecessors have not prepared, and
the A1 cold pilots should watch specifically for readers stalling there.

### A6 — Assessment calibration · P2

Common core criteria plus route- and genre-specific addenda, each with a stable
ID and anchored performance levels. One longitudinal example family with route
contrasts, not unrelated one-offs.

**Pass:** two qualified readers score a small response sample; criterion-level
disagreements are recorded by route and genre and the descriptors revised. A
learner can measurably improve a response using only the rubric and exemplars.

### A7 — Ethics stop-case tests · P1

Scenarios: a survey of identifiable people · uploading a proprietary dataset to
an AI service · scraping a site whose terms forbid it · linking two datasets
that re-identify individuals · a biological experiment · a public, already
de-identified dataset.

**Pass:** each scenario resolves to the correct state (`cleared` · `formal
determination required` · `pending` · `not authorized/stop`), identifies **who**
can decide, and distinguishes ethical reflection from formal authorization. The
book never implies the reader self-authorizes by passing a rubric. Safe public
or synthetic feasibility work remains permitted while a determination is pending.

### A8 — Release gate · P1 · machine where possible

**Pass:** the Station 11 release checklist fails unless every quantitative claim
in the artifact resolves to an output regenerated in a clean environment from
the packaged files. A preliminary presentation is permitted only when labeled
preliminary.

### A9 — Sources and locale freshness · P2 · machine

**Pass:** `book/references.bib` exists and Quarto renders the bibliography;
every citation is retrievable (the F9 corrections applied: PNAS author list,
the bounded-surprise claim, the Zahavy claim); each translated file records its
EN source hash and a state of machine / post-edited / human-reviewed; a stale
translation fails the build; `lang:` is set per edition.

### A10 — Identity stability · P1 · machine

**Pass:** inserting a test lesson changes no existing lesson ID and no existing
HTML URL. Identity comes from `BOOK_ARCHITECTURE.yml` semantic IDs, never from a
filename's numeric prefix. Orphan detection catches generated files whose source
was removed. Regeneration is deterministic. *(Legacy Colab shim notebooks are
explicitly out of scope per D35(6).)*

### A11 — Solo / low-resource path · P2

Every check is labeled **solo-capable**, **AI-assisted**, or
**human/expert-required**, and every human-required check has a valid solo
substitute. A downloadable static workbook form exists. Basic accessibility —
text alternatives, keyboard operation, zoom and reflow, color independence,
visible focus — is built into the workbook generator from the start; full
WCAG 2.2 AA assistive-technology QA across the three languages is deferred until
after the v1 freeze (D35(8)), so it does not test throwaway artifacts.

---

## 3. Freeze criteria — v0 → v1

Architecture v1 is declared only when **all** of the following hold:

1. Every **P1** acceptance test above passes.
2. EN prototypes exist and are cold-tested for Stations **4, 5, 7, and 10/11** —
   the four riskiest units (the provisional Contract gate, the route hub, the
   reproducible first analysis, and the genre-adaptation/reproduction boundary).
3. The two new lessons (uncertainty foundations, ethics and governance) are
   written and placed, **after** the identity layer exists.
4. The prerequisite graph is complete: for every Research Contract field —
   definition → worked example → faded practice → checkpoint — with no field
   assessed before it is taught. Machine-checked.
5. The 16-row course crosswalk is machine-verified against
   `planning/MEETING_SCHEDULE.csv` and the milestone briefs
   (`_research_project/2026Fall/`). The validator is the arbiter, not any
   reviewer's reading.
6. A written workload estimate covers canonical authoring, route variants,
   exemplar production, localization, code execution, and review labor — not
   generated-file counts.

On freeze: amend D24–D26 and CLAUDE.md, replace `BOOK_REVIEW_STATUS.yml`'s
boolean flags with content-addressed states (source hash, commit, reviewer,
date, per-stage status), and **resume chapter review**.

---

## 4. Open questions this document does not settle

Recorded so they are not mistaken for settled:

- Whether 10, 11, or 12 stations produces better learner outcomes. Twelve is an
  artifact-and-prerequisite design judgment, not an experimental result.
- Whether route- and genre-specific workbooks should be separate physical
  notebooks. Stations 5 and 10 need prototypes before the physical file count is
  fixed.
- Whether any external reader depends on the 111 legacy notebook URLs. Assumed
  no (D35(6)); revisit if the book circulates before v1.
- Actual authoring, translation, calibration, and maintenance hours for either
  architecture.
- The RDSS positioning statement: EDR|AI's scope is quantitative empirical
  research while RDSS spans quantitative, qualitative, and mixed methods, so
  "translates RDSS" overclaims. A coverage matrix (adopted · adapted · omitted ·
  EDR|AI-original) is owed before the preface language is finalized.


---

## A1 — the cold pilot was RUN (2026-08-01). Result: **No.**

A novice-reader pilot walked the book-only path from the home page through
Station 5 and into Station 6, producing real artifacts at each checkpoint.
Full record: `_adm/codex_reviews/2026-08-01_cold-pilot-A1/verdict.md`.

**The verdict, quoted:** *"The book carried me from curiosity to a thoughtful,
bounded plan. It did not carry me, on its own, to an empirical result or
defensible research claim."*

**The three findings that produced that answer, and what was done:**

1. **The first blocking stall was Chapter 1** — the book required an AI tool
   it never named, priced, or offered an alternative to. FIXED: the preface
   now has a "What you need before you start" section giving the Colab route,
   the AI-assistant options, and an explicit no-AI path that keeps the method
   and loses only the tool practice.
2. **The ethics requirement is correct and is genuinely blocking for an
   unaffiliated reader.** A book cannot substitute for a competent authority.
   FIXED, without weakening the rule: the ethics lesson now carries an
   explicit no-permission route — published aggregates, openly licensed
   record-free data, or simulation — which reaches every method the book
   teaches, and says plainly that a simulated dataset demonstrates a method
   but cannot support a claim about the world.
3. **Nothing in the architecture acquired data.** Station 6 assumed data had
   arrived; for a course student the course supplies them, for a solo reader
   nothing did. FIXED: Station 6 now opens with an acquisition route keyed to
   the reader's permission status, and its first practice step is settling
   and recording that route.

**Also fixed from the same pilot:** a generator bug rendering station steps as
raw Python dicts; "walk it past a colleague" with no solo substitute (now: put
it away, re-sort cold, compare — and an AI cannot be the peer, because your own
consistency is what is being tested); and ch12 naming
difference-in-differences, regression discontinuity, and instrumental variables
as if the book had taught them (now bounded to naming and defending what you
would have to learn).

**The honest standing position.** With these fixes a solo reader can reach a
defensible *plan*, a declared design, a permission determination, and — on the
no-permission route — an executed analysis with stated uncertainty. What has
not been demonstrated end to end is an unaffiliated reader reaching an original
empirical claim about the world. P1 therefore stays BOUNDED, and the preface
says what the book actually delivers. A second pilot on the no-permission route
is the test that could lift it.
