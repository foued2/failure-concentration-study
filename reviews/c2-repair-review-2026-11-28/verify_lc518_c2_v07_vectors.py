#!/usr/bin/env python3
"""Independent standard-library check of LC518 C2 v0.7 selection vectors.

This verifies only the deterministic pair-universe and hash-framing fixtures.
It does not fetch drand, verify a beacon, or perform a production selection.
"""
from __future__ import annotations

import hashlib
import struct

DOMAIN = b"LC518-REV11-C2-v1"
SEED = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
    "101112131415161718191a1b1c1d1e1f"
)
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
    if not 0 <= counter <= (1 << 64) - 1:
        raise ValueError("counter must fit uint64")
    message = (
        DOMAIN + b"\x00" + SEED + b"\x00" + label.encode("ascii")
        + b"\x00" + struct.pack(">Q", counter)
    )
    return hashlib.sha256(message).digest()


def universe() -> list[str]:
    return [
        f"M{i:02d}/M{j:02d}"
        for i in range(1, 9)
        for j in range(i + 1, 9)
    ]


def main() -> None:
    pairs = universe()
    encoded = ("\n".join(pairs) + "\n").encode("ascii")
    got_hash = hashlib.sha256(encoded).hexdigest()
    assert len(pairs) == 28, len(pairs)
    assert len(encoded) == 224, len(encoded)
    assert got_hash == EXPECTED_UNIVERSE_SHA256, got_hash
    print(f"PASS universe count={len(pairs)} bytes={len(encoded)} sha256={got_hash}")

    for label, counter, n, expected_hex, expected_index in VECTORS:
        raw = digest(label, counter)
        got_hex = raw.hex()
        x = int.from_bytes(raw, "big")
        limit = ((1 << 256) // n) * n
        assert got_hex == expected_hex, (label, counter, got_hex)
        assert x < limit, (label, counter, "vector unexpectedly rejected")
        index = x % n
        assert index == expected_index, (label, counter, index)
        print(f"PASS {label} counter={counter} n={n} index={index} sha256={got_hex}")

    first_index = int.from_bytes(digest("repeat-1", 0), "big") % 28
    first_pair = pairs[first_index]
    reduced = [pair for pair in pairs if pair != first_pair]
    second_index = int.from_bytes(digest("repeat-2", 0), "big") % 27
    second_pair = reduced[second_index]
    assert first_pair == "M01/M07", first_pair
    assert second_pair == "M04/M07", second_pair
    assert first_pair != second_pair
    print(f"PASS normal fixture pairs={first_pair},{second_pair}")

    # Check the first rejected integer for n=28 and n=27.
    rejected = (1 << 256) - 16
    for n in (28, 27):
        limit = ((1 << 256) // n) * n
        assert limit == rejected
        assert rejected >= limit
    print("PASS rejection boundary L=2^256-16 for n=28 and n=27")
    print("RESULT: 7 checks passed; no beacon fetched; no production selection performed")


if __name__ == "__main__":
    main()
