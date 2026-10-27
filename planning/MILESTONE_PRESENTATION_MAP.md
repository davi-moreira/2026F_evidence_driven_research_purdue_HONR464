# MILESTONE_PRESENTATION_MAP — develop → present → submit → revise, per milestone

Every milestone is presented or peer-reviewed — in class or on the course board —
before (or at) submission. With six enrolled students, every active project
presents every time and every student has an individual speaking or review role;
formats are deliberately varied so "presenting" never calcifies into one genre.
Under the studio-Friday rhythm, most presentations happen inside the Friday work
block (20–50 min); a few sit on Mon/Wed lecture days where hard dates force it
(the Week 12 practice presentations, the Week 15 package exchange), M6 and M16 run
asynchronously, and the URC Expo (Tue Nov 17) is a scheduled performance event and a
Final Project **Poster Presentation at the Purdue Undergraduate Research
Conference** score. Since D91 the conference block follows QM 47400's post-lock
sequence (M11–M16); M15 confirms the Expo presentation and M16 is the written
reflection. Kickoff venues live in `PROJECT_MILESTONES.md`.

This map is a **planning companion** to `PROJECT_MILESTONES.md` (the chain table)
and `course_config.yaml milestones:` (the machine-readable anchors that
`scripts/validate_milestones.py` actually checks). It is *not* itself validated —
treat `course_config.yaml` + `PROJECT_MILESTONES.md` as the source of truth and
this file as the presentation-format overlay on top of them.

Meeting numbers `M2…M43` are MEETINGS (calendar backbone); milestone IDs are
`M1…M17` (D91). Dates are the v2 backbone from `planning/MEETING_SCHEDULE.csv`.

Legend: dev = in-class development meetings · pres = presentation/review moment ·
due = submission (11:59 PM unless noted) · rev = revision path (standing policy in
`PROJECT_MILESTONES.md`: eligible milestones revisable within 7 days of feedback
for up to half the lost points).

| ID | Presentation format (audience action) | dev | pres | due | rev |
|---|---|---|---|---|---|
| M1 | **30-second curiosity pitch** + baseline share — class gives one strength + one question each | M2–M3 | M4 (studio) | Sun Aug 30 | folds into M2 |
| M2 | **2-minute landscape pitch** — class votes the compass position + names one risk | M4–M6 | M7 (studio) | Mon Sep 7 | eligible; feedback feeds M4 |
| M3 | **Contribution-map gallery walk** — claim/evidence maps on screens; sticky-note challenges; one challenge incorporated live | M7–M8 | M9 (studio) | Sun Sep 13 | eligible |
| M4 | **3-minute charter declaration** — listeners each write one clarifying question; declaration revised from them | M9–M13 | M17 (studio) | Sun Sep 20 | eligible |
| M5 | **Design-audit walkthrough** — listeners file two-line reviews (best rung / weakest rung of the measurement ladder) | M17–M16 | M16 (studio) | Sun Sep 27 | eligible |
| M6 | **90-second causal/boundary statement + peer red-team** — classmates reply naming the identification move or the language boundary | M16–M16 | M17 (studio) | Sun Oct 4 | eligible |
| M7 | **Protocol clinic + abstract workshop** — claim-anatomy checklist, rotating consults, partner proof-read, inside the studio block; URC abstract cleared the internal gate | M17–M19 | M20 (studio) | Tue Oct 13 | protocol eligible; abstract not revisable (gate) |
| M8 | **Protocol cross-review** — partner swaps declared-analysis protocols and pre-registers one predicted attack on the other's plan | M20–M21 | M22 (studio) | Sun Oct 18 | eligible |
| M9 | **First-evidence walkthrough** — 60-second redesign pitch: weakness, fix, before/after diagnosands on the first computed estimate | M22–M24 | M25 (studio) | Sun Oct 25 | eligible |
| M10 | **Poster-draft red-team** — the five audits (claim boundary, figure honesty, read path, uncertainty, accessibility); two peers + the required Poster Critic and Robustness & Sensitivity Reviewer roles; author triages hits | M25–M27 | M28 (studio) | Sun Nov 1 | eligible |
| M11 | **Poster production labs** (M29–M31, and M27–M28 for the M10 draft): one-on-one instructor consultations at the boards + the print-scale check (M31); the final poster is the print file (D91, amended 2026-10-27) | M29–M31 | M30 (Wed) + M31 (studio) | **Sun Nov 8 — TERMINAL** | none (terminal) |
| M12 | **Pitches under typed adversarial questioning** (M33) — the three timed pitches with the boundary sentence at every length; Round 02 meeting confirmed | M32–M33 | M33 (Wed) | Wed Nov 11 | eligible |
| M13 | **Written peer review** of every other poster from the shared folder — tangible feedback + questions, then the questions asked live at the **practice presentations** (M34) | M33 | M34 (studio) | Thu Nov 12 | eligible (process score) |
| M14 | **LinkedIn invitation** — the public post, copied from the official program | M34 | public post | Sun Nov 15 | none (completion) |
| M15 | **URC Expo** (Tue Nov 17: present your poster; the live presentation is scored there) — photo in front of the poster | M35 | Expo (Tue Nov 17) | Tue Nov 17 | none (completion) |
| M16 | **Conference reflection** — the survey (M36, async) and the plan to improve and complete the research (M37, async) | M36–M37 | async | Mon Nov 23 | eligible |
| M17 | **In-class package exchange** (M39) — you cold-run a colleague's package from their written instructions and hand them a threat-ranked report; repair block, two blocking gates and second clean run at the studio (M40) | M38–M40 | M39 (Wed) + M40 (studio) | Sun Dec 6 | eligible |
| — | **Evidence Defense** (D54: in-class practice, no grade weight) — oral defense (claims, choices, verification) + cross-examination where every non-defender asks ≥1 ledger-grounded question; the Week 15–16 Wednesday blocks | M40–M42 | M42–M43 (Mon/Wed/Fri) | **Fri Dec 11** | none (terminal) |

## Presentation-format variety audit

Formats used: pitch (30-sec / 90-sec / 2-min / 3-min / 60-sec technical), gallery
walk (M3), clarifying-question rounds, written two-line reviews, async
recorded statement + board replies (M6), clinic/consults, protocol cross-review,
five-audit red-team (M10), the poster production labs (M11), pitches under typed
questioning (M12), written peer review asked live at the practice presentations
(M13), the public invitation (M14), **public conference (the URC Expo, M15)**, the
reflection survey and plan (M16), and the in-class package exchange (M17), which
closes the chain.
**No format repeats in consecutive milestones**, satisfying the "vary the studio"
guardrail in `COURSE_MASTER_PLAN.md`.

## Oral-communication ramp (deliberate)

30-sec (M1) → 2-min (M2) → gallery walk (M3) → 3-min declared (M4) → measurement
walkthrough (M5) → 90-sec recorded async (M6) → clinic/workshop (M7) →
cross-review (M8) → 60-sec technical (M9) → structured five-audit red-team (M10) →
the poster production labs (M11) → the three-layer pitch under questioning (M12) → the
practice presentation answering classmates' questions (M13) → **public conference
at the URC Expo (M15)** → the in-class package exchange (M17), the chain's close.
Stakes and polish rise monotonically; format length does not — compression is
trained as its own skill, and the terminal artifacts (the Nov 8 print file and the
Expo itself) carry no revision window.
