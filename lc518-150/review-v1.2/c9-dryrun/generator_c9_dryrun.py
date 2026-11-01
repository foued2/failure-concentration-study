"""C9 dry-run generator (review artifact, NOT a bank). Implements CORRECTIONS_RECORD_v1.2.1 C9
items 1-8 as written. Where the spec is silent, the convention used is printed in GAPS and
recorded in the sidecar log. Spec mandate violations are recorded as SPEC_DEFECT events and
generation continues (so output stays deterministic and inspectable)."""
import hashlib, json, math, random, sys
from collections import defaultdict

INT32 = 2**31 - 1
CAP = 1000
SEEDS = {"diagnostic": 11052026, "heldout": 20261101}
GAPS = []      # spec silences / inconsistencies, documented as encountered
LOG = []       # sidecar events
DEFECTS = []   # mandate failures

def oracle(amount, coins):              # LC518 combinations count (unbounded, combinations)
    dp = [0] * (amount + 1); dp[0] = 1
    for c in coins:
        for a in range(c, amount + 1): dp[a] += dp[a - c]
    return dp[amount]

def n0(amount, coins):                  # N0: 0/1 subset-count over distinct coin values
    dp = [0] * (amount + 1); dp[0] = 1
    for c in set(coins):
        for a in range(amount, c - 1, -1): dp[a] += dp[a - c]
    return dp[amount]

def min_count(amount, coins):           # M(a) minimum coins (D5 reference only)
    INF = float("inf"); M = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and M[a - c] + 1 < M[a]: M[a] = M[a - c] + 1
    return M[amount]

def greedy_count(amount, coins):
    cnt, r = 0, amount
    for c in sorted(coins, reverse=True):
        q, r = divmod(r, c); cnt += q
    return cnt if r == 0 else None

def distinct(rng, lo, hi, n, exclude=()):   # one randrange per attempt; immediate redraw on collision
    out = []
    while len(out) < n:
        x = rng.randrange(lo, hi + 1)
        if x not in out and x not in exclude: out.append(x)
    return out

class Bank:
    def __init__(self, name, seed):
        self.name = name; self.rng = random.Random(seed)
        self.records = []; self.keys = set(); self.seq = 0

    def defect(self, where, msg):
        DEFECTS.append({"where": where, "msg": msg})

    def emit(self, stratum, rule_id, rule_params, amount, coins, canonical_id, redraws):
        self.seq += 1
        self.records.append({
            "input_id": f"{self.name[0].upper()}-{self.seq:03d}", "amount": amount,
            "coins": list(coins), "canonical_id": canonical_id, "stratum": stratum,
            "rule_id": rule_id, "rule_params": rule_params,
            "int32_guard": {"status": "redrawn" if redraws else "accepted", "redraws": redraws},
        })
        self.keys.add((amount, tuple(sorted(coins))))
        if redraws: LOG.append({"bank": self.name, "stratum": stratum, "seq": self.seq, "redraws": redraws})

    def accept_check(self, amount, coins, where, mandate=None):
        """returns (ok, answer) for int32 guard and canonical collision; mandate is callable(answer)->bool"""
        ans = oracle(amount, coins)
        if ans > INT32: return False, ans
        key = (amount, tuple(sorted(coins)))
        if key in self.keys: return False, ans
        if mandate is not None and not mandate(ans):
            self.defect(where, f"mandate failed: answer={ans} amount={amount} coins={coins}")
        return True, ans

def gen_single(bank, stratum, k, rule_id, rule_params, build, mandate=None, mode="defect"):
    """whole-record redraw loop: build(rng) returns (amount, coins, extra_params) consuming RNG"""
    redraws = 0
    for _ in range(CAP):
        amount, coins, params = build()
        if len(set(coins)) != len(coins) or any(not (1 <= c <= 5000) for c in coins) \
           or not (0 <= amount <= 5000):
            raise SystemExit(f"VALIDITY ABORT {stratum}-{k}: amount={amount} coins={coins}")
        ok, ans = bank.accept_check(amount, coins, f"{stratum}-{k}", None if mode == "redraw" else mandate)
        if ok and mode == "redraw" and mandate is not None and not mandate(ans):
            ok = False
        if ok:
            p = dict(rule_params); p.update(params)
            bank.emit(stratum, rule_id, p, amount, coins, f"{stratum}-{k:02d}", redraws)
            return
        redraws += 1
    raise SystemExit(f"CAP ABORT {stratum}-{k}")

