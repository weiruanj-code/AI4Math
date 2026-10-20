# Uniform Bernstein–Sato Factors and Contact Roots for Surface Germs with a Multiple Smooth Tangent Cone

Date: 20 October 2026

[TeX source](bernstein_sato_contact_roots.tex) · [PDF](bernstein_sato_contact_roots.pdf) · [CC BY 4.0 license](../LICENSE)

The compiled PDF has 17 pages and was built with XeLaTeX on October 20, 2026.

## Main content

This paper studies local Bernstein–Sato polynomials of surface germs whose first two homogeneous layers are

    f = g_e^r + h_D + R_{>D},    D = er + k,

with e ≥ 3, r ≥ 2, k ≥ 1, and with the projective plane curve C = V(g_e) smooth.

The general analytic theorem assumes only that h_D restricted to C is not identically zero. It allows arbitrary convergent analytic higher terms R_{>D}, including singular H = V(h_D), and proves the uniform factor

    product_{j=0}^{D-1} (s + (3r+k)/(rD) + j/D)

in the local polynomial b_{f,0}(s). The manuscript also gives a triangular family of exact roots obtained from holomorphic numerators.

The contact results have narrower hypotheses: they concern the exact two-layer germ f = g_e^r + h_D and require H = V(h_D) to be smooth at every point of C ∩ H. Each actual nontransverse contact of order q ≥ 2 gives an exact contact root

    -[q(3(r-1)+k)+k] / [q((r-1)D+k)].

Under these same two-layer smooth-contact assumptions, every pole of the local topological zeta function is simple and is a root of b_{f,0}. The paper also gives an explicit infinite family in which a contact root lies outside the triangular root set although the corresponding topological pole cancels.

The proofs use compact residue periods, a cyclic cover of the smooth tangent curve, Riemann–Roch, and a weighted Newton calculation.

## Scope and limitations

- The uniform-root theorem is the general analytic result. Its hypotheses do not include the smoothness condition on H used by the contact and topological-zeta statements.
- Contact orders are actual intersection multiplicities, and the contact-root and pole statements are only for the exact two-layer smooth-contact family described above.
- The manuscript proves a factor and selected exact roots; it does not compute or claim the complete local Bernstein–Sato polynomial.
- Finite exact-arithmetic checks are diagnostics for displayed identities. They do not by themselves prove cycles, resolutions, geometric realization, nonzero periods, analytic-unit comparisons, or Bernstein–Sato roots.
- No general conjecture is asserted here beyond the stated theorems and their stated hypotheses.

## Verification scripts

The following existing scripts are the published finite-arithmetic verification set:

- [check_contact_residue_parameters.py](computations/check_contact_residue_parameters.py)

      python computations/check_contact_residue_parameters.py

- [check_arbitrary_gap_parameters.py](computations/check_arbitrary_gap_parameters.py)

      python computations/check_arbitrary_gap_parameters.py

- [check_root_block_parameters.py](computations/check_root_block_parameters.py)

      python computations/check_root_block_parameters.py

Run these commands from this directory without the optional --json argument. All three scripts use exact finite arithmetic only; their successful checks do not establish the geometric or analytic statements listed above, nor do they compute the complete Bernstein–Sato polynomial.

Verification status recorded on 20 October 2026: all three parameter-script commands completed successfully without --json, and the manuscript source check passed.

## Reproducibility

From this directory, run XeLaTeX and repeat the commands until references and citations are stable:

~~~~sh
xelatex -interaction=nonstopmode -halt-on-error bernstein_sato_contact_roots.tex
xelatex -interaction=nonstopmode -halt-on-error bernstein_sato_contact_roots.tex
~~~~

## AI assistance

This mathematical paper was prepared with the assistance of artificial intelligence. The full acknowledgment appears in the manuscript.

## License

The original manuscript text, LaTeX source, and compiled PDF are released under the [CC BY 4.0 license](../LICENSE), subject to the third-party material terms stated there.
