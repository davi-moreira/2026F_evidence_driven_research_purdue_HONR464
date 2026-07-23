# Multi-Agent Worksheet

*The Week 16 (M15) worksheet for running several AI roles on one research task,
then deciding for yourself when they disagree. Managing a team of AI roles is a
skill: split the work, wire the dependencies, run it, and reconcile the outputs
with a human override. Fill one worksheet per task and attach it to your
AI-management portfolio.*

---

## The idea

One AI role gives you one lens. A research task usually needs several: a drafter,
a critic, a fact-checker, a skeptic. But more roles do not mean more truth. Three
roles that quietly share one wrong assumption will agree confidently and lead you
straight off a cliff. This worksheet trains the two hard parts: **decomposing a
task across roles** and **reconciling their outputs when they clash**, with you as
the decider, not a vote-counter.

The stopping rule at the end is the point. You are not done when the roles agree.
You are done when *you* can defend the decision.

## Step 1 — Decompose the task

Write the task in one sentence, then break it into subtasks small enough that one
role can own each.

```
TASK: ________________________________________________________

Subtask 1: ____________________________  Role: ______________
Subtask 2: ____________________________  Role: ______________
Subtask 3: ____________________________  Role: ______________
Subtask 4: ____________________________  Role: ______________
```

Pull roles from the [agent role cards](agent_role_cards.md). Give each subtask to
the role whose job it actually is; do not ask a drafter to also be its own critic.

## Step 2 — Declare dependencies

Some subtasks can run at the same time; others must wait for an input. Mark each.

```
Subtask 1  → runs: [ ] in parallel  [ ] after subtask ___
Subtask 2  → runs: [ ] in parallel  [ ] after subtask ___
Subtask 3  → runs: [ ] in parallel  [ ] after subtask ___
Subtask 4  → runs: [ ] in parallel  [ ] after subtask ___
```

**Parallel** is for independent lenses on the same input (a drafter and a
fact-checker can both read the same source). **Sequential** is for a chain (you
cannot critique a draft that does not exist yet). Getting this wrong wastes
effort and, worse, lets an early error flow downstream unchecked.

## Step 3 — Run and log conflicting outputs

Run the roles. When two disagree on anything that matters, log it before you
resolve it.

```
CONFLICT LOG
# | Roles in conflict | What each claimed | Consequential? (Y/N)
1 |                   |                   |
2 |                   |                   |
3 |                   |                   |
```

Only "consequential" conflicts (ones that would change a claim, a design, or a
number) need resolving now. Note the rest and move on.

## Step 4 — Diagnose each conflict

For every consequential conflict, decide which of three things you are looking at.
This diagnosis is the intellectual core of the worksheet.

- **Real disagreement.** The roles genuinely see the evidence differently. This is
  *useful*. It usually means the question is open, and the disagreement points you
  to what to verify.
- **Correlated error.** The roles *agree*, but on the same wrong assumption, so the
  agreement is worthless. Test: could they both be wrong the same way? If yes,
  their consensus proves nothing.
- **False consensus.** The roles agree only because your prompt framed the task so
  they had to. You led all the witnesses. Reframe neutrally and rerun.

```
Conflict 1 → [ ] real disagreement  [ ] correlated error  [ ] false consensus
Conflict 2 → [ ] real disagreement  [ ] correlated error  [ ] false consensus
Conflict 3 → [ ] real disagreement  [ ] correlated error  [ ] false consensus
```

The trap to fear most is agreement, not conflict. Conflict announces itself.
Correlated error and false consensus feel like confirmation. When roles agree on
something consequential, actively ask whether they are independent before you
trust it.

## Step 5 — Decide with human override

For each consequential conflict, *you* make the call, verify it with a non-AI
method, and record why.

```
DECISION RECORD
Conflict | My decision | Verification method (non-AI) | Why I overrode / accepted
1        |             |                              |
2        |             |                              |
3        |             |                              |
```

The override is the whole point. The roles inform; you decide. A decision that
just picked the majority of roles is not a decision, it is a vote, and votes among
correlated models are meaningless.

## Step 6 — Write the stopping rule

Before you started, you should know what "done" looks like. Write it now if you
have not.

> **I will stop when:** ______________________________________________

A good stopping rule is about *your* confidence, not the roles' agreement, for
example: "when I can defend each surviving claim to a hostile reviewer with a
verification I ran myself." A bad one is "when the roles all agree," because that
can happen while everyone is wrong.

## Worked mini-example — reviewing a chapter draft

**Task:** review a draft of your research-note chapter before submission.

- **Decompose:** (1) draft-quality review → Research-Note Reviewer; (2)
  claim-boundary check → Research-Question Diagnostician; (3) citation check →
  Evidence & Citation Verifier; (4) robustness of the headline → Robustness &
  Sensitivity Reviewer.
- **Dependencies:** subtasks 2, 3, 4 run in parallel on the current draft;
  subtask 1 runs after, so the writing review sees the fixes.
- **Conflict:** the Reviewer calls your headline sentence "clear and strong"; the
  Diagnostician flags that same sentence as reaching past your sample to the
  population.
- **Diagnose:** real disagreement, and a valuable one. The Reviewer optimized for
  fluency, the Diagnostician for the claim boundary. Fluency upgraded the claim.
- **Decide:** you side with the Diagnostician, rewrite the headline to state its
  reach, and verify by re-reading it against your inquiry declaration
  (non-AI check). You log the override: kept the boundary, softened the sentence.
- **Stop:** when every claim in the chapter traces to a ledger row and sits inside
  its declared reach, checked by you.

---

*Attach the completed worksheet to your M15 AI-management portfolio. See also:
[agent_role_cards.md](agent_role_cards.md) (the roles) ·
[ai_error_taxonomy.md](ai_error_taxonomy.md) (correlated errors, false
consensus) · [escalation_protocol.md](escalation_protocol.md) (when a conflict
touches a yours-alone decision).*
