# Distractor Rewrite Instructions — Removing the Answer-Length Cue

## Background

An audit (`scripts/audit_answer_length.py`) confirmed that across the 2026Summer
quiz banks and midterm case banks, the correct option is the strictly longest
option in 86–99.5% of questions (chance: 25%). Students can score ~100% by
always picking the longest option. Your job: rewrite the **incorrect** options
(distractors) in your assigned CSV file(s) so option length carries no signal,
while keeping every question pedagogically sound.

## File format (Brightspace D2L CSV — preserve EXACTLY)

Each question block looks like:

```
NewQuestion,MC,,,
Title,,,,
QuestionText,"<stem>",,,
Points,1,,,
Difficulty,1,,,
Option,100.00,"<correct option>",,
Option,0.00,"<distractor>",,
Option,0.00,"<distractor>",,
Option,0.00,"<distractor>",,
```

Rules:
- Keep every non-Option line byte-for-byte identical. Keep `QuestionText` lines untouched.
- Option lines must keep the form `Option,<weight>,"<text>",,` — text ALWAYS
  wrapped in double quotes, internal double quotes doubled (`""`), two trailing
  commas. Do not reorder options. Do not change weights. Keep the same number
  of options per question.
- Edit with Python (parse carefully, write lines manually in the format above)
  or with careful text edits. After writing, confirm the file still parses:
  same question count, exactly one 100.00 option per question.

## What to change

For EVERY question in your file(s):

1. **The correct option (weight 100.00):** keep its meaning and decision
   unchanged. If it is longer than ~280 characters, you MAY tighten the wording
   (compress, don't cut substance) — it must remain unambiguously the correct
   answer. Never add new claims to it.
2. **The three distractors (weight 0.00):** rewrite each one so that it is:
   - **Elaborated to comparable length.** Every option in the question
     (including the correct one) must be at least 60% of the length of that
     question's longest option. Aim for all four options within a similar
     visual band.
   - **Plausible but unambiguously wrong on content.** The wrongness must come
     from a real, specific misconception a student could hold (e.g., evaluating
     on training data, tuning on the test set, confusing precision with recall,
     treating correlation as causation, fitting the scaler before the split,
     using accuracy under class imbalance) — never from silly claims, absolute
     words ("always", "never") as a tell, or vague hand-waving. A student who
     mastered the material must still be able to eliminate it with confidence;
     a student who didn't must find it tempting.
   - **Stylistically identical to the correct option:** same voice, same level
     of technical detail, same sentence structure, and a similar density of
     connector/justification words (because, so that, which, rather than,
     therefore, while). Each distractor should carry its own (flawed) rationale,
     just like the correct option carries a sound one.
   - **Distinct:** the three distractors in one question must each embody a
     different misconception.
3. **Kill the length ranking signal:** across your whole file, the correct
   option must be the strictly longest option in **at most 40% of questions**
   (ideally ~25%, matching chance). In most questions, deliberately make one
   distractor the longest option. Also vary which position holds the longest
   option. The correct option should land at every length rank (longest,
   2nd, 3rd, shortest) across the file.
4. Do not change question order, stems, points, or difficulty. Do not add or
   remove questions.

## Domain grounding

- Quiz files (`_quizzes/2026Summer/quiz_nbNN_v*.csv`): questions reference the
  course notebooks (`notebooks/nbNN_*_student.ipynb`). Misconceptions should be
  ones plausible for that notebook's topic. You do not need to read the
  notebook unless an option's content is unclear.
- Midterm files (`_midterm_exam/2026Summer/midterm_<case>_*.csv`): each case
  has a blueprint `_midterm_exam/2026Summer/midterm_blueprint_<case>.md`
  describing the scenario, the correct managerial decisions, and the
  "manager-failure archetypes" used for distractors. Skim it first. Distractors
  must read as confident managerial decisions with flawed reasoning, consistent
  with the case facts (company name, cost ratios, class balance, etc.).
- Style conventions: `$` and `~` appear as plain characters in these CSVs (no
  escaping). Match existing punctuation style. No markdown inside options.

## Verification (MANDATORY before you finish)

Run, for each file you edited:

```
.venv/bin/python scripts/audit_answer_length.py --file <path>
```

It prints per-question lengths and ends with PASS or FAIL. You must get PASS:
- correct option strictly longest in ≤ 40% of questions, AND
- every option ≥ 60% of its question's longest option.

If FAIL, adjust lengths and re-run until PASS. Then report: file name(s),
questions touched, final correct-is-longest rate, and any question where you
tightened the correct option's wording.
