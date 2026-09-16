# AI Tool Survey — the instrument and the decision it settles

**Purpose.** Decide whether the course buys every student a seat in an
instructor-administered AI workspace, and if so, whether that workspace comes
from **Anthropic (Claude)** or **OpenAI (ChatGPT)**.

**Status.** Hand-authored, not generated. `qualtrics_ai_tool_survey.txt` in this
folder is the Qualtrics Advanced Format import file and is the source of truth
for the wording; edit it there, re-import, and never rebuild the questions by
hand inside the Qualtrics UI.

**Not graded.** This is **not** a participation item (D57 fixes participation at
three item families, N = 14, and this is none of them), **not** an IYT Practice
item (D61), and not a milestone. Nothing it collects may set any grade. The
announcement says so explicitly and the survey's first screen repeats it.

**Identified, and honest about it.** The username is collected because the
decision is per student: who needs a seat, who already pays for one, who needs
setup help. At n = 4 anonymity is not achievable and the instrument does not
claim it. Responses are FERPA-adjacent and live only in Qualtrics and in the
gitignored `_adm/`, never in a tracked path.

---

## Settings to apply in Qualtrics after import

The TXT format carries questions, not survey options. After importing, click:

| Setting | Value | Why |
|---|---|---|
| Force response | On for `student`, `subs_current`, `student_offers`, `tools_extent`, `training_need`, `preference`, `purdue_account` | These seven are the decision inputs. |
| Request response | On for `tools_verify`, `training_topics`, `machine`, `terminal` | Useful, not decisive. |
| Force response | **Off** for every `TE:Essay` and for `subs_spend` | Spending is optional by design; prose must never be compelled. |
| Anonymize responses | **Off** | Deliberate: the decision is per student. |
| Survey expiration | The announced deadline | Keeps the record clean. |

---

## How the answers decide the question

Read them in this order. The first rule that fires settles it.

**1. Does the course need to buy anything at all?**
If `student_offers` shows a working education route for a company, or
`access_other` shows most of the four already covered through a job or another
program, the answer may be **buy nothing**. Confirm the Purdue IT and Claude for
Education questions before spending either way.

**2. Does anyone already pay?**
`subs_current` is the duplication check. Buying a workspace from the vendor a
student already pays for gives them a second copy of what they have; buying the
other one gives them a second tool. Neither is automatically better, but a
student paying $20 a month out of pocket for the vendor you are about to buy
should be told they can cancel.

**3. What can they actually run?**
`machine` and `terminal` gate the whole plan. A Chromebook or a lab machine they
do not control cannot run a local agentic assistant, and "never opened a
terminal" from most of the room means the desktop-app path is mandatory and the
training block is not optional. If this row is bad enough, the honest answer is
that the course does not adopt an agentic tool this term.

**4. Where is the existing fluency?**
`tools_extent` is the substantive input. Concentrated real use on one vendor's
agentic tool is a live argument for that vendor: it is the one with a student in
the room who can help another student. Uniform "never heard of it" means
fluency is not a tiebreaker and the decision falls to instructor support
capacity, which favors Claude Code.

**5. What do they want, and why?**
`preference` and `preference_why`. At n = 4 a stated preference with a real
reason outweighs a thin margin on any other row. A student who says switching
vendors would slow their project down is reporting a true cost.

**6. How much teaching does this add?**
`training_need` and `training_topics` price the decision in class time, which is
scarcer than the money. If the modal answer needs a full session plus a guide,
that session has to come from somewhere, and Weeks 11 to 14 are the conference
block.

**7. Will they join at all?**
`purdue_account`. A "no" here is not an obstacle to route around; it is a
finding. The AI Research Ledger rule and the public-data-only boundary apply
whatever tool a student uses, and the course has never required a specific
vendor.

`tools_verify` does not decide the vendor. It is a teaching signal: rare or
never checking output is the exact habit the course exists to correct, and it
belongs in the training block and in how the ledger is introduced, not in the
purchase decision.

---

## What the answers may not be used for

- Setting or adjusting any grade, including participation.
- Identifying a student in class as the one who does or does not pay.
- Quoting a named student in the announcement of the decision.

## After the decision

Post the outcome to the class, record it in `_project_docs/DECISIONS.md` if it
changes what the course provides, and — if a workspace is bought — add the seat
provisioning, the invitation date, and the Dec 11 cancellation to the course
task tracker. Raw responses stay out of this repository.
