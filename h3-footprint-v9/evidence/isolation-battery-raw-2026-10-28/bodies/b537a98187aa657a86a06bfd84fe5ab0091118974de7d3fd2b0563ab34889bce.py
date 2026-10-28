"""Test outbound network access from inside the guest.

A loopback connect to a socket this process just opened is the positive control:
it proves the socket stack works. The external connect must then fail, and the
exact exception class and message are recorded. No payload is sent in either
direction.
"""

import json
import socket

MARKER = "V9PROBE"
EXTERNAL_HOST = "1.1.1.1"
EXTERNAL_PORT = 443


def _try_tcp(host, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        return True, None, ""
    except OSError as exc:
        detail = (exc.strerror or str(exc) or "")[:120]
        return False, type(exc).__name__, detail
    finally:
        sock.close()


def _loopback():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(3.0)
    try:
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]
        connected, error, detail = _try_tcp("127.0.0.1", port, 2.0)
        try:
            accepted, _ = server.accept()
            accepted.close()
        except OSError:
            pass
        return connected, error, detail, port
    finally:
        server.close()


def solve_job(payload):
    loopback_connected, loopback_error, loopback_detail, loopback_port = _loopback()
    external_connected, external_error, external_detail = _try_tcp(
        EXTERNAL_HOST, EXTERNAL_PORT, 3.0
    )
    report = {
        "probe": "network",
        "loopback_port": loopback_port,
        "loopback_connected": loopback_connected,
        "loopback_error": loopback_error,
        "loopback_detail": loopback_detail,
        "external_target": f"{EXTERNAL_HOST}:{EXTERNAL_PORT}",
        "external_connected": external_connected,
        "external_error": external_error,
        "external_detail": external_detail,
        "paths": dict(payload.get("paths") or {}),
    }
    print(MARKER + " " + json.dumps(report, sort_keys=True))
    return 1
