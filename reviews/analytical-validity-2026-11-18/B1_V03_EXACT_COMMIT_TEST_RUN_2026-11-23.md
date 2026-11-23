# B1 v0.3 exact-commit test execution record — 2026-11-23

## Result

**All 59 tests passed.** The repaired successor commit compiles, the complete committed unittest suite ran to completion, and the process exited with code 0. This is a test-execution result, not Claude's code-review verdict and not authorization to merge or execute the research census.

## Source and commit identity

- Repository: `foued2/failure-concentration-study`
- Successor branch: `gpt/b1-v06-intake-syntax-repair-2026-11-23`
- Tested commit: `258c68df4a2ede77c0acd2e9ab0382080ae305b6`
- Parent: `a48cc9dfdc5af87661762f6be9b98e11030ce9b8`
- Starting test-file blob: `fdce4a663516b122e0ffa5803554242457445360`
- Successor test-file blob: `606078403788dd0e3e1444dda26060dc5904c518`
- Tested manifest-schema blob: `0f2865e606fa61400184c09abd01601497637a6b` (24,279 bytes)
- Tested validator blob: `cbffe0df924eba17de01e7342694da6455ee5b85`
- Tested sidecar-schema blob: `72fc746c3d6129534aeb2fdbcd866842865f98c7`

The commit's GitHub diff was inspected before committing. It has exactly one changed file, `census-intake/tests/test_b1_census_intake.py`, with six additions and six deletions at lines 176, 274, 347, 416, 499, and 591. No other file changed. The parent is exactly `a48cc9d`. PR #10 and its original branch were not changed.

The new test-file blob and manifest-schema blob were then read from a fresh detached checkout of the tested commit. The manifest schema Git blob SHA matches the frozen pin embedded in the validator and asserted by the test suite.

## Execution environment and commands

Execution used a fresh clone in an isolated remote command sandbox, checked out detached at the exact tested commit. The Git worktree was clean before execution and remained clean after the suite.

- Python: `3.13.18`
- `jsonschema`: `4.26.0`, installed from the committed `census-intake/requirements.txt`
- Compile command, from repository root:
  `python -m py_compile census-intake/validate_records.py census-intake/tests/test_b1_census_intake.py`
- Test command, from `census-intake/`:
  `python -m unittest discover -s tests -v`

Compilation succeeded. The complete suite was run twice against the same unchanged commit. The recorded second run produced no stderr output and reported:

```
Ran 59 tests in 4.495s

OK
UNITTEST_EXIT=0
```

The initial combined checkout/compile/test invocation also completed with all 59 tests passing. It emitted one non-fatal Git attributes warning during checkout; the repeat test run after checkout produced no warning or stderr output. No source file was modified between runs.

## Individual test outcomes

All 59 outcomes were `OK`:

- `test_aggregate_fields_are_not_manifest_properties`
- `test_bad_digest_format_rejected`
- `test_cd_formula_uses_failure_vector_only_and_is_cited`
- `test_cli_manifest_only_exit_code_and_report`
- `test_cli_rejected_sidecar_does_not_change_manifest_decision`
- `test_cli_rejects_root_outcome_field_with_exit_code_2`
- `test_complete_17_field_manifest_passes_schema_and_local_checks`
- `test_datetime_format_enforced`
- `test_different_valid_id_sets_rejected`
- `test_duplicate_record_id_within_variant_rejected`
- `test_duplicate_variant_id_rejected`
- `test_empty_manifest_rejected`
- `test_evaluation_row_count_must_be_78`
- `test_excluded_variant_emits_no_zero_counts_or_cell`
- `test_expected_not_run_decision_cannot_follow_snapshot`
- `test_expected_not_run_emits_no_zero_counts_or_cell`
- `test_external_checks_are_explicitly_not_performed`
- `test_fixed_exposure_facts_and_independence_prohibition_enforced`
- `test_future_generation_selection_requires_protocol_ref`
- `test_identical_artifact_digests_flagged_for_adjudication`
- `test_incomplete_has_provisional_vectors_but_no_cell_or_c_d`
- `test_incomplete_with_zero_received_records_has_no_vectors_or_cell`
- `test_invalid_result_count_and_stratum_count_rejected`
- `test_invalid_terminal_status_rejected`
- `test_invalid_variant_emits_no_zero_counts_or_cell`
- `test_malformed_diagnostic_evidence_ref_rejected`
- `test_malformed_status_decision_refs_rejected`
- `test_non_string_measurement_basis_rejected`
- `test_null_diagnostic_evidence_ref_rejected`
- `test_null_runnable_digest_rejected`
- `test_null_semantic_source_digest_rejected`
- `test_outcome_exclusion_assertion_true_rejected`
- `test_packaged_manifest_schema_exact_source_identity`
- `test_parent_family_mapping_mismatch_rejected`
- `test_parent_roster_duplicate_rejected`
- `test_pre_diagnostic_status_must_precede_campaign_start`
- `test_same_id_set_reuse_across_valid_variants_is_allowed`
- `test_sidecar_aggregate_mismatch_reason`
- `test_sidecar_boolean_aggregate_entry_is_malformed`
- `test_sidecar_duplicate_variant_assertion_rejected`
- `test_sidecar_for_rejected_manifest_is_rejected_and_cannot_override_it`
- `test_sidecar_malformed_aggregate_reason`
- `test_sidecar_manifest_sha_mismatch_rejected`
- `test_sidecar_matching_vectors_are_consistency_only_and_do_not_change_manifest`
- `test_sidecar_schema_blob_is_pinned_in_validator`
- `test_sidecar_schema_blob_sha_mismatch_rejected`
- `test_sidecar_unknown_field_rejected`
- `test_sidecar_unknown_variant_rejected`
- `test_status_decision_derived_counts_consulted_true_rejected`
- `test_status_decision_missing_required_field_rejected`
- `test_status_decision_terminal_values_consulted_true_rejected`
- `test_status_decision_unknown_nested_field_rejected`
- `test_unknown_diagnostic_result_outcome_field_rejected`
- `test_unknown_nested_artifact_reference_field_rejected`
- `test_unknown_root_correctness_outcomes_rejected`
- `test_unknown_variant_outcome_field_rejected`
- `test_unresolved_does_not_change_cd_when_failure_vector_is_fixed`
- `test_unsupported_measurement_basis_rejected`
- `test_valid_zero_failure_uses_label_not_numeric_cd`

## Scope and disposition

The suite used its committed local test fixtures only. No real manifest, bank, solver, diagnostic execution, outcome data, census, or predictive analysis was used.

The six-line repair was limited to the approved syntax corrections. No validator logic, schema, requirements, test assertions, or other file changed in the repair commit.

**Test execution: PASS (59/59). Claude's review verdict: NOT PASS remains operative pending Claude's independent review of this successor commit and the complete test evidence.** No merge is authorized by this result. Gate 1 remains BLOCKED / NOT ASSESSABLE; the scientific proposition remains UNPROVEN; the census-authorization question remains unanswered.
