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

Current figures (first tranche, D26): ch11 random-vs-convenience sampling,
ch14 overfitting (train vs holdout error), ch15 the randomization
distribution of a difference in means.
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
        "test": "Holdout error",
        "xlabel_deg": "Model flexibility (polynomial degree)",
        "ylabel_rmse": "Prediction error (RMSE)",
        "best": "honest best",
        "truth_ate": "true effect = {v:.1f} pp",
        "mean_est": "mean of estimates = {v:.1f} pp",
        "xlabel_ate": "Estimated effect of the reminder (percentage points)",
        "ylabel_n": "Number of re-randomizations",
    },
    "book-pt": {
        "random": "Amostras aleatórias\n(n = 500)",
        "convenience": "Canal de\nconveniência (n = 500)",
        "truth_age": "média verdadeira = {v:.1f}",
        "xlabel_age": "Idade média da amostra (anos)",
        "train": "Erro de treino",
        "test": "Erro no conjunto de teste",
        "xlabel_deg": "Flexibilidade do modelo (grau do polinômio)",
        "ylabel_rmse": "Erro de predição (RMSE)",
        "best": "melhor honesto",
        "truth_ate": "efeito verdadeiro = {v:.1f} pp",
        "mean_est": "média das estimativas = {v:.1f} pp",
        "xlabel_ate": "Efeito estimado do lembrete (pontos percentuais)",
        "ylabel_n": "Número de re-sorteios",
    },
    "book-es": {
        "random": "Muestras aleatorias\n(n = 500)",
        "convenience": "Canal por\nconveniencia (n = 500)",
        "truth_age": "media verdadera = {v:.1f}",
        "xlabel_age": "Edad media de la muestra (años)",
        "train": "Error de entrenamiento",
        "test": "Error en el conjunto de prueba",
        "xlabel_deg": "Flexibilidad del modelo (grado del polinomio)",
        "ylabel_rmse": "Error de predicción (RMSE)",
        "best": "mejor honesto",
        "truth_ate": "efecto verdadero = {v:.1f} pp",
        "mean_est": "media de las estimaciones = {v:.1f} pp",
        "xlabel_ate": "Efecto estimado del recordatorio (puntos porcentuales)",
        "ylabel_n": "Número de reasignaciones",
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
    rng = np.random.default_rng(SEED)

    def world(n):
        x = rng.uniform(-3, 3, n)
        return x, np.sin(1.5 * x) + rng.normal(0, .35, n)

    x_train, y_train = world(40)
    x_test, y_test = world(40)
    degrees = np.arange(1, 13)
    train_err, test_err = [], []
    for d in degrees:
        coefs = np.polyfit(x_train, y_train, d)
        train_err.append(np.sqrt(np.mean(
            (np.polyval(coefs, x_train) - y_train) ** 2)))
        test_err.append(np.sqrt(np.mean(
            (np.polyval(coefs, x_test) - y_test) ** 2)))
    best = degrees[int(np.argmin(test_err))]

    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    ax.plot(degrees, train_err, color=BLUE, lw=2, marker="o", ms=4)
    ax.plot(degrees, test_err, color=ORANGE, lw=2, marker="o", ms=4)
    ax.axvline(best, color=INK, ls=":", lw=1)
    ax.text(degrees[-1], train_err[-1], "  " + s["train"], color=BLUE,
            fontsize=9, va="center")
    ax.text(degrees[-1], test_err[-1], "  " + s["test"], color=ORANGE,
            fontsize=9, va="center")
    ax.text(best + .1, max(test_err) * .95, s["best"], color=INK, fontsize=9)
    ax.set_xlabel(s["xlabel_deg"])
    ax.set_ylabel(s["ylabel_rmse"])
    ax.set_xlim(degrees[0], degrees[-1] + 3.4)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5", lw=.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / "ch14_overfitting.png", dpi=150)
    plt.close(fig)
    return {"best": int(best), "train_at_12": train_err[-1],
            "test_at_12": test_err[-1], "test_at_best": min(test_err)}


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


def main() -> None:
    for edition, strings in L.items():
        out = REPO / edition / "images" / "sims"
        out.mkdir(parents=True, exist_ok=True)
        stats11 = fig_ch11(strings, out)
        stats14 = fig_ch14(strings, out)
        stats15 = fig_ch15(strings, out)
        print(f"✓ {edition}: 3 figures → {out.relative_to(REPO)}/")
    print("ch11:", {k: (round(v, 2) if isinstance(v, float) else v)
                    for k, v in stats11.items()})
    print("ch14:", {k: (round(v, 3) if isinstance(v, float) else v)
                    for k, v in stats14.items()})
    print("ch15:", {k: round(float(v), 2) for k, v in stats15.items()})


if __name__ == "__main__":
    main()
