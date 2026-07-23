# FINAL REPORT — HONR 46400 v2 Course Rebuild

**Course:** HONR 46400 — SP: Evidence-Driven Research (Fall 2026, Honors College, MWF in person)
**Instructor:** Professor Davi Moreira
**Report date:** 2026-07-23
**Status:** Build complete; Phase-7 audit complete; **Stage-8 revision pending** (see `planning/AUDIT_FIXLIST.md`)
**Governing decisions:** `_project_docs/DECISIONS.md` D17–D21 · **CLAUDE.md v5.0**
**v1 preserved at:** git tag `v1-compass-build`

---

## 1. Executive summary

The course was rebuilt from the ground up to the instructor's Fall 2026
master-prompt architecture: **16 weekly topic notebooks (nb00–nb15)**, **16
milestone packages (M0–M15)**, a **Student Research Lead flipped-classroom
system**, the **AI Research Ledger + SDIIVDD** responsible-AI spine, the **Purdue
GenAI Studio reviewer bench (13 roles)**, a **37-chapter open-access course
book**, the full Quarto site with a Book tab, and GitHub Actions CI. Every
machine gate is green and the build is committed, rendered, and synced to the
private instructor repo.

An 11-auditor Phase-7 review then stress-tested the corpus across consistency,
feasibility, book↔notebook alignment, link integrity, accessibility,
reproducibility, STEM breadth, poster/evidence chain, adversarial AI use,
adversarial design, and GenAI over-selling. **No CRITICAL defects were found.**
The audit surfaced **41 findings total: 0 critical, 11 high, 12 medium, 18 low.**
The course is fundamentally sound and close to ship-ready; the high-severity
findings are concentrated and fixable in one focused revision pass, with the
single largest work item being a **v1→v2 reconciliation of the poster/conference
protocol layer**, which was never migrated off the retired M00–M23 numbering.

---

## 2. What the v2 rebuild created

### 2.1 Weekly topic notebooks — nb00–nb15 (16)
One notebook per week, Colab-first, no code-writing required of students, SEED=464
throughout, GitHub-raw-first data loading with local fallback. Built via the
instructor-first pipeline (`_production_kit/nb_sources/nbNN_*.py` → `scripts/nbbuild.py`),
committed as answer-stripped student files with instructor mirrors synced to the
private repo. Coverage: AI-as-arm-not-brain (nb00), curiosity→problem (nb01),
research-builds-on-research (nb02), anatomy of design (nb03), the five design
pathways nb04–nb08 (observational descriptive / observational causal /
experimental descriptive / prediction / experimental causal), attack-the-analysis
(nb09), poster criticism + lock (nb10), poster delivery (nb11), conference (nb12),
replication + red-team (nb13), poster-to-research-note (nb14), managing multiple
AI agents (nb15).

### 2.2 Milestone packages — M0–M15 (16)
Each milestone ships a brief in `_research_project/2026Fall/milestone_NN_*.md`, a
matching studio notebook `ms00–ms15`, and a band rubric. The chain is a cumulative
Research Project Dossier where each milestone feeds the next: baseline → opportunity
landscape → verified evidence map → charter/MIDA → pathway audits → first minimum
viable analysis (M8, first reproducing estimate) → research audit → terminal poster
lock (M10) → presentation package → URC Expo/conference reflection (M12) → peer
replication red-team (M13) → research note + reproducibility capsule (M14) → final
chapter + AI-management portfolio + defense (M15).

### 2.3 SRL flipped-classroom system (D18)
Every Mon/Wed lecture from Week 2 is led by a **Student Research Lead** running a
Socratic investigation (25 lead slots ÷ 5 students = 5 leads each, rotation seats
A–E). Fixed 50-minute four-section architectures enforced by the session-guide
generator; SRL handbook, templates, and a 9-dimension rubric in `project/srl/`.

### 2.4 AI Research Ledger + SDIIVDD (D21)
One structured artifact (eight fields: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · **responsible
researcher**) carried in every notebook and appended at every milestone. The
everyday shorthand is **Ask → Verify → Document**; the full loop is **SDIIVDD**
(Specify → Delegate → Interrogate → Inspect → Verify → Document → Defend). Missing
ledger entries hard-cap the rubric's Craft criterion to 0 and the submission is
returned unread.

