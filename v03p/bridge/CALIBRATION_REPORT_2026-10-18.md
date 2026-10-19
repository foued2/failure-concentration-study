# Calibration report - bridge gamma* (scenarios (a)/(c))

**Date:** 2026-10-18.  **Status:** executed under the owner
bridge authorization (Foued, 2026-10-18) and the GPT/
calibration work order (2026-10-18), after the battery stage
closed (standing record `BATTERY_REPORT_2026-10-18.md`,
commit `4618f31`).

**Every number in this file is PROVISIONAL /
NOT A COMPLETE-RULE ESTIMATE.**  Scenario (b) is out of scope
(bridge NOT DEFINED there).  `I_k` is the bucket-local
support proxy under Rev F 5A as drafted; P(pass) = 0 for the
complete rule is unchanged (draft A2.3).  NC1 is closed;
NC2, Phase 1, solver generation, hidden-outcome collection,
spending, and master merge remain unauthorized.

## Frozen settings

- `GH_NODES_CAL`: 256
- `GH_NODES_PREV`: 128
- `GH_TOL_CAL`: 1e-12
- `CAL_SEED`: 20261019
- `MC_DRAWS_CAL`: 2000000
- `BISECT_GAMMA_TOL`: 1e-09
- `BRACKET_START`: 8.0
- `BRACKET_STEP`: 4.0
- `BRACKET_HI_CAP`: 64.0
- `PEAK_COARSE`: 0.5
- `PEAK_HI0`: 32.0
- `PEAK_EXT_CAP`: 64.0
- `GOLDEN_TOL`: 1e-06
- `TAU`: 1.4142135623730951
- `SREF`: 0.12703
- `dstar`: 0.020273255405408218
- `2dstar`: 0.040546510810816436
- `ridge`: 0.0

Objective: `f(gamma) = L_baseline_unpen - L_extended_unpen`,
both families refitted at their unpenalized population
optima against per-cell targets `pbar(k,c;gamma)` (GH-256 at
tau = sqrt(2)); IRLS mirror of `study/models.py` (tol 1e-13,
<= 50 iterations, ridge 0.0); the same support-conditioned
weights for both families (battery production weightsets).

Integrity (verified at run time inside the frozen execution):
- `battery`: committed == working = `cfec42ad6866a10bf8930badc0e7b928b477efea`
- `calibrate`: committed == working = `2764c41e11dac4e3c7779acd78fa170710727c50`
(battery.py frozen machinery, module imported read-only;)

## Row weightsets (support-conditioned, both families)

### a-hist
- `w5`: 0.19044540162718873
- `w10`: 0.8095545983728113
- `var5`: 0.02393710636581739
- `var10`: 0.005682367235387023
- `pi5`: [0.014092524401232445, 0.4830564668442984, 0.3622923499959422, 0.12557139509859147, 0.014987263659918544]
- `pi10`: [3.943620969830307e-05, 0.24499131235637975, 0.42460681728772653, 0.330362434146195]
- `levels5`: [0.2, 0.4, 0.6, 0.8, 1.0]
- `levels10`: [0.2, 0.3, 0.4, 0.5]
### a-50:50
- `w5`: 0.1400203305151545
- `w10`: 0.8599796694848454
- `var5`: 0.02238568705966753
- `var10`: 0.005605967719073061
- `pi5`: [0.006181615218900605, 0.4848683864753781, 0.3636511897130241, 0.13755956506233324, 0.007739243530336278]
- `pi10`: [0.00012976446433283497, 0.23671653567435294, 0.4306710050771318, 0.33248269478418363]
- `levels5`: [0.2, 0.4, 0.6, 0.8, 1.0]
- `levels10`: [0.2, 0.3, 0.4, 0.5]
### c-hist
- `w5`: 0.43845907631444453
- `w10`: 0.5615409236855554
- `var5`: 0.02151680922044847
- `var10`: 0.00638194682652309
- `pi5`: [0.00035021191672835264, 0.47954275973375016, 0.36315822058383024, 0.15570144344868203, 0.0012473643169964397]
- `pi10`: [5.15451045894337e-06, 0.28671651959054933, 0.35698068262646365, 0.35629764327252744]
- `levels5`: [0.2, 0.4, 0.6, 0.8, 1.0]
- `levels10`: [0.2, 0.3, 0.4, 0.5]
### c-50:50
- `w5`: 0.23614074775369373
- `w10`: 0.7638592522463062
- `var5`: 0.019819704348678895
- `var10`: 0.0062188354374110594
- `pi5`: [0.00020761257908313602, 0.4898413221233253, 0.37901961851243765, 0.1301234734621955, 0.0008079733229473486]
- `pi10`: [7.824009468537997e-06, 0.28316294430790384, 0.37466003713718726, 0.3421691945454409]
- `levels5`: [0.2, 0.4, 0.6, 0.8, 1.0]
- `levels10`: [0.2, 0.3, 0.4, 0.5]

