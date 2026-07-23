# BUILD_STATUS_V2 — the v2 rebuild re-entry point

**Read this first on resume.** The Fall 2026 course was rebuilt to the
instructor's master-prompt architecture (16 weekly topics nb00–nb15, milestones
M0–M15, Student Research Lead flipped classroom, AI Research Ledger + SDIIVDD,
GenAI Studio reviewer bench, 37-chapter course book). Governing decisions:
`_project_docs/DECISIONS.md` D17–D21; operating manual: `CLAUDE.md` v5.0;
audit + rulings + reuse map: `planning/SOURCE_AUDIT_V2.md`; the prototype
quality bar: `planning/QUALITY_REPORT_P3.md`. v1 preserved at git tag
`v1-compass-build`; v1 notebook sources archived in
`_production_kit/nb_sources_v1/`.

> ## ✅ v2 BUILD COMPLETE (2026-07-23)
> All seven phases done: spine, resources, prototype (3-reviewer pass), 16
> notebooks + 16 milestone packages, GenAI Studio suite, 37-chapter book, and
> the Phase-7 cross-course + adversarial audit (0 critical) with Stage-8 fixes
> applied and Stage-9 validation verified. Full battery green; site + book live;
> instructor repo synced. Remaining items are instructor course-design decisions,
> not defects — see `planning/FINAL_REPORT_V2.md` (Stage-8 outcomes + deferred
> items). v1 preserved at tag `v1-compass-build`; v2 shipped at `v2-audit-shipped`.

Last updated: 2026-07-23, after **Phase 4 COMPLETE** (all 16 notebooks + 16
studios + 16 briefs built and gate-green; a second completion workflow ran
14/14 agents clean after the rate limit reset). Adversarial verify pass on the
15 workflow-built notebooks COMPLETE (15/15 clean). Phase 6 book + Phase 7 audit
+ Stage-8 fixes COMPLETE.

## DONE (committed + pushed + rendered + instructor-repo synced)

- **Phases 0–3, 5:** full v2 spine, all governance docs, all resource suites
  (SRL 8 · AI 9 · reproducibility 8 · GenAI Studio 18), course-level docs,
  hardened `ACTIVITY_TEMPLATE` + validators + generators + msNN build pipeline,
  GitHub Actions CI, the **fully-verified Week-5 prototype** (nb04 + M4, 12
  must-fixes applied), and **Phase 6 groundwork** (BOOK_MAP 37-ch manifest +
  `validate_book_sync.py`).
- **16 / 16 topic notebooks** built + executed + validated + badged live
  (nb00–nb15); **16 / 16 studio notebooks** (ms00–ms15); **16 / 16 milestone
  briefs** (M0–M15). Full battery green: validate_calendar / build_meeting_schedule
  / validate_milestones / validate_coverage (full file-level) / validate_notebooks
  / voice_lint / audit_sources.

## IN PROGRESS

- **Adversarial verify pass** (workflow) on the 15 notebooks that skipped the
  nb04-grade quality gate (all except nb04): re-derive numbers vs executed
  output, orphan-requirement check vs brief, prompt-quality audit, fix + rebuild.

## REMAINING after verify

- **Phase 6:** author the 37 book chapters (part-waves, gated by
  `validate_book_sync.py`) into `book/`; add the Book tab to `_quarto.yml`;
  render to `docs/book/`.
- **Phase 7:** cross-course audit (progression, workload, deadlines, terminology,
  links, citations, book↔notebook sync), a final adversarial "assume-failure"
  review, the Stage-9 validation checklist, and `planning/FINAL_REPORT_V2.md`.

## SUPERSEDED (historical — the first Phase-4 workflow's partial state)

The section below documented the mid-build remainder after the rate-limited
first workflow; it is now fully resolved (all artifacts built). Retained for
history only.

## REMAINING (the completion pass — needs agent capacity; session limit resets 12:20 ET)

## REMAINING (the completion pass — needs agent capacity; session limit resets 12:20 ET)

### A. Topic notebooks (4) — sources exist but are truncated/partial
| nb | slug | state | needs |
|---|---|---|---|
| nb02 | nb02_research_builds_on_research | 26 cells, first half only | author the tail: Make a Design Choice, Practice, Project Transfer, Exit Defense, Wrap-Up, Sources, thank-you; keep the good first half |
| nb03 | nb03_anatomy_of_design | 26 cells, first half only | same tail profile; 2-lecture week (MIDA + DAG) |
| nb10 | nb10_poster_criticism_lock | 53 cells, missing closing blocks | author the tail: Human-Only Checkpoint, AI Research Ledger, Exit Defense, Wrap-Up, Sources, thank-you (comm week — runnable-exempt) |
| nb15 | nb15_managing_ai_agents | 5 cells, barely started | author in full (capstone: multi-agent management + final defense) |

### B. Milestone briefs (9): M2, M3, M6, M7, M9, M10, M11, M14, M15
Pattern = `_research_project/2026Fall/milestone_04_observational_descriptive_audit.md`
(the v2 exemplar); mine v1 via `git show v1-compass-build:_research_project/2026Fall/<v1slug>.md`.

### C. Studio notebooks (12)
- Sources complete, need only an em-dash-budget voice fix then build: **ms05,
  ms08, ms13** (each has 2–6 em-dashes in 1–3 markdown cells; budget is ≤1/cell).
- Author + build: **ms02, ms03, ms06, ms07, ms09, ms10, ms11, ms14, ms15**.
  Registry slugs are in `scripts/notebooks_map.py MS_NOTEBOOKS`.

### D. Adversarial verify pass owed (11 notebooks)
The workflow-built + manually-recovered notebooks passed stage-1 authoring +
the automated gates but SKIPPED the stage-3 adversarial verify (the session
limit): **nb00, nb01, nb05, nb06, nb07, nb08, nb09, nb11, nb12, nb13, nb14.**
Each needs the nb04-grade pass: re-derive ≥3 reported numbers against executed
output (hunt output-vs-narration contradictions), orphan-requirement check
against its milestone brief, and prompt-quality/commit-first audit. nb04 is
already fully verified.

## Completion recipe (after reset)

1. Do NOT `resumeFromRunId` the original workflow — nb06/nb09/nb14 were rebuilt
   manually and a resume would re-author (overwrite) them. Launch a NEW workflow
   scoped to A–D above.
2. Suggested shape: `pipeline` over the 4 remaining weeks (author tail → brief →
   verify) + a `parallel` fan-out for the 9 standalone briefs + a `parallel`
   fan-out for the 12 studios + a final `parallel` verify pass over the 11
   unverified notebooks. Each agent: chunked writes; build with `--no-badges`;
   iterate to green.
3. Central finalize: `update_schedule_badges.py` (→ 16/16), `build_material_page.py`,
   `quarto render`, commit docs, push, `sync_instructor_repo.sh`.
4. Then Phase 6 (37-chapter book) and Phase 7 (cross-course + adversarial audit,
   Stage-9 checklist, `planning/FINAL_REPORT_V2.md`).

## Build reminders
- `.claude/.autocommit-off` is present (session autocommit disabled during batch
  builds) — remove it when the batch work is done to restore turn-end autocommit.
- Parallel notebook builds MUST use `.venv/bin/python scripts/nbbuild.py nbNN --no-badges`;
  regenerate badges once, centrally, at the end.
- Every gate green before commit: validate_notebooks, voice_lint_notebooks,
  audit_sources; then render before committing docs/.
