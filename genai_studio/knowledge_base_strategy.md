# Knowledge base strategy — GenAI Studio for HONR 46400

*How the course grounds its reviewer roles in course-authored knowledge, what
may and may not be uploaded, how the collections are shared with the five
students, and when they are refreshed.*

A GenAI Studio custom model becomes a **RAG-supported assistant** (level 3 of
the taxonomy) when you attach a *Knowledge* collection to it: uploaded documents
that the model retrieves from and answers grounded in. This document is the plan
for those collections. It is verified against GenAI Studio's documented behavior
(custom models + attached Knowledge, shareable via groups) as of 2026-07-22.

---

## Design principles

1. **Course-authored material only.** Every document in every collection is
   written by the instructor or generated from this repository. This keeps the
   knowledge base copyright-clean and keeps the roles anchored to *this course's*
   definitions, not the open internet.
2. **Grounding narrows, it does not license.** Attaching a collection makes a
   role cite the course's own definitions instead of drifting. It does **not**
   make the role authoritative. A grounded role can still retrieve the wrong
   passage, miss context, or hallucinate around a real quote. Every role still
   ends with "What you must verify yourself," and every output is still verified.
3. **Small, named, single-purpose collections.** Each collection covers one kind
   of knowledge so a role can attach exactly what it needs and nothing that would
   dilute retrieval.

---

## ⚠️ What must never be uploaded

These prohibitions are hard rules. Violating any one is an integrity and
possibly a copyright or privacy failure.

- **No RDSS chapters, and no other copyrighted or third-party text.** *Research
  Design in the Social Sciences* (Blair, Coppock & Humphreys) is the assigned
  theory text; students read it from the free authorized edition. Its chapters,
  figures, and long quotations do **not** go into a knowledge base. The
  `research-design-definitions` collection paraphrases course concepts in the
  instructor's own words and cites RDSS by chapter for the student to read
  directly — it never reproduces the book.
- **No student data.** Never upload a student's dataset, survey responses, or any
  file that could carry personal or identifying information about research
  subjects.
- **No student drafts containing personal information.** Anonymized exemplars
  written or cleared by the instructor are fine; a live student's named draft is
  not.
- **No secrets.** No API keys, passwords, gradebooks, or the contents of the
  private instructor repository.

When in doubt, leave it out and ask the instructor. A role grounded in slightly
less material is fine; a knowledge base that leaks a subject's data is not.

---

## The seven collections

Each collection lists what goes in and which roles attach it. Source paths are
this repository's course-authored files; the instructor exports or copies the
relevant sections into GenAI Studio Knowledge uploads.

### 1. `course-policies`
- **Contains:** the AI policy and the SDIIVDD / Ask → Verify → Document loop; the
  never-delegate list; the AI Research Ledger definition and its eight fields;
  the evidence-integrity and uncertainty-and-limitations rules; academic-integrity
  expectations. Sourced from `course_config.yaml ai_policy:`,
  `ai_resources/ai_research_ledger_template.md`, and the syllabus policy pages.
- **Attached to:** socratic_research_tutor, ai_research_team_orchestrator, and (as
  a secondary attachment) every touchpoint role, so each can point a student back
  to the never-delegate boundary.

### 2. `milestone-briefs`
- **Contains:** the M0–M15 student-facing briefs and their submission
  requirements. Sourced from `_research_project/2026Fall/milestone_NN_*.md`.
- **Attached to:** research_question_diagnostician, ai_research_team_orchestrator,
  and each touchpoint role for the milestone it serves.

### 3. `rubrics`
- **Contains:** the 100-point, four-band, five-virtue rubric menu (compass
  alignment, evidence integrity, verification, uncertainty & limitations, craft)
  and the hard-cap penalties. Sourced from `_research_project/2026Fall/rubric/`
  and the per-milestone inline rubrics.
