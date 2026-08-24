#!/usr/bin/env python3
"""Build the one-link, per-studio EDR|AI reader-feedback survey.

The unit of observation is the studio (D57). The instrument is deliberately a
revision instrument, not a course evaluation or a psychometric scale: six
single-click items route the author's attention, and one short located answer
supplies the passage and proposed action.

The studio choices are generated from planning/MEETING_SCHEDULE.csv and the
book manifest. All question wording, documentation, force-response safeguards,
and revision mappings are authored here. The two files in surveys/ are generated
projections and must not be hand-edited.

Usage:
    .venv/bin/python scripts/build_studio_feedback_survey.py
"""
from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from session_readings import lesson_index, parse  # noqa: E402

OUT = REPO / "surveys"
SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.csv"
PROMPT_VERSION = "fixed_revision_v1"
TICK = chr(96)


@dataclass(frozen=True)
class ClosedItem:
    qid: str
    construct: str
    prompt: str
    choices: tuple[str, ...]
    revision_decision: str
    force_honesty: str
    reading_rule: str


# Six stable, item-specific, single-answer questions. They are not a scale.
SPINE = (
    ClosedItem(
        "coverage",
        "Reading exposure",
        "How much of this studio's assigned reading did you reach? Your answer "
        "does not affect credit.",
        ("All", "Most", "About half", "A small part", "None"),
        "Qualify every other answer by exposure. If the located note says the "
        "reading itself stopped progress, inspect length, order, and pacing; an "
        "outside barrier does not trigger a manuscript change.",
        "The options run from all to none; reporting no reading is explicitly "
        "unscored.",
        "Read as an exposure category, never as effort, diligence, or a grade.",
    ),
    ClosedItem(
        "clarity",
        "Explanation breakdown",
        "How often did the reading leave an idea unclear?",
        ("Never", "Once", "A few times", "Many times",
         "Most of the reading", "Not enough reading to judge"),
        "Repeated uncertainty sends the author to the named passage to clarify "
        "wording, define a term, or rebuild the explanation.",
        "Never reports no clarity problem; the final option reports insufficient "
        "exposure without pretending the prose was clear or unclear.",
        "Keep the full categories. Do not turn the final option into a high or "
        "low clarity score.",
    ),
    ClosedItem(
        "purpose",
        "Research-purpose connection",
        "How clearly did the reading show why these ideas matter for research?",
        ("Not at all", "A little", "Somewhat", "Mostly", "Completely",
         "Not enough reading to judge"),
        "A weak connection calls for a sharper research-purpose bridge or a "
        "better motivating example, not automatically a simpler explanation.",
        "The final option separates insufficient exposure from a weak purpose "
        "connection.",
        "Read descriptively. It is not a satisfaction or usefulness score.",
    ),
    ClosedItem(
        "ready",
        "Instructional readiness",
        "In the \"It is your turn\" sections you reached, how often were the "
        "directions clear enough to act on?",
        ("Always", "Usually", "About half the time", "Rarely", "Never",
         "Did not reach one"),
        "Low readiness with otherwise clear reading sends the author to the task "
        "directions, sequence, inputs, or worked model.",
        "The final option reports that no task was reached instead of forcing a "
        "false readiness judgment.",
        "Do not code \"I did not reach one\" as low readiness.",
    ),
    ClosedItem(
        "notebook",
        "Companion-notebook result",
        "What best describes your overall notebook experience in this studio?",
        ("Did not open one", "Opened one; did not run it",
         "A technical problem stopped me",
         "Used one; it made the reading clearer",
         "Used one; it made no difference",
         "Used one; it made the reading harder"),
        "Nonuse is not blamed on the notebook; access failure triggers repair; "
        "no effect or added difficulty triggers an integration/content check; "
        "clearer supports preserving the notebook move.",
        "Nonuse, opening without running, technical failure, and three experienced "
        "effects are all represented.",
        "Treat exposure and result as categories. Do not order or average them.",
    ),
    ClosedItem(
        "revision_focus",
        "First revision lane",
        "Which kind of change would help the next reader most?",
        ("Clarify an idea or term", "Improve an example, figure, or table",
         "Shorten or reorder",
         "Clarify an \"It is your turn\" task",
         "Fix a notebook or link",
         "Check a fact, number, or citation",
         "Keep a place as it is", "Not enough reading to choose"),
        "Route the following located answer to the first revision pass: "
        "explanation, illustration, structure, task, notebook, fact-check, "
        "preserve, or insufficient exposure.",
        "The last two options cover a genuine no-change judgment and insufficient "
        "exposure.",
        "This is one priority, not an exhaustive defect count.",
    ),
)