## Per-variant results

### a-hist

- f(battery gamma grid): [(0.0, 5.551115123125783e-17), (0.25, 2.6364103808851347e-05), (0.5, 0.00011001184745862425), (1.0, 0.0004740259464121044), (1.5, 0.0011332181451357837), (2.0, 0.0021113849962965947), (3.0, 0.005014869189864046), (4.0, 0.008964823057688864), (6.0, 0.01814282803425904), (8.0, 0.025967871069018877)]
- broken down:
  - f(0.0) = 5.5511151231e-17
  - f(0.25) = 2.6364103809e-05
  - f(0.5) = 1.1001184746e-04
  - f(1.0) = 4.7402594641e-04
  - f(1.5) = 1.1332181451e-03
  - f(2.0) = 2.1113849963e-03
  - f(3.0) = 5.0148691899e-03
  - f(4.0) = 8.9648230577e-03
  - f(6.0) = 1.8142828034e-02
  - f(8.0) = 2.5967871069e-02
- delta* = 0.020273255405408218 solution:
  - gamma* = 6.483283771e+00  |f - d*| = 1.788e-12  (iters 33)
  - achieved |f - d*| against Rev F 1e-4 tolerance:
    1.788e-12 (within tolerance: True)
  - GH node agreement at gamma* (256 vs 128): 1.110e-16
  - baseline fit: beta [1.0853955370860475, 0.17786295295169466] iters 6 grad 3.123e-17
  - extended fit: beta [-1.3282404024599088, -1.7833684316005798, 4.8136005966161735] iters 6 grad 8.446e-17
  - MC cross-check (seed 20261019, 2000000 draws): f_MC = 2.0276663482e-02,
    SE = 2.934e-05, |f_MC - f_GH| = 3.408e-06 (<= 5*SE: True)
  - beta_pop (A2.3, truth-marginalized pbar): 1.214285522e-01
    - stratum k=5: cbar 5.288608814e-01 pbar_k 7.475136800e-01
      den_k 2.825072154e-01 beta_k 0.09612701208523014
    - stratum k=10: cbar 4.085292249e-01 pbar_k 5.443488842e-01
      den_k 2.850774368e-01 beta_k 0.14650197689302533
  - beta_pop fit-sensitivity (on qhat_ext): 1.214285522e-01
  - labeled average-derivative approximation: 1.876781560e-01
  - c*_prov = (1.25/beta_pop)^2 = 1.059688917e+02 -> no NC1 row (grid mismatch)
  - NC1-grid comparison: >39.0625; <156.25; <625.0
  - anchor: beta_min = 0.10 (c*_ref = 156.25);
    ratio c*_prov / c*_ref = 6.782009e-01
  - context: oracle Delta at gamma* (KL, delta_of) =
    2.0291678841e-02 (not a gate; decomposition context)
