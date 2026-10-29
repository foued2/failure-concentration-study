"""HOSTILE TEST BODY: bounded scratch fill (<= 90 x 1 MiB). n=5 fills TMPDIR; n=6 reports free MiB on /tmp
afterwards (probes the supervisor's between-probe cleanup)."""
import os


def solve(n, edges, s, t):
    if n == 5:
        d = os.environ.get("TMPDIR", "/tmp")
        written = 0
        try:
            for i in range(90):
                with open(os.path.join(d, "f%d" % i), "wb") as f:
                    f.write(b"Z" * (1024 * 1024))
                written += 1
        except OSError:
            pass
        return written
    if n == 6:
        st = os.statvfs("/tmp")
        return (st.f_bavail * st.f_frsize) // (1024 * 1024)
    return 0
