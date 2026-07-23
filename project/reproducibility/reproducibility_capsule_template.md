# Reproducibility Capsule Template — M14 / M15

*The frozen, self-contained bundle that lets anyone rebuild your findings after the
course ends. You assemble it for the M14 research-note capsule and finalize it
inside the M15 dossier. A capsule is complete when a competent stranger, with only
what is inside it, can reproduce your headline number and read every claim back to
its evidence.*

---

## What a capsule is

A **reproducibility capsule** is your whole project packaged so it survives on its
own: the notebook that produces the numbers, the data or a loader that fetches it,
the documentation that explains it, the tables that connect claims to evidence,
and the ledgers that show how AI was used and how everything was verified. "Frozen"
means it is the version of record. Once you sign it off, it does not drift.

Think of it as the answer to a simple test: *if you vanished today, could someone
rebuild your findings from this bundle alone?* If yes, it is a capsule. If they
would need to ask you a question, it is not done yet.

## The eight components (assemble all)

| # | Component | What it is | Reference |
|---|---|---|---|
| 1 | **Final notebook** | The runnable notebook, passing restart-and-run-all from a cold kernel | [clean_run_checklist.md](clean_run_checklist.md) |
| 2 | **Data snapshot or loader** | Either the exact data or the documented loader that fetches it from the public source, with its version | [README_template.md](README_template.md) |
| 3 | **README** | The front door: question, compass position, run order, expected outputs, verification map | [README_template.md](README_template.md) |
| 4 | **Data dictionary** | One row per variable: type, units, range, source, transformations, missingness | [data_dictionary_template.md](data_dictionary_template.md) |
| 5 | **Environment note** | Python version, result-critical package pins, runtime type, approximate run time | [environment_documentation.md](environment_documentation.md) |
| 6 | **Claim–evidence table** | Every claim your project makes, with its evidence, verification, boundary, and sensitivity survival | your claim ledger |
| 7 | **Ledgers** | The finalized AI Research Ledger and the claim ledger | [ai_research_ledger_template.md](../../ai_resources/ai_research_ledger_template.md) |
| 8 | **License / attribution** | The terms under which your data may be used and how each source is credited | provenance rows in the README |

A capsule missing any of these is incomplete. The seed policy is not a separate
file here; it lives inside the notebook's setup cell and is noted in the
environment note (component 5).

## The claim–evidence table (component 6)

This table is the spine of the capsule. It is where every public claim meets the
evidence that earns it, so a reader never has to take your word for anything.

```markdown
| Claim | Evidence (number + source) | Verification method | Boundary (what it does NOT claim) | Survived sensitivity? |
|---|---|---|---|---|
| [the claim as stated] | [the number and where it comes from] | [named method] | [the overreach it forbids] | [yes / moved / n/a] |
```

Every sentence in your research note and brief should trace to a row here. A claim
with no row is a claim with no evidence; either cut it or earn it a row.

## The sign-off attestation

A finalized capsule carries a signed line. It is the author's statement that the
bundle is complete and honest, and it is what makes the capsule the version of
record.

```
────────────────────────────────────────────────────────────────
REPRODUCIBILITY CAPSULE — SIGN-OFF

Project: ____________________________________________________
Author:  ____________________________________________________

I attest that:
  [ ] the notebook passes restart-and-run-all from a cold kernel,
  [ ] every reported number traces to a cell and a data source,
  [ ] every claim in my note traces to a claim–evidence row,
  [ ] the AI Research Ledger is complete and every output was verified,
  [ ] data sources are documented with their license and attribution,
  [ ] any residual non-determinism is stated honestly.

This capsule is the frozen version of record for my project.

Author signature: ____________________   Date: ______________
────────────────────────────────────────────────────────────────
```

If you cannot honestly check a box, the capsule is not ready. An honest gap
recorded in the notes is graded far better than a signed attestation a reproducer
then disproves.

## From M14 to M15

- **At M14**, you assemble the capsule around your research note and workshop it in
  the table read. Some components may still be tightening.
- **At M15**, the capsule is frozen inside the final dossier, signed, and defended.
  M15 is terminal; there is no revision window, so the capsule you sign is the one
  that stands.

## Quality bar

- ☐ All eight components are present and internally consistent.
- ☐ The notebook passes a cold restart-and-run-all and matches the README numbers.
- ☐ Every claim in the note has a claim–evidence row.
- ☐ Both ledgers are finalized.
- ☐ Data licenses and attributions are stated.
- ☐ The sign-off is signed, with no box checked that is not honestly true.

## Common failure modes

1. **A capsule that needs you in the room.** If a reproducer must ask you a
   question, a component is missing. Fill it before you sign.
2. **A claim with no row.** The claim–evidence table is the spine; a public claim
   outside it is unearned.
3. **Leaving the ledger for last.** It is a component, not an afterthought.
   Finalize it inside the capsule, not at the deadline.
4. **Signing an unhonest box.** A false attestation is an integrity failure; an
   honest residual note is good practice.

---

*Part of the reproducibility package. See also:
[README_template.md](README_template.md) ·
[data_dictionary_template.md](data_dictionary_template.md) ·
[clean_run_checklist.md](clean_run_checklist.md) ·
[replication_report_template.md](replication_report_template.md).*
