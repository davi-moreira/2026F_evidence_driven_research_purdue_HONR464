# Environment Documentation

*How to record the computing environment so your results do not drift when someone
else runs them. Colab-first, because that is where the course lives. A number that
depends on an unrecorded package version is a number no one can reliably reproduce.*

---

## Why the environment matters

The same code can give different answers on different setups: a package updates a
default, a Python version changes a behavior, a random step is unseeded. Recording
the environment is how you make "it worked on my machine" into "it works on
anyone's machine." For an honors project with no computing background assumed, the
good news is that Colab does most of this for you, and the rest is a short, fixed
routine.

## Colab is the standard environment

The course runs on **Google Colab, Python 3.11**. Using Colab as the shared
environment removes most reproducibility problems for free: everyone starts from
the same base image, so you are not debugging five different laptops. Build and
submit your package as a Colab notebook opened through the course badge, and a
reproducer opens the identical environment with one click.

## The three things to record

**1. The Python version.** State it in the README and confirm it in the notebook.
A single cell makes it self-documenting:

```python
import sys
print("Python", sys.version.split()[0])   # expect 3.11.x on Colab
```

**2. Package versions, where a default could move your result.** You do not need
to pin everything. You need to pin the packages whose behavior, if it changed,
would change a number you report. When in doubt about one, pin it. Record versions
with a cell like:

```python
import numpy, pandas
print("numpy", numpy.__version__, "| pandas", pandas.__version__)
# add any package whose default feeds your headline number
```

If a specific version matters, install it explicitly at the top of the notebook so
the environment is rebuilt the same way every time:

```python
# Pin only what must not drift. Example form:
# !pip install -q "pandas==2.2.2"
```

Keep pins minimal and purposeful. A wall of pins nobody understands is its own
kind of unreproducible.

**3. The seed.** Every stochastic step is seeded with the course seed so
simulations are identical run to run. This is covered in full in
[seed_policy.md](seed_policy.md); the environment's job is to make the seed
visible in the setup cell:

```python
import numpy as np
SEED = 464                       # course number
rng = np.random.default_rng(SEED)
```

## Why determinism matters

**Determinism** means the notebook produces the *same* output every time it runs,
given the same inputs. It matters for one blunt reason: if your own notebook gives
a different headline number each run, you cannot claim any of them, and a
reproducer cannot confirm any of them. Determinism is what makes a number a
finding instead of a coincidence. The seed plus a recorded environment is what
buys it.

Some steps are legitimately not fully deterministic even with a seed (certain
parallel or hardware-dependent operations). When that is true, you say so and
report the residual variation honestly, rather than pretending to a precision you
do not have.

## How to record the runtime

Along with versions, note two practical facts a reproducer needs:

- **Runtime type.** In Colab, `Runtime → Change runtime type`. Record whether you
  used the default CPU runtime (almost always sufficient for this course) or
  something else. If a GPU or high-RAM runtime was needed, that is part of the
  environment and must be stated.
- **Approximate wall-clock time** for a full restart-and-run-all, so a reproducer
  knows whether a ten-minute wait is normal or a sign something hung.

Put both in the README's environment and expected-outputs blocks.

## The environment block to paste in your README

```
## Environment
- Platform: Google Colab, Python 3.11 (confirmed in setup cell)
- Runtime type: [default CPU | other — state it]
- Seed: SEED = 464 via np.random.default_rng
- Pinned packages (only those that must not drift): [name==version, ...]
- Full restart-and-run-all takes approximately [___] on the default runtime.
```

## Quality bar

- ☐ The notebook prints its Python version in a cell.
- ☐ Versions of result-critical packages are printed and, where needed, pinned.
- ☐ The seed is set in the setup cell and visible.
- ☐ The runtime type and approximate run time are recorded.
- ☐ Any known non-determinism is stated, not hidden.

---

*Part of the reproducibility package. See also:
[seed_policy.md](seed_policy.md) · [clean_run_checklist.md](clean_run_checklist.md)
· [README_template.md](README_template.md).*
