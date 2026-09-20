# From Represented $PGL_2$ Orbit Shells to Rank-One Orientation Reciprocity

**Quadratic Residual Towers, Haar--Frobenius Comparison, and the Unramified Absolute-$A_1$ Theorem**

Author: **YINGFENG JIANG**

This repository contains the LaTeX source and compiled PDF of a research
manuscript on a rank-one geometric and arithmetic model for orbital
reciprocity.

## Main content

The paper studies the universal quadratic family

\[
U=\operatorname{Spec} k[a,a^{-1},(1-a)^{-1}],
\qquad \mathcal E_k=\mathcal O_U[z]/(z^2-a),
\]

and its represented $PGL_2$ positive-loop orbit shells.  Its two principal
theorem packages are:

1. **Universal quadratic $PGL_2$ package.**  The manuscript constructs the
   finite residual tower of truncated-unit quotients, identifies the first
   layer with the norm-one torus, and relates successive layers to the
   trace-zero vector line.  It compares represented positive-loop orbit
   sheaves with quadratic order lattices, quotient Haar masses, compact
   Frobenius traces, and the Weyl-normalized orbital generating series.

2. **Unramified absolute-$A_1$ orientation reciprocity.**  For the explicitly
   defined central-neutral standard spherical families, it classifies the
   split and unramified-elliptic shell patterns and packages the local Haar
   coefficients into an orbit-summed rational $K_0$ interpolation.  The
   resulting generating series satisfies a rank-one orientation reciprocity
   relation governed by the determinant/root-orientation line.

The paper also constructs a finite labelled-shell Verdier partner and a
separate height-graded polyhedral $K_0$ shadow.  The latter is deliberately a
rational $K_0$ statement rather than an incidence-bearing sheaf or a general
logarithmic skeletonization theorem.

## Scope and limitations

The strongest geometric statements concern the universal quadratic equal-
characteristic loop family and represented fppf orbit sheaves.  The manuscript
does **not** claim a general affine-Springer quotient, cross-shell incidence
theory, convolution theorem, Rees completion, or an unrestricted global
tropical realization.  Outside the saturated $PGL_2$ case, the extension is
an explicitly specified orbit-summed classification and rational $K_0$
interpolation, not a relative represented-shell theorem.

This repository contains a mathematical manuscript, not a Lean-certified
formalization.  The paper itself records that it was generated 100% by
artificial intelligence; all mathematical claims should therefore be checked
independently.

## Files

- [`universal_quadratic_pgl2_orbit_shells.tex`](universal_quadratic_pgl2_orbit_shells.tex): LaTeX source.
- [`universal_quadratic_pgl2_orbit_shells.pdf`](universal_quadratic_pgl2_orbit_shells.pdf): compiled manuscript.

## Reproducibility

With a LaTeX installation containing the packages used by the source, compile
the manuscript twice:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error universal_quadratic_pgl2_orbit_shells.tex
pdflatex -interaction=nonstopmode -halt-on-error universal_quadratic_pgl2_orbit_shells.tex
```

## Search keywords

`PGL2`, `PGL_2`, orbital integrals, affine Springer fibers, quadratic orders,
positive loop groups, norm-one torus, Kummer local systems, Haar measure,
geometric Frobenius, Verdier duality, orientation reciprocity, residual
towers, rank-one groups, unramified absolute A1, rational K0, polyhedral
skeletonization, shell generating functions.

