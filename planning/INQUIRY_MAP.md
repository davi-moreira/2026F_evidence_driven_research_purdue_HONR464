# INQUIRY_MAP — the inquiry compass across HONR 46400

*(Renamed from QUANTITATIVE_APPROACH_MAP.md when the course adopted the RDSS
taxonomy outright, 2026-07-19 — see DECISIONS.md. The four-approach grid is
retired; its claim-boundary drills survive as compass crossings.)*

The course's signature skill is **classifying a research question with the
inquiry compass** — two questions, both native to RDSS ch. 7 — and then holding
every claim inside the boundary that classification draws:

1. **KIND — descriptive or causal?** Does answering require a counterfactual
   contrast (what would differ under an intervention), or only the world as it
   is/was?
2. **REACH — for which units must the answer hold?** The data at hand · a
   population beyond the data · cases not yet seen.

Machine-readable core: `course_config.yaml` `inquiry_framework:`. Per-meeting
detail: `planning/MEETING_SCHEDULE.csv` (`inquiry`, `claim_permitted`,
`claim_not_permitted` columns).

## The compass (teaching device, introduced in nb02)

|  | **Reach: data at hand** | **Reach: a population** | **Reach: unseen cases** |
|---|---|---|---|
| **Descriptive** | **Description** (nb06) | **Generalization** (nb10) | **Prediction** (nb12) |
| **Causal** | **Causal reasoning** (nb13) — identification licenses the kind; sampling licenses the reach (SATE → PATE) | | |

The four named positions preserve the old modules; what changed is that they are
now *derived* from the book's two-kind split instead of standing beside it.
RDSS's design library (Part III) is organized by data strategy × kind
(observational/experimental × descriptive/causal, ch. 15–18); the course adds
the missing predictive entry (see Position 3).

## Crossings and licenses — the claim-boundary discipline, unified

Every overclaim in the wild is a **compass crossing without its license**. The
license is always a design element (D or A), and the proof is always diagnosis:

| Crossing | License (RDSS home) | Named violation (drilled) |
|---|---|---|
| sample → population | sampling data strategy (ch. 8) + uncertainty-bearing answer strategy (ch. 9) + diagnosis: coverage/power (ch. 10) | **the silent upgrade** (M21) |
| observed → unseen | prediction-time-honest data strategy (no leakage) + held-out diagnosands + baseline comparison under redesign | **leakage**; "tomorrow resembles the training data" (M25–M26) |
| descriptive → causal | assignment strategy (ch. 8, 18) or defended observational identification (ch. 16) | **after-therefore-because**; **design mimicry** (M27–M28) |

> You buy KIND and REACH with your data strategy, and you prove the purchase
> with diagnosis.

## Position 1 — Description (descriptive · data at hand)

- **Asks:** what is observed in the data at hand — patterns, distributions, differences.
- **Permits:** statements about these units: "in these 10,000 interviews, X% report Y."
- **Does NOT permit:** any reach beyond these units; causal readings.
- **Taught:** introduced M5 (nb02); **deep dive M13–M14 (nb06)**; exercised in the
  claim map (M8), honest visualization (M14), and every "Table 1" a project builds.
- **Datasets:** `lapop_brazil.csv` (with its 10k-resample provenance caveat, taught
  explicitly), `la_voter_file.csv`.
- **Milestone applications:** M02 (describing what sources claim), M04 (indicator
  distributions), M09 description-branch pilots, poster "what the data show" blocks.
- **Classic misclassification:** a descriptive question dressed in causal language
  (a kind-crossing: "does social media *make* people anxious?" when the underlying
  question is "how anxious are heavy users?").
- **RDSS home:** ch. 15 "Observational: descriptive" (+ ch. 17 for descriptive
  quantities measured by experiments).

## Position 2 — Generalization (descriptive · population)

*(Formerly "statistical/observational inference." Same content; the new name says
what the position does: carry a descriptive answer from the sample to the
population the sampling frame reaches.)*

- **Asks:** what holds beyond the sample — population/process estimates.
- **Permits:** estimates with quantified uncertainty for the population the frame
  reaches: "X ± interval among the population my sampling procedure covers."
- **Does NOT permit:** causal claims from association; reach past the frame.
- **Taught:** introduced M5 (nb02); data strategy M15–M16 (nb07); answer strategy
  M18–M19 (nb09); **deep dive M20–M22 (nb10)** — uncertainty, generalization,
  power; async claim diagnosis M17 (nb08).
- **Datasets/simulations:** `lapop_brazil.csv`, `la_voter_file.csv`, seeded
  sampling-distribution and power simulations (seed 464).
- **Milestone applications:** M05 (data strategy), M06 (answer strategy), M07
  (declaration + abstract uncertainty language), M09 generalization-branch pilots,
  M14 (uncertainty statement).
- **Classic misclassification:** the **silent upgrade** — association → link →
  impact → effect across a paragraph (taught by name in M21); reach claimed
  without a sampling design behind it.
- **RDSS home:** ch. 8 (data strategy), ch. 9 (answer strategy), ch. 10 (diagnosis:
  power/coverage), ch. 15–16 boundary. Not a separate inquiry family in the book —
  it is the D+A+diagnosis machinery applied to descriptive inquiries with
  population estimands (PATE vs SATE, ch. 7).

