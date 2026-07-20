# Course figures — inventory, assignments, and attribution

Every figure was **visually inspected before captioning** (evidence-integrity
rule). Notebooks embed them via the raw GitHub URL so they render in Colab:

```
https://raw.githubusercontent.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/main/notebooks/figures/<file>
```

## Sources & attribution lines (used verbatim in notebooks)

1. **RDSS replication archive** (`rdss_fig_*.png`, converted from the PDF
   figures in the book's MIT-licensed replication materials):
   *"Figure from the replication materials of Blair, Coppock & Humphreys
   (2023), Research Design in the Social Sciences (MIT-licensed archive; the
   book is free at book.declaredesign.org)."*
   Embedding these was an explicit instructor decision (2026-07-18),
   superseding the earlier re-implement-only default in SOURCE_AUDIT §8.
2. **Professor Moreira's QM 67000 Business Analytics slides** (his own
   material): *"From Professor Moreira's QM 67000 Business Analytics slides."*
3. **Personal photos** (nb00 introduction): Professor Moreira's own.
4. `steve-jobs-pie.jpg`: Apple keynote photograph (2008) — a classic
   visualization-criticism case, used in Professor Moreira's slides.

## Assignments (file → notebook · what it shows)

| File | NB | Shows |
|---|---|---|
| davi_moreira_photo.jpg | nb00 | the professor |
| palmeiras_logo.png / palmeiras_stadium.jpg | nb00 | Palmeiras (instructor's passion) |
| carnaval_olinda.jpg | nb00 | Olinda carnival (instructor's passion) |
| rdss_fig_2_1.png | nb00, nb02, nb12, nb19 | the MIDA map: M·I·D·A, theoretical/empirical, reality/simulation (nb02: compass→MIDA preview; nb12: declaring the predictive design) |
| random_assignment_sampling.png | nb02 | random sampling × random assignment → generalizability × causation (the compass's crossing licenses) |
| rdss_fig_5_1.png | nb04 | the MIDA map (returns for M+I) — same diagram as 2.1 |
| rdss_fig_6_1.png | nb04 | minimal DAG: Z→Y with unknown heterogeneity U |
| rdss_fig_6_2.png | nb04 | DAG vocabulary: confounder, moderator, mediator, collider, instrument |
| scale_measurement.png | nb05 | data → categorical/quantitative → nominal/ordinal/interval/ratio |
| rdss_fig_15_1.png | nb05 | sampling + survey question: latent Y* vs measured Y |
| rdss_fig_17_1.png | nb05 | measuring a sensitive trait: direct vs list question, sensitivity bias |
| variables_observations.png | nb06 | elements, variables, observations in a data table |
| spread_vs_center.png | nb06 | same mean, different spread (two campaigns) |
| shape_boxplot_map.png | nb06 | distribution shape ↔ boxplot (skew) |
| pie-vs-bar.png | nb06 | same data as pie vs bar |
| steve-jobs-pie.jpg | nb06 | the 2008 keynote 3-D pie (39% vs 19.5% perception) |
| data_ink.png | nb14 | the data-ink ratio: same bar chart before/after cleanup (MGMT474 lecture, after Tufte) |
| rdss_fig_8_1.png | nb07 | the data-strategy DAG: sampling S, assignment Z, response R, measurement Q |
| rdss_fig_8_2.png | nb07 | sampling procedures grid: simple/complete/stratified × individual/cluster/multistage |
| rdss_fig_21_1.png | nb07 | ethics: scientific benefits vs ethical costs by inquiry importance |
| rdss_fig_18_2.png | nb09 | covariate adjustment buys power/precision (by R²) |
| correlation_gallery.png | nb09 | reading r: −0.9 to +0.9 scatter gallery |
| rdss_fig_9_1.png | nb10 | simulated sampling distribution of estimates, estimand vs mean estimate |
| population_sample_inference.png | nb10 | population → sample → point/interval estimate (business example) |
| ci_mechanics.png | nb10 | what "95% confident" means: 20 intervals, one misses |
| moe_vs_n.png | nb10 | margin of error shrinks with √n (halving costs ~4×) |
| rdss_fig_11_2.png | nb10 | power vs true effect size at N=100/500/1000 |
| rdss_fig_10_1.png | nb11 | MIDA replicated k times = Monte-Carlo diagnosis |
| rdss_fig_10_5.png | nb11 | bias/precision targets: SD, Bias, RMSE |
| rdss_fig_11_1.png | nb11 | diagnosand power vs sample size, 0.8 target |
| rdss_fig_16_8.png | nb13 | RDD DAG: running variable, cutoff, treatment, outcome |
| rdss_fig_18_1.png | nb13 | experiment DAG: random Z, measurement Q, unknown U |
| rdss_fig_22_1.png | nb17 | a realized survey-experiment analysis (CATEs & differences, Bonilla–Tillery design) |

Notebooks without assigned external figures (nb01, nb03, nb08, nb12, nb14*,
nb15, nb16, nb18) generate their own plots or are text-performance units.
(*nb14 carries the MGMT474 data-communication lecture, whose demos are
generated in-code.)
