# Supplementary verification files

This directory contains two supplementary files for the manuscript:

- `verify_counterexample_independent.py` independently verifies the published controls and candidate counterexamples.
- `independent_counterexample_certificate.json` is the certificate produced by that script.

The files were tested with Python 3.12.10. The script uses only the Python standard library (`json` and `pathlib`), with no external downloads or dependencies.

From the project manuscript directory, run:

```text
python supplementary/verify_counterexample_independent.py
```

From this supplementary directory, run:

```text
python verify_counterexample_independent.py
```

The script writes its output certificate JSON beside the script. Rerunning it overwrites that file.

Expected candidate tuples `(size, cover_count, residue_1009)` are:

- `w=110100110110001100`: `(288, 882, 238)`
- `w=110110001101001100`: `(288, 882, 676)`

Both published controls have size 27 and determinant `95869805`.