### 2.5 GenAI Studio reviewer bench — 13 roles (D19)
Thirteen custom reviewer-role models in `genai_studio/roles/` (Socratic Research
Tutor, Evidence & Citation Verifier, Research-Question Diagnostician, MIDA Design
Reviewer, Observational Descriptive Auditor, Causal Identification Skeptic,
Experimental Design Reviewer, Prediction & Leakage Auditor, Poster Critic,
Robustness & Sensitivity Reviewer, Reproducibility Auditor, Research-Note Reviewer,
AI Research Team Orchestrator), shared via a course group with an
OpenAI-compatible-API Colab proof-of-concept and a first-class manual-UI fallback.
Implemented strictly at levels 1–4 of the six-level taxonomy; no autonomy claimed.

### 2.6 The course book — 37 chapters, six parts (D20)
"Evidence-Driven Research" in `book/`, rendered to `docs/book/` with a site Book
tab. Each chapter carries the research decision, a plain-language explanation, a
STEM worked example, a Colab lab link, AI prompts, a "Do not delegate" box, an AI
failure case, a verification lab, project transfer, and a defend-your-decision
activity. Parts I–VI map onto the notebook spine; RDSS remains the assigned theory
text.

### 2.7 Site + infrastructure
Full Quarto site (index / syllabus hand-edited; material, schedule, instructor
pages generated), the password-gated Instructor tab backed by the private
`_instructor` repo, a single canonical dataset zip
(`notebooks/data/honr46400_datasets.zip`), GitHub Actions CI, and the full
validator/generator battery.

---

## 3. What was preserved from v1

- **Infrastructure & pipeline:** the instructor-first notebook build (`nbbuild.py`),
  voice linter, source auditor, schedule-data generators, milestone/coverage
  validators, dataset-zip builder, instructor-repo sync, and the Quarto→`docs/`→Pages
  deployment all carried forward and were extended, not rewritten.
- **Policy spine:** the compass question-classification layer (RDSS ch. 7), the
  evidence-integrity / results-verification rule, lecture-labels-never-dates,
  undergraduate-friendly voice with the em-dash budget, no-fabricated-citations, and
  the studio-Friday principle (no new topic content on Fridays) all survive from
  D12–D16 into the v2 build.
- **Full v1 build tagged and mined:** all 20 v1 notebooks, 24 v1 milestone briefs,
  and the 44-meeting schedule are preserved at git tag `v1-compass-build`; v1
  notebook sources archived in `_production_kit/nb_sources_v1/` and mined per
  `planning/SOURCE_AUDIT_V2.md` §7.

---

## 4. Load-bearing design decisions (D17–D21)

| # | Decision | Essence |
|---|---|---|
| **D17** | Prompt-architecture rebuild — the v2 course | 16 weekly topics (nb00–nb15) over a 43-meeting calendar (41 in-person + 2 async; no class Wed Nov 18), milestones M0–M15; Weeks 5–9 = the five DeclareDesign pathways with prediction as its own objective; compass retained, four-approach grid stays retired; four-section studio Fridays. |
| **D18** | Flipped classroom — Student Research Lead | Every Mon/Wed lecture from Week 2 is student-led Socratic investigation; 5 leads per student; fixed four-section 50-min architectures; 9-dimension SRL rubric. |
| **D19** | AI stack — Gemini primary, GenAI Studio reviewer bench | Gemini stays the embedded assistant; GenAI Studio built as the reviewer bench with required milestone touchpoints; six-level taxonomy, implemented at levels 1–4 only, no autonomy claimed. |
| **D20** | The course book — 37 chapters, six parts | Full open-access Quarto book synchronized both ways with notebooks + site via `validate_book_sync.py`; built after notebooks stabilized to keep one source of truth. |
| **D21** | The AI Research Ledger | v1 ledger + disclosure block unified into one eight-field graded artifact, distinct from the claim ledger; missing entries → Craft 0, returned. |

---

## 5. Validation performed

