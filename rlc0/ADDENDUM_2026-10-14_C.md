# ADDENDUM - RLC-0 ARCHIVAL INTEGRITY NOTE (2026-10-14 C)

Provenance: prepared 2026-10-14 after GPT's follow-up audit of the published repository at commit
e036b88 found that the sidecar record `evidence/C2/MANIFEST_recomputed.sha256` (added by
ADDENDUM_2026-10-14_B) matched only 60 of 78 entries of the published ZIP snapshot at filename
level, with 18 mismatches, one of which (V1_STATUS.txt) GPT reported as not explained by a plain
LF/CRLF difference. CLAUDE reviewed the finding and ordered a narrow, read-only, per-file byte
reconciliation before anything is recorded. This note records that reconciliation. It does NOT
amend ADDENDUM_2026-10-14_B (or any earlier note), does NOT modify any frozen file, and does NOT
modify the committed manifest or the sidecar. No seed was compiled, executed, or submitted to
CBMC. No CBMC run, experiment, flag, budget, or protocol change occurred. The scientific
disposition of RLC-0 is unchanged.

## 1. Finding under review

GPT audited commit e036b88 (master of foued2/failure-concentration-study) and reported:

- Repository structure correct; the sidecar is structurally correct (78 named entries,
  `<sha256>  raw/<name>`, sorted).
- Comparing each sidecar hash against the corresponding entry of the published ZIP artifact
  `failure-concentration-study-worktree-94fd572.zip`: 60 of 78 match, 18 mismatch.
- Named mismatches included build_all.cmd, probe_q.cpp, run_bounded.ps1, and V1_STATUS.txt; the
  V1_STATUS.txt mismatch was reported as not explained by a plain one-step LF/CRLF conversion.

## 2. Method (read-only, all tools run outside the repository)

Artifact under test: the published ZIP on branch transfer-artifacts,
failure-concentration-study-worktree-94fd572.zip, SHA-256
d7cc8fe2f556bab708d232f699e9c8ede071fecf2f10f6a94083abdb1bcdfe68, 237,765 bytes (transfer hash
independently verified by GPT and re-verified locally for this note). The ZIP's end-of-central-
directory record carries a 40-hexadecimal archive comment,
94fd572159bc9a1dde807e98261987cee139b652 — the commit id of the closure commit — which is the
`git archive` signature; the artifact is a git archive of commit 94fd572, produced on a Windows
host with core.autocrlf=true (local repo config; no .gitattributes file exists anywhere in the
repository).

For each of the 78 files in `rlc0/evidence/C2/raw/` (enumerated from the working tree):

1. SHA-256 of the raw working-tree bytes and of the raw ZIP entry bytes (byte-for-byte, no
   decoding).
2. EOL transforms computed byte-safely (Latin-1 roundtrip): normalize = CRLF to LF; expand =
   LF to CRLF. Test: expand(normalize(working tree)) compared to the ZIP entry.
3. Git object identity: blob object id at HEAD (`git ls-tree`), and SHA-256 of the bytes from
   `git cat-file blob` compared to normalize(working tree).
4. Line-ending classification and NUL-byte detection per file.

## 3. Result

- Byte-identical working tree vs ZIP: **59 of 78**.
- Different: **19 of 78**. For every one of the 19, SHA-256(expand(normalize(worktree))) equals
  the ZIP entry hash exactly; the length delta equals the number of bare-LF newlines (one CR byte
  added per newline). Working-tree EOL classes of the 19: 13 pure-LF, 6 mixed.
- Universal content identity: after CRLF-to-LF normalization, working tree, ZIP entry, and git
  blob have identical bytes for all 78 files. Concretely verified: SHA-256(normalize(worktree))
  equals SHA-256(cat-file blob bytes) for 78/78; for the 77 text files,
  SHA-256(expand(normalize(worktree))) equals the ZIP entry hash; for the one binary-classified
  file (below) all three representations are byte-identical verbatim.
- Working-tree EOL census: 46 CRLF text files, 13 LF text files, 6 mixed-EOL text files, 12
  three-byte stderr sidecars with no newline at all, 1 binary file.
