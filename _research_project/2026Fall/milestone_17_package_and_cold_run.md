# Course milestone M17 — Reproducible Package and the Peer Cold Run

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge** — course milestone **M17**.
> This submission presents **Book Milestone 11 — Your reproducible package** (version 1): work from its [milestone page](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/studios/milestone11-reproduce-and-package.html#milestone).
<!-- book-milestone-bridge:end -->

<!-- carry-forward-start:begin -->
> **Start here: what this milestone collects from you.**
>
> 1. **Your carry-forward record, at the very top.** Open my review email and your research action plan side by side. Answer every numbered request for this milestone (each has an ID like `IR-M17-01`) and every step your plan sets for this milestone. Next to each one, write **Done** and exactly where I can find it, or **Not adopted**, with your reason and what you chose instead. Several items can point to the same piece of work. Component 9 shows the request table and Component 10 the plan section.
> 2. **Then your milestone work and files**, exactly as *What to Submit on Brightspace* and the components below list them.
>
> **How this counts.** Your answer to the action plan is worth 10 points of the rubric, scored for you individually. Each numbered request left unanswered costs 5 points, up to 20. Only requests and plan steps I sent you at least 48 hours before the deadline count; anything later moves to the next milestone. A step that is also a numbered request is counted once, as a request. If I sent you no numbered requests, or no plan steps apply, say so in one line. Not sure what applies to you? Write to me before the deadline; that is exactly what I am here for.
<!-- carry-forward-start:end -->

## About the Research Project

Your semester project is **individual by default**: one researcher, one question,
carried from curiosity to a defended, reproducible claim. With instructor
approval, and only if at least three active projects remain and the required
peer-evaluation assignments are feasible, you may instead complete the same
chain as a group. The same five Final Project components apply
in either mode. Unless this brief marks a requirement as individual, an approved
group submits one shared artifact naming every member, and its shared rubric
rows receive a common score. Each member's AI Research Ledger and any other
requirement marked individual are scored per member, so recorded milestone
scores can differ only on those rows. Every member remains responsible for the
complete work and their own defense. Peer Evaluation remains a true peer
rating: group members rate every teammate; an individual-project researcher
is rated by two instructor-assigned project peers; nobody rates themselves. See
[Final Project — Grading and Project Modes](final_project_grading_and_project_modes.md).
It runs through milestones
**M1–M17**, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes here, with the
reproducible package and the cold run. Every milestone
follows the same cadence: **Friday-studio kickoff → develop across the week →
work it at the Friday studio → submit by the deadline on the course platform,
11:59 PM → revise (where eligible)**. Every milestone also updates your
cumulative **Research Project Dossier** and appends at least one row to your
**AI Research Ledger** — the running record of what you handed to AI and how you
checked it. Milestone weights live in
[Final Project — Grading and Project Modes](final_project_grading_and_project_modes.md);
instructions and rubrics live one page per milestone, like this one.

This milestone closes the project: it produces the **reproducible package** that
carries your work past the semester, the bundle another researcher needs to
obtain your results without you in the room. It is **the last milestone in the
chain**, and its 100-point score is one of the seventeen averaged inside Final
Project's **Milestone Deliverables** component. M17 is **revision-eligible** under
the standing policy.

---

## What to Submit on Brightspace

Due: **Sunday, December 6, 11:59 PM.** The week builds it in order: on Monday you
assemble the package and run it cold yourself; on **Wednesday, in class, you and
a colleague exchange packages** and each runs the other's from the written
instructions alone; the Friday studio repairs your package against that run,
clears the two blocking gates, and makes the second clean run.

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m17_package.zip`** *or* a shared folder or repository link | Your **repaired reusable package** (Component 1): the seeded notebook, the data or its access recipe, the environment record, the README, the licence and permissions note, the decision log, the dated frozen manifest, and your current claim-to-evidence table, frozen with it. |
| 2 | **`lastname_m17.pdf`** | Your **package record**, in this order: the **Instructor Request Record** (Component 9); your **action plan's commitments** (Component 10); your own cold-run record (Component 2); the cold-run report you wrote on your colleague's package and your response to the report you received (Components 3 and 4); the two **blocking gate records** (Components 5 and 6); the **second clean-run record** (Component 7); this milestone's **AI Research Ledger** rows (Component 8); and the dossier line (Component 11). |
| 3 | **EDR\|AI "It is your turn" — ch. 36, ch. 37** | **Already submitted, not collected again here.** These sections were due on their own reading dates, as IYT Practice submissions; the dated list is on the course page. Confirm each one is complete and carry the work into this milestone and your Research Project Dossier. See "The Book Anchor" below. |

If you submit a folder or repository link, set sharing so the instructor can open
it, and confirm the package runs top to bottom in a clean session.

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook) **by the date that chapter's reading is
due**:

- Ch. 36 — [Replication and Reproduction](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part6-after-conference/32-replication-and-reproduction.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch36_replication_and_reproduction.ipynb)
- Ch. 37 — [Open and Reusable Research Packages](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part6-after-conference/34-open-and-reusable-research-packages.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch37_open_and_reusable_research_packages.ipynb)

These sections are the point of the reading, not extra work: across the
semester, the book's "It is your turn" sections — one per lesson, submitted on the date its reading is due — chain into a complete research artifact, so what you complete here is a
draft piece of your own. You hand each section in on the date its own reading is due, under
**IYT Practice** — the dated list is on the course page. They are not
collected a second time here: carry the completed work forward into this
milestone and your Research Project Dossier.

---

## Purpose

A result a reader believes but cannot rerun is half a claim. This milestone
builds the other half: a package that lets someone else obtain your numbers from
your data and your code, following only what you wrote down.

**Reproduction** means obtaining the same result from the same data and the same
code, following only the written instructions. It is not **replication**, which
gathers new data and asks whether the finding shows up again. Your package is
tested for reproduction: same inputs, same steps, same numbers, a different
session and a different pair of hands.

The test is a **cold run**, a run made in a clean environment by someone
following your written instructions and nothing else. A **clean environment** is
a fresh session with nothing left over from your work, such as a brand-new Colab
runtime where the file you uploaded last week no longer exists. Cold runs expose
the steps you know by heart and never wrote down: every question the runner has
to ask you is a missing line in your documentation.

**Reproduce the uncertainty, not only the point estimate.** If your interval,
standard error, or sensitivity range does not come back with the same value, your
result has not reproduced, however well the headline number matched.

> **A question that often comes up here:** *"My package reran with zero errors.
> Isn't it done?"* A clean run proves the package is **runnable**, not
> **correct**. No script can see that a seed is fixed on the wrong sample, that a
> logged reason is a bad reason, or that the analysis answers a different question
> than the one you declared. Those are failures a person finds reading your work
> cold, which is why your colleague's run exists, and why an AI-drafted README
> still needs a human run to validate it.

---

## Components

### 1. The reusable research package

Assemble the whole bundle before you test it, so the cold run tests the thing you
would actually hand over. A **research package** is everything another researcher
needs to obtain your result, with nothing assumed to live on your laptop:

- **The seeded notebook.** Your analysis notebook with `SEED = 464` set through
  `np.random.default_rng(SEED)`, passing **restart-and-run-all**: clear the
  kernel, run every cell from the top, no manual fixes, and the headline number
  comes back.
- **The data or its access recipe.** The file itself, when your permissions allow
  sharing it, or a written route to it: source, exact URL or archive record,
  retrieval date, and any registration the reader must complete.
- **The environment record.** The library versions your run used, such as a
  `requirements.txt` or a printed list of package versions.
- **The README.** Its first three lines say what the project asks, what the
  headline found, and how to run everything. Then the run order, the expected
  outputs, and where each output lands.
- **The licence and permissions note.** The terms under which the package may be
  reused, with the reuse boundary stated plainly. What you may share is set by
  your permission determination, and the package says so.
- **The decision log.** Every by-hand choice, each exclusion and cut point, with
  its reason.
- **The dated, frozen manifest**, with your **current claim-to-evidence table**
  frozen alongside it: every number, figure, and citation on your poster has its
  row.

Then audit the package against the **five package sins**: a **hard-coded path**
that exists only on your laptop, a **missing seed** that moves every run, a
**by-hand edit** no clean run reproduces, an **undocumented exclusion** with no
logged reason, and **stale or unversioned data** a reader cannot reobtain. Name
the sin you found and fixed.

### 2. Your own cold run, first

Before the exchange, run your package cold yourself: a fresh session, your
README only, after a real break. Record the environment, the date, every place
you stalled, and the documentation line you added for each. Label this record
honestly: **"solo proxy; external cold run pending."** **Author self-reproduction
is never independent verification**, because you carry the undocumented step in
your head.

### 3. The package exchange: your report on a colleague's package

On Wednesday, in class, you receive a colleague's package and run it from their
written instructions alone, while they run yours. Write a **cold-run report** for
them: whether the headline number and its uncertainty came back, every question
the run raised, and every instruction that was missing, ranked by how much each
threatens the result. Attach the report you wrote to your record. It is the
evidence that the exchange happened in both directions.

### 4. Your response to the report you received

Your colleague's report is your work order. For every item on it, record one of
two outcomes: **fixed**, naming the change and where it lives in the package, or
**logged**, with the reason it stays as it is. Nothing on the report is answered
with silence.

### 5. Gate 1 — the author self-reproduction log (blocking)

A dated log of a fresh-runtime, restart-and-run-all rerun of the repaired package
in which every number and every bound on your poster came back. Copy each poster
number next to the value the rerun produced, including its interval, and mark
each pair matched or not matched. Your poster is printed, so a number that does
not match is not hidden: name it, give its corrected value, and record the
correction in the README and the claim-to-evidence table.

### 6. Gate 2 — the release preflight (blocking)

A short table taken immediately before you freeze the package, with each row
marked clear, pending, or blocking:

- **Permissions.** Everything in the package is inside your permission
  determination, and nothing identifiable appears that should not.
- **Disclosure.** The package's README carries your AI-use disclosure, drafted
  from the full ledger: what you sent to tools and not only what they produced,
  and anything you did not verify.
- **Reproducibility.** The package is complete, and the numbers match the run in
  Gate 1.
- **Claim boundary.** The README's one-line finding stays inside the compass
  position your design licenses, and the uncertainty travels with it.

A pending row is a repair you name and finish. A **blocking gate** is a
pass-or-stop check that is not scored and cannot be averaged away by strong work
elsewhere: a submission without both gate records, or with a row still marked
blocking, is returned rather than graded.

### 7. The second clean run

Any change to the package makes the previous run's record stale: a number, the
data, the code, the environment record, or one line of the instructions. So after
your last edit, run the package once more in a fresh environment, following only
your written instructions. Record the date, the environment, and the result,
label it as an **author rerun**, and keep your colleague's run beside it as the
independent evidence.

### 8. AI Research Ledger rows

Every use of AI in building this package gets a row in your **AI Research
Ledger** (the eight fixed fields: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Drafting README sections, generating the environment record, and
listing the steps a stranger might stumble on are all delegable, and each needs a
row naming the run or check that tested the output against reality. An assistant
can generate documentation; only a cold human run can validate it.

**A missing ledger is not a minor lapse.** A missing AI Research Ledger entry
scores the *Craft, rails & AI Research Ledger* row **0**, and the submission is
**returned** for completion before it is graded.

### 9. Carry-forward of instructor review requests: the Instructor Request Record

<!-- d80-instructor-request-record -->
Open `lastname_m17.pdf` with an **Instructor Request Record**. Copy every request
numbered `IR-M17-##` from my reviews since M11 (the Brightspace feedback and the
mentoring emails that came with them), one row per request:

