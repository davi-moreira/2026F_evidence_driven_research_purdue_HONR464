#!/usr/bin/env python3
"""build_book_sim_figures.py — the book's seeded simulation figures (D26).

EDR|AI chapters embed seeded simulations that show a concept visually; the
chapter shows the code AND the figure, and the companion notebook lets the
reader rerun the code live. Because the book renders without executing code,
this script generates the figures offline, deterministically (SEED = 464),
with axis labels localized per edition, into:

    book/images/sims/       book-pt/images/sims/       book-es/images/sims/

The code block printed in each chapter is the same simulation as here; if you
change a simulation, change BOTH (the chapter block and this script) and rerun:

    .venv/bin/python scripts/build_book_sim_figures.py

Current figures: ch11 random-vs-convenience sampling, ch14 overfitting (train
vs holdout error), ch15 the randomization distribution of a difference in
means, ch15 treatment-dependent attrition (the complete-case contrast is not
the effect for everyone enrolled — the D35 Batch-A counterexample), and ch22 the
null reference spread (a valid null never prints 0.00 — Batch C).

D83 adds the five further-route figures (EN only; their labels live in
L["book"] and are read through _sim_label, so the frozen PT/ES editions fall
back to English rather than fail): natural experiments (event-study leads and
a regression discontinuity), survey experiments (list experiment vs a direct
question; conjoint AMCEs), audit studies (the name gap as cases grow; naive vs
clustered intervals), text as data (chance-corrected agreement; correcting an
AI labeler's prevalence), and evidence synthesis (a forest plot of the
published studies; a funnel plot of every study run).
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parent.parent
SEED = 464
BLUE, ORANGE, INK = "#2a78d6", "#eb6834", "#333333"
GREY = "#9a9a9a"  # D83: the evidence-synthesis funnel plot

L = {
    "book": {
        "random": "Random samples\n(n = 500)",
        "convenience": "Convenience\nchannel (n = 500)",
        "truth_age": "true mean = {v:.1f}",
        "xlabel_age": "Sample mean age (years)",
        "train": "Training error",
        "test": "Selection error",
        "final_pt": "Final holdout",
        "chosen": "chosen on selection",
        "xlabel_gap": "Final error minus the winning selection error",
        "ylabel_worlds": "Simulated worlds",
        "gapstat": "mean optimism = {mean:+.3f} RMSE (median {med:+.3f})\nworse than its crowning score in {p:.0f}% of worlds",
        "overflow": "{n} worlds beyond +{hi:.1f} (largest {mx:+.2f})",
        "xlabel_gap2": "True error of the winner minus its winning selection score",
        "xlabel_deg": "Model flexibility (polynomial degree)",
        "ylabel_rmse": "Prediction error (RMSE)",
        "best": "chosen on selection",
        "truth_ate": "true effect = {v:.1f} pp",
        "mean_est": "mean of estimates = {v:.1f} pp",
        "xlabel_ate": "Estimated effect of the reminder (percentage points)",
        "ylabel_n": "Number of re-randomizations",
        "cc_truth": "true effect for everyone enrolled = {v:.1f} pp",
        "cc_mean": "complete-case contrast = {v:.1f} pp",
        "cc_retention": "still measured at the end:\n{t:.0f}% of the reminder arm, {c:.0f}% of the control arm",
        "xlabel_cc": "Complete-case contrast (percentage points)",
        "null_truth": "true vehicle effect = 0",
        "null_one": "one experiment = {v:+.2f} mm",
        "null_band": "middle 95% of null readings:\n{lo:+.2f} to {hi:+.2f} mm",
        "xlabel_null": "Measured vehicle effect on zone diameter (mm)",
        "ylabel_exp": "Number of simulated experiments",
        # D83 further research routes (EN only; PT/ES fall back through _sim_label)
        "ne_parallel": "parallel trends hold",
        "ne_violated": "treated state already sliding",
        "ne_truth": "dashed line: true effect = {v:.1f}",
        "ne_xlabel_es": "Quarters relative to the wage raise",
        "ne_ylabel_es": "Workers per restaurant,\nA minus B, vs quarter -1",
        "ne_title_es": "Event study: the leads are the check",
        "ne_xlabel_rd": "Application score (grant at 70 and above)",
        "ne_ylabel_rd": "Jobs one year later",
        "ne_title_rd": "Regression discontinuity at the cutoff",
        "ne_jump": "estimated jump = {v:.2f}\n(95% interval {lo:.2f} to {hi:.2f})",
        "ne_binned": "binned means",
        "se_list": "list experiment",
        "se_direct": "direct question",
        "se_truth": "true prevalence = {v:.0f}%",
        "se_xlabel_n": "Respondents",
        "se_ylabel_prev": "Estimated prevalence (%)",
        "se_title_left": "A sensitive behaviour, two ways to ask",
        "se_title_right": "A conjoint of job offers",
        "se_xlabel_amce": "AMCE (percentage points)",
        "se_lvl_sal10": "Salary +10%",
        "se_lvl_sal20": "Salary +20%",
        "se_lvl_rem2": "Remote 2 days",
        "se_lvl_rem5": "Remote 5 days",
        "se_lvl_ai": "AI tools allowed",
        "aud_truth": "true gap = {v:.0f} points",
        "aud_xlabel_left": "Résumé templates in the audit (one run per name)",
        "aud_ylabel_left": "Name gap in advance rate (points)",
        "aud_title_left": "More cases, narrower interval",
        "aud_naive": "naive\n(1,000 outputs as cases)",
        "aud_cluster": "clustered\n(10 templates as cases)",
        "aud_cover": "covers the truth in\n{p:.0f}% of 1,000 reruns",
        "aud_xlabel_right": "Name gap in advance rate (points)",
        "aud_title_right": "Same 1,000 outputs, two intervals",
        "tad_pair_careful": "Two careful coders",
        "tad_pair_lazy": "Careful coder vs one\nwho marks almost nothing",
        "tad_observed": "Observed agreement",
        "tad_chance": "Agreement expected by chance",
        "tad_kappa": "Cohen's kappa",
        "tad_ylabel_agree": "Proportion (kappa on the same scale)",
        "tad_title_left": "Same 200 releases, two coder pairs",
        "tad_ai_only": "AI labels alone\n(all 6,000)",
        "tad_human_only": "Human-coded subset\nalone (300)",
        "tad_corrected": "AI labels corrected\nwith the subset",
        "tad_truth": "true share = {v:.1f}%",
        "tad_cover": "{v:.0f}% of 1,000 reruns cover the truth",
        "tad_xlabel_share": "Share of releases that claim credit (%), with 95% interval",
        "tad_title_right": "Estimating the share in 6,000 releases",
        "es_forest_title": "What the published record shows",
        "es_funnel_title": "Every study that was run",
        "es_study": "study {i}",
        "es_pooled_pub": "pooled, published only",
        "es_truth": "true average = {v:.1f}",
        "es_xlabel": "Effect on support (percentage points)",
        "es_ylabel_se": "Standard error (smaller = larger study)",
        "es_published": "published ({n})",
        "es_unpublished": "never published ({n})",
        "es_sigline": "significance line",
        "es_line_pub": "pooled, published: {v:.2f}",
        "es_line_all": "pooled, all run: {v:.2f}",
    },
    "book-pt": {
        "random": "Amostras aleatórias\n(n = 500)",
        "convenience": "Canal de\nconveniência (n = 500)",
        "truth_age": "média verdadeira = {v:.1f}",
        "xlabel_age": "Idade média da amostra (anos)",
        "train": "Erro de treino",
        "test": "Erro de seleção",
        "final_pt": "Holdout final",
        "chosen": "escolhido na seleção",
        "xlabel_gap": "Erro final menos o erro de seleção vencedor",
        "ylabel_worlds": "Mundos simulados",
        "gapstat": "otimismo médio = {mean:+.3f} RMSE (mediana {med:+.3f})\npior que a nota da coroação em {p:.0f}% dos mundos",
        "overflow": "{n} mundos além de +{hi:.1f} (maior {mx:+.2f})",
        "xlabel_gap2": "Erro verdadeiro do vencedor menos a sua nota de seleção",
        "xlabel_deg": "Flexibilidade do modelo (grau do polinômio)",
        "ylabel_rmse": "Erro de predição (RMSE)",
        "best": "escolhido na seleção",
        "truth_ate": "efeito verdadeiro = {v:.1f} pp",
        "mean_est": "média das estimativas = {v:.1f} pp",
        "xlabel_ate": "Efeito estimado do lembrete (pontos percentuais)",
        "ylabel_n": "Número de re-sorteios",
        "cc_truth": "efeito verdadeiro para todos os inscritos = {v:.1f} pp",
        "cc_mean": "contraste de casos completos = {v:.1f} pp",
        "cc_retention": "ainda medidos ao final:\n{t:.0f}% do braço com lembrete, {c:.0f}% do braço de controle",
        "xlabel_cc": "Contraste de casos completos (pontos percentuais)",
        "null_truth": "efeito verdadeiro do veículo = 0",
        "null_one": "um experimento = {v:+.2f} mm",
        "null_band": "95% central das leituras nulas:\n{lo:+.2f} a {hi:+.2f} mm",
        "xlabel_null": "Efeito medido do veículo no diâmetro do halo (mm)",
        "ylabel_exp": "Número de experimentos simulados",
    },
    "book-es": {
        "random": "Muestras aleatorias\n(n = 500)",
        "convenience": "Canal por\nconveniencia (n = 500)",
        "truth_age": "media verdadera = {v:.1f}",
        "xlabel_age": "Edad media de la muestra (años)",
        "train": "Error de entrenamiento",
        "test": "Error de selección",
        "final_pt": "Holdout final",
        "chosen": "elegido en la selección",
        "xlabel_gap": "Error final menos el error de selección ganador",
        "ylabel_worlds": "Mundos simulados",
        "gapstat": "optimismo medio = {mean:+.3f} RMSE (mediana {med:+.3f})\npeor que su nota de selección en {p:.0f}% de los mundos",
        "overflow": "{n} mundos más allá de +{hi:.1f} (el mayor {mx:+.2f})",
        "xlabel_gap2": "Error verdadero del ganador menos su nota de selección",
        "xlabel_deg": "Flexibilidad del modelo (grado del polinomio)",
        "ylabel_rmse": "Error de predicción (RMSE)",
        "best": "elegido en la selección",
        "truth_ate": "efecto verdadero = {v:.1f} pp",
        "mean_est": "media de las estimaciones = {v:.1f} pp",
        "xlabel_ate": "Efecto estimado del recordatorio (puntos porcentuales)",
        "ylabel_n": "Número de reasignaciones",
        "cc_truth": "efecto verdadero para todos los inscritos = {v:.1f} pp",
        "cc_mean": "contraste de casos completos = {v:.1f} pp",
        "cc_retention": "aún medidos al final:\n{t:.0f}% del brazo con recordatorio, {c:.0f}% del brazo de control",
        "xlabel_cc": "Contraste de casos completos (puntos porcentuales)",
        "null_truth": "efecto verdadero del vehículo = 0",
        "null_one": "un experimento = {v:+.2f} mm",
        "null_band": "95% central de las lecturas nulas:\n{lo:+.2f} a {hi:+.2f} mm",
        "xlabel_null": "Efecto medido del vehículo en el diámetro del halo (mm)",
        "ylabel_exp": "Número de experimentos simulados",
    },
}


def clean(ax) -> None:
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(left=False)
    ax.grid(axis="x", color="#e5e5e5", lw=.6)
    ax.set_axisbelow(True)


def fig_ch11(s: dict, out: Path) -> dict:
    rng = np.random.default_rng(SEED)
    population = np.clip(rng.normal(49, 17, size=100_000), 18, 90)
    truth = population.mean()
    random_means = [rng.choice(population, 500, replace=False).mean()
                    for _ in range(10)]
    weights = np.exp(-(population - 25) ** 2 / (2 * 12 ** 2))
    convenience = rng.choice(population, 500, replace=False,
                             p=weights / weights.sum())

    fig, ax = plt.subplots(figsize=(7.6, 2.9))
    ax.scatter(random_means, np.ones(10), s=60, color=BLUE, zorder=3)
    ax.scatter([convenience.mean()], [0], s=60, color=ORANGE, zorder=3)
    ax.axvline(truth, color=INK, ls="--", lw=1.2)
    ax.text(truth + .5, 1.55, s["truth_age"].format(v=truth), color=INK,
            fontsize=9)
    ax.set_yticks([0, 1], [s["convenience"], s["random"]], fontsize=9)
    ax.set_xlabel(s["xlabel_age"])
    ax.set_ylim(-.7, 1.9)
    clean(ax)
    fig.tight_layout()
    fig.savefig(out / "ch11_sampling_channels.png", dpi=150)
    plt.close(fig)
    return {"truth": truth, "conv_mean": convenience.mean(),
            "rand_spread": (min(random_means), max(random_means))}


def fig_ch14(s: dict, out: Path) -> dict:
    """Overfitting AND model-selection bias, with three honest data roles.

    Left: training error falls forever while selection error turns up; the
    degree is chosen on the SELECTION set, and only that one choice is scored
    on the locked final holdout. Right: model-selection bias measured as an
    EXPECTATION — in each of 500 fresh worlds the winner's true error (a
    10,000-point independent sample standing in for the truth) is compared
    with the selection score that crowned it. Mean, median, share-worse, and
    the tail are all reported; nothing is clipped without an overflow mark.

    Each panel restarts its own generator from SEED, so the code blocks
    printed in the chapter reproduce these numbers exactly (D26 sync rule).
    """
    degrees = np.arange(1, 13)

    def world(rng, n):
        x = rng.uniform(-3, 3, n)
        return x, np.sin(1.5 * x) + rng.normal(0, .35, n)

    def rmse(coefs, data):
        x, y = data
        return np.sqrt(np.mean((np.polyval(coefs, x) - y) ** 2))

    # --- left panel: one world, the three roles ------------------------
    rng = np.random.default_rng(SEED)
    training, selection, final = (world(rng, 40) for _ in range(3))
    fits = [np.polyfit(training[0], training[1], d) for d in degrees]
    train_err = np.array([rmse(c, training) for c in fits])
    sel_err = np.array([rmse(c, selection) for c in fits])
    chosen = int(np.argmin(sel_err))
    final_err = rmse(fits[chosen], final)

    # --- right panel: optimism in expectation, own fresh stream --------
    rng = np.random.default_rng(SEED)
    gaps = []
    for _ in range(500):
        tr, sel, big = world(rng, 40), world(rng, 40), world(rng, 10_000)
        f = [np.polyfit(tr[0], tr[1], d) for d in degrees]
        se = np.array([rmse(c, sel) for c in f])
        pick = int(np.argmin(se))
        gaps.append(rmse(f[pick], big) - se[pick])
    gaps = np.asarray(gaps)

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.5))
    ax = axes[0]
    ax.plot(degrees, train_err, color=BLUE, lw=2, marker="o", ms=4)
    ax.plot(degrees, sel_err, color=ORANGE, lw=2, marker="o", ms=4)
    ax.axvline(degrees[chosen], color=INK, ls=":", lw=1)
    ax.scatter([degrees[chosen]], [final_err], color=INK, marker="D", s=46,
               zorder=4)
    ax.text(degrees[-1], train_err[-1], "  " + s["train"], color=BLUE,
            fontsize=8, va="center")
    ax.text(degrees[-1], sel_err[-1], "  " + s["test"], color=ORANGE,
            fontsize=8, va="center")
    ax.text(degrees[chosen] + .25, final_err, "  " + s["final_pt"], color=INK,
            fontsize=8, va="center")
    ax.text(degrees[chosen] + .1, max(sel_err) * .97, s["chosen"], color=INK,
            fontsize=8)
    ax.set_xlabel(s["xlabel_deg"])
    ax.set_ylabel(s["ylabel_rmse"])
    ax.set_xlim(degrees[0], degrees[-1] + 4.6)

    ax = axes[1]
    lo, hi = -0.15, 0.3
    inside = gaps[(gaps >= lo) & (gaps <= hi)]
    n_over = int((gaps > hi).sum())
    ax.hist(inside, bins=27, range=(lo, hi), color=BLUE,
            edgecolor="white", lw=.4)
    ax.axvline(0, color=INK, lw=1)
    ax.axvline(gaps.mean(), color=ORANGE, ls="--", lw=1.5)
    ax.text(.03, .93, s["gapstat"].format(mean=gaps.mean(),
                                          med=np.median(gaps),
                                          p=100 * (gaps > 0).mean()),
            color=ORANGE, fontsize=8, va="top", transform=ax.transAxes)
    ax.annotate(s["overflow"].format(n=n_over, hi=hi, mx=gaps.max()),
                xy=(hi, 0), xytext=(.55, .55), textcoords="axes fraction",
                fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=.8))
    ax.set_xlabel(s["xlabel_gap2"])
    ax.set_ylabel(s["ylabel_worlds"])
    ax.set_xlim(lo, hi)

    for ax in axes:
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.grid(axis="y", color="#e5e5e5", lw=.6)
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / "ch14_overfitting.png", dpi=150)
    plt.close(fig)
    return {"chosen": int(degrees[chosen]), "sel_at_chosen": sel_err[chosen],
            "final_at_chosen": final_err, "mean_gap": gaps.mean(),
            "median_gap": float(np.median(gaps)),
            "pct_worse": 100 * (gaps > 0).mean(),
            "n_overflow": n_over, "max_gap": gaps.max(),
            # design constants, exported so the numbers gate can bind every
            # component the prose states (round-5 G-C)
            "n_worlds": 500, "noise": .35, "overflow_hi": hi}


def fig_ch15(s: dict, out: Path) -> dict:
    rng = np.random.default_rng(SEED)
    n, tau = 200, 5.0                      # true effect: +5 percentage points
    y0 = np.clip(rng.normal(70, 12, n), 20, 95)   # refill rate w/o reminder
    y1 = y0 + tau                                 # exactly +5 for every patient
    estimates = []
    for _ in range(2000):
        treated = rng.permutation(n) < n // 2
        estimates.append(y1[treated].mean() - y0[~treated].mean())
    estimates = np.array(estimates)

    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    ax.hist(estimates, bins=40, color=BLUE, edgecolor="white", lw=.4)
    ax.axvline(tau, color=INK, ls="--", lw=1.2)
    ax.text(.02, .92, s["truth_ate"].format(v=tau), color=INK, fontsize=9,
            transform=ax.transAxes)
    ax.text(.02, .82, s["mean_est"].format(v=estimates.mean()), color=BLUE,
            fontsize=9, transform=ax.transAxes)
    ax.set_xlabel(s["xlabel_ate"])
    ax.set_ylabel(s["ylabel_n"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5", lw=.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / "ch15_randomization.png", dpi=150)
    plt.close(fig)
    return {"mean_est": estimates.mean(), "sd_est": estimates.std(),
            "lo": np.percentile(estimates, 2.5),
            "hi": np.percentile(estimates, 97.5)}


def fig_ch15_attrition(s: dict, out: Path) -> dict:
    """Treatment-dependent attrition: the complete-case contrast is not the ATE.

    Random assignment stays honest; deleting outcomes afterward is what breaks
    the comparison. The reminder keeps only the healthier patients measurable,
    so the observed gap runs far above the true effect for everyone enrolled.
    """
    rng = np.random.default_rng(SEED)
    N, reps, tau = 2000, 2000, 5.0
    health = rng.normal(size=N)
    y0 = 60 + 10 * health + rng.normal(0, 5, size=N)   # refill rate, no reminder
    y1 = y0 + tau                                      # ... with the reminder
    r0 = health > -0.8         # who is still measurable under control
    r1 = health > -0.2         # ... under the reminder: the sickest drop out
    ate = float(np.mean(y1 - y0))

    contrasts = []
    for _ in range(reps):
        z = rng.permutation(N) < N // 2
        y = np.where(z, y1, y0)
        retained = np.where(z, r1, r0)
        contrasts.append(y[z & retained].mean() - y[(~z) & retained].mean())
    contrasts = np.asarray(contrasts)

    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    ax.hist(contrasts, bins=40, color=ORANGE, edgecolor="white", lw=.4)
    ax.axvline(ate, color=INK, ls="--", lw=1.2)
    ax.text(.02, .92, s["cc_truth"].format(v=ate), color=INK, fontsize=9,
            transform=ax.transAxes)
    ax.text(.02, .82, s["cc_mean"].format(v=contrasts.mean()), color=ORANGE,
            fontsize=9, transform=ax.transAxes)
    ax.text(.02, .58, s["cc_retention"].format(t=100 * r1.mean(),
                                               c=100 * r0.mean()),
            color="#777777", fontsize=8, transform=ax.transAxes)
    ax.set_xlabel(s["xlabel_cc"])
    ax.set_ylabel(s["ylabel_n"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5", lw=.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / "ch15_attrition.png", dpi=150)
    plt.close(fig)
    return {"ate": ate, "cc_mean": contrasts.mean(),
            "retention_t": r1.mean(), "retention_c": r0.mean()}


def fig_ch22(s: dict, out: Path) -> dict:
    """A valid null returns a spread of small readings, not a row of zeros.

    2,000 vehicle-versus-blank experiments in a world where the vehicle truly
    does nothing. The readings scatter around zero (exact unrounded zero is
    uncommon for a continuous estimator, though dozens round to 0.00 at two
    decimals). The histogram is an illustration of null variation, never a
    pass/fail band.
    """
    rng = np.random.default_rng(SEED)
    reps, pairs = 2000, 12
    plate = rng.normal(0, 0.4, size=(reps, pairs))       # shared plate effect
    blank = 6.3 + plate + rng.normal(0, .35, size=(reps, pairs))
    vehicle = 6.3 + plate + rng.normal(0, .35, size=(reps, pairs))
    nulls = (vehicle - blank).mean(axis=1)               # true effect: exactly 0
    lo, hi = np.percentile(nulls, [2.5, 97.5])
    observed = nulls[0]

    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    ax.hist(nulls, bins=40, color=BLUE, edgecolor="white", lw=.4)
    ax.axvline(0, color=INK, ls="--", lw=1.2)
    ax.axvline(observed, color=ORANGE, lw=2)
    ax.text(.02, .92, s["null_truth"], color=INK, fontsize=9,
            transform=ax.transAxes)
    ax.text(.02, .82, s["null_one"].format(v=observed), color=ORANGE,
            fontsize=9, transform=ax.transAxes)
    ax.text(.02, .64, s["null_band"].format(lo=lo, hi=hi), color="#777777",
            fontsize=8, va="top", transform=ax.transAxes)
    ax.set_xlabel(s["xlabel_null"])
    ax.set_ylabel(s["ylabel_exp"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5", lw=.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / "ch22_null_spread.png", dpi=150)
    plt.close(fig)
    return {"mean": nulls.mean(), "sd": nulls.std(), "lo": lo, "hi": hi,
            "first": observed, "exact_zeros": int((nulls == 0).sum()),
            "rounded_zeros": int((nulls.round(2) == 0).sum()),
            "obs_min": float(nulls.min()), "obs_max": float(nulls.max()),
            # design constants for the numbers gate (round-5 G-C)
            "reps": reps, "pairs": pairs}


# D83: the further-route figures read their labels through this helper, so an
# edition without the new keys (the frozen PT/ES books) falls back to English
# instead of raising KeyError.
def _sim_label(s: dict, key: str) -> str:
    return s.get(key, L["book"][key])


def fig_natural_experiments(s: dict, out: Path) -> dict:
    rng = np.random.default_rng(SEED)

    # ---- left: event study, 200 restaurants per state, quarters -4..3 ----
    n, quarters, tau = 200, np.arange(-4, 4), -1.0

    def event_study(extra_trend):
        base = rng.normal(20, 4, size=(2 * n, 1))           # each restaurant's level
        shock = rng.normal(0, 0.5, size=quarters.size)        # swings both states share
        treated = np.repeat([True, False], n)[:, None]        # first 200 are State A
        y = (base + shock + extra_trend * quarters * treated
             + tau * treated * (quarters >= 0)
             + rng.normal(0, 1.5, size=(2 * n, quarters.size)))
        d = y - y[:, [3]]                                     # change since quarter -1
        est = d[:n].mean(0) - d[n:].mean(0)
        se = np.sqrt(d[:n].var(0, ddof=1) / n + d[n:].var(0, ddof=1) / n)
        change = y[:, 4:].mean(1) - y[:, :4].mean(1)          # after avg minus before avg
        did = change[:n].mean() - change[n:].mean()
        did_se = np.sqrt(change[:n].var(ddof=1) / n + change[n:].var(ddof=1) / n)
        return est, se, did, did_se

    par, par_se, did_par, did_par_se = event_study(0.0)
    slide = -0.4                          # State A already losing 0.4 workers/quarter
    vio, vio_se, did_vio, did_vio_se = event_study(slide)

    # ---- right: regression discontinuity, grant at score >= 70 ----
    m, cut, jump = 2000, 70, 1.5
    score = rng.uniform(40, 100, m)
    x = score - cut
    noise = rng.normal(0, 2.0, m)                          # same draw as before
    jobs = 5 + 0.08 * x + 0.0008 * x**2 + jump * (x >= 0) + noise
    # Stress test (printed, not plotted): the same applicants and noise, but an
    # S-shaped curve that climbs fastest near 70 and levels off at both ends.
    bent = 5 + 3 * np.tanh(x / 12) + jump * (x >= 0) + noise

    def rd(h, y=jobs):
        fits = []
        for side in (x < 0, x >= 0):
            k = side & (np.abs(x) <= h)
            X = np.column_stack([np.ones(k.sum()), x[k]])
            b = np.linalg.lstsq(X, y[k], rcond=None)[0]
            resid = y[k] - X @ b
            cov = resid @ resid / (k.sum() - 2) * np.linalg.inv(X.T @ X)
            fits.append((b, np.sqrt(cov[0, 0])))
        (b0, s0), (b1, s1) = fits
        return b1[0] - b0[0], np.hypot(s0, s1), b0, b1

    rd_res = {h: rd(h) for h in (5, 10, 20)}
    rd_bent = {h: rd(h, bent) for h in (5, 10, 20)}
    below = int(((x >= -5) & (x < 0)).sum())
    above = int(((x >= 0) & (x < 5)).sum())

    # ---- figure ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 3.8))
    ax1.axhline(0, color="#bbbbbb", lw=.8)
    ax1.axvline(-0.5, color="#bbbbbb", ls=":", lw=1)
    ax1.plot([-0.5, 3.4], [tau, tau], color=INK, ls="--", lw=1.1)
    ax1.text(.98, .92, _sim_label(s, "ne_truth").format(v=tau), color=INK,
             fontsize=8, ha="right", transform=ax1.transAxes)
    ax1.errorbar(quarters - .12, par, yerr=1.96 * par_se, fmt="o", color=BLUE,
                 ms=4, capsize=2, lw=1, label=_sim_label(s, "ne_parallel"))
    ax1.errorbar(quarters + .12, vio, yerr=1.96 * vio_se, fmt="s", color=ORANGE,
                 ms=4, capsize=2, lw=1, label=_sim_label(s, "ne_violated"))
    ax1.set_xticks(quarters)
    ax1.set_xlabel(_sim_label(s, "ne_xlabel_es"))
    ax1.set_ylabel(_sim_label(s, "ne_ylabel_es"))
    ax1.set_title(_sim_label(s, "ne_title_es"), fontsize=10, loc="left")
    ax1.legend(fontsize=8, frameon=False, loc="lower left")

    edges = np.arange(40, 100.01, 2.5)
    mids = (edges[:-1] + edges[1:]) / 2
    idx = np.digitize(score, edges) - 1
    means = np.array([jobs[idx == i].mean() for i in range(mids.size)])
    ax2.scatter(mids, means, s=14, color="#777777", label=_sim_label(s, "ne_binned"),
                zorder=3)
    est10, se10, b0, b1 = rd_res[10]
    xl, xr = np.linspace(-10, 0, 20), np.linspace(0, 10, 20)
    ax2.plot(cut + xl, b0[0] + b0[1] * xl, color=BLUE, lw=2)
    ax2.plot(cut + xr, b1[0] + b1[1] * xr, color=BLUE, lw=2)
    ax2.axvline(cut, color=INK, ls="--", lw=1)
    ax2.text(.03, .80, _sim_label(s, "ne_jump").format(v=est10, lo=est10 - 1.96 * se10,
                                                 hi=est10 + 1.96 * se10),
             color=BLUE, fontsize=8, transform=ax2.transAxes)
    ax2.set_xlabel(_sim_label(s, "ne_xlabel_rd"))
    ax2.set_ylabel(_sim_label(s, "ne_ylabel_rd"))
    ax2.set_title(_sim_label(s, "ne_title_rd"), fontsize=10, loc="left")
    ax2.legend(fontsize=8, frameon=False, loc="lower right")
    for ax in (ax1, ax2):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.grid(axis="y", color="#e5e5e5", lw=.6)
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / "natural_experiments.png", dpi=150)
    plt.close(fig)

    stats = {"tau": tau, "jump": jump, "n_per_state": n, "n_applicants": m,
             "did_par": did_par, "did_vio": did_vio,
             "did_par_hw": 1.96 * did_par_se, "did_vio_hw": 1.96 * did_vio_se,
             "did_par_lo": did_par - 1.96 * did_par_se,
             "did_par_hi": did_par + 1.96 * did_par_se,
             "did_vio_lo": did_vio - 1.96 * did_vio_se,
             "did_vio_hi": did_vio + 1.96 * did_vio_se,
             "pre_slide": abs(slide),
             "below": below, "above": above,
             "density_z": (above - below) / np.sqrt(below + above),
             "density_z_abs": abs(above - below) / np.sqrt(below + above)}
    for q, i in zip(quarters, range(quarters.size)):
        tag = f"m{-q}" if q < 0 else f"p{q}"
        stats[f"par_{tag}"] = par[i]
        stats[f"vio_{tag}"] = vio[i]
        stats[f"par_hw_{tag}"] = 1.96 * par_se[i]
        stats[f"vio_hw_{tag}"] = 1.96 * vio_se[i]
    for h, (e, se, _, _) in rd_res.items():
        stats[f"rd{h}"] = e
        stats[f"rd{h}_lo"] = e - 1.96 * se
        stats[f"rd{h}_hi"] = e + 1.96 * se
    for h, (e, se, _, _) in rd_bent.items():
        stats[f"rdb{h}"] = e
        stats[f"rdb{h}_lo"] = e - 1.96 * se
        stats[f"rdb{h}_hi"] = e + 1.96 * se
    return {k: float(v) for k, v in stats.items()}


SE_SIZES = [300, 600, 1200, 2400, 4800]


def fig_survey_experiments(s: dict, out: Path) -> dict:
    """List experiment vs direct question (left); conjoint AMCEs (right)."""
    lab = lambda k: _sim_label(s, k)  # noqa: E731
    rng = np.random.default_rng(SEED)

    # LEFT -----------------------------------------------------------------
    truth, admit = 0.20, 0.45
    control_p = np.array([0.5, 0.3, 0.6, 0.2])
    rows = []
    for n in SE_SIZES:
        trait = rng.random(n) < truth
        listed = rng.permutation(n) < n // 2
        count = (rng.random((n, 4)) < control_p).sum(axis=1) + (listed & trait)
        lst = count[listed].mean() - count[~listed].mean()
        lst_se = np.sqrt(count[listed].var(ddof=1) / listed.sum()
                         + count[~listed].var(ddof=1) / (~listed).sum())
        said_yes = trait & (rng.random(n) < admit)
        d = said_yes.mean()
        rows.append((n, lst, lst_se, d, np.sqrt(d * (1 - d) / n)))

    # RIGHT ----------------------------------------------------------------
    R, T = 800, 5
    salary = rng.integers(0, 3, (R, T, 2))
    remote = rng.integers(0, 3, (R, T, 2))
    ai_ok = rng.integers(0, 2, (R, T, 2))
    util = (np.array([0, .35, .90])[salary] + np.array([0, .30, .55])[remote]
            + .15 * ai_ok + rng.logistic(0, 1, (R, T, 2)))
    chosen = (util == util.max(axis=2, keepdims=True)).astype(float)
    levels = [("sal10", "se_lvl_sal10", salary, 1),
              ("sal20", "se_lvl_sal20", salary, 2),
              ("rem2", "se_lvl_rem2", remote, 1),
              ("rem5", "se_lvl_rem5", remote, 2),
              ("ai", "se_lvl_ai", ai_ok, 1)]

    def amces(ix):
        return [chosen[ix][a[ix] == k].mean() - chosen[ix][a[ix] == 0].mean()
                for _, _, a, k in levels]

    est = np.array(amces(np.arange(R)))
    boot = np.array([amces(rng.integers(0, R, R)) for _ in range(300)])
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)

    # FIGURE ---------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.4))
    x = np.arange(len(SE_SIZES))
    ax1.errorbar(x - .1, [r[1] * 100 for r in rows],
                 [1.96 * r[2] * 100 for r in rows], fmt="o", color=BLUE,
                 label=lab("se_list"))
    ax1.errorbar(x + .1, [r[3] * 100 for r in rows],
                 [1.96 * r[4] * 100 for r in rows], fmt="s", color=ORANGE,
                 label=lab("se_direct"))
    ax1.axhline(truth * 100, color=INK, ls="--", lw=1)
    ax1.set_ylim(-20, 50)
    ax1.text(.03, .04, lab("se_truth").format(v=truth * 100), color=INK,
             fontsize=8, transform=ax1.transAxes)
    ax1.set_xticks(x, [str(n) for n in SE_SIZES])
    ax1.set_xlabel(lab("se_xlabel_n"))
    ax1.set_ylabel(lab("se_ylabel_prev"))
    ax1.set_title(lab("se_title_left"), fontsize=9)
    ax1.legend(fontsize=8, frameon=False, loc="upper right")
    y = np.arange(len(levels))[::-1]
    ax2.errorbar(est * 100, y, xerr=[(est - lo) * 100, (hi - est) * 100],
                 fmt="o", color=BLUE)
    ax2.axvline(0, color=INK, lw=.8)
    ax2.set_yticks(y, [lab(k) for _, k, _, _ in levels])
    ax2.set_xlabel(lab("se_xlabel_amce"))
    ax2.set_title(lab("se_title_right"), fontsize=9)
    for ax in (ax1, ax2):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.set_axisbelow(True)
    ax1.grid(axis="y", color="#e5e5e5", lw=.6)
    ax2.grid(axis="x", color="#e5e5e5", lw=.6)
    fig.tight_layout()
    fig.savefig(out / "survey_experiments.png", dpi=150)
    plt.close(fig)

    stats: dict = {"truth": truth * 100, "admit": admit * 100,
                   "n_resp_conjoint": R, "n_tasks": T, "n_boot": 300}
    for n, l, lse, d, dse in rows:
        stats[f"list_{n}"] = l * 100
        stats[f"list_hw_{n}"] = 1.96 * lse * 100
        stats[f"direct_{n}"] = d * 100
        stats[f"direct_hw_{n}"] = 1.96 * dse * 100
    for (key, _, _, _), e, a, b in zip(levels, est, lo, hi):
        stats[f"amce_{key}"] = e * 100
        stats[f"amce_{key}_lo"] = a * 100
        stats[f"amce_{key}_hi"] = b * 100
    stats["hw_ratio_1200"] = stats["list_hw_1200"] / stats["direct_hw_1200"]
    return stats


def fig_audit_studies(s: dict, out: Path) -> dict:
    """Audit-study precision: growing samples, and false precision from
    treating repeated model outputs as independent cases."""
    lbl = lambda k: _sim_label(s, k)  # noqa: E731
    rng = np.random.default_rng(SEED)
    TRUE_GAP = 0.06                          # mean of U(-0.24, 0.36)

    def templates(n):
        base = rng.uniform(0.40, 0.60, n)        # advance rate, name A
        gap = rng.uniform(-0.24, 0.36, n)        # this template's name gap
        return base, base - gap                  # rates for name A, name B

    # Left: one run per name per template, audits of growing size.
    sizes = [10, 20, 40, 80, 160, 320]
    est, lo, hi = [], [], []
    for n in sizes:
        pa, pb = templates(n)
        d = (rng.random(n) < pa).astype(float) - (rng.random(n) < pb)
        se = d.std(ddof=1) / np.sqrt(n)
        est.append(d.mean()); lo.append(d.mean() - 1.96 * se)
        hi.append(d.mean() + 1.96 * se)
    est, lo, hi = (100 * np.array(v) for v in (est, lo, hi))

    # Right: 10 templates x 50 repeated runs per name, rerun 1,000 times.
    J, K, reps = 10, 50, 1000
    T_9 = 2.262                              # t critical value, 9 df, 95%
    cover_naive = cover_clust = 0
    first = None
    for r in range(reps):
        pa, pb = templates(J)
        ya = rng.random((J, K)) < pa[:, None]
        yb = rng.random((J, K)) < pb[:, None]
        gap = ya.mean() - yb.mean()
        se_naive = np.sqrt(ya.mean() * (1 - ya.mean()) / (J * K)
                           + yb.mean() * (1 - yb.mean()) / (J * K))
        dj = ya.mean(axis=1) - yb.mean(axis=1)   # one gap per template
        se_clust = dj.std(ddof=1) / np.sqrt(J)
        cover_naive += abs(gap - TRUE_GAP) <= 1.96 * se_naive
        cover_clust += abs(gap - TRUE_GAP) <= T_9 * se_clust
        if r == 0:
            first = (gap, se_naive, se_clust)
    gap0, sn0, sc0 = first
    naive_ci = (100 * (gap0 - 1.96 * sn0), 100 * (gap0 + 1.96 * sn0))
    clust_ci = (100 * (gap0 - T_9 * sc0), 100 * (gap0 + T_9 * sc0))
    pct_naive = 100 * cover_naive / reps
    pct_clust = 100 * cover_clust / reps

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.6))
    x = np.arange(len(sizes))
    a1.errorbar(x, est, yerr=[est - lo, hi - est], fmt="o", color=BLUE,
                ecolor=BLUE, capsize=3, lw=1.4)
    a1.axhline(100 * TRUE_GAP, color=INK, ls="--", lw=1.1)
    a1.axhline(0, color="#999999", lw=.8)
    a1.text(.98, .05, lbl("aud_truth").format(v=100 * TRUE_GAP), color=INK,
            fontsize=9, ha="right", transform=a1.transAxes)
    a1.set_xticks(x, [str(n) for n in sizes])
    a1.set_xlabel(lbl("aud_xlabel_left"))
    a1.set_ylabel(lbl("aud_ylabel_left"))
    a1.set_title(lbl("aud_title_left"), fontsize=10, color=INK, loc="left")

    rows = [(clust_ci, 100 * gap0, BLUE, lbl("aud_cluster"), pct_clust),
            (naive_ci, 100 * gap0, ORANGE, lbl("aud_naive"), pct_naive)]
    for yv, (ci, g, col, lab, pct) in enumerate(rows):
        a2.plot(ci, [yv, yv], color=col, lw=3, solid_capstyle="butt")
        a2.plot([g], [yv], "o", color=col)
        a2.text(ci[1] + 0.6, yv, lbl("aud_cover").format(p=pct), color=col,
                fontsize=8, va="center")
    a2.axvline(100 * TRUE_GAP, color=INK, ls="--", lw=1.1)
    a2.axvline(0, color="#999999", lw=.8)
    a2.set_yticks([0, 1], [rows[0][3], rows[1][3]], fontsize=8)
    a2.set_ylim(-0.7, 1.7)
    a2.set_xlim(min(clust_ci[0], naive_ci[0]) - 2, max(clust_ci[1], naive_ci[1]) + 14)
    a2.set_xlabel(lbl("aud_xlabel_right"))
    a2.set_title(lbl("aud_title_right"), fontsize=10, color=INK, loc="left")
    for ax in (a1, a2):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "audit_studies.png", dpi=150)
    plt.close(fig)

    res = {"true_gap": 100 * TRUE_GAP, "n_small": sizes[0], "n_large": sizes[-1],
           "est_small": est[0], "lo_small": lo[0], "hi_small": hi[0],
           "est_large": est[-1], "lo_large": lo[-1], "hi_large": hi[-1],
           "gap_first": 100 * gap0,
           "naive_lo": naive_ci[0], "naive_hi": naive_ci[1],
           "clust_lo": clust_ci[0], "clust_hi": clust_ci[1],
           "width_ratio": sc0 * T_9 / (sn0 * 1.96),
           "pct_naive": pct_naive, "pct_clust": pct_clust,
           "n_templates": J, "n_repeats": K, "n_outputs": 2 * J * K,
           "n_reruns": reps}
    for n, e, l_, h in zip(sizes, est, lo, hi):
        res[f"est_{n}"], res[f"lo_{n}"], res[f"hi_{n}"] = e, l_, h
    return res


def fig_text_as_data(s: dict, out: Path) -> dict:
    """Chance-corrected agreement, and correcting an AI labeler's prevalence."""
    lbl = lambda k: _sim_label(s, k)  # noqa: E731
    rng = np.random.default_rng(SEED)

    # ---- the chapter block, verbatim in logic and RNG order ----
    # Left: 200 releases coded by two people. True credit-claiming share 15%.
    n_pair = 200
    truth_pair = rng.random(n_pair) < 0.15
    coder_a = np.where(rng.random(n_pair) < 0.95, truth_pair, ~truth_pair)
    coder_b = np.where(rng.random(n_pair) < 0.95, truth_pair, ~truth_pair)
    coder_lazy = rng.random(n_pair) < 0.02      # marks almost nothing

    def agreement(a, b):
        observed = np.mean(a == b)
        chance = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
        return observed, chance, (observed - chance) / (1 - chance)

    careful = agreement(coder_a, coder_b)
    lazy = agreement(coder_a, coder_lazy)

    # Right: 6,000 releases, 20% claim credit. The AI labeler catches 75% of
    # the credit claims and wrongly flags 3% of the rest.
    N, n_gold = 6000, 300
    truth = rng.random(N) < 0.20
    true_share = truth.mean()

    fpc = 1 - n_gold / N                       # the subset is 5% of a fixed corpus

    def run_once():
        ai = np.where(truth, rng.random(N) < 0.75, rng.random(N) < 0.03)
        gold = rng.permutation(N)[:n_gold]     # random subset a human codes
        p_ai = ai.mean()                       # AI share on every release
        se_ai = np.sqrt(p_ai * (1 - p_ai) / N)  # naive: labels taken as truth
        p_h = truth[gold].mean()
        se_h = np.sqrt(fpc * truth[gold].var(ddof=1) / n_gold)
        diff = truth[gold].astype(float) - ai[gold]  # human minus AI, per release
        p_c = p_ai + diff.mean()               # AI share + average gap
        se_c = np.sqrt(fpc * diff.var(ddof=1) / n_gold)
        return (p_ai, se_ai), (p_h, se_h), (p_c, se_c)

    first = run_once()
    covers = np.zeros((1000, 3), dtype=bool)
    for r in range(1000):
        for j, (p, se) in enumerate(run_once()):
            covers[r, j] = abs(p - true_share) <= 1.96 * se
    cover_pct = covers.mean(axis=0) * 100
    # ---- end of the chapter block ----

    fig, (axl, axr) = plt.subplots(1, 2, figsize=(10.4, 3.6),
                                   gridspec_kw={"width_ratios": [1, 1.25]})
    x = np.arange(2)
    w = 0.26
    obs = [careful[0], lazy[0]]
    chn = [careful[1], lazy[1]]
    kap = [careful[2], lazy[2]]
    axl.bar(x - w, obs, w, color=BLUE, label=lbl("tad_observed"))
    axl.bar(x, chn, w, color="#9bbfe9", label=lbl("tad_chance"))
    axl.bar(x + w, kap, w, color=ORANGE, label=lbl("tad_kappa"))
    for xi, vals in zip(x, zip(obs, chn, kap)):
        for off, v in zip((-w, 0, w), vals):
            axl.text(xi + off, max(v, 0) + .02, f"{v:.2f}", ha="center",
                     fontsize=8, color=INK)
    axl.set_xticks(x, [lbl("tad_pair_careful"), lbl("tad_pair_lazy")], fontsize=8.5)
    axl.set_ylim(min(0, min(kap)) - .05, 1.22)
    axl.axhline(0, color=INK, lw=.6)
    axl.set_ylabel(lbl("tad_ylabel_agree"), fontsize=8.5)
    axl.set_title(lbl("tad_title_left"), fontsize=9.5, color=INK)
    axl.legend(fontsize=7.5, frameon=False, loc="upper right",
               bbox_to_anchor=(1.0, 1.0), ncol=1)

    names = [lbl("tad_ai_only"), lbl("tad_human_only"), lbl("tad_corrected")]
    cols = [ORANGE, "#777777", BLUE]
    ys = [2, 1, 0]
    for y, (p, se), c, cp in zip(ys, first, cols, cover_pct):
        axr.errorbar(100 * p, y, xerr=100 * 1.96 * se, fmt="o", color=c,
                     ms=6, capsize=3, lw=1.6)
        axr.text(max(100 * (p + 1.96 * se), 100 * true_share) + .4, y + .12,
                 lbl("tad_cover").format(v=cp), fontsize=7.5, color=c)
    axr.axvline(100 * true_share, color=INK, ls="--", lw=1.2)
    axr.text(100 * true_share + .3, 2.55, lbl("tad_truth").format(v=100 * true_share),
             fontsize=8.5, color=INK)
    axr.set_yticks(ys, names, fontsize=8.5)
    axr.set_ylim(-.6, 2.9)
    axr.set_xlim(11, 28)
    axr.set_xlabel(lbl("tad_xlabel_share"), fontsize=8.5)
    axr.set_title(lbl("tad_title_right"), fontsize=9.5, color=INK)
    for ax in (axl, axr):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "text_as_data.png", dpi=150)
    plt.close(fig)

    (p_ai, se_ai), (p_h, se_h), (p_c, se_c) = first
    return {
        "careful_observed": careful[0], "careful_chance": careful[1],
        "careful_kappa": careful[2],
        "lazy_observed": lazy[0], "lazy_chance": lazy[1], "lazy_kappa": lazy[2],
        "true_share": 100 * true_share,
        "ai_share": 100 * p_ai, "ai_lo": 100 * (p_ai - 1.96 * se_ai),
        "ai_hi": 100 * (p_ai + 1.96 * se_ai),
        "human_share": 100 * p_h, "human_lo": 100 * (p_h - 1.96 * se_h),
        "human_hi": 100 * (p_h + 1.96 * se_h),
        "corrected_share": 100 * p_c, "corrected_lo": 100 * (p_c - 1.96 * se_c),
        "corrected_hi": 100 * (p_c + 1.96 * se_c),
        "cover_ai": cover_pct[0], "cover_human": cover_pct[1],
        "cover_corrected": cover_pct[2],
        "n_pair": n_pair, "n_corpus": N, "n_gold": n_gold, "reruns": 1000,
    }


