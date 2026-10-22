# Bug-detection count verification

Date: 2026-10-22

Source run: `natural-feasibility-pilot/bug-detection-check-20261022T063926Z-40003da9/`

Committed result: `2c29f0c`

## Verified counts

- Faulty variants: **7**
- Caught by diagnostic: **5/7**
- Caught by evaluation: **6/7**
- Caught by either bank: **7/7**
- Missed by both: **0**
- Correct reference: **30/30 diagnostic**, **20/20 evaluation**

The committed `BUG_DETECTION_RESULT.json`, `BUG_DETECTION_REPORT.md`, and
`INTEGRITY.json` agree. The summary is:

| Check | Result |
| --- | --- |
| Diagnostic-only | `reject_self_loops` |
| Evaluation-only | `early_return_on_target_push`, `directed_as_undirected` |
| Both banks | `unreachable_wrong_sentinel`, `skip_zero_weight_edges`, `last_parallel_edge`, `bfs_unweighted` |
| Neither bank | none |

`INTEGRITY.json` reports `status: PASS`, `all_hashes_match: true`,
`reference_control: PASS`, 240 diagnostic rows, 160 evaluation rows, and 16
retained capture directories.

## Transcription check

No transcription error was found. The 7/7, 5/7, and 6/7 figures match the
committed raw records. The earlier table's numbers are correct.

The frozen original banks and all earlier studies were not modified.