- 2d* = 0.040546510810816436 finding: NOT ATTAINABLE (evidence-based)
  - actual peak: f(gamma=1.097820312e+01) = 3.0671039338e-02
  - margin 2d* - peak = 9.8754714729e-03 (positive: the observed maximum on the frozen bracket lies below the target)
  - MC corroboration at the argmax: f_MC = 3.0660884439e-02 SE = 3.423e-05 gap = 1.015e-05
  - GH node agreement at the argmax: 2.220e-16
- actual peak of the sigma=1 objective on the scan:
  gamma_peak = 1.097820312e+01, f_peak = 3.0671039338e-02 (golden iters 31)

### a-50:50

- f(battery gamma grid): [(0.0, 0.0), (0.25, 2.2335480278301567e-05), (0.5, 9.317097304367694e-05), (1.0, 0.00040162677535721114), (1.5, 0.0009619448930626717), (2.0, 0.0017982701454749561), (3.0, 0.004317139500148226), (4.0, 0.00783350290156537), (6.0, 0.01642083569004915), (8.0, 0.024277711539714253)]
- broken down:
  - f(0.0) = 0.0000000000e+00
  - f(0.25) = 2.2335480278e-05
  - f(0.5) = 9.3170973044e-05
  - f(1.0) = 4.0162677536e-04
  - f(1.5) = 9.6194489306e-04
  - f(2.0) = 1.7982701455e-03
  - f(3.0) = 4.3171395001e-03
  - f(4.0) = 7.8335029016e-03
  - f(6.0) = 1.6420835690e-02
  - f(8.0) = 2.4277711540e-02
- delta* = 0.020273255405408218 solution:
  - gamma* = 6.911072448e+00  |f - d*| = 1.380e-12  (iters 33)
  - achieved |f - d*| against Rev F 1e-4 tolerance:
    1.380e-12 (within tolerance: True)
  - GH node agreement at gamma* (256 vs 128): 1.110e-16
  - baseline fit: beta [1.246647702523302, 0.30595642967237546] iters 6 grad 2.776e-17
  - extended fit: beta [-1.322260438519851, -1.783193231415908, 5.126522817965634] iters 6 grad 2.927e-17
  - MC cross-check (seed 20261019, 2000000 draws): f_MC = 2.0276889778e-02,
    SE = 3.141e-05, |f_MC - f_GH| = 3.634e-06 (<= 5*SE: True)
  - beta_pop (A2.3, truth-marginalized pbar): 1.303651355e-01
    - stratum k=5: cbar 5.311612870e-01 pbar_k 7.767190230e-01
      den_k 1.942445894e-01 beta_k 0.09391162879051616
    - stratum k=10: cbar 4.095506630e-01 pbar_k 5.758979659e-01
      den_k 2.987625660e-01 beta_k 0.15406588396346335
  - beta_pop fit-sensitivity (on qhat_ext): 1.303651355e-01
  - labeled average-derivative approximation: 1.979090877e-01
  - c*_prov = (1.25/beta_pop)^2 = 9.193843472e+01 -> no NC1 row (grid mismatch)
  - NC1-grid comparison: >39.0625; <156.25; <625.0
  - anchor: beta_min = 0.10 (c*_ref = 156.25);
    ratio c*_prov / c*_ref = 5.884060e-01
  - context: oracle Delta at gamma* (KL, delta_of) =
    2.0292066757e-02 (not a gate; decomposition context)
- 2d* = 0.040546510810816436 finding: NOT ATTAINABLE (evidence-based)
  - actual peak: f(gamma=1.120020232e+01) = 2.9659466467e-02
  - margin 2d* - peak = 1.0887044344e-02 (positive: the observed maximum on the frozen bracket lies below the target)
  - MC corroboration at the argmax: f_MC = 2.9649965141e-02 SE = 3.522e-05 gap = 9.501e-06
  - GH node agreement at the argmax: 1.110e-16
- actual peak of the sigma=1 objective on the scan:
  gamma_peak = 1.120020232e+01, f_peak = 2.9659466467e-02 (golden iters 31)

### c-hist

