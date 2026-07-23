# The Student Research Lead Handbook

*Your guide to leading a class the way a researcher leads an investigation.*

---

## What a Student Research Lead is

For most Monday and Wednesday lectures this semester, one of you runs the room.
That person is the **Student Research Lead**, or **SRL** for short. You will be
the SRL five times.

Being the SRL is not giving a presentation. You are not there to summarize a
reading, walk through slides, or tell the class what the notebook says. You are
there to run a **Socratic investigation**: a class session built out of good
questions, where the room works out the ideas by thinking, committing, testing,
and arguing. "Socratic" just means you lead by asking, not by telling. The best
SRL sessions feel less like a lecture and more like a lab meeting where a sharp
question is on the table and everyone is trying to crack it.

Here is the difference in one line. A presenter stands at the front and transfers
what they know. An SRL stands at the front and makes the room think.

## The philosophy: AI is your arm, not your brain

This course runs on one idea:

> **AI is your arm and your research assistant. It is not your brain.**

An arm is powerful. It reaches, fetches, lifts, and drafts. But it does not
decide where to go. You do. When you lead, you model exactly that relationship
for the room. You make the class think first, commit to an answer, then use AI
on purpose, and then interrogate whatever it hands back. **Interrogate** here
means to question a claim hard before you trust it: ask where it came from,
whether it is true, and what it is quietly assuming.

Four habits sit under everything an SRL does:

1. **You make the room think.** The class does the reasoning. Your questions do
   the steering.
2. **You make the room commit.** Before anyone opens an AI tool, the class writes
   down what it believes. A **commitment** is a stated answer you put on record
   before you consult AI, so you can tell later whether the AI changed your mind
   or just agreed with you.
3. **You consult AI strategically.** You do not ask the AI to think for the room.
   You point it at a specific job, then bring the answer back for inspection.
4. **You interrogate what comes back.** No answer from an AI tool ends the
   discussion. A human decision ends the discussion.

The everyday shorthand for the whole loop is **Ask, Verify, Document**. Ask the
AI for something specific. Verify what it gives you against real evidence.
Document what you decided and why. You will run the room through that loop live.

## The two lead formats

Your slot is either a Monday or a Wednesday, and each has its own shape. Both
run 50 minutes. The minute frames below are fixed, and the instructor posts
checkpoint signals at the section boundaries so you always know your pace.

### Monday: the guided investigation

Monday is where a new idea gets built from a puzzle. The class starts from
curiosity, commits to a belief, investigates with AI as the research partner,
and lands on a decision it can defend.

| Minutes | Section | What you do |
|---|---|---|
| **0–9** | **Your research puzzle** | Open with one concrete puzzle. Elicit prior beliefs. Get the room to commit to an answer in writing before any AI is opened. |
| **9–31** | **Guided AI investigation** | You facilitate as the class uses Gemini as a research partner on the puzzle. You direct the prompts, run a human-versus-AI comparison, and probe what comes back. The instructor monitors for accuracy in the background. |
| **31–43** | **Human verification and formalization** | The instructor steps in to formalize the concept and lock down what is actually correct. You help connect it back to the class's committed answers. |
| **43–50** | **Decision and defense** | You close by making the room commit to a decision and defend it. The class records an AI Research Ledger line and a Claim Ticket. |

Your two big blocks are **0–9** (you own it completely) and **9–31** (you run
the investigation while the instructor watches accuracy). The **31–43**
formalization is the instructor's block; your job there is to hand off cleanly
and keep the thread visible.

### Wednesday: the applied AI laboratory

Wednesday is where the idea gets used under pressure. You open with a challenge,
the class works hands-on with AI, then defends the results against hard questions
and carries the skill into their own projects.

