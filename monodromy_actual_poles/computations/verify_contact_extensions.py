"""Exact algebra checks for the finite-contact formulas.

This is an auxiliary numerical verification script, not a proof.  The contact
partitions generated below are formal numerical data; no geometric
realizability of an arbitrary partition is asserted.

The implementation deliberately uses only the Python standard library.  All
rational evaluations use :class:`fractions.Fraction`.
"""

from collections import Counter
from fractions import Fraction
from math import gcd


def divisors(n):
    """Return the positive divisors of ``n`` in increasing order."""

    result = []
    for d in range(1, n + 1):
        if n % d == 0:
            result.append(d)
    return result


def mobius(n):
    """Return the Moebius function of a positive integer."""

    value = 1
    prime = 2
    remaining = n
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            if remaining % prime == 0:
                return 0
            value = -value
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        value = -value
    return value


def data(e, r):
    """Return the integer parameters used by the formulas."""

    a_cap = e * r
    degree = a_cap + 1
    base = (r - 1) * degree + 1
    beta = 3 * r - 2
    chi = e * (3 - e)
    return a_cap, degree, base, beta, chi


def a_value(e, r, s):
    a_cap, _, _, _, _ = data(e, r)
    return a_cap * s + 3


def h_value(e, r, s):
    _, degree, _, _, _ = data(e, r)
    return r * degree * s + 3 * r + 1


def d_value(s):
    return s + 1


def k_value(e, r, q, s):
    _, _, base, beta, _ = data(e, r)
    return q * base * s + q * beta + 1


def p_value(q, s):
    return q * s + q + 1


def indicator(ell, n):
    return int(n % ell == 0)


def nonzero(mapping):
    """Return an ordinary dictionary with zero entries removed."""

    return {key: value for key, value in mapping.items() if value}


def delta_factors(e, r, contacts):
    """Raw ``(1-t^N)`` exponents in Delta2."""

    a_cap, degree, base, _, chi = data(e, r)
    b = len(contacts)
    factors = Counter()
    factors[1] -= 1
    factors[a_cap] += 3 - chi
    factors[r * degree] += b - chi
    factors[degree] += chi - b
    factors[base] -= b
    for q in contacts:
        factors[q * base] += 1
    return nonzero(factors)


def cyclotomic_multiplicities(factors):
    """Compute Phi_m exponents by enumerating divisors of every factor."""

    result = Counter()
    for n, exponent in factors.items():
        for divisor in divisors(n):
            result[divisor] += exponent
    return nonzero(result)


def recover_factor_exponents(cyclotomic, largest_n):
    """Invert ``C_m=sum_{m|N} f_N`` by descending divisor enumeration."""

    recovered = {}
    for n in range(largest_n, 0, -1):
        exponent = cyclotomic.get(n, 0)
        for multiple in range(2 * n, largest_n + 1, n):
            exponent -= recovered.get(multiple, 0)
        if exponent:
            recovered[n] = exponent
    return recovered


def expected_multiplicity(e, r, contacts, m):
    """The stated nontrivial order-m multiplicity M_m."""

    a_cap, degree, base, _, chi = data(e, r)
    b = len(contacts)
    value = (3 - chi) * indicator(m, a_cap)
    value += (b - chi) * (
        indicator(m, r * degree) - indicator(m, degree)
    )
    value += sum(
        indicator(m, q * base) - indicator(m, base) for q in contacts
    )
    if m == 1:
        value -= 1
    return value


