"""
Proxy replication of loss of plasticity under target non-stationarity (regression).

Phenomenon (Klein et al., 2026, Sec. 4.2/4.4): a network trained continually across
a sequence of changing regression targets loses the capacity to FIT new targets,
while a freshly initialized network fits each new target as well as ever. General
regularization toward the initial weights (L2-Init, Sec. 5.3) is expected to
mitigate the loss.

Design
------
* Inputs: a fixed synthetic design matrix X (drawn once).
* Non-stationarity: K sequential tasks. Each task draws a new random teacher
  function f_t(x) = scale * tanh(3 * x @ w_t / sqrt(d)); only the target mapping
  changes (pure target shift). Value-based RL's large-magnitude targets are
  reflected by `scale`.
* Arms:
    - continual : one network trained straight through all K tasks.
    - fresh     : network reinitialized from scratch on every task (the baseline).
    - l2init    : continual network with an L2 penalty toward its initial weights.
* Metric (matched to the phenomenon, not the drop): per task, the best fit reached
  within a fixed epoch budget, measured as R^2 on the training targets, and the
  number of epochs to reach an R^2 threshold (RATE). Dead-ReLU fraction is tracked
  as the mechanism. Retention is measured at the end as R^2 on task 1's targets.
"""

import numpy as np


class MLPRegressor:
    def __init__(self, n_in, n_hidden, rng):
        self.W1 = rng.standard_normal((n_in, n_hidden)) * np.sqrt(2.0 / n_in)
        self.b1 = np.zeros(n_hidden)
        self.W2 = rng.standard_normal((n_hidden, 1)) * np.sqrt(2.0 / n_hidden)
        self.b2 = np.zeros(1)
        self.W1_0, self.b1_0 = self.W1.copy(), self.b1.copy()
        self.W2_0, self.b2_0 = self.W2.copy(), self.b2.copy()

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = np.maximum(0.0, self.z1)
        self.yhat = (self.a1 @ self.W2 + self.b2).ravel()
        return self.yhat

    def dead_fraction(self, X):
        a1 = np.maximum(0.0, X @ self.W1 + self.b1)
        return float((a1.max(axis=0) == 0).mean())

    def sgd_step(self, X, y, lr, l2init=0.0):
        n = X.shape[0]
        yhat = self.forward(X)
        dy = (2.0 / n) * (yhat - y)[:, None]          # dL/dyhat, MSE
        gW2 = self.a1.T @ dy
        gb2 = dy.sum(axis=0)
        da1 = dy @ self.W2.T
        dz1 = da1 * (self.z1 > 0)
        gW1 = X.T @ dz1
        gb1 = dz1.sum(axis=0)
        if l2init > 0.0:
            gW1 += l2init * (self.W1 - self.W1_0); gb1 += l2init * (self.b1 - self.b1_0)
            gW2 += l2init * (self.W2 - self.W2_0); gb2 += l2init * (self.b2 - self.b2_0)
        self.W1 -= lr * gW1; self.b1 -= lr * gb1
        self.W2 -= lr * gW2; self.b2 -= lr * gb2


def r2(yhat, y):
    if not np.all(np.isfinite(yhat)):
        return np.nan
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum()) + 1e-12
    return 1.0 - ss_res / ss_tot


def make_task(X, rng, scale, freq):
    d = X.shape[1]
    w1 = rng.standard_normal(d); w2 = rng.standard_normal(d)
    return scale * (np.sin(freq * (X @ w1) / np.sqrt(d)) +
                    0.5 * np.sin(2 * freq * (X @ w2) / np.sqrt(d)))


def train_task(net, X, y, cfg, lr, l2init=0.0):
    rng = cfg["_task_rng"]; n = X.shape[0]
    curve = []
    for _ in range(cfg["epochs_per_task"]):
        idx = rng.permutation(n)
        for s in range(0, n, cfg["batch_size"]):
            b = idx[s:s + cfg["batch_size"]]
            net.sgd_step(X[b], y[b], lr, l2init)
        curve.append(r2(net.forward(X), y))
    return np.array(curve)


