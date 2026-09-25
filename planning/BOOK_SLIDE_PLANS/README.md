# Slide plans — the editorial overlay on the EDR|AI decks

One file per chapter, named for the chapter's **immutable lesson id** from
`planning/BOOK_ARCHITECTURE.yml` (never its number, never its filename):

    planning/BOOK_SLIDE_PLANS/<lesson-id>.yml

## What a plan is, and is not

`scripts/build_studio_slides.py` already reads every VERBATIM element straight
out of the chapter and needs no help with it: the research-decision thesis, the
key-term cards, the figures, the mermaid diagrams, the worked-example code, the
AI failure case, the "Do not delegate" rule, and the "It is your turn" steps.
None of those belong in a plan, and a plan can neither suppress nor rewrite
them.

What a plan covers is the **prose** — the paragraphs in which the chapter
argues. Prose does not fit on a slide unchanged, so the plan says how to cut
each prose section into slides: a headline, a few short lines, and the speaker
note the instructor reads from.

A section with no plan entry falls back to a mechanical rendering, so a partial
plan is valid and a missing plan is not an error. Adding one only makes the
deck sharper.

## Schema

```yaml
lesson: curiosity-to-problem          # the immutable id; must match the filename
source_sha256: "3f9a…"                # digest of book/<source> when written
sections:
  "Why this decision matters":        # EXACT `## ` heading from the chapter
    - title: "A menu from 2019"       # the slide headline
      bullets:                        # 2–5 lines, ≤ 18 words each
        - "An \\$11 meal now costs \\$16. Your first reaction: prices exploded."
        - "Useful. Not yet a finding."
      note: >                         # what the instructor says here
        The point of the example is that the first explanation stops being
        the only one you can see.
  "The concept":
    - title: "Abduction is the jump"
      layout: terms                   # a definition-card slide
      terms:
        - term: "Abduction"
          definition: "proposing what might explain a pattern in the first place"
    - title: "The cycle, drawn"
      mermaid: 0                      # the section's 1st mermaid block
  "A worked example":
    - title: "Sixty first-years, steps and sleep"
      bullets: ["…"]
      code: 0                         # the section's 1st code block
```

### Slide keys

| key | meaning |
|---|---|
| `title` | the slide headline. Required. A claim, not a label. |
| `bullets` | 2–5 short lines. Markdown allowed (`**bold**`, links, `[@cite]`). |
| `lead` | one emphasised sentence, set above the bullets |
| `note` | speaker notes — where the chapter's full argument goes |
| `layout` | `default` (bullets) · `terms` (definition cards) · `two-col` |
| `terms` | with `layout: terms`: a list of `{term, definition}` |
| `quote` | a sentence from the chapter, set in a quiet card |
| `table` | a markdown table |
| `figure` | a figure path used **in that section** of the chapter |
| `width` | figure width, default `70%` |
| `mermaid` | 0-based index of a mermaid block **in that section** |
| `code` | 0-based index of a code block **in that section** |

`figure`, `mermaid` and `code` address blocks that already exist in the
chapter. They cannot introduce new ones, and an out-of-range index is ignored.

### Keeping a section off the deck: `omit:`

A plan may also carry a top-level `omit:` list (D83, book-only further
routes). Each entry is the EXACT `##` heading of a chapter section that must
never reach the deck: no prose slide, no key-term card, no figure. The book
can then grow a section (a new design discussion, say) without changing the
lecture the live course already teaches from that deck.

```yaml
lesson: observational-causal
source_sha256: "…"
omit:
  - "Process tracing: causal inference inside one case"
sections:
  "The concept": [...]
```

An omission is invalid when `omit:` is not a list, when an entry is not an
exact `##` heading of the chapter (matching is case-sensitive), when it is
builder-owned ("An AI failure case", "It is your turn" cannot be omitted),
when it is listed twice, or when the same heading is also planned under
`sections:`. One read-only helper, `omit_problems()` in
`scripts/build_studio_slides.py`, owns that rule, and both tools call it:

- the **builder** runs it over every target plan **before writing anything**
  (logo, deck or figure) and exits 1 on any defect, in build and `--check`
  mode alike, leaving every deck byte untouched. This matters because the
  book-edit hook runs the builder directly: renaming an omitted heading
  without updating the plan would otherwise match nothing and push the
  section into a lecture through the mechanical fallback;
- `scripts/validate_slide_sync.py` reports the same defects in CI.

The check does not depend on the plan's digest. The builder honours `omit:`
even while the plan is STALE, so a valid omission keeps its section off the
deck through the fallback, and an invalid one still stops the build. Lessons
marked `scope: book-only` in the manifest join no deck at all and need no
plan.

