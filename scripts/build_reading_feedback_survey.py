#!/usr/bin/env python3
"""build_reading_feedback_survey.py — the Qualtrics reading-feedback instrument.

ONE survey serves every EDR|AI chapter. The student names the chapter on the
first question, so Brightspace carries one link and the export is one file, no
matter how the reading schedule changes.

The chapter list is GENERATED from the book manifest, exactly like the schedule
page: the survey can never offer a chapter the book does not publish, and never
miss one it does.

DESIGN PROVENANCE. The measurement core came out of a Codex partner run
(gpt-5.6-sol, xhigh, read-only, 2026-08-23; full deliverable at
~/.claude/codex-collab/HONR464/reading_feedback_instrument_codex.md) and was
verified and merged here. Three of its rulings changed the design:

  * ITEM-SPECIFIC RESPONSE OPTIONS, not a repeated agree/disagree grid. In a
    randomized multitrait-multimethod comparison, item-specific questions
    measured better than comparable agree/disagree items — Saris, Revilla,
    Krosnick & Shaeffer (2010), doi:10.18148/srm/2010.v4i1.2682. A grid also
    invites the undifferentiated responding Krosnick (1991),
    doi:10.1002/acp.2350050305, describes as satisficing, which is the exact
    failure mode of a form answered ~40 times.
  * PAAS'S SINGLE-ITEM 9-POINT MENTAL-EFFORT RATING for cognitive load —
    Paas (1992), doi:10.1037/0022-0663.84.4.429. Report it as PERCEIVED
    INVESTED EFFORT, never as a cognitive-load score; separating load types
    needs a multi-item instrument (Leppink et al. 2013,
    doi:10.3758/s13428-013-0334-1) that is far too long to repeat 40 times.
  * ONE ROTATING QUALITATIVE ANCHOR over a stable closed spine. The four
    prompt versions change the intellectual act; the closed items never move,
    so chapter-to-chapter comparison survives. The anchor sits BEFORE the
    housekeeping questions because later questions draw faster, shorter, more
    uniform answers — Galesic & Bosnjak (2009), doi:10.1093/poq/nfp031.

Two items are Davi's, kept over the partner design on course grounds: `coverage`
(unscored, and the survey says so) because a book author needs to know which
chapters get skimmed, and the AI-use pair, because this course grades an AI
Research Ledger every week and the disclosure habit should not switch off for
the reading.

Do NOT sum these items. They measure different constructs and do not form a
"chapter quality" scale.

Outputs (all in surveys/):
    qualtrics_reading_feedback.txt   Qualtrics "Advanced Format" import file
    reading_feedback_instrument.md   the instrument, its rationale and its sources

Usage:
    .venv/bin/python scripts/build_reading_feedback_survey.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from session_readings import lesson_index  # noqa: E402

OUT = REPO / "surveys"

# ---------------------------------------------------------------------------
# the closed spine: one construct per question, item-specific options
# (qid, construct, prompt, [options], recode note)

SPINE = [
    ("familiarity", "Prior topic familiarity",
     "Before you started this reading, how familiar were you with its main topic?",
     ["Not at all familiar", "Slightly familiar", "Moderately familiar",
      "Very familiar", "Extremely familiar"],
     "0–4"),
    ("explain", "Perceived explainability",
     "Right now, how well could you explain this chapter's main idea to a classmate?",
     ["I could not explain it yet",
      "I could name some parts, but not connect them",
      "I could give a basic explanation, with some gaps",
      "I could explain the main idea accurately",
      "I could explain the main idea and why it matters"],
     "1–5"),
    ("effort", "Invested mental effort (Paas 1992)",
     "How much mental effort did you invest in understanding this chapter? "
     "Mental effort means how much thinking work you put in, not how many "
     "minutes it took.",
     ["1 - Very, very low mental effort", "2", "3", "4", "5", "6", "7", "8",
      "9 - Very, very high mental effort"],
     "1–9"),
    ("reread", "Clarity breakdown",
     "How often did the writing make you stop and reread because the idea was "
     "not yet clear?",
     ["Never", "Once", "A few times", "Many times", "Through most of the chapter"],
     "0–4"),
    ("useful", "Perceived research utility",
     "How useful does this chapter seem for doing or judging research?",
     ["Not useful yet", "Slightly useful", "Moderately useful", "Very useful",
      "Essential", "I cannot tell yet"],
     "0–4; \"cannot tell yet\" is a separate code, never the midpoint"),
    ("ready", "Application readiness",
     "Without any more explanation, how ready are you to try this chapter's "
     "\"It is your turn\" task?",
     ["Not at all ready", "Slightly ready", "Moderately ready", "Very ready",
      "Fully ready", "I did not reach this section"],
     "1–5; \"did not reach\" is a separate code, never a low score"),
]

#: The rotating anchor. Qualtrics presents exactly ONE version per response and
#: stores which one fired. Every version demands the same thing — a specific
#: place in the chapter plus its consequence — so the four are comparable as
#: evidence even though they are not interchangeable as items. Each carries a
#: fallback clause so "nothing to report" still produces a located answer.
ANCHORS = [
    ("A", "anchor_a",
     "Point to one specific place that helped your understanding. Name the "
     "sentence, example, figure, or step, then say what it helped you see. "
     "If nothing helped, name where you first got stuck and say why."),
    ("B", "anchor_b",
     "Point to one specific place that slowed you down or blocked you. Name "
     "the sentence, example, figure, or step, then say what needs to change. "
     "If nothing blocked you, name the hardest place and say what made it work."),
    ("C", "anchor_c",
     "Choose one place you would revise. Say where it is and exactly what you "
     "would change. If you would change nothing, name one place that should "
     "stay exactly as it is, and say why."),
    ("D", "anchor_d",
     "Write one question this chapter left you with, and name the passage that "
     "prompted it. If you have no open question, write a check-for-understanding "
     "question for a classmate, and give the answer."),
]

ANCHOR_INSTRUCTION = ("Answer in one to three sentences. Be specific enough "
                      "that your instructor can find the passage. Longer "
                      "answers earn no more credit than short exact ones.")

INTRO = (
    "This takes about three minutes. You are reporting on ONE chapter you have "
    "just read. Answer from the reading, not from class."
    "<br><br>"
    "<b>Three things worth knowing before you start.</b>"
    "<br><br>"
    "<b>One.</b> This is scored on whether you submitted a real, chapter-specific "
    "response on time. It is never scored on what you said. A careful complaint "
    "and a careful compliment earn exactly the same credit, and the complaint is "
    "more useful."
    "<br><br>"
    "<b>Two.</b> The book is still being written. What you flag here is what gets "
    "rewritten, and you will see the changes."
    "<br><br>"
    "<b>Three.</b> Your name is attached, because this carries participation "
    "credit. Your ratings and your comments never affect any other grade."
)

AI_NOTE = ("One course rule applies here too: AI is your arm, not your brain. "
           "You may use a tool while you read. Just say so, the way you would "
           "in your AI Research Ledger. Using one is fine. Hiding it is not.")


def q(kind: str, qid: str, text: str, choices=None) -> str:
    out = [f"[[Question:{kind}]]", f"[[ID:{qid}]]", text]
    if choices:
        out.append("[[Choices]]")
        out += list(choices)
    return "\n".join(out) + "\n"


def build_txt(chapters: list[str]) -> str:
    p: list[str] = ["[[AdvancedFormat]]\n", "[[Block:Intro and chapter]]\n"]
    p.append(q("DB", "intro", INTRO))
    p.append(q("TE:SingleLine", "student",
               "Your Purdue username (the part of your email before @purdue.edu)."))
    p.append(q("MC:DropDown", "chapter",
               "Which chapter are you reporting on?", choices=chapters))
    p.append("[[PageBreak]]\n")

    p.append("[[Block:The reading]]\n")
    for qid, _construct, prompt, options, _recode in SPINE:
        kind = ("MC:SingleAnswer:Horizontal" if qid == "effort"
                else "MC:SingleAnswer:Vertical")
        p.append(q(kind, qid, prompt, choices=options))
        if qid == "effort":
            p.append("[[PageBreak]]\n")
    p.append("[[PageBreak]]\n")

    # the anchor comes BEFORE the housekeeping questions, on its own page
    p.append("[[Block:Your evidence anchor]]\n")
    p.append(q("DB", "anchor_note", ANCHOR_INSTRUCTION))
    for _v, qid, prompt in ANCHORS:
        p.append(q("TE:Essay", qid, prompt))
    p.append("[[PageBreak]]\n")

    p.append("[[Block:Housekeeping]]\n")
    p.append(q("MC:SingleAnswer:Vertical", "coverage",
               "How much of the chapter did you actually read? This answer is "
               "never scored. Answer it honestly, so the workload numbers mean "
               "something.",
               choices=["All of it, closely", "All of it, some parts quickly",
                        "Most of it", "About half", "I skimmed it",
                        "I did not read it this time"]))
    p.append(q("MC:SingleAnswer:Vertical", "notebook",
               "Did you use this chapter's companion Colab notebook?",
               choices=["No, I did not open it", "I opened it but did not run it",
                        "I ran it as written", "I ran it and changed things"]))
    p.append(q("MC:SingleAnswer:Vertical", "notebook_effect",
               "If you used it: what did the notebook do for your understanding?",
               choices=["Made it much harder", "Made it a little harder",
                        "No difference", "Helped a little", "Helped a lot"]))
    p.append(q("DB", "ainote", AI_NOTE))
    p.append(q("MC:SingleAnswer:Vertical", "ai_used",
               "Did you use an AI tool while reading this chapter?",
               choices=["No", "Yes, to summarise or explain part of it",
                        "Yes, to help with the \"It is your turn\" task",
                        "Yes, something else"]))
    p.append(q("TE:Essay", "ai_what",
               "If you used one: what did you ask it, and what did you check "
               "for yourself afterwards?"))
    p.append("[[PageBreak]]\n")

    p.append("[[Block:Anything broken]]\n")
    p.append(q("MC:MultipleAnswer:Vertical", "defect",
               "Did you find anything broken? Tick everything that applies.",
               choices=["A typo or a wording error", "A number that looks wrong",
                        "A link or a notebook that did not open",
                        "A figure or table I could not read",
                        "A term used before it was defined",
                        "Something else", "Nothing"]))
    p.append(q("TE:Essay", "defect_where",
               "If you ticked anything: where is it, and what is wrong?"))
    p.append(q("TE:Essay", "anything",
               "Anything else you want on the record? Optional."))
    return "\n".join(p)


def build_md(chapters: list[str]) -> str:
    spine = "\n".join(
        f"| `{qid}` | {c} | {prompt} | {' · '.join(o)} | `{rec}` |"
        for qid, c, prompt, o, rec in SPINE)
    anchors = "\n".join(f"| **{v}** | `{qid}` | {prompt} |" for v, qid, prompt in ANCHORS)
    n = len(chapters)
    return f"""# Reading Feedback Survey — the instrument

