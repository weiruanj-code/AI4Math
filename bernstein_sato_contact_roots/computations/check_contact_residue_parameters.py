"""Exact arithmetic checks for the contact-residue parameter family.

The checks in this file are deliberately limited to the normalized-form
arithmetic supplied for the family.  They do not establish any statement
about cycles, Bernstein polynomials, geometric realization, or analytic
units.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


COMPUTATIONS_DIR = Path(__file__).resolve().parent

E_MIN = 3
E_MAX = 32
R_MIN = 2
R_MAX = 12
Q_MIN = 2
Q_MAX = 96
RESONANCE = (7, 3, 2)

Vector = tuple[int, int, int]


def require(condition: bool, message: str) -> None:
    """Raise an explicit runtime failure when an exact check is false."""

    if not condition:
        raise RuntimeError(message)


def add_vectors(*vectors: Vector) -> Vector:
    """Add integer exponent vectors componentwise."""

    return tuple(sum(vector[index] for vector in vectors) for index in range(3))  # type: ignore[return-value]


def scale_vector(scalar: int, vector: Vector) -> Vector:
    """Scale an integer exponent vector."""

    return tuple(scalar * component for component in vector)  # type: ignore[return-value]


def determinant(rows: Sequence[Vector]) -> int:
    """Return the determinant of a three-by-three integer matrix."""

    require(len(rows) == 3, "the exponent matrix must have three rows")
    (a11, a12, a13), (a21, a22, a23), (a31, a32, a33) = rows
    return (
        a11 * (a22 * a33 - a23 * a32)
        - a12 * (a21 * a33 - a23 * a31)
        + a13 * (a21 * a32 - a22 * a31)
    )


def fraction_text(value: Fraction) -> str:
    """Render a Fraction exactly, including integer values."""

    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def curve_row(e: int, r: int) -> dict[str, object]:
    """Return and validate one curve-residue parameter row."""

    require(e >= 3 and r >= 2, f"invalid curve parameters {(e, r)}")

    a = e * r
    d = a + 1
    n_r = r * d
    nu_r = 3 * r + 1
    alpha_r = Fraction(nu_r, n_r)
    a_r = 3 - a * alpha_r
    b_r = alpha_r - a_r

    require(
        a_r == Fraction(3 - e, d),
        f"a_R identity failed at {(e, r)}: {a_r} != {Fraction(3 - e, d)}",
    )
    require(
        b_r == Fraction(1, r),
        f"b_R identity failed at {(e, r)}: {b_r} != {Fraction(1, r)}",
    )
    require(
        Fraction(0) < alpha_r < 1,
        f"alpha_R bounds failed at {(e, r)}: {alpha_r}",
    )
    if e >= 4:
        require(
            -Fraction(1, r) < a_r < 0,
            f"a_R bounds failed at {(e, r)}: {a_r}",
        )
        require(
            a_r.denominator != 1,
            f"a_R unexpectedly integral at {(e, r)}: {a_r}",
        )

    require(
        e * nu_r - 3 * d == e - 3,
        f"curve transition identity failed at {(e, r)}",
    )
    require(
        a * d == e * n_r,
        f"curve degree identity failed at {(e, r)}",
    )
    require(
        -e * nu_r + 3 * d + (e - 3) == 0,
        f"curve transition weight failed at {(e, r)}",
    )
    require(
        alpha_r - Fraction(3, a) == Fraction(e - 3, e * r * d),
        f"alpha_R shift failed at {(e, r)}",
    )

    return {
        "e": e,
        "r": r,
        "N_R": n_r,
        "nu_R": nu_r,
        "alpha_R": fraction_text(alpha_r),
        "a_R": fraction_text(a_r),
        "b_R": fraction_text(b_r),
        "theta_power": e - 3,
    }


def exact_row(e: int, r: int, q: int) -> dict[str, object]:
    """Return the exact parameter row after validating its identities."""

    require(e >= 3 and r >= 2 and q >= 2, f"invalid parameters {(e, r, q)}")

    a = e * r
    d = a + 1
    b = (r - 1) * d + 1
    beta = 3 * r - 2
    n = q * b
    nu = q * beta + 1

    alpha = Fraction(nu, n)
    lambda1 = d * alpha - 3
    lambda2 = Fraction(1, q)
    lambda3 = alpha - lambda1 - lambda2

    expected_lambda1 = (Fraction(d - 3) + Fraction(d, q)) / b
    expected_lambda3 = -Fraction(r * (q * (e - 3) + d), q * b)
    require(
        lambda1 == expected_lambda1,
        f"lambda1 identity failed at {(e, r, q)}: {lambda1} != {expected_lambda1}",
    )
    require(
        lambda3 == expected_lambda3,
        f"lambda3 identity failed at {(e, r, q)}: {lambda3} != {expected_lambda3}",
    )
    require(
        alpha - Fraction(3, a)
        == (Fraction(r * (e - 3)) + Fraction(a, q)) / (a * b),
        f"alpha shift failed at {(e, r, q)}",
    )
    require(Fraction(0) < alpha < 1, f"alpha bounds failed at {(e, r, q)}: {alpha}")
    require(
        Fraction(0) < lambda1 < Fraction(3, 2),
        f"lambda1 bounds failed at {(e, r, q)}: {lambda1}",
    )
    require(lambda2 > 0, f"lambda2 positivity failed at {(e, r, q)}: {lambda2}")
    require(lambda3 < 0, f"lambda3 negativity failed at {(e, r, q)}: {lambda3}")
    require(
        lambda1.denominator != 1,
        f"lambda1 unexpectedly integral at {(e, r, q)}: {lambda1}",
    )

    integral_lambda3 = lambda3.denominator == 1
    require(
        integral_lambda3 == ((e, r, q) == RESONANCE),
        f"lambda3 resonance mismatch at {(e, r, q)}: {lambda3}",
    )

    u: Vector = (q * (r - 1), -1, -(r - 1))
    v: Vector = (q, 0, -1)
    w: Vector = (1, 0, 0)
    exponent_determinant = determinant((u, v, w))
    require(
        exponent_determinant == 1,
        f"monomial exponent determinant failed at {(e, r, q)}: {exponent_determinant}",
    )

    actual_monomials = (
        add_vectors(scale_vector(a, u), scale_vector(r, v)),
        add_vectors(scale_vector(a, u), u, v),
        add_vectors(scale_vector(a, u), u, scale_vector(q, w)),
    )
    expected_monomials = (
        (n, -d + 1, -b),
        (n, -d, -b),
        (n, -d, -b + 1),
    )
    require(
        actual_monomials == expected_monomials,
        f"F exponent vectors failed at {(e, r, q)}: {actual_monomials}",
    )

    # For u^2 du dv dw, the monomial Jacobian contributes u v w/(t x y).
    volume_exponent = add_vectors(
        scale_vector(3, u), v, w, (-1, -1, -1)
    )
    expected_volume_exponent = (nu - 1, -4, -beta - 1)
    require(
        volume_exponent == expected_volume_exponent,
        f"volume exponent failed at {(e, r, q)}: {volume_exponent}",
    )

    return {
        "e": e,
        "r": r,
        "q": q,
        "A": a,
        "D": d,
        "B": b,
        "beta": beta,
        "N": n,
        "nu": nu,
        "alpha": fraction_text(alpha),
        "lambda1": fraction_text(lambda1),
        "lambda2": fraction_text(lambda2),
        "lambda3": fraction_text(lambda3),
    }


def check_sample(e: int, r: int, q: int, expected: dict[str, str]) -> dict[str, object]:
    """Validate one requested exact sample and return its report row."""

    row = exact_row(e, r, q)
    for key, expected_value in expected.items():
        actual_value = row[key]
        require(
            actual_value == expected_value,
            f"sample {(e, r, q)} {key} mismatch: {actual_value} != {expected_value}",
        )
    return row


def build_report() -> dict[str, object]:
    """Run the full exact sweep and assemble a JSON-serializable report."""

    curve_checked_count = 0
    for e in range(E_MIN, E_MAX + 1):
        for r in range(R_MIN, R_MAX + 1):
            curve_row(e, r)
            curve_checked_count += 1
    expected_curve_count = (E_MAX - E_MIN + 1) * (R_MAX - R_MIN + 1)
    require(
        curve_checked_count == expected_curve_count,
        f"curve sweep count mismatch: {curve_checked_count}",
    )

    resonances: list[dict[str, object]] = []
    checked_count = 0
    for e in range(E_MIN, E_MAX + 1):
        for r in range(R_MIN, R_MAX + 1):
            for q in range(Q_MIN, Q_MAX + 1):
                row = exact_row(e, r, q)
                checked_count += 1
                if row["lambda3"] and Fraction(str(row["lambda3"])).denominator == 1:
                    resonances.append(row)

    expected_count = (E_MAX - E_MIN + 1) * (R_MAX - R_MIN + 1) * (Q_MAX - Q_MIN + 1)
    require(checked_count == expected_count, f"sweep count mismatch: {checked_count}")
    require(
        [(row["e"], row["r"], row["q"]) for row in resonances] == [RESONANCE],
        f"resonance rows mismatch: {resonances}",
    )

    sample_rows = [
        check_sample(
            4,
            2,
            2,
            {
                "alpha": "9/20",
                "lambda1": "21/20",
                "lambda2": "1/2",
                "lambda3": "-11/10",
            },
        ),
        check_sample(
            7,
            3,
            2,
            {
                "alpha": "1/6",
                "lambda1": "2/3",
                "lambda2": "1/2",
                "lambda3": "-1",
            },
        ),
    ]
    curve_sample = curve_row(4, 2)
    require(
        curve_sample
        == {
            "e": 4,
            "r": 2,
            "N_R": 18,
            "nu_R": 7,
            "alpha_R": "7/18",
            "a_R": "-1/9",
            "b_R": "1/2",
            "theta_power": 1,
        },
        f"curve sample mismatch: {curve_sample}",
    )

    return {
        "checked_count": checked_count,
        "curve_checked_count": curve_checked_count,
        "curve_sample": curve_sample,
        "sweep": {
            "e": [E_MIN, E_MAX],
            "r": [R_MIN, R_MAX],
            "q": [Q_MIN, Q_MAX],
        },
        "sample_rows": sample_rows,
        "resonances": resonances,
        "monomial_substitution": {
            "determinant": 1,
            "F_vectors": [
                ["N", "-D+1", "-B"],
                ["N", "-D", "-B"],
                ["N", "-D", "-B+1"],
            ],
            "volume_powers": ["nu-1", -4, "-beta-1"],
        },
        "limitation": (
            "Checks normalized-form arithmetic only; it does not establish cycles, "
            "b-functions, geometric realization, or analytic units."
        ),
    }


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
    """Resolve a requested report path and keep it in this computations folder."""

    resolved = (COMPUTATIONS_DIR / path if not path.is_absolute() else path).resolve()
    try:
        resolved.relative_to(COMPUTATIONS_DIR)
    except ValueError as exc:
        raise RuntimeError(
            f"--json path must be under {COMPUTATIONS_DIR}: {path}"
        ) from exc
    return resolved


def main(argv: Iterable[str] | None = None) -> int:
    """Run checks, print compact JSON, and optionally write the same report."""

    args = parse_args(argv)
    try:
        report = build_report()
        rendered = json.dumps(report, indent=2, sort_keys=True)
        if args.json_path is not None:
            output_path = report_path(args.json_path)
            output_path.write_text(rendered + "\n", encoding="utf-8")
    except (OSError, RuntimeError) as exc:
        raise SystemExit(f"check failed: {exc}") from exc

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
