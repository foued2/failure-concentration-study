"""Deterministic arithmetic checks for the concentration math specification.

This is NOT a simulation. It makes no random draws, does not generate solvers,
does not read or change an input bank, and does not call any model/API. It
calculates only the illustrative score and concentration examples in
09_CONCENTRATION_MATHEMATICAL_SPEC.md using the standard library.
"""

from fractions import Fraction

EVAL_FAMILY_SIZES = (9, 9, 23, 23, 31, 3)
N_EVAL = sum(EVAL_FAMILY_SIZES)
N_FAMILIES = len(EVAL_FAMILY_SIZES)


def diagnostic_summary(profile: tuple[int, ...]) -> tuple[int, float | None]:
    """Return (k, C); C is None when k=0."""
    if len(profile) != N_FAMILIES:
        raise ValueError("profile must have six family counts")
    if any((not isinstance(x, int)) or x < 0 or x > 5 for x in profile):
        raise ValueError("diagnostic counts must be integers from 0 to 5")
    k = sum(profile)
    return k, (max(profile) / k if k > 0 else None)


def evaluation_scores(failures: tuple[int, ...]) -> tuple[Fraction, Fraction]:
    """Return exact (domain-weighted score, equal-family score)."""
    if len(failures) != N_FAMILIES:
        raise ValueError("evaluation failure vector must have six entries")
    if any(
        (not isinstance(x, int)) or x < 0 or x > cap
        for x, cap in zip(failures, EVAL_FAMILY_SIZES)
    ):
        raise ValueError("evaluation failures must be integers within family sizes")

    domain_score = Fraction(N_EVAL - sum(failures), N_EVAL)
    equal_family_score = 1 - sum(
        (Fraction(x, cap) for x, cap in zip(failures, EVAL_FAMILY_SIZES)),
        Fraction(0, 1),
    ) / N_FAMILIES
    return domain_score, equal_family_score


def main() -> None:
    profiles = {
        "localized": (5, 0, 0, 0, 0, 0),
        "spread": (1, 1, 1, 1, 1, 0),
        "same-C profile A": (2, 2, 1, 0, 0, 0),
        "same-C profile B": (2, 1, 1, 1, 0, 0),
        "k=0 reference": (0, 0, 0, 0, 0, 0),
    }

    print("DIAGNOSTIC PROFILES")
    print("profile                 k     C")
    for name, profile in profiles.items():
        k, concentration = diagnostic_summary(profile)
        c_text = "undefined" if concentration is None else f"{concentration:.6f}"
        print(f"{name:22s} {k:2d}  {c_text}")

    print("\nONE ENTIRE EVALUATION FAMILY FAILS")
    print("family-size  domain-score  equal-family-score")
    for family_size in sorted(set(EVAL_FAMILY_SIZES)):
        family_index = EVAL_FAMILY_SIZES.index(family_size)
        e = tuple(
            cap if j == family_index else 0
            for j, cap in enumerate(EVAL_FAMILY_SIZES)
        )
        domain_score, equal_score = evaluation_scores(e)
        print(
            f"{family_size:11d}  {float(domain_score):.6f}      "
            f"{float(equal_score):.6f}"
        )

    print("\nSAME DIAGNOSTICS, DIFFERENT POSSIBLE EVALUATION OUTCOMES")
    outcomes = {
        "no evaluation failures": (0, 0, 0, 0, 0, 0),
        "all failures in family 1": (9, 0, 0, 0, 0, 0),
        "all evaluation inputs fail": EVAL_FAMILY_SIZES,
    }
    for name, e in outcomes.items():
        domain_score, equal_score = evaluation_scores(e)
        print(
            f"{name:31s} domain={float(domain_score):.6f}  "
            f"equal-family={float(equal_score):.6f}"
        )

    # Exact, deterministic checks on the values cited in the specification.
    assert diagnostic_summary(profiles["localized"]) == (5, 1.0)
    assert diagnostic_summary(profiles["spread"]) == (5, 0.2)
    assert diagnostic_summary(profiles["same-C profile A"]) == (5, 0.4)
    assert diagnostic_summary(profiles["same-C profile B"]) == (5, 0.4)
    assert diagnostic_summary(profiles["k=0 reference"]) == (0, None)

    domain, equal = evaluation_scores((9, 0, 0, 0, 0, 0))
    assert domain == Fraction(89, 98)
    assert equal == Fraction(5, 6)
    assert evaluation_scores((0, 0, 0, 0, 0, 0)) == (Fraction(1), Fraction(1))
    assert evaluation_scores(EVAL_FAMILY_SIZES) == (Fraction(0), Fraction(0))

    print("\nCHECKS: PASS (deterministic arithmetic only)")


if __name__ == "__main__":
    main()
