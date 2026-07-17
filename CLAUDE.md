# HONR 46400 Evidence-Driven Research — AI Assistant Guide

This file documents the rules and workflows that change Claude's behavior in this
repository. Reference material lives in linked files — read those when relevant,
not by default.

## Project Mission

**HONR 46400 — SP: Evidence-Driven Research**, a semester-long Honors College
seminar (Fall 2026, meeting **Mon/Wed/Fri, in person**) for Purdue's Honors
College. The course teaches honors students — **without assuming a strong
quantitative or computing background** — to turn curiosity into credible,
evidence-based insight: identify meaningful gaps in a chosen field, translate gaps
into well-scoped research problems, formulate answerable research questions, select
and justify an appropriate quantitative method **family** (description, statistical
inference, predictive modeling, and/or causal reasoning) at a **conceptual** level,
and use computational tools + AI to locate sources, operationalize concepts,
analyze evidence, verify results, and document decisions responsibly. Students
finish able to design and defend a rigorous research approach, interpret findings
with appropriate uncertainty and limitations, and communicate results effectively
in **written AND oral** formats.

- **Instructor:** Professor Davi Moreira
- **Repository:** https://github.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464
- **Website:** https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/
- **Deployment:** Quarto → `docs/` → GitHub Pages

## See Also (Reference Files)

| File | When to read | Status |
|---|---|---|
| `_project_docs/ACTIVITY_TEMPLATE.md` | Creating/restructuring a student activity — full section skeleton | ✓ seeded (renamed from NOTEBOOK_TEMPLATE.md) |
| `_project_docs/DECISIONS.md` | Before proposing changes to conventions (deliverable formats, AI-tool stack, sourcing standards) | ✓ seeded (adapt) |
| `_project_docs/TROUBLESHOOTING.md` | Render fails, Pages stale, git push rejected, leaked solutions | ✓ seeded |
| `_project_docs/COURSE_MATERIAL_WORKFLOW.md` | Producing one unit end-to-end (activity → session plan → Brightspace page → quiz) | ✓ seeded (adapt for MWF/in-person) |
| `_project_docs/HONR464_Semester_Plan_2026Fall.md` | Master course plan — source of truth for sequencing | ⬜ **to create** (curriculum session) |
| `CONVERSATION_LOG.md` | Project history and prior decisions | ✓ fresh |
| `scripts/voice_check_guides.py` | Before every session-guide edit | ✓ seeded (repointed) |
| `scripts/audit_answer_length.py` | Before importing any MC quiz CSV (only if MC banks are used) | ✓ seeded (optional) |
| `scripts/audit_sources.py` | Before shipping any activity with empirical claims (citation-integrity gate) | ⬜ **to create** |