1. **Full machine gate battery — green:** `validate_calendar`, `build_meeting_schedule`,
   `validate_milestones` (M0–M15), `validate_coverage` (full file-level),
   `validate_notebooks`, `voice_lint_notebooks`, `audit_sources`,
   `validate_book_sync`.
2. **Week-5 prototype quality pass:** nb04 + M4 taken to a fully-verified reference
   bar (12 must-fixes applied) as the quality template for the remaining notebooks.
3. **15-notebook adversarial verify pass:** every notebook except the nb04 prototype
   run through a re-derive-the-numbers, orphan-requirement, and prompt-quality
   adversarial check with fix-and-rebuild.
4. **Phase-7 cross-course audit (this report):** 11 independent auditors across
   consistency, feasibility, book-align, links, accessibility, reproducibility,
   STEM-breadth, poster-evidence, adversarial-AI, adversarial-design, and
   GenAI-oversell.

**Aggregate audit result: 0 critical · 11 high · 12 medium · 18 low (41 total).**

---

## 6. Audit results by dimension

Each auditor's ship verdict, with finding counts. Full findings and fixes are in
`planning/AUDIT_FIXLIST.md`.

| Dimension | Verdict | H | M | L | Headline issue |
|---|---|---|---|---|---|
| **consistency** | Fix 2 highs before ship | 2 | 1 | 2 | Ledger field 8 is "responsible student" in the published syllabus but "responsible researcher" everywhere students use it; the "four required GenAI Studio milestones" policy is contradicted by graded consults built into M6 and M8 (six in fact). |
| **feasibility** | Mechanically sound; **workload density needs attention** | 2 | 3 | 2 | Post-Thanksgiving pile-up (M13→M14→M15 in three weeks) and the Week-9 technical peak (hardest notebook nb08 + first real analysis M8 together); no credit-hour/workload calibration anywhere. |
| **book-align** | Fundamentally sound; one live-site defect | 1 | 1 | 1 | 7 chapters link the verification guide with a relative path that 404s on the published site; book chapters bypass the citation gate. |
| **links** | Essentially sound | 1 | 0 | 1 | `callingbullshit.org/tools/` 404s across 7 student notebooks (correct path is `/tools.html`); one-way book navigation. |
| **accessibility** | Largely sound, one real fix | 1 | 1 | 1 | Accessibility is taught + drilled as a required poster-review lens but is absent from the graded red-team protocol and poster rubric; 17 `<img>` tags lack alt text. |
| **reproducibility** | Fundamentally sound; light cleanup | 0 | 2 | 3 | Hidden `tau` cross-cell dependency in nb08's spillover/clustering cells; stale v1 notebook mapping in the data README. |
| **stem-breadth** | Fundamentally sound; ships as-is | 0 | 1 | 1 | All five hands-on datasets are civic/political-science; a bio/chem student computes on off-field (and politically charged) data in every lab. |
| **poster-evidence** | **Needs a v1→v2 reconciliation pass** | 2 | 2 | 2 | The 9-file poster/conference protocol suite is still on v1 M00–M23 (all "Governs" links dangle); two competing 100-point poster rubrics govern the same terminal poster, one omitting the ledger row that returns the submission unread. |
| **adv-ai** | Sound to ship | 0 | 0 | 3 | Strong: commit-first prompts, never-delegate lists, human-only checkpoints, oral defense. Only label-consistency and pre-stated-headline polish. |
| **adv-design** | Sound; ships | 0 | 0 | 1 | One cross-validation wording gloss in ch14 looser than its own lab (nb07). |
| **genai-oversell** | Core sound; modest reconciliation | 2 | 1 | 1 | Three docs promise nb15 teaches the six-level taxonomy / levels 5–6, but the notebook never mentions it; `agent_role_cards.md` contradicts the rest of the suite on where 8 of 13 roles live. |

**Cross-cutting theme (the biggest single work item):** four findings
(poster-evidence ×2 high + ×2 medium) plus the data-README stale mapping share one
root cause — **the poster/conference layer and a couple of provenance docs were
never migrated off the retired v1 M00–M23 numbering.** Treat these as one
reconciliation pass in Stage-8.

