# Reading Feedback — how it is scored

Reading feedback is graded inside **Participation (9%)**, which the syllabus
defines as "feedback surveys, lecture-notebook completion, and other
constructive contributions to the course."

The instrument is in [`reading_feedback_instrument.md`](reading_feedback_instrument.md).
The per-chapter deadlines are in
[`../planning/READING_FEEDBACK_SCHEDULE.md`](../planning/READING_FEEDBACK_SCHEDULE.md).

> ⚠ **One decision is still yours.** The syllabus states Participation as a
> single 9% block and does not split it. The split below is a proposal, not a
> published rule. Confirm it or change it before the survey link goes on
> Brightspace, then mirror it into `brightspace/gradebook_spec.md`.

| Component | Share of the course |
|---|---|
| Reading feedback (this instrument) | 5% |
| Lecture-notebook completion | 2% |
| Constructive contribution in class | 2% |

*A reasonable alternative, argued in the partner design: make reading feedback
the operational definition of the whole 9%. Grading "how often a student spoke"
in a five-person seminar is hard to defend and harder to evidence, while this
instrument produces a dated, auditable record. The cost is that it contradicts
the syllabus as published, so it is a change for a future edition, not this one.*

---

## The credit rule

The grade attaches to **identity and timing**, never to content. Praise,
criticism, confusion, low ratings and reported AI use are all worth the same.

| Credit | Condition |
|---|---|
| **1.0** | A valid response, submitted before the class the reading was assigned for |
| **0.5** | A valid response, submitted after that class but within seven days |
| **0** | Missing, more than seven days late, or still non-responsive after one offered revision |

A **valid** response has all five of:

1. an attributable Purdue username;
2. the right chapter;
3. all six closed spine items answered;
4. an anchor answer that names something **specific to that chapter** — a
   passage, example, figure, step, revision or question — rather than an answer
   that would fit any chapter;
5. a location for any problem it reports.

Resubmitting the same chapter replaces the earlier response inside the same
window. It never earns extra credit.

## The formula

Let **R** be the number of chapter responses assigned to that student, and
**d = ⌈0.10 × R⌉** the number of lowest credits dropped automatically.

```
reading-feedback points = 5.0 × (sum of the highest R − d credits) / (R − d)
```

For this edition, **R = 36** for a typical student: 34 chapters required of
everyone, plus 2 pathway chapters (your declared route and the contrast the
instructor assigns you). One further chapter binds only if your design has
stages, and it raises R for that student. So **d = 4**, and **32 valid, on-time
responses earn the full 5 points.** There is no credit for more than R.

**Four free drops.** Your four lowest credits are dropped automatically. No
excuse, no email, no negotiation. Illness, a bad week, a chapter you genuinely
could not get to: the drops exist so none of that has to become a conversation.
For an excused absence longer than the drops can absorb, remove those chapters
from that student's **R** rather than scoring them zero.

---

## What is deliberately NOT scored

**Whether you liked the chapter.** A careful complaint and a careful compliment
score identically. Say this on the first day, and say it again the first time
someone writes an obviously nervous compliment. An instrument that pays for
praise collects praise, and praise cannot revise a book.

**How much of the chapter you read.** The `coverage` item is unscored and says
so on the page. A self-report of effort that carries a penalty measures fear,
not effort.

**Any of the ratings.** `explain` is self-reported comprehension, not
demonstrated mastery, and self-assessment diverges from performance in
predictable ways (Dunning, Heath & Suls 2004,
[doi:10.1111/j.1529-1006.2004.00018.x](https://doi.org/10.1111/j.1529-1006.2004.00018.x)).
It must never become a mastery grade. `effort` is not a virtue score either:
high effort on a hard chapter is the design working.

**Whether you used AI.** Using a tool while reading is allowed. Concealing it is
the violation, and that is the rule the AI Research Ledger already runs on.

**Length.** Two exact sentences beat two vague paragraphs, and the anchor box
caps at 600 characters for exactly that reason. Say it out loud once; students
carry an assumption that longer is safer.

---

## Running it each week

1. Qualtrics → **Data & Analysis → Export → CSV**, with *Use choice text*.
2. Filter to chapters whose deadline has passed.
3. **Credit ledger view.** Read four columns: `student`, `chapter`, timestamp,
   and the anchor text. Award 1 / 0.5 / 0 on the rule above. At roughly fifteen
   seconds a response this is about twenty minutes a week for a seminar of five.
4. **Revision view.** Drop the student column and read the closed items,
   `prompt_version` + anchor, notebook answers and defect flags. This is the
   book-revision pass, and it is a different sitting from grading.
5. Enter the running total in Brightspace at the same cadence as the quizzes.

**Borderline calls.** When an anchor is chapter-specific but thin, award the
credit and reply once asking for the missing specificity next time. Reserve 0
for responses that are absent or that could have been written without opening
the chapter. A first non-responsive answer gets one offered revision, not a zero.

**Close the loop, or the instrument decays.** At the start of Studios 4, 8 and
12, spend two minutes on three columns — **You noticed · I changed or will
test · I am keeping this, because**. Never quote an identifiable comment. The
point is to make the contract observable: responses enter a decision, and "no
change" still gets a reason.
