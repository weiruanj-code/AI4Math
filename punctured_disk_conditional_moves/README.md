# Uniform conditional moves and positivity thresholds in punctured-disk electrical networks

This directory contains the unified merged manuscript for the result. It is the publication-facing merged paper; the separate `../punctured_disk_positive_rays/` work directory is development material, not a separately published paper. The manuscript and build are dated 2026-10-18.

## Main content

For every `n >= 3`, the paper constructs the four prescribed opposite-side conditional moves for punctured-disk electrical networks. The moves preserve the full response, including the observed center. A positive source admits the prescribed positive target if and only if the signed center-coordinate minors are all positive. Along positive skeleton rays—natural-edge rays and spike rays—the positive realization set is a single initial interval `(0, epsilon_*)` with an explicit threshold. At a finite endpoint, the limiting network is obtained by deleting center edges.

## Scope and limitations

The results apply to the prescribed graph family, natural-edge or spike rays, and positive sources with the full response retained. They do not claim arbitrary network rewrites or arbitrary parameter paths. Finite computations provide checks and supporting evidence; they do not replace a general proof or independent formalization.

## Files

- [TeX manuscript](punctured_disk_conditional_moves.tex)
- [Compiled PDF (27 pages)](punctured_disk_conditional_moves.pdf)
- [Seven-ring move figure source](figures/seven_ring_move.tex)
- [Combined supplementary archive](supplementary/punctured_disk_moves_and_rays_supplement.zip)
- [Archive SHA-256 file](supplementary/punctured_disk_moves_and_rays_supplement.zip.sha256)
- [Combined supplement README](supplementary/README_combined.md)
- [Combined SHA-256 manifest](supplementary/SHA256SUMS_combined.txt)

## Build

The manuscript was compiled on 2026-10-18. From this directory, run XeLaTeX twice:

```sh
xelatex -interaction=nonstopmode -halt-on-error punctured_disk_conditional_moves.tex
xelatex -interaction=nonstopmode -halt-on-error punctured_disk_conditional_moves.tex
```

The source requires TikZ.

## AI assistance

This manuscript was prepared with assistance from artificial intelligence. The paper’s acknowledgment credits humanity’s textual record, mathematicians throughout history, researchers who advanced neural networks, and the OpenAI team for the training and development of the models used in preparing it.

Licensed under [CC BY 4.0](../LICENSE).
