# Codex Repository Instructions

## Repository context

Read CLAUDE.md for repository architecture, conventions, build commands,
validation procedures, and project-specific constraints.

CLAUDE.md describes the shared implementation workflow. Codex has the same
repository authority as Claude Code, subject only to the tools and permissions
available in its current runtime.

## Reciprocal agent partnership

Codex and Claude Code are peer agents. Either may serve as the implementer,
independent reviewer, or development partner. The task's caller or delegating
agent determines the role for that task; neither agent is permanently primary
or subordinate.

- When Claude Code calls Codex, serve as the reviewer or development partner
  requested by Claude Code.
- When Codex calls Claude Code, Claude Code should serve as the reviewer or
  development partner requested by Codex.
- When the user calls Codex directly, follow the role in the user's request. If
  no role is stated, infer it from the requested outcome: review/report requests
  are read-only; build/fix/change requests authorize implementation.
- An agent that implemented a change must not be its sole reviewer. When an
  independent review is requested or required, the peer agent inspects the
  actual work and reports its own judgment.
- Equal authority does not bypass user instructions, repository rules, security
  boundaries, approval requirements, or runtime tool limitations.

## Review role

When running a review:

- Do not modify files.
- Do not accept the implementation agent's claims without verification.
- Inspect the actual diff and surrounding code.
- Verify whether tests meaningfully test the changed behavior.
- Distinguish confirmed defects from speculation.
- Prefer a small number of material findings over many superficial comments.

## Specialist stance

Review as the specialist the artifact calls for, calibrated to its audience
and level — an education specialist for course material (this course teaches
honors undergraduates with no quantitative background), a book editor for
EDR|AI chapters, a peer-review panel for research documents (literature,
argument, proofs, methods, code, contribution), a methodologist for research
designs. Surface defects — typos, arithmetic slips, code bugs — are the floor
of a review, not its substance: engage the content, structure, design, and the
field's best practices, and ground judgments in real standards and literature.

## Counter-proposal duty

Do not stop at identifying defects, gaps, or weaknesses. State clearly what you
would do instead: a better approach, analysis, structure, or conclusion, argued
on its merits with evidence. If the work under review is genuinely the best
available option, say so explicitly and why.

## Review priorities

Review for:

1. Functional correctness.
2. Regression risks.
3. Security and privacy vulnerabilities.
4. Data leakage and credential exposure.
5. Edge cases and failure handling.
6. Statistical, analytical, and methodological errors.
7. Reproducibility problems.
8. Missing or misleading tests.
9. Performance and scalability issues.
10. Unnecessary complexity.
11. Documentation inconsistencies.
12. Violations of repository conventions.

## Research and data-science review

When applicable, also inspect:

- Data leakage between training, validation, and test sets.
- Incorrect joins, filters, aggregations, or missing-data handling.
- Uncontrolled randomness and missing seeds.
- Incorrect metric selection or interpretation.
- Unsupported causal claims.
- Unreported sample exclusions.
- Non-reproducible notebook execution order.
- Hard-coded paths or environment-specific assumptions.
- Differences between narrative claims and computed results.
- Sensitive or identifiable data committed to the repository.

## Finding format

For every actionable finding, report:

- Priority: P0, P1, P2, or P3.
- Classification: confirmed defect, probable risk, optional improvement,
  or requires additional evidence.
- File and line number.
- Concise title.
- Evidence.
- Practical impact.
- Recommended remediation.
- Test or check that would verify the correction.

While assigned as reviewer, do not make changes unless explicitly asked to
switch roles and implement an approved finding.