*Generated by `scripts/build_reading_feedback_survey.py`. Do not hand-edit;
edit the script.*

One Qualtrics survey covers all **{n}** chapters of EDR\\|AI. The student names
the chapter on the first page, so Brightspace carries **one link** and the
export is **one file** with a `chapter` column.

**Import it:** Projects → Create project → Survey → **From a file** → upload
`qualtrics_reading_feedback.txt`.

---

## The shape of the instrument

A **stable closed spine**, **one rotating qualitative anchor**, and a
**conditional defect channel**, with the grade separated completely from the
content of the answers. It is a recurring *reader's field report*, not a
miniature course evaluation. It is not built to find out whether you liked a
chapter.

Two design rules follow from that, and both are load-bearing:

**No agree/disagree grid.** Every closed question asks about one construct with
options written for that construct. In a randomized multitrait-multimethod
comparison, item-specific questions measured better than comparable
agree/disagree items — Saris, Revilla, Krosnick & Shaeffer (2010),
[doi:10.18148/srm/2010.v4i1.2682](https://doi.org/10.18148/srm/2010.v4i1.2682).
A repeated grid also invites the undifferentiated responding Krosnick (1991),
[doi:10.1002/acp.2350050305](https://doi.org/10.1002/acp.2350050305), calls
satisficing, which is precisely the failure mode of a form answered {n} times.

**The closed items never change; only the anchor rotates.** With five students,
rotating the closed measures would leave too few observations per chapter to
read, and any apparent difference between chapters would partly be an artifact
of having asked different questions.

---

## 1. Identification

`student` (Purdue username) and `chapter` (dropdown, generated from the book
manifest so it can never drift from what the book publishes).

It is graded, so it cannot be anonymous. Say that on the page, as the intro
does, rather than letting students infer it. Identification creates a real risk
that criticism of the instructor's own book feels socially costly; the
literature on sensitive questions documents misreporting tied to
social-desirability and disclosure concerns — Tourangeau & Yan (2007),
[doi:10.1037/0033-2909.133.5.859](https://doi.org/10.1037/0033-2909.133.5.859).
Mitigate it structurally rather than promising it away: grade only submission,
keep the two views separate (below), and show the class that critical responses
changed the book.

## 2. The closed spine

| Item | Construct | Prompt | Options | Recode |
|---|---|---|---|---|
{spine}

`effort` is Paas's single-item nine-point mental-effort rating, adapted in
context — Paas (1992),
[doi:10.1037/0022-0663.84.4.429](https://doi.org/10.1037/0022-0663.84.4.429);
sensitivity discussed in Paas, van Merriënboer & Adam (1994),
[doi:10.2466/pms.1994.79.1.419](https://doi.org/10.2466/pms.1994.79.1.419).
Report it as **perceived invested effort**, never as a cognitive-load score:
separating intrinsic, extraneous and germane load takes a multi-item
instrument (Leppink et al. 2013,
[doi:10.3758/s13428-013-0334-1](https://doi.org/10.3758/s13428-013-0334-1))
that is far too long to repeat {n} times.

**Do not sum these six.** They answer different revision questions and do not
form a latent "chapter quality" scale. Do not compute a reliability
coefficient across them and do not publish a composite.

**"I cannot tell yet" and "I did not reach this section" are separate codes,
never low scores and never the midpoint.** Converting them silently destroys
the only distinction that makes them worth asking.

## 3. The rotating anchor (one of four, required)

| Version | Item | Prompt |
|---|---|---|
{anchors}

Shown above all four: *"{ANCHOR_INSTRUCTION}"*

Every version demands the same thing — a specific place in the chapter plus its
consequence — and every version carries a fallback clause, so "nothing to
report" still produces a located answer instead of a blank. What rotates is the
intellectual act: notice, diagnose, decide, or ask.

**Store which version fired.** Export it as `prompt_version` alongside the text,
and never read the four as answers to one question.

The anchor sits **before** the housekeeping questions on purpose. In a
web-survey experiment, later questions drew faster, shorter and more uniform
answers, and longer stated questionnaires reduced starts and completions —
Galesic & Bosnjak (2009),
[doi:10.1093/poq/nfp031](https://doi.org/10.1093/poq/nfp031). The highest-value
open response should not be the one that degrades.

## 4. Housekeeping

`coverage` — how much you actually read. **Never scored, and the question says
so on the page.** A self-report of effort that carries a penalty measures fear,
not effort. Unscored, it tells the author which chapters get skimmed, which is
the single most useful thing a reader can report about a book still being
written.

`notebook` and `notebook_effect` — the companion Colab notebook is a separate
artifact from the chapter and can fail on its own. A notebook cannot be
credited or blamed when it was never opened, so exposure is asked before effect.

`ai_used` and `ai_what` — on-brand, not surveillance. This course grades an AI
Research Ledger every week; the disclosure habit should not switch off for the
reading. Say plainly, as the survey does, that using a tool is allowed and only
concealing it is not.

## 5. The defect channel

`defect` (multi-select) and `defect_where` (conditional). This is the erratum
queue: typos, wrong numbers, dead links, unreadable figures, terms used before
they are defined. **Inspect any specific factual, broken-resource or
accessibility report even when only one student raises it.** A flag is a
request to inspect, not proof of an error.

---

## What the import file cannot carry

Advanced Format imports blocks, questions, choices and page breaks. Set these
five by hand after importing, in this order:

1. **Rotate the anchor.** Block "Your evidence anchor" → *Question
   Randomization* → **Randomly present 1 of the total questions**, with **Evenly
   Present Elements** on. That balances the four versions across the semester
   globally; it does **not** guarantee one of each per chapter, so do not
   describe it that way.
2. **Require the anchor.** All four anchor questions → *Force Response*, plus
   **content validation: 20–600 characters**. Leave the housekeeping block
   optional; forcing every question buys straightlining, not data.
3. **Show the conditional follow-ups only when they apply.** `notebook_effect`
   → show if `notebook` is not "No, I did not open it". `ai_what` → show if
   `ai_used` is not "No". `defect_where` → show if `defect` is anything other
   than "Nothing".
4. **Require the closed spine.** The six spine questions → *Force Response*.
   They are one click each.
5. **Optional: carry the chapter in the link.** Survey Flow → *Embedded Data* →
   `chapter_id`, then post per-chapter links `…?chapter_id=ch14` and hide the
   dropdown when it is set. Embedded fields must be **saved in Survey Flow** to
   appear in the export
   ([Qualtrics: Understanding Your Dataset](https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/data/download-data/understanding-your-dataset/)).
   With a seminar of five, one link plus the dropdown is less to administer.

Recommended options: **ballot-box stuffing prevention OFF** (the same student
submits {n} times), **save and continue ON**, **back button ON**, **anonymize
responses OFF**.

**Pilot with two readers before launch**, fix ambiguous wording, then **freeze
the spine**. Changing an item later changes what the time series means, so
record the date of any change you do make.

---

## Two views, one export

Export CSV with *Use choice text*
([Qualtrics: Export Response Data](https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/data/download-data/export-data-overview/)),
then work from two views of it:

**The credit ledger** — `student`, `chapter`, timestamp, and whether the anchor
is chapter-specific. This is the only view grading touches. Scoring is in
[`reading_feedback_grading.md`](reading_feedback_grading.md); per-chapter
deadlines are in
[`../planning/READING_FEEDBACK_SCHEDULE.md`](../planning/READING_FEEDBACK_SCHEDULE.md).

**The revision view** — chapter, Studio, the closed items, `prompt_version` and
the anchor text, notebook answers, and defect flags, with the student column
dropped. This is procedural separation, not anonymity: in a five-person
seminar, a writing style or a referenced experience can still identify someone.
Treat it accordingly.

### Reading it per chapter

Keep the full distribution. With five students, medians and counts are honest
summaries; means to two decimals and significance tests are not. Inspect a
chapter when **two or more** students report weak explainability, repeated
rereading, or low application readiness — and inspect **any** specific factual,
broken-resource or accessibility report, however few raise it.

Profiles are more informative than single scores:

| Pattern | Likely reading |
|---|---|
| High effort · strong explainability · little rereading | Productive challenge. Leave it alone. |
| High effort · weak explainability · repeated rereading | The explanation is failing. Go to the passage named in the anchor. |
| Strong explainability · low readiness | The idea landed; the applied instructions are underspecified. |
| Low usefulness · strong comprehension | The chapter needs a research-purpose bridge, not a simpler explanation. |
| Notebook made it harder · a broken-asset flag | Inspect the notebook now. |
| Several students quote the **same** passage in the anchor | One paragraph is doing the damage. Highest-value edit in the book. |

### Watch for degradation, without policing

Flag for inspection, never for automatic penalty: identical anchor text across
different chapters, anchors at the character minimum, sudden completion-time
outliers, repeated "I cannot tell yet" or "I did not reach", and a rising share
of late submissions. Duration alone never invalidates a response.

### Close the loop, or it decays

At the start of Studios 4, 8 and 12, spend two minutes on three columns: **You
noticed · I changed or will test · I am keeping this, because**. Never quote an
identifiable comment. The point is to make the contract observable: responses
enter a decision, and "no change" still gets a reason.

---

## Sources

All verified against the DOI or the publisher's page.

| Source | Used for |
|---|---|
| Saris, Revilla, Krosnick & Shaeffer (2010), [doi:10.18148/srm/2010.v4i1.2682](https://doi.org/10.18148/srm/2010.v4i1.2682) | Item-specific options over agree/disagree |
| Krosnick (1991), [doi:10.1002/acp.2350050305](https://doi.org/10.1002/acp.2350050305) | Satisficing; why a repeated grid is the wrong instrument here |
| Paas (1992), [doi:10.1037/0022-0663.84.4.429](https://doi.org/10.1037/0022-0663.84.4.429) | The single-item nine-point mental-effort rating |
| Paas, van Merriënboer & Adam (1994), [doi:10.2466/pms.1994.79.1.419](https://doi.org/10.2466/pms.1994.79.1.419) | Sensitivity of that rating |
| Leppink et al. (2013), [doi:10.3758/s13428-013-0334-1](https://doi.org/10.3758/s13428-013-0334-1) | Why one item is not a cognitive-load score |
| Galesic & Bosnjak (2009), [doi:10.1093/poq/nfp031](https://doi.org/10.1093/poq/nfp031) | Question position and response quality |
| Dunning, Heath & Suls (2004), [doi:10.1111/j.1529-1006.2004.00018.x](https://doi.org/10.1111/j.1529-1006.2004.00018.x) | Why `explain` is never a mastery grade |
| Tourangeau & Yan (2007), [doi:10.1037/0033-2909.133.5.859](https://doi.org/10.1037/0033-2909.133.5.859) | Sensitive questions under identification |
| Graham, Taylor, Olchowski & Cumsille (2006), [doi:10.1037/1082-989X.11.4.323](https://doi.org/10.1037/1082-989X.11.4.323) | Planned-missing designs, and why not here |

*Measurement core designed in a Codex partner run (gpt-5.6-sol, xhigh,
read-only, 2026-08-23) and verified and merged by Claude. The unscored
`coverage` item and the AI-use pair are course additions.*
"""


def main() -> None:
    index = lesson_index()
    chapters = [f"Ch. {l['display']} — {l['title']}"
                for l in sorted(index.values(), key=lambda l: l["display"])]
    OUT.mkdir(exist_ok=True)
    (OUT / "qualtrics_reading_feedback.txt").write_text(build_txt(chapters))
    (OUT / "reading_feedback_instrument.md").write_text(build_md(chapters))
    print(f"  ✓ surveys/qualtrics_reading_feedback.txt ({len(chapters)} chapters, "
          f"{len(SPINE)} spine items, {len(ANCHORS)} anchor versions)")
    print(f"  ✓ surveys/reading_feedback_instrument.md")


if __name__ == "__main__":
    main()
