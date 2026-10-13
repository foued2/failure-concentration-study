extern "C" void __CPROVER_assume(int);
extern "C" void __CPROVER_assert(int, const char*);
int main() {
    unsigned n;
    __CPROVER_assume(n <= 10);
    __CPROVER_assume(__CPROVER_forall(unsigned i; i < 10 ==> i != n));
    __CPROVER_assert(n != 3, "Qd-cpp");
    return 0;
}
