# AI Agent Role Cards

*One card per AI research role the course uses. Give a role a narrow job and it
gives you a sharper, more checkable answer than a general "help me" ever will.
Each card is a pocket reference: purpose, when to consult, what to feed it, what
it hands back, its blind spots, and the line where it must hand the decision back
to you. Full system prompts live in `genai_studio/roles/`, not here.*

---

## How to read a card

Two homes for these roles. **GenAI Studio custom models** are the course's
purpose-built reviewer bench, wired to the course knowledge base and used at
graded milestone touchpoints. **Gemini prompted roles** you create yourself in
Colab by pasting the role's briefing at the top of a chat. The card tags which is
which. Every card ends with an **escalation line** because every role informs a
decision that stays yours (see the
[human responsibility checklist](human_responsibility_checklist.md)).

Whichever role you consult, the same discipline applies: verify what it returns
and log it in your [AI Research Ledger](ai_research_ledger_template.md).

---

## Framing and question roles (Gemini prompted)

### Socratic Research Tutor
- **Purpose:** helps you think, by asking rather than answering. Turns your half-formed idea into a sharper question through guided questioning.
- **When to consult:** early, when your curiosity is still vague and you want to develop it yourself, not be handed a topic.
- **Give it:** your rough interest, your field, and an instruction to ask, not tell ("Do not give me a question; ask me questions until I find one").
- **Returns:** a chain of questions that narrows your thinking; occasional reflections back to you.
- **Blind spots:** can lead you toward whatever it finds interesting; may sound wise while adding nothing. Sycophancy if you seek approval.
- **Escalation line:** this role must hand back to you when a research problem or question is actually chosen. Selecting the question is yours alone.

### Evidence & Citation Verifier
- **Purpose:** pressure-tests whether a source, statistic, or citation is real and says what you think it says.
- **When to consult:** whenever you are about to cite something, and before any source enters your evidence map (M2).
- **Give it:** the exact citation or claim, and the instruction to flag anything it is not confident exists.
- **Returns:** a confidence flag per item and what you would search to confirm it independently.
- **Blind spots:** it can confidently fabricate the very thing you asked it to verify. Its "yes, this is real" is a lead, not proof.
- **Escalation line:** this role must hand back to you when a citation is accepted. You confirm existence by opening the actual source; the role never substitutes for that read.

### Research-Question Diagnostician
- **Purpose:** classifies your question on the inquiry compass (kind and reach) and checks the wording matches the classification.
- **When to consult:** at M3 (the inquiry declaration) and any time you revise the question.
- **Give it:** your exact question wording and the compass definitions.
- **Returns:** a proposed kind and reach, the words in your question that fix them, and the nearest wrong classification with why it is wrong.
- **Blind spots:** may accept a silent scope change (reading a causal question as descriptive, or the reverse) if your wording is loose.
- **Escalation line:** this role must hand back to you when the design and target population are declared. The declaration is yours to defend.

---

## Design roles (RDSS library pathways)

### MIDA Design Reviewer *(Gemini prompted)*
- **Purpose:** checks that your Model, Inquiry, Data strategy, and Answer strategy fit together and actually answer your question.
- **When to consult:** at M3 and whenever a design element changes.
- **Give it:** your four MIDA components and your question.
- **Returns:** where the four pieces are misaligned; whether the answer strategy targets the inquiry.
- **Blind spots:** can bless a tidy-looking design that cannot identify what it claims. Format neatness is not soundness.
- **Escalation line:** this role must hand back to you when the design is declared. You own the design and its defense.

### Observational Descriptive Auditor *(Gemini prompted)*
- **Purpose:** for observational descriptive work (Week 5), audits sampling frame, measurement, and whether a descriptive claim stays descriptive.
- **When to consult:** M4, when building an observational descriptive design.
- **Give it:** your sampling frame, your measures, and your intended claim.
- **Returns:** coverage gaps, measurement worries, and any place the claim drifts toward cause or over-reaches its frame.
- **Blind spots:** may miss frame gaps you did not describe; only sees what you tell it about the data.
- **Escalation line:** this role must hand back to you when you judge data quality and set the claim boundary.

### Causal Identification Skeptic *(GenAI Studio custom model — M5 touchpoint)*
- **Purpose:** the hostile causal reviewer. Attacks every reason your claimed effect might not be identified.
- **When to consult:** M5, the required touchpoint for observational causal work, and any time you use a causal verb.
- **Give it:** your identification argument, your design, and the effect you claim.
- **Returns:** ranked threats to identification (confounding, selection, open backdoor paths) and what each would take to rule out.
- **Blind spots:** can generate plausible-but-wrong threats, or miss one specific to your setting. A threat is a lead to check, not a verdict.
- **Escalation line:** this role must hand back to you when you decide which claims the evidence justifies, and whether a causal claim survives.

