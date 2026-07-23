# GenAI Studio — the course reviewer bench

*Workstream overview for HONR 46400, Evidence-Driven Research (Purdue Honors,
Fall 2026). This directory holds everything the course needs to run **Purdue
GenAI Studio** as a bench of AI reviewer roles that critique student research
and never do it for them.*

The course's one rule governs every file here: **AI is your arm and your
research assistant, not your brain.** The full loop is **SDIIVDD** (Specify,
Delegate, Interrogate, Inspect, Verify, Document, Defend); the everyday
shorthand is **Ask → Verify → Document**. GenAI Studio sits inside that loop as
a source of *proposals and critiques you must verify*, never a source of
answers you may trust.

---

## What Purdue GenAI Studio is

Purdue GenAI Studio is Purdue's self-hosted generative-AI platform, run by RCAC
(the Rosen Center for Advanced Computing). These capabilities are **verified
against the official RCAC knowledge base (rcac.purdue.edu/knowledge/genaistudio)
as of 2026-07-22**. The course treats them as ground truth and claims nothing
beyond them.

- **Access.** Web app at `https://genai.rcac.purdue.edu`, signed in with your
  Purdue account (Purdue SSO / CILogon).
- **Open-source models.** The catalog is open-source models (the LLaMA family,
  with others added by RCAC on request). There is no GPT-4-class or Gemini model
  inside GenAI Studio.
- **Custom models.** You can save a *custom model* = a base model + a system
  prompt + attached *Knowledge* (uploaded documents). The 13 course reviewer
  roles are exactly this: one saved custom model each.
- **RAG knowledge bases.** You can upload documents into a *Knowledge* collection
  (a retrieval-augmented backend) and attach it to a custom model, so the model
  answers grounded in those documents. Collections are shareable across a
  **group**.
- **Groups.** A group shares custom models and knowledge bases with a set of
  Purdue users. The course runs one group for its five students.
- **Multi-model comparison.** One chat can send the same prompt to two or more
  models at once and show the answers side by side. This powers the
  model-disagreement laboratory (see `multi_model_comparison_lesson.md`).
- **OpenAI-compatible API.** A REST endpoint at
  `https://genai.rcac.purdue.edu/api/chat/completions` accepts OpenAI-style
  chat payloads. You generate a personal key under **Settings → Account**. This
  powers the optional Colab proof-of-concept (see `colab_api_poc.md`).

**Not available, and never implied anywhere in this course.** GenAI Studio has
**no autonomous agents** (a model that plans and acts on its own across steps),
**no native orchestration** (built-in multi-agent coordination), and no
documented tools/pipelines, rate limits, or explicit student-eligibility terms.
Any file that could be read as promising these is a defect. Overselling the
platform is treated as an integrity error, the same as overclaiming a research
result.

---

## The six-level capability taxonomy (and where GenAI Studio stops)

The course teaches AI collaboration on an honest six-level scale so you always
know what you are and are not using. **GenAI Studio implements only levels 1–4.**

| Level | Name | What it is | In GenAI Studio? |
|---|---|---|---|
| 1 | Prompted role | You paste a role instruction into a plain chat with a base model. | ✓ Yes |
| 2 | Custom model with system prompt | A saved model that carries the role instruction for you. | ✓ Yes |
| 3 | RAG-supported assistant | A custom model with an attached course knowledge base. | ✓ Yes |
| 4 | Sequential multi-role workflow | You run several roles in a planned order, carrying each output to the next — by hand in the UI, or scripted through the API. **You** are the orchestrator. | ✓ Yes (you sequence it) |
| 5 | Autonomous agent | A model that plans and takes actions on its own, without a human in each step. | ✗ No — not in GenAI Studio |
| 6 | Multi-agent orchestration | Several autonomous agents coordinating a task. | ✗ No — not in GenAI Studio |

