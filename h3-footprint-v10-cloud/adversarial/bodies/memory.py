"""HOSTILE TEST BODY: bounded memory pressure. Allocates at most 60 x 10 MiB of untouched bytearrays (calloc).
Returns number of blocks allocated before MemoryError; -60 means no limit stopped it."""


def solve(n, edges, s, t):
    if n == 5:
        blocks = []
        try:
            for _ in range(60):
                blocks.append(bytearray(10 * 1024 * 1024))
        except MemoryError:
            return len(blocks)
        return -len(blocks)
    return 2
