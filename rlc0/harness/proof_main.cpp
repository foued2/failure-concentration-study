#ifndef RLC0_SOLVER_HEADER
#error "RLC0_SOLVER_HEADER must be defined, e.g. /DRLC0_SOLVER_HEADER=canary_n63.h"
#endif
#define RLC0_STRINGIFY2(x) #x
#define RLC0_STRINGIFY(x) RLC0_STRINGIFY2(x)
#include RLC0_STRINGIFY(RLC0_SOLVER_HEADER)
#include "proof_harness.h"

int main() {
    rlc0_input in;
    in.present = 0;
    rlc0_build(&in);
#if defined(OBL_IN_F)
    __CPROVER_assume(in.present == 1);
#elif defined(OBL_D_F)
    __CPROVER_assume(in.present == 0);
#elif defined(OBL_FULL_D)
#else
#error "exactly one of OBL_IN_F / OBL_D_F / OBL_FULL_D must be defined"
#endif
    std::vector<int> v;
    v.m_data = in.buf;
    v.m_size = static_cast<rlc0_size_t>(in.n);
    Solution s;
    int r = s.search(v, in.target);
    rlc0_assert_correct(r, in.n, in.buf, in.target, in.present);
    return 0;
}
