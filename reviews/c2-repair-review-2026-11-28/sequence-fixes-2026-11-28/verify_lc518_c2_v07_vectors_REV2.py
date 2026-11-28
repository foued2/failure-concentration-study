#!/usr/bin/env python3
"""Revision 2 deterministic vector and rejection-loop verifier for LC518 C2 v0.7.

This verifies only frozen deterministic selection fixtures. It does not query
drand, validate BLS signatures, create Git refs, or perform a production
selection. The injected rejected digest is a fault-injection value, not claimed
to be a real SHA-256 output.
"""
from __future__ import annotations

import hashlib
import struct

DOMAIN = b"LC518-REV11-C2-v1"
SEED = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
    "101112131415161718191a1b1c1d1e1f"
)
MAX_COUNTER = (1 << 64) - 1
EXPECTED_UNIVERSE_SHA256 = (
    "d5e54cd8a071fde1fd06a897b611fb9d"
    "39bfa28f5aeecb06e46537a2f93149bd"
)

VECTORS = (
    ("repeat-1", 0, 28,
     "996627683d5bd28b1445281d42762ae3c0fafaca315c33deb096582a9970f659", 5),
    ("repeat-1", 1, 28,
     "c59aff206cf93ecd342e7b6a70af095a0e40ff1d3cfffe38e13b74ec70fd0ddb", 23),
    ("repeat-2", 0, 27,
     "bce13a787bba4cf2849ecc7f9291e17459543545a9162f34b0f37a7256474881", 19),
    ("repeat-2", 1, 27,
     "8f096ae539624f40ea1ad9a5bf6272e0673c0e85d33f48971d7719edb55f3561", 13),
)


def digest(label: str, counter: int) -> bytes:
    if not isinstance(label, str) or not label.isascii():
        raise ValueError("label must be an ASCII string")
    if not isinstance(counter, int) or isinstance(counter, bool):
        raise TypeError("counter must be an integer")
    if not 0 <= counter <= MAX_COUNTER:
        raise ValueError("counter must fit uint64")
    message = (
        DOMAIN + b"\x00" + SEED + b"\x00" + label.encode("ascii")
        + b"\x00" + struct.pack(">Q", counter)
    )
    return hashlib.sha256(message).digest()


def rejection_limit(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("universe size n must be a positive integer")
    return ((1 << 256) // n) * n


def select_index(
    label: str,
    n: int,
    *,
    start_counter: int = 0,
    first_digest_override: bytes | None = None,
) -> tuple[int, int, str]:
    """Execute rejection sampling, optionally injecting the first digest.

    The override is consumed only on the first iteration. If rejected, the
    loop computes the real SHA-256 digest for the same label at the incremented
    counter. This tests the actual retry path, not just the boundary arithmetic.
    """
    if not isinstance(start_counter, int) or isinstance(start_counter, bool):
        raise TypeError("start_counter must be an integer")
    if not 0 <= start_counter <= MAX_COUNTER:
        raise ValueError("start_counter must fit uint64")
    if first_digest_override is not None and len(first_digest_override) != 32:
        raise ValueError("injected digest must be exactly 32 bytes")

    counter = start_counter
    override_pending = first_digest_override is not None
    while True:
        raw = first_digest_override if override_pending else digest(label, counter)
        override_pending = False
        assert raw is not None
        x = int.from_bytes(raw, "big", signed=False)
        limit = rejection_limit(n)
        if x < limit:
            return x % n, counter, raw.hex()
        if counter == MAX_COUNTER:
            raise OverflowError("rejected digest at uint64 maximum; counter must not wrap")
        counter += 1


def universe() -> list[str]:
    return [
        f"M{i:02d}/M{j:02d}"
        for i in range(1, 9)
        for j in range(i + 1, 9)
    ]


def check(condition: bool, label: str, detail: str) -> None:
    if not condition:
        raise AssertionError(f"FAIL {label}: {detail}")
    print(f"PASS {label}: {detail}")


def main() -> None:
    checks = 0

    pairs = universe()
    encoded = ("\n".join(pairs) + "\n").encode("ascii")
    got_hash = hashlib.sha256(encoded).hexdigest()
    check(
        len(pairs) == 28 and len(encoded) == 224
        and got_hash == EXPECTED_UNIVERSE_SHA256,
        "01 universe",
        f"count={len(pairs)} bytes={len(encoded)} sha256={got_hash}",
    )
    checks += 1

    for number, (label, counter, n, expected_hex, expected_index) in enumerate(VECTORS, start=2):
        raw_hex = digest(label, counter).hex()
        index, used_counter, selected_hex = select_index(
            label, n, start_counter=counter
        )
        check(
            raw_hex == expected_hex and selected_hex == expected_hex
            and index == expected_index and used_counter == counter,
            f"{number:02d} vector {label} counter={counter}",
            f"n={n} index={index} sha256={selected_hex}",
        )
        checks += 1

    first_index, _, _ = select_index("repeat-1", 28)
    first_pair = pairs[first_index]
    remaining = [pair for pair in pairs if pair != first_pair]
    second_index, _, _ = select_index("repeat-2", 27)
    second_pair = remaining[second_index]
    check(
        first_pair == "M01/M07" and second_pair == "M04/M07"
        and first_pair != second_pair,
        "06 normal two-stage fixture",
        f"first={first_pair} second={second_pair}",
    )
    checks += 1

    rejected = (1 << 256) - 16
    check(
        rejection_limit(28) == rejected and rejection_limit(27) == rejected
        and rejected >= rejection_limit(28) and rejected >= rejection_limit(27),
        "07 rejection boundary",
        "injected x=2^256-16 is rejected for n=28 and n=27",
    )
    checks += 1

    injected = rejected.to_bytes(32, "big")
    retry_one_index, retry_one_counter, retry_one_hex = select_index(
        "repeat-1", 28, first_digest_override=injected
    )
    check(
        retry_one_counter == 1 and retry_one_hex == VECTORS[1][3]
        and retry_one_index == VECTORS[1][4],
        "08 repeat-1 executed rejection/counter advance",
        f"injected counter=0 rejected; accepted counter={retry_one_counter} "
        f"index={retry_one_index} sha256={retry_one_hex}",
    )
    checks += 1

    retry_two_index, retry_two_counter, retry_two_hex = select_index(
        "repeat-2", 27, first_digest_override=injected
    )
    check(
        retry_two_counter == 1 and retry_two_hex == VECTORS[3][3]
        and retry_two_index == VECTORS[3][4],
        "09 repeat-2 executed rejection/counter advance",
        f"injected counter=0 rejected; accepted counter={retry_two_counter} "
        f"index={retry_two_index} sha256={retry_two_hex}",
    )
    checks += 1

    overflowed = False
    try:
        select_index(
            "repeat-1",
            28,
            start_counter=MAX_COUNTER,
            first_digest_override=injected,
        )
    except OverflowError:
        overflowed = True
    check(
        overflowed,
        "10 uint64 counter overflow",
        "rejection at 2^64-1 raises; counter does not wrap",
    )
    checks += 1

    assert checks == 10, checks
    print(
        f"RESULT: {checks} checks passed; no drand query; no BLS verification; "
        "no production selection"
    )


if __name__ == "__main__":
    main()