| Minutes | Section | What you do |
|---|---|---|
| **0–7** | **Your retrieval challenge** | Open with a challenge that forces recall and exposes a fault line. Good challenges: a common error, an ambiguous claim, a flawed AI output, a design conflict, or a result that needs interpreting. |
| **7–30** | **Applied AI laboratory** | You steer the room through hands-on work with AI. Everyone runs prompts, splits roles, and hunts for AI-failure patterns. This is the longest block, so pacing is on you. |
| **30–42** | **Peer defense** | The class defends its results while classmates ask adversarial questions. **Adversarial** here means friendly but relentless: questions designed to find the weak point, not to attack the person. |
| **42–50** | **Transfer to projects** | You close by connecting the skill to each person's own research project. The class records an AI Research Ledger line and a Claim Ticket. |

Your owned blocks are **0–7** and **7–30**. The **30–42** peer defense you
referee; you keep the questions coming and the answers honest.

## The seat rotation

There are 25 lead slots across the semester, and five of you, so **each person
leads five times**. Slots are assigned by rotation seat, labeled **A** through
**E**. The rotation starts at the first led lecture and cycles A, B, C, D, E,
A, B, C, and so on.

| Your seat | Your five slots |
|---|---|
| A | slots 1, 6, 11, 16, 21 |
| B | slots 2, 7, 12, 17, 22 |
| C | slots 3, 8, 13, 18, 23 |
| D | slots 4, 9, 14, 19, 24 |
| E | slots 5, 10, 15, 20, 25 |

Which calendar meeting each slot lands on, and whether it is a Monday or a
Wednesday format, lives on the **Schedule page of the course website**. Check it
early so you know your dates and your format well in advance. This handbook
never prints dates on purpose, so it never goes stale. The Schedule page is the
single source of truth for when your slot is.

## Your preparation timeline

Good SRL sessions are built, not improvised. Here is the rhythm.

### Five days before your lead

- You receive the **instructor notebook's SRL page** for your slot. It names the
  concept in play, the compass position or design in focus, and a seed puzzle
  you can use or adapt. It also flags the one thing the class most needs to leave
  understanding.
- Read the week's notebook and the matching chapter yourself, as a learner. You
  cannot lead an investigation into an idea you have not sat with.
- Pick your puzzle. Use the seed, sharpen it, or bring your own. A puzzle works
  when it has a real answer, more than one tempting wrong answer, and can be
  stated in a few sentences.
- Rough out your three Socratic questions and the moment you will have the room
  commit before touching AI.

### Two days before your lead

- Submit your **preparation template** (`srl_prep_template.md`). This is your
  script: the puzzle, the commitment question, three Socratic questions with the
  answers you expect (right and wrong), the exact Gemini prompt or prompts the
  class will run, what you expect the AI to get right and wrong, your
  assumption-probe, your counterexample request, the decision you will make the
  room defend, a timing plan, and a fallback if the AI tool is down.
- The instructor reviews it and sends notes. Treat those notes seriously; they
  are the difference between a session that lands and one that stalls.

### The day of your lead

- Arrive a few minutes early. Open Colab, confirm Gemini responds, and paste your
  first prompt into a scratch cell so it is ready.
- Load your puzzle where the room can see it.
- Have your fallback ready in case the AI tool is slow or down. A dead tool
  should never kill your session.
- Breathe. You are not performing. You are hosting a good argument.

## The ten SRL moves

These are the moves that turn a session from a talk into an investigation. You
will not use all ten every time. Learn them, then reach for the ones your puzzle
needs.

1. **Introduce a concrete puzzle.** Start with something specific and real, not a
   definition. "Here are two studies that disagree about one arrow in a diagram"
   beats "Today we will discuss confounding."
2. **Ask before you define.** When a term comes up, ask the room what they think
   it means before you or the AI supplies the definition. Their guesses tell you
   where the confusion lives.
3. **Elicit prior beliefs.** Get answers on the record before any evidence
   arrives. "Hands up, who thinks the effect is positive?" A **prior belief** is
   what someone expects to be true before they look, and surfacing it makes
   learning visible.
