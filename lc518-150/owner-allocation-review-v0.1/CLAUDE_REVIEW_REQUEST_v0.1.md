# Independent Claude review request: LC518 new allocation v0.1

Please review the complete proposal in `NEW_ALLOCATION_DESIGN_v0.1.md`, the machine-readable JSON, and the 23-test script. Treat this as a new design, not a recovered annex. Do not review candidate solver source because none has been constructed.

Please return explicit PASS / NOT PASS for the proposal as a design candidate, with findings on:

1. Whether M01-M08 are eight sufficiently distinct and scientifically defensible mutation mechanisms for Coin Change II. Challenge overlaps, especially M03 vs M05 and M02 vs M08.
2. Whether each mechanism's stated trigger condition, intended D1-D8 reach and family adapters are correct. Check K4 binary-doubling semantics for M08.
3. Whether the 28+2 schedule covers all pairs exactly, whether the two repeated pairs are appropriate, and whether their reversed orientations are a defensible balance rule.
4. Whether each parent assignment and S-extra assignment is internally consistent with the frozen G01-G30 family roster and the no-duplicate-S-extra rule.
5. Whether the SAB merge precedence preserves the declared mutations and makes sense; identify pairs where interaction masks one mutation.
6. Whether the 16 raw `(mechanism,family)` candidate cells and 48 witness skeletons are arithmetically correct under the proposal's assumptions. Do not mistake them for Rev 11 admissible witnesses or C6 PASS.
7. Whether the synthetic tests are adequate and truthful about their scope. They test five formulation-level models, not every source-level parent tactic.
8. Any additional design defect that should block source construction.

No repository write, source generation, candidate execution, dynamic diagnostic or held-out run is requested by this review. Please keep the proposal unadopted until your independent verdict is returned.