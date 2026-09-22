# AI4Math

An open collection of AI-assisted mathematical research manuscripts. Each
paper is placed directly in its own top-level directory
so that source files, compiled PDFs, notes, and future revisions can be
separated cleanly.

## Repository structure

```text
AI4Math/
├── README.md                         # repository-wide index
├── LICENSE                           # CC BY 4.0
├── universal_quadratic_pgl2_orbit_shells/
│   ├── README.md                     # paper summary and search metadata
│   ├── universal_quadratic_pgl2_orbit_shells.tex
│   └── universal_quadratic_pgl2_orbit_shells.pdf
├── three_realization_submission/
│   ├── README.md                     # paper summary and search metadata
│   ├── three_realization_submission.tex
│   └── three_realization_submission.pdf
└── semistable_morita_refinement/
    ├── README.md                     # paper summary and search metadata
    ├── semistable_morita_refinement.tex
    └── semistable_morita_refinement.pdf
```

## Paper index

### From Represented $PGL_2$ Orbit Shells to Rank-One Orientation Reciprocity

**Quadratic Residual Towers, Haar--Frobenius Comparison, and the Unramified
Absolute-$A_1$ Theorem**

Folder: [`universal_quadratic_pgl2_orbit_shells/`](universal_quadratic_pgl2_orbit_shells/)

#### Main content

The paper studies represented positive-loop orbit shells in a universal
quadratic $PGL_2$ family. It constructs a residual tower, compares quadratic
order lattices with orbit sheaves, and derives rank-one orientation reciprocity
with a rational $K_0$ shadow.

#### Scope and limitations

The main geometric statements are restricted to the universal quadratic
equal-characteristic loop family and represented fppf orbit sheaves. General
affine-Springer quotients, cross-shell incidence, convolution, Rees completion,
and unrestricted global tropical realization are not claimed.

The paper directory contains the detailed summary, citation suggestion,
build instructions, and the latest source/PDF pair.

### Local Kummer Realizations and Verdier Duality

**Continuous cohomology, nearby cycles, and finite-root traces**

Folder: [`three_realization_submission/`](three_realization_submission/)

#### Main content

For a fixed semistable node with smooth disc directions, this paper constructs
a geometric inverse system of traces from genuine finite-root shriek
pushforwards. Its integral limit is compared with the derived dual of
continuous inertia cochains, nearby costalks, and analytic compact support,
while retaining finite group bars, coefficient maps, module actions, and
integral torsion.

#### Scope and limitations

The results concern the stated local semistable/Kummer chart and selected
perfect cartesian adic coefficient systems. The paper does not define a shriek
functor on the bare infinite-root fibre, nor claim global weak base-inertia
extensions, an unrestricted common algebraic coefficient source, or an
equivalence with the ordinary unrigidified Artin fan. Proper-image and larger
coefficient-source issues remain explicit obstructions.

### Morita Coefficients, Incidence, and Semistable Refinement

**A supported comparison for a subdivided annulus**

Folder: [`semistable_morita_refinement/`](semistable_morita_refinement/)

#### Main content

For a thickness-two nodal model and its explicit blow-up, the paper computes
the charts, exceptional support, and tube subdivision. It develops supported
Morita comparisons for geometric and finite logarithmic coefficients, including
generation, recollement, attaching maps, Verdier partners, minimal diagonal
kernels, fixed-thickness refinements, and a one-modification bridge to the
companion Kummer realization.

#### Scope and limitations

The proved comparisons are pairwise or organized over a fixed coarse support
index. The paper does not claim an unrestricted coherent support profile,
arbitrary model or base-change independence, full relative-product
convolution, a general base-inertia/logarithmic comparison, or integral
supported refinement.

## Search keywords

This is the merged search index for all papers in the repository. When adding
a future paper, append only genuinely new terms that are not already listed.

`PGL2`, `PGL_2`, orbital integrals, affine Springer fibers, quadratic orders,
positive loop groups, norm-one torus, Kummer realizations, Kummer local
systems, Kummer torsors, Haar measure, geometric Frobenius, Verdier duality,
orientation reciprocity, residual towers, rank-one groups, unramified absolute
A1, rational K0, polyhedral skeletonization, shell generating functions,
nearby cycles, vanishing cycles, continuous cohomology, pro-l inertia,
finite-root stacks, infinite root stacks, adic coefficients, Artin stacks,
Iwasawa cohomology, analytic compact support, tame nearby cycles, logarithmic
geometry, semistable nodes, finite-carrier traces, six operations, derived
categories, Morita coefficients, supported comparison, semistable refinement,
subdivided annuli, thickness-two nodal models, exceptional curves, fs log
blow-ups, Fujiwara--Kato acyclicity, costalk support, cellular Morita data,
incidence diagrams, integer-cut models, coarse support diagrams, minimal
diagonal kernels.

## Adding future papers

Create one lowercase, search-friendly directory directly under the repository
root for each manuscript. Every paper directory should contain:

1. a `README.md` with `Main content`, `Scope and limitations`, and the
   paper-specific summary, together with the title, status, citation
   suggestion, and build instructions;
2. the stable source file(s), normally `.tex` or `.md`;
3. the latest compiled PDF when one is available.

Then add the same two summary sections to that paper's entry in this root
README, and add only new search terms to the merged keyword index above. Keep
review reports, temporary compilation folders, and unrelated drafts outside
the published paper directory unless they are intentionally part of that
paper's public record.

## License and attribution

Unless a file states otherwise, the original manuscript text, PDFs, LaTeX
source, and README material in this repository are released under the
[Creative Commons Attribution 4.0 International license (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
You may copy, redistribute, translate, adapt, and reuse them, including
commercially, provided that you provide appropriate attribution, link to the
license, and
indicate changes. Third-party works cited by a paper retain their own
licenses.

This collection contains research manuscripts rather than Lean-certified
formalizations. Mathematical claims should be independently checked before
being relied upon.
