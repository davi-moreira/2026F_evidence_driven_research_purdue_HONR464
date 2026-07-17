#!/usr/bin/env python3
"""Audit Brightspace MC question banks for the 'longest answer is correct' cue.

Parses every quiz CSV (_quizzes/2026Summer) and midterm case CSV
(_midterm_exam/2026Summer) in the D2L NewQuestion/Option format, then tests:

  H0: the correct option's position in the length ranking is random
      (P(correct is strictly longest) = 1/4 with 4 options)
  H1: the correct option is the longest more often than chance

Tests reported per bank group:
  1. Exact one-sided binomial test on #(correct == strictly longest) vs p=1/4.
  2. Paired Wilcoxon signed-rank + paired t-test on
     len(correct) - mean(len(distractors)).
  3. (midterm only, secondary) same pair of tests on discourse-connector
     counts, matching the 'more elaboration/connectors' phrasing.

Usage: python scripts/audit_answer_length.py [--per-file]
"""
import csv
import glob
import re
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent

CONNECTORS = re.compile(
    r"\b(because|since|so that|therefore|thus|hence|which|while|whereas|"
    r"although|though|and|but|or|so|then|before|after|when|if|unless|"
    r"rather than|instead of|as well as|in order to|versus|plus)\b",
    re.IGNORECASE,
)


def parse_bank(path):
    """Return list of questions: dict(stem, options=[(weight, text), ...])."""
    questions = []
    cur = None
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row:
                continue
            tag = row[0].strip()
            if tag == "NewQuestion":
                cur = {"stem": "", "options": []}
                questions.append(cur)
            elif tag == "QuestionText" and cur is not None:
                cur["stem"] = row[1] if len(row) > 1 else ""
            elif tag == "Option" and cur is not None:
                weight = float(row[1])
                text = row[2] if len(row) > 2 else ""
                cur["options"].append((weight, text))
    return [q for q in questions if len(q["options"]) >= 2]


def measure(questions, metric):
    """Per question: (value_correct, mean_value_distractors, is_strict_max)."""
    rows = []
    for q in questions:
        correct = [t for w, t in q["options"] if w > 0]
        wrong = [t for w, t in q["options"] if w == 0]
        if len(correct) != 1 or not wrong:
            continue
        c = metric(correct[0])
        ds = [metric(t) for t in wrong]
        rows.append((c, float(np.mean(ds)), c > max(ds), len(q["options"])))
    return rows


def report(label, rows):
    n = len(rows)
    k = sum(r[2] for r in rows)
    # null prob correct is strictly longest, averaged over option counts
    p0 = float(np.mean([1.0 / r[3] for r in rows]))
    binom = stats.binomtest(k, n, p0, alternative="greater")
    diffs = np.array([r[0] - r[1] for r in rows])
    t = stats.ttest_1samp(diffs, 0.0, alternative="greater")
    try:
        w = stats.wilcoxon(diffs, alternative="greater")
        wp = w.pvalue
    except ValueError:
        wp = float("nan")
    print(f"\n=== {label} ===")
    print(f"  questions analyzed:            {n}")
    print(f"  correct option strictly max:   {k}  ({k/n:.1%}; chance = {p0:.1%})")
    print(f"  binomial test (one-sided):     p = {binom.pvalue:.3g}")
    print(f"  mean(correct) vs mean(distractor): {np.mean([r[0] for r in rows]):.1f} vs {np.mean([r[1] for r in rows]):.1f}")
    print(f"  mean paired difference:        {diffs.mean():+.1f} (sd {diffs.std(ddof=1):.1f})")
    print(f"  paired t-test (one-sided):     t = {t.statistic:.2f}, p = {t.pvalue:.3g}")
    print(f"  Wilcoxon signed-rank:          p = {wp:.3g}")
    return {"n": n, "k": k, "rate": k / n, "binom_p": binom.pvalue,
            "t_p": t.pvalue, "wilcoxon_p": wp, "mean_diff": diffs.mean()}


def check_file(path):
    """Per-question diagnostics for one bank. Exit 1 if the length cue remains.

    Gate: correct option is strictly longest in <= 40% of questions, AND no
    option in any question is shorter than 60% of that question's longest
    option (so length alone can't separate options).
    """
    qs = parse_bank(path)
    fails, longest_hits = [], 0
    for i, q in enumerate(qs, 1):
        lens = [len(t) for w, t in q["options"]]
        correct_len = max((len(t) for w, t in q["options"] if w > 0), default=0)
        mx = max(lens)
        is_max = correct_len == mx and lens.count(mx) == 1 and correct_len > 0
        longest_hits += is_max
        spread_ok = min(lens) >= 0.6 * mx
        flag = []
        if not spread_ok:
            flag.append(f"spread min={min(lens)} max={mx}")
            fails.append(i)
        print(f"  Q{i:>2}: lens={lens} correct={correct_len}"
              f" {'LONGEST' if is_max else '       '} {' '.join(flag)}")
    rate = longest_hits / len(qs) if qs else 0
    ok = rate <= 0.4 and not fails
    print(f"  -> correct-is-strictly-longest: {longest_hits}/{len(qs)} ({rate:.0%});"
          f" spread failures: {fails or 'none'}; {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


def main():
    per_file = "--per-file" in sys.argv
    if "--file" in sys.argv:
        check_file(sys.argv[sys.argv.index("--file") + 1])
        return
    chars = len
    conn = lambda t: len(CONNECTORS.findall(t))

    quiz_files = sorted(glob.glob(str(ROOT / "_quizzes/2026Summer/quiz_nb*_v*.csv")))
    mid_files = sorted(glob.glob(str(ROOT / "_midterm_exam/2026Summer/midterm_*_classification.csv"))) + \
        sorted(glob.glob(str(ROOT / "_midterm_exam/2026Summer/midterm_*_regression.csv")))

    def nb_num(p):
        return int(re.search(r"nb(\d+)", Path(p).name).group(1))

    early = [f for f in quiz_files if nb_num(f) <= 8]
    late = [f for f in quiz_files if nb_num(f) >= 9]

    groups = [
        ("QUIZZES nb09-nb19 (reported) — CHARACTERS", late, chars),
        ("QUIZZES nb01-nb08 (context) — CHARACTERS", early, chars),
        ("MIDTERM all 14 cases — CHARACTERS", mid_files, chars),
        ("MIDTERM all 14 cases — CONNECTOR WORDS", mid_files, conn),
    ]
    for label, files, metric in groups:
        rows = []
        for f in files:
            qrows = measure(parse_bank(f), metric)
            rows.extend(qrows)
            if per_file:
                k = sum(r[2] for r in qrows)
                print(f"    {Path(f).name}: {k}/{len(qrows)} correct-is-longest")
        if rows:
            report(label, rows)


if __name__ == "__main__":
    main()
