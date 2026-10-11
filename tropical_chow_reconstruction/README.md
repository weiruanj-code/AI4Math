# Weighted tropical Chow reconstruction for space curves

This directory contains the current mathematical manuscript on weighted
tropical Chow reconstruction for space curves.

## Main content

The paper proves injectivity of the weighted tropical Chow transform on finite
rational polyhedral one-chains with signed rational weights, without imposing
balancing. This yields reconstruction of balanced embedded tropical curves in
`R^4/R·1` with positive integer weights. Bounded edges, unbounded rays, and
non-fan supports are allowed; equality retains weights and positions after
common subdivision in the ambient coordinates.

## Scope and limitations

The theorem is restricted to the stated finite space-curve setting. It does
not claim a result for infinite complexes, higher-dimensional cycles, or a
Chow-polytope fan replacement, and the weights remain part of the input. The
literature-priority check is kept separate from the mathematical injectivity
claim.

## Files

- [LaTeX source](weighted_tropical_chow_reconstruction.tex)
- [PDF (10 pages)](weighted_tropical_chow_reconstruction.pdf)

## AI-assisted manuscript

This manuscript was prepared with AI assistance. Its source `Acknowledgments`
section credits, in order, textual data produced by humanity as a whole, the
accumulated achievements of mathematicians throughout history, successive
generations of neural-network researchers, and the OpenAI team. This describes
preparation assistance and does not replace mathematical verification.

## Reproducibility

Compiled with XeLaTeX on October 11, 2026.

Run from this directory with XeLaTeX twice:

```text
xelatex -interaction=nonstopmode -halt-on-error weighted_tropical_chow_reconstruction.tex
xelatex -interaction=nonstopmode -halt-on-error weighted_tropical_chow_reconstruction.tex
```

## License

Unless otherwise noted, the manuscript source and PDF are released under the
[CC BY 4.0 root LICENSE](../LICENSE).