---

## 7. Remaining external dependencies (out of our control — instructor to confirm)

1. **URC abstract deadline (TBD):** the internal abstract gate is currently coupled
   to the Oct 9 studio; the real Purdue URC Expo abstract deadline must be confirmed
   and the internal gate scheduled to precede it with slack.
2. **GenAI Studio student-access verification:** the reviewer bench assumes all 5
   students can reach `genai.rcac.purdue.edu` and the shared course group. Instructor
   must verify access before the semester (open item flagged in D19).
3. **Honors College grading confirmation:** the 16-graded-milestone cadence and the
   SRL-led lecture grading need Honors College sign-off on grade weighting and the
   every-week deliverable model.
4. **Poster print logistics:** URC Expo poster print size, deadline, and print vendor
   for Tue Nov 17 are not yet fixed; production checklist references need a real print
   path.
5. **Nov 18 no-class day:** confirm the instructor-declared "post-Expo" cancellation
   against the official Purdue Fall 2026 academic calendar and document the
   contact-hour rationale if it is not a university non-instructional day.

---

## 8. Recommended next steps

1. **Run Stage-8 from `planning/AUDIT_FIXLIST.md`, highs first.** The 11 high-severity
   items cluster into five workstreams:
   - **(a) v1→v2 poster/conference reconciliation** — renumber the 9 protocol files
     and `MILESTONE_PRESENTATION_MAP.md` to M0–M15, repoint every "Governs" link,
     collapse the two poster rubrics to `milestone_10` as the single source, and
     repoint `scripts/schedule_data/part3.py`/`part4.py` (then regenerate the
     schedule so the poster-criticism week no longer shows "—" for its reading).
   - **(b) Terminology fixes** — `responsible student` → `responsible researcher` in
     `syllabus.qmd`; reconcile the "four vs six required GenAI Studio milestones"
     policy across syllabus/index/config/README/M6/M8.
   - **(c) Broken links** — the 7-chapter verification-guide relative path and the
     `callingbullshit.org/tools/` 404 (fix in the `_production_kit` sources, then
     `nbbuild.py` + `sync_instructor_repo.sh`).
   - **(d) Accessibility in the graded instruments** — add a 5th accessibility audit
     block + rubric criterion; add alt text to all 17 `<img>` tags.
   - **(e) GenAI Studio doc↔notebook reconciliation** — add the taxonomy/levels-5–6
     cell to nb15 (or soften the three docs) and fix `agent_role_cards.md`.
2. **Address the two feasibility highs deliberately** (design decisions, not just
   edits): relieve the post-Thanksgiving pile-up (push M14 to Dec 7 and/or reduce M13
   to reproduce-only) and decouple the Week-9 technical peak (move M8 earlier or
   hard-cap the first estimate; ship a fill-in-the-blank worked exemplar). Add a
   credit-hour + expected-weekly-hours line to the syllabus and a per-brief effort
   budget.
3. **Sweep the mediums/lows** in the same pass where cheap: nb08 `tau` fix + rebuild,
   regenerate the data-README "Course use" column, extend `audit_sources.py` over the
   book chapters, add the STEM teaching dataset (or the neutral-instrument sentence).
4. **Re-run the full gate battery** after fixes, **re-render `docs/`** (site + book),
   commit, push, and **re-sync the instructor repo**.
5. **Close the external dependencies** in §7 with the instructor before Week 1.
6. **Tag `v2-audit-shipped`** once Stage-8 lands and the battery is green again.

---

*Prepared by the Phase-7 lead reviewer, synthesizing 11 independent auditors.
Companion: `planning/AUDIT_FIXLIST.md` (severity-ranked fix list driving Stage-8).*

---

## Stage-8 revision outcomes (2026-07-23)

All **11 HIGH** findings and the load-bearing mediums are resolved; the full
validator battery is green and the site + book re-rendered.

**Fixed (committed):**
- **H1/H2/H7/M-PE1/M-PE2** — the poster + conference protocol suite (9 docs) and
  `MILESTONE_PRESENTATION_MAP.md` migrated off v1 M00–M23 to v2 M0–M15; every
  dangling "Governs" link repointed to an existing brief; a single poster rubric
  (milestone_10); an Accessibility audit added to the red-team protocol; the
  schedule-data references corrected so the published schedule shows real
  readings.