INTRO = (
    "About three minutes. Report on one studio from its reading and companion "
    "notebooks, not from class."
    "<br><br>"
    "Your Purdue username is attached because submission earns participation "
    "credit. Credit depends only on submitting by the deadline, never on what "
    "you say, and no answer affects another grade."
    "<br><br>"
    "I record credit first. Later, I remove the username column and use "
    "responses to revise the book. This is not anonymity in a five-person "
    "seminar. I report changes without naming or quoting you."
    "<br><br>"
    "Every question is required. The feedback items include honest none and "
    "did-not-reach answers."
)

STUDENT_PROMPT = (
    "Your Purdue username (the part of your email before @purdue.edu)."
)
STUDIO_PROMPT = "Which studio are you reporting on?"
ANCHOR_INSTRUCTION = (
    "One or two sentences. Be short and exact."
)
ANCHOR_PROMPT = (
    "Name the one place the author should work on first. Give the chapter and "
    "a heading, sentence, example, figure, step, or notebook cell so it can be "
    "found. Say what to change and why. If you would change nothing, name one "
    "place to keep and say why. If you stopped or did not start, name the "
    "chapter and say whether the reading or something outside it stopped you. "
    "No personal detail is needed."
)
ANCHOR_DECISION = (
    "Open the named location and either make the proposed change, test a "
    "competing change, preserve the named feature deliberately, or investigate "
    "the reported barrier."
)
ANCHOR_FORCE_HONESTY = (
    "The prompt supplies separate fallbacks for no change, stopping partway, "
    "and not starting; each fallback still names a chapter or place, and the "
    "barrier fallback asks for no personal detail."
)


def q(kind: str, qid: str, text: str,
      choices: tuple[str, ...] | list[str] | None = None) -> str:
    out = [f"[[Question:{kind}]]", f"[[ID:{qid}]]", text]
    if choices:
        out.append("[[Choices]]")
        out.extend(choices)
    return "\n".join(out) + "\n"


def expected_questions(studios: list[str]) -> list[
        tuple[str, str, str, tuple[str, ...]]]:
    questions = [
        ("DB", "intro", INTRO, ()),
        ("TE:SingleLine", "student", STUDENT_PROMPT, ()),
        ("MC:DropDown", "studio", STUDIO_PROMPT, tuple(studios)),
    ]
    questions.extend(
        ("MC:SingleAnswer:Vertical", item.qid, item.prompt, item.choices)
        for item in SPINE
    )
    questions.extend([
        ("DB", "anchor_note", ANCHOR_INSTRUCTION, ()),
        ("TE:Essay", "anchor", ANCHOR_PROMPT, ()),
    ])
    return questions


def build_txt(studios: list[str]) -> str:
    parts: list[str] = [
        "[[AdvancedFormat]]\n",
        f"[[ED:prompt_version:{PROMPT_VERSION}]]\n",
        "[[Block:Intro and studio]]\n",
        q("DB", "intro", INTRO),
        q("TE:SingleLine", "student", STUDENT_PROMPT),
        q("MC:DropDown", "studio", STUDIO_PROMPT, choices=studios),
        "[[PageBreak]]\n",
        "[[Block:Fast revision triage]]\n",
    ]
    for item in SPINE:
        parts.append(q(
            "MC:SingleAnswer:Vertical",
            item.qid,
            item.prompt,
            choices=item.choices,
        ))
    parts.extend([
        "[[PageBreak]]\n",
        "[[Block:Your revision note]]\n",
        q("DB", "anchor_note", ANCHOR_INSTRUCTION),
        q("TE:Essay", "anchor", ANCHOR_PROMPT),
    ])
    return "\n".join(parts).rstrip() + "\n"


def visible_word_count(studios: list[str], include_all_studios: bool) -> int:
    studio_text = (
        " ".join(studios)
        if include_all_studios
        else max(studios, key=lambda label: len(label.split()))
    )
    text = " ".join([
        INTRO,
        STUDENT_PROMPT,
        STUDIO_PROMPT,
        studio_text,
        *(item.prompt for item in SPINE),
        *(choice for item in SPINE for choice in item.choices),
        ANCHOR_INSTRUCTION,
        ANCHOR_PROMPT,
    ])
    plain = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"[A-Za-z0-9]+(?:[’'@-][A-Za-z0-9]+)*", plain))