def gen_pair(bank, stratum, inst, rule_id, build, params_base):
    redraws = 0
    for _ in range(CAP):
        amount, coins, perm = build()        # perm: Fisher-Yates permutation of coins (drawn by rng)
        ok, ans = bank.accept_check(amount, coins, f"{stratum}-pair{inst}")
        if ok and (amount, tuple(sorted(coins))) not in bank.keys and len(set(map(tuple, [coins, perm]))) >= 1:
            cid = f"{stratum}-pair{inst:02d}"
            bank.emit(stratum, rule_id, dict(params_base, pair_id=inst, ordering="original"),
                      amount, coins, cid, redraws)
            # permutation shares the canonical key, so bypass the duplicate check for this one record
            bank.records.append({
                "input_id": f"{bank.name[0].upper()}-{bank.seq+1:03d}", "amount": amount, "coins": list(perm),
                "canonical_id": cid, "stratum": stratum, "rule_id": rule_id,
                "rule_params": dict(params_base, pair_id=inst, ordering="permutation"),
                "int32_guard": {"status": "redrawn" if redraws else "accepted", "redraws": redraws}})
            bank.seq += 1
            return
        redraws += 1
    raise SystemExit(f"CAP ABORT pair {stratum}-{inst}")

def shuffle_perm(rng, coins):
    p = list(coins); rng.shuffle(p); return p

def build_diagnostic(rng):
    B = Bank("diagnostic", SEEDS["diagnostic"]); return B

