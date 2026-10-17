# O2 exact feasibility calculation (pre-freeze, temporary)

- Status: TEMPORARY. Not published, no repo changes, no commit.
- Interpreter: 3.14.0 (main, Nov 19 2025, 22:43:52) [MSC v.1944 64 bit (AMD64)]
- Generated (UTC): 2026-10-17T12:16:57.554763+00:00
- Event: S1-m4 support + TrainRa (tra,tb>=1; tra+tb>=8) + CVD
  (both readings) + test tea,teb>=1 and tea+teb>=8 (B_split=8).
- Excluded: matrix rank/conditioning criterion; 3-bucket scenarios;
  attempt-budget modeling; validity/dedup modeling.

| scen | N | T0 (no CVD) | P(atleastone) | P(each) | A1 lib ref | A1 cons ref |
|---|---|---|---|---|---|---|
| a-50:50 | 113 | 0.02717949558 | 0.02717932953 | 0.02680785173 | 0.2226954628 | 6.494216202e-08 |
| a-50:50 | 150 | 0.1611214183 | 0.1611211321 | 0.1602358625 | 0.5831837129 | 1.250131202e-05 |
| a-50:50 | 450 | 0.9964473887 | 0.9964473887 | 0.9964461587 | 0.9996787765 | 0.3713456684 |
| a-50:50 | 600 | 0.9999294941 | 0.9999294941 | 0.999929479 | 0.9999832026 | 0.7749382298 |
| a-hist | 113 | 0.01484337922 | 0.01484329972 | 0.01464728902 | 0.1084602013 | 2.493999584e-08 |
| a-hist | 150 | 0.1065408825 | 0.1065407252 | 0.1058959492 | 0.346303811 | 4.847083197e-06 |
| a-hist | 450 | 0.9927130036 | 0.9927130036 | 0.9926841197 | 0.9957626627 | 0.1776201779 |
| a-hist | 600 | 0.999461965 | 0.999461965 | 0.999460474 | 0.9995130092 | 0.4695528107 |
| c-50:50 | 113 | 4.878662324e-07 | 4.878483997e-07 | 4.592630611e-07 | 1.629518117e-05 | 2.95961931e-16 |
| c-50:50 | 150 | 2.023029613e-05 | 2.022962067e-05 | 1.922527556e-05 | 0.0004361227638 | 4.415359518e-13 |
| c-50:50 | 450 | 0.1640256015 | 0.164025203 | 0.1630599526 | 0.5733690784 | 4.236859149e-05 |
| c-50:50 | 600 | 0.4492996571 | 0.4492995336 | 0.4486203728 | 0.8660282462 | 0.001065273221 |
| c-hist | 113 | 3.582909786e-07 | 3.582778252e-07 | 3.373788434e-07 | 1.186246626e-05 | 2.124723212e-16 |
| c-hist | 150 | 1.504471973e-05 | 1.504421524e-05 | 1.430304434e-05 | 0.0003197288974 | 3.17155711e-13 |
| c-hist | 450 | 0.1454618657 | 0.1454615251 | 0.1445754025 | 0.4882543948 | 3.063961796e-05 |
| c-hist | 600 | 0.4253012651 | 0.4253011503 | 0.4245239303 | 0.8015943891 | 0.0007740640776 |

## checks

