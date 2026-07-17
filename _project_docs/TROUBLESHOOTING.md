# Troubleshooting

Common issues encountered while developing or deploying course materials, with proven solutions.

---

## Issue: Quarto Render Fails

**Symptoms:** Error when running `quarto render`.

**Solutions:**
1. Check `_quarto.yml` syntax (YAML is whitespace-sensitive).
2. Verify all `.qmd` files have valid frontmatter.
3. Check for broken links in `.qmd` files.
4. Try rendering individual files first: `quarto render index.qmd`.
5. Confirm Quarto is installed at the expected path: `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto --version`.

---

## Issue: GitHub Pages Not Updating

**Symptoms:** Website shows old content after `git push`.

**Solutions:**
1. **Most common cause: forgot to render and commit `docs/`.** Run `quarto render`, then `git add docs/`, `git commit`, `git push`.
2. Wait 2–5 minutes (first deployment can take longer).
3. Check GitHub Actions: Repository → Actions tab.
4. Verify `docs/` directory exists and contains `index.html`.
5. Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows).
6. Check GitHub Pages settings: Settings → Pages → main branch, `/docs` folder.

---

## Issue: Notebook Won't Run in Colab

**Symptoms:** Errors when clicking "Open in Colab".

**Solutions:**
1. Check the Colab badge URL — must match the notebook filename exactly (including the `_student` suffix).
2. Verify all imports are standard libraries or first-cell `pip install`.
3. Test in a fresh Colab runtime: Runtime → Disconnect and delete runtime.
4. Check for hardcoded local file paths — use raw GitHub URLs instead.
5. If the notebook references `notebooks/figures/...`, confirm the figure exists in the repo at that path.

---

## Issue: Git Push Rejected

**Symptoms:** `! [rejected] main -> main (fetch first)`.

**Solutions:**
1. Pull first: `git pull origin main`.
2. Resolve any conflicts.
3. Push again: `git push origin main`.

---

## Issue: Missing Files After Clone

**Symptoms:** Expected files not present after `git clone`.

**Solutions:**
1. Check `.gitignore` — files may be excluded intentionally.
2. `_adm_stuff/`, instructor notebooks, `video_guides/`, and large files are excluded by design.
3. `docs/` should be present — if not, run `quarto render`.

---

## Issue: Instructor-Solution Cells Leaking to Student Notebook

**Symptoms:** Generated student notebook still shows solution code.

**Cause:** A solution cell did not contain the literal marker `INSTRUCTOR SOLUTION`.

**Solutions:**
1. Markdown solution headings must read: `### INSTRUCTOR SOLUTION — Exercise N`.
2. Code solution cells must start with `# INSTRUCTOR SOLUTION` as the first comment.
3. Hidden markdown solutions (e.g., "Reading the output") must start with `<!-- INSTRUCTOR SOLUTION -->` as the first line.
4. Student placeholder cells (`### YOUR FINDINGS HERE:`) must NOT contain `INSTRUCTOR SOLUTION`.
5. Re-run the strip step:
   ```bash
   cp notebooks/nbNN_topic_instructor.ipynb notebooks/nbNN_topic_student.ipynb
   # then strip cells matching INSTRUCTOR SOLUTION
   ```
6. Update the Colab badge in the student copy to point at `_student.ipynb`.

---

## Issue: Voice-Check Grep Returns Hits

**Symptoms:** `grep -iE '\bstudents?\b|\bthe instructor\b|on camera|speaking prompt' notebooks/nbNN_*_student.ipynb` returns lines.

**Cause:** Instructor-voice or third-party "students" language leaked into a student-facing cell.

**Solutions:**
1. Rewrite each hit in second person (`you`), neutral imperative (`print X`), or first person (`I want to see Y`).
2. False positives: `Student's t` (the test name) is the only acceptable match. Whitelist it manually.
3. For Gemini prompts: replace trailing `"so students see X"` with `"to show X"` or `"so the comparison is explicit"`.
4. Re-run the grep until clean before commit.

---

## Issue: CV-First Audit Returns Unexpected Hits

**Symptoms:** `python scripts/audit_cv_first.py` returns hits outside `nb14` cell 33 and `nb18` Kaggle-submission demo.

**Cause:** Model-evaluation code (e.g., `model.score(X_test, ...)`, `roc_auc_score(y_test, ...)`) snuck into nb09–nb20 evaluation logic.

**Solutions:**
1. Replace `.score(X_test, ...)` with `cross_val_score(model, X_train, y_train, cv=...)` and report mean ± 95% CI.
2. Replace `classification_report(y_test, model.predict(X_test))` with `classification_report(y_train, cross_val_predict(model, X_train, y_train, cv=...))`.
3. For permutation importance that needs a held-out sample: split `X_train` further (75/25 inside the cell) — never touch `X_test`.
4. For calibration: use `CalibratedClassifierCV(base, cv=5)` on `X_train`; evaluate Brier on `X_val`.
5. Re-run `python scripts/audit_cv_first.py` until only the nb14/nb18 exceptions remain.

---

## Issue: Dollar Signs Render as Math in Colab

**Symptoms:** A markdown cell mentioning `$50,000` shows broken LaTeX or eats subsequent text.

**Cause:** Unescaped `$` triggers MathJax in Colab's markdown renderer.

**Solution:** In markdown cells (NOT code cells), always escape: `\$50,000`, `\$100k`. Apply globally to any monetary expression.

---

## Issue: Colab Badge Points to Wrong File

**Symptoms:** Clicking the badge opens the instructor notebook (404) or the wrong topic.

**Cause:** Badge URL was not updated when the notebook was generated/renamed.

**Solution:** Edit the header markdown cell. Badge URL must be:
```
https://colab.research.google.com/github/davi-moreira/2026Summer_predictive_analytics_purdue_MGMT474/blob/main/notebooks/nbNN_topic_student.ipynb
```
The trailing filename must end in `_student.ipynb`, never `_instructor.ipynb`.
