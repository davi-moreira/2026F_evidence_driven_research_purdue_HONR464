# The model-disagreement laboratory

*A lesson protocol for GenAI Studio's multi-model comparison, used in Week 10's
adversarial-review lecture (nb09) and again in Week 16 (nb15). You run the same
prompt across two or more models, study where they disagree, and — the harder
lesson — learn why their **agreement is not proof**.*

The one-line takeaway: **disagreement is a flag to investigate; agreement is not a
verdict.** Two models that were trained on overlapping data can be confidently
wrong in the same direction. This lab teaches you to use multiple models as a
source of *questions*, never as a vote you can trust.

---

## What GenAI Studio gives you

GenAI Studio's chat can send **one prompt to two or more models at once** and show
their answers side by side (verified capability, RCAC docs 2026-07-22). The models
are open-source (the LLaMA family; others by ticket). You may also add a
non-GenAI-Studio model you use elsewhere (for example, Gemini in Colab) by running
the same prompt there and bringing its answer in. There are **no autonomous agents
and no orchestration** here — you drive every comparison by hand.

---

## Why agreement is not confirmation

Before the protocol, the concept it exists to teach.

- **Correlated errors.** Large models share training data, architectures, and
  internet-scale text. When they agree, they may be repeating the same popular
  misconception, not converging on truth. Independent instruments that share a
  common flaw are not independent.
- **False consensus.** Two confident, matching answers *feel* like evidence. That
  feeling is the trap. Agreement raises a hypothesis worth checking; it does not
  discharge the check.
- **The public, verifiable premise behind this lab** (from Scott Cunningham's
  causal-inference writing, part 24, the one public fragment used): validate
  analytical work by comparing independent implementations, while staying mindful
  that the errors across implementations may be correlated. Comparison is a probe,
  not a proof.

So: when models disagree, you have found a place to dig. When they agree, you have
found a hypothesis to verify against the world, not a fact.

---

## Protocol A — the disagreement run

1. **Fix the prompt.** Write one clear prompt for a real question in your project
   (a classification, a critique, a factual claim, a design read). Send only
   course-authored and de-identified material.
2. **Send it to 2+ models** using multi-model comparison (add a third from outside
   GenAI Studio if you have one).
3. **Log each answer** verbatim, labeled by model.
4. **Mark every point of disagreement.** For each, note what the models actually
   differ on — a fact, a judgment, a definition, a boundary.
5. **Investigate the disagreements, not the agreements first.** A disagreement is a
   crack; open it. Which model, if either, is right? Confirm against your own
   materials or a real source.
6. **Then interrogate the agreements.** For each point where the models agree, ask:
   is this true, or is it a shared assumption? Verify at least the load-bearing
   ones independently.

---

## Protocol B — the prompt-sensitivity probe

A single model's answer can hinge on how you phrased the question. Test it.

1. **Take one question. Write three honest phrasings** of it — not trick versions,
   just the ways a careful person might naturally ask.
2. **Send all three to the same model.**
3. **Compare.** If the substance of the answer moves with the phrasing, the model
   is keying on wording, not reasoning, and its answer is fragile.
4. **Record the spread.** A stable answer across phrasings is more trustworthy (not
   proven — more trustworthy). A volatile one is a warning to verify hard before
   using anything it said.

---

## Protocol C — the confidence-calibration check

Models state false things with the same fluency as true ones. Separate confidence
from correctness.

1. **For a claim a model made confidently, ask it how it would be checked** and
   what would show it to be wrong.
2. **Do that check yourself.** If a confidently stated claim fails an easy
   verification, treat that model's confidence as uninformative for this topic.
3. **Note the calibration.** Over a few checks you learn where a model is reliable
   and where its confidence is empty — for *this* kind of question, not in general.

---

## The write-up form

Every run of this lab produces a short record. Use this shape; it doubles as your
AI Research Ledger evidence.

**1. The question and the fixed prompt.** State both.

**2. Who said what.** A row per model:

| Model | Answer (verbatim or tight paraphrase) |
|---|---|
| (model A) | … |
| (model B) | … |
| (model C, if any) | … |

**3. Where they agreed and where they disagreed.** List the agreement points and
the disagreement points separately.

**4. Was the agreement verified independently?** For each agreement point you
relied on: how you checked it against your own materials or a real source, and the
result. "The models agreed" is **not** an entry here — only your independent check
is.

**5. The decision and the ledger row.** What *you* concluded and did, then a
completed AI Research Ledger row: task delegated · tool used (name each model) ·
prompt · output summary · decision · verification method · remaining concern ·
responsible student.

---

## Where this lab is used

- **Week 10 (nb09), "Share the research and attack the analysis."** You run
  Protocol A on a claim from your own project during the adversarial-review
  lecture, feeding the M9 research audit. Disagreement between models becomes a
  list of things to stress-test with the Robustness & Sensitivity Reviewer.
- **Week 16 (nb15), "Managing multiple AI agents; the final defense."** You run all
  three protocols as part of the AI-management capstone, and you name — in
  taxonomy terms — why comparing models by hand (level 4) is not the same as
  trusting an autonomous consensus (levels 5–6 the course does not use). The
  correlated-error lesson is exactly what a defense examiner will press on.

---

## The habit this builds

You will finish the course able to hold several AI answers at once without being
captured by any of them: mining disagreement for questions, refusing to read
agreement as truth, and settling every load-bearing claim with your own
verification against the evidence. That habit — not any single model's answer — is
what the final defense assesses.