def _t975(df: int) -> float:
    """97.5th percentile of Student's t with df degrees of freedom (numpy only)."""
    c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)
    x = np.linspace(0.0, 12.0, 240001)
    pdf = c * (1 + x**2 / df) ** (-(df + 1) / 2)
    cdf = 0.5 + np.concatenate([[0.0], np.cumsum((pdf[1:] + pdf[:-1]) / 2 * np.diff(x))])
    return float(np.interp(0.975, cdf, x))


def fig_evidence_synthesis(s: dict, out: Path) -> dict:
    """Forest plot of the published studies; funnel plot of every study run."""
    lab = {k: _sim_label(s, k) for k in L["book"] if k.startswith("es_")}
    rng = np.random.default_rng(SEED)

    k, mu, tau = 30, 1.0, 0.5            # 30 studies RUN; true average +1.0 pp
    se = rng.uniform(0.3, 2.5, k)        # small studies carry large standard errors
    theta = rng.normal(mu, tau, k)       # each study's own true effect
    est = rng.normal(theta, se)          # what each study reports
    significant = est / se > 1.96
    published = significant | (rng.random(k) < 0.25)   # nulls rarely get out

    def pool(y, sv):
        """Random-effects mean (DerSimonian-Laird spread) with an HKSJ interval."""
        w = 1 / sv**2
        fe = np.sum(w * y) / np.sum(w)
        q = np.sum(w * (y - fe) ** 2)
        n = len(y)
        t2 = max(0.0, (q - (n - 1)) / (np.sum(w) - np.sum(w**2) / np.sum(w)))
        wr = 1 / (sv**2 + t2)
        m = np.sum(wr * y) / np.sum(wr)
        qstar = np.sum(wr * (y - m) ** 2) / (n - 1)
        se_h = math.sqrt(max(qstar, 1.0) / np.sum(wr))
        half = _t975(n - 1) * se_h
        return float(m), float(m - half), float(m + half), float(t2)

    all_m, all_lo, all_hi, all_t2 = pool(est, se)
    pub_m, pub_lo, pub_hi, pub_t2 = pool(est[published], se[published])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.2),
                                 gridspec_kw={"width_ratios": [1.05, 1]})
    # ---- left: forest plot of the published studies, most precise on top
    idx = np.where(published)[0]
    idx = idx[np.argsort(se[idx])]
    ys = np.arange(len(idx), 0, -1) + 1.0
    a1.errorbar(est[idx], ys, xerr=1.96 * se[idx], fmt="s", color=BLUE,
                ms=4, lw=1, capsize=0)
    a1.fill([pub_lo, pub_m, pub_hi, pub_m], [0.5, 0.85, 0.5, 0.15], color=ORANGE)
    a1.axvline(0, color=GREY, lw=0.8)
    a1.axvline(mu, color=INK, ls="--", lw=1.1)
    a1.set_yticks(list(ys) + [0.5])
    a1.set_yticklabels([lab["es_study"].format(i=i + 1) for i in idx]
                       + [lab["es_pooled_pub"]], fontsize=7.5)
    a1.text(mu + 0.2, len(idx) + 1.9, lab["es_truth"].format(v=mu), color=INK,
            fontsize=8, ha="left")
    a1.set_ylim(-0.2, len(idx) + 2.4)
    a1.set_xlabel(lab["es_xlabel"], fontsize=8.5)
    a1.set_title(lab["es_forest_title"], fontsize=9.5, loc="left")

    # ---- right: funnel plot of every study run
    a2.scatter(est[published], se[published], color=BLUE, s=22, zorder=3,
               label=lab["es_published"].format(n=int(published.sum())))
    a2.scatter(est[~published], se[~published], facecolors="none",
               edgecolors=GREY, s=22, zorder=3,
               label=lab["es_unpublished"].format(n=int((~published).sum())))
    grid = np.linspace(0, se.max() * 1.05, 50)
    a2.plot(1.96 * grid, grid, color=GREY, ls=":", lw=1,
            label=lab["es_sigline"])
    a2.axvline(pub_m, color=ORANGE, lw=1.4,
               label=lab["es_line_pub"].format(v=pub_m))
    a2.axvline(all_m, color=BLUE, lw=1.4,
               label=lab["es_line_all"].format(v=all_m))
    a2.axvline(mu, color=INK, ls="--", lw=1.1)
    a2.invert_yaxis()
    a2.set_xlabel(lab["es_xlabel"], fontsize=8.5)
    a2.set_ylabel(lab["es_ylabel_se"], fontsize=8.5)
    a2.set_title(lab["es_funnel_title"], fontsize=9.5, loc="left")
    a2.legend(fontsize=7, frameon=False, loc="upper right")
    for ax in (a1, a2):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.tick_params(labelsize=7.5)
    fig.tight_layout()
    fig.savefig(out / "evidence_synthesis.png", dpi=150)
    plt.close(fig)

    unpub = ~published
    return {
        "k_run": k,
        "mu": mu,
        "tau": tau,
        "n_pub": int(published.sum()),
        "n_unpub": int(unpub.sum()),
        "n_sig_all": int(significant.sum()),
        "n_sig_pub": int(significant[published].sum()),
        "n_null_pub": int((published & ~significant).sum()),
        "n_unpub_below_mu": int((est[unpub] < mu).sum()),
        "all_m": all_m,
        "all_lo": all_lo,
        "all_hi": all_hi,
        "pub_m": pub_m,
        "pub_lo": pub_lo,
        "pub_hi": pub_hi,
        "pub_t2": pub_t2,
        "all_t2": all_t2,
        "inflation_ratio": pub_m / all_m,
    }