## Position 3 — Prediction (descriptive · unseen cases)

- **Asks:** can we forecast new/unseen cases usefully?
- **Permits:** out-of-sample performance claims against a stated baseline and
  metric: "on held-out cases, beats the baseline by [margin] on [metric]."
- **Does NOT permit:** explanation or causation; feature importance as mechanism;
  any score computed on data the model saw.
- **Taught:** introduced M6 (nb02); **deep dive M25–M26 (nb12)** — target, baseline,
  train/test split, metric, leakage — declared in MIDA form as
  **"Observational: predictive," the design-library entry RDSS stops short of**
  (the book's Part III covers ch. 15–18; nb12 authors the missing entry in the
  book's own declare-diagnose-redesign format; documented in `SOURCE_AUDIT.md` §9).
  In MIDA terms: I = the target defined for unseen units; D = what is honestly
  available at prediction time (leakage = a D violation); A = learner + baseline +
  the entire selection procedure (ch. 9.1.3); diagnosis = held-out performance as
  a diagnosand; redesign = baseline and feature-set comparisons.
- **Datasets:** `la_voter_file.csv` (turnout prediction), incl. one deliberately
  leaky engineered feature.
- **Milestone applications:** each project's prediction-angle decision memo (M25),
  M09 prediction-branch pilots, M19 split/metric perturbation checks.
- **Classic misclassification:** "the model predicts well, so X causes Y" — a
  kind-crossing dressed as performance (the performance-understanding gap, taught
  with the leaky-feature demonstration).
- **RDSS home:** none in Part III (the fresh entry); ch. 9's answer-strategy
  framing and ch. 10's diagnosand logic carry over directly.

## Position 4 — Causal reasoning (causal kind)

- **Asks:** what would happen if we intervened?
- **Permits:** an effect claim **under a stated identification argument**
  (randomization, or a defended observational design).
- **Does NOT permit:** effects when identification assumptions fail or no design
  supplies leverage; "after therefore because."
- **Taught:** introduced M6 (nb02); model/potential outcomes M9 (nb04); assignment
  M16 (nb07); **deep dive M27–M28 (nb13)** — counterfactuals, experiments,
  DiD/RDD/IV intuition; the diagnosis engine (nb11) stress-tests causal designs.
- **Datasets:** `foos_etal.csv` (real randomized GOTV field experiment),
  `cliningsmith_etal.csv`, `bonilla_tillery.csv` (survey experiment; also used for
  measurement in nb05).
- **Milestone applications:** M03 (model + inquiry with DAG), M08 (diagnosis of the
  causal design), M09 causal-branch pilots, the identification paragraph every
  project writes at M27 (or its honest absence).
- **Classic misclassification:** design-mimicry — DiD/RDD/IV vocabulary decorating
  a comparison whose assumptions were never argued (named and drilled in M28).
- **Reach within the causal kind:** SATE vs PATE (ch. 7) — the sample→population
  crossing applies here too; identification licenses the kind, sampling licenses
  the reach.
- **RDSS home:** ch. 6–7 (model/inquiry), ch. 16 "Observational: causal",
  ch. 18 "Experimental: causal" (declaration_18.1 two-arm trial).

## EDA — not a compass position: the explore → declare → confirm loop

Exploratory data analysis has no box on the compass because it is not a kind of
claim — it is what happens **before, inside, and after** declared designs. Its
four homes (all RDSS-native):

| Home | Where taught | RDSS |
|---|---|---|
| Upstream: explore to calibrate M and discover candidate I | nb04 | ch. 6–7 |
| The loop taught by name (exploration → declaration → confirmation) | **nb06 (anchor)** | ch. 15 + ch. 2 |
| Inside A: exploration that influenced estimator choice is part of the declared procedure ("multiple bites at the apple") | nb09 | ch. 9.1.3 |
| Downstream: an unexpected pattern is a *new inquiry* → pivot + reconciliation | nb17, M09 pilots | ch. 22 |

The boundary drilled at the anchor: **an exploratory finding is not a confirmed
claim** — it earns claim status only through declaration (and ideally fresh data).

## Where the classification skill itself lives

| Moment | What happens |
|---|---|
| M5–M6 (nb02) | The compass is taught: kind + reach drills, question cards, class compass-votes |
| M6 | Every project question gets a class-voted compass hypothesis (kind + reach) |
| M17 (nb08) | Applied to a claim in the wild (async diagnosis: which crossing is being smuggled?) |
| M25 | Every project writes a defended prediction-angle verdict |
| M27 | Every project writes its identification paragraph or its honest absence |
| M38 (nb17) | Sensitivity checks branch by compass position — the classification has consequences |
| M42–M43 | The Evidence Defense cross-examines the classification and its boundary |
| M44 (nb19) | One question, every compass position, jointly — the synthesis exercise |

## Combinations (justified, not accidental)

Projects may combine positions when the question demands it (e.g., describe the
sample, generalize to a population, AND probe a causal channel). The rule
(CLAUDE.md Inquiry-Declaration Justification): every position used must state
(1) why the kind and reach fit the question's words, (2) what crossing licenses
it holds, (3) key limitations. The `project/templates/INQUIRY_DECLARATION.md`
template enforces this per project from M03 onward.
