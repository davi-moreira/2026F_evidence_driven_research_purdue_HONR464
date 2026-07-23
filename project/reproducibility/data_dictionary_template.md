# Data Dictionary Template

*One row per variable, so a stranger knows exactly what each column means, where
it came from, and what a valid value looks like. A dataset without a dictionary is
a pile of numbers no one can check. Include a completed dictionary for every
dataset in your package (M14 capsule).*

---

## Why a data dictionary

Your code is only as trustworthy as your understanding of the data it runs on.
The dictionary is where you write that understanding down: what each variable
measures, in what units, over what range, and how you handled the messy parts.
When a reproducer or a red-teamer questions a number, the dictionary is where they
check whether a value is even possible. It is also where measurement problems
surface before they reach your claim.

Fill one table per dataset. If a variable is one you *created* by transforming
others, its provenance is the transformation itself; say so.

## The template (one table per dataset)

```markdown
## Data dictionary — [dataset file name]
Source: [where this dataset came from] · Version/date: [___] · Rows: [___]

| Variable | Type | Units | Allowed range / values | Source | Transformations | Missingness handling |
|---|---|---|---|---|---|---|
| [name] | [numeric / integer / categorical / date / text / boolean] | [e.g. years, USD, count, unitless] | [e.g. 0–100; {low, med, high}; ≥ 0] | [raw column, or "derived"] | [none, or how it was built/recoded] | [how missing values are treated, and how many] |
```

## Field guidance

- **Variable** — the exact column name in your data, so it matches the code.
- **Type** — numeric, integer, categorical, date, text, or boolean. The type tells
  a reproducer what operations are even valid on the column.
- **Units** — the real-world unit (years, dollars, counts, a 1–5 scale). "Unitless"
  is a valid answer; a blank is not. Many silent errors are unit confusions.
- **Allowed range / values** — the values a *valid* entry can take. A number
  outside this range is a data-quality flag, and the dictionary is what makes that
  flag visible.
- **Source** — the raw column it came from, or "derived" if you built it.
- **Transformations** — every recode, rescale, or computation you applied. If you
  turned a date into an age, or binned a continuous score, it goes here. A number
  that appears with no transformation trail is a lineage gap.
- **Missingness handling** — how missing values are treated (dropped, imputed,
  kept as a category) and *how many* there were. Undocumented row-dropping is one
  of the package sins; this column is where you prevent it.

## Worked row (illustrative shape, not real data)

```markdown
## Data dictionary — example_survey.csv
Source: [survey source] · Version/date: 2026 access · Rows: 1,200

| Variable | Type | Units | Allowed range / values | Source | Transformations | Missingness handling |
|---|---|---|---|---|---|---|
| respondent_id | integer | unitless | ≥ 1, unique | raw | none | none missing |
| age | integer | years | 18–90 | raw | none | 14 missing; rows kept, age unused for those |
| support | categorical | unitless | {oppose, neutral, support} | raw | none | 3 missing; dropped, logged in decision log |
| age_group | categorical | unitless | {18–29, 30–49, 50+} | derived | binned from `age` | inherits age missingness |
```

Notice the last two columns carry the weight: they are where a reproducer learns
that three rows were dropped and one variable was built from another. That is the
lineage the red-team traces.

## Quality bar

- ☐ Every variable the notebook uses has a row.
- ☐ Every "derived" variable names the transformation that built it.
- ☐ Every allowed range is specific enough to flag an impossible value.
- ☐ Missingness is stated with a count and a handling rule, not left blank.
- ☐ Dropped rows are recorded here and cross-referenced in the decision log.

## Common failure modes

1. **A blank units column.** "It's obvious" is how unit errors survive. State it.
2. **Silent derivation.** A column that appears from nowhere with no transformation
   trail cannot be trusted or reproduced.
3. **Undocumented missingness.** Rows dropped with no count and no rule is one of
   the five package sins; the dictionary is the first place to catch it.
4. **A dictionary that drifts from the code.** If you rename a column in the
   notebook, rename it here. A stale dictionary misleads worse than none.

---

*Part of the reproducibility package. See also:
[README_template.md](README_template.md) ·
[clean_run_checklist.md](clean_run_checklist.md) ·
[reproducibility_capsule_template.md](reproducibility_capsule_template.md).*