### Experimental Design Reviewer *(Gemini prompted)*
- **Purpose:** reviews experimental designs (descriptive or causal) for assignment, blocking, and whether the design supports the intended answer objective.
- **When to consult:** Weeks 7 and 9, when building an experimental design.
- **Give it:** your assignment procedure, arms, and the inquiry the experiment serves.
- **Returns:** assignment weaknesses, power and balance concerns, and whether experimental assignment is being over-read as automatically causal.
- **Blind spots:** may assume an experiment implies a causal inquiry; hold the line that assignment does not force the kind.
- **Escalation line:** this role must hand back to you when the design and its claim boundary are declared.

### Prediction & Leakage Auditor *(GenAI Studio custom model — M7 touchpoint)*
- **Purpose:** for predictive work, hunts for leakage and dishonest evaluation, and checks the held-out and baseline are real.
- **When to consult:** M7, the required touchpoint for prediction, and any predictive claim.
- **Give it:** your data pipeline, your train/held-out split, your baseline, and your metric.
- **Returns:** places where information leaks from held-out into training, and whether your reported number is prediction-time honest.
- **Blind spots:** can miss a subtle leak it was not shown; sees only the pipeline you describe.
- **Escalation line:** this role must hand back to you when you decide what the held-out performance licenses you to claim about unseen cases.

---

## Analysis, robustness, and communication roles

### Robustness & Sensitivity Reviewer *(GenAI Studio custom model — M9 touchpoint)*
- **Purpose:** probes whether your result survives reasonable alternative choices, and where it is fragile.
- **When to consult:** M9, alongside the Poster Critic, and whenever you finalize a result.
- **Give it:** your headline result, the choices behind it (exclusions, specifications), and your data.
- **Returns:** which alternative specifications to run and which would most threaten your claim if the result flipped.
- **Blind spots:** can suggest probes that do not fit your design; correlated with your own assumptions if you framed the prompt narrowly.
- **Escalation line:** this role must hand back to you when you decide which claims survive and how to bound them.

### Poster Critic *(GenAI Studio custom model — M9 touchpoint)*
- **Purpose:** the 90-second stranger. Attacks the poster's headline, figure honesty, read path, and visible uncertainty.
- **When to consult:** M9 draft review and before the final lock (M10).
- **Give it:** your draft poster (or a faithful description) and its declared compass position.
- **Returns:** overclaims, dishonest figures, broken read paths, and missing bounds, named specifically.
- **Blind spots:** works from what you show it; a figure it cannot see, it cannot audit.
- **Escalation line:** this role must hand back to you when you set the final headline claim and its boundary.

### Reproducibility Auditor *(GenAI Studio custom model — M13 touchpoint)*
- **Purpose:** checks whether your package (or a peer's) can be rebuilt by a stranger, and traces numbers from data to claim.
- **When to consult:** M13 replication and red-team, and when assembling your capsule (M14).
- **Give it:** the package contents, run order, and the headline number to trace.
- **Returns:** the five package sins if present (hard-coded paths, missing seeds, by-hand edits, undocumented exclusions, stale data) and broken lineage links.
- **Blind spots:** cannot actually run the notebook; a clean-run claim still needs a real restart-and-run-all by a human.
- **Escalation line:** this role must hand back to you when you sign an attestation. Only a human clean run justifies "it reproduces."

### Research-Note Reviewer *(Gemini prompted)*
- **Purpose:** reviews your research note and brief for claims that outrun their ledger and caveats dropped under polish.
- **When to consult:** M14, when drafting the note and brief.
- **Give it:** your draft and your claim ledger.
- **Returns:** sentences that upgrade a claim past its evidence, and places uncertainty fell out of the prose.
- **Blind spots:** may smooth your writing into a stronger claim than the evidence supports; watch for the very upgrade you asked it to catch.
- **Escalation line:** this role must hand back to you when you decide the final wording of a claim and its stated uncertainty.

### AI Research Team Orchestrator *(Gemini prompted)*
- **Purpose:** helps you plan how to split a task across several roles, in what order, and how to reconcile their outputs. Used in Week 16.
- **When to consult:** M15, when running multiple roles on one task.
- **Give it:** the task, the roles available, and your dependency questions.
- **Returns:** a proposed decomposition, an order (parallel vs sequential), and a plan for logging conflicts.
- **Blind spots:** can manufacture false consensus by having roles echo one framing; it does not resolve disagreements, you do.
- **Escalation line:** this role must hand back to you at every consequential decision. Orchestration organizes the work; the human override decides it. See the [multi-agent worksheet](multi_agent_worksheet.md).

---

*Note on availability: GenAI Studio runs prompted roles, custom models,
retrieval assistants, and sequential workflows, but no autonomous agents and no
native orchestration. The Orchestrator role is a planning aid you drive by hand,
not a system that runs the other roles for you. See `course_config.yaml
genai_studio:` and `genai_studio/roles/` for the full specifications.*
