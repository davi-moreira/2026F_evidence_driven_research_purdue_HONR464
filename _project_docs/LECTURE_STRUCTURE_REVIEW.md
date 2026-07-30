# Lecture-Structure Review — the D33 Monday/Wednesday architecture

> **⚠️ Superseded in part (2026-07-30, D34).** An independent Codex critique
> recomputed this review's measurements and audited the repository; several
> numbers and recommendations below did not survive. See the **Verification
> addendum** at the end of this document for the corrected figures, the
> recommendations withdrawn, and the rulings actually applied
> (`_project_docs/DECISIONS.md` Decision 34).

**Prepared:** 2026-07-30 · **Status:** advisory review, no rulings applied yet
**Tracks:** private task issue #18 ("Evaluate the new MW lecture structure (D33)")
**Scope:** the four-block / seven-move 50-minute MW frame as built and pushed
(`f7ef83b`, `792190e`, `7422ca1`), reviewed as a higher-education specialist
against the current evidence base on active learning and on generative AI in
instruction.

**Method:** measured the ritual density of all 27 built lectures directly from
`notebooks/student/nb*_student.ipynb`; read the generated frame cells, the
session-guide run-of-show tables, `_project_docs/ACTIVITY_TEMPLATE.md` §7, and
DECISIONS D22 / D30 / D31 / D32 / D33.

---

## Verdict

The pedagogy is right and unusually well aligned; the **notation** has outgrown
the room. Nearly every design choice sits on the strong side of the evidence —
high-intensity active learning, retrieval, prediction-before-reveal, peer
defense, and (most impressively) AI guardrails that match the only causal
evidence we have on generative AI and learning. Three problems:

1. **Wednesday generates without an expert consolidating.**
2. **The structure is expressed at too fine a grain** — a labelled transition
   every 4.4 minutes.
3. **The scaffold never fades** across sixteen weeks.

All three are fixable without touching the four blocks or the seven moves.

---

## What was measured

| | value |
|---|---|
| Lectures governed | 27 (`# Lecture N` headings across nb01–nb16) |
| Named ritual headings per lecture | **11.3 mean** → one labelled transition every **4.4 min** |
| Student production events (written + code) | **9.1 mean** → one every **5.5 min** |
| Wednesday typical | 13 named headings, 7 written responses |
| Densest lecture | **nb08-L1: 16 headings, 11 written, 8 code = 19 events in 50 min (one per 2.6 min)** |
| `💡 AI Prompt` blocks above the ⏸ line | 1.6 per lecture |
| Meetings with a named instructor-formalization block | 13 of 43 — **all Mondays; Wednesday's run-of-show has none** |

Single-lecture weeks that absorbed two lectures of content: **nb03, nb08** (and
nb13, the conference week, by design).

---

## 1. What the evidence backs (do not touch these)

**Intensity is the right bet.** Freeman et al. (2014, *PNAS*, 225 studies) put
active learning at ~0.47 SD on exams with failure rates of 21.8% vs 33.8% under
lecturing. Theobald et al. (2020, *PNAS*) show gap-narrowing of ~33% (exams) and
~45% (passing) for underrepresented students — and critically, the effect
concentrates in *high-intensity* implementations. This design is at the ceiling
of that variable. Koedinger et al. (2015) add the "doer effect": doing practice
predicts learning several times more strongly than reading or watching.

**The AI architecture is the best-evidenced part of the course.** Bastani et al.
(2024/2025) ran the field's most informative RCT: ~1,000 students; unrestricted
GPT-4 raised *practice* performance sharply but **lowered unaided exam
performance by roughly 17%** versus control — while a guardrailed tutor (hints
not answers, instructor-designed prompting) preserved gains with no harm. Fan et
al. (2025, *BJET*) name the mechanism: **metacognitive laziness** — learners
offload regulation, immediate task performance rises, transfer does not. The
🔮 commit-first, 🔁 modify-the-prompt, 🔬 interrogate, 🧑‍⚖️ AI-closed
checkpoint and 📒 ledger are, structurally, the guardrail condition generalized
into a course. Kestin et al. (2025, *Scientific Reports*) complete the picture:
a well-designed AI tutor beat an active-learning classroom on gains per unit
time — so the question is design, not presence. **The course's central thesis is
the one the literature currently supports.** Say that out loud in Week 1.

**Constructive alignment is textbook (Biggs, 1996).** 🛡️ → oral evidence
defense · 📒 → AI-management portfolio · ⚖️ → the design justification in the
chapter · 📝 → the Friday quiz · 🎯 → the poster and chapter. Most courses fail
here. This one does not.

**The retrieval spine is sound.** Wednesday's drill on Monday's decision rule
plus the Friday printed quiz gives two spaced retrievals per topic per week.
Dunlosky et al. (2013, *PSPI*) rate practice testing and distributed practice as
the only two high-utility techniques of the ten they examined.

