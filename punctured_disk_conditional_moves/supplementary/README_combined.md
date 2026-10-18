# Combined computational supplement

This archive accompanies the merged punctured-disk manuscript.  It contains
the exact finite controls for the conditional local moves and the positive-ray
non-reentry calculations.  The archive is self-contained: the ray programs'
`PREDECESSOR` imports resolve to the sibling move directory inside this
archive, so no checkout of the surrounding project is required.

The package was validated with Python **3.12.10**.  The scripts use the Python
standard library only; no third-party package is required.  The commands below
are run from the extracted archive root.  Every recomputed certificate is
written below `results/`, leaving the packaged certificates unchanged.

## Independent smoke checks

These are the two checks used for the package validation.  Both ray checks
explicitly insert the packaged sibling directories, so `-I` makes the run
independent of user-site packages and the caller's import path.

```text
python -c "from pathlib import Path; Path('results').mkdir(exist_ok=True)"
python -I papers/punctured_disk_positive_rays/computations/audit_minor_coordinates.py --n-min 3 --n-max 10 --output results/audit_minor_coordinates_n3_n10.json
python -I papers/punctured_disk_positive_rays/computations/verify_wedge_structure.py --n-min 3 --n-max 6 --output results/wedge_structure_n3_n6.json
```

Expected output is `all_cases_pass: True` in both runs.  The first run checks
the exact diagonal separating-minor coordinate identity for every `n=3,...,10`
case.  The second checks the explicit layered paths, separator sizes, and
actual graph separation for `n=3,...,6`.

## Move controls

The following commands rerun the exact move-side controls.  They use explicit
result paths so the cached JSON files under `papers/.../computations` are not
overwritten.

```text
python papers/punctured_disk_conditional_moves/computations/verify_local_controls.py --input papers/punctured_disk_conditional_moves/notes/local_graphs.json --output results/local_control_certificate.json
python papers/punctured_disk_conditional_moves/computations/verify_uniform_path_table.py --output results/path_table_certificate.json
python papers/punctured_disk_conditional_moves/computations/verify_uniform_minors.py --output results/uniform_minors_certificate.json
python papers/punctured_disk_conditional_moves/computations/verify_uniform_transform.py --output results/uniform_transform_certificate.json
python papers/punctured_disk_conditional_moves/computations/verify_locality_and_inverse.py --output results/locality_inverse_certificate.json
python papers/punctured_disk_conditional_moves/computations/verify_feature_minor_formulas.py --output results/feature_minor_certificate.json
python papers/punctured_disk_conditional_moves/computations/verify_three_sided_formula.py --output results/three_sided_formula_certificate.json
python papers/punctured_disk_conditional_moves/computations/verify_n7_closed_move.py --output results/n7_closed_move_certificate.json
```

The move-side cached certificates record the finite ranges used in the
manuscript: path tables through `n=30`, the layered minor check through
`n=14`, recovery and source transforms through `n=10`, and the local controls
and `n=7` exact checks described in the computation README.

## Ray controls

The exact ground-state and ray probes are available with the same independent
layout.  Their output paths should also point into `results/`:

```text
python -I papers/punctured_disk_positive_rays/computations/verify_ground_state_criterion.py --output results/ground_state_criterion_certificate.json
python -I papers/punctured_disk_positive_rays/computations/scan_reentry_exact.py --output results/reentry_exact_scan_certificate.json --checkpoint results/reentry_exact_scan_checkpoint.json
python -I papers/punctured_disk_positive_rays/computations/probe_n7_symbolic_ray.py --output results/n7_symbolic_ray_certificate.json
```

The packaged `wedge_witness_certificate.json` is intentionally labelled by
its recorded status.  Its `run_status` is `timed_out`: all completed witness
cases are `n=3,...,16`, and `n=17,...,20` were not completed.  The certificate
therefore does not claim a complete `n=17` run.  To request a fresh bounded
run, keep both output files outside the package and make the range explicit:

```text
python -I papers/punctured_disk_positive_rays/computations/verify_wedge_witnesses.py --n-min 3 --n-max 16 --parity-budget 0 --time-limit 300 --output results/wedge_witness_n3_n16.json --checkpoint results/wedge_witness_n3_n16.checkpoint.json
```

The witness program is a finite diagnostic.  It does not replace the general
planar uniqueness proof in the manuscript.

## Archive layout and manifest

The sibling layout is preserved under `papers/`:

```text
papers/punctured_disk_conditional_moves/computations/   move scripts and certificates
papers/punctured_disk_conditional_moves/notes/           local_graphs.json
papers/punctured_disk_positive_rays/computations/       ray scripts and certificates
```

Every `.py` file in both computation directories is included, together with
every non-checkpoint `.json` certificate/output and both computation READMEs.
Checkpoint files and bytecode caches are omitted.  `SHA256SUMS.txt` contains
the SHA-256 digest of every other file in the archive.  The sibling
`punctured_disk_moves_and_rays_supplement.zip.sha256` records the digest of the
ZIP itself.
