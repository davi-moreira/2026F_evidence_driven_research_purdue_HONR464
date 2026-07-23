# BOOK_MAP — the course book "Evidence-Driven Research" (37 chapters, 6 parts)

Authoritative manifest for the open-access Quarto book (D20). RDSS remains the
assigned theory text; this book is the course's own AI-era research manual.
Each chapter carries the same ten elements (the research decision · conceptual
explanation · a STEM worked example · a Colab lab link to its primary notebook ·
recommended AI prompts · a "Do not delegate" box · an AI failure case · a
verification lab · project transfer · a defend-your-decision activity), the same
undergraduate voice + citation rules as the notebooks, and a Colab link to its
**primary notebook**. `scripts/validate_book_sync.py` checks, both directions,
that every chapter links its notebook and every notebook nb00–nb15 is the
primary of ≥1 chapter.

Book project: `book/` (Quarto book) rendered into `docs/book/`; a **Book** tab
is added to `_quarto.yml`. Chapter files: `book/<part-slug>/<NN>-<slug>.qmd`.

| Part | Ch | Title | Primary notebook |
|---|---|---|---|
| I — Research when AI can produce almost everything | 1 | AI Is Your Arm, Not Your Brain | nb00 |
| I | 2 | The Student as Research Director | nb00 |
| I | 3 | Specify, Delegate, Interrogate, Inspect, Verify, Document, Defend | nb00 |
| I | 4 | Research Responsibility and Intellectual Ownership | nb00 |
| II — From curiosity to research design | 5 | From Curiosity to a Research Problem | nb01 |
| II | 6 | Descriptive, Predictive, and Causal Questions | nb01 |
| II | 7 | Research Builds on Research | nb02 |
| II | 8 | Finding and Verifying Prior Evidence | nb02 |
| II | 9 | Model, Inquiry, Data Strategy, and Answer Strategy | nb03 |
| II | 10 | Declaring and Diagnosing a Research Design | nb03 |
| III — Research pathways | 11 | Observational Descriptive Research | nb04 |
| III | 12 | Observational Causal Research | nb05 |
| III | 13 | Experimental Descriptive Research | nb06 |
| III | 14 | Prediction and Generalization | nb07 |
| III | 15 | Experimental Causal Research | nb08 |
| III | 16 | Hybrid and Complex Designs | nb03 |
| IV — Producing credible evidence with AI | 17 | Data Provenance and Data Quality | nb02 |
| IV | 18 | Measurement and Operationalization | nb04 |
| IV | 19 | AI as Programmer | nb04 |
| IV | 20 | AI as Analytical Assistant | nb09 |
| IV | 21 | Robustness and Sensitivity | nb09 |
| IV | 22 | Diagnostics and Negative Tests | nb09 |
| IV | 23 | AI as Adversarial Reviewer | nb09 |
| IV | 24 | Recognizing False Confidence | nb00 |
| V — Communicating and defending research | 25 | From Results to Claims | nb10 |
| V | 26 | Claim–Evidence Tables | nb10 |
| V | 27 | Research Posters | nb10 |
| V | 28 | Poster Criticism | nb10 |
| V | 29 | Research Pitches | nb11 |
| V | 30 | Difficult Questions and Uncertainty | nb11 |
| V | 31 | AI Disclosure and Research Integrity | nb12 |
| VI — Research after the conference | 32 | Replication and Reproduction | nb13 |
| VI | 33 | From Poster to Research Note | nb14 |
| VI | 34 | Open and Reusable Research Packages | nb14 |
| VI | 35 | Managing Multiple AI Agents | nb15 |
| VI | 36 | Conflicting Agents and Human Escalation | nb15 |
| VI | 37 | Final Research and AI-Management Portfolio | nb15 |

Coverage check: every notebook nb00–nb15 is the primary of at least one chapter
(nb00 ×5, nb01 ×2, nb02 ×3, nb03 ×3, nb04 ×3, nb05 ×1, nb06 ×1, nb07 ×1, nb08 ×1,
nb09 ×4, nb10 ×4, nb11 ×2, nb12 ×1, nb13 ×1, nb14 ×2, nb15 ×3). Part-slug map:
I=part1-research-with-ai · II=part2-curiosity-to-design · III=part3-pathways ·
IV=part4-credible-evidence · V=part5-communicating · VI=part6-after-conference.

Build order (Phase 6): the book is authored AFTER the notebooks are final, so
each chapter distills its primary notebook's decision + labs and never drifts
from it. Chapters are written in part-waves; `validate_book_sync.py` gates each
wave; the site gets the Book tab once Part I renders.
