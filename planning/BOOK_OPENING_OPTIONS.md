# Book-opening options — should EDR|AI start with Studio 2? (for D43 ruling)

**Date:** 2026-08-04 · **Prepared by:** Claude (implementer track) + Codex
(mirror partner track, gpt-5.6-sol xhigh, read-only) — two independent
analyses, merged; run artifacts in
`_adm/codex_collab/2026-08-04_opening-sequence/`.

**Davi's question.** Would it not be better to start the book with Studio 2
instead of Studio 1, so the sequence says *scientific discovery/research
with AI*, not the other way around? That may also fit the course better.
What are the options, and what other adjustments are worth the value?

---

## The ruling sentence

**The concern is correct, and the diagnosis is confirmed by both tracks
independently — but the best remedy is not the swap.** Make the reader's
first act research (a human-only curiosity commitment) and the first AI act
governed (ledger before prompt), inside the existing studio order. The full
swap is kept on the table as a post-launch contingency, priced honestly
below.

The felt sequence today, and the recommended experienced sequence:

- *Current felt sequence:* AI principle → AI role → AI protocol → AI
  ownership → research question.
- *Recommended:* **human curiosity → ledger and rules → verified AI
  assistance → formal research question.**

## Why the concern is right (evidence)

- The ToC's first four lessons are all AI-titled; the organization page's
  figure literally draws Studio 1 as a frame *containing* "the road" of
  Studios 2–12 (`build_book_part1_figure.py`); the preface's opening
  paragraph leads with what AI can produce (`book/index.qmd:15–35`).
- Yet the underlying design is already research-first where it counts:
  **ch1 opens the AI Research Ledger and demands human-written curiosities
  BEFORE its first AI prompt** (`01-…qmd:160–205`). The presentation hides
  the book's own best move.
- The course already models the recommended order: nb01 requires a human
  curiosity sentence before the first AI prompt, and M0 places the three
  curiosities before the AI baseline.

## The non-negotiable criterion (both tracks, independently)

**The first-AI invariant:** *human commitment → ledger opened → AI prompt →
independent check → ledger row.* Any option that breaks it is ruled out
regardless of rhetorical appeal. This is what kills the naive swap: ch5
carries three AI prompts and ch6 three more, logging to a ledger that would
not yet exist (`05-…qmd:167–246`), and ch5/ch1/ch2 carry explicit
continuity lines ("There is no question yet", "You have a ledger and three
curiosities") that a reorder falsifies.

## Options compared

| # | Option | Reader's first act | First AI interaction | Book cost | Course risk (launch Aug 24) |
|---|---|---|---|---|---|
| 1 | Full swap (S2↔S1, repaired) | Their research problem | Ch5's prompts, needs a new "safety boot" before them | ~10–15 days¹: 6 lessons rewired, both milestone semantics, URL/alias migration, figure, S3 references | HIGH — reopens D41 (W1/W2, M0/M1, nb01/nb02, briefs, quizzes, schedule) |
| 2 | Partial braid (ch5→S1, ch4→S2) | Their research problem | Same ch5 repair needed | ~6–10 days¹; no URL moves, but both milestone identities blur | HIGH — W1/W2 repartition |
| 3 | New AI-free opening lesson ("Begin with a curiosity") | A curiosity, no tools | Unchanged (ch1, governed) | ~5–8 days¹: a 40th lesson, authored + companion + review + replay; risks duplicating ch1's curiosity exercise and adding W1 load | MEDIUM — one new M0 assignment |
| 4 | **Research-first on-ramp in Studio 1 (RECOMMENDED)** | A curiosity, no tools (authored "opening move" on the S1 opener, carried into the workbook) | Unchanged (ch1, governed) | ~2–4 days¹: opener field + generator, ch1 bridge, S1 retitle, preface + figure + organization page | LOW — no crosswalk change; nb01 makes the ledger's creation visible; S1 display title updates |
| 5 | Preface/figure reframe only | Unchanged | Unchanged | ~0.5–1.5 days¹ | NONE — but the ToC still opens with four AI titles; a patch, not a fix |

¹ Maintainer-day figures are UNVERIFIED planning estimates (Codex track),
counting authoring + review + validation + course propagation + replay.

## The recommended package (Option 4, in full)

1. **The opening move.** A new authored field on Studio 1's opener (and
   workbook), human-only, before "The milestone ahead": write one thing you
   genuinely want to understand, why an answer would matter, and what
   evidence could change your current belief. No tool allowed. Feeds ch1.
2. **Studio 1 retitle** (display only, id/rank/URLs unchanged): something
   like "Begin the research and govern the work" — final wording Davi's.
3. **Ch1 bridge:** "There is no question yet" becomes a bridge from the
   opening move; the three-curiosity exercise broadens the committed
   curiosity; ledger-before-prompt order preserved.
