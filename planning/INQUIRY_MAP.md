# INQUIRY_MAP — the inquiry compass and the design library across HONR 46400 (v2)

The course's signature skill is **classifying a research question with the
inquiry compass**, then holding every claim inside the boundary that
classification draws, and then **matching the classified question to a design
pathway**. Two layers, one shared axis (**kind**):

- **Compass (RDSS ch. 7) — classifies QUESTIONS** by kind × reach. Taught in
  Week 2 (`nb01`); used in every declaration from M3 onward.
- **Design library (RDSS ch. 15–18) — organizes DESIGNS** by kind × data
  strategy. Gives Weeks 5–9 (`nb04`–`nb08`) their sequence.

Machine-readable core: `course_config.yaml inquiry_framework:` (positions,
crossings, and `pathways:`). The v1 map is preserved at git tag
`v1-compass-build`; its compass definitions, crossing licenses, and named
violations are carried forward here unchanged.

## The two classifying questions (the compass)

1. **KIND — descriptive or causal?** Does answering require a counterfactual
   contrast (what would differ under an intervention), or only the world as it
   is or was?
2. **REACH — for which units must the answer hold?** The data at hand · a
   population beyond the data · cases not yet seen.

| | **Reach: data at hand** | **Reach: a population** | **Reach: unseen cases** |
|---|---|---|---|
| **Descriptive** | **Description** | **Generalization** | **Prediction** |
| **Causal** | **Causal reasoning** (identification licenses the kind; sampling licenses the reach) | | |

The four named positions are *derived* from the two-kind split, not standing
beside it. All four are introduced together when the compass is taught (`nb01`);
each is deepened later inside its matched pathway.

## Crossings, licenses, and named violations — the claim-boundary discipline

Every overclaim in the wild is a **compass crossing without its license**. The
license is always a design element (a data strategy D or answer strategy A), and
the proof is always diagnosis:

| Crossing | License (RDSS home) | Named violation (drilled) |
|---|---|---|
| sample → population | sampling data strategy (ch. 8) + uncertainty-bearing answer strategy (ch. 9) + diagnosis: coverage/power (ch. 10) | **the silent upgrade** |
| observed → unseen | prediction-time-honest data strategy (no leakage) + held-out diagnosands + baseline comparison under redesign | **leakage**; "tomorrow resembles the training data" |
| descriptive → causal | assignment strategy (ch. 8, 18) or a defended observational identification argument (ch. 16) | **after-therefore-because**; **design mimicry** |

> You buy KIND and REACH with your data strategy, and you prove the purchase
> with diagnosis.

## Position 1 — Description (descriptive · data at hand)

