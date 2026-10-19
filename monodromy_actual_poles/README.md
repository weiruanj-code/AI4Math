# Contact Reconstruction and Spectral Balance for Surface Singularities with a Multiple Smooth Tangent Cone

## Main content

This paper studies the family of surface germs
\(f=g_e^r+h_{er+1}\), with \(e\ge 3\) and \(r\ge 2\). The monodromy characteristic polynomial and the local topological zeta function each reconstruct the degree parameters and the full finite contact profile. The paper also proves a spectral balance, compares monodromy representations, and analyzes contact collisions.

For this family, the explicit formulas give actual simple poles and twisted holomorphy statements. The source is [monodromy_actual_poles.tex](monodromy_actual_poles.tex). The compiled [PDF](monodromy_actual_poles.pdf) has 18 pages and was built with XeLaTeX on October 19, 2026.

The independent verification scripts use only the Python standard library:

- [verify_audited_compression.py](computations/verify_audited_compression.py)
- [verify_contact_extensions.py](computations/verify_contact_extensions.py)

Both scripts passed on October 19, 2026. They verify finite formal contact-data calculations; such data do not guarantee geometric realizability, and the scripts do not replace the mathematical proofs.

## Scope and limitations

The results apply to \(f=g_e^r+h_{er+1}\), \(e\ge 3\), \(r\ge 2\), where \(C=V(g_e)\subset\mathbb P^2\) is smooth and \(H=V(h_{er+1})\) is smooth at every point of the finite set \(C\cap H\). Reconstruction of the two invariants, spectral balance, actual simple poles, and twisted holomorphy are conclusions for this stated family.

These results do not establish a general monodromy conjecture and do not give a complete classification of non-semisimple monodromy. Finite formal contact data alone do not guarantee that the corresponding geometry is realizable.

## Reproduction

Run these commands from this directory.

Two-pass XeLaTeX compilation:

```text
xelatex -interaction=nonstopmode -halt-on-error monodromy_actual_poles.tex
xelatex -interaction=nonstopmode -halt-on-error monodromy_actual_poles.tex
```

Standard-library verification:

```text
python -B computations/verify_audited_compression.py
python -B computations/verify_contact_extensions.py
```

## AI assistance and license

This mathematical paper was prepared with the assistance of artificial intelligence. The work is released under the [CC BY 4.0 license](../LICENSE).
