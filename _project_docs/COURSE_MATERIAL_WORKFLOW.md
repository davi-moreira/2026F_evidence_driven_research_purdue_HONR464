# Course Material Production Workflow (per notebook)

The end-to-end pipeline for producing **one notebook's full set of course materials**: the Jupyter notebook, the recorded videos, the Brightspace page, the NotebookLM concept videos, and the quizzes. It generalizes the sequence used to build **NB19** and refined across NB01–NB18. Run it once per notebook (`nbNN`).

> This doc **sequences the whole pipeline**. The behavior-changing *quality gates* for each step (instructor-first editing, the voice check, the CV-first audit, render + commit) live in `CLAUDE.md` — this doc points to them, it does not restate them.

---

## Where each artifact lives (and what is public)

| Artifact | Path | Git |
|---|---|---|
| Instructor notebook (source of truth) | `notebooks/nbNN_*_instructor.ipynb` | ignored (local) |
| **Student notebook (the deliverable)** | `notebooks/nbNN_*_student.ipynb` | **tracked / public** |
| Video lecture guide | `video_guides/NN_video_lecture_guide.md` | ignored |
| Brightspace page | `brightspace/NN_*.md` | ignored |
| NotebookLM source + splits | `_notebook_lm/nbNN_*_instructor.md`, `…_vN.md` | ignored |
| Quiz blueprint + CSVs | `_quizzes/2026Summer/quiz_blueprint_nbNN.md`, `quiz_nbNN_vN.csv` | ignored |
| Recorded / edited videos | external (`*.mp4` are gitignored) | ignored |

Only the **student notebook** (plus the rendered `docs/`, `schedule.qmd`, and the planning docs) is public. Everything else is instructor-facing and local-only.

---

## The pipeline

### Phase A — Notebook (the source of truth)

**A1. Develop the notebook.** Edit `nbNN_*_instructor.ipynb` **first**, then generate the student copy (delete every `INSTRUCTOR SOLUTION` cell, fix the Colab badge). Apply the narrative-polish + voice rules, test in Colab (*Run all*), then run the voice-check grep and (nb09+) the CV-first audit, `quarto render`, and commit the **student** notebook + `docs/` and push.
*Gates: CLAUDE.md → Instructor-First Editing, Voice & Audience, CV-First, Commit + Render.*

The instructor notebook is the spine of every downstream artifact: the videos follow its sections, the Brightspace page summarizes them, the NotebookLM markdown is generated from it, and the quizzes are written from it.

### Phase B — Videos

**B1. Record the video lecture** — one segment per planned section range (a segment ≈ one "Video N").
**B2. Edit the videos.** The **edited videos are the source of truth for the final split**: their count and boundaries may differ from the original plan, and the Brightspace page, the NotebookLM splits, and the quizzes must all match the edited reality.

### Phase C — Brightspace page

**C1. Create the Brightspace page** (`brightspace/NN_*.md`) following the established pattern (the canonical pages 01–15; pick the closest analog by notebook type — content notebook vs. milestone walkthrough). The page's **Videos** section is where each segment's range is declared: `### Video N [Section X–Y]`, with two placeholders per segment when applicable (a **Topic AI Video** concept clip + a **Notebook Video** walkthrough).

**C2. Lock the video splits to the edited videos.** Set the page's video count and section ranges to match the **actual recorded/edited** videos (e.g., NB17 became 2 videos, not the planned 3). **This is the lock point** — every downstream artifact follows these ranges.

**C3. Generate per-video titles + descriptions.** Paste the developed notebook into an LLM (ChatGPT) and run the prompt below over a section range (fill in the boundary), then paste the result into the page's Video sections.

> **Prompt (verbatim — fill in the section boundary):**
> *"provide me a summary and description from the start to before Section 8 as if it was a video: a very short 2-3 sentence summary, a paragraph for course documentation + provide me a short title for each of the videos."*

Collect, per video: the **short title**, the **2–3 sentence summary**, and the **documentation paragraph**.

### Phase D — NotebookLM concept videos

