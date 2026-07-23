# Prompt Design Guide

*How to brief an AI research partner so it gives you an answer worth checking.
The skill here is not a magic sentence. It is a **sequence**: brief, decompose,
follow up, interrogate. A better prompt earns a better draft, and a better draft
is still an unverified draft you must run through the
[verification guide](verification_guide.md) and log in your
[AI Research Ledger](ai_research_ledger_template.md).*

---

## The one idea

People hunt for the perfect prompt the way they hunt for a lucky charm. There
isn't one. Good AI research work comes from **briefing well, then arguing well**.
You set the job up carefully, read what comes back like a skeptical reviewer, and
push until the answer is either trustworthy or clearly not. This guide gives you
the moves for each step.

**The reminder that governs everything below:** a sharper prompt makes the output
*more useful to check*, not *safe to trust*. You still verify.

## Part 1 — The seven-part briefing

Weak prompts leave the AI to guess. A briefing tells it who to be, what to do,
what it is working with, what rules to obey, what evidence to bring, how to lay
the answer out, and how you will check it. Give it all seven and the guessing
drops.

| Part | What you supply | Example phrasing |
|---|---|---|
| **Role** | The expert lens you want | "Act as a skeptical peer reviewer in \[field]." |
| **Task** | The single job | "Assess whether my research question is answerable as written." |
| **Context** | Your project, level, constraints | "This is an honors project; I have no coding background and one dataset." |
| **Constraints** | The rules of the answer | "Only cite work you are confident exists. If unsure, say so." |
| **Evidence** | What backing you require | "For each claim, name the reasoning or the source it rests on." |
| **Format** | The shape of the reply | "Return a table: issue, why it matters, suggested fix." |
| **Verification** | How you plan to check | "Flag which of your claims I most need to verify independently." |

You will not use all seven every time. For a quick code snippet, Role and Task
may be enough. For anything that will touch a claim you defend, use all seven.

## Part 2 — The interrogation moves

Once a draft is back, you switch from briefer to interrogator. These are the
follow-ups that separate a real answer from a confident-sounding one. Keep them
where you can reach them; they are the heart of the skill.

- **Decompose.** "Break this into the smallest steps and show each." A big answer
  hides its weak step; a decomposed one exposes it.
- **Surface assumptions.** "What are you assuming that, if wrong, breaks this
  answer?" Fabrication and scope-slips usually live in an unstated assumption.
- **Demand competing explanations.** "Give two other explanations that fit the
  same evidence, and how I would tell them apart." Guards against the first
  plausible story.
- **Ask for a counterexample.** "Describe a case where this advice would be
  wrong." If it can't find one, be more suspicious, not less.
- **Require evidence and a test.** "What observation would prove this claim
  false?" A claim with no falsifier is not yet knowledge.
- **Force uncertainty.** "Rate your confidence in each point and say what drives
  the low ones." Missing uncertainty is a named failure mode; make it show.
- **Request structured output.** A table or numbered list is easier to audit than
  a paragraph, because each cell is a claim you can check on its own.
- **Ask for a code check.** "Explain what this code does line by line, then give
  me an independent way to confirm its result." You verify the result, not the
  explanation.
- **Ask it to critique itself.** "Now argue against your own answer as a hostile
  reviewer would." Sycophantic agreement dissolves under a role change.

## Part 3 — A worked sequence (literature scoping)

Watch a real task move from a vague ask to something you can actually verify. The
task: find out whether the gap you want to study is a real, open gap.

**Step 1 — the vague prompt (what not to do).**

> "Is there research on social media and student stress?"

You get a confident paragraph, maybe a few study names, no venues, no way to know
what is real. This is where fabricated citations enter a project.

**Step 2 — the briefed prompt.**

> "Act as a literature-review assistant in education research (Role, Context).
> List peer-reviewed studies from the last ten years measuring a link between
> social-media use and academic stress in undergraduates (Task). For each, give
> title, authors, year, venue, and one-line finding, in a table (Format). Only
> include work you are confident exists; mark anything uncertain (Constraints).
> For each row, note the study's design so I can judge what it can claim
> (Evidence). At the end, flag the two rows I should verify first (Verification)."

Now the output is a checkable table, not a paragraph.

**Step 3 — the follow-up.**

> "For the three strongest rows, what does each one NOT settle, and where is the
> open gap a new study could fill?"

This turns a reading list into a gap map, which is what the milestone needs.

**Step 4 — the interrogation.**

> "Which of these titles are you least certain are real? What would I search to
> confirm each one exists, and what would tell me you invented it?"

**Step 5 — you verify (this is the point).** You open the library database,
search each kept title, and open the actual paper. Rows you cannot find are cut.
Only then does a row earn a place in your evidence map. You log the whole
sequence as one ledger entry: tool, the briefed prompt, what came back, your
decision (kept four, cut two), and the verification method (primary-source read).

**The lesson:** the briefing and the follow-ups got you a far better draft. The
verification is what made it evidence. Skipping step 5 would have imported
whatever the model guessed straight into your project.

## Anti-patterns to drop

- **The one-shot wish.** Expecting a perfect answer from one line. Real work is a
  sequence.
- **Copy-paste trust.** Pasting an output into your notebook without a decision
  and a check. That is exactly what the ledger's Decision and Verification columns
  exist to stop.
- **Leading the witness.** "Confirm that my hypothesis is right." You will get
  agreement, not evidence. Ask it to try to break your claim instead.
- **Verifying the explanation, not the result.** A fluent explanation of code or
  math can accompany a wrong result. Check the number, not the paragraph about
  the number.

---

*Next: run the output through [verification_guide.md](verification_guide.md),
watch for the failures in [ai_error_taxonomy.md](ai_error_taxonomy.md), and record
the sequence in your [AI Research Ledger](ai_research_ledger_template.md).*