4. **Require commitment before AI.** Have everyone write down their answer before
   the AI is opened. This is the single most important move. Without it, the AI's
   answer becomes everyone's answer and no one learns anything.
5. **Direct strategic AI use.** Point Gemini at one specific job with a prompt you
   chose in advance. Never let the room type "explain this topic" and read the
   result aloud. That is outsourcing the thinking.
6. **Compare human versus AI answers.** Put the room's committed answer next to
   the AI's answer, side by side. Where they agree, ask why. Where they differ,
   ask who is right and how you would know.
7. **Probe assumptions.** For any claim, human or AI, ask what has to be true for
   it to hold. An **assumption** is a condition a claim quietly depends on. Naming
   it is often the whole lesson.
8. **Demand counterexamples and evidence.** Ask for a case where the claim would
   fail, and ask what evidence would settle it. A claim with no possible
   counterexample and no supporting evidence is not yet a finding.
9. **Call out unjustified AI confidence.** When the AI sounds certain, ask the
   room to check whether the certainty is earned. Confident tone is not
   evidence. This is a graded habit, not a nicety.
10. **Close by making the room defend a decision.** End on a human decision, and
    make someone defend it out loud against a hard question. The session is not
    over when the AI answers. It is over when a person commits and holds up.

## When an answer is wrong or uncertain

Someone will give a wrong answer. The AI will give a wrong answer. You will not
always know the right one in the moment. All three are normal, and all three are
useful.

- **Treat every wrong answer as data, never as failure.** A wrong answer tells
  the room exactly which assumption to examine. Say "interesting, walk me
  through how you got there," not "no, that's wrong." You are studying the
  reasoning, not scoring it.
- **Never humiliate.** A room that fears looking foolish stops talking, and a
  silent room cannot be led. Protect the person, examine the idea.
- **When you are genuinely unsure, say so and turn it into an investigation.**
  "I don't know either. How could we find out?" is a strong SRL move, not a weak
  one. Uncertainty is the raw material of research.
- **When the AI is uncertain or hedges, notice it out loud.** Missing certainty
  is one of the AI-failure patterns you are hunting. Do not let a vague answer
  pass as a settled one.

## How the instructor will step in

You are not alone at the front. The instructor is monitoring, especially during
the Monday investigation block, and will step in on purpose. Expect it, and do
not read it as a rescue.

- If a **conceptual error starts spreading**, the instructor flags it without
  taking the room from you. You keep leading; the error gets corrected.
- If the **room goes quiet**, the instructor may seed a cold-call to restart the
  flow. Pick the thread back up.
- If the **AI produces a failure you miss**, the instructor will often ask you to
  ask the room about it, rather than answering directly. Follow that thread.
- The instructor owns the **Monday 31–43 formalization block**, where the correct
  version of the concept gets locked in.

The full details are in the instructor intervention protocol, which you do not
need to read. You just need to know that stepping in is part of the design, and
it keeps your session accurate.

## Logistics, in one place

- You lead **five times** across the semester, on the dates listed for your seat
  on the **Schedule page**.
- You receive the **instructor notebook's SRL page** for your slot **five days
  ahead**.
- You submit your **preparation template two days ahead**; the instructor sends
  notes.
- Each session ends with the class recording an **AI Research Ledger** line and a
  **Claim Ticket**, the two records that travel with every session in this
  course.
- Your leading is graded on the **SRL rubric** (`srl_rubric.md`). Read it before
  your first slot so you know what strong leading looks like.
- Classmates give you quick feedback after each session on the **peer feedback
  form** (`srl_peer_feedback_form.md`). Read it. It is the fastest way to get
  better before your next slot.

---

*You are going to be nervous the first time. Every researcher is nervous the
first time they run a room. The fix is not to know every answer. The fix is to
ask better questions than anyone expected, and to make the room glad it had to
think. Go make them think.*
