# FREEZE — v0.2

**Frozen at:** 2026-10-12T12:56:28.023907+00:00
**v0.2 protocol hash:** `99a7f7f00d14b98e48a9606da78d909981359630f9b0838c3eba6312c01921ae`
**Confirmatory seeds:** `int.from_bytes(sha256(f'99a7f7f00d14b98e:confirmatory:{i}')[:4],'big')` for i = 0..39, asserted distinct from pilot seeds 101-103

## Gate evidence

- G1: 180/180 probes exact-one predicate (reused instrument)
- G2: 4 v0.2 chain checks (soft labels, instance weights, LOIO, shared relabel)
- G3: 160 hidden inputs checked vs brute force, 0 mismatches
- All pass: **True**

## v0.2 file hashes

- `v02/PROTOCOL_V02.md`: `99a7f7f00d14b98e48a9606da78d909981359630f9b0838c3eba6312c01921ae`
- `v02/spec_v02.json`: `c5aa8fe2bc52b3e692dcb81899f694f8805b33c17d745693870752167d398eac`
- `v02/models_v02.py`: `65d4b15764cc9890985e6de5a063208623df43d7829588da33d6af6cef8b0730`
- `v02/run_gates_v02.py`: `34f6270352a54adc5c1da46aab5fa806f81e7803a095af8d5125a13d8e8ce304`
- `v02/run_pilot_v02.py`: `737b3440a641741932a40a36939e34543ad604cc1d898a314650271fa41346af`
- `v02/run_confirmatory_v02.py`: `19c4104759038dcc5bcd6977baca6e73412f3b08f9f14565c23620e48953845e`
- `v02/generate_pack.py` (added by addendum before any pack emission; body frozen): `d7c3f86fbdd9cb162b8c619f3e358f6fad87765e877e6158b22973e084f8a907`
- `generation_v02/pack/` (120 single-shot submissions; ordered SHA256-of-SHA256 manifest): `cc695487c9e31c00424ae283b493ae2ded584eaf087a1bfa63458364a3ff828e`

## Reused v0.1 instrument hashes (imported unchanged)

- `study/sssp.py`: `d92463d7b274e8078181e08d7beb6598437d03828153a8595e4558e44b5b8824`
- `study/families.py`: `5da53226991e4103ec6886ee7bdddcdc9849c462e00d803658f9314388be31e2`
- `study/probes.py`: `cc123c8f0bbbe2625f5a1d6ea9e6ba8f7ea1530565c999e367eafa0baf149ead`
- `study/instances.py`: `200830f924d2149ffe9aa9ac4b0c31aaebb8f30a16d8e6595bf838ff651bcb5b`
- `study/features.py`: `0447aa085eea65a964422110d2e18bebba965a14f225c09b5835dda3bf493a6a`
- `study/models.py`: `4e4226fe055dcfdfc4074c77eb5cbf8860f1c747a21dd15dc53a8af3c6c4c420`
- `specs/instrument_spec.json`: `7631f368e1b48dd044e51cbd01a6f4766cffe30a618058c7054175fe99907bc6`

Post-freeze: G3 re-run on all 40 confirmatory hidden sets before pack execution; recorded in confirmatory log.
Outcome rules and pilot gate as frozen in v02/PROTOCOL_V02.md §§5-6.
