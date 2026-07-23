# Verification Guide

*The menu of ways to confirm an AI output is true, with a note on when to reach
for each. Verification is the graded habit at the center of the course. Whatever
method you use, **name it in column 6 of your
[AI Research Ledger](ai_research_ledger_template.md)** — "it looked right" is not
a verification.*

---

## Why a menu, not a rule

Different outputs fail in different ways, so they need different checks. A number
is verified by recomputing it; a citation is verified by opening the paper; a
method choice is verified by finding the case where it breaks. Picking the right
check is part of the skill. This page is the menu you pick from, and the rule is
simple: **every AI-assisted result gets at least one named method before you
trust it, and the name goes in the ledger.**

## The verification menu

Each method below carries a one-line "reach for this when" and a short worked
example. Match the method to what could go wrong with the output.

**1. Direct calculation.** *Reach for this when the output is a number you could
get another way.* Recompute it by hand or with a second, simpler expression.
*Example:* AI reports a group mean of 4.2; you sum the ten values and divide,
getting 4.2. Confirmed.

**2. Simulation.** *Reach for this when a claim is about how a procedure behaves,
not a fixed number.* Generate data where you know the answer and see if the method
recovers it. *Example:* unsure a formula estimates a difference correctly, you
simulate two groups with a known gap of 3 and check the code returns about 3.

**3. Documentation lookup.** *Reach for this when the output uses a function,
argument, or default you did not choose yourself.* Open the official docs.
*Example:* AI calls a function with `ddof=0`; you read the docs to confirm that is
the default you want, not a silent choice that changes your result.

**4. Primary-source reading.** *Reach for this when the output cites a study, a
statistic, or a fact from the literature.* Find the actual source and read the
relevant line. *Example:* AI attributes a finding to a 2019 paper; you locate the
paper, open it, and confirm the finding and the year before citing it.

**5. Alternative code.** *Reach for this when a code result would change your
claim.* Recompute the same quantity a different way and compare. *Example:* a
`groupby` gives a difference of 0.8; you filter each group manually and subtract,
getting 0.8. Two roads, one answer.

**6. Benchmark result.** *Reach for this when you have a known-good reference
value.* Compare the output against a published or previously verified number.
*Example:* your replication of a textbook example should match the textbook's
reported estimate within rounding; if it doesn't, something in your pipeline is
off.

**7. Counterexample.** *Reach for this when the output states a general rule or a
method recommendation.* Try to find one case where it fails. *Example:* AI says
"always drop missing rows"; you construct a case where the missing rows are the
signal, showing the rule is not universal.

**8. Causal diagram.** *Reach for this when the output makes or implies a causal
claim.* Draw the diagram of what causes what and check whether the claimed effect
is actually identified. *Example:* AI reads a correlation as an effect; your
diagram shows an open backdoor path (a common cause), so the effect is not
identified and the claim must be softened.

**9. Holdout sample.** *Reach for this when the output is a prediction or a fitted
model.* Check performance on data the model never saw. *Example:* a model looks
accurate on the data it was fit to; you evaluate it on a held-out slice, and the
honest number is lower. The held-out number is the one you report.

**10. Falsification test.** *Reach for this when a claim should have an
observable consequence.* State what you would see if the claim were false, then
look. *Example:* if your treatment truly had no effect, a placebo outcome that it
cannot affect should show nothing; you check, and it does show nothing, which
supports your setup.

**11. Peer reasoning.** *Reach for this when the output rests on judgment a second
human can pressure-test.* Walk it past a classmate or the instructor and see if
the reasoning survives. *Example:* you explain your identification argument to a
partner; their one question exposes an assumption you had not defended, which goes
into your limitations.

## Choosing fast

A quick way to pick:

- Output is a **number** → direct calculation or alternative code.
- Output is a **citation or fact** → primary-source reading.
- Output is a **method or general rule** → counterexample, or simulation.
- Output is a **causal claim** → causal diagram, falsification test.
- Output is a **prediction** → holdout sample.
- Output is a **judgment call** → peer reasoning.

When a result matters a lot, use two methods from different rows. Two independent
checks that agree are much stronger than one, and they guard against the
[correlated-error](ai_error_taxonomy.md) trap where one flawed idea passes its own
flawed check.

## The rule, restated

1. Every AI-assisted result gets **at least one** named method before you trust
   it.
2. High-stakes results (anything that reaches your poster, brief, or defense) get
   **two independent** methods.
3. The method's **name goes in the ledger**, column 6. A blank or a vague word
   there is treated as no verification, which caps the Craft criterion.
4. If you **cannot** verify an output, that is itself a finding: you do not use
   it, and you escalate per the
   [escalation protocol](escalation_protocol.md).

---

*See also: [prompt_design_guide.md](prompt_design_guide.md) (getting an output
worth checking) · [ai_error_taxonomy.md](ai_error_taxonomy.md) (what each method
is defending against) · [ai_research_ledger_template.md](ai_research_ledger_template.md)
(where the method is recorded).*
