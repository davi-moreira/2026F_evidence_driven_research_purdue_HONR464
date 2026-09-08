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
agent should quietly action. D-04 is the one row so far that was fixed by the
assistant, and only because Davi forwarded the student's report with an explicit
instruction to solve it: that is the "unless asked" case, and it should be
recorded that way whenever it happens again.

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

### D-05 · ch04 — the Defend *definition* models a results statement with no uncertainty framing

- **File:** `book/part1-research-with-ai/03-specify-delegate-interrogate-inspect-verify-document-defend.qmd:74-76`
- **Severity:** medium, and it is the parent of the defect D-04 fixed.
- **What is wrong.** Step 7 of the seven-step list defines Defend with the
  example *"turnout was six points higher in these precincts, among registered
  voters, in this one election."* That bounds **reach** (these precincts, this
  election, registered voters) and says nothing about how much the number could
  have moved. Under the project's Uncertainty & Limitations rule a results
  statement with no uncertainty framing is a defect. The worked example's Defend
  sentence, which D-04 has now bounded, was generated by this definition; leaving
  the definition unchanged lets the pattern regenerate.
- **Note for the fix.** It also uses "six **points**" while the same chapter now
  teaches percentage points against relative increase forty lines later, so the
  two uses should be reconciled in one pass. This needs an authorial decision
  about how much a Studio-2 reader can be asked to bound, so it was not folded
  into D-04.
- **Found by:** the ch04 fix pass, 2026-09-08 (one of three judge agents);
  confirmed here by reading `:74-76` against the Uncertainty rule in `CLAUDE.md`.

### D-06 · ch04 — an optional prompt imports Studio-4 machinery into Studio 2

- **File:** `book/part1-research-with-ai/03-specify-delegate-interrogate-inspect-verify-document-defend.qmd:302-315`
- **Severity:** medium (a sequencing leak, student-facing, copied into a tool verbatim).
- **What is wrong.** The "Locate the standard method" prompt asks the reader to
  have an AI tool *"name the standard statistical test for comparing two
  proportions and the exact library function that implements it"*. Chapter 4 sits
  in Studio 2; hypothesis tests, standard errors and intervals are taught in
  `book/part2-curiosity-to-design/uncertainty-foundations.qmd` (Chapter 11,
  Studio 4). The reader is asked to fetch a tool they have not met and cannot yet
  judge, and confirming that a function exists does not verify that its
  assumptions fit this log.
- **Note for the fix.** The exercise's real target is *confident fabrication*, and
  that can be exercised without a significance test. One candidate replacement,
  proposed by the Codex partner run, has the reader ask the tool to list what the
  log records against what it would still need to know, and to mark anything that
  needs a missing column as unresolved. Replacing a whole exercise is an authorial
  call, so it was left for the review pass.
- **Found by:** the Codex partner run, 2026-09-08; confirmed here by reading
  `:302-315` against `book/_quarto.yml` and `uncertainty-foundations.qmd`.

### D-07 · ch04 — "this second angle" introduces the first angle

- **File:** `book/part1-research-with-ai/03-specify-delegate-interrogate-inspect-verify-document-defend.qmd:300` against `:316`
- **Severity:** low.
- **What is wrong.** Line 300 introduces the FIRST optional prompt with "run this
  second angle when you want more practice", and line 316 then introduces the
  next one with "*A second angle, optional:*". The reader counts two seconds and
  no first.
- **Note for the fix.** Line 300's sentence is boilerplate shared with other
  chapters, so check whether the collision is chapter-local before editing the
  shared string.
- **Found by:** the ch04 fix pass, 2026-09-08; confirmed by reading both lines.

---

## Resolved

### D-04 · ch04 — the chapter states a number its own code does not produce, and defends a claim the log cannot support  *(FIXED 2026-09-08)*

- **File:** `book/part1-research-with-ai/03-specify-delegate-interrogate-inspect-verify-document-defend.qmd`
- **Reported by:** Ishita Trivedi, a student in the course, by email on
  2026-09-04, after running the chapter's own code. She found it by doing
  exactly what the chapter's Verify step tells the reader to do.
- **What was wrong, both parts confirmed by execution.**
  1. The "An AI failure case" section said the tool reported the new page
     *"converts 50 percent better"* and that Verify *"collapses the '50 percent'
     to about 6"*, while the chapter's own block prints **+39.02%**. The prose
     landed 2026-07-27 (`8e7ea18`); the code block arrived six days later in the
     D38 worked-example pass (`21170c8`) and the two were never reconciled.
  2. The Defend sentence asserted the new page *"converted about 6 percent
     better"*. Week 2 is 200/5,000 against 212/5,000: twelve purchases,
     z = 0.60, p = 0.55, 95% CI on the difference [-0.54, +1.02] percentage
     points. More fundamentally, the constructed log records no assignment
     mechanism, no shopper identity and no day, so it licenses a **descriptive**
     statement about this log and nothing about future performance. A results
     statement with no uncertainty framing is a defect under the project's own
     rule, and this was one, inside the chapter that teaches Verify.
- **Collateral fixed in the same pass.** "recompute one version's rate for a
  single day" (`:288`) could not be carried out against a log whose columns are
  `version`, `week`, `bought`; the window was stated three ways ("the second
  week", "the five days both were live", "the days they actually ran side by
  side"); percentage points and relative increase were never distinguished,
  which is the confusion the student actually hit; the Defend sentence silently
  changed the unit from visits to shoppers; "lift" and "pooled" were used as
  technical terms before definition.
- **How it was fixed.** The prose moved, the **constructed data did not**. Two
  workflow judge agents and the Codex partner run independently rejected retuning
  `cells` to make "50 percent" true: it repairs a false assertion by rewriting the
  evidence until the assertion becomes true, which is the move this chapter exists
  to condemn, and it would erase the student's finding from the record. A
  one-integer variant (105 to 83) was rejected on separate grounds: it yields
  49.82%, which only *displays* as `+50%` because the format is `:+.0f`, so it
  rebuilds the identical trust gap one rounding step quieter in the one chapter
  that orders the reader to recompute by hand. The failure case now reports
  39 percent; Verify names both scales and then names what the log does not hold;
  Defend states the rates, the gap on both scales, the twelve purchases, and
  refuses the performance claim; a `> **A question that often comes up here:**`
  block answers the student's question in the book, in the book's voice, with a
  plain-prose forward pointer to the uncertainty lesson rather than the book's
  first chapter-to-chapter link; day-level language became week-level throughout;
  and the single 18-line fence became two 11-line fences, the second printing
  counts before rates and the gap on both scales.
- **Propagated:** `planning/BOOK_SLIDE_PLANS/sdiivdd.yml` (worked-example section
  rewritten to five slides including a `terms` slide and separate `code: 0` /
  `code: 1` slides, digest restamped),
  `notebooks/book/ch04_*.ipynb`, `lecture_slides/studio02.qmd`, `docs/`. PT and ES
  are frozen under D36 and still carry the defect: logged as
  `planning/TRANSLATION_BACKLOG.md` item 24, a **correctness** divergence that
  hard-gates the end-of-freeze sync.
- **Not machine-caught, and still is not.** `validate_slide_sync.py` performs no
  numeric cross-check between a chapter and its slide plan, and the chapter fence
  is ```` ```python ````, not ```` ```{python} ````, so Quarto never executes it.
  A hardening option exists and was not taken: register the block's printed
  numbers in `planning/MISCONCEPTION_MANIFEST.yml`'s `numbers:` family, which
  already binds prose strings to executed seeded computations for ch14, ch15 and
  ch22.
