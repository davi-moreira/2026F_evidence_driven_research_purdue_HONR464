# Replication & Red-Team Audit Rubric (100 points) — M13

*The quality bar for the replication and red-team report. Five rows, four bands,
scored on the honesty and rigor of your audit, never on whether the peer's project
was good. Instantiates the shared rubric DNA in
`planning/ASSESSMENT_ARCHITECTURE.md`. Applied to the report submitted the Sunday
of the async module week; governs
[replication_report_template.md](replication_report_template.md).*

The report earns points for how competently and honestly you audited a stranger's
package: did you actually reproduce it, trace its numbers, probe its choices,
report your findings honestly, and keep a clean ledger of your own audit work.

## Grading rubric

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Reproduction rigor** (25) | You ran restart-and-run-all from a cold kernel, obtained the headline number (or logged a precise break), and the report shows the clean-run evidence (22–25) | Reproduction attempted and logged; the run evidence is present but thin in one place (18–21) | Reproduction described in general terms; the clean-run log is partial or its result is asserted more than shown (11–17) | No genuine cold run behind the verdict, or "reproduces" claimed with no clean-run log (0–10) |
| **Lineage tracing** (20) | Every reported number traced claim → figure → cell → data, with each link marked solid or broken and the breaks located exactly (18–20) | The headline lineage is traced end to end; a secondary number's trace is lighter (14–17) | Lineage traced only partway, or links asserted without showing where the number actually comes from (8–13) | No real tracing; the report accepts the numbers as given (0–7) |
| **Probe quality** (20) | One or two consequential alternative specifications run, each named, with a clear held/moved outcome and what it means for the claim (18–20) | Probes are relevant and run, but their consequence for the claim is stated loosely (14–17) | Probes are cosmetic or unrun (suggested, not executed), so they test nothing (8–13) | No probes, or probes that miss the choices that actually matter (0–7) |
| **Findings honesty & prioritization** (20) | Findings are specific and fair; the top-3 recommendations are genuinely the most important; the "could not verify" section is present and candid (18–20) | Findings specific; prioritization mostly right; the could-not-verify section present but brief (14–17) | Findings vague in places; recommendations unranked or padded; the could-not-verify section thin (8–13) | Findings unusable (vague or unfair), no real prioritization, or the could-not-verify section missing — the false-completeness defect (0–7) |
| **Craft & ledger** (15) | Report on-format and readable; your own AI-audit ledger is complete, with every check named and verified (13–15) | On-format; ledger present with a minor gap (10–12) | Format lapses or a ledger with a named check missing (5–9) | Off-format, or the AI Research Ledger for your audit is missing (0–4) |

## The hard cap (the rule with teeth)

**Claiming "reproduces" without a clean-run log caps Reproduction rigor at
Beginning**, regardless of the rest of that row. Reproduction is something you
*did* and can *show*, not something you assert. This mirrors the poster's
untraceable-number cap and the course's standing evidence-integrity rule: a
verification claim with no evidence behind it is treated as no verification.

A second standing cap applies course-wide: a **missing AI Research Ledger** for
your audit work scores the Craft & ledger row 0 and returns the submission, the
same rule that governs every deliverable.

## How the four bands are read

Each row is scored in one of four bands, with the point range inside a band
placing you at its top or bottom:

- **Exemplary** — the audit virtue is fully present; the author could not fault
  your rigor or honesty.
- **Proficient** — present with one honest, repairable weakness.
- **Developing** — the virtue wavers; a trace is incomplete or a probe is
  cosmetic.
- **Beginning** — the virtue is absent or a cap has been triggered.

## Row → shared rubric DNA

Each row instantiates one standing virtue, so this audit rewards exactly what every
milestone rewards:

| Audit row | Rubric-DNA virtue |
|---|---|
| Reproduction rigor | Verification |
| Lineage tracing | Evidence integrity |
| Probe quality | Compass alignment (does the claim survive its own boundary?) |
| Findings honesty & prioritization | Uncertainty & limitations |
| Craft & ledger | Craft & communication |

## Self-check before you submit

- ☐ I actually ran the package from a cold kernel and logged the result.
- ☐ Every number in the report traces to a cell, or is listed as untraceable.
- ☐ My probes were run, not just proposed.
- ☐ My "could not verify" section is honest and specific.
- ☐ My own audit ledger is complete, every check named.

---

*Part of the reproducibility package. See also:
[replication_report_template.md](replication_report_template.md) (what this grades)
· [clean_run_checklist.md](clean_run_checklist.md) ·
[reproducibility_capsule_template.md](reproducibility_capsule_template.md).*
