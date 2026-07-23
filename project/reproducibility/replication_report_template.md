# Replication and Red-Team Report Template — M13

*The report you write after trying to rebuild a peer's findings from their package
alone. You receive an anonymized package, run it cold, trace its numbers, probe
its choices, and report honestly what you could and could not verify. Graded with
[redteam_audit_rubric.md](redteam_audit_rubric.md). Due the Sunday of the async
module week.*

---

## What this milestone is

You are handed a classmate's reproducibility package with the identifying headers
stripped. Your job is not to be kind and not to be cruel; it is to be a competent,
honest stranger. You attempt their headline number from the package alone, trace
every reported number back to the code and data that produced it, probe whether
the result survives reasonable alternative choices, and write down exactly what
held up and what did not.

The discipline that governs your own work governs this report too:
**Ask → Verify → Document.** Every check you run gets named, and your AI use in
the audit goes in your ledger. A finding you cannot verify is reported as
unverified, never dressed up as confirmed.

## The report template (fill every section)

```markdown
# Replication & Red-Team Report — [package code, anonymized]
Reviewer: [you] · Date: [___]

## 1. What I received
[List the package contents you were given: notebook, data or loader, README,
data dictionary, environment note, ledgers. Note anything missing.]

## 2. What ran / what failed
[The clean-run result. Did restart-and-run-all pass? Where did it break, if it
did? Be specific: the cell, the error, the likely cause.]
- Restart-and-run-all: [ ] passed  [ ] failed at [cell/step]
- Headline number claimed: [___]
- Headline number I obtained from the package alone: [___]
- Match: [ ] yes, within stated tolerance  [ ] no  [ ] could not reach it

## 3. Lineage check (data → code → figure → poster claim)
[Trace the headline claim backwards. Does the poster/README claim rest on a figure?
Does the figure come from a cell? Does the cell read the documented data? Note
every link that is solid and every link that breaks.]
| Link | Solid? | Note |
|---|---|---|
| claim → figure | | |
| figure → cell | | |
| cell → data | | |

## 4. Alternative-specification probes
[Reasonable choices the author could have made differently. Re-run with one or two
and report whether the result holds or moves. Name each probe and its outcome.]
| Probe (the choice I varied) | Result held / moved | What it means |
|---|---|---|

## 5. Hidden assumptions found
[Assumptions the package relies on but does not state: an unmodeled confounder
treated as absent, a sample read as a population, a leak into a held-out set. One
line each.]

## 6. Poster-vs-evidence agreement verdict
[Does the headline claim, as stated to the public, match what the package actually
supports? One of: agrees / overclaims / underclaims, with the specific gap.]

## 7. AI-related weaknesses
[Where the author's ledger shows thin verification, an unchecked AI output, or a
claim that traces to an AI result never independently confirmed. Read their ledger
as a primary source.]

## 8. Prioritized recommendations (top 3)
1. [the single most important fix]
2. [___]
3. [___]

## 9. What I could NOT verify
[Honest and specific. The numbers, claims, or steps you were unable to check, and
why — missing data, a step you could not run, a claim with no traceable evidence.
This section is graded on its honesty, not penalized for its length.]
```

## How to run the audit

1. **Reproduce cold first.** Before reading their reasoning, try to get the
   headline number from the package alone. Your confusion is data; log where it
   breaks.
2. **Trace, do not trust.** For the headline claim, walk backwards: claim → figure
   → cell → data. A claim that cannot be traced to a cell fails the
   evidence-integrity bar no matter how plausible it sounds.
3. **Probe, do not nitpick.** Vary one or two consequential choices, not every
   cosmetic one. The question is whether the *finding* survives, not whether you
   would have styled it differently.
4. **Read their ledger.** The AI Research Ledger is a primary source for section 7.
   Thin verification there is a real weakness to name, specifically and fairly.
5. **Report what you could not check.** Section 9 is not an admission of failure;
   it is the honesty the whole exercise rewards. A confident "reproduces" with no
   clean-run log behind it is the worst possible answer.

## The rule with teeth

You may only write "**reproduces**" in section 2 if you actually ran it and
obtained the number. A claim of reproduction with no clean-run log behind it caps
your reproduction-rigor score at Beginning (see
[redteam_audit_rubric.md](redteam_audit_rubric.md)). Reproduction is a thing you
*did*, not a thing you *assume*.

## Common failure modes

1. **Grading the topic, not the package.** Your job is whether the numbers rebuild
   and the claim matches the evidence, not whether you like the question.
2. **Vague hits.** "The analysis is unclear" is unusable. Name the cell, the
   number, the assumption.
3. **Claiming reproduction you did not perform.** The hard cap exists for exactly
   this. Run it or say you could not.
4. **Skipping the "could not verify" section.** Omitting it reads as false
   completeness; the honest gap is worth more than a padded verdict.

---

*Part of the reproducibility package. See also:
[clean_run_checklist.md](clean_run_checklist.md) (what the author should have done)
· [redteam_audit_rubric.md](redteam_audit_rubric.md) (how this report is graded) ·
[reproducibility_capsule_template.md](reproducibility_capsule_template.md).*