# D83: the further-route figures, in book order (Chapters 41-44 and 46).
FURTHER_SIMS = [
    ("natural-experiments", fig_natural_experiments),
    ("survey-experiments", fig_survey_experiments),
    ("audit-studies", fig_audit_studies),
    ("text-as-data", fig_text_as_data),
    ("evidence-synthesis", fig_evidence_synthesis),
]


def main() -> None:
    # D36 freeze (round-5 L1): localized figures for PT/ES are frozen with
    # their editions; generate EN only until the translation pass.
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--editions", default="en",
                    help="'en' (default, D36 freeze), 'all', or a comma list "
                         "of edition dirs")
    sel = ap.parse_args().editions
    active = (L if sel == "all"
              else {k: v for k, v in L.items()
                    if k in {"book" if s == "en" else f"book-{s}"
                             for s in sel.split(",")}})
    for edition, strings in active.items():
        out = REPO / edition / "images" / "sims"
        out.mkdir(parents=True, exist_ok=True)
        stats11 = fig_ch11(strings, out)
        stats14 = fig_ch14(strings, out)
        stats15 = fig_ch15(strings, out)
        stats15a = fig_ch15_attrition(strings, out)
        stats22 = fig_ch22(strings, out)
        further = {name: fn(strings, out) for name, fn in FURTHER_SIMS}
        print(f"✓ {edition}: {5 + len(FURTHER_SIMS)} figures → "
              f"{out.relative_to(REPO)}/")
    print("ch11:", {k: (round(v, 2) if isinstance(v, float) else v)
                    for k, v in stats11.items()})
    print("ch14:", {k: (round(v, 3) if isinstance(v, float) else v)
                    for k, v in stats14.items()})
    print("ch15:", {k: round(float(v), 2) for k, v in stats15.items()})
    print("ch15-attrition:", {k: round(float(v), 3) for k, v in stats15a.items()})
    print("ch22:", {k: round(float(v), 3) for k, v in stats22.items()})
    for name, st in further.items():
        print(f"{name}:", {k: round(float(v), 3) for k, v in st.items()})


if __name__ == "__main__":
    main()