def build_md(studios: list[str]) -> str:
    n = len(studios)
    listing = "\n".join(
        f"| **{i}** | {studio} |" for i, studio in enumerate(studios, 1)
    )
    spine_rows = "\n".join(
        f"| {TICK}{item.qid}{TICK} | {item.construct} | {item.prompt} | "
        f"{'<br>'.join(item.choices)} | {item.revision_decision} |"
        for item in SPINE
    )
    force_rows = "\n".join(
        f"| {TICK}{item.qid}{TICK} | {item.force_honesty} |"
        for item in SPINE
    )
    reading_rows = "\n".join(
        f"| {TICK}{item.qid}{TICK} | {item.reading_rule} |"
        for item in SPINE
    )
    required_ids = ("student", "studio", *(item.qid for item in SPINE), "anchor")
    required_list = ", ".join(f"{TICK}{qid}{TICK}" for qid in required_ids)
    total_words = visible_word_count(studios, include_all_studios=True)
    typical_words = visible_word_count(studios, include_all_studios=False)
    reading_seconds = round(typical_words / 238 * 60)
    planning_seconds = reading_seconds + 25 + 50

    return f"""# Studio Feedback Survey — the instrument

*Generated by {TICK}scripts/build_studio_feedback_survey.py{TICK}. Do not
hand-edit this file; edit the script.*

One Qualtrics survey covers all **{n}** Studios. The first page records the
Purdue username and studio, so the course page carries one link all semester
and the export is one file with a {TICK}studio{TICK} column. The unit of
observation is the studio, never the chapter.

**Purpose:** collect the smallest set of signals that can change a revision to
EDR\\|AI. This is not a course evaluation, a satisfaction survey, or a scale.
Every response question is required.

**Import:** Projects → Create project → Survey → **From a file** → upload
{TICK}qualtrics_studio_feedback.txt{TICK}.

**Due:** 11:59 PM on the Sunday that ends the studio week, except Studio 12,
which closes Friday, December 11. The generated dated schedule is
[{TICK}../planning/STUDIO_FEEDBACK_SCHEDULE.md{TICK}](../planning/STUDIO_FEEDBACK_SCHEDULE.md).

| # | Studio |
|---|---|
{listing}

---

## Instrument architecture

The response path has **nine answer fields**: username, studio, six
single-answer triage items, and one short located revision note. It has three
pages and no randomization, display logic, conditional follow-up, optional
question, matrix, or composite score. The embedded field
{TICK}prompt_version={PROMPT_VERSION}{TICK} records the wording version in
every export.

**Operational rule:** if any prompt or choice changes after collection begins,
bump {TICK}PROMPT_VERSION{TICK} before regenerating so unlike wordings are
never treated as one instrument.

The six closed items remain stable across all {n} administrations. The one
open item also remains fixed. Its required fallbacks let a reader report no
change, partial reading, or no reading without inventing a defect.

### Exact first-page text

{INTRO}

| Item | Exact prompt | Response |
|---|---|---|
| {TICK}student{TICK} | {STUDENT_PROMPT} | Single line |
| {TICK}studio{TICK} | {STUDIO_PROMPT} | The {n} generated choices above |

### The six closed items, in order

| Item | Construct | Exact prompt | Exact choices | Revision decision |
|---|---|---|---|---|
{spine_rows}

The revision mappings in the last column are **UNVERIFIED design judgments**.
They are explicit action rules for this book-revision workflow, not claims
that these single items have established psychometric validity.

Do not sum the six items. They were designed to route attention to different
revision decisions and have not been tested as a scale (**UNVERIFIED for this
instrument**).

### The one open item, last

Shown above it: *"{ANCHOR_INSTRUCTION}"*

{TICK}anchor{TICK}: *"{ANCHOR_PROMPT}"*

**Construct:** located revision action. **Revision decision:** {ANCHOR_DECISION}

The fixed prompt replaces four rotating prompts. With only five responses per
studio, rotation bought variety at the cost of prompt-dependent evidence and
manual setup. Choosing one direct action prompt is an **UNVERIFIED
instrument-specific design judgment**; pilot it before launch.

---

## Why the item set is this short

| Current element | Decision | Why |
|---|---|---|
| Prior familiarity | Cut | It contextualized self-report but did not identify a manuscript action. The located note and insufficient-exposure options handle interpretation more directly. |
| Self-rated explainability | Cut | It overlapped clarity and readiness, and self-assessment is not mastery. Nothing in this survey is used to grade learning. |
| Nine-point mental effort | Cut | Invested effort can mean productive challenge, inefficient prose, or persistence. Without performance evidence it does not select a revision. |
| Rereading frequency | Reworded as {TICK}clarity{TICK} | The new wording asks about meaning breakdown and sends the author to a named passage. |
| Broad usefulness | Reworded as {TICK}purpose{TICK} | A purpose connection points to a concrete bridge or motivating example; generic usefulness drifts toward evaluation. |
| Application readiness | Kept and made behavioral | Frequency across reached tasks works for studios with one to six chapters and separates non-exposure. |
| Four rotating anchors | Replaced by one fixed {TICK}anchor{TICK} | Every response now names a location and an action under the same prompt. |
| Notebook exposure + effect | Merged into {TICK}notebook{TICK} | One exhaustive item separates nonuse, no run, technical failure, help, no effect, and harm. |
| AI-use pair | Cut | It serves the course's AI Research Ledger, but it does not by itself choose a book revision. |
| Defect checklist + location | Merged into {TICK}revision_focus{TICK} + {TICK}anchor{TICK} | The category routes the issue; the single open item supplies its location and action. |
| Optional “anything else” | Cut | It had no guaranteed revision decision and cannot be honestly forced without becoming a “none” box. |

These keep/cut rulings are **UNVERIFIED instrument-specific design judgments**.
They should be reconsidered only if pilot responses show that a removed item
would have changed a manuscript decision that the retained items missed.

---

## Force Response audit

After import, Force Response applies to exactly these nine answer fields:
{required_list}. Text/Graphic items {TICK}intro{TICK} and
{TICK}anchor_note{TICK} display instructions and have no response field.

| Item | Why a forced answer stays honest |
|---|---|
| {TICK}student{TICK} | The respondent has one factual Purdue username; attribution is required for participation credit. |
| {TICK}studio{TICK} | The dropdown contains every scheduled studio with its chapter range. |
{force_rows}
| {TICK}anchor{TICK} | {ANCHOR_FORCE_HONESTY} |

This audit is a **UNVERIFIED response-process judgment** until cognitive
pretesting confirms that readers interpret the options and fallbacks as
intended.

---

## Burden budget

The import contains **{total_words} respondent-visible words** if someone
reads every one of the {n} studio labels and every response option. A more
realistic path, counting one studio label but every prompt and response
option, contains **{typical_words} words**.

- **VERIFIED source input:** Brysbaert's meta-analysis estimates average adult
  English silent reading of nonfiction at 238 words per minute
  ([doi:10.1016/j.jml.2019.104047](https://doi.org/10.1016/j.jml.2019.104047)).
  At that rate, the realistic-path text alone is about **{reading_seconds}
  seconds**.
- **UNVERIFIED planning allowances:** 25 seconds for username, studio,
  six clicks, and page movement; 50 seconds to compose one or two located
  sentences.
- **UNVERIFIED pre-pilot estimate:** about **{planning_seconds // 60}:{planning_seconds % 60:02d}**
  for a typical response, with a target median at or below **3:00**. Repetition
  should reduce studio-selection and instruction time, but that expectation has
  not been measured.

Before launch, run two think-aloud pilots with readers at the course level,
time them from link open to submission, and revise if either cannot answer
honestly or the median exceeds 3:00. After Studio 1, inspect Qualtrics Duration
as a workflow check, never as a validity score. CDC's CCQDER describes
cognitive interviewing as a way to learn how respondents understand, think
about, and answer questions (**VERIFIED**, retrievable at
[CDC CCQDER](https://www.cdc.gov/nchs/CCQDER/index.html)).

---

## Post-import manual steps

Qualtrics Advanced TXT carries the blocks, questions, IDs, choices, page
breaks, and the {TICK}prompt_version{TICK} embedded field. Its documented tag
set does not carry the response requirements or survey options below
(**VERIFIED**, [Qualtrics: Import & Export Surveys](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/)).

Do exactly these steps after import:

1. Select the nine answer fields {required_list} and enable **Add requirements
   → Force response**. Do not use Request Response.
2. In Survey Options, set **Ballot-box stuffing prevention OFF** so the same
   person can submit {n} times; **Anonymize responses OFF** because the survey
   is identified; **Back button ON**; and **Save and continue ON**.
3. Open Survey Flow and confirm the imported Embedded Data field
   {TICK}prompt_version{TICK} has the fixed value
   {TICK}{PROMPT_VERSION}{TICK}.
4. Preview one honest path for each edge case: no reading, no clarity problem,
   no task reached, no notebook opened, technical notebook failure, and no
   revision requested. Confirm that every path reaches Submit with exactly the
   nine required answers.
5. Publish one anonymous-link distribution and keep it open for all {n}
   submissions. Do not add question randomization, display logic, skip logic,
   minimum-length validation, or per-studio survey copies.

Force Response itself is documented by Qualtrics (**VERIFIED**,
[Qualtrics: Response Requirements & Validation](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/validation/)).
There are no other post-import logic or validation steps.

---

## Reading the export for revision

Export CSV with choice text. Make two separate working views:

1. **Credit view:** username, studio, timestamp, and submission status only.
   Content, direction, coverage, and ratings do not enter the grade.
2. **Revision view:** remove the username column; retain studio,
   {TICK}prompt_version{TICK}, the six closed items, and {TICK}anchor{TICK}.
   Removing the column is procedural separation, not anonymity in a
   five-person seminar.

Read all responses as cases; the sample is too small for scale construction or
inferential statistics by design. Start each revision pass with
{TICK}anchor{TICK}: open the named place, use {TICK}revision_focus{TICK} to
route it, and use clarity, purpose, readiness, notebook result, and coverage
to decide what kind of inspection it needs. Any exact claim of a wrong fact,
number, citation, inaccessible asset, or broken code is an inspection request,
not proof of a defect.

| Item | Reading rule |
|---|---|
{reading_rows}
| {TICK}anchor{TICK} | Preserve the location, proposed action, and reason together. Never detach the comment from its studio and prompt version. |

The two-pass procedure and reporting changes back to the class are
**UNVERIFIED context-specific mitigations** for the social pressure created by
identified feedback. They do not remove that pressure and must not be described
as anonymity.

---

## Evidence base and source audit

Every source below was retrieved by DOI, publisher page, or official
documentation on 2026-08-23. “Retained” means the source supports a design
choice still present; “cut with item” means the citation is real but no longer
earns space in the instrument rationale.

| Status | Source | Decision and bounded use |
|---|---|---|
| **VERIFIED · retained** | Saris, Revilla, Krosnick & Shaeffer (2010), [doi:10.18148/srm/2010.v4i1.2682](https://doi.org/10.18148/srm/2010.v4i1.2682) | Their randomized MTMM comparison supports item-specific response options over agree/disagree formats. It does not validate these six items. |
| **VERIFIED · retained** | Krosnick (1991), [doi:10.1002/acp.2350050305](https://doi.org/10.1002/acp.2350050305) | Defines survey satisficing and response strategies under cognitive demand; supports minimizing repeated burden. |
| **VERIFIED · retained** | Galesic & Bosnjak (2009), [doi:10.1093/poq/nfp031](https://doi.org/10.1093/poq/nfp031) | In a web-survey experiment, longer stated length reduced starts/completions and later questions drew faster, shorter, more uniform answers; supports keeping only six clicks before the one open response. |
| **VERIFIED · retained, application bounded** | Tourangeau & Yan (2007), [doi:10.1037/0033-2909.133.5.859](https://doi.org/10.1037/0033-2909.133.5.859) | Reviews situational misreporting on sensitive questions. Treating criticism of an identified instructor-authored book as socially sensitive is an **UNVERIFIED contextual inference**. |
| **VERIFIED · retained** | Brysbaert (2019), [doi:10.1016/j.jml.2019.104047](https://doi.org/10.1016/j.jml.2019.104047) | Supplies the 238-wpm adult nonfiction reading estimate used only in the burden budget. |
| **VERIFIED · retained** | CDC/NCHS CCQDER, [official page](https://www.cdc.gov/nchs/CCQDER/index.html) | Supports cognitive interviewing to examine how respondents understand and answer questions; it does not prove that a two-person pilot finds every problem. |
| **VERIFIED · technical** | Qualtrics, [Import & Export Surveys](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/) and [Response Requirements & Validation](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/validation/) | Defines supported Advanced TXT tags and the manual Force Response setting. |
| **VERIFIED · cut with {TICK}effort{TICK}** | Paas (1992), [doi:10.1037/0022-0663.84.4.429](https://doi.org/10.1037/0022-0663.84.4.429) | The nine-point item measures perceived invested mental effort; the construct did not select a manuscript action here. |
| **VERIFIED · cut with {TICK}effort{TICK}** | Paas, van Merriënboer & Adam (1994), [doi:10.2466/pms.1994.79.1.419](https://doi.org/10.2466/pms.1994.79.1.419) | Supports reliability/sensitivity of subjective mental-effort ratings in the studied instructional settings, not their actionability for this book. |
| **VERIFIED · cut with {TICK}effort{TICK}** | Leppink et al. (2013), [doi:10.3758/s13428-013-0334-1](https://doi.org/10.3758/s13428-013-0334-1) | Develops a multi-item instrument for types of cognitive load; it does not rescue a single ambiguous revision signal. |
| **VERIFIED · cut with {TICK}explain{TICK}** | Dunning, Heath & Suls (2004), [doi:10.1111/j.1529-1006.2004.00018.x](https://doi.org/10.1111/j.1529-1006.2004.00018.x) | Reviews systematic limits of self-assessment. The survey no longer asks for self-rated mastery. |
| **VERIFIED · cut with rotation** | Graham, Taylor, Olchowski & Cumsille (2006), [doi:10.1037/1082-989X.11.4.323](https://doi.org/10.1037/1082-989X.11.4.323) | The planned-missing-design paper is real, but no planned-missing or rotating design remains. |

"""