| Request ID | Exact request | Source | Your response | Where I can verify it |
|---|---|---|---|---|
| `IR-M17-01` | copy the request as I wrote it | the feedback or email it came from, dated | **Done:** what you changed. Or **Not adopted:** your scientific reason and the choice you made instead. | file, section, page, figure, table, or cell in this submission |

A request is **addressed** in one of two ways: you completed it and give the
exact place in this submission where I can verify the change; or you did not
adopt it and give a specific reason grounded in the evidence, the design, ethics
or permissions, or the project's feasibility, together with the choice you made
instead. A defended "no" counts as addressed even when I would have chosen
differently; the quality of the choice itself is judged by the rubric, once. A
missing row, a "done" with no locatable change, or "I disagree" with no reason
is unaddressed.

Only numbered `IR-M17-##` requests count; advice outside the numbered block is
advice. The same request repeated in Brightspace and in an email keeps one ID
and counts once. If I issued no numbered requests, write one line: **No numbered
instructor requests were issued for M17.** For an approved group, one record
travels with the shared artifact and names the member responsible for each
response; a request I marked individual is scored for that member only.

### 10. Your action plan's commitments for this milestone

<!-- action-plan-commitments -->
You hold a personal **research action plan**, written for your project and
reissued after every review, with a version number that tells you which one is
current. It is where this course's general instructions become the specific next
moves your project needs.