**Canonical activity reference:** `activities/act01_*_student.ipynb` — match its
formatting exactly (once the first activity exists).

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
grep -iE '\bstudents?\b|\bthe instructor\b|on camera|speaking prompt' activities/actNN_*_student.ipynb   # expect 0 hits
python3 scripts/voice_check_guides.py session_guides/NN_session_guide.md
```

---

## 🚨 CRITICAL RULE — Narrative Polish Pattern (Named-Stakeholder Style)  *(KEEP — swap personas)*

Every student-facing markdown cell follows the course narrative style:
1. **"Why This Matters" cell** opened by a named research-world stakeholder whose
   concern is a direct quote — a **thesis advisor**, **journal reviewer**, **IRB
   reviewer**, **skeptical peer**, or **policy stakeholder**.
2. **Narrative prose over bullet lists** in "Reading the evidence" cells.
3. **Inline Q&A blocks** with the grep-findable phrase **"A question that often
   comes up here:"** — `> **A question that often comes up here:** *"<q>"* <one flowing paragraph>`.
4. **Section bridges** naming each transition in one sentence.
5. **Warm wrap-ups** ending with a bridge to the next activity.

---

## 🚨 CRITICAL RULE — Evidence-Integrity & Results-Verification  *(REPLACES the CV-First rule)*

The course's methodological spine — the analog of what CV-first was to the quant
course. Every empirical claim in any student-facing or deliverable material must be
**traceable and verified**:

1. **Every empirical claim traces to a real, retrievable source.** No fabricated,
   hallucinated, or unverifiable citations. If a claim came from an AI tool, the
   underlying source is independently located and confirmed to exist.
2. **Every result is verified before it is reported** — the deliverable records how
   the output was cross-checked (recomputed, triangulated, or spot-checked).
3. **Decisions are documented, not just outcomes** — which sources, which
   operationalization, which method family, and *why*.

```bash
python3 scripts/audit_sources.py activities/actNN_*_student.ipynb   # (to create) flags uncited claims, dead links, hallucinated-citation patterns
```

---

## 🚨 CRITICAL RULE — Method-Selection Justification  *(NEW)*

Whenever a student picks a method family (description / statistical inference /
predictive modeling / causal reasoning), the activity or milestone must state, **at
a conceptual level**: (1) why that family fits the question, (2) what it can and
cannot establish, and (3) its key limitations and sources of uncertainty. A method
choice with no stated justification or limitation is incomplete.

---

## 🚨 CRITICAL RULE — Responsible-AI-Use Documentation  *(NEW — instantiates the mission)*

Every deliverable that used an AI tool records, in a short disclosure block: which
tool, for what task (locate sources / operationalize / draft / critique), and how
its output was verified. The verify step is a **graded habit**, not a formality.
Embedded AI prompts carry an **"After running, verify:"** checklist recast as a
responsible-AI habit — confirm cited sources exist, cross-check facts, log the
decision.

---

## 🚨 CRITICAL RULE — Uncertainty & Limitations in Communication  *(NEW)*

Findings are never communicated as certainties. Every written report and oral
defense states the uncertainty around its claims and the limitations of its evidence
and method. A results statement with no uncertainty/limitations framing is a defect
(the "overclaiming certainty" researcher-failure archetype).

---

## 🚨 CRITICAL WORKFLOW — Instructor-First Activity Editing  *(KEEP — "notebook"→"activity")*

ALWAYS edit `activities/actNN_*_instructor.ipynb` FIRST, then generate the student
file by stripping every cell whose source contains `INSTRUCTOR SOLUTION`.

- Markers (unchanged so audits keep working): `### INSTRUCTOR SOLUTION — Exercise N`,
  `# INSTRUCTOR SOLUTION`, `<!-- INSTRUCTOR SOLUTION -->`.
- Student placeholders: `### YOUR ANSWER HERE:` (text) / `# YOUR SOLUTION HERE`.
- The "solution" is now a **model exemplar** (a well-appraised source, a well-scoped
  question, a worked method-justification), not working ML code.
- Only `*_student.ipynb` is committed; instructor files are gitignored.

---

## 🚨 CRITICAL WORKFLOW — Sync Session Guides and Planning Docs  *(KEEP — repoint)*

Every time an activity is updated: (1) update its session guide
(`session_guides/NN_session_guide.md`, gitignored) and (2) if significant, update
the sequencing rationale in `_project_docs/HONR464_Semester_Plan_2026Fall.md`.

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

---

## 🚨 OPTIONAL RULE — MC Option-Length Parity  *(only if MC quizzes are used)*

If the course uses auto-graded Brightspace MC quizzes: every option ≥ 60% of the
longest option's length; the correct option is strictly longest in ≤ 40% of a
bank's questions; distractors carry equally-elaborated but flawed rationale.

```bash
python3 scripts/audit_answer_length.py --file <path-to-csv>   # PASS required before import
```

If the course assesses only via written/oral deliverables + rubrics, this rule and
its script are dormant but harmless.

---

## Style Guidelines  *(KEEP markdown hygiene; DROP the ML constants)*

| Setting | Value |
|---|---|
| Money in markdown cells | Always escape: `\$50,000` (unescaped `$` triggers LaTeX) |
| Tildes in markdown cells | Always escape: `\~30 sources`, `(\~0.5)` |
| Emoji vocabulary | `✓` success, `⚠️` warning, `📝` exercise, `💡` insight |

> `RANDOM_SEED = 474` and the 60/20/20 split from the source course are **dropped** —
> there is no model fitting here. Reintroduce a seed only if some later unit adds
> light reproducible computation.

## Naming and Commit Conventions  *(KEEP)*

- Student activities (committed): `actNN_topic_student.ipynb`
- Instructor activities (gitignored): `actNN_topic_instructor.ipynb`
- Commit messages: `<type>: <subject>` (feat|fix|docs|chore|build|refactor) with a
  trailing `Co-Authored-By:` line. Stage specific files — never `git add .`.

---

**Version:** 1.0 — seeded from 2026Summer_predictive_analytics_MGMT474 infra; quant
content spine replaced with the evidence-driven-research spine.
**Maintained by:** Professor Davi Moreira + AI Assistants