- **Attached to:** mida_design_reviewer, observational_descriptive_auditor,
  experimental_design_reviewer, robustness_sensitivity_reviewer, poster_critic,
  research_note_reviewer.
- **Boundary note:** rubric grounding lets a role tell you *which quality a
  criterion asks for*. It must never be used to predict, assign, or negotiate a
  grade. Roles are instructed to refuse grade estimation; see each System Prompt.

### 4. `research-design-definitions`
- **Contains:** the inquiry compass (kind × reach), the four named positions
  (description, generalization, prediction, causal reasoning), the three crossings
  and their licenses, and the design-library pathways — all in the instructor's
  own words. Sourced from `planning/INQUIRY_MAP.md`,
  `course_config.yaml inquiry_framework:`, and the course glossary. **Paraphrase
  of course concepts; not RDSS text.**
- **Attached to:** socratic_research_tutor, research_question_diagnostician,
  mida_design_reviewer, observational_descriptive_auditor,
  causal_identification_skeptic, experimental_design_reviewer,
  prediction_leakage_auditor.

### 5. `poster-requirements`
- **Contains:** the poster storyboard, data-ink standards, the claim-boundary and
  untraceable-number rules, the poster red-team protocol, and the URC Expo poster
  format expectations. Sourced from `project/poster/`.
- **Attached to:** poster_critic.

### 6. `reproducibility-standards`
- **Contains:** the reproducibility-capsule and replication-package requirements,
  the cold-reproduction and signed-attestation protocol, and the red-team report
  format. Sourced from `project/reproducibility/`.
- **Attached to:** reproducibility_auditor, research_note_reviewer,
  robustness_sensitivity_reviewer.

### 7. `examples-and-counterexamples`
- **Contains:** short, instructor-written or instructor-cleared exemplars of good
  and flawed research moves — a well-scoped question next to an overclaiming one,
  a defended identification argument next to a design-mimicry one, a leak-free
  protocol next to a leaking one. **Anonymized and course-authored only; no live
  student work.**
- **Attached to:** causal_identification_skeptic, prediction_leakage_auditor,
  reproducibility_auditor.

---

## Group sharing setup

- **One course group.** The instructor creates a single group (for example,
  `HONR464-F26`) and adds the five enrolled students with **read access** to the
  shared custom models and their attached knowledge collections. Read access lets
  students *use* the roles; it does not let them edit a system prompt or alter a
  collection.
- **The instructor owns every model and collection.** Only the instructor creates,
  edits, or deletes the roles and the knowledge uploads. This keeps the reviewer
  bench identical for all five students and prevents drift.
- **No cross-posting of student material into the group.** Students consult the
  shared roles with their *own* pasted artifacts in their *own* chats. Nothing a
  student pastes into a role chat is added to a shared collection.

Step-by-step group and model creation lives in `instructor_setup_guide.md`.

---

## Refresh cadence

Knowledge collections are living documents. Refresh them on these triggers, not
on a fixed clock:

- **After any milestone-brief change.** If a brief in
  `_research_project/2026Fall/` is edited, re-upload it to `milestone-briefs` the
  same day, so a touchpoint role never grades a student against a stale
  requirement.
- **After any rubric change.** Re-upload to `rubrics`.
- **After a definitions or pathway change** (an edit to `INQUIRY_MAP.md` or the
  `inquiry_framework:` block): re-export the paraphrased definitions to
  `research-design-definitions`.
- **After a poster or reproducibility protocol change:** refresh
  `poster-requirements` or `reproducibility-standards`.
- **Version stamp.** Each collection's first document carries a one-line
  "Refreshed: YYYY-MM-DD from <source>" note, so the instructor can see at a
  glance whether a role is running on current material.

A refresh is re-uploading the changed document and confirming, in one test chat,
that the role now retrieves the new version. Because the roles are grounded but
still fallible, the refresh does not remove the standing requirement that every
output be verified against the source of truth in this repository.