def run(bank_name):
    seed = SEEDS[bank_name]
    if bank_name == "diagnostic":
        B = Bank("diagnostic", seed)
        # D1 boundary-amount: n -> coins -> derived amount (PATTERN)
        for k in range(1, 9):
            def b1(k=k):
                n = B.rng.randrange(1, 5); coins = distinct(B.rng, 1, 20, n)
                cmin = min(coins)
                PATTERN = [0, 1, 2, cmin - 1, cmin, cmin + 1, 2*cmin, 2*cmin + 1]
                return PATTERN[k-1], coins, {"c_min": cmin, "pattern_index": k-1}
            gen_single(B, "D1", k, "D1", {}, b1)
        # D2 exact-match: m -> c* -> distractors -> amount=c*
        for k in range(1, 9):
            def b2():
                m = B.rng.randrange(1, 5); cstar = B.rng.randrange(1, 5001)
                dis = distinct(B.rng, 1, 5000, m, exclude=(cstar,))
                return cstar, [cstar] + dis, {"match_coin": cstar}
            gen_single(B, "D2", k, "D2", {}, b2)
        GAPS.append("D2: as-given coin order (match coin first) not pinned; chosen [c*]+distractors")
        # D3 unreachable
        for k in range(1, 5):
            def b3():
                while True:
                    n = B.rng.randrange(2, 7); coins = distinct(B.rng, 1, 5000, n)
                    if min(coins) != 1: break
                cmin = min(coins)
                amount = B.rng.randrange(1, cmin) if cmin - 1 >= 2 else 1
                return amount, coins, {"mechanism": "min-coin"}
            gen_single(B, "D3", k, "D3", {}, b3, mandate=lambda a: a == 0)
        for k in range(5, 9):
            def b3g():
                g = B.rng.randrange(2, 11); n = B.rng.randrange(2, 7)
                t = distinct(B.rng, 1, 5000 // g, n); coins = [g*x for x in t]
                while True:
                    amount = B.rng.randrange(1, 5001)
                    if amount % g: break
                return amount, coins, {"mechanism": "gcd", "g": g}
            gen_single(B, "D3", k, "D3", {}, b3g, mandate=lambda a: a == 0)
        GAPS.append("D3 gcd: n drawn after g (order not pinned beyond amount-last rule)")
        # D4 modular-parity
        GAPS.append("D4 records 3-8: coin-set size n not specified; chosen randrange(2,7)")
        GAPS.append("D4 records 1-2/3-4: draw order not pinned; chosen amount,n,coins (default)")
        for k in range(1, 5):
            def b4(k=k):
                amount = None
                n = B.rng.randrange(2, 7)
                t = distinct(B.rng, 1, 2500, n)
                coins = [2*x - 1 for x in t]
                want_even = (k <= 2)
                while True:
                    a = B.rng.randrange(0, 5001)
                    if (a % 2 == 0) == want_even: break
                return a, coins, {"mechanism": "odd-even-amt" if want_even else "odd-odd-amt"}
            gen_single(B, "D4", k, "D4", {}, b4, mandate=(None if k <= 2 else (lambda a: a == 0)))
        for k in range(5, 9):
            def b4g():
                n = B.rng.randrange(2, 7)
                while True:
                    t = distinct(B.rng, 1, 2500, n)
                    g = 0
                    for x in t: g = math.gcd(g, x)
                    if g == 1: break
                    LOG.append({"bank": "diagnostic", "stratum": "D4", "event": "t-set redraw gcd!=1"})
                coins = [2*x for x in t]
                while True:
                    a = B.rng.randrange(0, 5001)
                    if a % 2 == 1: break
                return a, coins, {"mechanism": "gcd2"}
            gen_single(B, "D4", k, "D4", {}, b4g, mandate=lambda a: a == 0)
        # D5 non-greedy
        for k, (amt, coins) in enumerate([(6, [1, 3, 4]), (10, [1, 3, 4])], start=1):
            gen_single(B, "D5", k, "D5", {"anchor": True}, lambda amt=amt, coins=coins: (amt, coins, {}))
        for k in range(3, 9):
            def b5():
                while True:
                    n = B.rng.randrange(3, 6); rest = distinct(B.rng, 2, 9, n - 1)
                    coins = [1] + rest; amount = None
                    for _ in range(CAP):
                        a = B.rng.randrange(5, 31)
                        if greedy_count(a, coins) != min_count(a, coins): amount = a; break
                    if amount is not None: return amount, coins, {"anchor": False}
                    LOG.append({"bank": "diagnostic", "stratum": "D5", "event": "whole-record redraw (no divergence)"})
            gen_single(B, "D5", k, "D5", {}, b5)
        GAPS.append("D5 records 3-8: draw order n->coins->amount chosen (not stated); anchor flag set False")
        # D6 reorder pairs (instances 1-4): amount -> n -> coins -> shuffle
        for inst in range(1, 5):
            def b6():
                amount = B.rng.randrange(10, 201); n = B.rng.randrange(3, 9)
                coins = distinct(B.rng, 1, 200, n); perm = shuffle_perm(B.rng, coins)
                return amount, coins, perm
            gen_pair(B, "D6", inst, "D6", b6, {})
        # D7 wide-n, D8 large-amount
        for k in range(1, 9):
            def b7():
                amount = B.rng.randrange(50, 501); n = B.rng.randrange(50, 301)
                return amount, distinct(B.rng, 1, 5000, n), {}
            gen_single(B, "D7", k, "D7", {}, b7)
        for k in range(1, 9):
            def b8():
                amount = B.rng.randrange(2000, 5001); n = B.rng.randrange(3, 31)
                return amount, distinct(B.rng, 1, 5000, n), {}
            gen_single(B, "D8", k, "D8", {}, b8)
        return B
    else:
        B = Bank("heldout", seed)
        # H1 tiny-amount (amount 0 must give answer 1)
        for k in range(1, 13):
            def h1(k=k):
                amount = B.rng.randrange(0, 2) if k <= 3 else B.rng.randrange(2, 13)
                n = B.rng.randrange(1, 5); return amount, distinct(B.rng, 1, 20, n), {"edge": k <= 3}
            gen_single(B, "H1", k, "H1", {}, h1, mandate=None)  # amount-0 rule checked below
        for r in B.records:
            if r["stratum"] == "H1" and r["amount"] == 0 and oracle(0, r["coins"]) != 1:
                B.defect("H1", "amount-0 answer != 1")
        # H2 small-amount: records 1-4 forced coin 1; record 1 amount=max(coins)
        for k in range(1, 13):
            def h2(k=k):
                while True:
                    n = B.rng.randrange(2, 7)
                    if k <= 4:
                        coins = [1] + distinct(B.rng, 2, 60, n - 1)
                    else:
                        coins = distinct(B.rng, 1, 60, n)
                    if k == 1:
                        amount = max(coins)
                        if amount >= 13: break
                    else:
                        amount = B.rng.randrange(13, 61); break
                return amount, coins, {"forced_coin_1": k <= 4, "match_amount": k == 1}
            gen_single(B, "H2", k, "H2", {}, h2, mandate=lambda a: a >= 2, mode="redraw")
        GAPS.append("H2 records 5-12: n not specified; chosen randrange(2,7); H2 record 2-4 amount order default")
        # H3 single-coin
        for k in range(1, 9):
            def h3():
                amount = B.rng.randrange(0, 5001); coin = B.rng.randrange(1, 51)
                return amount, [coin], {}
            gen_single(B, "H3", k, "H3", {}, h3)
        # H4 two-coin
        for k in range(1, 9):
            def h4(k=k):
                if k <= 2:
                    coins = distinct(B.rng, 1, 5000, 2)
                    amount = max(coins)
                    while amount < 20:
                        coins = distinct(B.rng, 1, 5000, 2); amount = max(coins)
                    return amount, coins, {"match_amount": True}
                coins = distinct(B.rng, 1, 5000, 2); amount = B.rng.randrange(20, 5001)
                return amount, coins, {"match_amount": False}
            gen_single(B, "H4", k, "H4", {}, h4)
        # H5 many-coins
        for k in range(1, 11):
            def h5():
                amount = B.rng.randrange(100, 2001); n = B.rng.randrange(30, 121)
                return amount, distinct(B.rng, 1, 5000, n), {}
            gen_single(B, "H5", k, "H5", {}, h5)
        # H6 large-amount: 6 singletons + 2 reorder pairs
        for k in range(1, 7):
            def h6():
                amount = B.rng.randrange(3500, 5001); n = B.rng.randrange(5, 41)
                return amount, distinct(B.rng, 1, 5000, n), {"singleton": True}
            gen_single(B, "H6", k, "H6", {"singleton": True}, h6)
        for inst in range(1, 3):
            def h6p():
                amount = B.rng.randrange(3500, 5001); n = B.rng.randrange(5, 41)
                coins = distinct(B.rng, 1, 5000, n); perm = shuffle_perm(B.rng, coins)
                return amount, coins, perm
            gen_pair(B, "H6", inst, "H6", h6p, {})
        # H7 unreachable
        for k in range(1, 5):
            def h7():
                while True:
                    n = B.rng.randrange(2, 7); coins = distinct(B.rng, 1, 5000, n)
                    if min(coins) != 1: break
                cmin = min(coins); amount = B.rng.randrange(1, cmin) if cmin - 1 >= 2 else 1
                return amount, coins, {"mechanism": "min-coin"}
            gen_single(B, "H7", k, "H7", {}, h7, mandate=lambda a: a == 0)
        for k in range(5, 9):
            def h7g():
                g = B.rng.randrange(2, 11); n = B.rng.randrange(2, 7)
                t = distinct(B.rng, 1, 5000 // g, n); coins = [g*x for x in t]
                while True:
                    amount = B.rng.randrange(1, 5001)
                    if amount % g: break
                return amount, coins, {"mechanism": "gcd", "g": g}
            gen_single(B, "H7", k, "H7", {}, h7g, mandate=lambda a: a == 0)
        # H8 rich-combination
        for k in range(1, 13):
            def h8(k=k):
                if k <= 6:
                    anchor = [1, 2, 3]
                    n = B.rng.randrange(3, 9); rest = distinct(B.rng, 4, 5000, n - 3)
                    amount = B.rng.randrange(6, 801); return amount, anchor + rest, {"anchor": "1-2-3", "anchor_fixed": True}
                if k == 7:
                    return 6, [1, 3, 4], {"anchor": "1-3-4", "anchor_fixed": True}
                n = B.rng.randrange(3, 9); rest = distinct(B.rng, 2, 5000, n - 3, exclude=(1, 3, 4))
                amount = B.rng.randrange(6, 801); return amount, [1, 3, 4] + rest, {"anchor": "1-3-4", "anchor_fixed": True}
            gen_single(B, "H8", k, "H8", {}, h8)
        GAPS.append("H8 records 8-12: count of further coins not specified; chosen n=randrange(3,9) as records 1-6")
        return B

def serialize(rec):
    payload = {k: rec[k] for k in ("input_id","amount","coins","canonical_id","stratum","rule_id","rule_params","int32_guard")}
    b = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    out = dict(payload); out["record_sha256"] = hashlib.sha256(b).hexdigest()
    return json.dumps(out, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n"

if __name__ == "__main__":
    outdir = sys.argv[1]
    import os; os.makedirs(outdir, exist_ok=True)
    banks = {}
    for name in ("diagnostic", "heldout"):
        LOG.clear()
        B = run(name); banks[name] = B
        with open(f"{outdir}/{name}.jsonl", "w", encoding="utf-8", newline="\n") as f:
            for r in B.records: f.write(serialize(r))
        with open(f"{outdir}/{name}.sidecar.jsonl", "w", encoding="utf-8", newline="\n") as f:
            for e in LOG: f.write(json.dumps(e, sort_keys=True, separators=(",", ":")) + "\n")
    inter = banks["diagnostic"].keys & banks["heldout"].keys
    report = {"diagnostic_records": len(banks["diagnostic"].records), "heldout_records": len(banks["heldout"].records),
              "cross_bank_canonical_collisions": len(inter), "spec_defects": DEFECTS, "gaps": GAPS}
    with open(f"{outdir}/report.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=1, sort_keys=True)
    print(json.dumps({k: (v if k != "spec_defects" else len(v)) for k, v in report.items() if k != "gaps"}, indent=1))
