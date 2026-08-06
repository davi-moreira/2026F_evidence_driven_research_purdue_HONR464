# Course figures — inventory, assignments, and attribution

Every figure was **visually inspected before captioning** (evidence-integrity
rule). Notebooks embed them via the raw GitHub URL so they render in Colab:

```
https://raw.githubusercontent.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/main/notebooks/figures/<file>
```

## Retired: the RDSS figure conversions (D48, 2026-08-05)

The eighteen `rdss_fig_*.png` files were removed from the repository. They were
exact conversions of figures published in Blair, Coppock & Humphreys (2023),
*Research Design in the Social Sciences* (Princeton University Press, all
rights reserved). Attribution in a README is not permission to redistribute a
copyrighted figure, and the MIT license on the `rdss` R package does not
establish redistribution rights for converted book figures. The v1 notebooks
that once displayed them were retired with the v1 build (git tag
`v1-compass-build`), so nothing in the current course or book referenced them.

**The replacement rule: the book draws its own.** Concept diagrams are
generated in the book's monochrome house style by
`scripts/build_book_concept_figures.py` (the same pattern as
`scripts/build_book_part1_figure.py`), and the frameworks they illustrate are
credited in the surrounding prose. Never commit a figure copied or converted
from a copyrighted source; draw the concept yourself and cite whoever developed
it.

## Sources & attribution lines (used verbatim in notebooks)

1. **Professor Moreira's QM 67000 Business Analytics slides** (his own
   material): *"From Professor Moreira's QM 67000 Business Analytics slides."*
2. **Personal photos** (nb01 introduction): Professor Moreira's own.
3. `steve-jobs-pie.jpg`: Apple keynote photograph (2008) — a classic
   visualization-criticism case, used in Professor Moreira's slides.

## Assignments (file → notebook · what it shows)

| File | NB | Shows |
|---|---|---|
| davi_moreira_photo.jpg | nb01 | the professor |
| palmeiras_logo.png / palmeiras_stadium.jpg | nb01 | Palmeiras (instructor's passion) |
| carnaval_olinda.jpg | nb01 | Olinda carnival (instructor's passion) |
| random_assignment_sampling.png | nb03 | random sampling × random assignment → generalizability × causation (the compass's crossing licenses) |
| scale_measurement.png | nb06 | data → categorical/quantitative → nominal/ordinal/interval/ratio |
| variables_observations.png | nb07 | elements, variables, observations in a data table |
| spread_vs_center.png | nb07 | same mean, different spread (two campaigns) |
| shape_boxplot_map.png | nb07 | distribution shape ↔ boxplot (skew) |
| pie-vs-bar.png | nb07 | same data as pie vs bar |
| steve-jobs-pie.jpg | nb07 | the 2008 keynote 3-D pie (39% vs 19.5% perception) |
| correlation_gallery.png | nb10 | reading r: −0.9 to +0.9 scatter gallery |
| population_sample_inference.png | nb11 | population → sample → point/interval estimate (business example) |
| ci_mechanics.png | nb11 | what "95% confident" means: 20 intervals, one misses |
| moe_vs_n.png | nb11 | margin of error shrinks with √n (halving costs ~4×) |
| data_ink.png | nb15 | the data-ink ratio: same bar chart before/after cleanup (MGMT474 lecture, after Tufte) |

Notebook numbers in this table refer to the v1 build (git tag
`v1-compass-build`); the v2 course generates its plots in-code. The book's own
diagrams live in `book/images/` and are generated, never copied.
