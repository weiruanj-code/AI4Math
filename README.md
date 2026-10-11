# AI4Math

An open collection of AI-assisted mathematical research manuscripts. Each paper
has its own top-level directory. Publication index updated: October 11, 2026.
The collection includes completed manuscripts and an explicitly unfinished
research draft; the descriptions below preserve that distinction.

## Paper index

| Paper | Source | PDF |
| --- | --- | --- |
| Relative Quadratic Orbit Shells | [LaTeX](universal_quadratic_pgl2_orbit_shells/universal_quadratic_pgl2_orbit_shells.tex) | [PDF](universal_quadratic_pgl2_orbit_shells/universal_quadratic_pgl2_orbit_shells.pdf) |
| Local Kummer Realizations and Verdier Duality | [LaTeX](three_realization_submission/three_realization_submission.tex) | [PDF](three_realization_submission/three_realization_submission.pdf) |
| Morita Coefficients, Incidence, and Semistable Refinement | [LaTeX](semistable_morita_refinement/semistable_morita_refinement.tex) | [PDF](semistable_morita_refinement/semistable_morita_refinement.pdf) |
| Verdier-Compatible Kernel Skeletonization | [LaTeX](verdier_kernel_skeletonization/verdier_kernel_skeletonization.tex) | [PDF](verdier_kernel_skeletonization/verdier_kernel_skeletonization.pdf) |
| Exceptional and Completed Root Kernel Calculus: A Single-Transition Problem (research draft) | [LaTeX](global_root_kernel_calculus/global_root_kernel_calculus.tex) | [PDF](global_root_kernel_calculus/global_root_kernel_calculus.pdf) |
| Supported Morita Descent for Semistable Curves | [LaTeX](supported_morita_descent/supported_morita_descent.tex) | [PDF](supported_morita_descent/supported_morita_descent.pdf) |
| Weighted Tropical Chow Reconstruction for Space Curves | [LaTeX](tropical_chow_reconstruction/weighted_tropical_chow_reconstruction.tex) | [PDF](tropical_chow_reconstruction/weighted_tropical_chow_reconstruction.pdf) |
| Cyclic Symmetry and Failure of Block-Permutation Invariance in Dexter Intervals | [LaTeX](dexter_block_permutation/dexter_block_permutation.tex) | [PDF](dexter_block_permutation/dexter_block_permutation.pdf) |

### Relative Quadratic Orbit Shells

**Main content:** Quadratic positive-loop orbit shells, residual towers, and
orientation coefficients in a represented rank-one family.

**Scope and limitations:** The specified quadratic family and represented
orbit sheaves; no unrestricted affine-Springer or global convolution theorem.

### Local Kummer Realizations and Verdier Duality

**Main content:** Local comparisons of root, nearby-cycle, and tube cohomology,
continuous inertia cochains, finite-root traces, and supported Verdier partners.

**Scope and limitations:** The stated semistable chart and selected adic
coefficient source; no unrestricted global log/root equivalence.

### Morita Coefficients, Incidence, and Semistable Refinement

**Main content:** Supported Morita coefficients, branch incidence, and
comparisons under the specified semistable subdivisions.

**Scope and limitations:** The paper's fixed models and coefficient/support
conditions; no arbitrary global model-independent kernel calculus.

### Verdier-Compatible Kernel Skeletonization

**Main content:** One-sided kernel descent for anchored semistable models,
compatible with convolution, units, and geometric Verdier mates.

**Scope and limitations:** The specified generated source and anchored
models; no general global root-kernel source or unrestricted descent.

### Exceptional and Completed Root Kernel Calculus: A Single-Transition Problem

**Main content:** An unfinished research draft isolating a unit, convolution,
and localization problem on one complete nodal support and one root transition.
It records local calculations and the obstruction to ordinary distribution gluing.

**Scope and limitations:** The kernel calculus is not constructed. The recorded
diagrams do not solve the single-transition problem, and no global realization
theorem is claimed.

### Supported Morita Descent for Semistable Curves

**Main content:** Geometric rational nearby-module support profiles on proper
nodal curves, descent under actual integer-cut refinements, and a one-sided
kernel counit giving strong convolution and Morita-Verdier comparisons.
Extensions cover curve rectangles and specified finite etale support spans.

