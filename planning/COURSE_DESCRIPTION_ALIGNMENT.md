# COURSE_DESCRIPTION_ALIGNMENT — every clause of the official description, mapped

The official course description (as published in `syllabus.qmd` / `index.qmd`),
decomposed clause by clause, with the units, readings, notebooks, milestones, and
assessments that deliver each clause. If a clause has no home, the build is
incomplete; if an artifact serves no clause, it needs a justification.

> This Honors seminar teaches you to turn curiosity into credible, evidence-based
> insight — no strong background in quantitative methods or computing required.
> You will learn to identify meaningful gaps in a chosen field, translate a gap
> into a well-scoped research problem, formulate answerable research questions,
> choose and justify an appropriate position on the inquiry compass (description,
> generalization, prediction, and/or causal reasoning) at a conceptual level,
> and use computational tools and AI to locate sources, operationalize concepts,
> analyze evidence, verify results, and document decisions responsibly. You will
> finish able to design and defend a rigorous research approach, interpret
> findings with appropriate uncertainty and limitations, and communicate results
> in written and oral formats.

| # | Clause | Meetings / unit | Notebooks | Readings | Milestones | Assessment |
|---|---|---|---|---|---|---|
| 1 | "turn curiosity into credible, evidence-based insight" | the whole arc, opened M1–M2 | nb00, nb01 | RDSS ch. 1–2 | M00 → M23 (the full chain) | all components |
| 2 | "no strong background in quantitative methods or computing required" | design constraint on every meeting: low-floor/high-ceiling; all machinery provided, students fill parameters and interpret | all notebooks (provided-code convention; nb23-style helpers narrated, never authored by students) | RDSS read conceptually; no math prerequisites invoked | milestone rubrics grade reasoning + verification, never coding elegance | grading philosophy in `ASSESSMENT_ARCHITECTURE.md` |
| 3 | "identify meaningful gaps in a chosen field" | M3 (gap typology), M7–M8 (literature) | nb01 §3, nb03 | RDSS ch. 3–4 | M01 (gap), M02 (claim map with placed gap) | milestone bucket (30%) |
| 4 | "translate a gap into a well-scoped research problem" | M3–M4 | nb01 §3–4 | RDSS ch. 4 | M01 | milestone bucket |
| 5 | "formulate answerable research questions" | M4 (answerability rubric) | nb01 §4 | RDSS ch. 4 | M01, refined through M03 | milestone bucket |
| 6 | "choose and justify an appropriate position on the inquiry compass … at a conceptual level" | M5–M6 (the skill), deep dives M13–M14, M20–M22, M25–M26, M27–M28 | nb02; nb06, nb10, nb12, nb13 | RDSS ch. 7, 15–18 | M03 (inquiry declaration), M09 (compass-branched pilot), the `INQUIRY_DECLARATION` template | milestone bucket + defense |
| 7 | "use computational tools and AI to locate sources" | M7 (AI-assisted search + hallucination catch) | nb03 | fresh + RDSS ch. 4 | M02 | milestone bucket + AI-ledger habit |
| 8 | "operationalize concepts" | M11–M12 (concept→construct→indicator) | nb05 | RDSS ch. 8 (measurement) | M04 | milestone bucket |
| 9 | "analyze evidence" | M13–M28 (description → generalization → prediction → causal; the pilot) | nb06–nb13 | RDSS ch. 8–11, 15–18 | M05–M09 | milestone bucket |
| 10 | "verify results" | every notebook's "After running, verify" blocks; M17 recompute; M39–M40 reproduction exchange | all; esp. nb08, nb18 | RDSS ch. 21–22 | M09 (verification log), M19 (sensitivity), M20 (reproducibility audit with partner sign-off) | dossier bucket (20%) + engagement |
| 11 | "document decisions responsibly" | decision logs + AI-use ledger, introduced M1, finalized M39 | nb00 (ledger start), nb18 | RDSS ch. 21 | every milestone carries a decision/disclosure block; M20, M23 | dossier bucket |
| 12 | "design and defend a rigorous research approach" | M22 (full declaration), M23–M24 (diagnose/redesign), M42–M43 (Evidence Defense) | nb10, nb11, nb19 | RDSS ch. 10–11 | M07, M08, M22 | defense component (5%) + milestone bucket |
| 13 | "interpret findings with appropriate uncertainty and limitations" | M20 (uncertainty), M21 (generalization), M33 (ULN move) | nb10, nb15 | RDSS ch. 9–10 | M14 (uncertainty & limitations statement), every results-bearing milestone | poster + dossier buckets |
| 14 | "communicate results … written" | M29–M31 (poster), M40–M41 (brief), dossier | nb14, nb18 | fresh | M10–M12, M21, M23 | poster bucket (20%) + dossier bucket |
| 15 | "communicate results … oral" | M32–M35 (pitches, ULN, hot seat, rehearsal), URC Nov 17, defenses Dec 7/9 | nb15, nb19 | fresh | M13–M16, M22 | poster bucket + defense component |

## Reverse check — artifacts with no clause

- **Claim Tickets (exit tickets M1–M44):** serve clauses 1, 6, 13 as the daily
  habit-former; graded inside the engagement component.
- **Calling Bullshit optional analyses:** serve clauses 6 and 13 (claim
  evaluation); optional by locked decision, graded inside the concept-check
  component only when used.
- **`translation/` R→Python parity project:** serves **no clause** — by design.
  It is the separate parallel project (locked decision #4), not course content.

## Standing course promises the description implies

- **Individual projects** (5 students, 5 projects) — `course_config.yaml`
  `project_mode: individual`.
- **URC poster (Nov 17) is required** — clause 15's public instantiation (M16).
- **No conventional midterm/final exam** — the Evidence Defense + dossier are the
  culminating assessments (`ASSESSMENT_ARCHITECTURE.md`).
