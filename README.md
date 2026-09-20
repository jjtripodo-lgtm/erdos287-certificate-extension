# Erdős Problem #287: 60-step good-prime-chain certificate extension

This bundle is a replayable certificate extension inside the already-public good-prime-chain framework discussed on the Erdős Problem #287 thread.

It is **not** a proof of Erdős Problem #287.

## Claim boundary

Safe claim:

```text
A 60-step certificate extension inside the public good-prime-chain framework.
```

Unsafe claim:

```text
#287 solved.
```

## Files

- `certificate.json`: recursive Pocklington-style certificate data for the chain.
- `verify.py`: pure-Python verifier with no external dependencies.
- `expected_output.txt`: exact output from a successful clean replay.
- `SHA256SUMS`: hash manifest for the public bundle files.

## Public baseline and extension

Public thread baseline:

```text
p_m = 147573952589666836319
n_1 > 39943925344138028689
k >= 68634921076157089631
```

This bundle extends that framework to:

```text
final p_m: 170141183460458188881246205425652556267
T = 2*p_m - 3: 340282366920916377762492410851305112531
candidate conclusion: n_1 > 46052210507667183445041489711610410843
candidate conclusion: k >= 79130676475695223796910814477834233015
```

## Clean replay

From a clean folder containing these files, run:

```bash
python3 verify.py certificate.json
```

The exact expected output is:

```text
OK: certificate chain verified
extensions: 60
final p_m: 170141183460458188881246205425652556267
T = 2*p_m - 3: 340282366920916377762492410851305112531
candidate conclusion: n_1 > 46052210507667183445041489711610410843
candidate conclusion: k >= 79130676475695223796910814477834233015
```

## Attribution

This extends the public good-prime-chain framework built from prior forum work by Woett, catsflowers5544, and KentaKitamura.

## AI assistance disclosure

AI tools helped with repository packaging, verification workflow cleanup, and documentation drafting. The certificate replay and exact output were checked locally before treating this bundle as ship-ready.

## Verifier repair, 20 September 2026

A failed small-prime certificate now raises an error. Previously its Boolean failure could be ignored by the top-level chain loop; a forged 7 -> 9 step with q=4 was accepted. This was a verifier-input validation defect, not a failed check in the published 60-step certificate. The certificate bytes and expected successful output are unchanged. Run `python3 -m unittest test_verify.py` for the published certificate and negative controls.