**This submission delivers what your current action plan commits you to for this
milestone.** Take the row for this milestone from your plan's
milestone-to-poster table, together with any decision the plan leaves open with a
closing date on or before this milestone, and deliver them here. Where a plan
commitment and a component above describe the same work, they are one deliverable
written twice: do it once.

This is the milestone where your action plan's reproducibility steps come due: the package that produces every number on your poster, run cold by you and by a colleague, repaired against their run, and rerun clean after your last change.

If a commitment has become wrong, say so in one line, with the reason and what you
are doing instead. A defended departure is a decision; a silent one is drift. If
your plan and this brief genuinely conflict, follow the brief and tell me, so the
plan gets corrected.

**How it is scored.** This is the rubric's *Carry-forward: your action plan's steps* row (10 points), scored for you individually. The plan that counts is the latest version I sent you at least 48 hours before the deadline, and a step that is also a numbered request is answered once, in your Instructor Request Record.

### 11. Dossier update line

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your repaired package with its dated manifest, your cold-run
records with their honest labels, the two gate records, and the second clean run.
Name the file or section where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Package** | Seeded notebook (`SEED = 464`) passing restart-and-run-all; data or its access recipe; environment record; README (asks / found / how to run); licence and permissions note; decision log; dated frozen manifest; claim-to-evidence table frozen with it |
| **Five sins** | Audited; the one found and fixed named |
| **Own cold run** | Clean environment, README only, after a real break; stalls and fixes logged; labeled **"solo proxy; external cold run pending"** |
| **Exchange** | The cold-run report you wrote on your colleague's package attached; every item on the report you received fixed or logged with its reason |
| **Gate 1 — author self-reproduction log** | Dated fresh-runtime rerun; every poster number and bound marked matched or not; any mismatch named, corrected, and recorded; blocking |
| **Gate 2 — release preflight** | Permissions, disclosure, reproducibility, claim boundary, each clear / pending / blocking; blocking |
| **Second clean run** | Dated after your last change; the headline number and its uncertainty reproduce; labeled as an author rerun |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague |
| **Dossier line** | Package, cold-run records, gate records, and second clean run located by file or section |
| **Studio work** | Package exchanged in Wednesday's class; repairs, gates, and the second clean run worked at the Friday studio |
| **Filenames** | `lastname_m17_package.zip` (or a shared link) and `lastname_m17.pdf` |
| **Location** | Brightspace → Assignments → M17 |
| **Instructor Request Record** | Opens `lastname_m17.pdf`; every `IR-M17-##` request copied and marked **Done** with an exact location or **Not adopted** with a specific scientific reason and the choice made instead; if none were issued, the record says so |
| **Action-plan commitments** | This milestone's row from your research action plan is delivered here, and any commitment you departed from is named in one line with its reason |

