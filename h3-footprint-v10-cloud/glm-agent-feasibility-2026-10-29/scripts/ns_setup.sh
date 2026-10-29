#!/bin/sh
# ns_setup.sh — runs INSIDE `unshare -r -m -n` (private user+mount+network ns).
# Purpose: H3 candidate execution boundary (GLM-agent exploratory pilot, 2026-10-29).
#
# Usage: unshare -r -m -n /bin/sh ns_setup.sh <scratch_id> <cmd...>
#   cmd paths are CHROOT-RELATIVE (view root), e.g.
#   /usr/bin/python3 -I -B /trusted/candidate_child.py --probe-timeout 5.0
#
# Architecture:
#   1. bind host staging /var/tmp/h3trusted -> /mnt while /var/tmp is host view
#   2. fresh size-capped tmpfs over /home/z /root /var/tmp /tmp /dev/shm /run
#      (hides repository, .env credentials, and all host user data)
#   3. build a minimal view root at /var/tmp/view with READ-ONLY binds:
#      /usr, /lib, /lib64, /dev/null; trusted harness at /trusted;
#      candidate body at /candidate (matches the v10 container layout)
#   4. chroot into the view (no /proc, no host paths reachable)
#   5. env -i, per-probe scratch under /var/tmp/scratch/<id> (tmpfs, discarded)
#
# Network: the -n namespace has no external interface beyond a down loopback.
set -u
SCRATCH_ID="$1"; shift

# 1) hold staging while /var/tmp is still the host view
mount --bind /var/tmp/h3trusted /mnt 2>/dev/null || exit 88

# 2) cover host data and writable areas with fresh, size-capped tmpfs
mount -t tmpfs -o size=8m,mode=0711,nosuid,noexec  none /home/z  2>/dev/null; R_HOME=$?
[ -d /root ] && mount -t tmpfs -o size=1m,mode=0711,nosuid,noexec none /root 2>/dev/null; R_ROOT=$?
mount -t tmpfs -o size=32m,mode=0711,nosuid        none /var/tmp 2>/dev/null || exit 90
mount -t tmpfs -o size=16m,mode=0711,nosuid,noexec none /tmp     2>/dev/null; R_TMP=$?
mount -t tmpfs -o size=4m,mode=0555,nosuid,noexec  none /dev/shm 2>/dev/null; R_SHM=$?
mount -t tmpfs -o size=4m,mode=0755,nosuid,noexec  none /run     2>/dev/null; R_RUN=$?

# 3) minimal view root (dash has no brace expansion - explicit mkdir)
V=/var/tmp/view
mkdir -p "$V/usr" "$V/lib" "$V/lib64" "$V/bin" "$V/dev" "$V/tmp" \
         "$V/var/tmp/scratch" "$V/candidate" "$V/trusted" || exit 91
mount --bind /mnt/candidate "$V/candidate" || exit 92
mount -o remount,ro,bind "$V/candidate" 2>/dev/null || true
mount --bind /mnt/trusted  "$V/trusted" || exit 93
mount -o remount,ro,bind "$V/trusted" 2>/dev/null || true
umount /mnt 2>/dev/null || true
mount --bind /usr    "$V/usr"    || exit 94
mount -o remount,ro,bind "$V/usr" 2>/dev/null || true
mount --bind /lib64  "$V/lib64"  2>/dev/null || true
mount -o remount,ro,bind "$V/lib64" 2>/dev/null || true
mount --bind /lib    "$V/lib"    2>/dev/null || true
mount -o remount,ro,bind "$V/lib" 2>/dev/null || true
: > "$V/dev/null" 2>/dev/null
mount --bind /dev/null "$V/dev/null" 2>/dev/null || true

# 4) chroot into the view; env wiped; scratch as HOME/TMPDIR
export SCRATCH_DIR=/var/tmp/scratch/"$SCRATCH_ID"
mkdir -p "$V$SCRATCH_DIR" || exit 95
exec chroot "$V" /usr/bin/env -i \
    PATH=/usr/bin:/bin \
    HOME="$SCRATCH_DIR" TMPDIR="$SCRATCH_DIR" \
    PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 \
    NS_MOUNT_FACTS="home:$R_HOME root:$R_ROOT tmp:$R_TMP shm:$R_SHM run:$R_RUN proc:absent" \
    SCRATCH_ID="$SCRATCH_ID" \
    "$@"
