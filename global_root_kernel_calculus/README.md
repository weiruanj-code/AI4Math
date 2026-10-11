# Exceptional and Completed Root Kernel Calculus: A Single-Transition Problem

This directory contains an unfinished research draft. It is separate from the
nearby-kernel manuscript and does not claim a global theorem.

## Main content

The draft isolates one decisive problem for a fixed `xy=t^4` transition with
`B={2}`: construct an exceptional, completed, or mixed root-kernel source,
unit, and convolution on a full nodal support, and verify both unit laws for a
cross-node rectangular kernel while retaining the actual localization
boundary.

## Scope and limitations

No global theorem is claimed. The global root-kernel source, full-fibre
generating kernel and integral, strong convolution, and global
Verdier/refinement construction remain unfinished. Ordinary stalk/pullback
distributional inverse gluing has been ruled out, but the local and coarse
checks do not establish a global construction. The draft therefore remains a
research problem rather than a completed fourth main result.

## Files

- [LaTeX source](global_root_kernel_calculus.tex)
- [PDF (8 pages)](global_root_kernel_calculus.pdf)

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
xelatex -interaction=nonstopmode -halt-on-error global_root_kernel_calculus.tex
xelatex -interaction=nonstopmode -halt-on-error global_root_kernel_calculus.tex
```

## License

Unless otherwise noted, the manuscript source and PDF are released under the
[CC BY 4.0 root LICENSE](../LICENSE).
