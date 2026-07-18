# DECLAREPY BUILD PROMPT — the parallel R→Python parity project (read, then execute)

> This is the **parallel project**, NOT the course. The Fall 2026 course is fully built
> and must not be disturbed. Your job: turn the `rdss` / DeclareDesign instructional
> ecosystem into a real, tested Python package (`declarepy`). The `translation/` docs are
> the spec; the course notebooks are the reference implementations. Reading this file =
> executing it. Don't ask questions unless genuinely blocked; make documented assumptions.

## STEP 0 — READ FIRST (the spec is already written)
- `translation/R_TO_PYTHON_INVENTORY.md` — the 16-function load-bearing surface + what each R source contains, by chapter.
- `translation/API_MAPPING.md` — **the canonical Python reference implementations** (the inline helpers the course ships); `declarepy` extracts and generalizes these.
- `translation/SEMANTIC_DIFFERENCES.md` — the 10 R↔Python traps (RNG non-portability, NA semantics, HC2 default, tidy-eval, …); honor every stated **Convention**.
- `translation/VALIDATION_REPORT.md` — the tolerance-based validation protocol (5 checks) + the status ledger you will extend.
- `translation/TRANSLATION_ROADMAP.md` — the 6 tranches (T0 done → T5 release), acceptance gates, non-goals, risks.
- `translation/PARITY_MATRIX.csv` — the per-function status table (columns: r_function, r_package, python_target, status, course_notebook, course_date, priority, notes) — keep it current.
- `course_config.yaml` + `CLAUDE.md` — conventions, seed `464`, MIT + attribution to Blair, Coppock & Humphreys.

Reference material (read as needed, do not modify):
- R source: `_adm/_references/book/replication-materials/code/{declarations,diagnoses,figures,utilities}/*.R`; datasets `.../data/*.csv`; saved diagnosis objects `.../diagnosis_objects/*.rds`; problem sets `.../exercises/*.Rmd`.
- Python reference impls: `notebooks/instructor/nb0{4,7,9}_*.ipynb`, `nb1{0,1,3}_*.ipynb` (and their gitignored cell sources `_production_kit/nb_sources/`).

## MISSION
Build `declarepy` — a transparent, tested Python translation of the MIDA
declare → diagnose → redesign engine + the estimators, assignment/sampling
procedures, declaration library, and diagnosis objects the book uses — validated
against the book's published/reference outputs within tolerance.

## GUARDRAILS (do not violate)
1. **Isolation.** Touch ONLY `src/`, `tests/`, `examples/`, `pyproject.toml`, and the
   `translation/` docs. NEVER modify `notebooks/`, `_research_project/`, `planning/`
   (except `PARITY_MATRIX.csv`/`VALIDATION_REPORT.md`), `schedule.qmd`, `docs/`, or run
   `quarto render`. Parity work never changes a shipped notebook mid-semester (swaps
   happen between terms).
2. **Transparent core.** Design steps take **explicit callables and column names** — no
   tidy-eval / quosure emulation (SEMANTIC_DIFFERENCES §10). The pedagogy (explicit
   `Y0`/`Y1` potential-outcome columns, printed shape/NA checks) carries into the API.
3. **Validated, not assumed.** RNG streams are NOT portable (§1) — "parity" means
   **statistical agreement within tolerance**, never digit equality. Every element runs
   the VALIDATION_REPORT protocol before it is marked validated.
4. **MIT + attribution** throughout; carry a LICENSE/citation notice to Blair, Coppock &
   Humphreys and note upstream `randomizr`/`estimatr` licenses (verify at package time).
5. **Confirm the public name** (`declarepy` is a working name) with the DeclareDesign
   authors before any PyPI/release naming (T5); until then the importable name is `declarepy`.

## ENVIRONMENT
- Repo-local `.venv` exists (numpy/pandas/scipy/statsmodels/sklearn/networkx/nbclient).
  Add dev tools as needed: `pytest`, `mypy`, `plotnine` (T4 only, if chosen), `build`.
- **R is available locally** (`/usr/local/bin/Rscript`). Use it to generate **reference
  outputs** for validation: install `rdss` + `DeclareDesign` + `estimatr` + `randomizr`
  from CRAN, run the book's declaration/diagnosis `.R` files, and emit structured JSON/CSV
  the Python harness compares against. Also read the book's saved `diagnosis_objects/*.rds`
  (via `Rscript -e 'saveRDS→jsonlite'`) as ground truth. `rpy2` is allowed as an optional
  dev/validation aid — never a runtime dependency of `declarepy`.
