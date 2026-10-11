# FREEZE — v0.1

**Frozen at:** 2026-10-11T11:21:36.718675+00:00
**Protocol hash (sha256(PROTOCOL.md)):** `6c4991cc0a8741ece4728791d8cad1a7e9dc8f35dec183ad4de5a0b051f6bd39`
**Confirmatory seed derivation:** `int.from_bytes(sha256(f'6c4991cc0a8741ec:confirmatory:{i}')[:4],'big')` for i = 0..N_c-1

## Gate evidence (must pass before freeze)

- G1 partition: 240/240 probes satisfy exactly one declared predicate across seeds [101, 102, 103, 201, 202, 203, 204, 205]; violations: 0
- G2 measurement chain: 6 hand-computed cases passed (k/C values, eligibility boundary, Y labels, crash-as-failure, output identity)
- G3 oracle chain: reference vs brute force on 60 tiny random graphs; mismatches: 0
- All gates pass: **True** (report: gates/gates_report.json)

G1 establishes the declared partition property only — not construct validity (PROTOCOL.md §3).

## Frozen file hashes (sha256)

- `PROTOCOL.md`: `6c4991cc0a8741ece4728791d8cad1a7e9dc8f35dec183ad4de5a0b051f6bd39`
- `specs/instrument_spec.json`: `7631f368e1b48dd044e51cbd01a6f4766cffe30a618058c7054175fe99907bc6`
- `specs/generator_spec.json`: `c4b85ac0e01ef13c9f92b60da440da118b88e69a55e6a3fa97a1d3b74840e1ec`
- `study/sssp.py`: `d92463d7b274e8078181e08d7beb6598437d03828153a8595e4558e44b5b8824`
- `study/families.py`: `5da53226991e4103ec6886ee7bdddcdc9849c462e00d803658f9314388be31e2`
- `study/probes.py`: `cc123c8f0bbbe2625f5a1d6ea9e6ba8f7ea1530565c999e367eafa0baf149ead`
- `study/instances.py`: `200830f924d2149ffe9aa9ac4b0c31aaebb8f30a16d8e6595bf838ff651bcb5b`
- `study/features.py`: `0447aa085eea65a964422110d2e18bebba965a14f225c09b5835dda3bf493a6a`
- `study/models.py`: `4e4226fe055dcfdfc4074c77eb5cbf8860f1c747a21dd15dc53a8af3c6c4c420`
- `scripts/run_gates.py`: `5f84617e9bc5434f2fe2409b504edff339b726f6f74ab3dbae04332c39ea13e6`
- `scripts/run_pilot.py`: `aeed1b957086929aff2c357bc2762cd89acf9d737c43f4b7099efa0a8ee6b390`
- `scripts/freeze.py`: `92e1d859af434d4f22ad8be2ece57445cdcca60c92dac1e7c50383cf26d7e234`

## Terminology (binding, PROTOCOL.md §6 / GPT ratification)

- An observation is a (solver, instance) pair.
- The binary outcome Y is whether that solver passes all 20 hidden oracle inputs assigned to that instance.
- The 20 hidden inputs are never counted as 20 independent observations.
- Inference concerns unseen problem instances under the fixed generator and solver-pack protocol, not unseen solver-generating models.

## Scope of any positive result

Predictive value only, conditional on the frozen instrument, generator, class, and threshold δ = 0.01 nats. Not localization. Not novelty. All outcomes terminal.
