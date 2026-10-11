# Cyclic symmetry and failure of block-permutation invariance in Dexter intervals

This directory contains the manuscript on cyclic symmetry, block permutations,
and derived categories of Dexter intervals.

## Main content

The paper proves derived invariance under cyclic rotation of the blocks,
exhibits an explicit integer-Euler counterexample to arbitrary block
permutation, and derives the resulting two-class statement for the specified
three blocks. It also records the boundary-attachment obstruction and the
positive subfamilies covered by the construction.

## Scope and limitations

The counterexample disproves a general block-permutation theorem; the paper
does not claim invariance under arbitrary permutations, minimality of the
counterexample, or external confirmation of novelty. The positive rotation,
mutation, and block-transfer statements remain restricted to their stated
families and hypotheses.

## Files

- [LaTeX source](dexter_block_permutation.tex)
- [PDF (24 pages)](dexter_block_permutation.pdf)
- [Supplementary verification files](supplementary/README.md)

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
xelatex -interaction=nonstopmode -halt-on-error dexter_block_permutation.tex
xelatex -interaction=nonstopmode -halt-on-error dexter_block_permutation.tex
```

The independent numerical checks are documented in the
[supplementary README](supplementary/README.md).

## License

Unless otherwise noted, the manuscript source and PDF are released under the
[CC BY 4.0 root LICENSE](../LICENSE).
