# BOOK_STRUCTURE_OPTIONS — should the lessons live inside the stations?

**For Davi's ruling (would be D38).** Prepared 2026-08-03 by the two-track
loop: an independent Codex design run (mirror mode, no seeding) and an
independent Claude analysis, verified against each other and merged; then an
adversarial critique of this memo — its verdict and the resulting revision
are in the final section. Nothing here is implemented.

**The question (Davi's):** the book has 6 parts, 39 chapters, 12 practice
stations. For a learning-by-doing undergrad textbook with AI as partner,
should the 6 parts / 39 chapters be embedded INSIDE the 12 stations? Goal: a
business/econ/polsci/biology undergrad produces high-level research
artifacts by completing the book.

**Both tracks converged on yes — embed.** They differed on one design point
(ch33's home, resolved below) and the merged recommendation is stronger than
either track alone.

---

## Facts every option must survive (verified in the repo)

1. **The lesson→station map is already a perfect partition.** 39 lessons,
   each in exactly one station; sizes 4/2/2/4/6/2/2/4/4/4/2/3.
2. **A TOC restructure changes ZERO urls.** Quarto parts are display
   groupings; a part can be a page (Part I's overview already is). Lesson
   ids, url_paths, and companion paths stay untouched, so the identity
   epoch is satisfied — the A10 machinery was built for exactly this move.
3. **Station-first relocates exactly TWO lessons** (disclosure and the
   research note), which changes seven display positions in the Parts V–VI
   region — and every change enacts what D35 already ruled:
   disclosure (ch31) and the note (ch33) come BEFORE the genre adaptations
   (posters ch27–28, pitches ch29), Difficult Questions (ch30) comes after
   a chosen genre exists, and replication/packaging (ch32+ch34) reunite in
   Station 11. The current 6-part order silently preserves the course's
   poster-first history against the book's own dossier-first ruling (A3).
4. **The cold pilot (2026-08-01) hit this exact seam**: "the two-grain
   structure works conceptually yes, operationally no" — Next links carried
   the reader through 39 chapters while the stations read as a second book
   at the end.
5. **Display chapter numbers are derived labels** (ruled in the Phase-2
   schema review). Renumbering ch29–35 regenerates every projection
   (briefs, BOOK_MAP, material page, adoption table) mechanically; the
   course crosswalk keys off lesson ids and is unaffected.
6. **Quarto book parts cannot nest** — but Quarto DOES support custom
   sidebar sections with nested navigation independent of the part
   structure, which means a station-grouped sidebar is achievable WITHOUT
   making stations into parts (this fact is what enables Option 5 below).

---

## The options

### Option 1 — Twelve Studios containing the lessons  ← RECOMMENDED

The stations become the book's parts. Each studio is a complete
read-a-little/do-a-lot unit:

```
Studio 4 · Declare and Diagnose            <- opener = existing station page
  Ch — MIDA                                   (purpose · the artifact you
  Ch — Uncertainty Before You Need It          will produce · the road ahead)
  Ch — Declaring and Diagnosing a Design
  Ch — Research Ethics and Data Governance
  Checkpoint: Contract v0                  <- generated closer (steps · rubric ·
                                              workbook badge · write version)
```

Top level of the whole book: front matter → 12 studios → appendices. The
six-part narrative survives as an intellectual map in the overview and as
cosmetic arc prefixes if wanted ("Found 1–3 · Design 4–5 · Evidence 6–8 ·
Deliver 9–12") — never a navigational level.

- **Rhythm:** brief → read → do → checkpoint, enforced by structure instead
  of taught in the preface.
- **Branching becomes legible:** Studio 5's opener presents the five
  pathways as a choice (route cards), so a prediction reader no longer
  wades past four chapters that are not theirs; Studio 10 does the same for
  genres.
- **Completion promise:** *twelve studios, twelve versioned artifacts, one
  defensible research project* — with the two honest outcomes stated:
  authorized-data route → a bounded empirical claim with uncertainty and a
  reproducibility package; public/synthetic route → a full demonstration of
  the method and apparatus, explicitly not a claim about the world.
- **Naming (Codex's point, endorsed):** "practice station" sounds
  supplementary; "**Studio**" reads as the primary unit. Display titles are
  mutable; station ids stay immutable slugs either way. Naming is Davi's
  call — Station and Studio both work structurally.

### Option 2 — Keep the six parts, weave the stations in

Insert each station page after its last lesson inside the existing parts.
Cheapest and it keeps the 6-part narrative — but Stations 9/10/11
interleave ACROSS Parts V–VI, so threading them cleanly requires the same
7-lesson resequencing as Option 1, at which point you have paid Option 1's
price and kept two competing structures. The pilot's "which grain am I in?"
confusion survives. **Dominated by Option 1.**

### Option 3 — Project path + field guide (lab-manual model)

A lean 12-station project path up front; the 39 lessons demoted to a
just-in-time reference "field guide" behind links. Attractive for
instructors and experienced readers; **weakest for the actual audience** — a
novice alone with a browser is asked to jump continuously between a project
book and a reference book, which is the pilot's split reversed, not fixed.

### Option 4 — Full merge (12 mega-chapters)

Dissolve the lessons into station chapters. **Rejected**: destroys or hides
lesson urls, makes Studio 5 a ~15k-word monolith, kills the reading
modularity D35 deliberately created, leaves per-lesson companions homeless.

---

## Tradeoff table

| | Opt 1 Studios | Opt 2 Weave | Opt 3 Path+Guide | Opt 4 Merge |
|---|---|---|---|---|
| Navigation for a novice | one spine, 12 units | two grains remain | constant jumping | one spine, huge units |
| Learning-by-doing rhythm | enforced | partial | do-first, read-maybe | enforced |
| Route/genre legibility | choice inside studio | buried in parts | good | buried in mega-chapter |
| Enacts D35's A3 ordering | yes | only if resequenced | yes | yes |
| Identity/urls | unchanged | unchanged | unchanged | broken/hidden |
| Migration cost | TOC + 7 ranks + generators | same resequencing + less payoff | new nav layer | prohibitive |
| Trade pitch | "12 studios → 1 project" | "39 chapters" | "manual + reference" | "12 long chapters" |

---

## Pre-migration fix both tracks endorse (one found it, one adjudicated it)

**ch33 is inconsistent in the manifest**: it carries `genre: note` +
`role: branch` while sitting in Station 9 — and the `note` token sits in the
genre registry as a Station-10 branch. D35's own table settles it: Station
9's checkpoint IS "a stand-alone research note draft". The note is the
**core artifact**; poster/pitch/brief are adaptations of it (A3). Fix:
ch33 → `role: core`, genre token removed; registry keeps poster/talk (add
`brief` only when a brief lesson exists). The display title becomes "From
Dossier to Research Note" (mutable; url unchanged).

## Migration sketch for Option 1 (what changes / what provably doesn't)

**Changes:** `_quarto.yml` becomes GENERATED from the manifest (new
`build_book_toc.py` — closing the last hand-maintained ordering source, as
the Phase-2 critique already asked); re-rank the 7 moved lessons (ranks are
mutable by design); split station output into opener (existing page, url
kept) + generated Checkpoint closer; make companion-notebook **Next links
station-aware** (a branch lesson's Next returns to its studio, never chains
a prediction reader into the experimental-causal lesson — Codex's sharpest
risk catch); reword lesson pointers from "this work feeds Station N" to
"you are working inside Studio N"; preface two-grain section rewritten;
ch33 manifest fix above.

**Provably unchanged:** every lesson id, url, companion path (identity
epoch enforces it); the course crosswalk and all 16 notebooks; the
misconception gate and its surfaces; PT/ES (frozen; divergence widens as
already accepted and noticed on-page).

**Riskiest steps:** branch-aware navigation; opener/closer split without
duplicate or orphan pages; the Studio 9/10/11 boundary (disclosure earlier,
note as core, reproduce-before-release preserved) — test the three genre
paths separately. **Then a second cold pilot on the restructured spine.**

**Bookkeeping:** this is D38; architecture goes v2; the v1 freeze (D37, two
days old) reopens for the structure only — chapter review continues, since
lesson CONTENT is untouched by the restructure.

---

## Recommendation (both tracks, independently)

**Option 1.** Embed, exactly two navigational levels (studio → page), the
six parts demoted to an intellectual map, ch33 fixed to core-note first,
branch-aware navigation, TOC generated, second cold pilot after migration.

One caution both tracks flagged: **embedding fixes wayfinding, not the A4
gap** — station workbooks still need worked examples, starter data, and
faded scaffolds before the completion promise is real. The restructure makes
that gap more visible, which is a feature, not a risk.


---

## The adversarial critique ruled AGAINST Option 1 (2026-08-03)

Full verdict: `_adm/codex_reviews/2026-08-03_structure-memo-critique/verdict.md`.
Its corrections are folded into the text above. The material findings:

1. **The T&F proposal constrains the timeline decisively.** The proposal
   (v2, filled 2026-08-03) states the six-part structure was frozen on
   Aug 1, schedules the ToC freeze for Aug 31, and internal submission in
   early September. Adopting Option 1 now would falsify the proposal weeks
   before submission.
2. **The migration is smaller than the memo claimed in one way** (two
   relocations, not seven) **and larger in others**: the opener/closer
   split is a schema migration, not a page split (the validator would
   reject closer pages as orphans; numbering policy is undefined); and the
   decisive branching promise needs an explicit **navigation graph**
   (entry/branch/join/checkpoint/continue edges) that the manifest does not
   yet carry — without it, twelve parts still chain a prediction reader
   into the causal pathway, in HTML and in the companions.
3. **The pilot supports the diagnosis, not this remedy.** It judged the
   two-grain concept sound and proposed boundary navigation; no evidence
   compares 12 studios against 6 parts for this audience. The
   learning-science case (problem-centred tasks, worked examples, fading)
   argues for completing the station KITS (A4), not for changing the ToC.
4. **"Studio" collides with the course's own "Friday studio"** terminology.
5. It found three live repo defects while checking the memo's claims
   (stale material/instructor projections; a hand-kept lab table in For
   Instructors still carrying pre-D35 anchors; the EN language switcher
   404ing into the frozen editions for the 14 new pages). All three are
   fixed as of this revision — independent of the ruling.

### Option 5 — the critique's counter-proposal (operational stations, six-part spine)

1. Keep the six parts as the publication/proposal spine.
2. Relocate ONLY disclosure and the note, enacting D35's order (both
   tracks want this regardless).
3. One page and one URL per station: opener + a `#checkpoint` return
   anchor — no closer pages, no schema migration.
4. Add the **navigation graph** to the manifest and generate explicit
   entry/branch/join/checkpoint/continue links for both HTML and
   companion notebooks — this, not the hierarchy, is what actually stops
   a prediction reader from being marched into the causal chapter.
5. Station-grouped custom sidebar (Quarto supports it without parts).
6. Keep the name **Station** pending reader/publisher testing.
7. Prototype-compare Options 1 and 5 at the two branch-heavy seams
   (Stations 5 and 10) with target novices before any freeze reversal.

## Revised recommendation (post-critique synthesis — Claude's, labeled as such)

The two independent tracks agree on the destination — the station journey
becomes the reader's primary experience — and disagree on whether the
PUBLICATION HIERARCHY must change to deliver it. The critique demonstrated
it does not have to yet, and that the T&F calendar punishes changing it now.

**Recommendation: adopt Option 5 now; hold Option 1 as the tested
end-state candidate.**

- **Now (before the Aug 31 ToC freeze):** the two-lesson relocation, the
  station navigation graph, sidebar grouping, checkpoint anchors, and the
  boundary Next-links (Ch 4 → Station 1 → Ch 5). This is D38 if ruled: it
  keeps every statement in the proposal true, captures most of the
  pedagogical value, and none of it is thrown away if Option 1 wins later —
  the navigation graph is prerequisite work for Option 1 anyway.
- **After submission:** run the critique's comparison protocol (Options 1
  vs 5 prototyped at Stations 5 and 10, five routes and the genre paths,
  cold novices, wrong-route clicks and time-to-next-task measured). If
  Option 1 wins with readers and the publisher, adopt it as the v3
  architecture in coordination with T&F — a 12-studio ToC may well be the
  stronger trade identity, but that is a decision to make WITH the
  publisher, on evidence, not against the proposal calendar.
- **Independent of the ruling:** completing the station kits (worked
  examples, starter data, faded scaffolds — A4) matters more for the
  book's promise than either hierarchy. Both tracks and the critique
  agree on this.