**Scope and limitations:** Fixed trait, specified constructibility profiles,
geometric rational coefficients, and kernel products over the residue field.
Independent contraction of arbitrary coupled-kernel endpoints fails;
higher-dimensional modifications and global root shriek sources are excluded.
Frozen companion inputs remain in the local project archive; the public release
contains this manuscript, with links to the current companion papers.

### Weighted Tropical Chow Reconstruction for Space Curves

**Main content:** Injectivity of the weighted tropical Chow transform on finite
rational polyhedral one-chains with signed weights, yielding reconstruction of
space curves in R^4/R1 without a fan hypothesis. The proof uses affine-span
separation, local incidence cones, and thin-band length-measure recovery.

**Scope and limitations:** Finite polyhedral structures in the specified
finite-coordinate tropical tori, with weights and positions retained. No claim
for infinitely many cells, higher-dimensional sources, or extra boundary strata.

### Cyclic Symmetry and Failure of Block-Permutation Invariance in Dexter Intervals

**Main content:** Cyclic block rotation preserves derived categories over every
field, while two 288-element Dexter intervals obstruct arbitrary block
permutation. The specified six permutations form two cyclic derived classes;
boundary attachment explains the obstruction. An independent Python verifier
and complete certificate are included in [supplementary](dexter_block_permutation/supplementary/README.md).

**Scope and limitations:** The stated Dexter intervals and boundary comparisons.
General block-permutation invariance is disproved, and minimality of the
counterexample is not claimed. The computational certificate does not constitute
a Lean formalization of the paper.

## Search keywords

This is one merged index. Future papers add only terms not already present.

`PGL2`, `PGL_2`, orbital integrals, affine Springer fibers, quadratic orders,
positive loop groups, norm-one torus, Kummer realizations, Kummer local
systems, Kummer torsors, Haar measure, geometric Frobenius, Verdier duality,
orientation reciprocity, residual towers, rank-one groups, unramified absolute
A1, rational K0, polyhedral skeletonization, shell generating functions,
nearby cycles, vanishing cycles, continuous cohomology, pro-l inertia,
continuous cochain algebras, rational unipotent coefficients,
finite-root vector-bundle carriers, finite-root stacks, infinite root stacks,
adic coefficients, Artin stacks, Iwasawa cohomology, analytic compact support,
tame nearby cycles, logarithmic geometry, semistable nodes, finite-carrier
traces, six operations, derived categories, Morita coefficients, supported
comparison, semistable refinement, subdivided annuli, thickness-two nodal
models, exceptional curves, fs log blow-ups, Fujiwara--Kato acyclicity,
costalk support, cellular Morita data, incidence diagrams, integer-cut models,
coarse support diagrams, minimal diagonal kernels, kernel skeletonization,
anchored semistable models, one-sided kernel descent, generated kernel sources,
complete inverse-image supports, geometric unipotent nearby coefficients,
completed root kernel calculus, dual-unit trace systems, distribution gluing
obstruction, constructibility profiles, loop holonomy, finite etale support
spans, tropical Chow transform, tropical space curves, weighted reconstruction,
signed polyhedral chains, Tripoli reconstruction problem, thin-band measures,
Dyck paths, Dexter order, Dexter intervals, cyclic block rotation,
block-permutation counterexample, incidence algebras, integral Euler polynomials,
boundary pullbacks, tilting complexes, pyramid blocks, reproducible certificates.

## Adding future papers

Use one top-level paper directory containing its README, stable LaTeX source,
and compiled PDF. Add its main content and scope to this index, and append only
new search keywords. Publish required supplementary verification files with the
paper; keep local research notes, reviews, build intermediates, and frozen
companion manuscripts in the local workspace unless separately authorized.

## License and attribution

Original manuscript text, PDFs, LaTeX source, README material, and original
supplementary files are released under [CC BY 4.0](LICENSE). Reuse and adaptation,
including commercial reuse, are allowed with appropriate attribution, a link
to the license, and an indication of changes. Cited third-party works retain
their own licenses.

## Local workspace navigation

The local project was reorganized on October 11, 2026. This repository is
`D:\AIProject\AIformath\papers`; the full workspace also contains
`../PROJECT_INDEX.md`, `../PROJECT_PATHS.json`, `../research/`, `../reviews/`,
and `../archive/`. Those workspace records are not part of this Git repository.

Existing published papers retain their committed source/PDF versions until
their revisions are separately published. The four newly added source/PDF
pairs were compiled together for this release.
