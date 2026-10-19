"""Blind exact recovery checks for the compressed finite-contact formulas.

This is an auxiliary algebra check, not a proof.  The contact partitions in
the test data are formal numerical data; the program makes no claim that all
of them are geometrically realizable.

Only the Python standard library is used.  Polynomials are dense lists of
integers and all rational evaluations use ``fractions.Fraction``.
"""

from collections import Counter
from fractions import Fraction
from math import gcd, isqrt


def trim(poly):
    """Return a copy with trailing zero coefficients removed."""

    result = list(poly)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def coefficient(poly, index):
    """Read a coefficient, treating indices beyond the list as zero."""

    return poly[index] if 0 <= index < len(poly) else 0


def add(poly_a, poly_b):
    length = max(len(poly_a), len(poly_b))
    result = [0] * length
    for index, value in enumerate(poly_a):
        result[index] += value
    for index, value in enumerate(poly_b):
        result[index] += value
    return trim(result)


def multiply(poly_a, poly_b):
    if poly_a == [0] or poly_b == [0]:
        return [0]
    result = [0] * (len(poly_a) + len(poly_b) - 1)
    for i, value_a in enumerate(poly_a):
        if value_a == 0:
            continue
        for j, value_b in enumerate(poly_b):
            if value_b:
                result[i + j] += value_a * value_b
    return trim(result)


def power(poly, exponent):
    result = [1]
    base = list(poly)
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1
    return result


def divide_exact(numerator, denominator):
    """Polynomial long division, requiring an integer zero remainder."""

    numerator = trim(numerator)
    denominator = trim(denominator)
    if denominator == [0]:
        raise AssertionError("division by zero polynomial")
    if len(numerator) < len(denominator):
        if numerator != [0]:
            raise AssertionError("nonzero polynomial has negative quotient degree")
        return [0]

    work = list(numerator)
    quotient = [0] * (len(numerator) - len(denominator) + 1)
    denominator_degree = len(denominator) - 1
    denominator_lead = denominator[-1]
    while len(work) - 1 >= denominator_degree and work != [0]:
        shift = len(work) - 1 - denominator_degree
        lead, remainder = divmod(work[-1], denominator_lead)
        if remainder:
            raise AssertionError(
                f"non-exact polynomial division at degree {shift + denominator_degree}"
            )
        quotient[shift] += lead
        for index, value in enumerate(denominator):
            work[index + shift] -= lead * value
        work = trim(work)
    if work != [0]:
        raise AssertionError(f"nonzero polynomial division remainder: {work}")
    return trim(quotient)


def one_minus_monomial(n):
    result = [0] * (n + 1)
    result[0] = 1
    result[n] = -1
    return result


def geometric_sum(step, count):
    result = [0] * (step * (count - 1) + 1)
    for index in range(count):
        result[index * step] = 1
    return result


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def mobius(n):
    result = 1
    remaining = n
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            if remaining % prime == 0:
                return 0
            result = -result
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result = -result
    return result


def parameters(e, r):
    a_cap = e * r
    degree = a_cap + 1
    base = (r - 1) * degree + 1
    beta = 3 * r - 2
    chi = e * (3 - e)
    return a_cap, degree, base, beta, chi


def raw_factor_exponents(e, r, contacts):
    """Raw exponents of factors ``(1-t^N)`` in Delta2."""

    a_cap, degree, base, _, chi = parameters(e, r)
    b = len(contacts)
    factors = Counter()
    factors[1] -= 1
    factors[a_cap] += 3 - chi
    factors[r * degree] += b - chi
    factors[degree] += chi - b
    factors[base] -= b
    for q in contacts:
        factors[q * base] += 1
    return {n: exponent for n, exponent in factors.items() if exponent}


def cyclotomic_multiplicities(factors):
    result = Counter()
    for n, exponent in factors.items():
        for divisor in divisors(n):
            result[divisor] += exponent
    return {n: exponent for n, exponent in result.items() if exponent}


def generate_delta(e, r, contacts):
    """Build Delta2 with exact multiply/divide operations."""

    a_cap, degree, base, _, chi = parameters(e, r)
    b = len(contacts)
    delta = power(one_minus_monomial(a_cap), 3 - chi)
    delta = divide_exact(delta, one_minus_monomial(1))
    w_r = divide_exact(
        one_minus_monomial(r * degree), one_minus_monomial(degree)
    )
    delta = multiply(delta, power(w_r, b - chi))
    for q in contacts:
        w_q = divide_exact(
            one_minus_monomial(q * base), one_minus_monomial(base)
        )
        delta = multiply(delta, w_q)
    return delta


