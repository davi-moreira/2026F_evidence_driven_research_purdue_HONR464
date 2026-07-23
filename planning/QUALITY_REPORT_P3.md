# QUALITY REPORT — Phase 3 Prototype Review (Week 5: nb04 + M4 + ms04)

**Date:** 2026-07-23 · Three independent reviewers (pedagogy/Socratic/timing/
accessibility; design-accuracy/STEM/reproducibility with number re-derivation;
AI-intensity/ownership/milestone-alignment). Verdicts converge: **fit to be the
canonical template after targeted fixes, not as-is.** All numbers below were
independently re-derived by the design reviewer (frame mean 48.798 ✓; nonresponse
drift +0.647 ✓; dataset shapes/summaries ✓).

## Must-fix (criticals + highs) — the P3 fix list

| # | Finding | Source |
|---|---|---|
| F1 | ms04 DAG scaffold crashes (KeyError) on the exact rename students are told to make — `pos` dict hardcodes node names; build positions from the variables | pedagogy C1 |
| F2 | `rdss_fig_8_1.png` caption dumps 7 undefined variables on a no-quant audience; introduce only S/R with definitions or drop the figure | pedagogy C2 |
| F3 | Lecture 1 (and L2) overstuffed vs the 22/23-min frames; add explicit "⏸ In class through here — the rest is homework" dividers; move ⚖️ Design Choice + 📝 Practice below the line | pedagogy C3 + M10 |
| F4 | Rebuild ALL six Gemini prompts to the course's own standard: a one-line written human commitment BEFORE each; brief→follow-up→interrogate sequences; genuinely delegable tasks (locate / list-to-verify / red-team), never re-explaining the notebook's prose; verify steps that name the specific ai_error_taxonomy failure they counter (no rubber-stamp source checks on citation-free prompts) | AI H1/H2/H3/M8/M9/M10 |
| F5 | Designate ONE "live in class" Gemini prompt per lecture; mark the rest "homework depth" | pedagogy H6 |
| F6 | Terminology: "selection **DAG**" everywhere (introduced once as "a selection diagram, also called a DAG — directed acyclic graph"); teach **silent exclusion** in §1; teach the three-rung **concept → construct → indicator** ladder in §4 — nb04 must teach every term M4 grades | pedagogy H7 + AI H4/H5/M12 |
| F7 | Boundary discipline: the Human-Only Checkpoint and 🎯 Project Transfer require TWO sentences (the licensed population sentence + the named forbidden silent upgrade), matching M4 §4 | AI H6 |
| F8 | Nonresponse caveat ordering: student drafts the boundary FIRST, AI attacks it; scope AI caveat-drafting to the teaching estimate only; reword the worked ledger row to model attack-not-draft | AI M7 |
| F9 | Ex5 instructor solution says "about 4.96"; executed output + rederivation say **5.074 / +0.647** — correct to "about 5.07 (up ~0.65 from 4.43)"; harmonize all drift wording to ~0.65 | design H1 + L6 |
| F10 | Predict-first gating: add 🔮 Pause & Predict before the convenience reveal and the nonresponse reveal; keep reveal prose out of the same cell as its commit prompt | pedagogy H4 |
| F11 | Convenience exercise is pre-answered (channel description names the mechanism); describe the channel neutrally and let the by-party table expose it; drop the answer from its verify checklist | pedagogy H5 + AI M10 |
| F12 | DAG edge labels contradict the notebook's own definitions; relabel target→accessible = "access/reach gap", accessible→frame = "coverage / frame error", frame→observed = "sampling / selection" | design M2 |

## Should-fix (mediums/lows bundled into the same pass)

Reframe the L1 dining-hall puzzle as a stakeable yes/no claim (pedagogy M8);
SRL pages for slots 06/07 in the instructor notebook (pre-drafted Socratic
questions + expected-AI-error note) (pedagogy M12); human-first markers on
compass-critical practice/transfer cells (AI M11); Exit Defense requires
accept/change/reject verb + the specific check (AI L13); ledger row count note
+ header harmonization to course_config fields (AI L14/L15); one-line
plain-language description under every figure (pedagogy L13); distinct hue for
the convenience marker vs the truth line (pedagogy M11); jitter the ten-means
strip (pedagogy L14); import networkx in setup with a local-install comment
(pedagogy L15); add nb04 to notebooks/data/README.md course-use rows and
notebooks/figures/README.md fig map (design L3); remove the dead `rng`
assignment or wire it in (design L4); "within a few years" → honest band
wording (design L5).

## What is strong and must survive the fixes

The concept arc (population/frame/sample → selection → random-vs-convenience →
honest summary → nonresponse boundary); the undergraduate voice; the
🧑‍⚖️ Human-Only Checkpoint at the highest-temptation point; the 🔁 Modify /
🔬 Interrogate pair; the worked ledger row's specificity; MNAR simulation
correctness; STEM breadth (river nitrate, bird point-counts, alloy
survivorship, telemetry opt-out); seed discipline and clean-run integrity;
ms04's delegable-work prompt pattern (better than nb04's — propagate it).

## Template-level lessons (encoded in ACTIVITY_TEMPLATE for the P4 scale)

1. "⏸ In class through here" demarcation cell per lecture (in-class load sized
   to the 22/23-minute frame; overflow explicitly homework).
2. One designated live Gemini prompt per lecture; others marked homework depth.
3. Prompt-sequence standard: commit line → brief → follow-up/interrogate →
   taxonomy-named verify. Delegable tasks only.
4. Predict-before-reveal gating on every reveal, not just one.
5. Vocabulary continuity contract: every term a milestone rubric grades is
   taught (bold → definition → example) in that week's notebook.
6. One-line plain-language description under every figure (accessibility).
7. Studio scaffolds must be edit-safe (single source of truth for names).