---

## 2. Where the evidence pushes back

### ① Wednesday generates but never consolidates — highest-priority defect

Monday budgets ~6 minutes of instructor formalization. **Wednesday budgets
zero**: SRL challenge → AI lab → peer defense → transfer → ledger. Every
framework that licenses "let them construct first" requires an expert
consolidation phase after it. Productive failure is explicitly two-phase (Kapur,
2008, 2016; Loibl, Roll & Rummel, 2017 — the instruction phase is what makes the
exploration pay). Kirschner, Sweller & Clark (2006) and the worked-example
literature say novices left unguided acquire misconceptions efficiently.
Rosenshine (2012) lists "provide models" and "check for understanding" as
non-negotiable.

Wednesday has five novice students, a peer as the day's authority, and an AI
partner that is confidently wrong on a predictable schedule — and it ends by
writing the day's conclusion into a **ledger and a Claim Ticket**, i.e.
recording it as verified. That is the failure mode: an unadjudicated error
entering the permanent record with a verification stamp on it.

> **Fix (costs nothing outside the 50 minutes): retime Wednesday to
> 7 / 20 / 15 / 8.** Block 2 gives up 3 minutes (the block the as-built review
> already flags as tightest); block 3 becomes ⚖️ (3) + peer defense (7) +
> **named instructor adjudication (5)**. Additionally, move 🔬 *Interrogate the
> Output* out of block 2 and into block 3 — interrogating AI output is a
> verification act and belongs next to peer defense, not inside the lab.

### ② The grain is too fine — 11 labelled transitions in 50 minutes

This is not a working-memory claim; the frame is a repeated routine and does
automate by Week 4 (routines *reduce* extraneous load — Sweller, van Merriënboer
& Paas, 2019). The cost is **transition overhead**. A discrete named activity
costs 30–60 seconds to enter and exit — settle, read the prompt, find the cell,
regroup. At 11.3 transitions that is 6–11 minutes of a 50-minute class,
**12–22% of instructional time**, spent switching. That is arithmetic plus the
classic allocated-versus-engaged-time distinction, not a citation, and is
flagged as such.

The deeper issue: **the seven moves are verbs the student performs, and they
have been rendered as cells the student navigates.** Those are different
objects. A 2-minute spoken drill does not need its own `###` heading. And in
Monday's block 4, 🎯 + 🛡️ + 📒 + Claim Ticket are four named artifacts in seven
minutes, three of which are "state your decision and why" — from the student's
chair, the same act performed four times under different labels. That is where
**ritual compliance** starts: the artifact gets produced because it is graded,
not because it is thought.

### ③ The scaffold never fades

All 24 governed lectures run the identical 11-element frame. Expertise reversal
(Kalyuga et al., 2003) and guidance fading (Renkl & Atkinson, 2003) both say
support that helps a novice becomes redundant processing for the more competent
learner; cognitive apprenticeship (Collins, Brown & Newman, 1989) names fading
as an explicit phase. By Week 12 these students are defending a poster at a real
conference — they should not still need a labelled 🎯 cell to remember to
connect a lecture to their own project.

### ④ D33 traded away writing, which is independently evidenced

Graham, Kiuhara & MacKay (2020, *Review of Educational Research*) find
writing-to-learn improves content learning at around 0.30 SD. D33 turned ⚖️ from
a paragraph into one line and 🎯 from a spine draft into one sentence. The trade
bought room, and should not be reversed — but the fix is free: **constrain the
form instead of the length.** One line that must contain a *because*-clause and
the alternative rejected does more cognitive work than a vague paragraph.

### ⑤ Two affective risks in a five-person room

**Anxiety.** Everyone is called on every day, and every day includes defending
aloud under adversarial questioning. Cooper, Downing & Brownell (2018) and
England et al. (2017) find active-learning practices with public evaluation
raise anxiety for a meaningful minority, moderated by *predictability*, *low
stakes*, and *writing before speaking*. The identical frame supplies
predictability. But D33 made 📝 **spoken with writing optional** — removing the
write-before-speak protection exactly at the cold-call moment, and reducing
retrieval from five students to the two who answer.

> **Fix: 60–90 seconds of silent free recall, then call out.** Same 2–3 minutes.
> Everyone retrieves (Roediger & Karpicke, 2006; Kornell, Hays & Bjork, 2009),
> and the anxious student speaks from a page instead of from nothing. Highest
> benefit-to-cost ratio in this review.

**Students will report learning less.** Deslauriers et al. (2019, *PNAS*) showed
students in active classrooms learn more but *feel* they learn less, misreading
a polished lecture's fluency for understanding. In a 5-student honors seminar,
feedback surveys carry real weight. Budget 10 minutes in Week 1 to explain the
effect, and repeat it after the first quiz when they can see their own scores.