def recover_contacts_from_delta(e, r, contacts, cyclotomic):
    """Recover b and the contact multiplicities from independent factor data."""

    a_cap, degree, base, _, chi = data(e, r)
    b = len(contacts)
    m_r = cyclotomic.get(r, 0)
    recovered_b = m_r - 3 + 2 * chi
    if recovered_b != b:
        raise AssertionError(
            f"b recovery failed for (e,r)=({e},{r}): "
            f"got {recovered_b}, expected {b}"
        )

    raw = recover_factor_exponents(cyclotomic, max(delta_factors(e, r, contacts)))
    expected_raw = delta_factors(e, r, contacts)
    if raw != expected_raw:
        raise AssertionError(
            f"factor inversion failed for (e,r)=({e},{r}), contacts={contacts}: "
            f"got {raw}, expected {expected_raw}"
        )

    # Remove the A, rD, D and (1-t) factors.  What remains is Gamma(t^B).
    base_factors = Counter(
        {
            1: -1,
            a_cap: 3 - chi,
            r * degree: b - chi,
            degree: chi - b,
        }
    )
    residual = Counter(raw)
    for n, exponent in base_factors.items():
        residual[n] -= exponent
    residual = nonzero(residual)

    scaled = {}
    for n, exponent in residual.items():
        if n % base:
            raise AssertionError(
                f"residual factor {n} is not a multiple of B={base}"
            )
        scaled[n // base] = exponent

    max_q = max(contacts)
    gamma = {
        d: sum(
            exponent
            for q, exponent in scaled.items()
            if q % d == 0
        )
        for d in range(2, max_q + 1)
    }
    recovered_nq = {
        q: sum(
            mobius(j) * gamma.get(j * q, 0)
            for j in range(1, max_q // q + 1)
        )
        for q in range(2, max_q + 1)
    }
    expected_nq = Counter(contacts)
    for q in range(2, max_q + 1):
        if recovered_nq[q] != expected_nq.get(q, 0):
            raise AssertionError(
                f"contact recovery failed for (e,r)=({e},{r}), "
                f"q={q}: got {recovered_nq[q]}, "
                f"expected {expected_nq.get(q, 0)}"
            )
    recovered_n1 = recovered_b - sum(recovered_nq.values())
    if recovered_n1 != expected_nq.get(1, 0):
        raise AssertionError(
            f"q=1 recovery failed for (e,r)=({e},{r}): "
            f"got {recovered_n1}, expected {expected_nq.get(1, 0)}"
        )


def mu_degree(e, r, contacts):
    """Degree of Delta2, including the -1 factor at order one."""

    a_cap, degree, base, _, chi = data(e, r)
    b = len(contacts)
    return (
        a_cap * (3 - chi)
        + (r - 1) * degree * (b - chi)
        + base * sum(q - 1 for q in contacts)
        - 1
    )


def m_r(e, r, contacts):
    _, _, _, _, chi = data(e, r)
    return len(contacts) + 3 - 2 * chi


def local_twisted_expanded(e, r, q, ell, s):
    """Expanded cone expression from the twisted formula."""

    a_cap, degree, base, beta, _ = data(e, r)
    a = a_cap * s + 3
    h = r * degree * s + 3 * r + 1
    k = q * base * s + q * beta + 1
    p = q * s + q + 1
    g = gcd(degree, q)
    delta_r = indicator(ell, r)
    delta_g = indicator(ell, g)
    delta_b = indicator(ell, base)
    delta_rg = indicator(ell, r * g)
    delta_qb = indicator(ell, q * base)
    return (
        delta_r * (q / (a * k) + 1 / (a * h * k))
        + delta_g * (r / (h * k) + q * (r - 1) / (p * k))
        - delta_b * q / k
        - delta_rg / (h * k)
        - delta_g * q * (r - 1) / (p * k)
        + delta_qb / k
    )


def local_twisted_compact(e, r, q, ell, s):
    """Compact form of the same twisted local contribution."""

    a_cap, degree, base, beta, _ = data(e, r)
    a = a_cap * s + 3
    h = r * degree * s + 3 * r + 1
    k = q * base * s + q * beta + 1
    g = gcd(degree, q)
    delta_r = indicator(ell, r)
    delta_g = indicator(ell, g)
    delta_b = indicator(ell, base)
    delta_rg = indicator(ell, r * g)
    delta_qb = indicator(ell, q * base)
    return (
        delta_r / (a * h)
        + (
            q * delta_r
            + r * delta_g
            - delta_rg
            + h * (delta_qb - q * delta_b)
        )
        / (h * k)
    )


def global_twisted(e, r, contacts, ell, s):
    """Global twisted expression assembled from the compact local formula."""

    a_cap, degree, _, _, chi = data(e, r)
    b = len(contacts)
    a = a_cap * s + 3
    h = r * degree * s + 3 * r + 1
    g_tw = indicator(ell, r) / (a * h)
    g_tw += (
        r * indicator(ell, degree) - indicator(ell, r * degree)
    ) / h
    result = (3 - chi) * indicator(ell, a_cap) / a
    result += (chi - b) * g_tw
    result += sum(
        local_twisted_compact(e, r, q, ell, s) for q in contacts
    )
    return result


def candidate_ells(e, r, contacts):
    """Finite set of relevant orders, including all relevant divisors."""

    a_cap, degree, base, _, _ = data(e, r)
    numbers = [a_cap, degree, r, r * degree, base]
    for q in set(contacts):
        g = gcd(degree, q)
        numbers.extend((q * base, r * g, g))
    result = set(range(2, 31))
    for number in numbers:
        result.update(divisor for divisor in divisors(number) if divisor > 1)
    return sorted(result)


def has_no_global_source(e, r, contacts, ell):
    a_cap, degree, base, _, _ = data(e, r)
    if indicator(ell, a_cap) or indicator(ell, r * degree):
        return False
    return all(
        q == 1 or not indicator(ell, q * base) for q in contacts
    )


def global_z(e, r, contacts, s):
    """The global Z(s) expression used for the residue checks."""

    a_cap, degree, base, beta, chi = data(e, r)
    b = len(contacts)
    a = a_cap * s + 3
    h = r * degree * s + 3 * r + 1
    d = s + 1
    contact_sum = sum(
        (q - 1) / (q * base * s + q * beta + 1) for q in contacts
    )
    return (
        (3 - chi) / a
        + (chi - b) * (r - 1) / h
        + chi / (a * h)
        + (chi + b * (r - 1)) / (d * h)
        - r * s * (degree * s + 4) / (d * h) * contact_sum
    )


def formal_profiles(e, r):
    """Return the requested formal numerical contact partitions."""

    _, degree, _, _, _ = data(e, r)
    total = e * degree
    profiles = [
        ("no tangencies", (1,) * total),
        ("one q2", (2,) + (1,) * (total - 2)),
        ("several q2/q3", (2, 2, 3, 3) + (1,) * (total - 10)),
        # q=D shares all of D's prime factors and remains a valid formal part.
        ("q sharing factors with D", (degree,) + (1,) * (total - degree)),
    ]
    for _, contacts in profiles:
        if sum(contacts) != total or not contacts:
            raise AssertionError(f"invalid formal profile: {contacts}")
    return profiles


def check_profile(e, r, contacts, stats):
    a_cap, degree, base, _, _ = data(e, r)
    factors = delta_factors(e, r, contacts)
    cyclotomic = cyclotomic_multiplicities(factors)
    largest_n = max(factors)

    # Compare every order, including m=1 where the explicit -1 is required.
    for m in range(1, largest_n + 1):
        observed = cyclotomic.get(m, 0)
        expected = expected_multiplicity(e, r, contacts, m)
        if observed != expected:
            raise AssertionError(
                f"M_{m} failed for (e,r)=({e},{r}), contacts={contacts}: "
                f"got {observed}, expected {expected}"
            )
        stats["cyclotomic"] += 1

    expected_mr = len(contacts) + 3 - 2 * data(e, r)[4]
    if cyclotomic.get(r, 0) != expected_mr:
        raise AssertionError("primitive-r multiplicity identity failed")
    stats["primitive_r"] += 1
    recover_contacts_from_delta(e, r, contacts, cyclotomic)
    stats["contact_recovery"] += 1

    degree_from_factors = sum(n * exponent for n, exponent in factors.items())
    if degree_from_factors != mu_degree(e, r, contacts):
        raise AssertionError(
            f"degree failed for (e,r)=({e},{r}), contacts={contacts}"
        )
    stats["degree"] += 1

    for index, q in enumerate(contacts):
        if q == 1:
            continue
        resolved = contacts[:index] + (1,) * q + contacts[index + 1 :]
        mu_increase = mu_degree(e, r, contacts) - mu_degree(e, r, resolved)
        primitive_drop = m_r(e, r, resolved) - m_r(e, r, contacts)
        if mu_increase != q - 1 or primitive_drop != q - 1:
            raise AssertionError(
                f"collision check failed for q={q}, (e,r)=({e},{r})"
            )
        stats["collision"] += 1


def check_twisted(e, r, contacts, stats, s):
    for q in sorted(set(contacts)):
        for ell in candidate_ells(e, r, (q,)):
            expanded = local_twisted_expanded(e, r, q, ell, s)
            compact = local_twisted_compact(e, r, q, ell, s)
            if expanded != compact:
                raise AssertionError(
                    f"twisted local mismatch for (e,r,q,ell)=({e},{r},{q},{ell})"
                )
            stats["twisted_local"] += 1
            if q == 1:
                expected = indicator(ell, r) / (
                    a_value(e, r, s) * h_value(e, r, s)
                )
                if expanded != expected:
                    raise AssertionError(
                        f"q=1 twisted reduction failed for (e,r,ell)=({e},{r},{ell})"
                    )
                stats["twisted_q1"] += 1

    for ell in candidate_ells(e, r, contacts):
        if not has_no_global_source(e, r, contacts, ell):
            continue
        if global_twisted(e, r, contacts, ell, s) != 0:
            raise AssertionError(
                f"source-free twist did not vanish for (e,r,ell)=({e},{r},{ell})"
            )
        stats["twisted_vanishing"] += 1


def check_boundary_residues(e, r, contacts, stats):
    a_cap, degree, base, beta, chi = data(e, r)
    if e == 3:
        s0 = -Fraction(1, r)
        d0 = s0 + 1
        b = len(contacts)
        contact_sum = Fraction(0)
        for q in contacts:
            k0 = q * base * s0 + q * beta + 1
            if k0 != 1:
                raise AssertionError("e=3 boundary K_q did not cancel to one")
            contact_sum += Fraction(q - 1, k0)
        # x=rs+1.  After canceling x from a=3x and H=Dx, the
        # expression x Z has this exact finite value at s=s0.
        x_z = (
            Fraction(1)
            - Fraction(b * (r - 1), degree)
            + Fraction(b * (r - 1), d0 * degree)
            + contact_sum / degree
        )
        residue = x_z / r
        if x_z != 4 or residue != Fraction(4, r):
            raise AssertionError(
                f"e=3 boundary residue failed for (r,contacts)=({r},{contacts})"
            )
        stats["boundary_e3"] += 1
    elif e >= 4:
        s_star = -Fraction(3, a_cap)
        h_star = h_value(e, r, s_star)
        if not h_star:
            raise AssertionError("largest-residue point is not isolated")
        residue = (Fraction(3 - chi) + Fraction(chi, h_star)) / a_cap
        expected = -Fraction(3 * (e - 1), a_cap)
        if residue != expected:
            raise AssertionError(
                f"largest residue failed for (e,r)=({e},{r}): "
                f"got {residue}, expected {expected}"
            )
        recovered_e = 1 + residue / (-Fraction(3, a_cap))
        recovered_r = -Fraction(3, e * (-Fraction(3, a_cap)))
        if recovered_e != e or recovered_r != r:
            raise AssertionError("boundary parameter inversion failed")
        stats["boundary_e_ge_4"] += 1

    for q in contacts:
        if q < 2:
            continue
        s_q = -Fraction(q * beta + 1, q * base)
        recovered_q = -Fraction(1, base * s_q + beta)
        if recovered_q != q:
            raise AssertionError(
                f"new-pole inversion failed for q={q}, (e,r)=({e},{r})"
            )
        stats["new_pole"] += 1


def check_collision_z(e, r, contacts, stats, sample_points):
    """Check the global Z collision identity at two regular rational points."""

    _, degree, _, _, _ = data(e, r)
    for index, q in enumerate(contacts):
        if q == 1:
            continue
        transverse = contacts[:index] + (1,) * q + contacts[index + 1 :]
        for s in sample_points:
            h = h_value(e, r, s)
            k = k_value(e, r, q, s)
            actual = global_z(e, r, contacts, s) - global_z(
                e, r, transverse, s
            )
            expected = (
                (q - 1) * (r - 1) * s / ((s + 1) * h)
                - (q - 1) * r * s * (degree * s + 4)
                / ((s + 1) * h * k)
            )
            if actual != expected:
                raise AssertionError(
                    f"collision Z identity failed for q={q}, "
                    f"(e,r,s)=({e},{r},{s})"
                )
            stats["collision_z"] += 1


def check_transverse_reference_z(stats, sample_points):
    """Check the independent e=3,r=2 all-q=1 specialization."""

    e, r = 3, 2
    contacts = (1,) * (e * (e * r + 1))
    for s in sample_points:
        actual = global_z(e, r, contacts, s)
        expected = (1 - 2 * s) / ((s + 1) * (2 * s + 1))
        if actual != expected:
            raise AssertionError(
                f"transverse reference Z failed at s={s}: "
                f"got {actual}, expected {expected}"
            )
        stats["transverse_reference_z"] += 1


def main():
    stats = Counter()
    profile_count = 0
    sample_points = (Fraction(2, 7), Fraction(5, 11))
    nonsingular_s = sample_points[0]

    for e in range(3, 7):
        for r in range(2, 6):
            for _, contacts in formal_profiles(e, r):
                profile_count += 1
                check_profile(e, r, contacts, stats)
                check_twisted(e, r, contacts, stats, nonsingular_s)
                check_boundary_residues(e, r, contacts, stats)
                check_collision_z(e, r, contacts, stats, sample_points)

    check_transverse_reference_z(stats, sample_points)

    # A false exact-order inference: M_3 vanishes here, while the twisted
    # rational expression still detects the D=9 contribution.
    e, r = 4, 2
    contacts = tuple(1 for _ in range(e * (e * r + 1)))
    s = nonsingular_s
    if expected_multiplicity(e, r, contacts, 3) != 0:
        raise AssertionError("false-order counterexample has nonzero M_3")
    expected_twist = -Fraction(40, h_value(e, r, s))
    if global_twisted(e, r, contacts, 3, s) != expected_twist:
        raise AssertionError("false exact-order twisted counterexample failed")
    stats["false_order"] += 1

    print(
        "PASS verify_contact_extensions: "
        f"{profile_count} formal profiles; "
        f"{stats['cyclotomic']} cyclotomic orders; "
        f"{stats['contact_recovery']} contact recoveries; "
        f"{stats['collision']} collision checks; "
        f"{stats['collision_z']} collision-Z checks; "
        f"{stats['twisted_local']} local twisted comparisons; "
        f"{stats['twisted_vanishing']} source-free twists; "
        f"{stats['boundary_e3'] + stats['boundary_e_ge_4']} residue checks; "
        f"{stats['new_pole']} new-pole inversions; "
        f"{stats['false_order']} false-order counterexample; "
        f"{stats['transverse_reference_z']} transverse-reference Z checks."
    )
    print(
        "Caveat: all contact partitions used here are formal numerical data; "
        "no geometric realizability is asserted."
    )


if __name__ == "__main__":
    main()
