# Course datasets — provenance and attribution

All five CSVs ship from the **`rdss` R package v1.0.14** (Blair, Coppock &
Humphreys, **MIT License**), the companion package to *Research Design in the
Social Sciences: Declaration, Diagnosis, and Redesign* (Princeton University
Press, 2023; free online at book.declaredesign.org).

The package's MIT license requires its notice to travel with every copy, so the
upstream notice is reproduced verbatim in
[`LICENSE-rdss.txt`](LICENSE-rdss.txt) and ships inside `data.zip`. A prose
credit alone does not satisfy the license. **If you download a single CSV from
the raw URL below rather than the zip, download the notice with it** — it lives
at the same base URL.

> **Open rights question (D48, flagged for the instructor).** The package
> license covers the packaged distribution. It does not by itself establish
> that each original investigator authorized public redistribution of the
> underlying study data, and the package documentation restricts the
> LAPOP-derived resample to teaching use. Until a per-file rights record exists
> (original archive or DOI, owner, license or permission, allowed
> transformations, and a hash comparison against the source archive), treat
> these files as *teaching copies whose upstream chain is not fully
> documented*. The studies belong to their original investigators, named in the
> table below.

> **Attribution line (used in every notebook that loads these files):**
> *Dataset from the `rdss` package (Blair, Coppock & Humphreys, MIT License),
> companion to* Research Design in the Social Sciences *(2023).*

| File | Shape | What it is | Course use |
|---|---|---|---|
| `lapop_brazil.csv` | 10,000 × 10 | AmericasBarometer (LAPOP) Brazil survey items — **a 10,000-row resample with replacement of the original**, suitable for planning/teaching, NOT for substantive research claims (per the package documentation; this caveat is itself taught in nb05) | the course workhorse: nb01, nb02, nb03, nb04, nb05, nb06, nb08, nb09, nb10, nb11, nb13, nb16 |
| `la_voter_file.csv` | 1,000 × 4 | Los Angeles voter-file extract (party, age, census tract, 2012 turnout) | known frame for seeded sampling & selection demos: nb01, nb02, nb04, nb05, nb15 |
| `foos_etal.csv` | 8,375 × 5 | Foos et al. UK get-out-the-vote field experiment replication (treatment, 2014 turnout, ward/street, weights) | randomized field experiment: nb05, nb07, nb14, nb15 |
| `cliningsmith_etal.csv` | 958 × 8 | Clingingsmith, Khwaja & Kremer Hajj-lottery study replication (lottery success, views toward other groups) | observational causal: natural experiment / identification (nb05) |
| `bonilla_tillery.csv` | 849 × 10 | Bonilla & Tillery survey experiment replication (treatment `Z`, BLM support, linked fate, demographics) | experimental descriptive: survey experiment as a measurement system (nb05, nb06) |

The `fairfax` shapefile set (spatial, optional) is **not** shipped — no course
unit and no EDR|AI chapter requires spatial data (documented scope decision;
see `planning/SOURCE_AUDIT.md` §6). The book itself needs no external data
file at all: every runnable block in every chapter is a seeded simulation.

## Downloading the bundle

Everything above ships in **`data.zip`** (five CSVs + this README + the MIT
notice), linked from the Material and Schedule pages. Unzip it in your working
directory: it restores the files under `notebooks/data/`, which is the first
local path `load_course_data()` looks in, so the notebooks run offline without
any edit.

Notebooks load these files from the repo's raw GitHub URL with a local-path
fallback, so they work in Colab and locally:

```python
DATA_URL = ("https://raw.githubusercontent.com/davi-moreira/"
            "2026F_evidence_driven_research_purdue_HONR464/main/notebooks/data/")
```
