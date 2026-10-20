"""Exact diagnostics for the root block and its formal contact normalization.

For D = er+k this script checks the proposed block

    alpha_j = (3r+k)/(rD) + j/D,   0 <= j < D,

and the elementary order bookkeeping attached to formal contact partitions.
It also searches a finite parameter box for zeros of the contact correction
numerator.  These are arithmetic diagnostics only: no geometric realization,
Riemann--Roch, period, resolution, or Bernstein--Sato assertion is made.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Iterable


COMPUTATIONS_DIR = Path(__file__).resolve().parent

E_RANGE = range(3, 11)
R_RANGE = range(2, 6)
K_RANGE = range(1, 7)

CANCEL_E_RANGE = range(3, 15)
CANCEL_R_RANGE = range(2, 8)
CANCEL_K_RANGE = range(1, 17)
CANCEL_Q_RANGE = range(2, 31)


def require(condition: bool, message: str) -> None:
    """Raise an explicit failure; this remains active under ``python -O``."""

    if not condition:
        raise RuntimeError(message)


def fraction_text(value: Fraction) -> str:
    """Render a Fraction without a redundant denominator 1."""

    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def make_partition(total: int, seed: int) -> list[int]:
    """Make a deterministic positive partition of ``total``."""

    require(total >= 1, f"partition total must be positive: {total}")
    if total == 1:
        return [1]
    part_count = 2 + seed % min(5, total - 1)
    state = (seed ^ 0x5DEECE66D) & 0x7FFFFFFF
    parts: list[int] = []
    remaining = total
    for index in range(part_count - 1):
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        slots_after = part_count - index - 1
        largest = remaining - slots_after
        part = 1 + state % largest
        parts.append(part)
        remaining -= part
    parts.append(remaining)
    require(len(parts) == part_count and all(part > 0 for part in parts), "invalid generated partition")
    require(sum(parts) == total, "generated partition sum mismatch")
    return parts


def formal_partitions(e: int, r: int, k: int) -> dict[str, list[int]]:
    """Return formal contact partitions; no geometric realization is assumed."""

    D = e * r + k
    total = e * D
    seed = 1009 * e + 101 * r + k
    partitions = {
        "all_ones": [1] * total,
        "one_contact": [total],
        "e_equal_contacts": [D] * e,
        "deterministic_partition": make_partition(total, seed),
    }
    for name, partition in partitions.items():
        require(partition and all(q > 0 for q in partition), f"nonpositive {name} partition")
        require(sum(partition) == total, f"partition sum failed for {name} at {(e, r, k)}")
    return partitions


def root_block(e: int, r: int, k: int) -> list[dict[str, object]]:
    """Check the root-block parameters for one (e,r,k)."""

    require(e >= 3 and r >= 2 and k >= 1, f"invalid root parameters {(e, r, k)}")
    D = e * r + k
    alpha_zero = Fraction(3 * r + k, r * D)
    b = Fraction(1, r)
    rows: list[dict[str, object]] = []
    for j in range(D):
        alpha_j = alpha_zero + Fraction(j, D)
        a_j = Fraction(3 + j - e, D)
        require(a_j + b == alpha_j, f"root sum failed at {(e, r, k, j)}")
        require(Fraction(j, D) < 1, f"root shift failed at {(e, r, k, j)}")
        require(a_j < 1, f"root a<1 failed at {(e, r, k, j)}: {a_j}")
        if j <= e - 3:
            require(a_j <= 0, f"nonpositive root range failed at {(e, r, k, j)}: {a_j}")
        if j >= e - 2:
            require(a_j > 0 and a_j.denominator != 1, f"positive noninteger root failed at {(e, r, k, j)}: {a_j}")
        rows.append(
            {
                "j": j,
                "alpha": fraction_text(alpha_j),
                "a": fraction_text(a_j),
                "b": fraction_text(b),
            }
        )
    return rows


def triangular_roots(e: int, r: int, k: int) -> tuple[list[Fraction], dict[str, int | Fraction]]:
    """Check the two-index triangular block and its classical endpoint."""

    require(e >= 3 and r >= 2 and k >= 1, f"invalid triangular parameters {(e, r, k)}")
    g = gcd(r, k)
    D = e * r + k
    N = r * D // g
    nu = (3 * r + k) // g
    require((r * D) % g == 0 and (3 * r + k) % g == 0, "triangular divisibility failed")
    alpha_R = Fraction(3 * r + k, r * D)
    values: list[Fraction] = []
    pair_count = 0
    for ell in range(r - 1):
        for j in range(D):
            if Fraction(ell, r) + Fraction(j, D) >= 1:
                continue
            pair_count += 1
            m_numerator = ell * D + j * r
            require(m_numerator % g == 0, f"triangular m divisibility failed at {(e, r, k, ell, j)}")
            m = m_numerator // g
            require(0 <= m < N, f"triangular m range failed at {(e, r, k, ell, j)}")
            alpha = Fraction(nu + m, N)
            expected_alpha = alpha_R + Fraction(ell, r) + Fraction(j, D)
            require(alpha == expected_alpha, f"triangular alpha failed at {(e, r, k, ell, j)}")
            A_j = Fraction(3 + j - e, D)
            B_j = Fraction(ell + 1, r)
            require(A_j + B_j == alpha and alpha > 0, f"triangular Euler sum failed at {(e, r, k, ell, j)}")
            require(0 < B_j < 1, f"triangular B range failed at {(e, r, k, ell, j)}")
            if A_j > 0:
                require(A_j < 1 and A_j.denominator != 1, f"triangular A range failed at {(e, r, k, ell, j)}")
            values.append(alpha)

    classical_ell = r - 1
    classical_j = e - 3
    classical_sum = Fraction(classical_ell, r) + Fraction(classical_j, D)
    require(classical_sum < 1, f"classical triangular point is outside simplex at {(e, r, k)}")
    classical_numerator = classical_ell * D + classical_j * r
    require(classical_numerator % g == 0, f"classical m divisibility failed at {(e, r, k)}")
    classical_m = classical_numerator // g
    require(classical_m < N, f"classical m is not below N at {(e, r, k)}")
    classical_alpha = Fraction(nu + classical_m, N)
    require(classical_alpha == 1, f"classical alpha failed at {(e, r, k)}: {classical_alpha}")
    require(Fraction(3 + classical_j - e, D) == 0, f"classical A failed at {(e, r, k)}")
    require(Fraction(classical_ell + 1, r) == 1, f"classical B failed at {(e, r, k)}")

    return values, {
        "pair_count": pair_count,
        "distinct_count": len(set(values)),
        "classical_m": classical_m,
        "N": N,
        "nu": nu,
    }


def order_value(D: int, ell: int, q: int, d: int, n: int) -> int:
    """Compute the normalized numerator order and require integrality."""

    numerator = D * (n + 1) - ell * q - d
    require(numerator % d == 0, f"order numerator not divisible by d: {(D, ell, q, d, n)}")
    return numerator // d


def check_partition_normalization(
    e: int,
    r: int,
    k: int,
    j: int,
    partition: list[int],
) -> dict[str, int | bool]:
    """Check all contact orders and the degree lower bound for one partition."""

    D = e * r + k
    require(sum(partition) == e * D, f"partition total failed at {(e, r, k)}")
    ell = j + 3 - e
    require(j >= e - 2 and ell > 0, f"root-block index required: {(e, r, k, j)}")
    n_values: list[int] = []
    order_checks = 0
    for q in partition:
        d = gcd(D, q)
        n = (ell * q) // D
        require(
            n * D <= ell * q < (n + 1) * D,
            f"floor normalization failed at {(e, r, k, j, q)}",
        )
        order_n = order_value(D, ell, q, d, n)
        order_nm1 = order_value(D, ell, q, d, n - 1)
        require(order_n >= 0, f"normalized order is negative at {(e, r, k, j, q)}")
        require(order_nm1 < 0, f"n-1 order is not negative at {(e, r, k, j, q)}")
        n_values.append(n)
        order_checks += 1

    degree_L = e * j - sum(n_values)
    require(degree_L >= e * (e - 3), f"degree bound failed at {(e, r, k, j)}")
    e3_zero_degree = e == 3 and degree_L == 0
    if e3_zero_degree:
        for q, n in zip(partition, n_values):
            require((j * q) % D == 0, f"e=3 divisibility failed at {(r, k, j, q)}")
        if j > 0:
            require(any(n >= 1 for n in n_values), f"e=3 missing positive n at {(r, k, j)}")
            for q, n in zip(partition, n_values):
                d = gcd(D, q)
                require(
                    order_value(D, j, q, d, n - 1) == -1,
                    f"e=3 exact -1 order failed at {(r, k, j, q)}",
                )

    return {
        "degree_L": degree_L,
        "order_checks": order_checks,
        "e3_zero_degree": e3_zero_degree,
    }


def cancellation_scan() -> dict[str, object]:
    """Search the finite correction numerator box and test its e=3 identity."""

    checked = 0
    zero_count = 0
    first_zeros: list[dict[str, object]] = []
    e3_relation_checked = 0
    for e in CANCEL_E_RANGE:
        for r in CANCEL_R_RANGE:
            for k in CANCEL_K_RANGE:
                D = e * r + k
                B = (r - 1) * D + k
                beta = 3 * (r - 1) + k
                h = gcd(k, r - 1)
                for q in CANCEL_Q_RANGE:
                    checked += 1
                    d_q = gcd(gcd(k, r), q)
                    t = gcd(k, q * (r - 1))
                    s_q = -Fraction(q * beta + k, q * B)
                    H_q = r * D * s_q + 3 * r + k
                    G_q = H_q * (t * t - q * h * h) - k * (d_q * d_q + q * (r - 1) - r)
                    if G_q == 0:
                        zero_count += 1
                        if len(first_zeros) < 20:
                            first_zeros.append(
                                {
                                    "e": e,
                                    "r": r,
                                    "k": k,
                                    "q": q,
                                    "H_q": fraction_text(H_q),
                                }
                            )
                    if e == 3:
                        e3_relation_checked += 1
                        require(B == r * beta, f"e=3 B=r beta failed at {(r, k, q)}")
                        require(
                            H_q == -Fraction(D * k, q * beta),
                            f"e=3 H relation failed at {(r, k, q)}: {H_q}",
                        )
                        require(H_q != 0, f"e=3 H unexpectedly zero at {(r, k, q)}")
    return {
        "checked_count": checked,
        "zero_count": zero_count,
        "first_zeros": first_zeros,
        "e3_H_relation_checked_count": e3_relation_checked,
        "e3_H_relation": "H_q = -D*k/(q*beta), with B=r*beta",
    }


def unified_cancellation_family() -> dict[str, object]:
    """Check the divisibility-four cancellation family on a finite box."""

    checked = 0
    family_rows: list[dict[str, object]] = []
    for r in range(3, 16):
        for e in range(3, 25):
            k = r - 1
            D = r * (e + 1) - 1
            if D % 4 != 0:
                continue
            q = D // 4
            checked += 1
            B = (r - 1) * D + k
            beta = 3 * (r - 1) + k
            require(B == k * (4 * q + 1), f"unified B identity failed at {(e, r)}")
            require(beta == 4 * k, f"unified beta identity failed at {(e, r)}")
            alpha_q = Fraction(q * beta + k, q * B)
            alpha_R = Fraction(3 * r + k, r * D)
            require(alpha_q == Fraction(1, q), f"unified alpha_q failed at {(e, r)}")
            require(alpha_q - alpha_R == Fraction(1, r * D), f"unified alpha gap failed at {(e, r)}")
            t = gcd(k, q * (r - 1))
            require(D == 4 * q and t == k, f"unified T gcd failed at {(e, r)}")
            require(q * B // t == q * (4 * q + 1), f"unified N failed at {(e, r)}")
            require((q * beta + k) // t == 4 * q + 1, f"unified nu failed at {(e, r)}")
            contact_a = Fraction(D * alpha_q - 3, k)
            contact_b = Fraction(1, q)
            contact_c = -Fraction(r * (q * (e - 3) + D), q * B)
            require(
                (contact_a, contact_b, contact_c) == (Fraction(1, k), Fraction(1, q), -Fraction(1, k)),
                f"unified contact Euler failed at {(e, r)}",
            )

            H_minus_one_q = r * D * (-Fraction(1, q)) + 4 * r - 1
            require(H_minus_one_q == -1, f"unified H(-1/q) failed at {(e, r)}")
            require(e * D - q - 2 > e * (e - 3), f"unified degree margin failed at {(e, r)}")

            for s in (Fraction(0), Fraction(1, 7), Fraction(1), Fraction(2)):
                H = r * D * s + 4 * r - 1
                K = k * (4 * q + 1) * (q * s + 1)
                d_q = gcd(gcd(k, r), q)
                G = H * (t * t - q * k * k) - k * (d_q * d_q + q * (r - 1) - r)
                require(
                    G == -k * k * (q - 1) * (H + 1),
                    f"unified G identity failed at {(e, r, s)}",
                )
                require(K != 0, f"unified K vanished at {(e, r, s)}")
                ratio = G / K
                expected_ratio = -Fraction(4 * r * k * (q - 1), 4 * q + 1)
                require(ratio == expected_ratio, f"unified G/K failed at {(e, r, s)}: {ratio}")

            family_rows.append(
                {
                    "e": e,
                    "r": r,
                    "k": k,
                    "D": D,
                    "q": q,
                    "alpha_q": fraction_text(alpha_q),
                    "T": [q, q, 1],
                    "N": q * (4 * q + 1),
                    "nu": 4 * q + 1,
                }
            )

    example_values, example_data = triangular_roots(6, 3, 2)
    extra_values = [Fraction(1, 6), Fraction(1, 5), Fraction(1)]
    require(len(set(example_values)) == 34, "requested triangular example count failed")
    require(all(value not in set(example_values) for value in extra_values), "requested extra root collision")
    require(len(set(example_values).union(extra_values)) == 37, "requested total distinct count failed")

    return {
        "checked_count": checked,
        "family_rows": family_rows,
        "example_e6_r3_k2": {
            "D": 20,
            "triangle_distinct_count": len(set(example_values)),
            "extra_values": [fraction_text(value) for value in extra_values],
            "total_distinct_count": len(set(example_values).union(extra_values)),
            "classical_data": example_data,
        },
        "identities": {
            "H": "r*D*s+4r-1",
            "K": "k*(4q+1)*(qs+1)",
            "G": "-k^2*(q-1)*(H+1)",
            "G_over_K": "-4*r*k*(q-1)/(4q+1)",
            "contact_Euler": ["1/k", "1/q", "-1/k"],
            "T": ["q", "q", "1"],
        },
    }


def build_report() -> dict[str, object]:
    """Run the finite root-block, partition, and cancellation checks."""

    parameter_count = 0
    root_block_count = 0
    partition_count = 0
    normalization_count = 0
    e3_zero_degree_count = 0
    e3_divisibility_contact_count = 0
    e3_exact_minus_one_count = 0
    sample_partitions: dict[str, list[int]] | None = None
    triangular_parameter_count = 0
    triangular_pair_count = 0
    triangular_distinct_count = 0
    triangular_classical_count = 0
    triangular_example_values: list[Fraction] | None = None
    triangular_example_data: dict[str, int | Fraction] | None = None

    for e in E_RANGE:
        for r in R_RANGE:
            for k in K_RANGE:
                parameter_count += 1
                rows = root_block(e, r, k)
                root_block_count += len(rows)
                partitions = formal_partitions(e, r, k)
                partition_count += len(partitions)
                for name, partition in partitions.items():
                    for row in rows[e - 2 :]:
                        j = int(row["j"])
                        result = check_partition_normalization(e, r, k, j, partition)
                        normalization_count += int(result["order_checks"])
                        if result["e3_zero_degree"]:
                            e3_zero_degree_count += 1
                            e3_divisibility_contact_count += len(partition)
                            if j > 0:
                                e3_exact_minus_one_count += len(partition)
                if (e, r, k) == (4, 2, 2):
                    sample_partitions = partitions

    for e in range(3, 11):
        for r in range(2, 8):
            for k in range(1, 9):
                triangular_parameter_count += 1
                values, data = triangular_roots(e, r, k)
                triangular_pair_count += int(data["pair_count"])
                triangular_distinct_count += int(data["distinct_count"])
                triangular_classical_count += 1
                if (e, r, k) == (6, 3, 2):
                    triangular_example_values = values
                    triangular_example_data = data

    require(sample_partitions is not None, "requested partition sample was not generated")
    sample_e4 = root_block(4, 2, 2)
    sample_e3 = root_block(3, 2, 1)
    require(
        [row["alpha"] for row in sample_e4]
        == ["2/5", "1/2", "3/5", "7/10", "4/5", "9/10", "1", "11/10", "6/5", "13/10"],
        "e=4,r=2,k=2 root sample mismatch",
    )
    require(
        [row["alpha"] for row in sample_e3]
        == ["1/2", "9/14", "11/14", "13/14", "15/14", "17/14", "19/14"],
        "e=3,r=2,k=1 root sample mismatch",
    )
    require(triangular_example_values is not None and triangular_example_data is not None, "triangular example missing")

    cancellation = cancellation_scan()
    unified = unified_cancellation_family()
    report: dict[str, object] = {
        "root_sweep": {
            "e": [E_RANGE.start, E_RANGE.stop - 1],
            "r": [R_RANGE.start, R_RANGE.stop - 1],
            "k": [K_RANGE.start, K_RANGE.stop - 1],
            "parameter_count": parameter_count,
            "root_block_count": root_block_count,
            "formal_partition_count": partition_count,
            "normalization_contact_count": normalization_count,
            "e3_zero_degree_case_count": e3_zero_degree_count,
            "e3_divisibility_contact_count": e3_divisibility_contact_count,
            "e3_exact_minus_one_count": e3_exact_minus_one_count,
        },
        "triangular_sweep": {
            "e": [3, 10],
            "r": [2, 7],
            "k": [1, 8],
            "parameter_count": triangular_parameter_count,
            "candidate_pair_count": triangular_pair_count,
            "distinct_alpha_count_sum": triangular_distinct_count,
            "classical_endpoint_checked_count": triangular_classical_count,
            "example_e6_r3_k2": {
                "D": 20,
                "triangle_distinct_count": len(set(triangular_example_values)),
                "classical_data": triangular_example_data,
            },
        },
        "requested_root_examples": {
            "e4_r2_k2_D10": {
                "D": 10,
                "alphas": [row["alpha"] for row in sample_e4],
            },
            "e3_r2_k1_D7": {
                "D": 7,
                "alphas": [row["alpha"] for row in sample_e3],
            },
        },
        "requested_partitions_e4_r2_k2": sample_partitions,
        "cancellation_scan": cancellation,
        "unified_cancellation_family": unified,
        "limitation": (
            "Finite exact arithmetic only. Formal contact partitions are not claimed "
            "to be geometrically realizable. The checks do not prove Riemann--Roch, "
            "cycles, periods, resolutions, nonzero residues, or Bernstein--Sato roots; "
            "zeros in the cancellation scan are only finite-search data."
        ),
    }
    return report


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        dest="json_path",
        type=Path,
        metavar="PATH",
        help="also write the JSON report under this computations folder",
    )
    return parser.parse_args(argv)


def report_path(path: Path) -> Path:
    """Resolve a report path and keep it inside the computations directory."""

    resolved = (COMPUTATIONS_DIR / path if not path.is_absolute() else path).resolve()
    try:
        resolved.relative_to(COMPUTATIONS_DIR)
    except ValueError as exc:
        raise RuntimeError(f"--json path must be under {COMPUTATIONS_DIR}: {path}") from exc
    return resolved


def main(argv: Iterable[str] | None = None) -> int:
    """Run checks, print JSON, and optionally write the report."""

    args = parse_args(argv)
    try:
        report = build_report()
        rendered = json.dumps(report, indent=2, sort_keys=True)
        if args.json_path is not None:
            report_path(args.json_path).write_text(rendered + "\n", encoding="utf-8")
    except (OSError, RuntimeError, ZeroDivisionError) as exc:
        raise SystemExit(f"check failed: {exc}") from exc

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