Levels 5 and 6 are taught **conceptually** in Week 16 (nb15, "Managing multiple
AI agents; the final defense") so you can name them, recognize their risks, and
explain why the course does not hand a research decision to either. The Week-16
"orchestrator" (`roles/ai_research_team_orchestrator.md`) is a **level-4
planning aid**, not a level-5 agent: it helps *you* decide which role to consult
next; it never calls the other roles itself.

---

## What the course uses it for

Three uses, all inside the Ask → Verify → Document loop.

1. **A reviewer bench of role models** (`roles/`). Thirteen saved custom models,
   each a single-minded critic: a citation verifier, a causal-identification
   skeptic, a leakage auditor, a poster critic, a reproducibility auditor, and
   so on. You bring an artifact; the role attacks one dimension of it and hands
   back a structured critique plus a list of things you must verify yourself.
   Primary Gemini use stays inside the Colab notebooks; GenAI Studio is the
   *second opinion* bench.
2. **The model-disagreement laboratory** (`multi_model_comparison_lesson.md`).
   Using multi-model comparison, you run the same prompt across two or more
   models and study where they disagree. Disagreement is a flag to investigate;
   **agreement is not proof**, because models trained on overlapping data share
   correlated errors and can be confidently wrong together.
3. **The Week-16 sequential multi-role workflow** (nb15). You plan and run a
   short chain of roles by hand or through the API, keeping a human decision and
   a ledger row at every hand-off. This is the level-4 capstone: you experience
   orchestrating AI reviewers while staying the orchestrator.

---

## The four required milestone touchpoints

Most role use is optional support. At four milestones, consulting a specific
role is **required**, and a named output section goes into your **AI Research
Ledger** (`ai_resources/ai_research_ledger_template.md`). Milestone definitions
are the v2 chain in `planning/PROJECT_MILESTONES.md` and
`course_config.yaml milestones:`.

| Milestone | Due | Required role(s) | What you submit to the role |
|---|---|---|---|
| **M5** — Causal identification strategy or causal-language boundary | Fri Oct 2 (async) | Causal Identification Skeptic | Your identification argument, or your defense that your language stays descriptive |
| **M7** — Declared analysis protocol | Fri Oct 16 | Prediction & Leakage Auditor | Your declared analysis protocol, focusing on any out-of-sample / prediction claim |
| **M9** — Poster draft 1 and research audit | Fri Oct 30 | Poster Critic **and** Robustness & Sensitivity Reviewer | Your poster draft, and your claim-and-evidence table with robustness checks |
| **M13** — Replication and red-team report | Sun Nov 29 (async) | Reproducibility Auditor | The peer reproducibility package you are replicating |

Each of these five role files carries a **"Milestone scope"** statement naming
the artifact submitted and the ledger section the output feeds. Requiring the
touchpoint does **not** mean accepting the output. You still verify, decide, and
own every conclusion.

---

## The 13 reviewer roles

Each file in `roles/` is a complete specification: Purpose, Scope, the full
copy-paste System Prompt, Knowledge Sources, Expected Input, Output Schema,
Verification Requirements, Limitations & Failure Modes, Escalation Conditions,
Student Use, and Instructor Use.

| Role file | Reviews | Course home |
|---|---|---|
| `roles/socratic_research_tutor.md` | Your thinking, by questioning — never by answering | All weeks; SRL prep |
| `roles/evidence_citation_verifier.md` | Whether a citation is specific enough to be checkable (you still retrieve it) | Week 3 · M2 |
| `roles/research_question_diagnostician.md` | Question classification on the compass (kind × reach) and scope | Week 2 · M1 |
| `roles/mida_design_reviewer.md` | Your MIDA declaration (Model, Inquiry, Data, Answer) and diagnosis plan | Week 4 · M3 |
| `roles/observational_descriptive_auditor.md` | Sampling frame, coverage, index construction, generalization boundary | Week 5 · M4 |
| `roles/causal_identification_skeptic.md` | Identification assumptions and causal-language boundary **(M5 touchpoint)** | Week 6 · M5 |
| `roles/experimental_design_reviewer.md` | Assignment, blocking, randomization checks, experiment ethics | Weeks 7 & 9 · M6/M8 |
| `roles/prediction_leakage_auditor.md` | Leakage, baseline, held-out honesty, metric choice **(M7 touchpoint)** | Week 8 · M7 |
| `roles/robustness_sensitivity_reviewer.md` | Specification robustness and sensitivity of a claim **(M9 touchpoint)** | Week 10 · M9 |
| `roles/poster_critic.md` | Claim boundary, untraceable numbers, uncertainty, data-ink **(M9 touchpoint)** | Week 11 · M9/M10 |
| `roles/reproducibility_auditor.md` | Whether a package reproduces from scratch **(M13 touchpoint)** | Weeks 14–15 · M13/M14 |
| `roles/research_note_reviewer.md` | Research-note structure, uncertainty/limitations, claim traceability | Week 15 · M14 |
| `roles/ai_research_team_orchestrator.md` | Which roles to consult next — a level-4 planning aid, not an agent | Week 16 · M15 |

---

## The knowledge base

The roles are grounded in course-authored knowledge collections, described in
`knowledge_base_strategy.md`: course-policies, milestone-briefs, rubrics,
research-design-definitions, poster-requirements, reproducibility-standards, and
examples-and-counterexamples. **Only course-authored material goes in.** Never
upload RDSS chapters or any copyrighted third-party text, and never upload
student data or drafts containing personal information.

---

## Two paths, equal standing

Everything works two ways, and neither is second-class:

- **Manual UI path (the guaranteed path).** Workspace → open the course group's
  role model → paste your artifact → copy the structured output. This needs
  nothing but a browser and a Purdue login. Every milestone touchpoint is
  designed to work UI-only.
- **API / Colab path (an enhancement).** The OpenAI-compatible endpoint lets you
  call roles from a Colab notebook and script the Week-16 workflow. It depends on
  each student having a working API key, which is the open item below. If the API
  is unavailable, the course loses nothing essential — the UI path covers every
  requirement.

---

## Open item (instructor, before the semester)

**The instructor must verify student access and API-key availability before the
term starts.** GenAI Studio's explicit student-eligibility terms and rate limits
are not documented publicly, so student accounts, group membership, and personal
API keys are confirmed by hand during setup (see `instructor_setup_guide.md`).
Until confirmed, treat the **manual UI workflow as the guaranteed path and the
API as an enhancement**. If student API access does not materialize, the course
runs UI-only with no change to any milestone.

---

## Files in this directory

- `README.md` — this overview.
- `roles/` — the 13 reviewer role specifications.
- `knowledge_base_strategy.md` — what goes in each knowledge collection, sharing,
  and refresh cadence.
- `colab_api_poc.md` — the secure Colab proof-of-concept, cell by cell, with the
  manual-UI fallback as an equal path.
- `instructor_setup_guide.md` — pre-semester checklist, term-time maintenance,
  no-API contingency, and teardown.
- `multi_model_comparison_lesson.md` — the model-disagreement laboratory
  protocol for Weeks 10 and 16.

---

*See also: `_project_docs/DECISIONS.md` D19 (the AI-stack ruling),
`planning/SOURCE_AUDIT_V2.md` §8 (the verified capability audit),
`course_config.yaml` (`ai_policy`, `genai_studio`), and
`ai_resources/ai_research_ledger_template.md` (the ledger every touchpoint
feeds).*
