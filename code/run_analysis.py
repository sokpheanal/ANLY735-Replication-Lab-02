"""Run the full experiment (6 seeds), write results/ tables and figures/ plots.

Usage:  python3 run_analysis.py [--force]
Outputs:
    results/metrics.csv      per-task, per-arm summary across seeds
    results/summary.json     headline numbers used in the report
    results/out.pkl          cached raw run
    figures/fig1_new_learning.png     best R^2 vs task index (the diagnostic plot)
    figures/fig2_rate.png             within-task R^2 curves, early vs late task
    figures/fig3_dead_units.png       dead-ReLU fraction vs task index (mechanism)
"""
import json
import os
import pickle
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from plasticity_regression import run, DEFAULT_CFG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "figures"); RES = os.path.join(ROOT, "results")
os.makedirs(FIG, exist_ok=True); os.makedirs(RES, exist_ok=True)
NAVY, GOLD, GREY = "#12233f", "#b8860b", "#9aa0a6"
SEEDS = [0, 1, 2, 3, 4, 5]
CFG = dict(DEFAULT_CFG); K = CFG["n_tasks"]


def to_native(o):
    if isinstance(o, dict): return {k: to_native(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [to_native(v) for v in o]
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, np.generic): return o.item()
    return o


CACHE = os.path.join(RES, "out.pkl")
if os.path.exists(CACHE) and "--force" not in sys.argv:
    print("Loading cached run (use --force to rerun)")
    out = pickle.load(open(CACHE, "rb"))
else:
    print(f"Running {len(SEEDS)} seeds, config={ {k:v for k,v in CFG.items() if not k.startswith('_')} }")
    out, _ = run(CFG, SEEDS)
    pickle.dump(out, open(CACHE, "wb"))

x = np.arange(1, K + 1)
early, late = slice(0, 5), slice(K - 5, K)
def ms(name, key, sl): return float(np.nanmean(out[name][key][sl]))

# ---- metrics table -------------------------------------------------------- #
rows = []
for name in ["continual", "fresh", "l2init"]:
    for t in range(K):
        rows.append(dict(arm=name, task=t + 1,
                         best_r2_mean=out[name]["best_mean"][t],
                         best_r2_std=out[name]["best_std"][t],
                         steps_to_thr_mean=out[name]["steps_mean"][t],
                         dead_frac_mean=out[name]["dead_mean"][t]))
pd.DataFrame(rows).to_csv(os.path.join(RES, "metrics.csv"), index=False)

# per-seed late gap for a spread-based verdict
late_gap = (out["fresh"]["best_raw"][:, late].mean(1)
            - out["continual"]["best_raw"][:, late].mean(1))
summary = dict(
    config={k: v for k, v in CFG.items() if not k.startswith("_")}, seeds=SEEDS,
    continual_early_r2=ms("continual", "best_mean", early),
    continual_late_r2=ms("continual", "best_mean", late),
    fresh_late_r2=ms("fresh", "best_mean", late),
    l2init_late_r2=ms("l2init", "best_mean", late),
    continual_dead_late=ms("continual", "dead_mean", late),
    l2init_dead_late=ms("l2init", "dead_mean", late),
    continual_retention=out["continual"]["retention_mean"],
    fresh_retention=out["fresh"]["retention_mean"],
    l2init_retention=out["l2init"]["retention_mean"],
    continual_late_steps=ms("continual", "steps_mean", late),
    fresh_late_steps=ms("fresh", "steps_mean", late),
    l2init_late_steps=ms("l2init", "steps_mean", late),
    late_gap_mean=float(np.nanmean(late_gap)),
    late_gap_std=float(np.nanstd(late_gap)),
    late_gap_per_seed=[round(float(v), 3) for v in late_gap],
)
json.dump(to_native(summary), open(os.path.join(RES, "summary.json"), "w"), indent=2)

# ---- fig 1: new-learning (best R^2) vs task index ------------------------- #
def smooth(a, w=7):
    return pd.Series(a).rolling(w, center=True, min_periods=1).mean().values
plt.figure(figsize=(7, 4.3))
for name, col, lab in [("fresh", GREY, "Fresh init (baseline)"),
                       ("l2init", GOLD, "Continual + L2-Init"),
                       ("continual", NAVY, "Continual")]:
    m = out[name]["best_mean"]
    plt.plot(x, m, color=col, lw=0.8, alpha=0.25)
    plt.plot(x, smooth(m), color=col, lw=2.4, label=lab)
plt.xlabel("Task index (successive target changes)")
plt.ylabel("Best $R^2$ on the new target within budget")
plt.title("New-learning capacity across successive tasks (7-task rolling mean)")
plt.legend(frameon=False, fontsize=9); plt.tight_layout()
plt.savefig(os.path.join(FIG, "fig1_new_learning.png"), dpi=150); plt.close()

# ---- fig 2: within-task rate, early vs late ------------------------------- #
ep = np.arange(1, CFG["epochs_per_task"] + 1)
plt.figure(figsize=(7, 4.3))
plt.plot(ep, out["continual"]["early_curve"], color=GREY, lw=2, label="Continual, task 1")
plt.plot(ep, out["continual"]["late_curve"], color=NAVY, lw=2, label=f"Continual, task {K}")
plt.plot(ep, out["fresh"]["late_curve"], color=GOLD, lw=2, ls="--", label=f"Fresh, task {K}")
plt.axhline(CFG["threshold"], color="k", lw=0.8, ls=":", alpha=0.6)
plt.xlabel("Epoch within task"); plt.ylabel("$R^2$ on the current target")
plt.title("Learning rate within a task: early vs late")
plt.legend(frameon=False, fontsize=9); plt.tight_layout()
plt.savefig(os.path.join(FIG, "fig2_rate.png"), dpi=150); plt.close()

# ---- fig 3: dead-unit fraction vs task index ------------------------------ #
plt.figure(figsize=(7, 4.3))
for name, col, lab in [("continual", NAVY, "Continual"), ("l2init", GOLD, "Continual + L2-Init")]:
    plt.plot(x, out[name]["dead_mean"], color=col, lw=2, label=lab)
plt.xlabel("Task index"); plt.ylabel("Fraction of dead ReLU units")
plt.title("Mechanism: inactive units accumulate in the continual network")
plt.ylim(0, 1.03); plt.legend(frameon=False, fontsize=9); plt.tight_layout()
plt.savefig(os.path.join(FIG, "fig3_dead_units.png"), dpi=150); plt.close()

print("\n== SUMMARY ==")
for k, v in summary.items():
    if k not in ("config", "seeds", "late_gap_per_seed"):
        print(f"{k:24s} {v}")
print("late_gap_per_seed        ", summary["late_gap_per_seed"])
print("\nwrote results/ and figures/")