- f(battery gamma grid): [(0.0, 0.0), (0.25, 3.946254502962265e-05), (0.5, 0.00016467758789256992), (1.0, 0.0007088460922874962), (1.5, 0.001690359315123069), (2.0, 0.0031368520200413252), (3.0, 0.00735366678168814), (4.0, 0.012868662010382503), (6.0, 0.02421219272790176), (8.0, 0.03113557852850235)]
- broken down:
  - f(0.0) = 0.0000000000e+00
  - f(0.25) = 3.9462545030e-05
  - f(0.5) = 1.6467758789e-04
  - f(1.0) = 7.0884609229e-04
  - f(1.5) = 1.6903593151e-03
  - f(2.0) = 3.1368520200e-03
  - f(3.0) = 7.3536667817e-03
  - f(4.0) = 1.2868662010e-02
  - f(6.0) = 2.4212192728e-02
  - f(8.0) = 3.1135578529e-02
- delta* = 0.020273255405408218 solution:
  - gamma* = 5.256996254e+00  |f - d*| = 5.109e-13  (iters 33)
  - achieved |f - d*| against Rev F 1e-4 tolerance:
    5.109e-13 (within tolerance: True)
  - GH node agreement at gamma* (256 vs 128): 1.110e-16
  - baseline fit: beta [0.6973621228366476, -0.18397308564245318] iters 5 grad 4.917e-17
  - extended fit: beta [-1.3339470965473732, -1.7769763024412317, 3.9027363683486125] iters 6 grad 4.494e-17
  - MC cross-check (seed 20261019, 2000000 draws): f_MC = 2.0277085038e-02,
    SE = 2.772e-05, |f_MC - f_GH| = 3.830e-06 (<= 5*SE: True)
  - beta_pop (A2.3, truth-marginalized pbar): 1.048519539e-01
    - stratum k=5: cbar 5.355905977e-01 pbar_k 6.676026616e-01
      den_k 5.846478240e-01 beta_k 0.09948993247996128
    - stratum k=10: cbar 4.069570815e-01 pbar_k 4.541360154e-01
      den_k 2.220864169e-01 beta_k 0.11896760396810134
  - beta_pop fit-sensitivity (on qhat_ext): 1.048519539e-01
  - labeled average-derivative approximation: 1.519359285e-01
  - c*_prov = (1.25/beta_pop)^2 = 1.421238522e+02 -> no NC1 row (grid mismatch)
  - NC1-grid comparison: >39.0625; <156.25; <625.0
  - anchor: beta_min = 0.10 (c*_ref = 156.25);
    ratio c*_prov / c*_ref = 9.095927e-01
  - context: oracle Delta at gamma* (KL, delta_of) =
    2.0279792333e-02 (not a gate; decomposition context)
- 2d* = 0.040546510810816436 finding: NOT ATTAINABLE (evidence-based)
  - actual peak: f(gamma=9.383552183e+00) = 3.2428669520e-02
  - margin 2d* - peak = 8.1178412910e-03 (positive: the observed maximum on the frozen bracket lies below the target)
  - MC corroboration at the argmax: f_MC = 3.2416418754e-02 SE = 3.285e-05 gap = 1.225e-05
  - GH node agreement at the argmax: 2.220e-16
- actual peak of the sigma=1 objective on the scan:
  gamma_peak = 9.383552183e+00, f_peak = 3.2428669520e-02 (golden iters 31)

### c-50:50

- f(battery gamma grid): [(0.0, -5.551115123125783e-17), (0.25, 2.7118441509488278e-05), (0.5, 0.00011310307533290986), (1.0, 0.00048716500439582866), (1.5, 0.0011652482551457455), (2.0, 0.0021741508002948162), (3.0, 0.005189710662713454), (4.0, 0.0093353104231374), (6.0, 0.01903856005148785), (8.0, 0.027124424723578233)]
- broken down:
  - f(0.0) = -5.5511151231e-17
  - f(0.25) = 2.7118441509e-05
  - f(0.5) = 1.1310307533e-04
  - f(1.0) = 4.8716500440e-04
  - f(1.5) = 1.1652482551e-03
  - f(2.0) = 2.1741508003e-03
  - f(3.0) = 5.1897106627e-03
  - f(4.0) = 9.3353104231e-03
  - f(6.0) = 1.9038560051e-02
  - f(8.0) = 2.7124424724e-02
