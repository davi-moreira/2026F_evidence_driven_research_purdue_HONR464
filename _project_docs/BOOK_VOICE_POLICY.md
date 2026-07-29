# BOOK_VOICE_POLICY — how EDR|AI must sound (D28)

The book's prose must read as though a first-rate human editor wrote it for
undergraduates: controlled, concrete, warm, and clean. It must never sound
machine-generated. This policy adapts the "rewrite-introduction" style guide
(github.com/mgaldino/agents-workflow, `skills-docs/rewrite-introduction/
references/style-guide.md`) to this book's audience: honors undergraduates
with no quantitative background. Every new or revised passage — English
first, then the PT/ES translations — is written under this policy. Existing
chapters are brought under it as Davi's review advances (the
BOOK_REVIEW_STATUS banner workflow), so the sweep happens chapter by chapter,
never as a blind global rewrite.

The linter `scripts/voice_lint_book.py` checks the mechanical subset
(warnings by default, `--strict` to fail). The rest is judgment, applied at
writing time.

## What stays — the book's teaching devices are not AI-tells

These are deliberate pedagogy (D14) and remain untouched:

- Second person throughout; the reader is "you", doing the work.
- Named research-world stakeholders opening sections, and inline Q&A blocks.
- **Bold term** → one-sentence plain definition → concrete example, on every
  technical term's first use. Bold exists for THIS, and for referring to
  named sections ("the **It is your turn** section"), nowhere else.
- Short-to-medium sentences (roughly 12–25 words), one idea each — but with
  deliberate variation, not a metronome.
- The book's one italicized motto (*AI is your arm and your research
  assistant, not your brain*). No other italicized stress.

## The tells to eliminate

1. **Contrast-formula defaults.** "It is not X, but Y", "Rather than X, this
   chapter shows Y" — only when the logic genuinely needs the contrast,
   never as sentence architecture.
2. **Pivot-word accumulation.** However, indeed, in fact, notably, crucially,
   moreover, furthermore. One earns its place occasionally; a rhythm of them
   is machine cadence.
3. **Typographic emphasis.** No bold or italics to make a point land (see
   the two allowed uses above). Em dashes rare; prefer commas, colons, or a
   full stop. No colon-heavy sentence chains, no semicolons to simulate
   sophistication.
4. **Neat symmetry.** No default triads ("clear, concrete, and compelling"),
   no balanced pair formulas. Lists exist when the content is genuinely a
   list, at whatever length the content has.
5. **Generic smart-sounding phrases.** Sheds light on, speaks to, at the
   heart of, underscores the importance of, plays a crucial role, raises
   broader questions, a testament to, in today's world, navigating the
   landscape of, delve into, unlock, harness. Say the specific thing instead.
6. **Vague upgrade words.** Robust, nuanced, compelling, powerful, striking,
   crucial, key, critical, vital — as intensifiers they explain nothing.
   Either show the property or drop the word.
7. **Synthetic paragraph endings.** No sweeping closers ("This matters far
   beyond this chapter"). A paragraph ends when its job is done.
8. **Filler and inflated setup.** "It is important to note that", "it is
   worth noting", "in the context of", "has implications for". Delete;
   state the claim.
9. **Inserted transitions.** Prose may move briskly. Do not add connective
   tissue only for smoothness.
10. **Empty compression.** Shortening that loses the analytical content is
    not concision. Keep the specifics; cut the ornament.

## Sentence craft for this audience

- Open sections with something concrete: a person, a number, a decision on
  the table — never with throat-clearing about what the section will do.
- Concrete nouns and strong verbs; abstraction only when the concept itself
  is the subject, and then immediately grounded in an example.
- State mechanisms explicitly. The reader never has to infer what causes
  what; this book teaches people who are learning to reason causally.
- Metadiscourse minimal: the structure of a chapter shows itself. (The
  standing D25/D27 corollary also applies: no artifact-boundary
  meta-commentary — never tell readers what something is NOT part of.)
- Claims stay honest and bounded: no novelty inflation, and uncertainty
  stated wherever results are stated (the course's own evidence rules apply
  to the book's prose too).

## Application

- **New prose**: drafted under this policy, then `voice_lint_book.py` run on
  the touched edition(s) before rendering.
- **Existing chapters**: swept when Davi reviews each chapter (flip in
  `planning/BOOK_REVIEW_STATUS.yml`); the linter report for that chapter is
  part of the review.
- **Translations**: PT/ES follow the same policy; the linter carries
  per-language tell lists. The EN edition remains the source of truth.
- **Notebooks and course material**: D14's notebook voice rules already
  cover the classroom side; where the generator copies book prose into the
  companion notebooks, fixing the chapter fixes the notebook on the next
  build.
