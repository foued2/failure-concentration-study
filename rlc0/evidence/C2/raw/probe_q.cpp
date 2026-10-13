extern "C" void __CPROVER_assume(int);
extern "C" void __CPROVER_assert(int, const char*);

int main() {
    int n;
    int buf[10000];
    int target;
    __CPROVER_assume(n >= 1 && n <= 10000);
    __CPROVER_assume(target > -10000 && target < 10000);
    __CPROVER_assume(__CPROVER_forall(unsigned i; i < (unsigned)n ==> (buf[i] > -10000 && buf[i] < 10000)));
    __CPROVER_assume(__CPROVER_forall(unsigned i; i + 1 < (unsigned)n ==> buf[i] < buf[i + 1]));
    __CPROVER_assert(n == 10000, "P1 top-of-domain reachable (expect FAILURE with n=10000 witness)");
    __CPROVER_assert(n < 2 || buf[0] < buf[1], "P2 strict-increase constraint propagated (expect SUCCESS)");
    return 0;
}
