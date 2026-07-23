# Seed Policy

*One page on the course seed: what it is, how to set it, what it does and does not
cover, and how to report the leftover randomness a seed cannot remove. Every
stochastic step in every notebook is seeded with 464.*

---

## The rule

Every random step in the course is seeded with **464** (the course number),
through a single generator created once in the setup cell:

```python
import numpy as np
SEED = 464
rng = np.random.default_rng(SEED)
```

From then on, every random draw goes through `rng`, not through the older global
`np.random.*` functions. One generator, seeded once, used everywhere. This is what
makes every simulation in your package identical from one run to the next.

## Why 464 and why one generator

The value is arbitrary on purpose; it is the course number so it is easy to
remember and consistent across every notebook. What matters is not the number but
that it is **fixed and shared**. Using `np.random.default_rng(SEED)` and threading
one `rng` through the notebook is more reliable than scattering `np.random.seed()`
calls, because there is a single, explicit source of randomness a reader can point
to.

Pass `rng` to anything that draws:

```python
sample = rng.choice(data, size=100, replace=False)
noise  = rng.normal(0, 1, size=len(df))
```

For scikit-learn steps that take a `random_state`, pass an integer seed derived
from the policy (for example `random_state=SEED`) so those steps are pinned too.

## What a seed covers

A seed makes **pseudo-random** steps reproducible: simulations, random samples,
shuffles, bootstrap resamples, random train/held-out splits, any model with a
random initialization. Run the notebook twice and these produce byte-identical
results. That is the whole value: your reported number is the same number every
time, so it can be claimed and checked.

## What a seed does NOT cover

A seed is not a magic wand. It does not fix:

- **Non-random nondeterminism.** Some parallel computations and certain
  hardware-dependent operations can vary slightly regardless of the seed. The seed
  has no authority over these.
- **Floating-point ordering.** Summing numbers in a different order can change the
  last decimal places. A seed does not control this.
- **External changes.** If the *data* changes, or a *package version* changes a
  default, the seed cannot save you. That is why data provenance and the
  [environment documentation](environment_documentation.md) sit alongside this
  policy.
- **Your own manual steps.** A number "corrected by hand" in a cell is outside the
  seed's reach and outside reproducibility entirely. Do it in code or log it.

## How to state residual non-determinism

When a step is not fully deterministic even with the seed, you do not hide it, and
you do not pretend to a precision you lack. You report it plainly:

> *"The headline estimate is seeded and reproduces exactly. The bootstrap interval
> may vary in its last reported digit across runtimes due to floating-point
> ordering; I report it to \[N] significant figures, within which it is stable."*

An honest statement of residual variation is graded as good practice. A false
claim of exact reproduction, when a reproducer then gets a different number, is
the failure this policy exists to prevent.

## Quality bar

- ☐ `SEED = 464` and `rng = np.random.default_rng(SEED)` are in the setup cell.
- ☐ Every random draw uses `rng` (no stray global `np.random.*` calls).
- ☐ Every scikit-learn step that accepts `random_state` receives the seed.
- ☐ The notebook gives the same headline number on two consecutive clean runs.
- ☐ Any residual non-determinism is stated, with the precision you actually claim.

---

*Part of the reproducibility package. See also:
[environment_documentation.md](environment_documentation.md) ·
[clean_run_checklist.md](clean_run_checklist.md) ·
[README_template.md](README_template.md).*