def epochs_to_threshold(curve, thr):
    hit = np.where(curve >= thr)[0]
    return int(hit[0] + 1) if hit.size else np.nan


def run_seed(seed, cfg):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((cfg["n_samples"], cfg["n_features"]))
    tasks = [make_task(X, np.random.default_rng(seed + 100 + t), cfg["scale"], cfg["freq"])
             for t in range(cfg["n_tasks"])]
    y_first = tasks[0]

    arms = {}
    for name in ["continual", "fresh", "l2init"]:
        net = MLPRegressor(cfg["n_features"], cfg["n_hidden"],
                           np.random.default_rng(seed + 7))
        best, steps, dead = [], [], []
        early_curve = late_curve = None
        for t, y in enumerate(tasks):
            if name == "fresh":
                net = MLPRegressor(cfg["n_features"], cfg["n_hidden"],
                                   np.random.default_rng(seed + 7 + t + 1))
            cfg["_task_rng"] = np.random.default_rng(seed + 5000 + t)
            lam = cfg["l2init_lambda"] if name == "l2init" else 0.0
            curve = train_task(net, X, y, cfg, cfg["lr"], lam)
            best.append(np.nanmax(curve) if np.isfinite(curve).any() else np.nan)
            steps.append(epochs_to_threshold(curve, cfg["threshold"]))
            dead.append(net.dead_fraction(X))
            if t == 0: early_curve = curve
            if t == cfg["n_tasks"] - 1: late_curve = curve
        retention = r2(net.forward(X), y_first)   # fit on task 1 after all tasks
        arms[name] = dict(best=np.array(best), steps=np.array(steps, float),
                          dead=np.array(dead), retention=retention,
                          early_curve=early_curve, late_curve=late_curve)
    return arms


def run(cfg, seeds):
    per = [run_seed(s, cfg) for s in seeds]
    out = {}
    for name in ["continual", "fresh", "l2init"]:
        best = np.stack([p[name]["best"] for p in per])       # (S, K)
        steps = np.stack([p[name]["steps"] for p in per])
        dead = np.stack([p[name]["dead"] for p in per])
        ret = np.array([p[name]["retention"] for p in per])
        ec = np.stack([p[name]["early_curve"] for p in per]).mean(0)
        lc = np.stack([p[name]["late_curve"] for p in per]).mean(0)
        out[name] = dict(best_mean=np.nanmean(best, 0), best_std=np.nanstd(best, 0),
                         steps_mean=np.nanmean(steps, 0), dead_mean=dead.mean(0),
                         retention_mean=float(np.nanmean(ret)), best_raw=best,
                         early_curve=ec, late_curve=lc)
    return out, per


DEFAULT_CFG = dict(n_samples=1000, n_features=16, n_hidden=48, batch_size=64,
                   n_tasks=100, epochs_per_task=40, lr=0.11, scale=1.0,
                   threshold=0.40, l2init_lambda=0.01, freq=2.5)

if __name__ == "__main__":
    import sys
    cfg = dict(DEFAULT_CFG)
    if "--quick" in sys.argv:
        cfg.update(n_tasks=20, epochs_per_task=30)
    out, _ = run(cfg, [0, 1])
    K = cfg["n_tasks"]; early = slice(0, 3); late = slice(K - 3, K)
    for nm in ["continual", "fresh", "l2init"]:
        e = out[nm]["best_mean"][early].mean(); l = out[nm]["best_mean"][late].mean()
        print(f"{nm:10s} R2 early={e:.3f} late={l:.3f} dead_late={out[nm]['dead_mean'][late].mean():.2f} "
              f"retention={out[nm]['retention_mean']:.3f}")
    print(f"gap(fresh-continual) late R2 = "
          f"{out['fresh']['best_mean'][late].mean()-out['continual']['best_mean'][late].mean():.3f}")
