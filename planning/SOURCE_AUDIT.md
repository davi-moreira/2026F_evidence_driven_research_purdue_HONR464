# SOURCE_AUDIT — HONR 46400 (Phase A)

Comprehensive inventory of the local source-of-truth materials, with the provenance
convention every schedule row and notebook must follow. Audited 2026-07-17.

## 1. File inventory by resource type

| Type | Where | Notes |
|---|---|---|
| **Primary book support** | `_adm/_references/book/` | RDSS replication + exercises + slides + syllabi (gitignored) |
| Problem sets (5) + answer keys | `…/book/exercises/rdss-problem-set-{1..5}[-answer-key].{Rmd,pdf}` | power analysis, sampling, estimators, experiments, observational |
| Declarations (~70) | `…/replication-materials/code/declarations/declaration_*.R` | MIDA design code, book numbering |
| Diagnoses (~70) | `…/code/diagnoses/diagnosis_*.R` | Monte-Carlo diagnosis code |
| Figures (~90) | `…/code/figures/figure_*.R` + `…/figures/*.pdf` | ggplot2 figures + PDFs |
| Utilities | `…/code/utilities/make_dag_df.R` | DAG helper |
| Datasets (5) | `…/replication-materials/data/*.csv` (+ `fairfax.shp` set) | see §6 |
| Pre-computed diagnoses | `…/diagnosis_objects/*.rds` | saved sim outputs |
| Sample slides (3) | `…/book/sample-slides/sample-slides-{1..3}.pdf` | instructor decks |
| Sample syllabi (2) | `…/book/sample-syllabi/` | Blair 2023; Coppock AQRD 2021 |
| Package doc | `…/book/students/CRAN_ Package rdss.pdf` | `rdss` v1.0.14 |
| **Course infra (built)** | repo root | Quarto site, `CLAUDE.md`, `scripts/`, `_project_docs/`, `_research_project/2026Fall/` |
| **Syllabus compliance** | `_syllabus/complementary_material/` | Daniels syllabus checklist/template, logos |

## 2. Edition & version information

- **Book:** Blair, Coppock & Humphreys, *Research Design in the Social Sciences:
  Declaration, Diagnosis, and Redesign*, Princeton University Press, **2023**
  (companion site book.declaredesign.org). Book **text is not in the repo** — only
  replication code, figures, exercises, datasets, sample slides/syllabi.
- **R package:** `rdss` **v1.0.14** (published 2025-01-09; MIT + LICENSE file).
  Imports: dplyr, rlang, generics, ggplot2, tibble, tidyr, dataverse, readr, broom,
  purrr, estimatr, randomizr. Suggests: DeclareDesign, testthat, etc.
- **Ecosystem:** DeclareDesign, randomizr, fabricatr, estimatr, DesignLibrary (the
  MIDA toolchain the declarations/diagnoses depend on).
- **Calling Bullshit:** Bergstrom & West (2020) — **not in repo** (see §9).

## 3. Table-of-contents reconstruction (from replication numbering + public structure)

Chapter numbers observed in `declaration_*/diagnosis_*/figure_*` span **2–23**.
Reconstructed structure (paraphrased, not reproduced):

- **Front (ch. 1–4):** what a research design is; the declaration→diagnosis→redesign
  workflow; MIDA overview; classifying research questions. → `nb00–nb02`
- **Model & Inquiry (ch. 5–9):** causal models, potential outcomes, DAGs, estimands/
  inquiries, descriptive vs. causal inquiries. → `nb04, nb06`
- **Data & Answer strategy (ch. 9–15):** sampling, assignment, measurement, estimators,
  uncertainty, power/diagnosis. → `nb05, nb07, nb09, nb10, nb11`
- **Design library (ch. 15–19):** descriptive, observational-descriptive, experimental,
  and observational-causal designs (regression, DiD, RDD, IV, matching). → `nb13`
- **Complex designs & realization (ch. 20–23):** heterogeneous effects, spillovers,
  mediation; writing, ethics, reproducibility. → `nb18, nb19`

> This reconstruction drives the provenance column in `MEETING_SCHEDULE`; exact
> chapter/section/page attributions are filled per-notebook from the problem sets and
> declaration files actually used (never invented).

## 4. Instructor-resource map

- **Worked exemplars:** answer-key `.Rmd` for each problem set → model solutions to
  translate into Python "instructor solution" cells (concept-level, not R).
- **Sample slides / syllabi:** Blair 2023 + Coppock AQRD 2021 pacing → sanity-check for
  our arc; confirm our low-floor honors adaptation diverges intentionally (no measure theory).
- **Figures + diagnosis objects:** reference outputs for validating Python re-implementations.