The guard has a committed negative test, which mutates a plan in memory and
builds into a scratch copy of `lecture_slides/` (no tracked file is written):

```bash
.venv/bin/python scripts/test_d83_guards.py
```

It renames an omitted heading on a stale plan and asserts that the builder
exits nonzero in both modes with deck bytes unchanged and that the validator
reports it; that a stale plan with a resolving omission still keeps the
section off (and that the section appears once the omission is removed); and,
for `planning/BOOK_MAP.md`, that only lessons listed under the crosswalk's
`not_adopted:` render as "— (book only)" while an adopted lesson stripped of
its home anchor fails both the generator and `build_book_map.py --check`.

## Rules a plan must obey

1. **Nothing new.** Every claim, number, name, and example on a slide is in the
   chapter. A plan compresses and orders; it never adds evidence, and it never
   softens or strengthens a claim the chapter bounded.
2. **No fabricated citations, ever** (D16). Carry `[@key]` through unchanged —
   the builder resolves it against `book/references.bib`. Never invent a key,
   an author, or a year.
3. **Second person, to the student** — the CRITICAL RULE on voice. Never write
   *"students"* as a third-party noun. `you`, or a neutral imperative.
4. **Undergraduate-friendly** (D14). Short sentences, one idea per line, a term
   defined before it is reused. Em dashes: at most one per bullet.
5. **No AI tells** (`_project_docs/BOOK_VOICE_POLICY.md`, D28). No *leverage*,
   *unlock*, *seamless*, *robust*, *powerful*, *delve*, *the power of*,
   *game-changer*, *empower*, *elevate*, *it is worth noting*, *in today's
   world*. No grand-but-empty closers. No rule-of-three for cadence.
6. **Uncertainty survives compression.** A claim the chapter states with its
   limits keeps them on the slide. A bullet that drops the bound is a defect.
7. **Escape money and tildes** in markdown: `\$50,000`, `\~30 sources`.
8. **Budget.** 8–14 planned slides per chapter across all its prose sections.
   A 6-chapter studio has to fit two 40-minute blocks.
9. **Headlines are claims.** "Abduction is the jump" beats "Abduction". A
   reader who sees only the headlines should get the chapter's argument.
10. **`source_sha256` is the chapter you actually read.** Compute it as
    `sha256` of the chapter file's bytes. When the chapter later changes, the
    mismatch is what tells us the plan needs revisiting — never fake it.

```bash
.venv/bin/python -c "import sys;sys.path.insert(0,'scripts');import slide_parts;print(slide_parts.digest_of('<source path>'))"
```

## Rebuild and check

```bash
.venv/bin/python scripts/build_studio_slides.py          # rebuild all 12 decks
.venv/bin/python scripts/validate_slide_sync.py          # fidelity + staleness
```

---

## Chapter defects the slide-plan pass surfaced

Building a deck means reading a chapter line by line against what a class will
see, and that pass found things in the BOOK that only the author can rule on.
None of them is a slide defect; each is recorded here so the fix happens in the
chapter, where it belongs.

| Chapter | What disagrees with what |
|---|---|
| `07-research-builds-on-research` | The worked example says the fabricated citation "took four minutes to find out"; the AI failure case says "You caught it in a minute." |
| `18-measurement-and-operationalization` | Line 91 puts the citation inside the quotation marks: `poor stand-in for "fitness [@cronbach1955construct]."` |
| `20-ai-as-analytical-assistant` | One filter has two names: the sample handle drops "the three who already had an offer in hand", the red-team paragraph refutes it as "the already-employed group". Line 113 also slips subject mid-sentence: "The block below builds the grid … then runs the placebo shuffle yourself." |
| `23-ai-as-adversarial-reviewer` | The prose says "the two loudest flags dissolved", but the same paragraph also refutes the third. |
| `26-claim-evidence-tables` | Row 1's claim carries two different evidence pairs: 48,900 / 79,800 in *The concept*, 47,871 / 78,117 in *A worked example*. Both round to 61.3%, in a chapter about traceability. |
| `28-poster-criticism` | The prose says the fix is "value labels and a hatch pattern"; the chapter's own code draws two grays plus a hatch and adds no value labels. |
| `29-research-pitches` | The middle pitch is "a three-minute walk" in the research decision, a "90-second walk" in *The concept*, and "the 3-minute version" in *It is your turn*. |
| `31-ai-disclosure-and-research-integrity` | Names Gemini in student-facing prose. D30 retired Gemini from student-facing surfaces; this chapter kept it. |

A plan may not paper over any of these: rule 1 says a slide carries what the
chapter says. When a chapter is corrected, its plan goes STALE by design and
gets revisited — that is the mechanism working, not a nuisance.
