> ⚠️ **SEEDED FROM MGMT474 — NOT YET ADAPTED FOR HONR 46400.**
> This template was carried over from the source Predictive-Analytics course and still
> describes machine-learning notebooks (`RANDOM_SEED`, 60/20/20 splits, ISLP bibliography,
> `nb01_eda_splits`). **Do not treat it as the canonical HONR 46400 activity template yet.**
> Adapt it during curriculum work — see `NEW_COURSE_SETUP.md` (gap list) and the
> "Adapt seeded `_project_docs`" task on the course board.

# Notebook Structure Template

> **Canonical reference:** `notebooks/nb01_eda_splits_student.ipynb` is the reference implementation. When creating or updating notebooks, match its header format, section organization, and conventions exactly. This file documents what nb01 demonstrates.

Every student notebook MUST include these sections in order.

---

## 1. Header Cell (Markdown)

```markdown
# [Topic Title]

<hr>

<center>
<div>
<img src="https://raw.githubusercontent.com/davi-moreira/2026Summer_predictive_analytics_purdue_MGMT474/main/notebooks/figures/mgmt_474_ai_logo_02-modified.png" width="200"/>
</div>
</center>

# <center><a class="tocSkip"></center>
# <center>QM47400 Predictive Analytics</center>
# <center>Professor: Davi Moreira </center>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/davi-moreira/2026Summer_predictive_analytics_purdue_MGMT474/blob/main/notebooks/XX_topic_student.ipynb)

---
```

**Important:** No "Day X:" prefix in titles. No date lines. Notebooks are self-paced and should not reference specific days or dates.

---

## 2. Learning Objectives (Markdown)

```markdown
## Learning Objectives

By the end of this notebook, you will be able to:

1. [Objective 1]
2. [Objective 2]
3. [Objective 3]
4. [Objective 4]
5. [Objective 5]

---
```

---

## 3. Setup Section (Code)

```python
# Standard imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import warnings

# Display settings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.precision', 3)
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# Set random seed for reproducibility
RANDOM_SEED = 474
np.random.seed(RANDOM_SEED)

print("✓ Setup complete!")
print(f"Random seed: {RANDOM_SEED}")
```

---

## 4. Content Sections (Numbered 1, 2, 3...)

- Clear section headers (`## 1. Title`, `## 2. Title`, etc.)
- Markdown explanation before each code cell
- Visualizations with clear labels
- Subsections as needed (`### 1.1`, `### 1.2`, etc.)

Apply the **Narrative Polish Pattern** (see `CLAUDE.md`):
- Open analytical sections with a "Why This Matters" cell anchored on a named stakeholder.
- Prefer narrative prose over bullet lists for "Reading the output" cells.
- Anticipate confusion with inline `"A question that often comes up here"` Q&A blocks.
- Bridge each section to the next with a one-sentence transition.

---

## 5. PAUSE-AND-DO Exercises (2 per notebook, ~10 min each)

### Text-only exercise (interpretation/analysis)

```markdown
## 📝 PAUSE-AND-DO Exercise X (10 minutes)

**Task:** [Clear, specific task]

---

### YOUR ANSWER HERE:

**[Question 1]:**
[Student response]

---
```

### Code exercise (students write code)

The code-exercise block has six cells in the **instructor** notebook. The student notebook strips cells 4–6.

1. Exercise prompt (markdown):
   ```markdown
   ## 📝 PAUSE-AND-DO Exercise X (10 minutes)

   **Task:** [Clear, specific task]

   ---
   ```

2. Gemini prompt (markdown):
   ```markdown
   > 💡 **Gemini Prompt:** "[Step-by-step instructions for Gemini]"
   >
   > **After running, verify:**
   > - [Expected output 1]
   > - [Expected output 2]
   ```

3. Student code cell (must NOT contain `INSTRUCTOR SOLUTION`):
   ```python
   # YOUR SOLUTION CODE HERE
   # Hint: Use the Gemini prompt above for step-by-step guidance
   ```

4. Solution heading (markdown, removed from student):
   ```markdown
   ### INSTRUCTOR SOLUTION — Exercise X
   ```

5. Solution code (code, removed from student):
   ```python
   # INSTRUCTOR SOLUTION
   # ... full solution ...
   ```

6. Reading-the-output (markdown, removed from student):
   ```markdown
   <!-- INSTRUCTOR SOLUTION -->
   ## Reading the Output
   [Narrative explanation of what the solution prints]
   ```

After the solution is stripped, the student notebook shows: prompt → Gemini guidance → empty student cell → student answer placeholder → bridge to next section.

---

## 6. Wrap-Up Section (Markdown)

```markdown
## N. Wrap-Up: Key Takeaways

### What We Learned Today:

1. [Key point 1]
2. [Key point 2]
3. [Key point 3]
4. [Key point 4]

### Remember:

> **"[Critical rule in blockquote]"**

[Closing paragraph that names the next notebook and what it builds on today's work. Often carries one final "A question that often comes up here" Q&A block.]

---
```

---

## 7. Bibliography (Markdown)

```markdown
## N+1. Bibliography

- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2023). *An Introduction to Statistical Learning with Python* (ISLP). Springer.
- [Other relevant citations]
- scikit-learn User Guide: [Relevant section](URL)

---
```

---

## 8. Thank You Cell (Markdown, final cell)

```markdown
<center>

Thank you!

</center>
```

---

## Naming Conventions

- **Student notebook:** `nbNN_topic_student.ipynb` (committed, rendered, published)
- **Instructor notebook:** `nbNN_topic_instructor.ipynb` (gitignored, local only)
- **Variables:** `lowercase_with_underscores`
- **Constants:** `UPPERCASE` (e.g., `RANDOM_SEED = 474`)
- **Emoji vocabulary:** `✓` success, `⚠️` warning, `📝` exercise, `💡` insight

## Style Guidelines (Load-Bearing Values)

| Setting | Value |
|---|---|
| Random seed | `RANDOM_SEED = 474` |
| Train/Val/Test split | 60/20/20 |
| Figure size | `plt.rcParams['figure.figsize'] = (10, 6)` |
| Display precision | `pd.set_option('display.precision', 3)` |
| Money in markdown | Always escape: `\$50,000` (unescaped `$` triggers LaTeX in Colab) |
