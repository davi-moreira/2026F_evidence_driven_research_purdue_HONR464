# COURSE_REFRAME_OPTIONS — matching the course to the Twelve Studios

**RULED (Davi, 2026-08-03): Option 2 adopted — see the D40 revision section
at the end and the D41 implementation record in `_project_docs/DECISIONS.md`.**

Prepared 2026-08-03 by the two-track
loop: an independent Codex partner run (mirror mode, gpt-5.6-sol, xhigh, no
seeding) and an independent Claude analysis, verified against each other and
merged. Run artifacts:
`_adm/codex_collab/2026-08-03_course-reframe-studios/` (options),
`_adm/codex_collab/2026-08-03_option2-implementation/` (implementation
blueprint + review).

**The question (Davi's):** the book is now the Twelve Studios (D38). Reframe
the course to follow it — the course is conditioned on the book, never the
reverse. Goals: (1) match the week topics to the new studio structure,
(2) hands-on activities every day, (3) build in the **AI-simulated flawed
colleague**: once each student's research goal is declared, Davi uses Claude
to simulate a colleague working essentially the student's own project through
the book — poster and artifacts included — **with seeded errors**; students
advance through the course reviewing the colleague's steps while developing
their own research.

---

## Facts every option must survive (verified in the repo)

1. **The checkpoint skeleton already aligns.** `COURSE_BOOK_CROSSWALK.yml`
   already fires all 12 studio checkpoints in studio order across M0–M15
   (S1→M0 … S12→M15). Both tracks independently concluded the same thing:
   **M0–M15 are dated course wrappers around the book's checkpoint
   versions**, and the reframe is about the VISIBLE spine (week identity,
   milestone naming, daily activity grain) — not about inventing a mapping.
2. **The Expo inversion is external, immovable — and book-licensed.** The
   Expo (Tue Nov 17; poster locked Fri Nov 6, 5 PM) forces Studio 10's
   poster branch before Studios 9 and 11 close at M14. The book's own A8
   release gate permits "a preliminary presentation … only when labeled
   preliminary", and the crosswalk's blocking reproduce-before-publish gate
   (M10) already enforces clean reproduction of whatever the poster claims.
   The course deviation is stated in the book's own vocabulary: **the Expo
   poster is a labeled-preliminary genre adaptation of a versioned claim**,
   revisited and finalized after the conference. (Caution, Codex: Purdue's
   public program confirms the Nov 16–20 Expo week but not the exact Tuesday
   session or the Nov 6 lock — confirm both from organizer communication.)
3. **The vocabulary collision is now live.** D38 chose "Studio" for the
   book knowing the course calls Fridays "Friday studio." The course must
   either lean in (Friday = studio time — the day the current Studio's
   checkpoint is assembled) or rename Fridays. Lean-in converts the
   collision into coherence.
4. **The daily hands-on inventory already exists.** `BOOK_STATIONS.yml`
   enumerates **52 workbook steps** (4/4/4/6/4/5/4/5/4/4/4/4) against 43
   meetings. Every meeting can own ≥1 named step inside the EXISTING
   50-minute frames — no frame change, no new activity content invented,
   and "hands-on every day" becomes validator-checkable (each session
   guide names its step ids).
5. **Studio 5 is the structural question.** The book says commit to YOUR
   pathway (5 branch lessons + optional hybrid); the course teaches all five
   as topic weeks W5–W9. With ~5 students on potentially 5 different
   pathways, shared weeks are what make the common quiz and the SRL system
   work — and comparative pathway literacy is a course ADDITION the book
   permits (the course may add; it may not contradict).
6. **Two integrity gates bind the colleague device.** A2: nothing about the
   colleague may enter book surfaces (chapters, studio pages, workbooks) —
   course artifacts only. **D16: no planted fake citations, even as a
   teaching device** — the "fabricated citation" error the device first
   imagined is prohibited; the compliant substitutes are a REAL but
   claim-mismatched citation, an unverified AI suggestion left unresolved,
   or a live AI output the student must try to verify. (Codex's catch.)
7. **Stale projections found while checking claims** (pre-work regardless
   of the ruling): `course_config.yaml` (lines 7, 250) and
   `COURSE_MASTER_PLAN.md` §8 still describe a "37-chapter/six-part" book;
   `ASSESSMENT_ARCHITECTURE.md` still carries the pre-D31 seven-component
   15%-SRL scheme while `course_config.yaml` rules 1/9/20/20/20/20/10;
   `BOOK_ASSESSMENTS.yml` still says `status: skeleton-revised` despite
   authored criteria; `BOOK_ARCHITECTURE.yml` still marks workbooks
   `pending` although `book/studios/` ships them.

---

## Option 1 — Checkpoint-repair overlay  ← both tracks' Fall 2026 pick

The semester is PRESENTED as the book's twelve Studios run as sprints; the
16-week machinery underneath keeps its identity (nb01–nb16 and M0–M15 stay
as file/Brightspace ids, each milestone subtitled by the checkpoint it
fires). **Three repairs are mandatory — without them this is relabeling,
not reframing** (Codex's formulation, endorsed):

1. **Studio 5 declares in Week 5.** M4 carries `pathway-declared-v1`;
   Weeks 6–9 become named **contrast/revisit clinics** (the declared
   pathway deepens; the other lenses are studied as contrasts, exactly the
   comparative literacy the compass drills need).
2. **Studio 9 produces a one-page bounded research-note v0 BEFORE poster
   adaptation** (Week 10) — the book's dossier-first order holds even with
   the Expo; the poster adapts a bounded claim that already exists.
3. **Studio 11's author self-reproduction and a Studio 12-style release
   preflight run before the Nov 6 poster lock** (the M10 gate already
   half-wires this).

### Sprint table (calendar verified; assignments proposed)

| Week | Meetings | Studio (sprint) → checkpoint (milestone) | Colleague beat |
|---|---|---|---|
| 1 | m1–3 | **S1 Govern the work** → `working-agreement-v0` (M0) | shared "Case 464" calibration; no individual colleague yet |
| 2 | m4–6 | **S2 Frame the inquiry** → `question-declared-v0` (M1) | student-approved synopsis collected at declaration |
| 3 | m7–8 | **S3 Ground in evidence** → `evidence-base-v0` (M2) | colleague released; evidence-boundary audit |
| 4 | m9–11 | **S4 Declare & diagnose** → `contract-v0` (M3) | Contract v0 audit |
| 5 | m12–14 | **S5 pathway hub** → `pathway-declared-v1` (M4) | wrong-pathway / wrong-warrant audit |
| 6 | m15–17 | S5 clinic: observational-causal contrast (M5) | identification / adjustment-set audit |
| 7 | m18–20 | S5 clinic + **S6 data & measurement** → `data-measurement-v1` (M6) | provenance / reliability audit |
| 8 | m21–22 | S5 clinic: prediction + **S7 launch** (M7) | leakage / protocol audit |
| 9 | m23–25 | S5 clinic: experimental-causal + **S7** → `first-analysis-v1` (M8) | result / uncertainty / restart audit |
| 10 | m26–28 | **S8 stress-test** → `robustness-audit-v1` + **S9 note v0** (M9) | robustness audit; claim-upgrade detection in the note |
| 11 | m29–31 | **S10 poster branch** + S11 self-reproduction gate + release preflight → M10 **poster lock** | flawed-poster audit |
| 12 | m32–34 | **S10 talk/defense branch** → `defense-ready-v1` (M11) | colleague fields difficult questions with an unjustified upgrade |
| 13 | m35–36 + Expo | S10/S12 revisit: rehearsal, public test, reflection (M12) | how the colleague reacts to public criticism |
| 14 | m37 async | **S11 reproduce & package** — peer cold-run practice (M13) | reproduce the colleague package alongside the peer task |
| 15 | m38–40 | **S9 + S11 close** → `bounded-claims-v1` + `package-v1` (M14) | repair the colleague note/package, transfer the check |
| 16 | m41–43 | **S12 release & next cycle** → `release-audit-v1` (M15) + final defense | stopping-rule / false-consensus audit, then close the real dossier |

### Daily hands-on pattern (D22/D33/D34 frames untouched)

- **Monday:** the SRL's 0–9 puzzle usually opens from a colleague artifact
  fragment; 9–31 sets the book's correct worked example against it; 31–43
  verifies and repairs; 43–50 transfers the rule to the student's own
  project (ledger + Claim Ticket as today).
- **Wednesday:** retrieval uses a fresh colleague claim; the 7–30 lab
  advances the student's own checkpoint (named workbook step of the day);
  30–38 peer defense includes colleague interrogation; 38–42 the accuracy
  lock debriefs the answer key; 42–50 checkpoint revision.
- **Friday (studio time, lean-in naming):** unchanged 10/5/30/5 — quiz,
  stand-up, own-project checkpoint production, ledger + submission. The
  colleague consumes no Friday production time beyond one transfer-oriented
  quiz item in a NEW context (never the colleague's wording).

**Changes:** milestone briefs (16, re-anchored to `#checkpoint` pages and
the authored studio rubrics), schedule_data + regenerated guides, notebook
framing cells (via nb_sources + nbbuild), quiz distractors, SRL briefs,
crosswalk annotations, syllabus/material page. Book files: zero.
**Cost:** ~7–12 maintainer-days [Codex estimate, unverified] + colleague
infrastructure. **Risk:** Weeks 5–9 still read as a braid (S5+S6+S7);
countermeasure is showing checkpoint chronology explicitly — declared in
W5, deepened in clinics, versioned at M8.

## Option 2 — Studio-first, route-selective semester

The cleanest expression of D38: Studio 5 becomes ONE route-selection week
(student reads their branch + one mandated contrast; class time runs a
five-route jigsaw), freeing dedicated weeks for S6 (W6), S7 (W7–8), S8
(W9), S9 (W10) — the rest as in Option 1. Rewrites nb05–nb10 substantially
(lighter nb11–nb16), W5–W12 quiz banks, SRL briefs, the full crosswalk.
**Cost:** ~18–30 maintainer-days [unverified]. **Risks:** less universal
pathway breadth; the instructor manages five simultaneous branches in W5;
with ~5 students the common quiz and peer-SRL coherence thin out (Claude's
decisive concern); the pre-Aug-24 build window is tight. **Standing:** the
better long-term architecture — adopt only with an explicit rebuild
authorization, or hold for a future iteration.

## Option 3 — Forensic Studio apprenticeship (Codex's; pilot only)

Makes correct-example → colleague-audit → own-project-transfer the
recurring Mon/Wed architecture, with amended frames and a separately
weighted **Verification Practicum** (10%, quizzes 20→10). Reopens settled
rulings (D22/D33 frames, D22 weights) and carries the inversion risk both
tracks flag: **the synthetic colleague becomes the center and the real
project becomes the transfer exercise** — the reverse of the intended
hierarchy. Standing: documented; at most pilot its meeting pattern in two
studios before any adoption.

---

## Tradeoff table

| | Opt 1 Overlay+repairs | Opt 2 Route-selective | Opt 3 Forensic |
|---|---|---|---|
| Matches "just match the weeks to the book" | yes | yes, deepest | yes |
| Hands-on every day | yes (52 steps + audits in frames) | yes | yes (audit-centered) |
| Book order honored | via repairs + labeled-preliminary Expo | fully | via repairs |
| Reuses authored course content | nearly all | rebuilds nb05–nb10 | rebuild + new frames |
| Rulings it reopens | none | route-selective reading | frames + weights |
| Fits 5-student SRL/quiz machinery | yes | strained | strained |
| Migration cost (unverified) | 7–12 days | 18–30 days | 25–40 days |
| Colleague-device fit | audits inside existing blocks | same | device becomes the course |

---

## The Synthetic Colleague — one device, pluggable into any option

**Identity.** Instructor-issued, AI-assisted practice case: a named
colleague persona per student, working a **near-isomorphic project** (the
student's own goal, per Davi's intent) on **synthetic or separately
verified open data** — never the student's real observations. Every
artifact carries a permanent "simulated case" banner. Candidate
student-facing names: "your AI colleague, \<Name\>" (Claude) or "Synthetic
Colleague Dossier" (Codex, arguing it cannot be read as mocking a real
peer). Copying the colleague is self-punishing by design — its work carries
seeded flaws, and milestone criteria require the student's own sources,
decisions, and verification.

**Staged launch (Codex, endorsed).** W1: one SHARED "Case 464" so the
instructor models confirm/challenge/repair and discloses the simulation.
After `question-declared-v0` (M1): collect a student-approved minimal
synopsis (objective, units, outcome, kind/reach, claim boundary, broad data
route — no raw data, nothing identifiable). W3: individualized colleagues
release. After Studio 4: a workload-and-confusion check — continue,
simplify, or suspend on observed evidence.

**Generation workflow (per sprint, not all 12 in advance).** Input: the
previous colleague checkpoint, the studio spec + step list, ONE selected
error family, permitted real sources, SEED=464. Output: (a) the
student-facing checkpoint artifact, visibly marked simulated; (b) a private
instructor key — seeded error, artifact locator, target rubric criterion,
expected evidence, correction, provenance, likely false positives. **Davi
verifies before release**: every cited source exists, every deliberate
numerical error behaves as intended, no accidental second defect. Correct
anchor first: students meet the book's correct worked example before the
flawed artifact whenever the concept is novel. Pivots regenerate forward
only, with version history kept. Workload estimate: ~4–6 h initial
creation, ~60–100 min per studio batch, ≈16–26 h/semester [unverified].

**Per-studio error menu** (one intended major flaw per artifact, count
undisclosed, plus correct-but-suspicious elements; keyed to
`MISCONCEPTION_MANIFEST.yml`, the 60 studio rubric criteria, and the named
crossing violations):

| Studio artifact | Seedable flaws (examples) | Registry hook |
|---|---|---|
| 1 working agreement | delegates a never-delegate decision; ledger row without verification | never_delegate; rails |
| 2 declared question | causal question relabeled descriptive because data are weak; silent reach upgrade | `compass-relabeling`; claim_upgrades |
| 3 evidence base | real source doesn't support the attributed claim; AI suggestion treated as verified; hidden failed searches | evidence rail (D16-compliant — no invented citations) |
| 4 contract v0 | bias as "average distance"; "80% power" with no test/threshold; permission "cleared" without an authority | `signed-bias`, `power-needs-a-rule`; permission gate |
| 5 pathway | confounded design presented as identified; adjust-for-everything; assignment treated as automatically causal | `adjustment-set`, `compass-relabeling` |
| 6 data & measurement | reliability splits respondents not items; provenance from memory; route change without permission recheck | `reliability-splits-items`; rails |
| 7 first analysis | analysis differs from the Contract; point estimate without uncertainty; no clean restart | station rubric; uncertainty rail |
| 8 robustness | "effect among stayers"; same-sign specs called robust; spec spread read as an interval; exact-zero criterion | `attrition-stayers`, `specification-spread`, `exact-zero` |
| 9 bounded claims | quiet causal/population upgrade; claim without a claim-evidence row; disclosure reconstructed from memory | claim_upgrades; S9 rubric |
| 10 genre adaptation | poster drops a limitation; untraceable figure number; pitch expands the claim; AI answers the defense | rails; `decision-owned` |
| 11 package | LOCF over post-treatment death as "neutral"; "AI cannot execute code"; point estimate reproduces but uncertainty doesn't | `locf-truncation`, `ai-cannot-execute` |
| 12 release | outcome-dependent stopping rule; multi-agent agreement treated as independent verification | rails; permission gate |

**In-class audit protocol** (18–22 min inside the existing Monday
investigation or Wednesday lab): commit (2′: each claim `supported` /
`unsupported` / `uncertain`) → locate (3′: exact sentence/cell/figure) →
verify (6–8′: retrieve the source, rerun the code, apply the book rule) →
diagnose (3′: name the misconception/crossing/criterion) → repair (3′:
smallest defensible correction + new boundary) → **calibrate** (2′: defend
one element that looked suspicious but is sound) → accuracy lock (2′: SRL
synthesizes, instructor corrects the record).

**Assessment (Options 1–2).** Audits score on a compact 4-row 0–2 rubric
(locator+verdict · rule+evidence · repair+boundary · **calibration** —
false positives cost points, which is the anti-"AI-is-always-wrong"
mechanism). Best 10 of 12 count **inside participation (9 pts)**, replacing
the generic AI-output interrogation rather than adding homework — milestone
grades stay exclusively about the student's real checkpoints (Codex's
placement, adopted over Claude's fold-into-milestones alternative because
it keeps the real-work hierarchy clean). AI used during an audit is logged
in the existing AI Research Ledger; no new dossier vocabulary.

**Safeguards.** Correct anchor first + same-session repair (students must
not encode the error); clean traps + scored false positives (no
pattern-matching); simulation banner + syllabus disclosure (integrity
optics); instructor-verified source registry (D16); minimal synopsis +
synthetic data (privacy); one flaw per artifact with early highlighted
regions, faded later (novice load); regenerate-forward on pivots
(workload); never enact unauthorized collection — faulty permission
DECISIONS are simulated on safe data (ethics).

**Evidence base (every entry independently verified by both tracks).**
Erroneous worked examples improve learning, with two firm caveats the
design already encodes: benefits concentrate on delayed/transfer measures,
and low-prior-knowledge learners need correct anchors and highlighted
errors first.

- Große & Renkl (2007), *Learning and Instruction* 17(6):612–634 —
  doi:10.1016/j.learninstruc.2007.09.008 (prior-knowledge caveat).
- McLaren, Adams & Mayer (2015), *IJAIED* — doi:10.1007/s40593-015-0064-x
  (delayed-test advantage of find-explain-fix).
- Adams et al. (2014), *Computers in Human Behavior* —
  doi:10.1016/j.chb.2014.03.053.
- Booth, Lange, Koedinger & Newton (2013), *Learning and Instruction*
  25:24–34 — doi:10.1016/j.learninstruc.2012.11.002 (correct + incorrect
  examples with self-explanation).
- Atkinson, Renkl & Merrill (2003), *JEP* 95(4):774–783 —
  doi:10.1037/0022-0663.95.4.774 (faded scaffolds).
- Butler & Roediger (2008), *Memory & Cognition* 36:604–616 —
  doi:10.3758/MC.36.3.604 (feedback prevents lure intrusion → the
  never-leave-an-error-uncorrected rule).
- Sun et al. (2015), *PLoS ONE* — doi:10.1371/journal.pone.0143177
  (peer assessment gains from producing evidence-grounded reviews).

**Honest boundary (both tracks + Codex's dead-end log):** no direct
empirical study exists of a semester-long, AI-personalized flawed colleague
shadowing individual undergraduate research projects. The evidence is
adjacent (math, algebra, decimals, statistics classrooms); transfer to
research-design dossiers is an inference — which is exactly what the
post-Studio-4 continue/simplify/suspend check is for.

---

## RECOMMENDATION (both tracks, convergent)

**Option 1 with the three mandatory repairs, plus the Synthetic Colleague
at standard intensity (Mon/Wed beats + audit scoring in participation;
Fridays protected for real production).** Option 2 stands as the tested
end-state candidate for a later iteration — the same now-vs-later shape as
D38 itself. Option 3 contributes its audit protocol and rubric (adopted
into the device) but not its architecture.

Pre-work regardless of the ruling: reconcile the stale projections in fact
7 (course_config/COURSE_MASTER_PLAN book description, ASSESSMENT_ARCHITECTURE
weights, BOOK_ASSESSMENTS status, workbook flags).

## The decisions that are genuinely Davi's

1. **Fall 2026 architecture:** Option 1 (recommended) or authorize the
   Option 2 rebuild (nb05–nb16, quiz banks, SRL briefs)?
2. **Studio 5 reading:** all five branch lessons for everyone (status quo,
   recommended with the clinics) or route-selective (own branch + one
   contrast)?
3. **Colleague grading:** inside participation (recommended) or Option 3's
   separate 10% Verification Practicum (reopens the weights)?
4. **Student-facing name:** "your AI colleague \<Name\>" or "Synthetic
   Colleague Dossier"?
5. **Friday naming:** lean in — Friday = studio time in the current Studio
   (recommended) — or rename Fridays to avoid the collision?
6. **Milestone identity:** keep M0–M15 with checkpoint subtitles
   (recommended) or renumber to the 12 checkpoint ids?
7. **Consent & storage:** may Claude receive each student's approved
   question synopsis, and do colleague artifacts + keys live in the private
   instructor repo?
8. **Dates:** confirm the exact Expo session (Tue Nov 17) and the Nov 6,
   5 PM lock from organizer communications (public Purdue material confirms
   only the Nov 16–20 week).

---

## Revision after D40, and the ruling (2026-08-03)

The book moved again after this memo was written. **D40** closed every
studio with a generated **Milestone chapter** — the book now carries its own
numbered milestone chain, **Milestones 1–12**, with artifact-first titles
("Milestone 2: Your question, declared"), a "What you bring" checklist, the
practice steps, the rails, the authored rubric, and the workbook badge.
`BOOK_STATIONS.yml` gained four authored fields per studio
(`milestone_title`, `milestone_reason`, `hands_forward`, and a
per-lesson `contributions:` map naming the exact "It is your turn" piece
each lesson hands its milestone), validator-gated.

**What D40 changes in this memo's analysis:**

1. **The course's anchor problem is solved by the book itself.** Every
   course submission can now open from a book Milestone chapter instead of
   a course-invented artifact description. The naming bridge becomes:
   course submissions keep their M0–M15 ids (Brightspace/calendar
   identity) and each presents a **book Milestone version** — 16
   submissions over 12 book milestones, with M6+M7, M9+M14, M10–M12, and
   M13+M14 carrying successive versions/events of Book Milestones 7, 9,
   10, and 11 respectively.
2. **Open question 6 (renumber the milestones?) is largely answered by
   the book**: keep M0–M15 as submission ids; the book's Milestone 1–12
   numbering is the student-facing arc. The For Instructors appendix
   already disambiguates the two.
3. **The `contributions` map feeds the briefs.** Book Anchor sections can
   now state not just which chapters a milestone reads but WHICH IYT piece
   each chapter hands the milestone — the anchor generator gains a richer
   source.
4. **Two D40 integrity fixes sharpen the Option 2 week split**: Contract
   v0 (Week 4) carries a *provisional* operationalization with measurement
   assessed in Studio 6 (Week 6), and Studio 12's stale-run gate widens
   the release-preflight requirement Option 2's Repair 3 already imposed
   before the poster lock.
5. **A2 note:** bare "Milestone N" is now BOOK vocabulary; the leakage
   scanner bans only course-CODED forms (`milestone M4`, `M4 brief`,
   `milestone_04`) in book surfaces. The colleague device and all course
   artifacts remain course-side only.

**The ruling.** Davi ruled **Option 2 — Studio-first, route-selective
semester** (not the Fall-2026-conservative Option 1 both tracks had
ranked first; the deciding argument was the one this memo already
recorded: Option 2 is the cleanest expression of D38, and choosing it
now avoids teaching one structure while the book argues another). The
implementation is phased — structure first (crosswalk, master plan,
milestone chain, config: **D41**), then content (briefs, schedule data,
quiz banks, SRL briefs, nb05–nb10 rebuild), then the Synthetic Colleague
infrastructure. Option 2's route-selective reading resolves open question
2: each student's pathway lesson is **route-required**, the other four
branches join the route-hub jigsaw with one mandated contrast, and
`hybrid-complex-designs` moves from blanket-required to recommended (a
recorded course-policy change).