## 5. R package & code inventory (translation scope)

Course-load-bearing DeclareDesign/`rdss` surface (full parity is the parallel project):
`declare_model` · `potential_outcomes` · `declare_inquiry` · `declare_sampling` ·
`declare_assignment` · `declare_measurement` · `reveal_outcomes` · `declare_estimator` ·
`declare_diagnosands` · `diagnose_design` · `redesign` · `run_design` /`draw_data` ·
`complete_ra`/`block_ra`/`simple_rs`/`complete_rs` · `difference_in_means` · `lm_robust`.
Mapped in `translation/API_MAPPING.md`; Python targets = numpy/pandas/scipy/statsmodels
+ small inline simulation helpers.

## 6. Dataset inventory (ship to `notebooks/data/` as CSV, MIT + attribution)

| Dataset | Rows/theme | Course use |
|---|---|---|
| `lapop_brazil.csv` | survey (AmericasBarometer, Brazil) | description, measurement, generalization |
| `la_voter_file.csv` | voter records | description, sampling, selection |
| `foos_etal.csv` | experiment replication | causal (experiments) |
| `cliningsmith_etal.csv` | experiment replication | causal |
| `bonilla_tillery.csv` | survey experiment | causal / measurement |
| `fairfax.{shp,dbf,shx,prj}` | spatial | optional description/mapping |

All available in the `rdss` package (CRAN) and in the replication archive; redistribute
the CSVs with an attribution note (see §8).

## 7. Prior-project implementation patterns worth preserving (MGMT 474 + QM670)

- Flat `notebooks/nbNN_topic_{student,instructor}.ipynb`; `figures/`, `data/`,
  `COMPLETION_STATUS.md`, `notebook_sequence_justification.md`.
- Milestone md (`_final_project/2026Summer/milestone_NN_*.md`): About → Submit table →
  Purpose → Components → Submission Expectations → Rubric (points) → Penalties → Pitfalls.
- Schedule Colab badge row format (see MGMT 474 `schedule.qmd` lines 39+).
- Hooks: MGMT 474 PostToolUse instructor→md sync; QM670 `.claude/hooks/`
  (`commit_push_reminder`, `guide_reminder`, `slide_voice_lint`, `brightspace_sync`).
- Incremental proposal→abstract→poster→final + peer eval + URC capstone cadence.

## 8. License & attribution constraints

- `rdss`: **MIT** (+ LICENSE) → translation of concepts and **redistribution of the
  bundled datasets is permitted with attribution**. Attribution line for shipped data:
  *"Dataset from the `rdss` package (Blair, Coppock & Humphreys, MIT License),
  companion to* Research Design in the Social Sciences *(2023)."*
- **Book text:** copyrighted — **paraphrase and transform**; never reproduce long
  passages. Figures: re-implement in Python rather than embedding the book PDFs.
- Calling Bullshit: cite the book; use only openly-licensed callingbullshit.org material.
- Keep `_adm/_references/` gitignored (already is).

## 9. Missing or ambiguous assets

- **Book chapter text** — absent (only replication code). Mitigation: reconstruct
  concepts from declarations/diagnoses/problem-sets + public structure; paraphrase.
- **Calling Bullshit materials** — absent. Mitigation: optional/light use from public
  callingbullshit.org; flag each CB touch as external provenance.
- **Confirmed URC abstract deadline** — TBD; internal gate M20 (Oct 9).
- **Prediction source** — RDSS stops short of a prediction entry in its design
  library; `nb12` authors the missing **"Observational: predictive"** entry in the
  book's own declare–diagnose–redesign format (still fresh scikit-learn content).

## 10. Which materials drive each unit
See the notebook table in `COURSE_MASTER_PLAN.md` §5 (per-notebook provenance column)
and `MEETING_SCHEDULE` (per-meeting). Description/generalization/causal draw on RDSS +
`rdss` datasets; prediction is fresh scikit-learn; communication/poster/dossier are
fresh; declaration→diagnosis→redesign draws on the declaration/diagnosis R files.

## 11. Source-provenance convention (used repo-wide)

Every schedule row and notebook records a provenance line:

```
provenance: <source-file or "fresh"> | <chapter/section/module> | <page/figure/exercise/dataset> | <transformation>
transformation ∈ { adapted | translated | extended | newly-constructed-from-source-concept | fresh }
```

Example: `provenance: declaration_18.1.R | RDSS ch.18 | declaration_18.1 (two-arm trial) |
translated (R→Python, DeclareDesign→numpy sim)`. Empirical claims trace to a real,
retrievable source; results are verified before reported; decisions (which source,
which operationalization, which compass position, and *why*) are documented, not just outcomes.
