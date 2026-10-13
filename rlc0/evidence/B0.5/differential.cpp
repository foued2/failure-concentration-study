#include <vector>
#include <stdio.h>

#ifdef RLC0_MODEL_BUILD
static void fill(std::vector<int>& v, const int* a, int n) {
    v.m_data = const_cast<int*>(a);
    v.m_size = n;
}
#else
static void fill(std::vector<int>& v, const int* a, int n) {
    for (int i = 0; i < n; i++) v.push_back(a[i]);
}
#endif

static void run_case(int k, const int* a, int n) {
    std::vector<int> v;
    fill(v, a, n);
    long long sum = 0;
    for (int i = 0; i < (int)v.size(); i++) sum += v[i];
    int found_target = v[n / 2];
    int found = -1;
    for (int i = 0; i < (int)v.size(); i++) {
        if (v[i] == found_target) {
            found = i;
            break;
        }
    }
    int maxv = v[0];
    int minv = v[0];
    for (int i = 0; i < (int)v.size(); i++) {
        if (v[i] > maxv) maxv = v[i];
        if (v[i] < minv) minv = v[i];
    }
    int absent_target = (maxv + 1 < 10000) ? maxv + 1 : minv - 1;
    int absent = -1;
    for (int i = 0; i < (int)v.size(); i++) {
        if (v[i] == absent_target) {
            absent = i;
            break;
        }
    }
    const std::vector<int>& cv = v;
    long long csum = 0;
    for (int i = 0; i < (int)cv.size(); i++) csum += cv[i];
    printf("c%d n=%d sum=%lld found=%d absent=%d csum=%lld\n",
           k, (int)v.size(), sum, found, absent, csum);
}

int main() {
    int buf[10000];
    int case_n[] = {1, 2, 3, 7, 8, 9, 15, 16, 17, 64, 1000, 9999, 10000};
    int case_base[] = {-5, -7, 0, 1, -3, 4, -2, 0, 7, -50, -100, -4999, -9999};
    int k = 0;
    for (int c = 0; c < 13; c++) {
        int n = case_n[c];
        int base = case_base[c];
        for (int i = 0; i < n; i++) buf[i] = base + i;
        run_case(k++, buf, n);
    }
    int w1[] = {1};
    run_case(k++, w1, 1);
    int w4[] = {0, 1, 2, 3, 4, 5, 6, 7};
    run_case(k++, w4, 8);
    int w5[] = {0};
    run_case(k++, w5, 1);
    int w6[] = {0, 2};
    run_case(k++, w6, 2);
    printf("done %d cases\n", k);
    return 0;
}
