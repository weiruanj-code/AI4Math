# Verdier-Compatible Kernel Skeletonization under Anchored Semistable Refinement

**Status:** scoped mathematical manuscript; source and compiled PDF included.

## Main content

For four fixed anchored semistable models of $xy=t^4$, with $B=\{2\}$, the
paper constructs geometric rational unipotent nearby coefficients and
complete inverse-image supports. It proves one-sided descent on a specified
generated kernel source and gives a Morita realization compatible with the
stated convolution, unit, Verdier-mate, support, and refinement comparisons.

## Scope and limitations

The results apply to the four stated models and the specified generated
source. The paper does not assert full faithfulness, unrestricted descent for
arbitrary supports or models, or a global root-kernel source. The appendices
contain local completed-root calculations and an obstruction to ordinary
distribution gluing; they do not establish a global root sheaf or costalk
descent category. The two dated companion manuscripts are cited as fixed
inputs but are not bundled with this public release.

## Search keywords

Anchored semistable models, kernel skeletonization, one-sided kernel descent,
generated kernel sources, complete inverse-image supports, geometric
unipotent nearby coefficients, Morita realization, Verdier mates.

## Citation suggestion

*Verdier-Compatible Kernel Skeletonization under Anchored Semistable
Refinement*, version dated 27 September 2026.

## Build

With XeLaTeX installed, run twice from this directory so references settle:

```powershell
xelatex -interaction=nonstopmode -halt-on-error verdier_kernel_skeletonization.tex
xelatex -interaction=nonstopmode -halt-on-error verdier_kernel_skeletonization.tex
```
