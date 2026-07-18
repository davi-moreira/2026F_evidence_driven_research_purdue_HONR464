# QUANTITATIVE_APPROACH_MAP — the four approaches across HONR 46400

The course's signature skill is **classifying a research question into one (or a
justified combination) of four quantitative approaches**, then holding every claim
inside its approach's boundary. This map is the operational reference: what each
approach is, where it is taught, where it is practiced, and where students must
apply it to their own projects. Machine-readable core: `course_config.yaml`
`approaches:`. Per-meeting detail: `planning/MEETING_SCHEDULE.csv` (`approach`,
`claim_permitted`, `claim_not_permitted` columns).

## The 2×2 the course teaches

|  | **Looks at the world as it is** | **Asks about intervening / the future** |
|---|---|---|
| **Pattern** | **Description** — what is observed here? | **Prediction** — can we forecast new cases? |
| **Process** | **Statistical/observational inference** — what generalizes, with how much uncertainty? | **Causal reasoning** — what would an intervention change? |

(The grid is a teaching device introduced in nb02; the four columns of
`course_config.yaml` are authoritative.)

## 1. Description

- **Asks:** what is observed in the data at hand — patterns, distributions, differences.
- **Permits:** statements about these data: "in these 10,000 interviews, X% report Y."
- **Does NOT permit:** generalization beyond the sample; causal readings.
- **Taught:** introduced M5 (nb02); **deep dive M13–M14 (nb06)**; exercised in the
  claim map (M8), honest visualization (M14), and every "Table 1" a project builds.
- **Datasets:** `lapop_brazil.csv` (with its 10k-resample provenance caveat, taught
  explicitly), `la_voter_file.csv`.
- **Milestone applications:** M02 (describing what sources claim), M04 (indicator
  distributions), M09 description-branch pilots, poster "what the data show" blocks.
- **Classic misclassification:** a descriptive question dressed in causal language
  ("does social media *make* students anxious?" when the student means "how anxious
  are students who use social media?").
- **RDSS home:** ch. 15 "Observational: descriptive" (+ ch. 17 for descriptive
  quantities measured by experiments).

## 2. Statistical / observational inference

- **Asks:** what holds beyond the sample — population/process estimates.
- **Permits:** estimates with quantified uncertainty for the population the frame
  reaches: "X ± interval among the population my sampling procedure covers."
- **Does NOT permit:** causal claims from association; generalization past the frame.
- **Taught:** introduced M5 (nb02); data strategy M15–M16 (nb07); answer strategy
  M18–M19 (nb09); **deep dive M20–M22 (nb10)** — uncertainty, generalization,
  power; async claim diagnosis M17 (nb08).
- **Datasets/simulations:** `lapop_brazil.csv`, `la_voter_file.csv`, seeded
  sampling-distribution and power simulations (seed 464).
- **Milestone applications:** M05 (data strategy), M06 (answer strategy), M07
  (declaration + abstract uncertainty language), M09 inference-branch pilots,
  M14 (uncertainty statement).
- **Classic misclassification:** the "silent upgrade" — association → link →
  impact → effect across a paragraph (taught by name in M21).
- **RDSS home:** ch. 8 (data strategy), ch. 9 (answer strategy), ch. 10 (diagnosis:
  power/coverage), ch. 15–16 boundary.

## 3. Predictive modeling

- **Asks:** can we forecast new/unseen cases usefully?
- **Permits:** out-of-sample performance claims against a stated baseline and
  metric: "on held-out cases, beats the baseline by [margin] on [metric]."
- **Does NOT permit:** explanation or causation; feature importance as mechanism;
  any score computed on data the model saw.
- **Taught:** introduced M6 (nb02); **deep dive M25–M26 (nb12)** — target, baseline,
  train/test split, metric, leakage. Built fresh with scikit-learn (RDSS treats
  prediction lightly — documented in `SOURCE_AUDIT.md` §9).
- **Datasets:** `la_voter_file.csv` (turnout prediction), incl. one deliberately
  leaky engineered feature.
- **Milestone applications:** each project's prediction-angle decision memo (M25),
  M09 prediction-branch pilots, M19 split/metric perturbation checks.
- **Classic misclassification:** "the model predicts well, so X causes Y" — the
  performance-understanding gap, taught with the leaky-feature demonstration.
- **RDSS home:** none substantive (fresh unit); ch. 9's answer-strategy framing
  carries over conceptually.

## 4. Causal reasoning

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
- **RDSS home:** ch. 6–7 (model/inquiry), ch. 16 "Observational: causal",
  ch. 18 "Experimental: causal" (declaration_18.1 two-arm trial).

## Where the classification skill itself lives

| Moment | What happens |
|---|---|
| M5–M6 (nb02) | The skill is taught: drills, question cards, class approach-votes |
| M6 | Every project question gets a class-voted approach hypothesis |
| M17 (nb08) | Applied to a claim in the wild (async diagnosis) |
| M25 | Every project writes a defended prediction-angle verdict |
| M27 | Every project writes its identification paragraph or its honest absence |
| M38 (nb17) | Sensitivity checks branch by approach — the classification has consequences |
| M42–M43 | The Evidence Defense cross-examines the classification and its boundary |
| M44 (nb19) | One question analyzed all four ways, jointly — the synthesis exercise |

## Combinations (justified, not accidental)

Projects may combine approaches when the question demands it (e.g., describe the
sample, infer to a population, AND probe a causal channel). The rule (CLAUDE.md
Method-Selection Justification): every family used must state (1) why it fits,
(2) what it can/cannot establish, (3) key limitations. The
`project/templates/QUANTITATIVE_APPROACH_DECLARATION.md` template enforces this
per project from M03 onward.
