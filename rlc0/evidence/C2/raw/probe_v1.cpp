extern "C" void __CPROVER_assume(int);
extern "C" void __CPROVER_assert(int, const char*);

int main() {
    int n;
    int buf[10000];
    unsigned i;
    __CPROVER_assume(n >= 1 && n <= 10000);
    __CPROVER_assume(__CPROVER_forall(i; i < (unsigned)n ==> (buf[i] > -10000 && buf[i] < 10000)));
    __CPROVER_assert(n != 10000, "V1 pre-declared quantifier (expect FAILURE with n=10000)");
    return 0;
}
