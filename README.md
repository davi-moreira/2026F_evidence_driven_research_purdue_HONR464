# HONR 46400 — SP: Evidence-Driven Research (Fall 2026)

Course materials for **HONR 46400: Evidence-Driven Research**, a semester-long
Honors College seminar at Purdue University (Fall 2026, Mon/Wed/Fri, in person),
taught by **Professor Davi Moreira**.

- **Website:** https://davi-moreira.github.io/2026F_evidence_based_research_purdue_HONR464/
- **Repository:** https://github.com/davi-moreira/2026F_evidence_based_research_purdue_HONR464

## What this course is

Honors students learn to turn curiosity into credible, evidence-based insight —
**without requiring a strong background in quantitative methods or computing**.
Students identify meaningful gaps in a chosen field, translate them into
well-scoped research problems, formulate answerable research questions, select and
justify an appropriate method family (description, statistical inference,
predictive modeling, and/or causal reasoning) at a **conceptual** level, and use
computational tools and AI to locate sources, operationalize concepts, analyze
evidence, verify results, and document decisions responsibly. They finish able to
design and defend a rigorous research approach, interpret findings with appropriate
uncertainty and limitations, and communicate results in **written and oral**
formats.

## Repository structure

| Path | Contents |
|---|---|
| `index.qmd`, `syllabus.qmd`, `schedule.qmd` | Quarto site pages (rendered to `docs/` → GitHub Pages) |
| `activities/` | Student activities / worksheets (`actNN_*_student.ipynb`) |
| `_research_project/` | Semester research-project milestone instructions + rubrics |
| `_project_docs/` | AI-assistant operating docs, templates, decisions, troubleshooting |
| `scripts/` | Course-ops automation (seed, sync, voice-check, eval analyzer, audits) |
| `styles.css`, `images/` | Site styling and assets |
| `CLAUDE.md` | AI-assistant operating manual for this repo |
| `NEW_COURSE_SETUP.md` | How this repo was seeded from the MGMT474 infra + the build plan |

Instructor-only materials (session guides, Brightspace pages, quizzes, worksheets,
handouts, grading, and any `*_instructor*.ipynb`) are gitignored and kept local.

## Provenance

The course **infrastructure** (Quarto site, `.claude` hooks, `scripts/` framework,
planning-doc templates, instructor→student generation, assessment/milestone
scaffolding) was seeded from
`2026Summer_predictive_analytics_purdue_MGMT474`. The quantitative machine-learning
**content spine** of that course was intentionally not carried over — HONR 46400 is
a different, non-quantitative course whose curriculum is built fresh. See
`NEW_COURSE_SETUP.md`.

## License

See `LICENSE`.