---

## Grading Rubric (100 points)

**What this rubric scores.** The book and the course together. Your book milestone's own checks are scored inside these rows: *complete and specific to your project* and *the milestone's own product* in **The package**; *a dated, numbered version with its reason* in **Craft, rails & AI Research Ledger**; *every judgment defended by you, not asserted by a tool* in **Verification and reproduction**; and *the four rails* (ethics and permissions, evidence, AI activity, uncertainty) across **Release preflight and honest labels**, **Verification and reproduction** and **Craft, rails & AI Research Ledger**. What the course adds is your carry-forward record: the **Carry-forward** row below scores your action plan's steps, and the adjustment after the table covers the numbered review requests.

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **The package** (20) | Every part present and usable by a stranger: README, seeded notebook, data or recipe, environment, licence and permissions, decision log, dated manifest, frozen claim table; the five sins audited with the found-and-fixed one named; complete and unmistakably about your project (18–20) | Complete; one part thin (14–17) | A part missing, or a README a stranger could not follow (8–13) | No usable package (0–7) |
| **Cold runs and the exchange** (20) | Your own cold run logged and honestly labeled; the report you wrote for your colleague is specific and threat-ranked; every item on the report you received is fixed or logged with its reason (18–20) | Complete; one report item answered thinly (14–17) | The exchange documented in one direction only, or items left unanswered (8–13) | No cold-run record or no exchange (0–7) |
| **Verification and reproduction** (25) | The headline number and its uncertainty rerun clean after your last change; Gate 1 matches every poster number and bound or names and corrects each mismatch; every verification method named; every judgment defended in your own reasoning, not a tool's (23–25) | Reproduces; one part thin (19–22) | The clean-run record predates a change to the package, or restart-and-run-all needs manual fixes (11–18) | The headline number does not rerun from the package (0–10) |
| **Release preflight and honest labels** (10) | Every preflight row dispositioned; the AI disclosure drafted from the full ledger; no author rerun presented as independent reproduction (9–10) | Complete; one row loosely argued (7–8) | A pending row left without its repair (4–6) | A proxy run sold as independent reproduction (0–3) |
| **Craft, rails & AI Research Ledger** (15) | On-format, on-time; the four rails carried; complete ledger; dossier line present; a dated, numbered version with a reason a reader could use (14–15) | Minor format lapses; ledger complete (11–13) | Missing pieces (6–10) | Missing AI Research Ledger (scored 0, submission returned) (0–5) |
| **Carry-forward: your action plan's steps** (10) | Every eligible step addressed in your record: done and located, or not adopted with your reason and the choice you made instead (10) | Most eligible steps addressed; the score is 10 × addressed ÷ eligible, rounded (5–9) | Fewer than half addressed; same formula (1–4) | No action-plan section in your record (0) |

