extern "C" void __CPROVER_assume(int);
extern "C" void __CPROVER_assert(int, const char*);

int main() {
    int n;
    int buf[10000];
    int target;
    int mode;
    __CPROVER_assume(n >= 1 && n <= 10000);
    __CPROVER_assume(target > -10000 && target < 10000);
    __CPROVER_assume(__CPROVER_forall(unsigned i; i < (unsigned)n ==> (buf[i] > -10000 && buf[i] < 10000)));
    __CPROVER_assume(__CPROVER_forall(unsigned i; i + 1 < (unsigned)n ==> buf[i] < buf[i + 1]));
    if (mode) {
        __CPROVER_assume(__CPROVER_exists(unsigned i; i < (unsigned)n && buf[i] == target));
        __CPROVER_assert(0, "F1 F-split reachable (expect FAILURE with present-target witness)");
    } else {
        __CPROVER_assume(__CPROVER_forall(unsigned i; i < (unsigned)n ==> buf[i] != target));
        __CPROVER_assert(0, "DF1 D-minus-F split reachable (expect FAILURE with absent-target witness)");
    }
    return 0;
}
