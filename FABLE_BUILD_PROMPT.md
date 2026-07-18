# FABLE BUILD PROMPT — HONR 46400 (read this file, then execute it fully)

> This file is a self-contained directive for a fresh session. Reading it = executing it.
> The plan, scope decisions, and verified calendar are already locked and on disk from a
> prior session. Do not re-plan, re-audit, or re-litigate decisions. Do not ask questions
> unless something is genuinely blocking and unresolvable from the repo — otherwise make a
> documented assumption and proceed.

Continue and **CONCLUDE** the autonomous build of HONR 46400 — "Evidence-Driven Research"
(Purdue Honors College, Fall 2026, MWF, 5 students, 5 individual projects).

## STEP 0 — READ FIRST (in order)
- `planning/BUILD_STATUS.md` — the re-entry point: locked decisions, what's done, the ordered "Next actions"
- `CLAUDE.md` — the 6 critical rules (voice, provenance, commit+render, etc.)
- `course_config.yaml` — machine-readable spine: calendar, 4 approaches, conventions
- `planning/COURSE_MASTER_PLAN.md` — arc + the 20 topic-notebook map (nb00–nb19)
- `planning/SOURCE_AUDIT.md` — RDSS/`rdss` inventory, datasets, provenance convention
- `NEW_COURSE_SETUP.md` — infra lineage + gap list

Skim the two reference repos for **patterns only** (do NOT copy their ML content):
- `../../predictive_analytics/2026Summer_predictive_analytics_purdue_MGMT474/notebooks`, its `_final_project` (milestone md pattern), and `.claude/settings.json` (instructor-sync hook)
- `../../business_analytics/2026F_business_analytics_qm670/.claude/hooks` (hook suite)

## LOCKED (do not change)
- **Notebooks = ONE PER TOPIC:** `notebooks/{student,instructor}/nbNN_topic_*.ipynb` (~20, nb00–nb19). Each absorbs all the MWF meetings its topic needs. **Instructor-FIRST:** author `nbNN_*_instructor.ipynb`, then generate the student file by stripping every cell containing `INSTRUCTOR SOLUTION`. Student committed; instructor gitignored.
- **Milestones = MARKDOWN only** (instructions + rubric), in `_research_project/2026Fall/`, MGMT474 `_final_project` pattern (About → Submit table → Purpose → Components → Submission Expectations → Rubric points → Penalties → Pitfalls). No milestone notebooks. Cover the brief's **M00–M23** as graded, submittable milestones.
- **Calling Bullshit = optional / light only** (public callingbullshit.org where used).
- **rdss/DeclareDesign full Python parity = SEPARATE parallel project:** fill `translation/` with roadmap/inventory docs, do NOT build the package now. Notebooks implement RDSS concepts directly (numpy/pandas/scipy/statsmodels + small inline declare→diagnose→redesign sim helpers).
- **Conventions:** Google Colab, Python 3.11; numpy/pandas/matplotlib/scipy/statsmodels/scikit-learn/networkx; **NO seaborn**; seed `464`; escape `\$` and `\~` in markdown; emoji ✓ ⚠️ 📝 💡. Every meeting names the approach(es) + the claim **PERMITTED** and the claim **NOT permitted**. Every notebook: ≥1 pre-run prediction, ≥1 runnable activity, ≥1 defended decision, ≥1 practice item, ≥1 interpretation, ≥1 milestone/project transfer, a Claim-Ticket exit; exposition ≤8 min/segment, <15 min total; ≥70% active.
- **Student-facing voice:** write TO the student (second person), never ABOUT students, never instructor-facing language in student cells (CLAUDE.md critical rule).
- **Provenance line on every schedule row + notebook** (SOURCE_AUDIT §11): `source-file | chapter/section | page/figure/exercise/dataset | transformation`. Never invent citations, chapters, functions, or datasets.

## EXECUTE the remaining phases end-to-end
Update `planning/BUILD_STATUS.md` after each artifact (check items off).

