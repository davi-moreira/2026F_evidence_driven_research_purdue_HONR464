# TRANSLATION_BACKLOG.md — deferred PT/ES work under the D36 freeze

**Status: FROZEN (D36, 2026-07-31).** PT/ES are not edited or rendered during
Phases 1–4 of the D35 build. Every PT/ES page carries a development notice
(injected by `book-pt/_lang-switcher.html` / `book-es/_lang-switcher.html`)
naming the English edition as the version of reference. This file is the
complete ledger of what the end-of-project translation pass must cover; an
item missing here is a defect. The 6.2 release blocker lives on: translations
may not ship *as current* before this backlog is worked and cleared.

**Freeze baseline:** commit `50f6ce9` (2026-07-31). The authoritative diff for
"what changed in English during the freeze" is
`git diff 50f6ce9..<end> -- book/` — this list annotates it, it does not
replace it.

## A. Already stale at the freeze (pre-existing debt)

1. **ch14 (PT/ES)** — round-4 verdict §6 (T1), exact fixes:
   - PT "o modelo **acerta** os coeficientes" → "ajusta"/"estima" (training
     fits coefficients; it does not get them right by definition).
   - PT `distância` / ES `distancia` for model-selection bias → "diferença
     com sinal entre..." / "diferencia con signo entre..." (the code computes
     a SIGNED gap; 36.4% of worlds are negative).
   - The noise-extension sentence (EN's old "raise the noise and watch all
     three grow") → the corrected EN wording: rerun several noise levels and
     compare mean, median, frequency, and maximum separately; a single seeded
     extreme need not move monotonically (verified: max FALLS at noise 0.70).
   - Then re-verify the whole chapter sentence-by-sentence against settled EN.
2. **ch21, ch22 (PT/ES)** — NEVER crossed. Both hold pre-correction text
   (spec-curve/estimand and null-spread content). Translate from settled EN
   only; round 4 explicitly gated their crossing.
3. **Preface bounded-claim fix** — applied to EN `book/index.qmd` on
   2026-07-31 (A1 mitigation: "guided path" phrasing, hard-coded "37"
   removed). `book-es/index.qmd` (~line with "37 secciones") and
   `book-pt/index.qmd` (lines ~79–86, "as 37 seções … caminho completo")
   still make the retired claim.
4. **ch25 grammar + emphasis (PT/ES)** — round-4 T2: `status é não
   identificada` / `estado es no identificada` attach a feminine participle
   to a masculine noun → `não identificado` / `no identificado` (or make
   resposta/respuesta the explicit noun). Also remove the repeated bold card
   labels and italicized status phrase (BOOK_VOICE_POLICY: bold at first
   definition only).

## B. Structural changes accumulating during the freeze (Phases 2–4)

4. **Two new lessons** (uncertainty foundations; ethics & data governance) —
   full translation, including seeded-simulation labels localized via
   `scripts/build_book_sim_figures.py`.
5. **Spine reorganization** — manifest-generated `_quarto.yml` order, any
   chapter renumbering, hard-coded chapter-number prose references swept to
   links. PT/ES `_quarto.yml` must be regenerated to mirror the EN manifest.
6. **Station workbooks (12) + versioned Research Contract** — new files,
   full translation.
7. **De-coursing edits** — Part VI retitle, ch33 dossier→note, ch37
   medium-neutral release audit, course-lab paragraphs moved out of chapter
   bodies, F10 reframing, preface updated to the stations spine.
8. **Authored rubrics** (`planning/BOOK_ASSESSMENTS.yml`) — localized rubric
   cells replace the auto-derived IYT rubrics in PT/ES companions.
9. **References apparatus** — `references.bib` shared; any in-prose citation
   sentences translated.
10. **PT/ES companion notebooks** (`notebooks/book/pt/`, `notebooks/book/es/`)
    — regenerate with `scripts/build_book_notebooks.py` ONLY after the PT/ES
    chapters are resynchronized (the generator skips PT/ES during the freeze).

## C. Verification required before the freeze lifts

11. **Human PT/ES methods review** — required by round 4: an English
    substring scanner cannot certify translated meaning; a human methods
    reader per language signs off on ch06/09/10/12/14/15/18/21/22/25/32 at
    minimum. Davi schedules this.
12. **Misconception gate over PT/ES** — extend/verify
    `planning/MISCONCEPTION_MANIFEST.yml` translated `rejects` families
    against the resynchronized text; `validate_misconceptions.py` green.
    Round-4 G4 addition: the `numbers:` evaluator must gain PER-EDITION
    claims — PT/ES numeric prose AND localized alt text for ch14/ch15/ch22
    (and any new seeded figure) — so a decimal-rendering drift in one
    language fails on its own.
13. **Sync validator over all three editions** — `validate_book_sync.py`
    restored to three-edition scope (EN-only scope during the freeze).
14. **Remove the freeze apparatus** — delete the development notices from
    both `_lang-switcher.html` files, restore any EN-page language buttons
    repointed to the PT/ES index (Phase 3) back to per-page counterparts,
    restore CLAUDE.md §6 to the resynchronize-on-every-edit rule, and mark
    this file CLEARED with the closing commit hash.
