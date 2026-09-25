# Replication Laboratory #2 — Reproducing Figure 3

Direct reproduction of Figure 3 in Klein et al. (2026), *Plasticity Loss in Deep
Reinforcement Learning: A Survey*: the visualization of categorical target
representations for value-based RL.

The figure contrasts three ways of turning a value-regression target into a
categorical target over a fixed support of atoms:

- **Two-hot** (Schrittwieser et al., 2020): mass on the two atoms bracketing a
  scalar target.
- **HL-Gauss** (Imani & White, 2018): a fixed-width Gaussian integrated over each bin.
- **C51** (Bellemare et al., 2017): a full return distribution propagated through
  the Bellman map `r + gamma*Z` and projected back onto the support.

Each mapping is deterministic and defined by a published equation, so the
reproduction needs no data, no training, and no random seed.

## Committed source (everything below is regenerated)

```text
README.md
replication-lab.qmd            # the report (renders to Word)
references.bib
requirements.txt
.gitignore
code/
  reproduce_fig3.ipynb         # implements two-hot, HL-Gauss, C51; writes figure + table
```

Generated at run time (git-ignored):

```text
figures/fig3_categorical_losses.png    # created by the notebook
results/categorical_masses.csv         # created by the notebook
replication-lab.docx                    # created by `quarto render`
```

## Reproduce

```bash
pip install -r requirements.txt
# run the notebook (writes figures/ and results/):
jupyter nbconvert --to notebook --execute --inplace code/reproduce_fig3.ipynb
# or open code/reproduce_fig3.ipynb in Jupyter and Run All
```

Then render the report:

```bash
quarto render replication-lab.qmd --to docx
```

The notebook creates the figure and table; `quarto render` builds the `.docx` and
embeds the figure, so run the notebook before rendering.

## Parameters

Fixed at the top of `code/reproduce_fig3.ipynb`: support of 5 atoms on [-1, 1];
scalar target y = 0.20; HL-Gauss sigma = 1 bin width; C51 reward r = 0.10 and
discount gamma = 0.80. The original figure is schematic and states none of these,
so they are documented choices; see report Sections 6 and 7.