**D1. Generate the NotebookLM source, then split it.** The full `_notebook_lm/nbNN_*_instructor.md` is produced automatically by the `PostToolUse` hook on any instructor-notebook edit (or run `bash scripts/sync_instructor_md.sh`). Then **split it into per-video files** (`…_vN.md`) whose ranges match the Brightspace **Videos** section locked in **C2**. Keep **both** the full file and the split files in `_notebook_lm/`. *(Done for NB19.)*

**D2. Generate the AI concept videos in NotebookLM** from the split files — one per segment. These become the **Topic AI Video** clips referenced on the Brightspace page.

### Phase E — Assessment

**E1. Generate the quizzes.** Follow `_quizzes/2026Summer/quiz_generation_plan.md`: first the per-notebook **blueprint** (`quiz_blueprint_nbNN.md`) covering all video splits, then the per-video **CSVs** (`quiz_nbNN_vN.csv`), byte-compatible with `_quizzes/2026Summer/sample_quiz.csv`. The blueprint is sourced from the **split video md files** (Phase D), so **E follows D**. *(Done for NB19.)*

**E2. Run the answer-length gate.** Before importing ANY quiz or exam CSV to Brightspace: `python scripts/audit_answer_length.py --file <csv>` must print PASS (no option-length cue to the correct answer — see the MC Option-Length Parity rule in `CLAUDE.md` and the spec in `scripts/_distractor_rewrite_instructions.md`). A bank that FAILs does not ship.

### Phase F — Sync the rest of the course

Once the notebook's materials are final, propagate the change:

- **Video guide** (`video_guides/NN_video_lecture_guide.md`) — keep cell refs, the section map, and the Suggested Video Structure in sync; run `python scripts/voice_check_guides.py`.
- **Schedule** (`schedule.qmd` **and** the syllabus `_syllabus/2026Summer/…_schedule.docx`) — set the day's **video count to the final segment count** (count "Video N" segments, not clips), then `quarto render` and commit `docs/`.
- **Planning docs** (`_project_docs/MGMT47400_Online4Week_Plan_2026Summer.md`, `_project_docs/claude_course_plan.md`) — update the sequencing rationale if sections, tools, or dependencies changed.

---

## Dependency order — what must precede what

```
A  notebook  ─►  B  record + edit videos  ─►  C2  LOCK the video splits (Brightspace Videos section)
                                                  │
                        ┌─────────────────────────┼─────────────────────────┐
                        ▼                         ▼                         ▼
                  C3 titles/desc            D1 notebook_lm split       (all wait on C2)
                                                  │
                                                  ▼
                                            D2 AI concept videos
                                                  │
                                                  ▼
                                            E  quizzes (from the splits)
                                                  │
                                                  ▼
                                  F  sync video guide + schedule + planning docs
```

**The lock point is C2.** The edited videos fix the split, and the Brightspace **Videos** ranges become the single source that both the NotebookLM splits (D) and the quiz blueprints (E) follow. **Do not start D or E until C2 is locked**, or the splits and quizzes will not line up with the videos.

---

## Who does what

| Step | Claude can do it | Manual (instructor) |
|---|---|---|
| A1 develop notebook | ✅ | review / Colab test |
| B1–B2 record + edit videos | — | ✅ |
| C1 create Brightspace page | ✅ | — |
| C2 lock splits to edited videos | ✅ (told the real counts) | confirm counts |
| C3 titles + descriptions | ✅ or ChatGPT | paste into page |
| D1 notebook_lm full + split | ✅ | — |
| D2 AI concept videos | — | ✅ (NotebookLM) |
| E1 quizzes | ✅ | import to Brightspace |
| F sync guide/schedule/planning | ✅ | — |

---

## Quality gates (apply at every relevant phase)

- Student-notebook **voice check** + **narrative polish** (CLAUDE.md). Zero non-`Student's t` hits.
- **CV-first audit** for nb09–nb20 (`scripts/audit_cv_first.py`).
- **Escape** `$`→`\$` and `~`→`\~` in all rendered markdown (notebooks, video guides, Brightspace pages, `.qmd`).
- **Render + commit `docs/` + push** after any `.qmd` / notebook / image change.
- Keep instructor-only artifacts (instructor notebook, `video_guides/`, `brightspace/`, `_notebook_lm/`, `_quizzes/`, `_production_kit/`) **out of git** — they are gitignored; only the student notebook ships.

---

*Last refined: 2026-06-04 — generalized from the NB19 production run.*
