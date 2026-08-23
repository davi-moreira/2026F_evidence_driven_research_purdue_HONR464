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

5. **Two new lessons** (uncertainty foundations; ethics & data governance) —
   full translation, including seeded-simulation labels localized via
   `scripts/build_book_sim_figures.py`.
6. **Spine reorganization** — manifest-generated `_quarto.yml` order, any
   chapter renumbering, hard-coded chapter-number prose references swept to
   links. PT/ES `_quarto.yml` must be regenerated to mirror the EN manifest.
7. **Station workbooks (12) + versioned Research Contract** — new files,
   full translation.
8. **De-coursing edits** — Part VI retitle, ch33 dossier→note, ch37
   medium-neutral release audit, course-lab paragraphs moved out of chapter
   bodies, F10 reframing, preface updated to the stations spine.
9. **Authored rubrics** (`planning/BOOK_ASSESSMENTS.yml`) — localized rubric
   cells replace the auto-derived IYT rubrics in PT/ES companions.
10. **References apparatus** — `references.bib` shared; any in-prose citation
   sentences translated.
11. **PT/ES companion notebooks** (`notebooks/book/pt/`, `notebooks/book/es/`)
    — regenerate with `scripts/build_book_notebooks.py` ONLY after the PT/ES
    chapters are resynchronized (the generator skips PT/ES during the freeze).
12. **D40 milestone restructure (2026-08-03)** — each studio now has TWO
    generated pages: the opener (milestone anticipation, `#checkpoint` legacy
    anchor, lessons with per-lesson contribution lines) and a **Milestone
    chapter** closing the part (practice steps, versioned record, rails,
    rubric, workbook badge). PT/ES must regenerate both page sets from
    `build_station_pages.py` + localized `BOOK_STATIONS.yml` milestone fields
    (`milestone_title`, `milestone_reason`, `hands_forward`, `contributions`),
    regenerate their TOCs (milestone chapter last in each part), and replay
    the reworded rubric texts in `BOOK_ASSESSMENTS.yml` (station/checkpoint →
    studio/milestone), the preface and "How this book is organized" milestone
    prose, the studio-continue pointer blocks in the last lesson of every
    studio, and the For Instructors milestone-disambiguation note.
13. **D40/D42 page behaviors** — `book/_page-behavior.html` (body links open
    in a new tab; References heading demoted to h2) and the `_quarto.yml`
    lines `reference-section-title: References` (D42 renamed it from
    Bibliography) + `include-after-body: _page-behavior.html` must be
    mirrored into `book-pt/` and `book-es/` (localized section title:
    "Referências" / "Referencias") when the freeze lifts.
