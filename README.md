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
└── universal_quadratic_pgl2_orbit_shells/
    ├── README.md                     # paper summary and search metadata
    ├── universal_quadratic_pgl2_orbit_shells.tex
    └── universal_quadratic_pgl2_orbit_shells.pdf
```

## Paper index

### From Represented $PGL_2$ Orbit Shells to Rank-One Orientation Reciprocity

**Quadratic Residual Towers, Haar--Frobenius Comparison, and the Unramified
Absolute-$A_1$ Theorem**

Folder: [`universal_quadratic_pgl2_orbit_shells/`](universal_quadratic_pgl2_orbit_shells/)

#### Main content

The paper studies represented positive-loop orbit shells in a universal
quadratic $PGL_2$ family. It constructs a finite residual tower whose first
layer is the norm-one torus, compares quadratic order lattices with orbit
sheaves, and relates quotient Haar masses to compact geometric-Frobenius
traces. It then derives rank-one orientation reciprocity for the normalized
orbital generating series and a rational $K_0$ shadow in the unramified
absolute-$A_1$ setting.

#### Scope and limitations

The strongest geometric statements concern the universal quadratic
equal-characteristic loop family and represented fppf orbit sheaves. The paper
does not claim a general affine-Springer quotient, cross-shell incidence
theory, convolution theorem, Rees completion, or unrestricted global
tropical realization. Outside the saturated $PGL_2$ case, the extension is an
explicit orbit-summed classification and rational $K_0$ interpolation, not a
relative represented-shell theorem.

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
categories.

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
