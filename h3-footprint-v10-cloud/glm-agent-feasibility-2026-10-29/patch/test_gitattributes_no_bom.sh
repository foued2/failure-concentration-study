#!/bin/sh
# test_gitattributes_no_bom.sh — verifies the BOM fix after applying
# 0001_fix_gitattributes_BOM.patch to a checkout containing v03p/a1/.
# Usage: sh test_gitattributes_no_bom.sh [repo_root]
set -u
REPO="${1:-.}"
FILE="$REPO/v03p/a1/.gitattributes"
fail() { echo "FAIL: $1"; exit 1; }

[ -f "$FILE" ] || fail "$FILE not found"
head -c 3 "$FILE" | od -An -tx1 | grep -q "ef bb bf" && fail "UTF-8 BOM still present on line 1"
grep -qx '\* -text' "$FILE" || fail "load-bearing '* -text' line missing"

# git must parse the file without the "not a valid attribute name" warning
cd "$REPO" || fail "cannot cd to $REPO"
OUT=$(git check-attr text -- v03p/a1/RUN.txt 2>&1) || fail "git check-attr errored: $OUT"
echo "$OUT" | grep -q "text: unset" || fail "expected 'text: unset' (byte-exact pin broken): $OUT"
echo "$OUT" | grep -q "not a valid attribute name" && fail "git still emits attribute-name warning"

echo "PASS: no BOM, '* -text' intact, attribute pin effective, no parser warning"
exit 0
