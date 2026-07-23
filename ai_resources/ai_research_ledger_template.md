# AI Research Ledger

*Your inspectable record of what you asked AI to do and how you checked it.
Copy the entry table into every notebook session and every milestone. This is
the artifact behind the course's one rule: **AI is your arm and your research
assistant, not your brain.** AI may propose. You must verify. The evidence must
support.*

---

## What the ledger is for

The ledger is not paperwork you add at the end. It is the running proof that you
stayed in charge. Every time AI did a piece of work for you, one row records the
task, the exact prompt, what came back, what **you** decided, and how you
confirmed the output was true before you trusted it.

**Why this matters:** a reviewer, a teammate, or you three weeks from now cannot
tell a verified answer from a lucky-sounding guess by looking at the answer.
They can only tell by looking at how it was checked. The ledger is where that
check lives. A finding with no ledger row is, for grading purposes, an unverified
claim.

The everyday shorthand is **Ask → Verify → Document**. The full loop the course
trains is **SDIIVDD**: Specify, Delegate, Interrogate, Inspect, Verify, Document,
Defend. The ledger is the written trace of the last three.

## The entry table (eight fields)

Every AI-assisted action gets one row. The eight fields are fixed so the same
information appears every time and a grader can scan it fast.

| # | Field | What goes here |
|---|---|---|
| 1 | **Task delegated** | The one job you handed to AI, in a sentence. One task per row. |
| 2 | **Tool used** | Which tool and role (for example, *Gemini in Colab*, *GenAI Studio — Causal Identification Skeptic*, *Microsoft Copilot*). |
| 3 | **Prompt** | The actual prompt you sent, or a tight paraphrase if it was long. A reader should be able to rerun it. |
| 4 | **Output summary** | What came back, in your words. Not a paste of the whole reply; the claim or artifact it produced. |
| 5 | **Decision** | What **you** did with it: accepted, edited, rejected, asked again. This column is where your judgment shows. |
| 6 | **Verification method** | How you confirmed the output was true, named from the verification menu (recompute, primary-source read, alternative code, counterexample, and so on). |
| 7 | **Remaining concern** | What you are still unsure about, or "none, and here is why." An honest concern scores better than a blank. |
| 8 | **Responsible researcher** | Your name. On an individual project this is always you; the field keeps the habit for any shared work. |

Copy this empty row to start:

```
| Task delegated | Tool used | Prompt | Output summary | Decision | Verification method | Remaining concern | Responsible researcher |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |
```

## Worked entries

Three real-shaped rows, one for each kind of task you will hand to AI. Notice
that in every row the **Decision** and **Verification method** columns carry the
weight. The output is never trusted on its own.

**A code task.**

| Task delegated | Tool used | Prompt | Output summary | Decision | Verification method | Remaining concern | Responsible researcher |
|---|---|---|---|---|---|---|---|
| Write pandas code to compute the mean outcome by treatment group | Gemini in Colab | "Given a dataframe `df` with columns `group` and `outcome`, write pandas to report the mean `outcome` for each `group`, and show the difference." | A `groupby("group")["outcome"].mean()` snippet plus a difference line | Accepted the groupby, rewrote the difference line to subtract in the direction my question asks | **Alternative code**: recomputed the same two means by hand-filtering each group and subtracting; matched to the fourth decimal | The group sizes are uneven; the raw difference ignores that, which I flag in my claim | You |

**A literature task.**

| Task delegated | Tool used | Prompt | Output summary | Decision | Verification method | Remaining concern | Responsible researcher |
|---|---|---|---|---|---|---|---|
| Find peer-reviewed work on my outcome measure to see if my gap is real | Gemini | "List peer-reviewed studies from the last ten years that measure \[my outcome] in \[my setting]. For each, give title, authors, year, venue, and a one-line finding." | Six studies with titles, authors, venues, and findings | Rejected two rows I could not locate; kept four after finding them myself | **Primary-source read**: searched each title in the library database, opened the actual paper, confirmed authors and finding match | One kept paper is a preprint, not yet peer-reviewed; I mark it as such | You |

**A critique task.**

| Task delegated | Tool used | Prompt | Output summary | Decision | Verification method | Remaining concern | Responsible researcher |
|---|---|---|---|---|---|---|---|
| Stress-test my claim that the sample difference generalizes to the population | GenAI Studio — Causal Identification Skeptic | "My question is descriptive with population reach. Here is my sampling frame and my claim. Name every reason this difference might not hold beyond my sample, ranked by how much it worries you." | Five threats, led by coverage gaps in my sampling frame | Accepted three, edited one into my limitations section, set one aside as not applicable to my frame | **Peer reasoning**: walked the top threat past a classmate, who agreed the frame misses a subgroup I had not named | I cannot fully bound the coverage gap without frame documentation I do not have yet | You |

**The pattern to copy:** the output is a proposal. The decision is yours. The
verification is named, not vague. The remaining concern is honest.

## The rules

1. **Every notebook session and every milestone appends.** A session where you
   used AI and left the ledger empty is incomplete, the same as a missing answer.
2. **One task per row.** If a prompt did two jobs, it gets two rows so each can
   be verified on its own.
3. **The verification column is never blank and never "looks right."** Name a
   method from the [verification guide](verification_guide.md). "It seemed
   correct" is not a verification.
4. **A missing ledger entry scores the rubric's Craft criterion 0 and returns
   the submission.** This is the hard cap; it mirrors the untraceable-number cap
   on the poster.
5. **The ledger is a primary source for two later deliverables.** Your M13
   red-team of a peer reads *their* ledger to find where verification was thin.
   Your M15 AI-management portfolio is built from *your* full-semester ledger.
   Keep it honest now so it serves you then.
6. **Disclose, do not hide.** Undisclosed AI use is an academic-integrity
   violation. A frankly logged weak spot is graded on its honesty; a hidden one
   is graded as misconduct.

## How this differs from the claim ledger

The course has two ledgers, and they answer different questions. Do not merge
them.

| | **AI Research Ledger** (this file) | **Claim ledger** (M8 onward) |
|---|---|---|
| Answers | What did AI do, and how did I check it? | What does my research assert, and what backs each claim? |
| One row is | One delegated task | One claim my project makes |
| Columns | task · tool · prompt · output · decision · verification · concern · you | claim · evidence · verification · boundary · sensitivity survival |
| Grows during | every session and milestone | the analysis and writing phases |
| Feeds | M13 peer red-team, M15 AI portfolio | the poster, the brief, the evidence defense |

A useful way to hold the difference: the **AI ledger** is about your *process*
(who did the work and how you policed it). The **claim ledger** is about your
*product* (what you are willing to say and why). A single finding can touch both,
but a row in one is never a substitute for a row in the other.

---

*See also: [prompt_design_guide.md](prompt_design_guide.md) (how to get a better
output worth verifying) · [verification_guide.md](verification_guide.md) (how to
fill column 6) · [ai_error_taxonomy.md](ai_error_taxonomy.md) (what column 7
should be watching for) · [escalation_protocol.md](escalation_protocol.md) (when
a row must stop and come back to you).*
