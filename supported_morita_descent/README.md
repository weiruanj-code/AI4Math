# Supported Morita Descent for Semistable Curves

This directory contains a scoped manuscript on supported coefficient and
kernel descent for semistable curves.

## Main content

For a fixed trait, the paper compares nearby coefficient-support systems for
the same integer cut and marked profile. It also proves, in the stated
geometric range, an actual one-sided kernel counit, strong convolution, and a
Morita--Verdier comparison. The manuscript records the corresponding
finite-etale support spans and rectangular cross-curve extension.

## Scope and limitations

The result is deliberately bounded: geometric `Q_ell` coefficients, the
specified support profiles, and the stated semistable presentations. It does
not cover high-dimensional modifications, relative-trait products, all
generic or logarithmic sources, arbitrary independent-endpoint kernel descent,
or a global root-`!` construction.

The frozen companion sources under `companion_sources/` and the input manifest
are local project-archive materials only. They are retained locally and are
not included in the public release. The following links point to current
public manuscript directories for related work; they are reference links, not
replacements for the frozen companion versions:

- [Local Kummer Realizations and Verdier Duality](https://github.com/weiruanj-code/AI4Math/tree/main/three_realization_submission)
- [Morita Coefficients, Incidence, and Semistable Refinement](https://github.com/weiruanj-code/AI4Math/tree/main/semistable_morita_refinement)
- [Verdier-Compatible Kernel Skeletonization under Anchored Semistable Refinement](https://github.com/weiruanj-code/AI4Math/tree/main/verdier_kernel_skeletonization)

## Files

- [LaTeX source](supported_morita_descent.tex)
- [PDF (32 pages)](supported_morita_descent.pdf)

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
xelatex -interaction=nonstopmode -halt-on-error supported_morita_descent.tex
xelatex -interaction=nonstopmode -halt-on-error supported_morita_descent.tex
```

## License

Unless otherwise noted, the manuscript source and PDF are released under the
[CC BY 4.0 root LICENSE](../LICENSE).
