void __CPROVER_assume(int);
void __CPROVER_assert(int, const char*);

int main() {
    int n;
    int buf[10000];
    __CPROVER_assume(n >= 1 && n <= 10000);
    __CPROVER_assume(__CPROVER_forall(unsigned i; i < (unsigned)n ==> (buf[i] > -10000 && buf[i] < 10000)));
    __CPROVER_assert(n != 10000, "C-mode quantifier (expect FAILURE with n=10000)");
    return 0;
}