*Carry-forward row:* this row is scored for you individually, even in an approved group. The eligible steps are the ones your action plan sets for this milestone, in the latest version I sent you at least 48 hours before the deadline; a step sent later moves to a later milestone. Leave out any step that is also a numbered request (`IR-M17-##`): it is answered in your Instructor Request Record and counted once, through the adjustment below. If no steps are eligible, name the plan version you checked and write "No eligible action-plan steps for M17"; that earns the full 10. This row scores your response; the quality of the research itself is scored in the rows above.

**Carry-forward adjustment (course decision D80; applies to this milestone score only).**
Let `U` be the number of numbered `IR-M17-##` requests left unaddressed in your
Instructor Request Record. After the rubric, its hard caps, and any late penalty
are applied:

`recorded M17 score = max(0, score − min(20, 5 × U))`

Five points per unaddressed request, capped at twenty. A completed and located
change is addressed; so is a reasoned decision not to adopt a request, with the
choice made instead. Where this milestone is revision-eligible, the deduction
follows the standing revision policy. A request can reduce this score only if
its numbered wording reached you at least 48 hours before the deadline.

**Hard caps (a single failure caps the row regardless of the rest):**

- A **non-reproducing result**, meaning the headline number does not rerun from
  your package, caps *Verification and reproduction* at Beginning.
- A **stale run record**, meaning the package changed after the run that vouches
  for it, is treated as a non-reproducing result until a fresh record is supplied.
