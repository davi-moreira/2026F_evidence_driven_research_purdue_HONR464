# Cold-test protocols — the first mile, and the second A1 pilot (D43)

Two observational instruments, prepared under D43. Running them needs
Davi's go (participant, timing); nothing here executes by itself.

## Protocol 1 — the first-mile test (45–60 minutes, one novice reader)

**Question.** Does the revised opening read as *research with AI*, not the
other way around, and does the first-AI invariant hold in a real reader's
hands?

**Participants.** One undergraduate (or comparable novice) minimum; 5–8
with mixed AI habits is the diagnostic ideal. Real readers, not simulated
ones; an AI-simulated pass may be run as a cheap pre-check but never
substitutes for the human sessions. Before recruiting, Davi determines the
applicable consent and institutional-review requirements.

**Materials.** The rendered book from the preface through Chapter 1's "It
is your turn", plus a blank sheet for the opening move; a screen the
observer can see; no coaching beyond the script.

**Script.**
1. "Read from the preface. Work anything the book asks you to work.
   Think aloud when you decide to skip something." (0–35 min)
2. Stop the reading at the end of Chapter 1's core cycle. Ask, in order:
   - "In one sentence, what is this book about?"
   - "What was the first thing the book asked you to DO?"
   - "When you used the AI tool, what did the book make you do first, and
     after?"
   - "Whose job is it to decide what the final claim says?"
3. Collect the artifacts: the opening-move page, the brainstorm receipt
   with its NEW labels, and the chosen problem with its reasons.

**Observation checklist (mark each yes/no with a timestamp).**
- Reader writes the opening move before opening any tool, and every AI
  exchange afterward leaves a receipt (task, tool, kept and rejected,
  check).
- Reader audits the brainstorm's NEW elements without prompting, and can
  say which stretch they rejected and why.
- Reader can state the book's subject as research (their words) rather
  than AI.
- Reader identifies the never-delegate boundary unprompted or when asked.
- Any point where the reader stalls, rereads twice, or skips: note where.

Two additions to the script, from the partner track: at the end, ask the
reader to reconstruct, without looking back, the order of their first five
moves (curiosity committed → stretched with a receipt → problem chosen →
ledger opened with the retrospective row → first verified catch); and note
every point
where they ask "do I have to do this?".

**Pass signals.** HARD GATE: zero readers carry forward a tool-chosen
problem they cannot defend as their own, and no AI exchange goes without a
receipt. Then, reported as numerators over denominators: most readers (aim
≥80%) complete the opening move without AI, carry their own curiosity into
Chapter 1, independently open a source rather than asking the AI to check
itself, reconstruct the five-move order, distinguish core from optional
depth, and describe the book unaided as doing research with governed AI.
**Fail signals.** "It's a book about AI"; a receipt-less exchange; a
tool-chosen problem; the
opening move skipped as decorative.

**Output.** One page: checklist, quotes, artifact photos, and the repair
list. File under `_adm/cold_tests/` (gitignored) with the date.

**Participant data management (required before recruitment).** Assign a
participant ID and redact names from artifacts before filing; obtain
written consent for any quotation or photo; store session materials in
the institution-approved location (the gitignored path only keeps them
out of git, it is not a privacy control); set and record a deletion date.
Davi completes the consent and institutional-review determination before
anyone is recruited.

## Protocol 2 — the second A1 pilot (end-to-end, no-permission route)

The instrument is already specified in `planning/BOOK_DESIGN_ACCEPTANCE.md`
(A1: a solo reader, working the studios in order on the no-permission
route — published aggregates, an open dataset, or simulated data — must
reach an executed analysis and a written, bounded claim). D43 adds only
the operational frame:

- Run AFTER the D43 opening changes and the Studio 1–4 practice kits are
  in place, so the pilot tests the current on-ramp.
- The reader is unaffiliated with the book's development, works from the
  book alone (no instructor, no hidden local knowledge, no paid AI
  dependency), starts from an original human curiosity, and takes the
  public/open no-permission route with real data whose provenance and
  terms are recorded.
- All twelve milestones are versioned; solo substitutes are labeled as
  proxies; the close is a complete note (methods, results, uncertainty,
  discussion, claim boundary, references, AI disclosure), a clean package
  run in a fresh environment, and a release-or-withhold decision.
- Every stall is logged with the studio and step that owns the missing
  instruction.
- PASS: a defensible original empirical claim, or an evidence-based
  withhold with the failed gate and redesign documented. A toy
  calculation or constructed-data walkthrough does not lift A1.

**Davi rules on:** who runs each protocol, when, and whether the first
mile passes. The evidence standard for lifting P1 stays the acceptance
document's.
