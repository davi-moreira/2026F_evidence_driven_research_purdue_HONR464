# Research-Package README Template

*The front door to your research package. A stranger opens this file first and
should learn, in one read, what you asked, how you answered it, and how to rebuild
every number. Fill every block. Reused as the top of your reproducibility capsule
(M14) and your final chapter's package (M15).*

---

## How to use this

Copy the skeleton below into a file named `README.md` at the top of your package.
Replace every bracketed prompt with your own content, and delete the guidance
italics. A good README lets a competent stranger run your notebook and reach your
headline number without asking you a single question. That is the bar the M13
red-team and the M14 capsule are checked against.

Keep it honest: the README describes what the package *actually does*, not what
you meant it to do. If a step is manual, say so. If a number takes ten minutes to
compute, say so.

## The skeleton

```markdown
# [Project title]

## Question
[One sentence. Units, outcome, comparison, and scope visible in the sentence.]

## Design pathway and compass position
- **Compass position:** [Description | Generalization | Prediction | Causal reasoning]
  ([kind] · [reach: data at hand / population / unseen cases])
- **Design pathway:** [observational descriptive | observational causal |
  experimental descriptive | prediction | experimental causal | cross-cutting]
- **What this position lets me claim:** [one sentence, inside the boundary]
- **What it does NOT let me claim:** [the nearest overreach, forbidden]

## Data sources and provenance
| Dataset (file) | Source | Version / date | License / use terms |
|---|---|---|---|
| [file.csv] | [where it came from] | [version or access date] | [license, attribution] |
[One row per dataset. Every file the notebook reads appears here.]

## Environment
- Runs on: Google Colab (Python 3.11)
- Seed: SEED = 464 (np.random.default_rng)
- Key packages: [name==version for anything whose default could shift a result]
- See [environment_documentation.md](environment_documentation.md) and
  [seed_policy.md](seed_policy.md).

## Run order
1. [Open the notebook in Colab via the badge, OR: notebook file name.]
2. Runtime → Restart and run all.
3. [Any one-time step, e.g. "accept the data-download cell"; ideally none.]
[The package should run top to bottom with no manual intervention. If it cannot,
that is a defect to fix, not a step to document around.]

## Expected outputs and runtimes
| Output | Where it appears | Approx. runtime |
|---|---|---|
| [headline number] | [cell / section] | [seconds] |
| [main figure] | [cell / section] | [seconds] |
[List what a correct run produces, so a reproducer knows what "it worked" looks
like.]

## Verification map
| Claim / number | How it was verified | Ledger / cell reference |
|---|---|---|
| [headline] | [named method] | [row # / cell] |
[Every reported number maps to the verification that stands behind it. This is
the lineage a red-teamer traces: data → code → number → claim.]

## AI disclosure
This package used AI as documented in the AI Research Ledger.
See: [path to your finalized ledger].
```

## Quality bar before you ship the README

- ☐ A stranger could reach the headline number from this file alone.
- ☐ Every dataset the notebook loads has a provenance row.
- ☐ The run order is truly "restart and run all," with no by-hand steps hidden in
  prose.
- ☐ The compass position and its claim boundary are stated, not just the topic.
- ☐ The verification map connects every reported number to a named check.
- ☐ The AI-ledger pointer resolves to a real, finalized ledger.

## Common failure modes

1. **A README that describes the intention, not the package.** If the notebook
   does not actually run top to bottom, fix the notebook; do not paper over it.
2. **Missing a dataset in the provenance table.** Every file the code reads must
   appear, with its license. A silent data source is an integrity gap.
3. **No claim boundary.** Naming the topic is not naming the position. State what
   the design can and cannot establish.
4. **A number with no verification-map row.** An unverified reported number is the
   defect the whole package exists to prevent.

---

*Part of the reproducibility package. See also:
[data_dictionary_template.md](data_dictionary_template.md) ·
[clean_run_checklist.md](clean_run_checklist.md) ·
[reproducibility_capsule_template.md](reproducibility_capsule_template.md).*
