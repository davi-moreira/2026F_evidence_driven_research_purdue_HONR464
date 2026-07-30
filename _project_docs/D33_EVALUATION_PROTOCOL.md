# D33/D34 Feasibility Evaluation Protocol — does the required path fit the room?

**Created:** 2026-07-30 (D34; closes the evidence gap named in task #18 and in
the Codex critique of the lecture-structure review).
**Question under test:** can a 50-minute period with ~5 honors students and a
student lead actually carry the seven-move required path, at D33/D34 in-class
weights, ending clean at minute 50?
**Status of every desk claim:** "the required path now fits the room" and
"Wednesday's 38–42 accuracy lock is enough consolidation" are HYPOTHESES.
This protocol is how they get data. No treatment-effect claims at n≈5 —
repeated descriptive evidence and failure logs only.

---

## 1. The four dry-run cases

Run these before or during Weeks 1–2, in this order of priority. Use five
participants whenever possible (colleagues, TAs, or honors volunteers), and
for at least one run have someone other than the instructor play the SRL from
the notebook's Lead Brief alone — that simulates the real information state of
a student lead.

| Run | Case | Why this one |
|---|---|---|
| 1 | **nb03 Lecture 1** (single-lecture week) | The AI/source-verification stress case: two sanctioned live exchanges, retrieval of real sources under time, the SDIIVDD chain end to end. |
| 2 | **nb08 Lecture 1** (single-lecture week) | The densest lecture in the course; also exercises the D34 compact cross-validation + shift probe before the verdict. |
| 3 | **One ordinary Monday** (nb05-L1 recommended — the gold standard) | The 9/22/12/7 frame under typical load. |
| 4 | **One ordinary Wednesday** (nb05-L2 recommended) | The 7/23/12/8 frame including the 30–38 peer defense and the 38–42 SRL synthesis + accuracy lock. |

## 2. The timing sheet (one per run)

Record actual clock time at each boundary, not whether it "felt fine".
Blocks are the D22 frames; sub-events are the moves inside them.

```
Run #___   Case: ______________   Date: ______   Participants: ___   SRL: ______

BLOCK BOUNDARIES (planned → actual)
  Block 1 ends      (Mon 9 / Wed 7)    planned ____  actual ____
  Block 2 ends      (Mon 31 / Wed 30)  planned ____  actual ____
  Peer defense ends (Wed only, 38)     planned  38   actual ____
  Block 3 ends      (Mon 43 / Wed 42)  planned ____  actual ____
  Room closes       (50)               planned  50   actual ____

MOVE-LEVEL EVENTS (start–end, one line each)
  🧩 puzzle/challenge ____-____   🔮 predict ____-____   🛠️ run ____-____
  🔍 read ____-____   📝 practice ____-____   ⚖️ choice ____-____
  🎯 one sentence ____-____   🛡️ ritual close ____-____   📒 ledger ____-____
  Claim Ticket ____-____   [Wed] 🧑‍⚖️ checkpoint ____-____
```

## 3. The AI-latency field

For EVERY live AI exchange in the run (there is exactly one per lecture; nb03
has two):

```
  Prompt sent at min ____   First usable output at min ____   Latency ____s
  Simultaneous users when sent: ___ of 5
  Failure? (timeout / refusal / fabrication / wrong direction): ____________
  Recovery action + minutes lost: ____________
```

If any student cannot reach the AI tool at all, log it as a failure with the
fallback used. Five simultaneous calls on one classroom network is part of
what is being tested.

## 4. Predeclared pass criteria

A run PASSES only if ALL of the following hold. Decide these from the sheet,
not from impressions, and decide them the same day.

1. The room closes by **minute 50** (52 = fail, not "close enough").
2. The final closing block (Mon 43–50 / Wed 42–50) keeps **at least 7 minutes**.
3. **All five participants** complete every required response: the written 🔮,
   the 🔍, the ⚖️ line, the 🎯 sentence, the four-line 🛡️, and the 📒 row.
   Spot-read them: an empty or gibberish cell counts as not completed.
4. **No verification step is skipped** — the "After running, verify" checklist
   of the live exchange is actually performed, not narrated.
5. **No unresolved claim enters a ledger.** On Wednesday, anything wrong that
   survived peer defense is corrected in the 38–42 accuracy lock BEFORE the
   ledger row; if a wrong claim reaches a ledger with a verification stamp,
   the run fails regardless of timing.
6. **The SRL keeps the room** — instructor interventions follow the
   intervention protocol (signal, prompt, correct); a takeover of a lead-owned
   block is a fail for the format even if timing passes.

## 5. Observer form (one per run, filled by whoever is not leading)

- The block that ran longest over plan, and what consumed it (transition,
  AI latency, discussion, writing, code trouble):
- Number of times students visibly lost their place in the notebook:
- The move that produced the weakest engagement, and what it looked like:
- Any anxiety signal at spoken moments (📝 aloud, peer defense, Claim
  Ticket) worth a design response:
- One thing to cut first if this lecture runs behind live:
- One thing that worked better than the plan assumed:

## 6. Short learning and accuracy checks

- **Immediate:** at close, each participant states the day's decision rule
  from memory in one line. Record how many of five can.
- **Delayed (real weeks only):** Wednesday's 0–7 retrieval drill IS the
  delayed check on Monday — record how many of five retrieve the rule
  unprompted before the lead reveals it.
- **Ledger audit:** within 24h, read the five 📒 rows. Count rows whose
  verification column names a real check (something that could have failed)
  versus a restatement. A verification column full of restatements means the
  ledger is being performed, not used — a curriculum problem, not a student
  problem.

## 7. The first-two-weeks review rule

After meetings 1–6 (Weeks 1–2), sit down once with the sheets and decide,
explicitly and in DECISIONS.md:

- **If runs pass:** freeze the structure until midterm; keep collecting
  timing sheets passively on Wednesdays (they cost one observer form).
- **If timing fails systematically in Wednesday block 2 (7–30):** cut there
  first — the block already has a designed cut order: the 🔁 rerun is
  optional, 🔬 interrogates output already in hand, and the lab's second
  comparison goes before the live exchange does. Do NOT reopen D22.
- **If the close (last 7–8 min) fails:** the pilot candidates from the
  specialist review go live — write-then-speak 📝 and the ⚖️ "I chose X over
  Y because Z" grammar — before any structural change.
- **If accuracy fails (criterion 5):** lengthen the accuracy lock inside
  block 3 (peer defense to 36) before touching anything else; that is a
  2-minute internal move, not a frame change.
- Only if two of the four levers above fail in BOTH weeks does a D22
  revision go on the table, as its own decision with these sheets as its
  evidence.

**File the sheets** (scans or photos are fine) in gitignored
`_production_kit/d33_eval_sheets/` so the midterm review can cite them.