- A **missing AI Research Ledger entry** scores *Craft, rails & AI Research
  Ledger* **0** and the submission is **returned** until it is supplied.

**Blocking gates are separate from the score.** A submission without both gate
records, or with a gate row still marked blocking, is returned rather than
graded. Neither gate can be averaged away by strong work elsewhere.

**Revision:** eligible under the standing policy. A revised submission within **7
days** of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies handled individually per Purdue policy).
- A headline number that does not rerun clean from your package: *Verification
  and reproduction* scores Beginning regardless of the rest. An honest "this part
  did not reproduce, and here is what broke" never triggers this; the cap is for
  the false pass.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.
- Numbered instructor review request left unaddressed in the Instructor Request
  Record: −5 points each, up to −20 on this milestone score (D80).

## Common Pitfalls

1. **The package that only runs on your machine.** A hard-coded path to your
   downloads folder, a file you uploaded by hand in a session that no longer
   exists, a step you always do without thinking. Each one is invisible to you and
   fatal to a stranger, which is exactly why the run has to be cold.
2. **The proxy sold as the real thing.** Rerunning your own package after lunch
   and writing "reproduced independently." Keep the label honest: solo proxy,
   external cold run pending, until your colleague's run exists.
3. **The stale run.** "It ran on Wednesday" offered for a package you edited on
   Friday. Any change makes that record a vouch for a package that no longer
   exists. Run it clean once more after your last edit.
4. **The invisible response.** You changed something because I asked, but the
   Instructor Request Record does not say where, or it says only "I disagree."
   Neither can be verified, so both count as unaddressed. Point to the exact
   place, or give the reason and the choice you made instead.

<!-- submission-pdf-howto:begin -->
## Making the PDF you hand in

Colab has no export-to-PDF button. You make the PDF by **printing the
notebook to a file**, which takes about a minute once you know the preparation
steps. Skipping them is the most common way a milestone arrives looking half
finished, because a notebook prints what is on the screen and nothing else.

### 1. Prepare the notebook

1. **Run the whole thing.** `Runtime` → `Run all`, then wait for it to finish.
   A cell you never ran prints with nothing underneath it, so an analysis you
   really did can reach the grader as an empty box.
2. **Expand every collapsed section.** Anything folded shut prints as a heading
   with nothing beneath it. Open all of them, including any Colab folded for you.
3. **Shorten any output that scrolls.** When Colab puts a scrollbar on an output,
   or tells you the output is truncated, only the visible part prints. Show the
   first twenty rows instead of the whole table, or summarise it, then rerun that
   cell. A reader did not want the whole table anyway.
4. **Read it once, top to bottom.** You are about to freeze it.

### 2. Print it to a file

`File` → `Print` opens your browser's print dialog. Set the destination to
**Save as PDF**, open the dialog's further settings, and turn on **Background
graphics**, so code cells keep their shading and your figures keep their
backgrounds. Save it under the file name this milestone asks for.

Wide tables and wide figures are the usual casualty. If something runs off the
right edge, switch the layout to **landscape** or reduce the scale, and print
again.

### 3. Check the PDF before you upload it

Open the file you just made and confirm three things: every figure is whole
rather than sliced by a page break, no output stops mid-line, and the pages run
in order with nothing missing. A PDF is an artifact like any other in this
course, so you verify it before your name goes on it.

### One route not to take

Ask an AI assistant how to export a Colab notebook and it will very likely hand
you `jupyter nbconvert --to pdf`. Do not spend your afternoon on it. Inside
Colab that route needs a large LaTeX installation, runs for several minutes, and
then either fails or quietly drops the symbols and emoji these notebooks are
full of. Printing to a file is the route that works.

That is a small, cheap instance of the rule this whole course runs on. The
confident answer is not automatically the correct one, and the way you find out
is to check it against what actually happens.
<!-- submission-pdf-howto:end -->

---

*Previous: [M16 — Conference Reflection](milestone_16_conference_reflection.md) —
your plan for the research after the Expo · This is the last milestone in the
chain.*