def generate_delta_geometrically(e, r, contacts):
    """Build the same polynomial from geometric finite sums."""

    a_cap, degree, base, _, chi = parameters(e, r)
    b = len(contacts)
    delta = multiply(
        power(one_minus_monomial(a_cap), 2 - chi),
        [1] * a_cap,
    )
    delta = multiply(delta, power(geometric_sum(degree, r), b - chi))
    for q in contacts:
        delta = multiply(delta, geometric_sum(base, q))
    return delta


def order_at_one(poly):
    order = 0
    current = list(poly)
    divisor = one_minus_monomial(1)
    while True:
        try:
            current = divide_exact(current, divisor)
        except AssertionError:
            return order
        order += 1


def blind_recover(coefficients):
    """Recover all contact data from the full Delta coefficient list alone."""

    delta = trim(coefficients)
    if not delta or delta[0] != 1:
        raise AssertionError("Delta must have constant coefficient one")

    # P=(1-t)Delta.  Missing coefficients are zero throughout this function.
    p = add(delta, [0] + [-value for value in delta])
    first_nonconstant = next(
        (index for index in range(1, len(p)) if coefficient(p, index)),
        None,
    )
    if first_nonconstant is None:
        raise AssertionError("P has no nonconstant coefficient")
    a_cap = first_nonconstant
    k = -coefficient(p, a_cap)
    if k <= 0:
        raise AssertionError("the first P coefficient must be -k with k>0")

    discriminant = 4 * k - 3
    root = isqrt(discriminant)
    if root * root != discriminant or (3 + root) % 2:
        raise AssertionError("k does not recover an integral e")
    e = (3 + root) // 2
    if e < 3 or e * e - 3 * e + 3 != k:
        raise AssertionError("recovered e is outside the intended range")
    if a_cap % e:
        raise AssertionError("A is not divisible by recovered e")
    r = a_cap // e
    if r < 2:
        raise AssertionError("recovered r is outside the intended range")

    degree = a_cap + 1
    base = (r - 1) * degree + 1
    chi = e * (3 - e)
    n = e * degree
    mu = len(delta) - 1
    mu_tr = a_cap * k + (r - 1) * degree * (n - chi) - 1
    b_from_degree = mu_tr + n - mu

    # The D coefficient of P is b-c; this is a second, local recovery of b.
    b = chi + coefficient(p, degree)
    if b != b_from_degree:
        raise AssertionError(
            f"b recovery disagreement: direct={b}, degree={b_from_degree}"
        )
    if b <= 0 or b > n:
        raise AssertionError("recovered contact count is out of range")

    residual = divide_exact(p, power(one_minus_monomial(a_cap), k))
    for _ in range(b - chi):
        residual = multiply(residual, one_minus_monomial(degree))
        residual = divide_exact(residual, one_minus_monomial(r * degree))

    if coefficient(residual, 0) != 1:
        raise AssertionError("Gamma must have constant coefficient one")
    for index, value in enumerate(residual):
        if value and index % base:
            raise AssertionError(
                f"Gamma coefficient at nonmultiple of B={base}: {index}"
            )
    gamma_degree = n - b
    if len(residual) - 1 != gamma_degree * base:
        raise AssertionError("Gamma degree does not equal B(n-b)")
    gamma = [coefficient(residual, index * base) for index in range(gamma_degree + 1)]
    if gamma[0] != 1:
        raise AssertionError("Gamma(u) must have gamma_0=1")

    # L_m are the coefficients of u Gamma'(u)/Gamma(u).  The recurrence is
    # valid through S+1, which also detects a single contact q=S+1.
    l_values = {}
    for m in range(1, gamma_degree + 2):
        value = m * coefficient(gamma, m)
        value -= sum(
            coefficient(gamma, j) * l_values[m - j]
            for j in range(1, m)
        )
        l_values[m] = value

    higher = {}
    for q in range(2, gamma_degree + 2):
        numerator = sum(
            mobius(q // d) * l_values[d] for d in divisors(q)
        )
        if numerator % q:
            raise AssertionError(f"n_{q} is not integral")
        count = -numerator // q
        if count < 0:
            raise AssertionError(f"n_{q} is negative")
        if count:
            higher[q] = count
    t = coefficient(gamma, 1)
    if coefficient(p, base) != t:
        raise AssertionError(
            f"P[B] does not recover higher-contact count: "
            f"P[B]={coefficient(p, base)}, Gamma'(0)={t}"
        )
    n1 = b - t
    if n1 < 0 or sum(higher.values()) != t:
        raise AssertionError("higher-contact or q=1 count is inconsistent")

    return {
        "e": e,
        "r": r,
        "A": a_cap,
        "D": degree,
        "B": base,
        "c": chi,
        "b": b,
        "mu": mu,
        "gamma_degree": gamma_degree,
        "gamma": gamma,
        "higher": higher,
        "n1": n1,
        "M1": order_at_one(delta),
    }


def contact_counts(contacts):
    counts = Counter(contacts)
    return {q: counts[q] for q in sorted(counts) if q >= 2}


def global_z(e, r, contacts, s):
    a_cap, degree, base, beta, chi = parameters(e, r)
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


def compressed_contact_delta(e, r, contacts, s):
    """Evaluate the U-transform formula with Q=H."""

    _, degree, base, beta, _ = parameters(e, r)
    transverse = (1,) * (e * degree)
    h = r * degree * s + 3 * r + 1
    x = base * s + beta
    counts = Counter(contacts)
    u_x = sum(
        count * (q - 1) / (1 + q * x)
        for q, count in counts.items()
        if q >= 2
    )
    s_zero = sum(
        count * (q - 1)
        for q, count in counts.items()
        if q >= 2
    )
    return (
        global_z(e, r, contacts, s) - global_z(e, r, transverse, s),
        s / ((s + 1) * h)
        * ((r - 1) * s_zero - r * (degree * s + 4) * u_x),
    )


def cubic_compressed_z(r, contacts, s):
    """The e=3 compressed expression, checked against the full Z formula."""

    e = 3
    _, degree, base, beta, _ = parameters(e, r)
    counts = Counter(contacts)
    result = Fraction(4, 1) / (r * s + 1) - Fraction(3, 1) / (s + 1)
    for q, count in counts.items():
        if q < 2:
            continue
        c_q = Fraction(
            (q - 1) * (q * (r - 1) * (3 * r - 2) - (3 * r + 1)),
            3 * r + 1,
        )
        k_q = q * base * s + q * beta + 1
        result += count * c_q * s / ((s + 1) * k_q)
    return result


def check_cubic_compression(r, contacts, sample_points, stats):
    for s in sample_points:
        actual = global_z(3, r, contacts, s)
        compressed = cubic_compressed_z(r, contacts, s)
        if actual != compressed:
            raise AssertionError(f"cubic Z compression failed for r={r}, s={s}")
        stats["cubic_Z"] += 1


def check_h_zero_residue(e, r, contacts, stats):
    """Compute Res_{H=0} Z from the explicit summands and compare its form."""

    if e < 4:
        return
    _, degree, base, beta, chi = parameters(e, r)
    b = len(contacts)
    s0 = -Fraction(3 * r + 1, r * degree)
    a0 = e * r * s0 + 3
    d0 = s0 + 1
    h0 = r * degree * s0 + 3 * r + 1
    if h0 or not a0 or not d0:
        raise AssertionError("unexpected singular-point cancellation data")
    contact_sum = sum(
        Fraction(q - 1, q * base * s0 + q * beta + 1)
        for q in contacts
    )
    # Multiplying the explicit global formula by H and setting H=0 removes
    # only its first summand; the remaining finite expression is exact.
    h_times_z = (
        (3 - chi) * h0 / a0
        + (chi - b) * (r - 1)
        + Fraction(chi, a0)
        + Fraction(chi + b * (r - 1), d0)
        - r * s0 * (degree * s0 + 4) / d0 * contact_sum
    )
    residue = h_times_z / (r * degree)
    delta = Fraction(e - 3, degree)
    u_delta = sum(
        Fraction(count * (q - 1), 1 + q * delta)
        for q, count in Counter(contacts).items()
        if q >= 2
    )
    c_residue = Fraction(
        (3 * r + 1) * (r - 1),
        r * degree * (r * degree - 3 * r - 1),
    )
    expected = c_residue * (e * (degree + e - 3) + b + u_delta)
    if residue != expected or residue <= 0 or expected <= 0:
        raise AssertionError(
            f"H=0 residue failed for (e,r)=({e},{r}), contacts={contacts}"
        )
    stats["H_zero_residue"] += 1


def determinant(vectors):
    (a, b, c), (d, e, f), (g, h, i) = vectors
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def cross(v, w):
    return (
        v[1] * w[2] - v[2] * w[1],
        v[2] * w[0] - v[0] * w[2],
        v[0] * w[1] - v[1] * w[0],
    )


def vector_gcd(v):
    return gcd(gcd(abs(v[0]), abs(v[1])), abs(v[2]))


def dot(v, w):
    return sum(x * y for x, y in zip(v, w))


def check_newton_indices(stats):
    for e in range(3, 6):
        for r in range(2, 5):
            a_cap, degree, base, beta, _ = parameters(e, r)
            for q in range(1, 7):
                x = (a_cap, r, 0)
                y = (degree, 1, 0)
                z = (degree, 0, q)
                u = (1, 0, 0)
                v = (0, 1, 0)
                w = (0, 0, 1)
                normal_r = (r, 1, 0)
                normal_s = (0, q, 1)
                normal_t = (q * (r - 1), q, 1)
                normals = (
                    (u, a_cap, 3),
                    (v, 0, 1),
                    (w, 0, 1),
                    (normal_r, r * degree, 3 * r + 1),
                    (normal_s, q, q + 1),
                    (normal_t, q * base, q * beta + 1),
                )
                for normal, expected_n, expected_nu in normals:
                    if vector_gcd(normal) != 1:
                        raise AssertionError(f"nonprimitive normal: {normal}")
                    actual_n = min(dot(normal, vertex) for vertex in (x, y, z))
                    actual_nu = 3 * normal[0] + normal[1] + normal[2]
                    if (actual_n, actual_nu) != (expected_n, expected_nu):
                        raise AssertionError(
                            f"normal data failed for (e,r,q)=({e},{r},{q})"
                        )
                    stats["newton_normal"] += 1

                vertex_indices = (
                    ((u, w, normal_t), q),
                    ((u, normal_r, normal_t), 1),
                    ((w, normal_s, normal_t), q * q * (r - 1)),
                    ((v, normal_r, normal_t), r),
                    ((v, normal_t, normal_s), q * (r - 1)),
                )
                for rays, expected_index in vertex_indices:
                    actual_index = abs(determinant(rays))
                    if actual_index != expected_index:
                        raise AssertionError(
                            f"vertex index failed for (e,r,q)=({e},{r},{q})"
                        )
                    stats["newton_vertex"] += 1

                edge_indices = (
                    ((w, normal_t), q),
                    ((normal_r, normal_t), 1),
                    ((normal_s, normal_t), q * (r - 1)),
                )
                for rays, expected_index in edge_indices:
                    actual_index = vector_gcd(cross(*rays))
                    if actual_index != expected_index:
                        raise AssertionError(
                            f"edge index failed for (e,r,q)=({e},{r},{q})"
                        )
                    stats["newton_edge"] += 1

                edges = (tuple(y[i] - x[i] for i in range(3)),
                         tuple(z[i] - x[i] for i in range(3)),
                         tuple(z[i] - y[i] for i in range(3)))
                if any(vector_gcd(edge) != 1 for edge in edges):
                    raise AssertionError("compact-face edge is not primitive")
                face_cross = cross(edges[0], edges[1])
                if vector_gcd(face_cross) != 1:
                    raise AssertionError("compact-face cross product is not primitive")
                stats["newton_face"] += 1


def formal_profiles(e, r):
    _, degree, _, _, _ = parameters(e, r)
    total = e * degree
    return (
        ("all1", (1,) * total),
        ("one2", (2,) + (1,) * (total - 2)),
        ("one2/one4", (2, 4) + (1,) * (total - 6)),
        ("two3", (3, 3) + (1,) * (total - 6)),
        ("mixed2/3", (2, 2, 3, 3) + (1,) * (total - 10)),
        ("single-maximal", (total,)),
    )


def check_pair_antichain(records, stats):
    for left_index, left in enumerate(records):
        for right in records[left_index + 1 :]:
            if left["mu"] != right["mu"]:
                if (left["mu"] - right["mu"]) * (
                    left["M_r"] - right["M_r"]
                ) >= 0:
                    raise AssertionError("degree and primitive-r order agree")
                stats["antichain_degree"] += 1
            else:
                if left["delta"] == right["delta"]:
                    raise AssertionError("equal-degree profiles have equal Delta")
                stats["antichain_equal_degree"] += 1


def check_quartic_example(records, stats):
    """Check the two equal-degree quartic formal profiles used in the article."""

    by_label = {record["label"]: record for record in records}
    first = by_label["one2/one4"]
    second = by_label["two3"]
    for record in (first, second):
        if record["mu"] != 419 or record["M_r"] != 43 or record["M1"] != 6:
            raise AssertionError("quartic example degree or multiplicity failed")
        stats["quartic_example"] += 1
    if first["M20"] != 2 or second["M20"] != 0:
        raise AssertionError("quartic example M_20 values failed")
    if first["M30"] != 0 or second["M30"] != 2:
        raise AssertionError("quartic example M_30 values failed")
    stats["quartic_example"] += 2
    if first["gamma"] != [1, 2, 2, 2, 1]:
        raise AssertionError("quartic (2,4) Gamma polynomial failed")
    if second["gamma"] != [1, 2, 3, 2, 1]:
        raise AssertionError("quartic (3,3) Gamma polynomial failed")
    stats["quartic_example"] += 2

    left = multiply(first["delta"], power(one_minus_monomial(30), 2))
    right = multiply(
        second["delta"],
        multiply(one_minus_monomial(20), one_minus_monomial(40)),
    )
    if left != right:
        raise AssertionError("quartic Delta cross-multiplication failed")
    stats["quartic_example"] += 1


def run_audit():
    stats = Counter()
    pairs = ((3, 2), (3, 3), (4, 2), (4, 3), (5, 2))
    sample_points = (Fraction(2, 7), Fraction(5, 11))

    for e, r in pairs:
        records = []
        for label, contacts in formal_profiles(e, r):
            if sum(contacts) != e * (e * r + 1):
                raise AssertionError(f"invalid formal profile: {label}")
            delta = generate_delta(e, r, contacts)
            if delta != generate_delta_geometrically(e, r, contacts):
                raise AssertionError(f"independent Delta builds differ: {label}")
            stats["polynomials"] += 1
            # One division for (1-t), one for W_{r,D}, and one per contact.
            stats["exact_divisions"] += 2 + len(contacts)

            recovered = blind_recover(delta)
            expected_higher = contact_counts(contacts)
            if recovered["e"] != e or recovered["r"] != r:
                raise AssertionError(f"blind (e,r) recovery failed: {label}")
            if recovered["higher"] != expected_higher:
                raise AssertionError(f"blind contact recovery failed: {label}")
            if recovered["n1"] != contacts.count(1):
                raise AssertionError(f"blind q=1 recovery failed: {label}")
            stats["blind_recoveries"] += 1

            a_cap, degree, _, _, chi = parameters(e, r)
            m1 = order_at_one(delta)
            if m1 != 2 - chi or recovered["M1"] != m1:
                raise AssertionError(f"M1 check failed: {label}")
            factors = raw_factor_exponents(e, r, contacts)
            cyclotomic = cyclotomic_multiplicities(factors)
            m_r = cyclotomic.get(r, 0)
            if len(delta) - 1 + m_r - m1 != a_cap ** 3 - a_cap ** 2 + a_cap:
                raise AssertionError(f"mu/M_r/M1 identity failed: {label}")
            stats["spectral_identities"] += 1

            for s in sample_points:
                actual, compressed = compressed_contact_delta(e, r, contacts, s)
                if actual != compressed:
                    raise AssertionError(
                        f"compressed contact transform failed: {label}, s={s}"
                    )
                stats["compressed_Z"] += 1
            if e == 3:
                check_cubic_compression(r, contacts, sample_points, stats)
            else:
                check_h_zero_residue(e, r, contacts, stats)

            records.append(
                {
                    "label": label,
                    "delta": delta,
                    "mu": len(delta) - 1,
                    "M_r": m_r,
                    "M1": m1,
                    "M20": cyclotomic.get(20, 0),
                    "M30": cyclotomic.get(30, 0),
                    "gamma": recovered["gamma"],
                }
            )
        check_pair_antichain(records, stats)
        if (e, r) == (4, 2):
            check_quartic_example(records, stats)

    if stats["antichain_equal_degree"] <= 0:
        raise AssertionError("equal-degree antichain branch was not exercised")
    check_newton_indices(stats)
    print(
        "PASS verify_audited_compression: "
        f"{stats['polynomials']} Delta polynomials; "
        f"{stats['blind_recoveries']} blind recoveries; "
        f"{stats['exact_divisions']} generation divisions; "
        f"{stats['spectral_identities']} M1/Mr identities; "
        f"{stats['compressed_Z']} compressed-Z checks; "
        f"{stats['cubic_Z']} cubic-Z checks; "
        f"{stats['H_zero_residue']} H=0 residue checks; "
        f"{stats['antichain_degree']} antichain degree-order checks; "
        f"{stats['antichain_equal_degree']} equal-degree checks; "
        f"{stats['quartic_example']} quartic-example checks; "
        f"{stats['newton_normal']} Newton-normal checks; "
        f"{stats['newton_vertex']} vertex-index checks; "
        f"{stats['newton_edge']} edge-index checks; "
        f"{stats['newton_face']} primitive-face checks."
    )
    print(
        "Caveat: every contact partition tested is formal numerical data; "
        "the checks do not assert geometric realizability or constitute a proof."
    )


if __name__ == "__main__":
    run_audit()
