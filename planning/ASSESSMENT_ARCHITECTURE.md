# ASSESSMENT_ARCHITECTURE — what is graded, why, and how it adds up

Authoritative reconciliation of the v2 grading system for `syllabus.qmd`.
Philosophy: **no conventional midterm or final exam.** The course assesses the
research chain itself — a semester-long individual project carried through
sixteen milestones (M0–M15), presented at the Purdue Fall Undergraduate Research
Expo, and closed with a public evidence defense and a reproducible final chapter.
Grading rewards correctness, transparency, reproducibility, question-design
(compass) alignment, and responsible interpretation — **never coding elegance**
(no computing background is assumed; all machinery is provided).

The v1 six-component / M00–M23 system is preserved at git tag `v1-compass-build`;
this file replaces it. Component weights match `course_config.yaml assessment:`
and the syllabus Assessments table exactly, and are a **proposal pending
instructor confirmation**. Every internal sub-weight below is likewise
**provisional** and marked so.

## The seven components (100%)

| Component | Weight | What it contains |
|---|---:|---|
| **1. Daily notebook preparation & engagement** | **10%** | Notebook completion (executed cells + written responses), Claim Tickets on assigned readings, in-class investigation and studio participation, red-team / cross-examination citizenship |
| **2. Student Research Lead (SRL) performance** | **15%** | Five flipped-lecture leads, each scored live on the 100-point SRL rubric (`project/srl/srl_rubric.md`) |
| **3. Milestone development & revisions (M0–M9)** | **25%** | The ten develop→present→submit→revise milestones that build the design and first evidence |
| **4. Poster & Expo (M10–M12)** | **20%** | M10 final poster lock (terminal), M11 presentation package, M12 conference reflection + poster-criticism portfolio incl. the required Expo presentation |
| **5. Replication & red-team (M13)** | **5%** | Reproduce a peer's anonymized package, attest the headline result, report fragility |
| **6. Research note, final chapter & portfolio, and defense (M14–M15)** | **15%** | M14 research-note draft + reproducibility capsule; M15 final chapter + AI-management portfolio + live evidence defense (terminal) |
| **7. Claim analyses & concept checks** | **10%** | Short concept checks across the term + structured claim-analysis exercises |
| | **100%** | |

## Provisional within-group weighting

Sub-weights sum to each group total; all are provisional pending instructor
confirmation. Presentations are graded **inside** each milestone's rubric (a
"presented + incorporated feedback" row), not as a separate ledger.

**Component 3 — Milestones M0–M9 (25%).** Early scoping milestones lighter; the
declaration, protocol, and first-evidence milestones heavier.

| M0 | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 2 | 2 | 3 | 2.5 | 2.5 | 2.5 | 3 | 2.5 | 3 |

**Component 4 — Poster & Expo (20%).** M10 final poster **8** · M11 presentation
package **4** · M12 **8** (within M12: live Expo presentation **5**, reflection +
poster-criticism portfolio **3**).

**Component 6 — M14–M15 (15%).** M14 research note + reproducibility capsule
**6** · M15 **9** (within M15: final chapter + AI-management portfolio **6**,
live evidence defense **3**).

**Component 1 (10%).** Notebook completion **5** · Claim Tickets **3** · studio /
red-team citizenship **2**.

**Component 2 (15%).** Five leads, **3 points each** (5 × 3 = 15); each lead's
raw 100-point rubric score scales to its 3-point share.

**Component 7 (10%).** Short concept checks **6** · claim-analysis exercises
**4** (Calling Bullshit–style analyses are optional per the locked CB decision;
if CB is skipped, the 4 points fold into an additional concept check).

## Why these weights

- **Development outweighs any single artifact** (25% for M0–M9 vs 8% for the
  poster itself): the course's claim is that the *chain* — declare, diagnose,
  redesign, verify — is the learning, and the weights say so out loud.
- **The flipped classroom is graded at 15%** because Mon/Wed lectures *are* the
  SRL performances; leading well is a rehearsal of the Expo and the defense.
- **Post-Expo work is substantive by construction** (20% across components 5–6
  lands after Nov 17), enforcing that the semester does not end at the Expo.
- **Nothing is auto-graded MC** by default; the MC option-length parity rule and
  `audit_answer_length.py` stay dormant unless concept checks later move to
  Brightspace auto-grading (allowed, not planned).

