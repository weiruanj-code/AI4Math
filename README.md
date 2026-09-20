# AI4Math

An open collection of AI-assisted mathematical research manuscripts by
YINGFENG JIANG. Each paper lives in its own directory so that source files,
compiled PDFs, notes, and future revisions can be separated cleanly.

## Repository structure

```text
AI4Math/
├── README.md                         # repository-wide index
├── LICENSE                           # CC BY 4.0
└── papers/
    ├── README.md                     # paper-directory conventions
    └── universal_quadratic_pgl2_orbit_shells/
        ├── README.md                 # paper summary and keywords
        ├── universal_quadratic_pgl2_orbit_shells.tex
        └── universal_quadratic_pgl2_orbit_shells.pdf
```

## Paper index

### From Represented $PGL_2$ Orbit Shells to Rank-One Orientation Reciprocity

**Quadratic Residual Towers, Haar--Frobenius Comparison, and the Unramified
Absolute-$A_1$ Theorem**

- Folder: [`papers/universal_quadratic_pgl2_orbit_shells/`](papers/universal_quadratic_pgl2_orbit_shells/)
- Summary: represented quadratic $PGL_2$ orbit shells, residual towers,
  norm-one tori, Haar/Frobenius comparison, orientation reciprocity, and a
  rational $K_0$ shadow for the unramified absolute-$A_1$ case.
- Keywords: `PGL2`, orbital integrals, affine Springer fibers, quadratic
  orders, Kummer local systems, Haar measure, geometric Frobenius, Verdier
  duality, rank-one reciprocity, rational K0.

The paper directory contains the detailed summary, scope, limitations,
citation suggestion, keywords, and compilation instructions.

## Adding future papers

Create one lowercase, search-friendly directory under `papers/` for each
manuscript. Every paper directory should contain:

1. a `README.md` with the title, author, abstract-style summary, status,
   limitations, keywords, citation suggestion, and build instructions;
2. the stable source file(s), normally `.tex` or `.md`;
3. the latest compiled PDF when one is available.

Then add one short entry to this index. Keep review reports, temporary
compilation folders, and unrelated drafts outside the published paper
directory unless they are intentionally part of that paper's public record.

## License and attribution

Unless a file states otherwise, the original manuscript text, PDFs, LaTeX
source, and README material in this repository are released under the
[Creative Commons Attribution 4.0 International license (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
You may copy, redistribute, translate, adapt, and reuse them, including
commercially, provided that you credit the author, link to the license, and
indicate changes. Third-party works cited by a paper retain their own
licenses.

This collection contains research manuscripts rather than Lean-certified
formalizations. Mathematical claims should be independently checked before
being relied upon.

