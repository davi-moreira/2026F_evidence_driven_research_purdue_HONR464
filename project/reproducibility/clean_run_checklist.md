# Clean-Run Checklist

*The final pass before you call a package reproducible. "It works on my machine" is
an untested claim; a clean run is the test. Walk this checklist, then run it once
more from a fresh kernel. If it does not pass for you, it will not pass for the
red-teamer.*

---

## What a clean run proves

A clean run is a single, uninterrupted execution of your notebook from an empty
kernel, top to bottom, that reproduces every number you report with no human
touching anything in between. It is the difference between believing your package
works and knowing it does. Everything in the M13 red-team and the M14 capsule
rests on this passing.

Do it *before* you hand the package to anyone. The whole point of the exchange is
that a stranger runs it cold; you do not want them discovering a break you could
have caught yourself.

## The checklist

Run through every line. A single unchecked box means the package is not yet clean.

- ☐ **Restart and run all passes.** In Colab, `Runtime → Restart and run all`
  completes with no error, from a fresh kernel, with no cells run out of order
  beforehand.
- ☐ **Top-to-bottom, no manual intervention.** No cell needs you to click, paste,
  edit a value, or run something by hand mid-way. If it does, fix the notebook.
- ☐ **The kernel exits clean.** No red error output anywhere; no cell left in a
  running or stalled state at the end.
- ☐ **Outputs match the reported numbers.** The headline number, and every number
  in your README and claim table, matches what the fresh run actually produces.
  If a reported number and the run disagree, the reported one is wrong.
- ☐ **No absolute paths.** No `/Users/you/...` or `C:\...` anywhere. Data loads by
  the course loader or a documented public URL, never a path only your laptop has.
- ☐ **Data loads from the public source.** The notebook pulls its data the way a
  stranger's would (the GitHub raw URL via `load_course_data`, or a documented
  source), not from a local file only you possess.
- ☐ **Figures regenerate.** Every figure you report is drawn by the run itself, not
  pasted in as a static image from an earlier session.
- ☐ **Seed is set and honored.** `SEED = 464`, one `rng`, every random step through
  it; two consecutive runs give the same headline number (see
  [seed_policy.md](seed_policy.md)).
- ☐ **The ledger is present and finalized.** The AI Research Ledger is in the
  package and complete, not left for the dossier deadline.
- ☐ **The AI disclosure is present.** The package points to the finalized ledger
  and states how AI was used and verified.

## The five package sins (kill them here)

These are the recurring breaks a clean run exposes. Find and fix each before the
exchange.

| Sin | What it looks like | Fix |
|---|---|---|
| **Hard-coded path** | `/Users/me/Desktop/data.csv` | Load via the course loader or a documented public URL. |
| **Missing seed** | a draw that differs every run | Seed every stochastic step through `rng`. |
| **By-hand edit** | a number "corrected" in the cell, not the code | Do it in code, or log it in the decision log. |
| **Undocumented exclusion** | rows dropped with no reason recorded | State the rule and its rationale in the data dictionary and decision log. |
| **Stale data / output** | notebook reads an old file, or shows an old pasted figure | Re-point to current data; regenerate every figure in the run. |

## The self-test before the exchange

The strongest version of this checklist is a rehearsal of the real thing:

1. Restart the kernel completely (not just "run all" from a warm state).
2. Run the whole notebook once, untouched.
3. Read your headline number off the fresh output and compare it to your README.
4. If they match and no box above is unchecked, the package is clean.
5. If anything breaks, fix the *cause*, not the symptom, and start over from step
   one.

A package that passes this for you is a package that will survive a stranger. One
that you have never run from a cold kernel is an untested claim, no matter how sure
you feel.

## Common failure modes

1. **"Run all" from a warm kernel.** Variables from earlier runs can mask a break.
   Restart first, always.
2. **Reporting a number the clean run does not produce.** The run is the truth; the
   reported number must match it, not the other way around.
3. **A pasted figure.** A static image hides whether the code still makes it.
   Regenerate every figure in the run.
4. **Fixing the symptom.** Patching one number by hand re-commits the by-hand-edit
   sin. Fix the code that produces it.

---

*Part of the reproducibility package. See also:
[README_template.md](README_template.md) · [seed_policy.md](seed_policy.md) ·
[replication_report_template.md](replication_report_template.md) (what the
red-teamer does with your clean run) ·
[reproducibility_capsule_template.md](reproducibility_capsule_template.md).*