- [x] F5 equals FTABLE entry -- f_s1 is the FTABLE builder for S1-m4
- [x] V2 H5(n,1) == F5(n) all n (rel) -- worst rel dev 2.912e-15
- [x] V2 H10(n,1) == F10(n) all n (rel) -- worst rel dev 1.313e-15
- [x] V2 H5 <= F5 pointwise -- 0 violations
- [x] V1 direct==RS real a-hist N=16 -- max abs dev 0.000e+00
- [x] V1 brute F5==analytic N=16 -- 5.995e-15
- [x] V1 brute H5==analytic N=16 -- 5.107e-15
- [x] V1 brute F10==analytic N=16 -- 3.442e-15
- [x] V1 brute H10==analytic N=16 -- 3.775e-15
- [x] V1 direct==RS harness N=16 -- max abs dev 0.000e+00
- [x] V1 direct==RS real a-hist N=20 -- max abs dev 0.000e+00
- [x] V1 brute F5==analytic N=20 -- 1.099e-14
- [x] V1 brute H5==analytic N=20 -- 9.437e-15
- [x] V1 brute F10==analytic N=20 -- 3.442e-15
- [x] V1 brute H10==analytic N=20 -- 4.219e-15
- [x] V1 direct==RS harness N=20 -- max abs dev 0.000e+00
- [x] V1 direct==RS real a-hist N=32 -- max abs dev 2.275e-24
- [x] V1 brute F5==analytic N=32 -- 3.120e-14
- [x] V1 brute H5==analytic N=32 -- 2.986e-14
- [x] V1 brute F10==analytic N=32 -- 6.217e-15
- [x] V1 brute H10==analytic N=32 -- 4.441e-15
- [x] V1 direct==RS harness N=32 -- max abs dev 2.168e-17
- [x] V4 cons<=T0<=lib a-hist@113 -- cons=2.494000e-08 T0=1.484338e-02 lib=1.084602e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 a-hist@113 -- P_each=1.464729e-02 P_one=1.484330e-02 T0=1.484338e-02
- [x] V4 cons<=T0<=lib a-hist@150 -- cons=4.847083e-06 T0=1.065409e-01 lib=3.463038e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 a-hist@150 -- P_each=1.058959e-01 P_one=1.065407e-01 T0=1.065409e-01
- [x] V4 cons<=T0<=lib a-hist@450 -- cons=1.776202e-01 T0=9.927130e-01 lib=9.957627e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 a-hist@450 -- P_each=9.926841e-01 P_one=9.927130e-01 T0=9.927130e-01
- [x] V4 cons<=T0<=lib a-hist@600 -- cons=4.695528e-01 T0=9.994620e-01 lib=9.995130e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 a-hist@600 -- P_each=9.994605e-01 P_one=9.994620e-01 T0=9.994620e-01
- [x] V4 cons<=T0<=lib a-50:50@113 -- cons=6.494216e-08 T0=2.717950e-02 lib=2.226955e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 a-50:50@113 -- P_each=2.680785e-02 P_one=2.717933e-02 T0=2.717950e-02
- [x] V4 cons<=T0<=lib a-50:50@150 -- cons=1.250131e-05 T0=1.611214e-01 lib=5.831837e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 a-50:50@150 -- P_each=1.602359e-01 P_one=1.611211e-01 T0=1.611214e-01
- [x] V4 cons<=T0<=lib a-50:50@450 -- cons=3.713457e-01 T0=9.964474e-01 lib=9.996788e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 a-50:50@450 -- P_each=9.964462e-01 P_one=9.964474e-01 T0=9.964474e-01
- [x] V4 cons<=T0<=lib a-50:50@600 -- cons=7.749382e-01 T0=9.999295e-01 lib=9.999832e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 a-50:50@600 -- P_each=9.999295e-01 P_one=9.999295e-01 T0=9.999295e-01
- [x] V4 cons<=T0<=lib c-hist@113 -- cons=2.124723e-16 T0=3.582910e-07 lib=1.186247e-05
- [x] V5 order 0<=P_each<=P_atleastone<=T0 c-hist@113 -- P_each=3.373788e-07 P_one=3.582778e-07 T0=3.582910e-07
- [x] V4 cons<=T0<=lib c-hist@150 -- cons=3.171557e-13 T0=1.504472e-05 lib=3.197289e-04
- [x] V5 order 0<=P_each<=P_atleastone<=T0 c-hist@150 -- P_each=1.430304e-05 P_one=1.504422e-05 T0=1.504472e-05
- [x] V4 cons<=T0<=lib c-hist@450 -- cons=3.063962e-05 T0=1.454619e-01 lib=4.882544e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 c-hist@450 -- P_each=1.445754e-01 P_one=1.454615e-01 T0=1.454619e-01
- [x] V4 cons<=T0<=lib c-hist@600 -- cons=7.740641e-04 T0=4.253013e-01 lib=8.015944e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 c-hist@600 -- P_each=4.245239e-01 P_one=4.253012e-01 T0=4.253013e-01
- [x] V4 cons<=T0<=lib c-50:50@113 -- cons=2.959619e-16 T0=4.878662e-07 lib=1.629518e-05
- [x] V5 order 0<=P_each<=P_atleastone<=T0 c-50:50@113 -- P_each=4.592631e-07 P_one=4.878484e-07 T0=4.878662e-07
- [x] V4 cons<=T0<=lib c-50:50@150 -- cons=4.415360e-13 T0=2.023030e-05 lib=4.361228e-04
- [x] V5 order 0<=P_each<=P_atleastone<=T0 c-50:50@150 -- P_each=1.922528e-05 P_one=2.022962e-05 T0=2.023030e-05
- [x] V4 cons<=T0<=lib c-50:50@450 -- cons=4.236859e-05 T0=1.640256e-01 lib=5.733691e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 c-50:50@450 -- P_each=1.630600e-01 P_one=1.640252e-01 T0=1.640256e-01
- [x] V4 cons<=T0<=lib c-50:50@600 -- cons=1.065273e-03 T0=4.492997e-01 lib=8.660282e-01
- [x] V5 order 0<=P_each<=P_atleastone<=T0 c-50:50@600 -- P_each=4.486204e-01 P_one=4.492995e-01 T0=4.492997e-01
- [x] V3 htab-vs-RS T0 a-hist@113 -- htab=0.01484337922 rs=0.01484337922 (1.5s)
- [x] V3 htab-vs-RS T0 c-hist@113 -- htab=3.582909786e-07 rs=3.582909786e-07 (1.5s)

## assumptions / limitations

- 2-bucket scenarios only (a-hist, a-50:50, c-hist, c-50:50); the
  3-bucket scenarios (b-hist, b-thirds) are outside A1's joint scope
  and are not computed here.
- Fixed N_b unique valid bodies; 25% holdout with exact fixed split
  sizes; A1's C|k composition model; no validity/dedup modeling.
- 'Eligible' test/training bodies = bodies in the included buckets.
- CVD literal reading: at least one included bucket has >=2 distinct
  C values among its training bodies (P_atleastone). Stricter reading:
  every included bucket does (P_each). Both reported; the choice is
  an owner decision.
- Matrix conditioning is excluded; results must not be presented as
  complete-rule feasibility.