4. **Preface rewrite** (first paragraphs): research problem first, AI as
   the instrument inside the method.
5. **Figure rebuild:** the research road from curiosity to release as the
   main visual, with governance/verification/evidence/ethics/uncertainty as
   rails crossing it — retiring the "Studio 1 contains the book" frame.
6. **Course side (small):** update the S1 display title in the master plan
   and schedule data; make nb01 visibly create the ledger before Exercise
   2's first prompt. No crosswalk or milestone-event changes.
7. **PT/ES:** one replay entry in TRANSLATION_BACKLOG.md; no frozen-source
   edits (D36).

**Reserve the full swap** for a post-launch cycle, only if first-reader
testing still reports "an AI book". A real swap then means: the five-step
first-AI safety boot before ch5's prompts, studio/milestone URL aliases (a
generator extension — milestone pages have no alias front matter today),
an immutable `workbook_path` field (Colab paths cannot be aliased),
orphan-file cleanup, rewritten milestone semantics both ways, S3's
"revision of your Studio 2 declaration" and the rubric line that quotes it,
and a deliberate D41 course amendment — never a quick rank edit.

## Pedagogy note (external evidence, partner track; DOIs opened there)

Problem-first sequencing helps on average (Sinha & Kapur 2021 meta-analysis,
DOI 10.3102/00346543211019105) but the effect rides on design fidelity, and
two quasi-experiments in social-science research methods specifically found
no advantage (DOI 10.1007/s11251-020-09525-2). Learner-generated relevance
reliably improves interest (Hulleman & Harackiewicz 2009, Science, DOI
10.1126/science.1177067). The safe inference: a bounded, personally
meaningful research move first, then just-in-time governance for the first
consequential AI use — which is exactly Option 4, not the raw swap.

## Other adjustments worth the value (merged, ranked)

1. **Finish the practice grain (A4): studio workbooks need worked examples,
   starter data, and faded tasks** — today they are blank response cells +
   one scratch cell. The largest documented gap between "manual" and
   "forms attached to a manual". Tranche: Studios 1–4 first. (~1–2
   days/studio¹.) Ruling needed only on the launch tranche size.
2. **A rolling author-review launch gate.** All 40 review flags are still
   `reviewed: false`; required course readings would reach students under
   an "unreviewed" banner. Proposal: Preface + organization page + Studios
   1–2 reviewed by Aug 24; each later studio one week before first course
   use. Only Davi can do this.
3. **Reduce and tier the opening workload.** Studio 1's four IYTs total
   ~2,800 words, 23 steps, ~12 prompt blocks (both tracks counted
   independently) — while M0 calls itself the smallest, warmest milestone.
   Proposal: one core contribution + one core AI cycle per opening lesson;
   further prompt angles marked optional depth; M0 requires the milestone
   checklist's named contributions, not every prompt. Changes what
   "complete the IYT" means → Davi's ruling.
4. **Two cold tests after the opening change:** a 45–60-minute "first mile"
   test (does a novice say the book is research-with-AI?) and the
   already-specified second A1 pilot on the no-permission route. Turns the
   sequencing question into observed reader behavior.
5. **Fix the RDSS positioning claim.** The preface still says EDR|AI
   "translates" RDSS; the acceptance record itself calls that an overclaim
   (`BOOK_DESIGN_ACCEPTANCE.md:299`). Build the adopted/adapted/omitted
   coverage matrix and narrow the sentence ("draws its design framework
   from"). Cheap, protects the book's scholarly identity.
6. *(Already queued in D40/D42 records, restated for completeness:)*
   policy-brief lesson depth; ch37 retitle; rank-free milestone URLs at
   the next URL-break; per-lesson IYT gap list; `_iyt-rubrics` retirement.

## Decisions for Davi (D43)

| Decision | Joint recommendation |
|---|---|
| Opening architecture | **Option 4**; no studio swap before launch |
| Studio 1 display title | "Begin the research and govern the work" (or Davi's wording) |
| First-AI invariant | Adopt as binding in book and nb01 |
| Full swap | Post-launch contingency only, with the priced migration |
| Opening IYT load | One core contribution + one core AI cycle; rest optional |
| Review gate | Preface + org page + Studios 1–2 by Aug 24 |
| A4 tranche | Studios 1–4 workbook practice kits first |
| RDSS positioning | Coverage matrix; retire unqualified "translates" |

**Process note.** Mirror-mode partner run and implementer track reached the
same primary recommendation independently (strong convergence evidence).
Codex-only contributions: the opening-move-on-the-opener design (leaner
than the implementer track's new-lesson variant), the workload counts, the
review-gate and RDSS items, the external pedagogy evidence, and the
full-swap migration details (milestone aliases, workbook_path). Implementer
track: the first-AI dependency analysis, course W1/M0 verification, and the
verification of every Codex repo claim cited here.