---

## 3. The recommended simplification

**Keep all seven moves. Reduce the *headings* from eleven to four, and unify the
two days into one routine with a variable third block.**

Both days already are: **Open → Investigate → Test → Close.** Only the Test
block differs. Name it once; students learn one routine instead of two.

| Block | Monday | Wednesday |
|---|---|---|
| **🧩 Open** (0–9 / 0–7) | puzzle · 🔮 predict | challenge · 📝 *written* recall then call-out · 🔮 |
| **🛠️ Investigate** (9–31 / 7–**27**) | run the study with your AI · 🔮 re-gates each reveal · 🔍 | run it live · 🔁 modify · 🔍 |
| **🔍 Test** (31–43 / **27–42**) | 🔍 verify vs the data · 📝 drill · **instructor formalizes** · ⚖️ | 🔬 interrogate · ⚖️ · peer defense · **instructor adjudicates (5 min)** |
| **🛡️ Close** (43–50 / 42–50) | 🎯 one sentence · 🛡️ · 📒 · Claim Ticket | same |

Mechanically: the move markers become **bold inline beats inside the block
sections** rather than `###` headings; code cells and answer cells stay exactly
where they are (one consolidated answer cell per block, with labelled
sub-prompts — which also puts a block's reasoning in one place for grading and
for the ledger). `validate_notebooks.py` checks for the seven markers *within*
the block, which is a one-function change. Students still see every move named,
in sequence, where it happens — they just stop navigating eleven peer-level
sections.

**Then fade it across the semester:**

| Weeks | Frame |
|---|---|
| 2–5 (nb02–nb05) | Full — four blocks, all seven beats labelled, minutes printed |
| 6–11 (nb06–nb11) | Compressed — four block headings, beats named in the frame line only |
| 12–16 (nb12–nb16) | Minimal — 🧩 open and 🛡️/📒 close remain; the middle is expected practice |

Two side benefits. **The SRL is the person who must hold the structure in
working memory while performing** — a novice teacher running an 11-element
routine gets less of the learning-by-teaching benefit (Fiorella & Mayer, 2013)
than one running four blocks. And with four visible sections, ruling ③ largely
dissolves: the required path is *visibly* four sections long.

---

## 4. Rulings recommended on issue #18 §9

**① Hoist nb07-L1's list experiment into class; move nb10-L1's placebo/influence
work to the Friday studio.** These are different problems wearing the same
clothes. The list experiment is the *only* place in the course where the
signature design of the experimental-descriptive pathway is executed — optional
depth that is required for pathway coverage is a coverage hole, not a depth
question. Placebo tests and leave-one-out influence, by contrast, are
*procedures you apply to your own analysis* — which is precisely what the Friday
studio is for, and precisely what M13's replication + red-team report demands.
Relocating them there also closes an alignment gap: **D30 retired the Friday
red-team block, so the most adversarial deliverable now gets its dedicated
rehearsal only in an async module.** One move fixes both.

**② Agreed — demote two of nb03-L1's three live exchanges, and check nb08-L1
while you are there.** The evidence reason is stronger than the standing rule:
three round-trips in fifty minutes guarantees each is interrogated shallowly,
and shallow interrogation *is* the metacognitive-laziness failure mode. One
exchange properly challenged beats three glanced at. But nb03-L1 is not the
densest lecture — **nb08-L1 is** (16 headings, 11 written responses, 8 code
cells: a production event every 2.6 minutes), and it is not on the ruling list.
Both are single-lecture weeks that absorbed two lectures of content. Treat them
as one problem.

**③ Amend the frame sentence rather than moving the prompts** — moving them
orphans them from the content they extend, and the frame is generated, so it is
one edit propagating to 25 lectures. Add a second signal: make 🏠 items and the
⏸ region share an identical prefix ("Optional depth — …"). Consistent marking
beats explanation. One measured caution: **only ~1.6 AI-prompt blocks per
lecture now sit above the ⏸ line**, against a template minimum of ≥4 per
notebook. If the prompts that teach the Ask → Verify → Document habit are the
ones drifting below the line, the course's central discipline is quietly
becoming optional. Audit which four are required.

---

## 5. Recommended order of work

1. Retime Wednesday to **7 / 20 / 15 / 8** and add the named 5-minute instructor
   adjudication. *(Fixes the one real defect.)*
2. Make 📝 **write-then-speak** on both days. *(Free; helps learning and anxiety
   at once.)*
3. Give ⚖️ a required grammar: *"I chose X over Y because Z."* *(Recovers the
   writing effect D33 traded away.)*
4. Collapse headings to four blocks with inline beats; unify Mon/Wed as
   Open · Investigate · Test · Close.
