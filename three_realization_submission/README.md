# Local Kummer Realizations and Verdier Duality

**Continuous cohomology, nearby cycles, and finite-root traces**

This directory contains the LaTeX source and compiled PDF of a local
three-realization manuscript for a semistable node with smooth disc
directions.

## Main content

For a fixed semistable node, the paper constructs a geometric inverse system
of traces from genuine finite-root shriek pushforwards. Its integral limit is
identified with the derived dual of continuous inertia cochains, including the
geometric shift and Tate twist, and is compared with nearby costalks and
analytic compact support.

The construction retains finite group bars, coefficient reduction, module
actions, coefficient maps, and integral torsion. On the selected perfect
cartesian adic source, the analytic realization is fully faithful and the
three ordinary images are continuous inertia cohomology. The construction
uses a fixed chart, base-root neutralization, compactification, and explicit
carriers.

## Scope and limitations

The results concern the stated local semistable/Kummer chart and selected
perfect adic coefficient systems; they are not a theorem for every abstract
constructible coefficient source. No shriek functor is defined on the bare
infinite-root fibre. The paper does not claim a global weak base-inertia
extension, an unrestricted common algebraic coefficient source, or an
equivalence obtained by replacing the relative Kummer face with the ordinary
unrigidified Artin fan. Proper-image presentations and larger coefficient
categories are treated as separate obstructions rather than absorbed into the
main comparison.

## Search keywords

`Kummer realizations`, `Verdier duality`, nearby cycles, vanishing cycles,
continuous cohomology, pro-l inertia, finite-root stacks, infinite root
stacks, adic coefficients, Artin stacks, Iwasawa cohomology, analytic compact
support, tame nearby cycles, logarithmic geometry, semistable nodes,
finite-carrier traces, six operations, Kummer torsors, derived categories.

## Files

- [`three_realization_submission.tex`](three_realization_submission.tex): LaTeX source.
- [`three_realization_submission.pdf`](three_realization_submission.pdf): compiled 75-page manuscript.

## Reproducibility

With the required LaTeX packages installed, compile the manuscript at least
twice so that cross-references and PDF bookmarks settle:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error three_realization_submission.tex
pdflatex -interaction=nonstopmode -halt-on-error three_realization_submission.tex
```

## Citation

*Local Kummer Realizations and Verdier Duality: Continuous cohomology, nearby
cycles, and finite-root traces*, AI4Math, 2026.

## License

The original manuscript material in this directory is released under
[CC BY 4.0](../LICENSE). Reusers may copy, redistribute, and adapt it,
including commercially, provided that they provide appropriate attribution,
link to the
license, and indicate changes.