- delta* = 0.020273255405408218 solution:
  - gamma* = 6.263394922e+00  |f - d*| = 2.018e-13  (iters 33)
  - achieved |f - d*| against Rev F 1e-4 tolerance:
    2.018e-13 (within tolerance: True)
  - GH node agreement at gamma* (256 vs 128): 2.220e-16
  - baseline fit: beta [1.0250645053524507, 0.1024389977696097] iters 5 grad 1.546e-17
  - extended fit: beta [-1.3291609533047888, -1.7810972024993834, 4.647821132120415] iters 6 grad 2.022e-17
  - MC cross-check (seed 20261019, 2000000 draws): f_MC = 2.0277009169e-02,
    SE = 3.022e-05, |f_MC - f_GH| = 3.754e-06 (<= 5*SE: True)
  - beta_pop (A2.3, truth-marginalized pbar): 1.213205071e-01
    - stratum k=5: cbar 5.282965746e-01 pbar_k 7.359579290e-01
      den_k 2.900384061e-01 beta_k 0.10015258953974931
    - stratum k=10: cbar 4.058990602e-01 pbar_k 5.255873777e-01
      den_k 2.943810242e-01 beta_k 0.14217616200512093
  - beta_pop fit-sensitivity (on qhat_ext): 1.213205071e-01
  - labeled average-derivative approximation: 1.809479552e-01
  - c*_prov = (1.25/beta_pop)^2 = 1.061577224e+02 -> no NC1 row (grid mismatch)
  - NC1-grid comparison: >39.0625; <156.25; <625.0
  - anchor: beta_min = 0.10 (c*_ref = 156.25);
    ratio c*_prov / c*_ref = 6.794094e-01
  - context: oracle Delta at gamma* (KL, delta_of) =
    2.0288602321e-02 (not a gate; decomposition context)
- 2d* = 0.040546510810816436 finding: NOT ATTAINABLE (evidence-based)
  - actual peak: f(gamma=1.072886741e+01) = 3.1400148490e-02
  - margin 2d* - peak = 9.1463623210e-03 (positive: the observed maximum on the frozen bracket lies below the target)
  - MC corroboration at the argmax: f_MC = 3.1389535431e-02 SE = 3.620e-05 gap = 1.061e-05
  - GH node agreement at the argmax: 1.110e-16
- actual peak of the sigma=1 objective on the scan:
  gamma_peak = 1.072886741e+01, f_peak = 3.1400148490e-02 (golden iters 31)

## Findings (PROVISIONAL, NOT A COMPLETE-RULE ESTIMATE)

- a-hist: gamma*(d*) = 6.4833; beta_pop = 0.1214 per s_ref unit-> c*_prov = 105.969 (no NC1 row (grid mismatch)); 2d* not attainable: actual peak 3.067104e-02 at gamma-peak 10.9782, margin 9.875e-03
- a-50:50: gamma*(d*) = 6.9111; beta_pop = 0.1304 per s_ref unit-> c*_prov = 91.9384 (no NC1 row (grid mismatch)); 2d* not attainable: actual peak 2.965947e-02 at gamma-peak 11.2002, margin 1.089e-02
- c-hist: gamma*(d*) = 5.2570; beta_pop = 0.1049 per s_ref unit-> c*_prov = 142.124 (no NC1 row (grid mismatch)); 2d* not attainable: actual peak 3.242867e-02 at gamma-peak 9.3836, margin 8.118e-03
- c-50:50: gamma*(d*) = 6.2634; beta_pop = 0.1213 per s_ref unit-> c*_prov = 106.158 (no NC1 row (grid mismatch)); 2d* not attainable: actual peak 3.140015e-02 at gamma-peak 10.7289, margin 9.146e-03

Elapsed seconds: 9.36
