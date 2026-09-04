# CHAPTER_DEFECTS — verified inconsistencies awaiting the author's review pass

Chapter review is **OPEN** (D37, after Architecture v1 froze). This file is the
standing register of **verified** defects found in EDR|AI chapter prose during
other work — figure building, deck generation, validation runs — so that a
finding made in passing is not lost between sessions.

**What belongs here.** A concrete, reproducible inconsistency inside a chapter:
a count that does not match its own list, a term defined one way and used
another, prose and code that disagree. Each row names the file and line so the
claim can be checked in seconds.

**What does not.** Style preferences, wording that merely reads awkwardly, and
anything already covered by `planning/TRANSLATION_BACKLOG.md` (PT/ES debt) or
`planning/BOOK_DESIGN_ACCEPTANCE.md` (the Architecture v1 contract).

**Who fixes these.** Not the assistant, unless asked. The book-first loop (D20,
rule 4) puts chapter edits with the instructor: Davi reviews and updates the
book, and the assistant then propagates the change across notebooks, decks and
site. A defect logged here is a candidate for his review pass, not a task an
agent should quietly action.

**Verification standard.** Every row below was independently confirmed by
reading the cited lines, not accepted on report. Rows found by one agent and
confirmed by another say so.

---

## Open

### D-01 · ch32 — "four ways" introduces eight named ways

- **File:** `book/part5-communicating/27-research-posters.qmd:42`
- **Severity:** low (a count, not a claim), but it is the section's opening
  sentence and a reader counts along.
- **What is wrong.** Line 42 reads "The decision is one judgment made four
  ways, and each way has a name." The bullets that follow name **eight**:
  headline claim, claim boundary, compass position, figure honesty, truncated
  axis, uncertainty on the page, accessibility, redundant encoding.
- **Note for the fix.** "Four" may be the stale number from an earlier draft, or
  the eight may be intended as four pairs (claim / boundary, honesty / axis,
  uncertainty / accessibility, redundancy / …) — the grouping is not stated
  either way, so this needs an authorial decision rather than a mechanical
  count change.
- **Found by:** the peer session's figure pass, with Codex; confirmed here by
  reading `:42` and the bullet run at `:44-72`.

### D-02 · ch32 — "compass position" is defined as kind × reach, then offered as a three-way list containing "associational"

- **File:** `book/part5-communicating/27-research-posters.qmd:50` against `:231`
- **Severity:** **the more serious of the two ch32 rows.** It touches a
  standing project rule, not just a count.
- **What is wrong.** Line 50 defines the term correctly: "**Compass position.**
  The kind and reach of the question your project answered." Line 231, inside
  an embedded AI prompt, asks the student to paste `my compass position:
  "[descriptive / associational / causal]"`. That list drops **reach**
  entirely, and "associational" is **not a compass position** — the compass's
  kinds are descriptive and causal (`planning/INQUIRY_MAP.md`), and
  "associational" is a claim-strength word describing what a warrant licenses.
- **Why it matters beyond the chapter.** Offering "associational" as a position
  invites exactly the move D35's relabelling prohibition forbids: a causal
  question with a weak design being re-described as something milder instead of
  being called *causal, currently unidentified*. The prompt is student-facing
  and is copied into a tool verbatim, so it teaches the wrong taxonomy at the
  point of use.
- **Suggested direction (author's call).** Make the prompt ask for kind **and**
  reach, matching `:50` and the ch06 figure `inquiry_compass.png`.
- **Found by:** the peer session's Codex run; confirmed here by reading both
  lines.

### D-03 · ch37 — the seed is the second package sin in prose and "sin four" in code

- **File:** `book/part6-after-conference/34-open-and-reusable-research-packages.qmd:54-57`
  against `:102`
- **Severity:** low, but it is the kind of thing a careful student notices and
  loses confidence over.
- **What is wrong.** The prose names the five package sins in order — a
  hard-coded path, a **missing seed**, a by-hand edit, an undocumented
  exclusion, stale data — making the seed **sin two**. The clean-capsule code
  cell at `:102` comments `SEED = 464   # sin four, fixed: the seed is pinned`.
- **Note for the fix.** Either the comment takes the prose's number, or the
  prose's order changes; the sins are not numbered anywhere else, so renumbering
  the list is cheap. Check the other four sins' code comments in the same cell
  for the same drift before deciding.
- **Found by:** the peer session; confirmed here by reading both locations.

---

## Resolved

*(none yet — a row moves here with the commit that fixed it, and keeps its id)*
