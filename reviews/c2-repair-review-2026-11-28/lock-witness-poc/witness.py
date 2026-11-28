"""Small local model of a durable, first-writer-wins lock witness."""
import hashlib
import json
import sqlite3
import time


class Conflict(Exception):
    pass


class Witness:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS claims(
            scope TEXT PRIMARY KEY, request_hash TEXT NOT NULL, sequence INTEGER NOT NULL UNIQUE);
          CREATE TABLE IF NOT EXISTS events(
            sequence INTEGER PRIMARY KEY, scope TEXT NOT NULL, kind TEXT NOT NULL,
            request_hash TEXT NOT NULL, payload TEXT NOT NULL, previous_hash TEXT NOT NULL,
            event_hash TEXT NOT NULL UNIQUE, recorded_ns INTEGER NOT NULL);
        """)

    @staticmethod
    def digest(text):
        return hashlib.sha256(text.encode()).hexdigest()

    def intent(self, scope, request):
        payload = json.dumps(request, sort_keys=True, separators=(",", ":"))
        request_hash = self.digest(payload)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            prior = self.db.execute("SELECT request_hash,sequence FROM claims WHERE scope=?", (scope,)).fetchone()
            if prior:
                if prior[0] != request_hash:
                    raise Conflict("scope already consumed by a different intent")
                self.db.execute("COMMIT")
                return prior[1], "duplicate"
            sequence = self.db.execute("SELECT COALESCE(MAX(sequence),0)+1 FROM events").fetchone()[0]
            prev = self.db.execute("SELECT event_hash FROM events ORDER BY sequence DESC LIMIT 1").fetchone()
            previous_hash = prev[0] if prev else "0" * 64
            recorded_ns = time.time_ns()
            body = f"{sequence}|{scope}|INTENT|{request_hash}|{previous_hash}|{recorded_ns}"
            event_hash = self.digest(body)
            self.db.execute("INSERT INTO claims VALUES(?,?,?)", (scope, request_hash, sequence))
            self.db.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?)",
                            (sequence, scope, "INTENT", request_hash, payload, previous_hash, event_hash, recorded_ns))
            self.db.execute("COMMIT")
            return sequence, "accepted"
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def verify(self):
        previous = "0" * 64
        rows = self.db.execute("SELECT sequence,scope,kind,request_hash,payload,previous_hash,event_hash,recorded_ns FROM events ORDER BY sequence").fetchall()
        for expected, row in enumerate(rows, 1):
            seq, scope, kind, request_hash, payload, prev, event_hash, ns = row
            body = f"{seq}|{scope}|{kind}|{request_hash}|{prev}|{ns}"
            if seq != expected or prev != previous or self.digest(body) != event_hash:
                return False
            if self.digest(payload) != request_hash:
                return False
            previous = event_hash
        # Detect partial event deletion or orphaned claims. A full database rollback
        # still requires an independently retained checkpoint to detect.
        claims = self.db.execute("SELECT scope,request_hash,sequence FROM claims ORDER BY sequence").fetchall()
        if len(claims) != len(rows):
            return False
        for scope, request_hash, sequence in claims:
            row = next((event for event in rows if event[0] == sequence), None)
            if row is None or (row[1], row[3]) != (scope, request_hash):
                return False
        return True

    def checkpoint(self):
        """Return a value an independent custodian must retain outside this DB."""
        row = self.db.execute("SELECT sequence,event_hash FROM events ORDER BY sequence DESC LIMIT 1").fetchone()
        return row if row else (0, "0" * 64)

    def count(self, scope):
        return self.db.execute("SELECT COUNT(*) FROM events WHERE scope=?", (scope,)).fetchone()[0]
