# AI Error Taxonomy

*The named ways an AI research partner goes wrong, each with a realistic example,
how to catch it, and the [verification](verification_guide.md) method that counters
it. Learn these names. Your [ledger's](ai_research_ledger_template.md) "remaining
concern" column is you watching for exactly these failures.*

---

## Why name the failures

You cannot guard against a danger you cannot name. AI tools fail in patterned,
repeatable ways, and once you know the patterns you stop being surprised by them.
Every failure below has caught real researchers. For each you get the same three
things: **what it looks like**, **how to detect it**, and **which verification
counters it**.

A running theme: the failures are convincing. A wrong answer from a good model is
fluent, confident, and well-formatted. **Fluency is not evidence.** That is why
the checks live outside the model.

## The eight failure modes

**1. Confident fabrication.** The model invents something that does not exist and
presents it with full confidence: a citation with real-sounding authors, a
precise statistic, a function that was never in the library.
- *Example:* asked for sources, it returns "Chen & Alvarez (2019), *Journal of
  Educational Psychology*" for a paper that does not exist.
- *Detect:* try to independently locate the exact thing. If you can't find it in
  seconds where it should live, treat it as fabricated until proven otherwise.
- *Counter:* **primary-source reading** for citations and facts;
  **documentation lookup** for functions.

**2. Plausible-but-wrong method.** It recommends an approach that sounds right and
is wrong for your case: the standard test when your data violate its assumptions,
a causal method where your design cannot identify the effect.
- *Example:* it suggests a technique that assumes independent observations for
  data that are clearly clustered.
- *Detect:* ask what the method assumes and check each assumption against your
  actual data.
- *Counter:* **counterexample** and **simulation**; a **causal diagram** when the
  method makes a causal claim.

**3. Silent scope change.** You ask a hard question; it quietly answers an easier,
adjacent one and hands you the answer as if it were yours.
- *Example:* you ask whether an effect *causes* an outcome; it returns evidence
  that the two are *associated*, phrased as if it settled causation.
- *Detect:* read the answer's claim next to your question's claim, word for word.
  Do the kind and the reach match?
- *Counter:* **peer reasoning** and re-reading against your inquiry declaration;
  a **causal diagram** when the swap is association-for-causation.

**4. Missing uncertainty.** It reports a result as a clean fact with no bound, no
caveat, no sense of how firm it is.
- *Example:* "The effect is 4.2" with no interval, no sample-size context, no
  mention that the estimate is noisy.
- *Detect:* if there is no uncertainty on the page, assume it was dropped, not
  that there was none.
- *Counter:* force it out with a prompt ("rate confidence, give the bound"), then
  confirm with **direct calculation** or a **holdout sample**. This failure maps
  straight to the course's overclaiming-certainty defect.

**5. Sycophantic agreement.** It agrees with whatever you propose because you
proposed it, telling you your idea is strong when it is not.
- *Example:* "Yes, that's an excellent question and your design is sound" for a
  design with an obvious hole.
- *Detect:* you asked a leading question. Praise that arrives without a single
  objection is a red flag.
- *Counter:* change the role. Ask it to argue against you as a hostile reviewer,
  then take the objections to **peer reasoning**.

**6. Stale knowledge.** Its training has a cutoff; it may miss recent work,
current tool versions, or a fact that changed after its knowledge ends.
- *Example:* it describes a package's old default that a newer version changed, or
  misses a recent study central to your gap.
- *Detect:* for anything time-sensitive, ask when its knowledge ends and check the
  current source yourself.
- *Counter:* **documentation lookup** for tools; **primary-source reading** for
  recent literature.

**7. Correlated errors across tools or roles.** Two AI tools (or two roles of one
tool) make the *same* mistake, so asking twice feels like confirmation when it is
just the same flaw echoed back.
- *Example:* Gemini and a second tool both inherit the same wrong assumption about
  your data and both "agree" on a wrong answer.
- *Detect:* if two AI sources agree, ask whether they could be wrong the *same*
  way. Agreement is only reassuring when the checks are independent.
- *Counter:* verify with a **non-AI** method from a different family (direct
  calculation, primary source, human peer). This is why the guide asks for two
  *independent* checks on high-stakes results.

**8. Illusion of completeness.** The output *looks* thorough — long, organized,
many sections — and quietly omits the one thing that matters.
- *Example:* a "comprehensive" limitations list, polished and confident, that
  never mentions the sampling-frame gap that most threatens your claim.
- *Detect:* "looks thorough" is not "is complete." Ask specifically: "What is the
  single most important thing you left out?" and check against your own list.
- *Counter:* **peer reasoning** and a deliberate **counterexample** hunt; compare
  the output against an independent checklist you wrote first.

## The one habit that catches most of these

Before you consult AI on anything that matters, **write down your own answer or
your own expectation first** (the notebook's initial human commitment). Then the
AI output has something to disagree with. A silent scope change, a missing
caveat, or a fabricated source is far easier to spot when you already hold a view
of your own to compare it against.

---

*See also: [verification_guide.md](verification_guide.md) (the counters in full) ·
[prompt_design_guide.md](prompt_design_guide.md) (interrogation moves that flush
these out) · [escalation_protocol.md](escalation_protocol.md) (what to do when a
failure touches a decision that is yours alone).*