5. Rebalance nb03-L1 **and nb08-L1**; hoist nb07-L1's list experiment; relocate
   nb10-L1's placebo work to Friday.
6. Fade the frame in three stages across the semester.
7. Add the Week 1 "why this room works this way" segment (Deslauriers).

Propagation path for any accepted ruling:
`_production_kit/nb_sources/` → `scripts/nbbuild.py nbNN` → validators →
site + 3 books → `scripts/sync_instructor_repo.sh`.

---

## Evidence appendix — with strength grading

**Strong (meta-analytic or randomized):** Freeman et al. 2014 *PNAS* · Theobald
et al. 2020 *PNAS* · Deslauriers et al. 2019 *PNAS* · Dunlosky et al. 2013
*PSPI* · Smith et al. 2009 *Science* · Graham, Kiuhara & MacKay 2020 *RER* ·
van Alten et al. 2019 *Educational Research Review* (flipped classroom,
g ≈ 0.3–0.4) · Bastani et al. 2024/2025 (generative-AI RCT) · Kestin et al. 2025
*Scientific Reports*.

**Moderate (theory with converging studies):** Kapur 2008/2016 and Loibl, Roll &
Rummel 2017 (productive failure requires consolidation) · Kirschner, Sweller &
Clark 2006 · Sweller, van Merriënboer & Paas 2019 · Kalyuga et al. 2003
(expertise reversal) · Renkl & Atkinson 2003 (guidance fading) · Collins, Brown
& Newman 1989 (cognitive apprenticeship) · Rosenshine 2012 · Fiorella & Mayer
2013 · Koedinger et al. 2015 · Chi & Wylie 2014 (ICAP) · Biggs 1996 · Cooper,
Downing & Brownell 2018 · England et al. 2017 · Fan et al. 2025 *BJET*.

**Weak — suggestive only:** Lee et al. 2025 *CHI* (self-reported
critical-thinking effort) · Kosmyna et al. 2025 (MIT Media Lab preprint,
N ≈ 54, not peer reviewed) · Gerlich 2025 (correlational). Given the course's
own evidence-integrity rule, do not put these in student-facing material without
the caveat attached.

> **Verification note.** Every reference above was drawn from the assistant's
> own knowledge, not retrieved during this session. Before any of it enters
> student-facing material, retrieve and confirm each source per the course's
> evidence-integrity rule (`scripts/audit_sources.py`).

---

## Verification addendum (2026-07-30, post-Codex critique — D34)

An independent Codex review (gpt-5.6-sol, xhigh; artifacts in gitignored
`_adm/codex_reviews/2026-07-30_d33-mw-lecture-structure/`) recomputed this
document's measurements and audited the claims. Corrections of record:

**Corrected measurements.** The lecture population is 28 built segments, of
which **24 are D33-governed** (nb01 ×2, nb13, nb14 exempt) — the headline
figures above averaged over exempt lectures and used "27 governed"
incorrectly. Governed-only figures: **12.1** ritual headings per lecture (not
11.3), **9.9** production events (not 9.1, and most counted code cells are
provided runs, not student productions), **1.7** AI-prompt blocks above the ⏸
line (not 1.6). The "≥4 per notebook" comparison was invalid: the template's
four-prompt minimum is notebook-wide and includes optional prompts. The
"transition every 4.4 minutes" and "12–22% of class time" claims rested on an
assumed 30–60-second cost per heading that was never measured; a heading is
not necessarily a transition. "Wednesday never consolidates" overstated the
premise: no dedicated timed slot existed, but the session guides, the
implementation guide, and the intervention protocol all assigned the
instructor a Wednesday adjudication role.

**Withdrawn recommendations.** The 7/20/15/8 Wednesday retime (reverses D22
while claiming not to touch the blocks); the four-heading collapse and
Mon/Wed unification (heading count ≠ transition count, and the change touches
template markers, validator regexes, source structures, answer stripping, SRL
briefs, and book sync — not one generator function); the fixed
Weeks 2–5/6–11/12–16 fading schedule (expertise reversal is expertise-
contingent, not calendar-contingent; accountability instruments like the
ledger are artifacts, not scaffolds, and never fade).

**What was applied instead (D34).** The Wednesday consolidation need was met
INSIDE D22's 30–42 block: 30–38 peer defense, 38–42 SRL synthesis +
instructor accuracy lock. The two implementation failures the critique found
— optional material still assessed/scheduled as required, and D33's in-class
weights not propagated into every prompt — drove an alignment sweep and
validator hardening. Write-then-speak 📝 and the ⚖️ choice grammar remain
candidates to pilot in the room. The evidence appendix above survives with
its caveat: every reference was recalled, then independently VERIFIED by the
Codex pass against publisher records, with the repeated warning that the
literature supports the design *principles*, not the specific doses, timings,
or schedules this review attached to them.