- v1_fieldsens.txt (676 bytes) contains 337 NUL bytes. Git therefore treats it as binary: the
  commit-time clean filter did not rewrite it (blob = working-tree bytes verbatim) and
  `git archive` did not convert it (ZIP entry = blob bytes verbatim). It is byte-identical across
  all three stores and is not a text/EOL case at all. It is the single file for which the text
  EOL transform does not apply, as expected for binary content.
- Re-verified alongside: sidecar vs current working tree, per file, 78/78; the committed
  (nameless) manifest's hash multiset vs the sidecar's hash multiset, equal; FREEZE.md section 5,
  26/26.

V1_STATUS.txt specifically (GPT's unexplained file): the working tree copy has mixed line
endings — 70 bare-LF lines among CRLF lines. A one-step conversion fails (converting only pairs,
or only bare LFs, cannot reproduce the ZIP entry); the two-step normalize-then-expand bridges
exactly: SHA-256
0676b92dc8b92f280e36ddf4ddc25afa59f33c9b45b833aea0588ee03af8d86d (working tree) normalizes to
04a70277b37fe2cc9004f9d488ad820f84dc42e9ad97ac1b450853b1050b5f0b, expands to
0f7ad9c503a6a2ad10d8fef29248f47290ce757bc918b20c86cba1a0ffee216e, which is exactly the ZIP
entry hash. Fully explained as EOL provenance; content unchanged.

Per-file table for the 19 mismatches (working-tree length, ZIP length, byte delta, working-tree
EOL class, git blob object id at HEAD, SHA-256 of working-tree bytes, SHA-256 of ZIP entry bytes;
every row additionally has expand(normalize(worktree)) hash equal to the ZIP hash, and
normalize(worktree) hash equal to the blob-content hash):

```text
name               wt    zip  delta eol    blob_oid                               wt_sha256                                                             zip_sha256
build_all.cmd      1535  1569  34   lf     c82b627feff930b7f31c842a15e0d5d378b60cfc 83ac8ec7d39894401c855938bea4df90f55234db73b2e6b683111f010bf4063d d535d1cdb961ec7afa7e0f0e085de5b890132e5189c3d89fe3bfd328a4f08e05
debug1.cmd         909   928   19   lf     9b0c04b8ebdd325ded42d7eb8a7933121b3c4914 78e0f7d97f675ecf7bbb9c6cff250ae196f91347e3d337310d714a9d02e883ad 7d685b6dc707937c71e3d50c031b326761dbef1a73a241f7cc8773ad66eacd24
domain_run.cmd     532   541   9    lf     a7238496a90a31d172182271a4079123d81fdee2 88fcd26bbef7e907e247716d9633af319906a6ee08676f5d5b8d84838a0a8f86 5200b1c9a2c044269dc2dd411ff32efebfbd4c83d4d6bf77066d6151a973dde6
probe_c.c          368   379   11   lf     9754a0611c3b89d69afa7dc98d0e00fcbfdd5d6a bde7e0f3deaeae738b27cdf86d50b48dd5db7e212a193dc598c01657a4ac8fe8 8b893ce9941076451d05ff82273d5beadfc62262717ed920449d17cefdec2573
probe_domain.cpp   1254  1279  25   lf     4add0e6be4272aa756c467a571bea23fa21468b7 efefac4318895fa33031ed333895d257c0f1145353e1bbd23209a10a28bc45fa e5fe207882c57f024b889108754b14eed5d6ad4f9fa504ed1fa508c610836a56
probe_q.cpp        686   701   15   lf     162e09081c4398d57074b58cc55c7052e0ef6b88 48210774937861468b670f06eec16eed3a5bb0ba9d4853dad5e2a5463e2fadc5 5a2c089f110da3457e9fed7d3394b28c8baf16002800ac7422fe8b2f6a568cb7
probe_run.cmd      1082  1107  25   lf     9281f1a5d04d5fbd92b1bdff973ed662698e3dd4 7670367215add5bbfc854b2036fd52d40cce9b10a85c12a8ecf66373199b2bc0 e45aa7c40fe7ec12a0061a836b093d386e6e3338324d3dfbaff6e75fe7e21b9a
probe_split.cpp    915   936   21   lf     42950727cacced3dcae41f47b9a840b88f87069c 08a5bb098fb66987d091f689b1efe8e2228cec7e566355400a1dfbe1e18a2217 bd94d78203e24d5dafa4ceb08f6c2ed899c049129ca8874b614741a95e6d4c9c
probe_v1.cpp       406   418   12   lf     cd84fe5b5b695d6218ec114d09101d03629c3b6d 372f0dd11a6c7ad2e7d6f2eb5ee24a3ba7aaf6d33547bcc702c42954743af5ed fff1a2fcb80b87db6a6e97c98d7a878784d5c082c9a6de4ef391b9ed2e5338a7
probe2_run.cmd     615   630   15   lf     9dfaff2265196e8be91aa0699ee341e79f5a1ea4 a13fab439f7b07898eaca1bb608ca6c7b5a6b180c0c91ec5937cf3948a6e68d5 4f52a9a749cf46292f289e10d9dd78044ef76ddd4c84576453ccb85fad185776
probe3_run.cmd     421   430   9    mixed  3e505878796dae289a163511765fc4e6c5b0ecd0 b9bd2d437823eb60de86ddb48d43e3deb0df7d70f9d54bf60c73513e1679b4a8 fb25105c34845e53f8a7955c288092e361006ad0ae0b740068b81f60592ec811
qa.c               253   261   8    mixed  9b8f5f9128da60ad0fe81712256662ea44931348 07cb14ae0ea79c59e1b6f0f088e6b4721bb9985d6081aecf776428b2b76525d7 8ed62888e23e16b5c95b5996157c5947f4fae5799f5dddc9c7d4e30eda7feba0
qb.c               252   260   8    mixed  3b6eda0eaab1102b0b49cfbfd5f080bb5c014db2 9cabf019727e24de1ff2d7b00b9da4ade074fc42d97cb7331b51964a2f74900c 299793dc5422e18d9cd2c65ee7e3c8f1e507c793b48ed5b210978b1e073eaaab
qc.c               253   261   8    mixed  52891bdcefc7202b11046ed82028b97e1119a229 a25c0010e611438732212bfb235317432b9093d18db44ae112dc88739f642619 4bc91269cfa8bf45e27a556ad50efe1b27a26d4d10d9361f2c1608c9a788d8d0
qd.cpp             279   287   8    mixed  4cc101cedea2c70a90206f20e8f5dd3a08d2ab54 e2053294f1666a6c08df01bf199bf312d61bdca641e8536921be73b7b4283512 5223ad5d632b6f391e7e3101337aaaefc9adbb7729320620df0515defecd010a
run_bounded.ps1    6835  6999  164  lf     ea4e1dc5e811434c010c6b676f81295c1b2bd5e0 f36d7327cd2df1f9dad6cd701f8dcd81b7969ac522de46842fdea87cf7cc7dee a41fb5f1fa72f48cffe258dcad4a710a0c55c9de0eecfc1a4b85053757eab940
selftest_alloc.ps1 173   179   6    lf     f8e9c0601f67e6a019c935be1d14d8092a9f08fc 34818d3afb998c885947e50f987eb4b4baaa5dfc34a56372773df02c161f7e15 ebd6289055098def8fa360c4c9a9e793a74b62d18e1b2f260e70fec908970e0f
V1_STATUS.txt      3753  3823  70   mixed  10c7a048e7a49142d7e31bef5c5d05a06ef5a4b9 0676b92dc8b92f280e36ddf4ddc25afa59f33c9b45b833aea0588ee03af8d86d 0f7ad9c503a6a2ad10d8fef29248f47290ce757bc918b20c86cba1a0ffee216e
verify_all.cmd     1302  1329  27   lf     e62ee9bcbcd59f8b62a298ded814b5e652c090cc 17f0f738fdd9063129d8f723c2e8644f0e8dbeb729c1d85f361e41bc87bc2df9 7416eb3f1039eae2b520ef84302b2cc843edf84f83a6908dccd9346fe55dad71
```

## 4. Count discrepancy against GPT's audit

The independent reconciliation obtained 59 matches and 19 mismatches; GPT reported 60 and 18.
The same published ZIP (transfer hash re-verified) and the same sidecar values were used, so the
one-file difference is a counting difference whose direction cannot be resolved from the retained
records (GPT's per-file list was not preserved in the transcript). It does not affect the
substantive conclusion: each of the 19 mismatches obtained here is proven, by exact SHA-256
equality of the stated transform, to differ from the ZIP entry only by line-ending expansion; no
content difference exists in any of the 78 files under either count.

## 5. Clarification of the 78/78 statement in ADDENDUM B

ADDENDUM_2026-10-14_B section 2 stated that recomputation "reproduces 78/78, 0 mismatches". The
basis of that statement is now explicit and was re-verified today: the committed nameless
manifest's hash multiset equals the multiset of current working-tree hashes (78/78), and the
sidecar equals the current working-tree hashes per file (78/78). The statement recorded
working-tree-byte identity only. Any reading of "78/78" as a claim of filename-level byte
identity between the sidecar and the published ZIP is withdrawn: that comparison is 59/78
byte-identical and 19/78 line-ending-expanded (sections 3-4). The working-tree-byte claim is
confirmed. This clarification is recorded here; ADDENDUM B itself is not edited.

## 6. Byte-provenance model (what each published representation contains)

Three byte conventions coexist for the same logical content of evidence/C2/raw, all now
verified for all 78 files:

- Git blob bytes (and therefore raw.githubusercontent.com downloads): CRLF-to-LF normalized at
  commit time (core.autocrlf=true), except the binary-classified file, which is stored verbatim.
- Published ZIP (git archive of 94fd572, produced with autocrlf=true): text entries are the LF
  blob bytes expanded to CRLF; the binary-classified file is stored verbatim.
- Working tree, FREEZE.md section 5, and the sidecar: working-tree bytes as authored — a mix of
  CRLF (tool-produced outputs), LF (authored scripts), mixed (V1_STATUS.txt and five probe
  sources), no-newline (three-byte stderr sidecars), and binary (v1_fieldsens.txt). This is the
  documented working-tree-byte convention of FREEZE.md sections 5 and 7.

Verified equations, per file, all 78: SHA-256(worktree) equals the sidecar value;
SHA-256(normalize(worktree)) equals SHA-256(blob bytes); for text files,
SHA-256(expand(normalize(worktree))) equals SHA-256(ZIP entry); for the binary file all three
are byte-identical. Any future cross-representation comparison must apply this normalization
model; a raw hash comparison across representations is expected to differ exactly where this
note's table says it differs.

## 7. Gate status update

- C3 (independent verification): still PARTIALLY SATISFIED, with one component upgraded. The
  ZIP-versus-sidecar discrepancy raised by GPT's follow-up audit is now reconciled with
  per-file, hash-level proof (sections 3-4), and content integrity of all 78 C2 raw evidence
  files is established across all three published representations. What remains unsatisfied is
  unchanged from ADDENDUM B: the committed manifest is defective as a name-to-hash record, and
  full-history cloning via the bundle was not exercised in GPT's environment.
- C2 remains NOT SATISFIED for its original purpose (canary FAIL never observed); unchanged.
- Scientific disposition unchanged: full-domain certification was not demonstrated; no seed
  verdicts exist; the seed-3 witness defect remains recorded and uncorrected.

## 8. Security note

As recorded in ADDENDUM_2026-10-14_B section 7: a GitHub OAuth credential for the repository
owner's account passed through a terminal transcript during the authorized publication; the
owner was advised to rotate the token. As of the writing of this note, rotation had not been
confirmed to this session. Rotation is the owner's action outside this record. No credential is
stored in this repository.

## 9. Authorization status (unchanged)

- No frozen file was edited by this note; FREEZE.md section 5 hashes were re-verified 26/26
  after this note was written and before it was committed.
- `rlc0-freeze` tag: never created; will not be created.
- Phase C (six-seed execution): never performed; prohibited and moot.
- No CBMC run, experiment, solver/flag/budget change, or successor project is authorized by this
  note. This is an archival integrity record appended to a closed study.

RLC-0 is complete. No follow-up is authorized.
