# Course datasets — provenance and attribution

All five CSVs ship from the **`rdss` R package v1.0.14** (Blair, Coppock &
Humphreys, **MIT License**), the companion package to *Research Design in the
Social Sciences: Declaration, Diagnosis, and Redesign* (Princeton University
Press, 2023; free online at book.declaredesign.org). Files are byte-identical
to the book's replication archive.

The MIT license permits this redistribution and requires that its notice travel
with every copy, so the upstream notice is reproduced verbatim in
[`LICENSE-rdss.txt`](LICENSE-rdss.txt) and ships inside the dataset zip. A
prose credit alone does not satisfy the license. The studies behind these files
belong to their original investigators, named in the table below and cited in
the book wherever a dataset is used.

> **Attribution line (used in every notebook that loads these files):**
> *Dataset from the `rdss` package (Blair, Coppock & Humphreys, MIT License),
> companion to* Research Design in the Social Sciences *(2023).*

| File | Shape | What it is | Course use |
|---|---|---|---|
| `lapop_brazil.csv` | 10,000 × 10 | AmericasBarometer (LAPOP) Brazil survey items — **a 10,000-row resample with replacement of the original**, suitable for planning/teaching, NOT for substantive research claims (per the package documentation; this caveat is itself taught in nb05 and nb07) | observational descriptive summaries: distribution, relationship, index + nonresponse stress-test (nb05); also question framing (nb02), robustness (nb10), research note (nb15) |
| `la_voter_file.csv` | 1,000 × 4 | Los Angeles voter-file extract (party, age, census tract, 2012 turnout) | known frame for seeded sampling & selection demos (nb05); readiness demo (nb01); prediction target + train/test split (nb08) |
| `foos_etal.csv` | 8,375 × 5 | Foos et al. UK get-out-the-vote field experiment replication (treatment, 2014 turnout, ward/street, weights) | experimental causal: randomized field experiment (nb09); reproduced in the replication module (nb14) |
| `cliningsmith_etal.csv` | 958 × 8 | Clingingsmith, Khwaja & Kremer Hajj-lottery study replication (lottery success, views toward other groups) | observational causal: natural experiment / identification (nb06) |
| `bonilla_tillery.csv` | 849 × 10 | Bonilla & Tillery survey experiment replication (treatment `Z`, BLM support, linked fate, demographics) | experimental descriptive: survey experiment as a measurement system (nb07) |

The book's `fairfax` shapefile set (spatial, optional) is **not** shipped —
no course unit requires spatial data (documented scope decision;
see `planning/SOURCE_AUDIT.md` §6).

Notebooks load these files from the repo's raw GitHub URL with a local-path
fallback, so they work in Colab and locally:

```python
DATA_URL = ("https://raw.githubusercontent.com/davi-moreira/"
            "2026F_evidence_driven_research_purdue_HONR464/main/notebooks/data/")
```