- Create `pyproject.toml` (PEP 621): package `declarepy` under `src/declarepy/`, typed
  public interfaces where practical, docstrings, `pytest` + `mypy` config, reproducible
  seeds, MIT license, authors/attribution.

## EXECUTE — tranche by tranche (autonomous; stop only on an unresolvable validation gate)
Update `PARITY_MATRIX.csv` + `VALIDATION_REPORT.md` (+ `SEMANTIC_DIFFERENCES.md`/`API_MAPPING.md`
when you discover new ones) after each element. Commit per element/tranche.

**T1 — core engine (`declarepy`), the prereq for everything.**
Extract the API_MAPPING helpers into composable step objects:
`Model` (+ `potential_outcomes`), `Inquiry`, `Sampling`, `Assignment`, `Measurement`
(+ `reveal_outcomes`), `Estimator`, `Diagnosands`, `diagnose()`, `redesign()`,
`run_design()`/`draw_data()`, and the procedures `complete_ra`/`block_ra`/`simple_rs`/
`complete_rs`. **Acceptance:** reproduces the course notebooks' outputs exactly (same
seed 464) AND recovers declaration_2.1 / 9.1 / 10.1 / 11.1 / 18.1 diagnosands within the
VALIDATION_REPORT tolerances (bias ±0.02·sd(Y), power ±0.05, coverage ±0.03, RMSE ±10%).

**T2 — estimator fidelity.** Design-based SEs matching `estimatr`: HC1/HC2/CR2, blocked &
clustered difference-in-means, via statsmodels/linearmodels. **Acceptance:** problem-set
answer keys 1–4 reproduce within tolerance; HC2 is the default (SEMANTIC_DIFFERENCES §5).

**T3 — declaration library (course chapters first).** Translate the replication
declarations in course-priority order: ch.9 (7) → ch.10–11 (10) → ch.18 (13) → ch.15–16
(13) → ch.17 (7) → ch.19+23 (8). Each file → translation + a VALIDATION_REPORT row +
provenance line (`source-file | chapter | object | translated`).

**T4 — diagnosis objects + figures.** Recompute the book's saved `diagnosis_objects/*.rds`
in Python within tolerance; re-implement priority figures (decide matplotlib vs plotnine
at tranche start — plotnine is NOT a course dependency, only a parity-project choice).

**T5 — polish & release.** `docs/`, examples, CI matrix, a "for DeclareDesign users"
migration guide, packaging. Coordinate naming with the DeclareDesign authors before any
public release.

**Non-goals** (do not build): tidy-eval/quosure emulation; the `dataverse` download client
(datasets ship as CSVs); `DesignLibrary` breadth before T5.

## VALIDATION PROTOCOL (from VALIDATION_REPORT.md — apply to every element)
1. Structural check (same M/I/D/A steps as the R source).
2. Diagnosand tolerance check (≥1,000 reps; the bands above).
3. Known-truth check (analytic estimand recovered as reps→large).
4. Real-data check (shipped datasets, e.g. foos_etal DiM, lapop_brazil summaries — exact
   to 3 decimals; real data has no RNG excuse).
5. Record every validated element in the ledger with seed, reps, deltas. Any tolerance
   failure is logged with its investigation before the element may be marked validated.

## WORKING DISCIPLINE
- Work on a dedicated branch **`declarepy`** (`git switch -c declarepy` if absent) so the
  course `main` and the live schedule/badge review flow stay undisturbed; merge when a
  tranche is green. Stage files **by name**; never `git add .`; never touch `docs/`.
- Commit messages `<type>: <subject>` (feat|fix|test|docs|build) + trailing
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- `pytest` + `mypy` green before each commit; keep the tracked tree clean.
- Optionally track progress on a private issue in the `…-HONR464-tasks` repo.

## DEFINITION OF DONE (do NOT claim the package "complete" until all hold — brief §16)
- Every in-scope exported function AND dataset has a `PARITY_MATRIX.csv` entry.
- All required course notebooks *could* run on `declarepy` (T1 acceptance proven), though
  the notebooks themselves stay on their inline helpers this term.
- Tests pass; numerical tolerances are justified and recorded.
- Semantic differences are documented; every exclusion is justified in the roadmap.
- `VALIDATION_REPORT.md` shows a validated row for every translated element.
Report status honestly per tranche; "conceptual parity" and "exact parity" are labeled
distinctly. When all tranches are green, summarize and stop.
