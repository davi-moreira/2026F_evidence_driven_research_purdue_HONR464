# Instructor setup guide — GenAI Studio for HONR 46400

*Instructor-facing. How to stand up the reviewer bench in Purdue GenAI Studio
before the semester, keep it current during the term, run the course if student
API access does not materialize, and tear it down at term end.*

The guiding fact: **the manual UI workflow is the guaranteed path; the API is an
enhancement.** Set up the UI bench first and confirm every touchpoint works
without a single API key. Then add the API if student access checks out.

---

## Pre-semester checklist

Work top to bottom. Nothing here needs code except the final smoke test.

### 1. Sign in and confirm the platform
- [ ] Sign in at `https://genai.rcac.purdue.edu` with your Purdue account (SSO /
  CILogon).
- [ ] Confirm you can see the model catalog. Note the exact ids of the open-source
  models available to you (the LLaMA family; others may require a ticket). Write
  the id you will standardize on — you will paste it into the Colab PoC's `MODEL`.

### 2. Create the course group
- [ ] Create one group (suggested name `HONR464-F26`).
- [ ] You are the owner. The group is how the five students get read access to the
  shared role models and knowledge collections.

### 3. Create the seven knowledge collections
Follow `knowledge_base_strategy.md`. For each collection, upload only the
course-authored source material named there.
- [ ] `course-policies` · `milestone-briefs` · `rubrics` ·
  `research-design-definitions` · `poster-requirements` ·
  `reproducibility-standards` · `examples-and-counterexamples`.
- [ ] **Do not upload** RDSS chapters or any copyrighted third-party text, student
  data, or student drafts with personal information.
- [ ] Stamp each collection's first document with "Refreshed: <date> from
  <source>."

### 4. Create the 13 custom models
For each file in `roles/`, create one custom model.
- [ ] Name it **HONR464 — <Role>** (for example, *HONR464 — Poster Critic*).
- [ ] Base model: the standardized open-source id from step 1.
- [ ] System prompt: paste the **complete** fenced *System Prompt* block from the
  role's spec file, verbatim. Do not paraphrase or trim it — the refusal language,
  the output schema, and the "What you must verify yourself" instruction are
  load-bearing.
- [ ] Attach the *Knowledge Sources* the role names.
- [ ] Share each model with the `HONR464-F26` group.

The 13 roles: socratic_research_tutor, evidence_citation_verifier,
research_question_diagnostician, mida_design_reviewer,
observational_descriptive_auditor, causal_identification_skeptic,
experimental_design_reviewer, prediction_leakage_auditor,
robustness_sensitivity_reviewer, poster_critic, reproducibility_auditor,
research_note_reviewer, ai_research_team_orchestrator.

### 5. Add the students
- [ ] Add the five enrolled students to the group with **read access** (they use
  the models; they do not edit prompts or collections).
- [ ] Confirm with one student that they can open a role model from **Workspace**.

### 6. Confirm the touchpoints work UI-only
- [ ] In the UI, open each of the five touchpoint models (Causal Identification
  Skeptic, Prediction & Leakage Auditor, Poster Critic, Robustness & Sensitivity
  Reviewer, Reproducibility Auditor) and paste a short test artifact. Confirm each
  returns the structured schema and ends with "What you must verify yourself."
- [ ] At this point the course is fully runnable. Everything below is enhancement.

### 7. (Enhancement) Enable API access
- [ ] Confirm the OpenAI-compatible API is available to your account: generate a
  key under **Settings → Account** and run the Colab PoC (`colab_api_poc.md`)
  yourself end to end.
- [ ] Have **each student** generate their own key under **Settings → Account** and
  store it as a Colab Secret named exactly `GENAI_API_KEY` (never in code).
- [ ] Run the PoC smoke test as a student would, with the standardized `MODEL` id.

### 8. If a needed model is missing
- [ ] If the base model you want is not in the catalog, submit an **RCAC ticket**
  requesting it, well before the term. Until it lands, standardize on an available
  LLaMA-family model; the roles are model-agnostic.

---

## Term-time maintenance

- **Refresh knowledge on change, not on a clock.** When a milestone brief, rubric,
  poster or reproducibility protocol, or a definition changes, re-upload the
  affected document the same day and re-stamp its date. A touchpoint role must
  never critique against a stale requirement. (See `knowledge_base_strategy.md`.)
- **Keep system prompts in sync with the specs.** If a `roles/*.md` System Prompt
  changes, update the corresponding custom model's system prompt to match,
  verbatim. The Colab PoC pulls prompts live from the repo, so a UI model that
  drifts from its spec will behave differently from the API path — keep them equal.
- **Watch the touchpoint weeks.** Before M5 (Fri Oct 2, async), M7 (Fri Oct 16), M9
  (Fri Oct 30), and M13 (Sun Nov 29), re-run the UI smoke test for that week's
  role(s) so students hit a working model.
- **Do not add student material to shared collections.** Students consult roles
  with their own pasted artifacts in their own chats; nothing they paste enters a
  shared knowledge base.

---

## If student API access is unavailable

This is planned for, not a failure mode. GenAI Studio's explicit
student-eligibility terms and rate limits are not publicly documented, so treat
student API access as unconfirmed until you have verified it per student.

- **Run the course UI-only.** Every milestone touchpoint (M5, M7, M9, M13) is
  designed to work through Workspace → the group's role model → paste → copy the
  structured output → complete the ledger row. No key required.
- **The Week-16 sequential workflow still runs by hand.** Students open roles in
  order in the UI, verifying and ledgering at each step. The API only automates
  the sequencing; the pedagogy (the human orchestrates) is identical.
- **Tell students plainly** that the UI path is complete and sufficient, so no one
  believes they are missing something by not using the API.

---

## Teardown at term end

- [ ] Export any records you want to keep (your own notes; do not export student
  chats containing their material).
- [ ] Remove students from the `HONR464-F26` group once grades are final.
- [ ] Retire or archive the 13 custom models and the knowledge collections, or keep
  them as the seed for the next offering (re-stamp and refresh before reuse).
- [ ] Remind students to delete their personal `GENAI_API_KEY` Colab Secret and, if
  they wish, revoke the key under **Settings → Account**.

---

## The open item, restated

Before day one, **you** confirm: (1) all five students can sign in and open a role
from the group, and (2) whether student API keys work. Item (1) is required and
gates nothing else — it is the whole course. Item (2) is a bonus; if it fails, the
course runs UI-only with no change to any milestone. Record the outcome so the
notebooks' touchpoint instructions can point students to the path that actually
works for your cohort.
