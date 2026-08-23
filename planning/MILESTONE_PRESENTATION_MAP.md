# MILESTONE_PRESENTATION_MAP — develop → present → submit → revise, per milestone

Every milestone is presented or peer-reviewed — in class or on the course board —
before (or at) submission. With five enrolled students, every active project
presents every time and every student has an individual speaking or review role;
formats are deliberately varied so "presenting" never calcifies into one genre.
Under the studio-Friday rhythm, most presentations happen inside the Friday work
block (20–50 min); a few sit on Mon/Wed lecture days where hard dates force it
(M13's gallery walk and oral defense, the M17 defenses), M6 and M16 run on the
async board, and the URC Expo (Tue Nov 17) is a scheduled performance event and a
Final Project **Poster Presentation at the Purdue Undergraduate Research
Conference** score. M15 separately grades the
written reflection checkpoint. Kickoff venues live in `PROJECT_MILESTONES.md`.

This map is a **planning companion** to `PROJECT_MILESTONES.md` (the chain table)
and `course_config.yaml milestones:` (the machine-readable anchors that
`scripts/validate_milestones.py` actually checks). It is *not* itself validated —
treat `course_config.yaml` + `PROJECT_MILESTONES.md` as the source of truth and
this file as the presentation-format overlay on top of them.

Meeting numbers `M2…M43` are MEETINGS (calendar backbone); milestone IDs are
`M1…M17`. Dates are the v2 backbone from `planning/MEETING_SCHEDULE.csv`.

Legend: dev = in-class development meetings · pres = presentation/review moment ·
due = submission (11:59 PM unless noted) · rev = revision path (standing policy in
`PROJECT_MILESTONES.md`: eligible milestones revisable within 7 days of feedback
for up to half the lost points).

| ID | Presentation format (audience action) | dev | pres | due | rev |
|---|---|---|---|---|---|
| M1 | **30-second curiosity pitch** + baseline share — class gives one strength + one question each | M2–M3 | M4 (studio) | Fri Aug 28 | folds into M2 |
| M2 | **2-minute landscape pitch** — class votes the compass position + names one risk | M4–M6 | M7 (studio) | Fri Sep 4 | eligible; feedback feeds M4 |
| M3 | **Contribution-map gallery walk** — claim/evidence maps on screens; sticky-note challenges; one challenge incorporated live | M7–M8 | M9 (studio) | Fri Sep 11 | eligible |
| M4 | **3-minute charter declaration** — listeners each write one clarifying question; declaration revised from them | M9–M13 | M17 (studio) | Fri Sep 18 | eligible |
| M5 | **Design-audit walkthrough** — listeners file two-line reviews (best rung / weakest rung of the measurement ladder) | M17–M16 | M16 (studio) | Fri Sep 25 | eligible |
| M6 | **90-second causal/boundary statement + peer red-team** — classmates reply naming the identification move or the language boundary | M16–M16 | M17 (studio) | Fri Oct 2 | eligible |
| M7 | **Protocol clinic + abstract workshop** — claim-anatomy checklist, rotating consults, partner proof-read, inside the studio block; URC abstract cleared the internal gate | M17–M19 | M20 (studio) | Fri Oct 9 | protocol eligible; abstract not revisable (gate) |
| M8 | **Protocol cross-review** — partner swaps declared-analysis protocols and pre-registers one predicted attack on the other's plan | M20–M21 | M22 (studio) | Fri Oct 16 | eligible |
| M9 | **First-evidence walkthrough** — 60-second redesign pitch: weakness, fix, before/after diagnosands on the first computed estimate | M22–M24 | M25 (studio) | Fri Oct 23 | eligible |
| M10 | **Poster-draft red-team** — the five audits (claim boundary, figure honesty, read path, uncertainty, accessibility); two peers + the required Poster Critic and Robustness & Sensitivity Reviewer roles; author triages hits | M25–M27 | M28 (studio) | Fri Oct 30 | eligible |
| M13 | **Poster Criticism I gallery walk** (M29) + **Criticism II oral defense** (M30) — three lenses (interdisciplinary / methods / skeptic), defend-or-concede on the record; pre-lock production at the Friday studio, then terminal Sunday submission | M28–M30 | M29 + M30 (Mon/Wed) + M31 (studio) | **Sun Nov 8, 11:59 PM** | none (terminal) |
| M17 | **Mock poster symposium** — the three pitch layers (30-sec hook, 90-sec walk, full pitch) under live fire; partner + AI reviewer flag every spoken upgrade | M32–M33 | M34 (studio) | Fri Nov 13 | eligible |
| M15 | **URC Expo** (Tue Nov 17: present your poster + evaluate ≥3 peer posters; live quality is graded only in Final Project) + **reflection story round** (M36) — 90-sec surprising moment, then read the pattern off your coded tally | M35–M36 | Expo (Tue Nov 17) + M36 (studio) | Fri Nov 20 | M15 written package eligible; Final Project live score terminal |
| M16 | **Anonymized reproduction exchange** (async) — you rebuild a stranger's headline number cold, red-team it, and post the residual to the board | M36–M37 | async board (module week) | **Sun Nov 29** | eligible |
| M16 | **Table read** — all five research notes read by all, margin notes (sharpest sentence / weakest claim); reproducibility capsule stub shown | M37–M39 | M40 (studio) | Fri Dec 4 | eligible |
| M17 | **Evidence Defense** — final oral defense (claims, choices, verification) + cross-examination where every non-defender asks ≥1 ledger-grounded question; **submission ceremony** closes the term | M40–M42 | M42–M43 (Mon/Wed/Fri) | **Fri Dec 11** | none (terminal) |

## Presentation-format variety audit

Formats used: pitch (30-sec / 90-sec / 2-min / 3-min / 60-sec technical), gallery
walk (M3, M13), clarifying-question rounds, written two-line reviews, async
recorded statement + board replies (M6), clinic/consults, protocol cross-review,
five-audit red-team (M10), oral defense with three lenses (M13), mock symposium
(M17), **public conference (the URC Expo, M15)**, reflection story round (M15),
anonymized reproduction exchange (M16, a different board genre from M6), table
read (M16), and formal Evidence Defense with cross-examination + ceremony (M17).
**No format repeats in consecutive milestones**, satisfying the "vary the studio"
guardrail in `COURSE_MASTER_PLAN.md`.

## Oral-communication ramp (deliberate)

30-sec (M1) → 2-min (M2) → gallery walk (M3) → 3-min declared (M4) → measurement
walkthrough (M5) → 90-sec recorded async (M6) → clinic/workshop (M7) →
cross-review (M8) → 60-sec technical (M9) → structured five-audit red-team (M10) →
gallery walk + adversarial three-lens oral defense (M13) → the three-layer pitch
under fire (M17) → **public conference at the URC Expo (M15)** → async
reproduction exchange (M16) → table read (M16) → **formal Evidence Defense (M17)**.
Stakes and polish rise monotonically; format length does not — compression is
trained as its own skill, and the two terminal performances (the Nov 8 poster lock
and the Dec 11 Evidence Defense) carry no revision window.
