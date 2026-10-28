# Course Reflection — the slot

**Due: Friday Dec 11, 2026, 11:59 PM** (the last class meeting; the Studio 12
feedback response closes the same night).

**Graded inside Participation (9%)**, for completion only — submitted or not.
One credit, exactly like every other participation item; the rule is in
[`participation_grading.md`](participation_grading.md).

**What it is not.** It is not a course milestone. The milestone chain closes at
M17, the reproducible package, due Sun Dec 6 (D91); Week 16 carries no milestone
(D54), and the last Friday collects this reflection under participation instead.
It is also not the M16 conference reflection, which is a milestone with its own
brief, worked in the two asynchronous sessions after the Expo (D91). Keep the two apart
in the gradebook and in how they are described to students.

**Why the last day.** The final session is the course-closing reflection
session. Writing it while the semester is still in the room produces a different
document from one written a week later, and the point of the exercise is the
first one.

---

> **Instrument written 2026-10-27** at Professor Moreira's request, with one goal:
> specific feedback on how to improve the course. (Until then this file recorded
> only the slot, the deadline and the grading rule, which are settled: D54 for
> the date, D57 for the grading.) The Qualtrics Advanced Format import file
> [`qualtrics_course_reflection.txt`](qualtrics_course_reflection.txt) is the
> source of truth for the wording; this page describes it.

**What must be true of it, whatever it asks**

- It is a reflection, so it is graded on submission, never on what it concludes.
  A student who reports that the course changed nothing earns the same credit as
  one who reports that it changed everything.
- It is distinct from the University's course evaluation, which is anonymous,
  administered separately, and never graded. Say that on the page so the two are
  not confused.

---

## The instrument

**Survey name.** Qualtrics project *HONR 46400: Course Reflection Survey*; students
see *Course reflection: scientific discovery and AI in research*. Answered in the
room during the last class (the 5–45 block of meeting 43), about twenty-five
minutes.

**No name is collected.** Candid criticism is the point, so the survey asks for no
name or username and Qualtrics is set to anonymize responses (no IP address or
location). Credit is verified the way the Brightspace item already asks: a
screenshot of the survey's confirmation page uploaded to *Participation:
Reflection Survey*. With four students a project can still be recognized from
what is written, so the intro promises that the answers are read **only after
final grades are submitted**. That is a promise to keep.

**How it is built.** Every question is forced except `anything_else`. Back
button on, finish later on. The end-of-survey message tells the student to
screenshot the page and upload it. Availability opens Fri Dec 11, 12:00 AM and
closes Sat Dec 19, 12:00 AM (Eastern), covering the seven-day half-credit window
of the participation rule.

| Block | ID | Type | What it asks | The decision it informs |
|---|---|---|---|---|
| Intro | `intro` | text | Purpose, credit rule, no-name rule, not the University evaluation, how to prove submission | — |
| Your semester as a researcher | `research_lesson` | essay | The most important thing learned about trustworthy evidence, read backwards from the Expo claim, and where it happened | Which weeks and milestones actually teach the course's core idea |
| | `ai_division` | essay | The task where AI helped most and the decision refused to any tool, and what prepared each | Whether the AI workflow is taught where it is used |
| | `readiness` | matrix (8 × 4) | Readiness to do each research step alone: question, design, sources, data, reproducible analysis, AI checking, bounded claim, public defense | Which skills need more course time |
| What helped and what to change | `components` | matrix (14 × 5) | How much each part of the course helped the project: book, IYT, lessons and notebooks, lab meeting, Friday studios, milestone instructions, written feedback and numbered requests, mentoring emails and action plan, mentor meetings, AI Research Ledger, AI tools, poster labs, pitches and peer review, package and cold run | What to keep, fix, or cut, part by part |
| | `keep` | essay | The one part to keep exactly as it is, named precisely | Protects what works from the next redesign |
| | `change_first` | essay | The one change to make first: where, what instead, what it fixes | The first revision for next fall |
| | `cut_add` | essay | One thing that cost time without helping, one thing missing | Scope: what to remove and what to add |
| Pace, feedback, and AI | `workload` | single choice | Workload against courses with the same credit | Calibration of the total load |
| | `hardest_stretch` | single choice | The milestone stretch hardest to keep up with (M1–4, M5–7, M8–10, M11–16, M17, none) | Where the calendar is overloaded |
| | `pace_fix` | essay | What made it hard, and the timing, instruction or support change that would help | The fix for that stretch |
| | `feedback_fix` | essay | One change to how feedback reached the student (reviews, numbered requests, emails, meetings) | The feedback and mentoring system |
| | `ai_fix` | essay | Where Ask, Verify, Document and the ledger helped or got in the way, and one change | The AI workflow and its paperwork |
| Looking ahead | `recommend` | single choice | Would recommend to a friend in the Honors College | A summary signal, read with `advice_next` |
| | `advice_next` | essay | What to tell someone deciding whether to take the course | The course's honest description |
| | `anything_else` | essay, optional | Anything else | — |

**Cut first if the room runs short:** `readiness`, then `recommend` and
`advice_next`. Keep `change_first`, `components` and `keep` whatever happens.

**Reading four responses.** After final grades: tabulate `components` and
`readiness` side by side (four rows each, so read counts, never averages);
read `change_first`, `cut_add`, `pace_fix`, `feedback_fix` and `ai_fix` together
and list each named location with its proposed change; where two or more
students name the same place, that change goes first into the next edition's
plan, and every adopted change is recorded in `_project_docs/DECISIONS.md`.
