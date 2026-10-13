#include "proof_harness.h"

int main() {
    rlc0_input in;
    in.present = 0;
    rlc0_build(&in);
    __CPROVER_assert(in.n == 10000, "D1 top of domain reachable (expect FAILURE, witness n=10000)");
    __CPROVER_assert(in.n <= 10000, "D2 upper bound enforced (expect SUCCESS)");
    __CPROVER_assert(!(in.n >= 2 && in.buf[0] >= in.buf[1]), "D3 strict increase active (expect SUCCESS)");
    __CPROVER_assert(!(in.buf[0] < -10000 || in.buf[0] > 10000), "D4 element range active (expect SUCCESS)");
    if (in.n == 1 && in.target == in.buf[0]) {
        __CPROVER_assert(in.present == 1, "D5 presence flag set (expect SUCCESS)");
    }
    if (in.n == 2 && in.target != in.buf[0] && in.target != in.buf[1]) {
        __CPROVER_assert(in.present == 0, "D6 presence flag clear (expect SUCCESS)");
    }
    if (in.n == 10000) {
        __CPROVER_assert(in.buf[9999] > -10000 && in.buf[9999] < 10000, "D7 last element constrained at n=10000 (expect SUCCESS)");
        __CPROVER_assert(in.buf[9998] < in.buf[9999], "D8 last pair strictly increasing at n=10000 (expect SUCCESS)");
        if (in.target == in.buf[9999]) {
            __CPROVER_assert(in.present == 1, "D9 presence flag set at last index (expect SUCCESS)");
        }
    }
    return 0;
}
