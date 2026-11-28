#!/usr/bin/env python3
"""Revision 3 deterministic vector and rejection-loop verifier for LC518 C2 v0.7.

Scope: frozen deterministic selection fixtures and rejection-sampling control flow.
This program does not query drand, verify BLS signatures, inspect GitHub Activity,
create Git refs, exercise an HTTP client, or perform a production selection.
Injected 256-bit candidates are explicit fault-injection values, not SHA-256 outputs.
"""
from __future__ import annotations

import hashlib
import struct
from collections.abc import Sequence

DOMAIN = b"LC518-REV11-C2-v1"
SEED = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
    "101112131415161718191a1b1c1d1e1f"
)
MAX_COUNTER = (1 << 64) - 1
U256 = 1 << 256
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

REPEAT_COUNTER_2 = {
    "repeat-1": (28, "d560753b262a38e0febea4886029ec8115e209879c56b118d3913b0bba97298b", 11),
    "repeat-2": (27, "e1df82a6608189025ba55fa1666a80936bcb64042cf6099df9a7787d357c1de5", 16),
}


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
    return (U256 // n) * n


def select_index(
    label: str,
    n: int,
    *,
    start_counter: int = 0,
    digest_overrides: Sequence[bytes] = (),
) -> tuple[int, int, str]:
    """Run rejection sampling, optionally overriding successive candidates.

    Overrides are consumed one per loop iteration. After the override sequence is
    exhausted, normal SHA-256 candidates are computed for the current counter.
    """
    if not isinstance(start_counter, int) or isinstance(start_counter, bool):
        raise TypeError("start_counter must be an integer")
    if not 0 <= start_counter <= MAX_COUNTER:
        raise ValueError("start_counter must fit uint64")
    if isinstance(digest_overrides, (bytes, bytearray, str)):
        raise TypeError("digest_overrides must be a sequence of 32-byte candidates")
    overrides = tuple(digest_overrides)
    if any(not isinstance(value, bytes) or len(value) != 32 for value in overrides):
        raise ValueError("each injected candidate must be exactly 32 bytes")

    counter = start_counter
    while True:
        offset = counter - start_counter
        raw = overrides[offset] if offset < len(overrides) else digest(label, counter)
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
        index, used_counter, selected_hex = select_index(label, n, start_counter=counter)
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
    limit_28 = rejection_limit(28)
    limit_27 = rejection_limit(27)
    check(
        limit_28 == rejected and limit_27 == rejected,
        "07 rejection-threshold arithmetic only",
        "L(28)=L(27)=2^256-16; this check does not execute the loop",
    )
    checks += 1

    accepted_candidate = (rejected - 1).to_bytes(32, "big")
    for number, (label, n) in enumerate((("repeat-1", 28), ("repeat-2", 27)), start=8):
        index, used_counter, selected_hex = select_index(
            label, n, digest_overrides=(accepted_candidate,)
        )
        check(
            index == n - 1 and used_counter == 0
            and selected_hex == accepted_candidate.hex(),
            f"{number:02d} x=L-1 accepted for {label}",
            f"n={n} index={index} counter={used_counter}",
        )
        checks += 1

    injected_rejection = rejected.to_bytes(32, "big")
    for number, (label, n, expected_hex, expected_index) in enumerate(
        (("repeat-1", 28, REPEAT_COUNTER_2["repeat-1"][1], REPEAT_COUNTER_2["repeat-1"][2]),
         ("repeat-2", 27, REPEAT_COUNTER_2["repeat-2"][1], REPEAT_COUNTER_2["repeat-2"][2])),
        start=10,
    ):
        index, used_counter, selected_hex = select_index(
            label, n, digest_overrides=(injected_rejection, injected_rejection)
        )
        check(
            used_counter == 2 and selected_hex == expected_hex and index == expected_index,
            f"{number:02d} two consecutive rejections then real digest for {label}",
            f"injected counters 0 and 1 rejected; accepted counter=2 index={index} sha256={selected_hex}",
        )
        checks += 1

    for number, (label, n, expected_hex, expected_index) in enumerate(
        (("repeat-1", 28, VECTORS[1][3], VECTORS[1][4]),
         ("repeat-2", 27, VECTORS[3][3], VECTORS[3][4])),
        start=12,
    ):
        index, used_counter, selected_hex = select_index(
            label, n, digest_overrides=(injected_rejection,)
        )
        check(
            used_counter == 1 and selected_hex == expected_hex and index == expected_index,
            f"{number:02d} one rejection and counter advance for {label}",
            f"injected counter 0 rejected; accepted counter=1 index={index} sha256={selected_hex}",
        )
        checks += 1

    overflowed = False
    try:
        select_index(
            "repeat-1", 28, start_counter=MAX_COUNTER,
            digest_overrides=(injected_rejection,),
        )
    except OverflowError:
        overflowed = True
    check(
        overflowed,
        "14 uint64 counter overflow",
        "rejection at 2^64-1 raises; counter does not wrap",
    )
    checks += 1

    assert checks == 14, checks
    print(
        f"RESULT: {checks} checks passed; no drand query; no BLS verification; "
        "no HTTP client test; no GitHub Activity test; no production selection"
    )


if __name__ == "__main__":
    main()