**PHASE B — finish the planning suite** (author from COURSE_MASTER_PLAN + CALENDAR_BACKBONE.csv):
- `planning/MEETING_SCHEDULE.csv` + `.md` — 44 rows (M1–M44), all **32 columns** from the brief §8 (meeting#, date, day, modality, unit, title, driving question, secondary questions, approach, claim-permitted, claim-not-permitted, RDSS reading, CB reading/case if any, other material, provenance, concepts, Python/R dependency, dataset/simulation, EXACT 50-min minute-by-minute dynamic — vary it, hands-on activity, practice, discussion prompt, project connection, milestone developed, milestone work time, milestone presentation/review, student prep, student artifact, exit ticket, homework/next milestone, instructor prep, risks/contingency).
- `planning/QUANTITATIVE_APPROACH_MAP.md`, `planning/COURSE_DESCRIPTION_ALIGNMENT.md` (map every clause of the official description → units/readings/notebooks/milestones/assessments), `planning/READING_MAP.md`, `planning/PROJECT_MILESTONES.md`, `planning/MILESTONE_PRESENTATION_MAP.md`, `planning/ASSESSMENT_ARCHITECTURE.md`, `planning/COURSE_DEPENDENCY_MAP.md`.
- `project/templates/QUANTITATIVE_APPROACH_DECLARATION.md`.

**PHASE C — technical foundation:**
- Adapt the notebook template (strip ML-isms from `_project_docs/ACTIVITY_TEMPLATE.md`: drop RANDOM_SEED=474 / 60-20-20 / ISLP / Gemini / seaborn; add the 4-approach + claim-boundary header block, the Ask→Verify→Document AI-prompt+verify block, the Claim Ticket).
- `.claude/settings.json` hooks: keep instructor→md sync; **ADD** `scripts/update_schedule_badges.py` that rewrites the schedule Colab-badge row when a `nbNN_*_student.ipynb` is finalized (wire as PostToolUse); adapt QM670 `commit_push_reminder` + a notebook voice-lint.
- Ship the 5 datasets to `notebooks/data/` as CSV (from RDSS replication, MIT + attribution).
- `translation/` 6 docs (`R_TO_PYTHON_INVENTORY.md`, `PARITY_MATRIX.csv`, `API_MAPPING.md`, `SEMANTIC_DIFFERENCES.md`, `TRANSLATION_ROADMAP.md`, `VALIDATION_REPORT.md`) — framed as the parallel project, prioritized by course calendar.
- Validation scripts: notebook metadata check, active-learning-section check, approach-metadata check, provenance-field check, "every meeting has a notebook" check, reading-vs-inventory check, milestone dev/presentation/submission-date check.

**PHASE D — notebooks:** build gold-standard `nb00` + `nb01` first (instructor→student), get them clean, THEN build `nb02`–`nb19` to the same standard against the COURSE_MASTER_PLAN rows. Colab-runnable, deterministic (seed 464), small datasets, robust data loading with a fallback, clear errors, self-checks. Validate every notebook executes (nbclient/nbconvert). Generate each student file by stripping `INSTRUCTOR SOLUTION` cells. After each student notebook, update `schedule.qmd`'s Colab badge (hook or `scripts/`).

**PHASE E — project + poster system:** ~22 milestone md (M00–M23) with instructions + rubrics + submission checklists + examples/non-examples grounded in local materials + common mistakes + next-milestone links; the pilot-analysis milestone branches by approach (description/inference/prediction/causal). Build `project/{poster,conference,final_dossier}/` protocols + rubrics (storyboard, red-team peer review, claim defense, presentation plan, dress rehearsal, conference reflection, post-conference redesign, Nov-23 async dossier module, reproducibility audit, research brief, Evidence Defense, final dossier checklist). Update `syllabus.qmd` Assessments to the reconciled weights; set project mode to individual.

**PHASE F — final audit:** run `scripts/validate_calendar.py` and all validators; execute all notebooks; verify the brief's Quality Gates (44 meetings; Oct 2 & Nov 23 async; Nov 6 poster deadline; Nov 17 URC; all 4 approaches explicitly taught with claim boundaries; milestones have prior in-class dev time + a presentation/review + submission + revision; poster work not delayed to November; post-conference work substantive; notebooks carry no instructor answers). Write `planning/FINAL_REPORT.md` (generated files, schedule/milestone/notebook/translation status, validation results, unresolved risks, recommended instructor review sequence).

## WORKING DISCIPLINE
- Stage files **BY NAME** (never `git add .`). Commit in logical chunks with conventional messages ending `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **Publishing is pre-authorized.** Once you finish each **TOPIC** (its notebook validated + student file generated + schedule Colab badge updated), run the render → commit → **push** cycle and **publish GitHub Pages**: `quarto render` (`/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto render`) → `git add` the changed files + `docs/` → commit → `git push origin main`. This publishes each notebook so the professor can review it by opening its **Colab badge link on the live course schedule page**. Follow the Commit-AND-Render rule every time; skipping the render leaves the site stale. If `git push` fails on auth, run `gh auth refresh -h github.com` (or ask the professor to).
- Keep `_adm/_references/` gitignored; never commit instructor notebooks or private dirs.
- Track progress on private issue **#15**; comment a summary when each phase completes.
- When everything is done, validated, and pushed, give a concise completion report. The professor will then **review the notebooks one by one by opening each Colab badge on the published schedule page**, and edits will propagate.