def parse_questions(txt: str) -> list[
        tuple[str, str, str, tuple[str, ...]]]:
    lines = txt.splitlines()
    parsed: list[tuple[str, str, str, tuple[str, ...]]] = []
    i = 0
    while i < len(lines):
        match = re.fullmatch(r"\[\[Question:(.+)]]", lines[i])
        if not match:
            i += 1
            continue
        kind = match.group(1)
        if i + 2 >= len(lines):
            raise ValueError(f"Incomplete question after line {i + 1}")
        id_match = re.fullmatch(r"\[\[ID:([A-Za-z0-9_]+)]]", lines[i + 1])
        if not id_match:
            raise ValueError(f"Question at line {i + 1} has no adjacent ID")
        qid = id_match.group(1)
        prompt = lines[i + 2]
        i += 3
        choices: list[str] = []
        if i < len(lines) and lines[i] == "[[Choices]]":
            i += 1
            while i < len(lines) and lines[i] and not lines[i].startswith("[["):
                choices.append(lines[i])
                i += 1
        parsed.append((kind, qid, prompt, tuple(choices)))
    return parsed


def validate_artifacts(txt: str, md: str, studios: list[str]) -> None:
    if len(studios) != 12 or len(set(studios)) != 12:
        raise ValueError("Expected exactly 12 unique studio choices")
    if not txt.startswith("[[AdvancedFormat]]\n") or not txt.endswith("\n"):
        raise ValueError("Advanced Format header or final newline is missing")

    expected = expected_questions(studios)
    parsed = parse_questions(txt)
    if parsed != expected:
        raise ValueError("Parsed Advanced Format questions differ from source data")

    qids = [qid for _kind, qid, _prompt, _choices in parsed]
    if len(qids) != len(set(qids)):
        raise ValueError("Question IDs must be unique")
    if txt.count("[[PageBreak]]") != 2:
        raise ValueError("Expected exactly two page breaks")
    expected_blocks = (
        "[[Block:Intro and studio]]",
        "[[Block:Fast revision triage]]",
        "[[Block:Your revision note]]",
    )
    if tuple(re.findall(r"\[\[Block:[^]]+]]", txt)) != expected_blocks:
        raise ValueError("Block order differs from the three-page design")

    allowed_exact = {
        "[[AdvancedFormat]]", "[[Choices]]", "[[PageBreak]]",
        f"[[ED:prompt_version:{PROMPT_VERSION}]]",
        *expected_blocks,
    }
    for tag in re.findall(r"\[\[[^]\n]+]]", txt):
        if (tag in allowed_exact
                or re.fullmatch(r"\[\[Question:(DB|TE:SingleLine|TE:Essay|"
                                r"MC:DropDown|MC:SingleAnswer:Vertical)]]", tag)
                or re.fullmatch(r"\[\[ID:[A-Za-z0-9_]+]]", tag)):
            continue
        raise ValueError(f"Unsupported Advanced Format tag: {tag}")

    for _kind, qid, prompt, choices in expected:
        if f"{TICK}{qid}{TICK}" not in md:
            raise ValueError(f"Documentation omits question ID {qid}")
        if prompt not in md:
            raise ValueError(f"Documentation wording differs for {qid}")
        for choice in choices:
            if choice not in md:
                raise ValueError(
                    f"Documentation omits choice {choice!r} from {qid}"
                )
    for item in SPINE:
        exact_row = (
            f"| {TICK}{item.qid}{TICK} | {item.construct} | {item.prompt} | "
            f"{'<br>'.join(item.choices)} | {item.revision_decision} |"
        )
        if exact_row not in md:
            raise ValueError(
                f"Documentation row differs from source data for {item.qid}"
            )
    for studio in studios:
        if txt.count(studio) != 1 or md.count(studio) != 1:
            raise ValueError(f"Studio choice is missing or duplicated: {studio}")

    response_ids = ("student", "studio", *(item.qid for item in SPINE), "anchor")
    force_sentence = ", ".join(
        f"{TICK}{qid}{TICK}" for qid in response_ids
    )
    if force_sentence not in md:
        raise ValueError("Force Response list is not generated from response IDs")
    if "Optional." in txt or "Anything else" in txt:
        raise ValueError("The response path contains an optional catch-all")


