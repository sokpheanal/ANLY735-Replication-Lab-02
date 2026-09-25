# Replication Laboratory #2 — Can the Model Keep Learning?

A from-scratch controlled experiment and a **proxy replication** of the
stability-plasticity phenomenon synthesized in Klein et al. (2026), *Plasticity Loss
in Deep Reinforcement Learning: A Survey*. The survey is a literature review, so
there is no original experiment to reproduce; this lab builds a controlled learning
experiment that induces non-stationarity and applies the Stability-Plasticity
Diagnostic (CHANGE, RETENTION, NEW LEARNING, RATE, TRADEOFF) to the resulting
behavior.

## Experiment

A single-hidden-layer MLP regresses a sequence of 100 random teacher functions over
fixed inputs (pure target non-stationarity). Three arms:

- **continual** — one network trained straight through all tasks.
- **fresh** — reinitialized each task (the plasticity-definition baseline).
- **L2-Init** — continual network regularized toward its initial weights (the
  mitigation arm).

Plasticity is diagnosed from post-change learning (best R^2 and rate on each new
target), not from the size of the drop.

## Committed source (everything else regenerates)

```text
README.md
replication-lab.qmd            # the report (renders to Word)
references.bib
custom-reference.docx          # Word styling for the render
apa.csl                        # APA citation style
requirements.txt
.gitignore
code/
  plasticity_regression.py     # experiment: MLP, three arms, task stream
  run_analysis.py              # runs all seeds, writes results/ and figures/
```

Generated at run time (git-ignored):

```text
results/metrics.csv results/summary.json results/out.pkl
figures/fig1_new_learning.png figures/fig2_rate.png figures/fig3_dead_units.png
replication-lab.docx
```

## Reproduce

```bash
pip install -r requirements.txt
cd code
python3 run_analysis.py --force    # ~90s on CPU; writes results/ and figures/
```

Then render the report:

```bash
quarto render replication-lab.qmd --to docx
```

## Configuration

Fixed in `code/plasticity_regression.py` (`DEFAULT_CFG`): 1000 samples, 16 features,
hidden width 48, batch 64, 100 tasks, 40 epochs/task, learning rate 0.11, target
frequency 2.5, R^2 threshold 0.4, L2-Init lambda 0.01. Seeds 0-5 in
`run_analysis.py`. The effect is regime-dependent: at low learning rates the
continual network stays plastic; at rates above ~0.12 the regression diverges. See
report Sections 6 and 7.