14. **D43 research-first on-ramp** — localize: the Studio 1 `opening_move`
    (four lines, no-AI stop) + retitle ("Begin the research and govern the
    work"), the ch1 bridge and widened step 2, the preface's research-first
    paragraphs and the narrowed RDSS sentence (MIDA, companion-not-
    substitute), the road-and-rails figure (labels already staged in
    `build_book_part1_figure.py` L dicts — rerun with the freeze lifted),
    the *Optional depth* labels on eight Studio 1 prompts, and the
    Studio 1–4 `practice_kit` blocks (worked example / faded task /
    starter / verification).

19. **Lesson title de-coursed (2026-08-05).** "The Student as Research
    Director" → **"You as a Research Director"**, matching the book's
    second-person voice rule and the CRC proposal's ToC. EN only; PT/ES
    still carry the third-person title. Identity is unchanged and must
    stay so: the file
    `part1-research-with-ai/02-the-student-as-research-director.qmd`, the
    companion `ch02_the_student_as_research_director.ipynb`, and the
    `url_path` keep the old slug (D35 P9 — a rename or URL move fails the
    build). Translate the display title only.

20. **D48 attribution pass (2026-08-05).** The plagiarism-risk audit's
    corrections were applied to ENGLISH ONLY; PT/ES still carry the
    uncredited text and must replay every item when the freeze lifts:
    - **Point-of-use framework credit** where each pathway is first
      taught: ch11, ch12, ch13, ch15 gained an opening sentence naming
      RDSS's design library; ch14 gained the sentence saying prediction
      is EDR|AI's own fifth pathway, extending rather than adapting it.
    - **MIDA credited to its authors** at first teaching in ch9 and
      ch16 (Blair, Cooper, Coppock & Humphreys), and **diagnosand**
      credited as their coined term in ch10.
    - **Two definitions widened for fidelity** in ch9: the data strategy
      now includes measurement, the answer strategy now includes
      uncertainty and interpretation. ch16's one-line MIDA gloss matches.
    - **ch11's four groups are no longer "nested"** — the frame can miss
      eligible units and carry ineligible ones and duplicates, with the
      Groves citation moved up to the definitions.
    - **ch5**: the surprise definition reworded away from the *Science*
      essay's own phrasing, and an adaptation credit added under the
      Einstein/Zahavy cycle diagram.
    - **ch27** cites WCAG 2.2 for the accessibility standard (Crameri
      keeps the color-vision evidence); **ch31** separates what ICMJE
      requires (tool + purpose) from the book's own verification column;
      **uncertainty-foundations** gained the RDSS inquiry/estimand
      lineage sentence.
    - **Generated pages** (from `planning/BOOK_STATIONS.yml`): Studio 1's
      milestone reason names Tom Zahavy and cites the position paper;
      Studio 4's milestone reason credits MIDA and the
      declare-and-diagnose loop; the MIDA step carries a parenthetical
      credit; "diagnosands" was replaced by plain language in the
      produces line and the Milestone 4 rubric
      (`planning/BOOK_ASSESSMENTS.yml`).
    - **New bibliography records** to localize: `blair2019declaring`
      (APSR, CC BY 4.0) and `w3c2024wcag22`; the `blair2023rdss` note no
      longer says EDR|AI "translates" RDSS.
    - **Three new generated figures** (`scripts/build_book_concept_figures.py`):
      `mida_map.png` (ch9), `diagnose_loop.png` (ch10),
      `sampling_groups.png` (ch11). PT and ES label dictionaries are
      already written in the script; rerun it with the freeze lifted and
      the localized figures build themselves.

## C. Verification required before the freeze lifts

12. **Human PT/ES methods review** — required by round 4: an English
    substring scanner cannot certify translated meaning; a human methods
    reader per language signs off on ch06/09/10/12/13/14/15/18/21/22/25/32 at
    minimum. Davi schedules this.
13. **Misconception gate over PT/ES** — extend/verify
    `planning/MISCONCEPTION_MANIFEST.yml` translated `rejects` families
    against the resynchronized text; `validate_misconceptions.py` green.
    Round-4 G4 addition: the `numbers:` evaluator must gain PER-EDITION
    claims — PT/ES numeric prose AND localized alt text for ch14/ch15/ch22
    (and any new seeded figure) — so a decimal-rendering drift in one
    language fails on its own.
14. **Sync validator over all three editions** — `validate_book_sync.py`
    restored to three-edition scope (EN-only scope during the freeze).
15. **Remove the freeze apparatus** — delete the development notices from
    both `_lang-switcher.html` files, restore any EN-page language buttons
    repointed to the PT/ES index (Phase 3) back to per-page counterparts,
    restore CLAUDE.md §6 to the resynchronize-on-every-edit rule, and mark
    this file CLEARED with the closing commit hash.

---

## D. Verification queue (not translation — logged here for visibility)

**Regulatory anchors for the ethics lesson, UNVERIFIED by the assistant.** A
partner run retrieved and quoted primary sources (US Common Rule §46.101/.102/
.116 on eCFR; EU GDPR Arts. 3–6, 9, 28, 32, 89 + Recitals 26/159 on EUR-Lex;
Canada TCPS 2 Introduction and Chapters 2–3) supporting four claims: that
course-based student research is expressly in scope in at least one national
framework; that intent to publish is not the test; that a public-information
exemption can require BOTH public availability and no reasonable expectation
of privacy; and that "processing" includes disclosure by transmission.

The assistant could NOT independently retrieve these (ethics.gc.ca returned a
certificate error; ecfr.gov redirected to an unblock page), so **no regulatory
text or citation was added to the chapter**. The chapter teaches the
principles jurisdiction-generally instead, which is correct either way.

If Davi wants the chapter to name and cite frameworks — which would strengthen
it — the sources must be retrieved and read first. The partner transcript with
its quotes and URLs is at
`_adm/codex_collab/2026-07-31_ethics-lesson/partner_raw.txt`.

**Review round (2026-08-05).** Codex reviewed the D48 pass: 12 findings applied (see DECISIONS D48 review round). New EN-only items to replay in PT/ES beyond item 20 above: the corrected MIDA figure row labels ("what you want to learn" / "how you will learn it" — PT/ES strings already in the figure script), the redrawn sampling figure with undercoverage / overcoverage / duplicate (PT/ES strings also in the script), ch11's three coverage terms, ch5's audience-level surprise framing, ch10's corrected RDSS subtitle, ch27's WCAG web-scope qualification, Studio 5's route-table credit, and the ch9/ch10/ch16 "It is your turn" credit sentences.

**Dataset bundle renamed (2026-08-23).** The student dataset bundle is now
`notebooks/data/data.zip` (was `honr46400_datasets.zip`), and its members are
stored under `notebooks/data/` inside the archive so the offline fallback in
`load_course_data()` resolves. The English `book/for-instructors.qmd:51` link
was repointed; the frozen translations still name the old file and must be
updated when the D36 freeze lifts:

- `book-pt/for-instructors.qmd:52`
- `book-es/for-instructors.qmd:54`
