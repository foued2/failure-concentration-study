extern "C" void __CPROVER_assume(int);

#include <vector>

struct rlc0_input {
    int n;
    int buf[10000];
    int target;
    int present;
};

static void rlc0_build(rlc0_input* p) {
    __CPROVER_assume(p->n >= 1 && p->n <= 10000);
    __CPROVER_assume(p->target > -10000 && p->target < 10000);
    for (int i = 0; i < 10000; i++) {
        if (i < p->n) {
            __CPROVER_assume(p->buf[i] > -10000 && p->buf[i] < 10000);
            if (i + 1 < p->n) {
                __CPROVER_assume(p->buf[i] < p->buf[i + 1]);
            }
            if (p->buf[i] == p->target) {
                p->present = 1;
            }
        }
    }
}

static void rlc0_assert_correct(int r, int n, const int* buf, int target, int present) {
    if (r == -1) {
        __CPROVER_assert(!present, "rlc0: returned -1 but target is present");
    } else {
        __CPROVER_assert(r >= 0 && r < n, "rlc0: return value outside [0, n)");
        if (r >= 0 && r < n) {
            __CPROVER_assert(buf[r] == target, "rlc0: return index does not contain target");
        }
    }
}
