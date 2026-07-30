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
means, and ch15 treatment-dependent attrition (the complete-case contrast is
not the effect for everyone enrolled — the D35 Batch-A counterexample).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parent.parent
SEED = 464
BLUE, ORANGE, INK = "#2a78d6", "#eb6834", "#333333"

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
        "gapstat": "worse on the final holdout in {p:.0f}% of worlds\ntypical gap = {m:+.3f} RMSE",
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
        "gapstat": "pior no holdout final em {p:.0f}% dos mundos\ndiferença típica = {m:+.3f} RMSE",
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
        "gapstat": "peor en el holdout final en {p:.0f}% de los mundos\ndiferencia típica = {m:+.3f} RMSE",
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
    on the locked final holdout. Right: repeating the whole procedure in 500
    fresh worlds shows the winner's selection score is optimistic on average.
    """
    rng = np.random.default_rng(SEED)
    degrees = np.arange(1, 13)

    def world(n):
        x = rng.uniform(-3, 3, n)
        return x, np.sin(1.5 * x) + rng.normal(0, .35, n)

    def rmse(coefs, data):
        x, y = data
        return np.sqrt(np.mean((np.polyval(coefs, x) - y) ** 2))

    def one_world():
        training, selection, final = world(40), world(40), world(40)
        fits = [np.polyfit(training[0], training[1], d) for d in degrees]
        tr = np.array([rmse(c, training) for c in fits])
        sel = np.array([rmse(c, selection) for c in fits])
        chosen = int(np.argmin(sel))
        return tr, sel, chosen, rmse(fits[chosen], final)

    train_err, sel_err, chosen, final_err = one_world()

    gaps = []
    for _ in range(500):
        _, sel, pick, fresh_final = one_world()
        gaps.append(fresh_final - sel[pick])
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
    # A couple of worlds explode when a degree-12 fit extrapolates wildly, so
    # the MEAN gap is outlier-driven. Show the bulk and report robust numbers.
    lo, hi = -0.2, 0.3
    ax.hist(np.clip(gaps, lo, hi), bins=28, range=(lo, hi), color=BLUE,
            edgecolor="white", lw=.4)
    ax.axvline(0, color=INK, lw=1)
    ax.axvline(np.median(gaps), color=ORANGE, ls="--", lw=1.5)
    ax.text(.03, .90, s["gapstat"].format(p=100 * (gaps > 0).mean(),
                                          m=np.median(gaps)),
            color=ORANGE, fontsize=8, va="top", transform=ax.transAxes)
    ax.set_xlim(lo, hi)
    ax.set_xlabel(s["xlabel_gap"])
    ax.set_ylabel(s["ylabel_worlds"])

    for ax in axes:
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.grid(axis="y", color="#e5e5e5", lw=.6)
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / "ch14_overfitting.png", dpi=150)
    plt.close(fig)
    return {"chosen": int(degrees[chosen]), "sel_at_chosen": sel_err[chosen],
            "final_at_chosen": final_err, "median_gap": float(np.median(gaps)),
            "mean_gap_outlier_driven": gaps.mean(),
            "pct_worse": 100 * (gaps > 0).mean()}


def fig_ch15(s: dict, out: Path) -> dict:
    rng = np.random.default_rng(SEED)
    n, tau = 200, 5.0                      # true effect: +5 percentage points
    y0 = np.clip(rng.normal(70, 12, n), 20, 99)   # refill rate w/o reminder
    y1 = np.clip(y0 + tau, 20, 100)               # ... with the reminder
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


def main() -> None:
    for edition, strings in L.items():
        out = REPO / edition / "images" / "sims"
        out.mkdir(parents=True, exist_ok=True)
        stats11 = fig_ch11(strings, out)
        stats14 = fig_ch14(strings, out)
        stats15 = fig_ch15(strings, out)
        stats15a = fig_ch15_attrition(strings, out)
        print(f"✓ {edition}: 4 figures → {out.relative_to(REPO)}/")
    print("ch11:", {k: (round(v, 2) if isinstance(v, float) else v)
                    for k, v in stats11.items()})
    print("ch14:", {k: (round(v, 3) if isinstance(v, float) else v)
                    for k, v in stats14.items()})
    print("ch15:", {k: round(float(v), 2) for k, v in stats15.items()})
    print("ch15-attrition:", {k: round(float(v), 3) for k, v in stats15a.items()})


if __name__ == "__main__":
    main()
