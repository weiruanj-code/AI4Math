"""Exact arithmetic diagnostics for the degree-gap ``k`` extension.

The script checks the parameter identities proposed for

    f = g_e^r + h_{er+k},   e >= 3, r >= 2, k >= 1.

It deliberately tests only the displayed lattice, Euler-parameter, and
rational-function identities.  It does not prove a resolution statement,
existence of the required cycles, geometric realization of a contact
partition, or a Bernstein--Sato root theorem.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Iterable


COMPUTATIONS_DIR = Path(__file__).resolve().parent

E_RANGE = range(3, 15)
R_RANGE = range(2, 8)
K_RANGE = range(1, 17)
Q_RANGE = range(1, 25)

# Rational-function checks use a deliberately smaller product grid.  The
# parameter sweep above is the main finite arithmetic check; this second grid
# keeps the Fraction calculation quick while sampling every exceptional branch
# (q=1 and k=1) repeatedly.
RATIONAL_E = (3, 4, 7, 10, 14)
RATIONAL_R = (2, 3, 5, 7)
RATIONAL_K = (1, 2, 3, 4, 8, 16)
RATIONAL_Q = (1, 2, 3, 4, 7, 12, 24)
RATIONAL_S = (Fraction(0), Fraction(1, 7), Fraction(1), Fraction(2))


def require(condition: bool, message: str) -> None:
    """Raise an explicit failure; this remains active under ``python -O``."""

    if not condition:
        raise RuntimeError(message)


def div(numerator: Fraction | int, denominator: Fraction | int, label: str) -> Fraction:
    """Divide after checking the denominator explicitly."""

    require(denominator != 0, f"zero denominator in {label}")
    return Fraction(numerator) / Fraction(denominator)


def fraction_text(value: Fraction) -> str:
    """Render a Fraction without a redundant denominator 1."""

    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


Vector = tuple[int, int, int]


def add_vectors(*vectors: Vector) -> Vector:
    """Add integer exponent vectors componentwise."""

    require(vectors, "cannot add an empty vector family")
    return tuple(sum(vector[index] for vector in vectors) for index in range(3))  # type: ignore[return-value]


def matrix_row_product(coefficients: tuple[int, ...], rows: tuple[Vector, ...]) -> Vector:
    """Multiply a coefficient row by an integer matrix whose rows are vectors."""

    require(len(coefficients) == len(rows), "coefficient/matrix size mismatch")
    return tuple(
        sum(coefficients[row_index] * rows[row_index][column] for row_index in range(len(rows)))
        for column in range(3)
    )  # type: ignore[return-value]


def determinant(rows: tuple[Vector, Vector, Vector]) -> int:
    """Return a three-by-three integer determinant."""

    (a11, a12, a13), (a21, a22, a23), (a31, a32, a33) = rows
    return (
        a11 * (a22 * a33 - a23 * a32)
        - a12 * (a21 * a33 - a23 * a31)
        + a13 * (a21 * a32 - a22 * a31)
    )


def cross_product(left: Vector, right: Vector) -> Vector:
    """Return the integer cross product left x right."""

    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def gcd_entries(vector: Vector) -> int:
    """Return the nonnegative gcd of the entries of an integer vector."""

    value = gcd(gcd(abs(vector[0]), abs(vector[1])), abs(vector[2]))
    require(value > 0, f"zero lattice vector encountered: {vector}")
    return value


def parameter_data(e: int, r: int, k: int, q: int) -> dict[str, int | Fraction]:
    """Compute and check all integer data for one (e,r,k,q)."""

    require(e >= 3 and r >= 2 and k >= 1 and q >= 1, f"invalid parameters {(e, r, k, q)}")
    a_big = e * r
    d_big = a_big + k
    b_big = (r - 1) * d_big + k
    beta = 3 * (r - 1) + k
    g = gcd(r, k)
    h = gcd(k, r - 1)
    j = gcd(k, r, q)
    t = gcd(k, q * (r - 1))

    require((q * b_big) % t == 0, f"contact N divisibility failed at {(e, r, k, q)}")
    require((q * beta + k) % t == 0, f"contact nu divisibility failed at {(e, r, k, q)}")
    require((r * d_big) % g == 0, f"curve N divisibility failed at {(e, r, k, q)}")
    require((3 * r + k) % g == 0, f"curve nu divisibility failed at {(e, r, k, q)}")

    alpha_zero = Fraction(3, a_big)
    alpha_r = Fraction(3 * r + k, r * d_big)
    alpha_q = Fraction(q * beta + k, q * b_big)

    return {
        "A": a_big,
        "D": d_big,
        "B": b_big,
        "beta": beta,
        "g": g,
        "h": h,
        "j": j,
        "t": t,
        "N_q": q * b_big // t,
        "nu_q": (q * beta + k) // t,
        "N_R": r * d_big // g,
        "nu_R": (3 * r + k) // g,
        "alpha_0": alpha_zero,
        "alpha_R": alpha_r,
        "alpha_q": alpha_q,
    }


def check_lattice_data(e: int, r: int, k: int, q: int) -> dict[str, object]:
    """Independently check the finite torus lattice and all cone indices."""

    data = parameter_data(e, r, k, q)
    a_big = int(data["A"])
    d_big = int(data["D"])
    b_big = int(data["B"])
    beta = int(data["beta"])
    h = int(data["h"])
    j = int(data["j"])
    t = int(data["t"])

    # The rows are the exponents of (u,v,w) in (t,xi,eta).  All F and
    # Jacobian exponents below are obtained by matrix multiplication with
    # this row matrix, so the expected vectors are independent targets.
    u: Vector = (q * (r - 1), -1, -(r - 1))
    v: Vector = (q * k, 0, -k)
    w: Vector = (k, 0, 0)
    exponent_matrix = (u, v, w)
    matrix_index = abs(determinant(exponent_matrix))
    require(matrix_index == k * k, f"torus matrix index failed at {(e, r, k, q)}")

    f_vectors = (
        matrix_row_product((a_big, r, 0), exponent_matrix),
        matrix_row_product((d_big, 1, 0), exponent_matrix),
        matrix_row_product((d_big, 0, q), exponent_matrix),
    )
    expected_f_vectors = (
        (q * b_big, -d_big + k, -b_big),
        (q * b_big, -d_big, -b_big),
        (q * b_big, -d_big, -b_big + k),
    )
    require(
        f_vectors == expected_f_vectors,
        f"F exponent matrix product failed at {(e, r, k, q)}: {f_vectors}",
    )

    volume_vector = add_vectors(
        matrix_row_product((3, 1, 1), exponent_matrix),
        (-1, -1, -1),
    )
    expected_volume = (q * beta + k - 1, -4, -beta - 1)
    require(
        volume_vector == expected_volume,
        f"volume exponent matrix product failed at {(e, r, k, q)}: {volume_vector}",
    )

    e1: Vector = (1, 0, 0)
    e2: Vector = (0, 1, 0)
    e3: Vector = (0, 0, 1)
    R: Vector = (r, k, 0)
    Q: Vector = (0, q, 1)
    T: Vector = (q * (r - 1), q * k, k)
    cone_rows = (
        (e1, e3, T),
        (e1, T, R),
        (e3, Q, T),
        (e2, R, T),
        (e2, T, Q),
    )
    cone_indices = tuple(abs(determinant(rows)) for rows in cone_rows)
    expected_cone_indices = (q * k, k * k, q * q * (r - 1), r * k, q * (r - 1))
    require(
        cone_indices == expected_cone_indices,
        f"cone determinant check failed at {(e, r, k, q)}: {cone_indices}",
    )

    edge_cone_indices = (
        gcd_entries(cross_product(e3, T)),
        gcd_entries(cross_product(R, T)),
        gcd_entries(cross_product(Q, T)),
    )
    expected_edge_cone_indices = (q * h, k * j, q * (r - 1))
    require(
        edge_cone_indices == expected_edge_cone_indices,
        f"edge cone gcd check failed at {(e, r, k, q)}: {edge_cone_indices}",
    )

    V0: Vector = (a_big, r, 0)
    V1: Vector = (d_big, 1, 0)
    V2: Vector = (d_big, 0, q)
    edge_lengths = (
        gcd_entries(add_vectors(V0, (-V1[0], -V1[1], -V1[2]))),
        gcd_entries(add_vectors(V0, (-V2[0], -V2[1], -V2[2]))),
        gcd_entries(add_vectors(V1, (-V2[0], -V2[1], -V2[2]))),
    )
    expected_edge_lengths = (h, j, 1)
    require(
        edge_lengths == expected_edge_lengths,
        f"edge length check failed at {(e, r, k, q)}: {edge_lengths}",
    )
    triangle_difference_1 = add_vectors(V1, (-V0[0], -V0[1], -V0[2]))
    triangle_difference_2 = add_vectors(V2, (-V0[0], -V0[1], -V0[2]))
    triangle_area_index = gcd_entries(cross_product(triangle_difference_1, triangle_difference_2))
    require(
        triangle_area_index == t,
        f"triangle area gcd failed at {(e, r, k, q)}: {triangle_area_index} != {t}",
    )

    return {
        "matrix_index": matrix_index,
        "F_vectors": f_vectors,
        "volume_vector": volume_vector,
        "cone_indices": cone_indices,
        "edge_cone_indices": edge_cone_indices,
        "edge_lengths": edge_lengths,
        "triangle_area_index": triangle_area_index,
    }


def check_curve_ladder(e: int, r: int, k: int) -> list[dict[str, object]]:
    """Check the old-curve root ladder l=0,...,e-3."""

    data = parameter_data(e, r, k, 1)
    d_big = int(data["D"])
    alpha_r = data["alpha_R"]
    require(isinstance(alpha_r, Fraction), f"curve alpha type failure at {(e, r, k)}")
    ladder: list[dict[str, object]] = []
    for ell in range(e - 2):
        alpha_ell = alpha_r + Fraction(ell, d_big)
        a_ell = Fraction(3 + ell - e, d_big)
        b_ell = Fraction(1, r)
        require(
            a_ell + b_ell == alpha_ell,
            f"curve ladder sum failed at {(e, r, k, ell)}",
        )
        require(0 <= Fraction(ell, d_big) < 1, f"curve ladder shift failed at {(e, r, k, ell)}")
        ladder.append(
            {
                "ell": ell,
                "alpha": fraction_text(alpha_ell),
                "a": fraction_text(a_ell),
                "b": fraction_text(b_ell),
            }
        )
    return ladder


def check_contact(e: int, r: int, k: int, q: int) -> dict[str, object]:
    """Check the contact Euler parameters for q>=2."""

    require(q >= 2, f"contact check requires q>=2, got {(e, r, k, q)}")
    data = parameter_data(e, r, k, q)
    d_big = int(data["D"])
    b_big = int(data["B"])
    beta = int(data["beta"])
    alpha_q = data["alpha_q"]
    alpha_r = data["alpha_R"]
    require(isinstance(alpha_q, Fraction) and isinstance(alpha_r, Fraction), "fraction type failure")

    a = div(d_big * alpha_q - 3, k, "contact a")
    a_alt = div(Fraction(d_big - 3) + Fraction(d_big, q), b_big, "contact a alternate")
    b = Fraction(1, q)
    c = -Fraction(r * (q * (e - 3) + d_big), q * b_big)
    require(a == a_alt, f"contact a identity failed at {(e, r, k, q)}")
    require(a > 0 and b > 0 and c < 0, f"contact signs failed at {(e, r, k, q)}")
    require(alpha_q < 1, f"contact alpha bound failed at {(e, r, k, q)}: {alpha_q}")
    require(
        a + b + c == alpha_q,
        f"contact Euler sum failed at {(e, r, k, q)}",
    )
    if r >= 3:
        require(a < 1, f"r>=3 contact a bound failed at {(e, r, k, q)}: {a}")
    else:
        require(a < Fraction(3, 2), f"r=2 contact a bound failed at {(e, r, k, q)}: {a}")

    integral_exception: dict[str, object] | None = None
    if a.denominator == 1:
        require(a == 1, f"unexpected integral contact a at {(e, r, k, q)}: {a}")
        require(d_big == q * (k + 3), f"integral a D identity failed at {(e, r, k, q)}")
        require(alpha_q == Fraction(1, q), f"integral a alpha identity failed at {(e, r, k, q)}")
        require(k % 2 == 0 and q % 2 == 0, f"integral a parity failed at {(e, r, k, q)}")
        v = k // 2
        require(v <= e - 3, f"integral a v bound failed at {(e, r, k, q)}")
        require(
            alpha_r + Fraction(v, d_big) == alpha_q,
            f"integral a alpha shift failed at {(e, r, k, q)}",
        )
        require(
            e - 3 - v == Fraction((q - 2) * (k + 3), 2),
            f"integral a residual identity failed at {(e, r, k, q)}",
        )
        integral_exception = {"v": v, "a": fraction_text(a)}

    return {
        "e": e,
        "r": r,
        "k": k,
        "q": q,
        "A": int(data["A"]),
        "D": d_big,
        "B": b_big,
        "beta": beta,
        "g": int(data["g"]),
        "h": int(data["h"]),
        "j": int(data["j"]),
        "t": int(data["t"]),
        "N": int(data["N_q"]),
        "nu": int(data["nu_q"]),
        "N_R": int(data["N_R"]),
        "nu_R": int(data["nu_R"]),
        "alpha_R": fraction_text(alpha_r),
        "alpha_q": fraction_text(alpha_q),
        "a": fraction_text(a),
        "b": fraction_text(b),
        "c": fraction_text(c),
        "integral_a_exception": integral_exception,
    }


def check_rational_identities(e: int, r: int, k: int, q: int, s: Fraction) -> dict[str, Fraction]:
    """Check the raw, cancelled, replacement, and curve formulas at s."""

    data = parameter_data(e, r, k, q)
    a_big = int(data["A"])
    d_big = int(data["D"])
    b_big = int(data["B"])
    beta = int(data["beta"])
    g = int(data["g"])
    h = int(data["h"])
    j = int(data["j"])
    t = int(data["t"])

    a0 = a_big * s + 3
    H = r * d_big * s + 3 * r + k
    d = s + 1
    K = q * b_big * s + q * beta + k
    P = q * s + q + 1
    for label, denominator in (("a0", a0), ("H", H), ("d", d), ("K", K), ("P", P)):
        require(denominator != 0, f"sample s={s} hits {label}=0 at {(e, r, k, q)}")

    vertices = (
        div(q * k, a0 * K, "vertices-1")
        + div(k * k, a0 * H * K, "vertices-2")
        + div(r * k, H * K, "vertices-3")
        + div(q * (q + 1) * (r - 1), P * K, "vertices-4")
    )
    edge_face = div(s, d, "edge prefactor") * (
        div(t * t - q * h * h, K, "edge-1")
        - div(k * j * j, H * K, "edge-2")
        - div(q * (r - 1), P * K, "edge-3")
    )
    z_raw = vertices + edge_face
    z_cancelled = div(
        div(q * k, a0, "cancelled-1")
        + div(k * k, a0 * H, "cancelled-2")
        + div(r * k, H, "cancelled-3")
        + div(q * (r - 1), d, "cancelled-4")
        + div(s, d, "cancelled-edge")
        * (t * t - q * h * h - div(k * j * j, H, "cancelled-edge-inner")),
        K,
        "cancelled total",
    )
    z_t = div(k, a0, "ZT-1") + div(r, d, "ZT-2")
    z_t = div(z_t, H, "ZT total")
    z_replacement = z_t + div(
        s * (H * (t * t - q * h * h) - k * (j * j + q * (r - 1) - r)),
        d * H * K,
        "replacement correction",
    )
    z_generic_curve = div(k, a0, "generic curve-1") + div(
        r - div(g * g * s, d, "generic curve-2"), 1, "generic curve numerator"
    )
    z_generic_curve = div(z_generic_curve, H, "generic curve total")

    require(z_raw == z_cancelled, f"raw/cancelled identity failed at {(e, r, k, q, s)}")
    require(z_raw == z_replacement, f"replacement identity failed at {(e, r, k, q, s)}")
    if q == 1:
        require(z_raw == z_t, f"q=1 reduction failed at {(e, r, k, s)}")
    if k == 1:
        require(b_big == (r - 1) * d_big + 1, f"k=1 B identity failed at {(e, r, q, s)}")
        expected_k1 = z_t - div(r * (q - 1) * s * (d_big * s + 4), d * H * K, "k=1 correction")
        require(z_raw == expected_k1, f"k=1 reduction failed at {(e, r, q, s)}")
        expected_generic = div(r - 1 + div(1, a0, "k=1 generic a") + div(1, d, "k=1 generic d"), H, "k=1 generic curve")
        require(z_generic_curve == expected_generic, f"generic curve k=1 failed at {(e, r, q, s)}")

    return {
        "s": s,
        "Z": z_raw,
        "Z2": z_cancelled,
        "Z3": z_replacement,
        "ZT": z_t,
        "ZG": z_generic_curve,
    }


def serialise_fraction(value: object) -> object:
    """Convert nested Fraction values to exact strings for JSON."""

    if isinstance(value, Fraction):
        return fraction_text(value)
    if isinstance(value, dict):
        return {str(key): serialise_fraction(item) for key, item in value.items()}
    if isinstance(value, list):
        return [serialise_fraction(item) for item in value]
    return value


def build_report() -> dict[str, object]:
    """Run the finite exact sweeps and return a JSON-compatible report."""

    parameter_count = 0
    contact_count = 0
    ladder_count = 0
    lattice_count = 0
    integral_contact_rows: list[dict[str, object]] = []

    for e in E_RANGE:
        for r in R_RANGE:
            for k in K_RANGE:
                ladder = check_curve_ladder(e, r, k)
                ladder_count += len(ladder)
                for q in Q_RANGE:
                    parameter_count += 1
                    parameter_data(e, r, k, q)
                    check_lattice_data(e, r, k, q)
                    lattice_count += 1
                    if q >= 2:
                        row = check_contact(e, r, k, q)
                        contact_count += 1
                        if row["integral_a_exception"] is not None:
                            integral_contact_rows.append(row)

    rational_count = 0
    q1_count = 0
    k1_count = 0
    sample_rational: list[dict[str, object]] = []
    for e in RATIONAL_E:
        for r in RATIONAL_R:
            for k in RATIONAL_K:
                for q in RATIONAL_Q:
                    for s in RATIONAL_S:
                        result = check_rational_identities(e, r, k, q, s)
                        rational_count += 1
                        if q == 1:
                            q1_count += 1
                        if k == 1:
                            k1_count += 1
                        if (e, r, k, q) == (4, 2, 2, 2):
                            sample_rational.append(
                                {
                                    "s": fraction_text(s),
                                    "Z": fraction_text(result["Z"]),
                                    "ZT": fraction_text(result["ZT"]),
                                }
                            )

    sample_contact = check_contact(4, 2, 2, 2)
    sample_lattice = check_lattice_data(4, 2, 2, 2)
    require(
        sample_contact["N"] == 12
        and sample_contact["nu"] == 6
        and sample_contact["alpha_q"] == "1/2"
        and sample_contact["a"] == "1"
        and sample_contact["b"] == "1/2"
        and sample_contact["c"] == "-1",
        f"requested contact sample mismatch: {sample_contact}",
    )
    sample_curve = parameter_data(4, 2, 2, 1)
    require(sample_curve["N_R"] == 10 and sample_curve["nu_R"] == 4, "requested curve sample mismatch")
    sample_ladder = check_curve_ladder(4, 2, 2)
    require(sample_ladder[1]["alpha"] == "1/2", f"requested l=1 sample mismatch: {sample_ladder}")

    report: dict[str, object] = {
        "sweep": {
            "e": [E_RANGE.start, E_RANGE.stop - 1],
            "r": [R_RANGE.start, R_RANGE.stop - 1],
            "k": [K_RANGE.start, K_RANGE.stop - 1],
            "q": [Q_RANGE.start, Q_RANGE.stop - 1],
        },
        "checked_count": parameter_count,
        "contact_checked_count": contact_count,
        "curve_ladder_checked_count": ladder_count,
        "lattice_checked_count": lattice_count,
        "integral_contact_rows": integral_contact_rows,
        "rational_function_sweep": {
            "e": list(RATIONAL_E),
            "r": list(RATIONAL_R),
            "k": list(RATIONAL_K),
            "q": list(RATIONAL_Q),
            "s": [fraction_text(value) for value in RATIONAL_S],
            "checked_count": rational_count,
            "q1_reduction_count": q1_count,
            "k1_reduction_count": k1_count,
        },
        "requested_sample": {
            "contact": {**sample_contact, "T": [1, 2, 1]},
            "lattice": sample_lattice,
            "curve": {
                "N_R": sample_curve["N_R"],
                "nu_R": sample_curve["nu_R"],
                "alpha_R": fraction_text(sample_curve["alpha_R"]),
            },
            "curve_ladder": sample_ladder,
            "rational_values": sample_rational,
        },
        "limitation": (
            "Exact arithmetic only.  The checks do not prove cycles, resolution "
            "or geometric realization, analytic-unit comparison, nonzero periods, "
            "Bernstein--Sato roots, or the formulas for all parameter values."
        ),
    }
    return serialise_fraction(report)  # type: ignore[return-value]


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
    """Run exact checks, print JSON, and optionally write a report."""

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