def studio_choices() -> list[str]:
    """"Studio 3: Ground it in verified evidence (Ch. 8-9)", generated.

    The label carries the chapters so the dropdown tells the respondent which
    reading the response covers. The chapter set comes from the same anchors
    that generate the course schedule.
    """
    index = lesson_index()
    meetings = list(csv.DictReader(SCHEDULE.open(newline="")))
    anchor: dict[str, int] = {}
    assigned_at: dict[str, int] = {}
    read_modes = ("first-read", "route", "route-contrast", "optional")
    for row in meetings:
        for lesson_id, mode in parse(row["book_reading"]):
            meeting = int(row["meeting"])
            if mode == "assigned":
                assigned_at.setdefault(lesson_id, meeting)
            if lesson_id in anchor or mode not in read_modes:
                continue
            anchor[lesson_id] = meeting
    for lesson_id, meeting in assigned_at.items():
        anchor.setdefault(lesson_id, meeting)

    at: dict[int, list[int]] = {}
    for lesson in index.values():
        at.setdefault(anchor[lesson["id"]], []).append(lesson["display"])

    studios: dict[int, dict] = {}
    for row in meetings:
        match = re.match(
            r"Week (\d+) — (Studio (\d+): .+)$",
            row["unit"].replace('"', ""),
        )
        if not match:
            continue
        studio = studios.setdefault(
            int(match.group(3)),
            {"title": match.group(2), "chapters": []},
        )
        studio["chapters"] += at.get(int(row["meeting"]), [])

    out = []
    for number in sorted(studios):
        chapters = sorted(studios[number]["chapters"])
        span = (
            f" (Ch. {chapters[0]}-{chapters[-1]})"
            if len(chapters) > 1
            else (f" (Ch. {chapters[0]})" if chapters else "")
        )
        out.append(f"{studios[number]['title']}{span}")
    return out


def main() -> None:
    studios = studio_choices()
    txt = build_txt(studios)
    md = build_md(studios)
    validate_artifacts(txt, md, studios)

    OUT.mkdir(exist_ok=True)
    (OUT / "qualtrics_studio_feedback.txt").write_text(
        txt, encoding="utf-8", newline="\n"
    )
    (OUT / "studio_feedback_instrument.md").write_text(
        md, encoding="utf-8", newline="\n"
    )
    print(
        "  ✓ surveys/qualtrics_studio_feedback.txt "
        f"({len(studios)} studios, {len(SPINE)} closed items, "
        "1 open item, 9 required response questions)"
    )
    print("  ✓ surveys/studio_feedback_instrument.md")
    print("  ✓ internal Advanced Format and documentation-parity checks")


if __name__ == "__main__":
    main()