- **Asks:** what is observed in the data at hand — patterns, distributions, differences.
- **Can establish:** statements about these units ("in these 10,000 interviews, X% report Y").
- **Cannot establish:** any reach beyond these units; causal readings.
- **Taught:** classification in `nb01`; design deep dive in `nb04`.
- **Classic misclassification:** a descriptive question dressed in causal language
  ("does social media *make* people anxious?" when the real question is "how
  anxious are heavy users?").
- **RDSS home:** ch. 15 (observational descriptive); ch. 17 for descriptive
  quantities measured *by* experiments.

## Position 2 — Generalization (descriptive · population)

- **Asks:** what holds beyond the sample — population or process estimates.
- **Can establish:** estimates with quantified uncertainty for the population the
  sampling frame reaches ("X ± interval among the population my procedure covers").
- **Cannot establish:** causation from association; reach past the frame.
- **Taught:** classification in `nb01`; design deep dive in `nb04` (sampling +
  uncertainty).
- **Classic misclassification:** the **silent upgrade** — association → link →
  impact → effect across a paragraph; reach claimed with no sampling design behind it.
- **RDSS home:** ch. 8 (data strategy), ch. 9 (answer strategy), ch. 10
  (diagnosis: power/coverage). Not a separate design family — it is the
  D + A + diagnosis machinery applied to descriptive inquiries with population
  estimands (SATE vs PATE, ch. 7).

## Position 3 — Prediction (descriptive · unseen cases)

- **Asks:** can we forecast new or unseen cases usefully?
- **Can establish:** out-of-sample performance against a stated baseline and metric
  ("on held-out cases, beats the baseline by [margin] on [metric]").
- **Cannot establish:** explanation or causation; feature importance as mechanism;
  any score computed on data the model already saw.
- **Prediction is a distinct answer objective** — generalization to unseen
  observations. It is **never** forced into the descriptive-vs-causal or
  observational-vs-experimental grids. In MIDA terms: I = the target for unseen
  units; D = what is honestly available at prediction time (leakage = a D
  violation); A = learner + baseline + the whole selection procedure (ch. 9.1.3);
  diagnosis = held-out performance; redesign = baseline and feature-set comparisons.
- **Taught:** classification in `nb01`; design deep dive in `nb07`, the
  course-authored library entry written in the book's declare-diagnose-redesign
  format (RDSS Part III stops short of a predictive entry).
- **Classic misclassification:** "the model predicts well, so X causes Y" — a
  kind-crossing dressed as performance (the performance-understanding gap).

## Position 4 — Causal reasoning (causal kind)

- **Asks:** what would happen if we intervened?
- **Can establish:** an effect **under a stated identification argument**
  (randomized assignment, or a defended observational design).
- **Cannot establish:** effects when identification assumptions fail or no design
  supplies leverage; "after therefore because."
- **Taught:** classification in `nb01`; design deep dives in `nb05` (observational
  causal: selection-on-observables, DiD, IV, RDD, natural experiments) and `nb08`
  (experimental causal: two-arm trials, blocking, cluster + factorial designs).
- **Reach within the causal kind:** SATE vs PATE (ch. 7) — the sample → population
  crossing applies here too; identification licenses the kind, sampling licenses
  the reach.
- **Classic misclassification:** **design mimicry** — DiD/RDD/IV vocabulary
  decorating a comparison whose assumptions were never argued.
- **RDSS home:** ch. 6–7 (model/inquiry), ch. 16 (observational causal), ch. 18
  (experimental causal).

## The design-pathway layer (Weeks 5–9)

The design library adds the axis the compass leaves open: **data strategy**
(observational vs experimental). Five pathways cover the space, plus prediction
as its own objective (`course_config.yaml pathways:`):

| Wk | Pathway | NB | RDSS | Example designs |
|---|---|---|---|---|
| 5 | Observational descriptive | `nb04` | ch. 15 | sample surveys, indices, case selection |
| 6 | Observational causal | `nb05` | ch. 16 | selection-on-observables, DiD, IV, RDD, natural experiments |
| 7 | Experimental descriptive | `nb06` | ch. 17 | audit, list, conjoint experiments; behavioral games; measurement experiments |
| 8 | Prediction | `nb07` | course-authored entry | baseline vs model, held-out evaluation, calibration |
| 9 | Experimental causal | `nb08` | ch. 18 | two-arm trials, blocking, cluster + factorial designs |

**Experimental assignment does NOT imply a causal inquiry.** Week 7 exists to
make this concrete: **experimental descriptive** designs (audit, list, conjoint,
behavioral games) use random assignment to *measure a descriptive quantity*, not
to identify a causal effect. Assignment is a data-strategy move; whether the
inquiry is causal is a question-kind matter decided on the compass.

## From question to design — the declaration matrix

A declaration commits a **compass position** (kind × reach, read off the
question's words) and a **pathway** (kind × data strategy, read off what the
student can actually do). The two must share the same **kind**; the pathway then
fixes the data strategy and names the crossing that must be licensed:

| Compass position (question) | Data strategy | Pathway (design) | Crossing to license |
|---|---|---|---|
| Description (descriptive · at hand) | observational | Observational descriptive (`nb04`) | none — the answer stays at hand |
| Description (descriptive · at hand) | experimental | Experimental descriptive (`nb06`) | none — an experiment *measures* a descriptive quantity |
| Generalization (descriptive · population) | observational + sampling | Observational descriptive + sampling (`nb04`) | sample → population |
| Prediction (descriptive · unseen) | prediction-time-honest | Prediction entry (`nb07`) | observed → unseen |
| Causal reasoning (causal · at hand/population) | observational | Observational causal (`nb05`) | descriptive → causal, via a defended identification argument |
| Causal reasoning (causal · at hand/population) | experimental | Experimental causal (`nb08`) | descriptive → causal, via randomized assignment |

**How a student moves across the matrix.** They classify the question on the
compass (M1), commit to a position and its permitted claim in the MIDA
declaration (M3), then select the pathway whose kind matches and whose data
strategy is feasible — auditing it against its crossing license (M4 onward). The
same descriptive question may be served observationally or experimentally; the
same causal question may be identified observationally or by assignment;
prediction sits outside both grids as its own objective. The
`project/templates/INQUIRY_DECLARATION.md` template enforces, per project, the
three required justifications (CLAUDE.md Inquiry-Declaration rule): (1) why the
kind and reach fit the question's words, (2) which crossing license the design
holds, and (3) key limitations and sources of uncertainty.

## Where the classification and matching skill lives

| Moment | What happens |
|---|---|
| Week 2 (`nb01`), M1 | The compass is taught (kind + reach drills); each project question gets a classified position |
| M3 | The MIDA declaration commits the position and its permitted claim |
| Weeks 5–9 (`nb04`–`nb08`), M4–M8 | Each pathway is deepened; the project's design is matched and audited against its crossing license |
| M5 (GenAI Studio: Causal Identification Skeptic) | The identification paragraph — or the honest causal-language boundary — is defended |
| M7 (GenAI Studio: Prediction & Leakage Auditor) | The declared analysis protocol; leakage and baseline honesty are audited |
| M9 / M13 | Robustness and replication branch by position — the classification has consequences |
| M15 (final defense) | The Evidence Defense cross-examines the classification, the pathway match, and the claim boundary |

## Combinations (justified, not accidental)

Projects may combine positions when the question demands it (describe the sample,
generalize to a population, and probe a causal channel). The rule is unchanged:
every position and pathway used must state why the kind and reach fit, which
crossing license it holds, and its limitations. A declaration with no stated
justification or limitation is incomplete.