- **H3** — the AI Research Ledger's 8th field is "responsible researcher" in the
  syllabus, matching everywhere else.
- **H4** — the four required GenAI Studio touchpoints (M5/M7/M9/M13) are now the
  single required set; the M6/M8 briefs reframe their reviewer consult as
  optional (Gemini or a Studio role), removing the contradiction.
- **H5/H6** — the 7 book chapters' verification-guide links and the
  `callingbullshit.org/tools` link (404) fixed; both now resolve.
- **H8** — nb15 gains a six-level AI-capability-taxonomy cell (this week = level 4;
  levels 5–6 named and marked as NOT used), closing the "agentic overreach" gap.
- **H9/M-GO1** — `agent_role_cards.md` reconciled (all 13 roles are Studio custom
  models; 8 also runnable as Gemini prompts); the multi-model lesson corrected to
  point at nb09.
- **M-C1/M-R1/M-R2/M-BA1** — INQUIRY_MAP pathway count; nb08 hidden-state; the
  data-README course-use column; and `audit_sources.py` now gates the 37 book
  chapters (blocklist).

**Deferred to the instructor as course-design decisions (NOT changed
unilaterally — they move validated calendar anchors or add scope):**
- **H10 / M-F1 / M-F2 — end-of-term deadline density.** M13 (Sun Nov 29, over
  Thanksgiving) → M14 (Fri Dec 4) → terminal M15 (Fri Dec 11) stack three heavy
  deliverables with no slack. Options: push M14 to Mon Dec 7; make M13's red-team
  optional; decouple the URC-abstract internal gate from the crowded Oct 9 studio;
  designate one no-new-milestone consolidation studio (e.g. after the M8 peak).
- **H11 — Week 9 peak.** nb08 (the most demanding notebook) coincides with M8
  (first real computed estimate). Consider a fill-in-the-blank worked exemplar or
  capping M8's first estimate to one number for causal/experimental projects.
- **M-F3 — workload transparency.** Add a credit-hours + expected-weekly-hours
  line to the syllabus and a one-line effort budget to each brief.
- **M-SB1 — STEM-dataset concentration.** All five shipped datasets are
  social/political science; the book teaches field-diverse examples but every
  in-lab dataset is civic. Consider shipping ≥1 STEM teaching CSV (environmental
  sensor / agronomy trial / materials) and routing 1–2 labs (nb04, nb08) to it,
  or a one-sentence framing per `load_course_data` cell. (Own-field data enters
  through each student's project.)

The remaining LOW findings (18) are cosmetic polish batched for a future pass.

## Stage-9 final validation — verified

- Every class totals 50 planned minutes (session-guide generator asserts the sum;
  regenerates clean). Mon/Wed run 4 sections with a central 22–23-min AI
  investigation; every Mon/Wed from Week 2 is Student-Research-Lead-led (**25
  slots, exactly 5 per student**).
- Every notebook carries the machine-checked AI-intensity contract (≥4 Gemini
  prompt sequences, prompt modification, output interrogation, Human-Only
  Checkpoint, AI Research Ledger, Exit Defense) + a runnable/human-verification
  step. All 16 executed clean and passed the adversarial verify pass.
- Every Friday advances the project; poster locked **Fri Nov 6**; conference prep
  precedes the **Tue Nov 17** Expo; **Wed Nov 18 is no class**; Thanksgiving work
  is the async nb13/M13; post-conference work spans reflection (M12), replication
  (M13), research note (M14), and the multi-agent chapter + portfolio (M15).
- Book, site, notebooks, milestones, and rubrics are synchronized and gate-checked
  (validate_book_sync, validate_coverage, validate_milestones, validate_notebooks,
  voice_lint, audit_sources incl. the book). No hardcoded secrets; no substantive
  placeholders. **0 critical findings.**

**Status: the v2 course ecosystem is complete and internally consistent.** The
deferred items above are the instructor's calls, not defects.