## Rubric DNA — five virtues, one menu

Every milestone rubric in `_research_project/2026Fall/` is a **100-point,
four-band** instrument (Exemplary / Proficient / Developing / Beginning) whose
criterion rows are drawn from this fixed menu, so the same virtues are rewarded
all semester. Each maps to a CLAUDE.md critical rule:

1. **Compass alignment** — the work matches its declared compass position (kind ×
   reach) and design pathway, and stays inside its claim boundary
   (*Inquiry-Declaration Justification*).
2. **Evidence integrity** — every empirical claim traces to a real, retrievable
   source or a reproducible computation (*Evidence-Integrity & Results-
   Verification*).
3. **Verification** — the deliverable records how outputs were cross-checked, and
   AI use is disclosed Specify→Delegate→Interrogate→Inspect→Verify→Document→
   Defend (*Evidence-Integrity* + *AI Research Ledger & SDIIVDD*).
4. **Uncertainty & limitations** — stated and calibrated, neither hidden nor
   spiraling (*Uncertainty & Limitations in Communication*).
5. **Craft & communication** — organized, on-format, on-time, audience-aware; the
   AI Research Ledger is complete (*AI Research Ledger & SDIIVDD*).

## Hard-cap penalty doctrine

Certain failures cap a rubric criterion regardless of the rest of the row — the
teeth behind the course's discipline:

- **Fabricated or unretrievable source** → Evidence integrity capped at Beginning.
- **Untraceable number** (no path from datum to reported figure) → Verification
  capped at Beginning.
- **Non-reproducing result** (headline number does not rerun from the package) →
  Verification capped at Beginning.
- **Missing AI Research Ledger entry** → Craft scored **0** and the submission
  **returned** unread (per the CLAUDE.md AI-Ledger rule).
- **SRL live cap** — presenting an AI answer as settled without verifying it caps
  SRL rubric row 4 (Productive use of AI) at Beginning (`srl_rubric.md`).

## Grade bands & policies

Letter bands follow the standard Purdue scale: A ≥ 93, A− ≥ 90, B+ ≥ 87, B ≥ 83,
B− ≥ 80, C+ ≥ 77, C ≥ 73, C− ≥ 70, D ≥ 60, F < 60. **No curve** (n = 5).

**Revision.** Feedback returns within 3 days of each milestone; most milestones
accept a revised version within **7 days** of feedback for up to half the lost
points (revising is part of the graded craft). **Terminal artifacts have no
revision window** — the deadline governs: **M10** final poster (Fri Nov 6,
5:00 PM), **M15** final chapter + portfolio (Fri Dec 11), and the live **Expo
presentation** (Tue Nov 17, a graded component of M12).

**Late.** −10% per day up to 3 days, then not accepted; documented emergencies
handled individually per Purdue policy.

**Honors GPA cap.** The Daniels School GPA-3.3 grading cap does **not** apply
(this is an Honors College course; the cap was removed from the seeded syllabus).
Confirm once with the Honors College before publishing — tracked on the course
board.

## Integrity instruments — where they are graded

- **AI Research Ledger** (what AI did and how it was checked) — appended to every
  deliverable and every notebook session; **audited at every milestone under the
  Craft criterion**, with a missing entry triggering the hard cap above. This is
  a graded habit, not a formality.
- **Claim ledger** (what the research asserts: claim · evidence · verification ·
  boundary · sensitivity survival) — a separate instrument, graded at **M9**
  (research audit), **M14** (research note), and **M15** (final chapter).
- **Reproduction sign-off** — at **M13**, a classmate attests whether the peer's
  headline number reproduces from the package alone.

## SRL grading pipeline

The Student Research Lead score (Component 2) is produced per slot:

1. The lead receives their SRL page **five days ahead** and submits a
   **preparation template two days ahead** for instructor review; the template
   pre-loads rows 2 (Socratic questions), 3 (assumption-probe), 4–5 (AI plan),
   7 (timing), and 8 (project connection).
2. The lead runs the room **live** and is scored on all nine rubric rows
   (`project/srl/srl_rubric.md`, 100 points) during the session.
3. **Revision does not apply** to a live performance; the next of the five slots
   is the improvement window, informed by peer feedback
   (`srl_peer_feedback_form.md`) and the instructor's notes.

Each slot's 100-point score scales to its 3-point course share; the five slots
sum to the 15% component.
