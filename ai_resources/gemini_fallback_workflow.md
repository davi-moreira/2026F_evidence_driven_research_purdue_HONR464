# Gemini Fallback Workflow

*What to do when Gemini is unavailable during class. An outage does not cancel the
lesson. The AI-investigation block has three fallbacks, the demo has a prepared
substitute, and the verification discipline never changes. This page is the calm
plan so a dead tool does not derail a lecture.*

---

## The principle

The course teaches a discipline, not a tool. **Ask → Verify → Document** works
with any AI partner, and the research thinking works with none. So when Gemini is
down (rate-limited, offline, or blocked on the campus network), you swap the
*tool*, never the *habit*. Every fallback below keeps the same ledger, the same
verification, the same human-owned decisions.

Plan for this. Outages happen on exactly the day you need the tool most.

## The two blocks an outage hits

A Mon/Wed lecture has two AI-dependent moments:

1. **The demo portion** — where a run is shown to the whole room.
2. **The guided AI investigation / applied AI laboratory** — where each person
   drives their own AI partner.

They fail differently and have different fallbacks.

## Fallback for the demo portion — prepared screenshots

The demo does not need a live tool; it needs a *worked run* to reason about.

- Before class, capture screenshots of a prior clean run of the demo prompt and
  its output, including one interrogation follow-up and one verification step.
- If Gemini is down, present the screenshots and walk the reasoning exactly as a
  live run: here is the brief, here is the draft, here is the follow-up, here is
  how we verified it.
- The teaching point is the *reasoning about the output*, which the screenshots
  carry fully. A frozen run is arguably clearer, since nothing hangs or wanders.

Keep a small folder of these prepared runs for each notebook so the demo is never
hostage to the network.

## Fallback for the AI investigation — three alternates, in order

When each person cannot reach Gemini for their own work, take these in order.

**Alternate 1 — the notebook's paper fallback.** Every notebook's instructor page
carries a **paper fallback**: the same investigation recast to run with no AI at
all, using the printed prompt, a provided sample output, and the reasoning
questions. Switch the AI-investigation block to the paper fallback and the lesson
proceeds on paper. This is the first move because it depends on nothing external.

**Alternate 2 — Microsoft Copilot.** Copilot is Purdue-provided and licensed, so
it is a legitimate substitute. Point the same briefed prompt at Copilot and
continue. **The ledger discipline is identical:** the tool-used column now reads
*Microsoft Copilot* instead of *Gemini*, and every output is still verified and
logged. Nothing about the standard relaxes because the tool changed.

**Alternate 3 — the GenAI Studio web UI.** Purdue GenAI Studio runs in the
browser independently of Colab. If Gemini-in-Colab is the thing that is down but
the network is fine, drive the same investigation through the GenAI Studio chat
interface, or through the relevant reviewer role if one fits the task.

If all three are unreachable, the paper fallback (Alternate 1) always works,
because it needs no service at all. That is why it is first.

## What changes for the Student Research Lead mid-class

The Student Research Lead is running the room when the tool dies. The move is to
switch tracks without losing the thread:

- **Announce the switch plainly:** "Gemini is down; we are moving to the paper
  fallback / Copilot." No scramble, no lost time.
- **Keep the same investigation question.** The puzzle and the reasoning do not
  change; only the partner that helps explore them does.
- **Hold the verification step especially hard.** An outage is the moment people
  are tempted to skip the check to save time. The Lead makes sure every output,
  from whatever tool, still gets a named verification and a ledger line.
- **Note the swap in the room's ledger discipline.** Everyone records the actual
  tool they used, so the ledgers stay honest about what really happened.

A tool outage handled well is itself a small lesson in the course's point: the
researcher, not the tool, is running the investigation.

## Before-class checklist for the instructor

- ☐ Prepared screenshots of the demo run are in the notebook's folder.
- ☐ The notebook's instructor page has its paper fallback ready to distribute.
- ☐ Copilot access is confirmed for the term.
- ☐ The GenAI Studio UI loads on the classroom network.

---

*See also: [prompt_design_guide.md](prompt_design_guide.md) (the same briefing
works on any tool) · [ai_research_ledger_template.md](ai_research_ledger_template.md)
(log the tool you actually used) · [agent_role_cards.md](agent_role_cards.md)
(GenAI Studio roles as alternates).*
