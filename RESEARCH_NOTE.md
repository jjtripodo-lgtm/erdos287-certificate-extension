# A 60-Step Good-Prime-Chain Certificate Extension for Erdős Problem #287

**Author:** John Tripodo  
**Version:** 1.0.0  
**Date:** 25 September 2026  
**Status:** Finite computational certificate contribution; not a solution of Erdős Problem #287.

## Abstract

This note documents a replayable 60-step extension of the public
good-prime-chain certificate framework used in work on Erdős Problem #287. The
extension starts from the previously public endpoint

`147573952589666836319`

and reaches

`170141183460458188881246205425652556267`.

The accompanying pure-Python verifier checks recursive Pocklington-style
primality certificates, every extension relation, the required chain
inequality, and the exact rational-arithmetic calculations used to produce the
reported framework-level candidate bounds. The artifact is intentionally
narrow: it verifies the finite extension and associated arithmetic, while the
interpretation of those numbers for Erdős Problem #287 depends on the upstream
public good-prime-chain framework.

## 1. Exact contribution

Let `p_0 = 147573952589666836319`, the starting endpoint imported from the
earlier public work. The file `certificate.json` supplies 60 successive
extensions. For every listed step the verifier checks

`p_next = 2*q + 1`

with `q` prime, together with

`p_next <= 2*p_current - 3`.

Primality is checked recursively from the certificate data rather than accepted
from a floating-point or probable-prime oracle.

After 60 steps the final endpoint is

`p_60 = 170141183460458188881246205425652556267`.

The corresponding stored coverage endpoint is

`T = 2*p_60 - 3 = 340282366920916377762492410851305112531`.

Within the upstream framework, the bundle records the corresponding candidate
numerical conclusions

`n_1 > 46052210507667183445041489711610410843`

and

`k >= 79130676475695223796910814477834233015`.

Those last two inequalities are **not** presented here as a standalone proof of
Erdős Problem #287. Their problem-level interpretation relies on the earlier
framework that this repository does not reprove.

## 2. What the verifier checks

`verify.py` checks four layers of the artifact:

1. recursive Pocklington-style primality certificates for the listed primes;
2. the relation `p_next = 2*q + 1` and the chain inequality at every step;
3. consistency of the final endpoint and the stored value `T = 2*p_final - 3`;
4. the reported numerical conversions using exact rational upper and lower
   bounds for `e`, rather than binary floating-point approximations.

A clean replay is:

```bash
python3 verify.py certificate.json
```

and the successful output is fixed in `expected_output.txt`.

The regression suite is:

```bash
python3 -m unittest test_verify.py
```

It includes negative controls intended to reject malformed or forged
certificates.

## 3. Verifier repair and integrity

On 20 September 2026, a defect was repaired in the small-prime validation path:
a false Boolean result could previously be ignored by the top-level chain loop.
The repair makes such a failure raise an error and adds adversarial regression
tests, including a forged `7 -> 9` example.

This repair did **not** alter `certificate.json` or the expected successful
output for the 60-step extension. The repository's checksum manifest records
the exact bytes of the current public bundle.

## 4. Provenance and attribution

The original public bundle is preserved in Git history at commit

`2caf568d7ebfc90faf22657dbcf7dd3ae29ae798`.

This extension builds on the public good-prime-chain framework and earlier
endpoint work attributed in the repository to **Woett, catsflowers5544, and
KentaKitamura**. Those upstream contributions are not claimed as original work
of this artifact.

The bounded contribution claimed by this repository is the 60-step extension,
the certificate data needed to replay it, and the accompanying verification
and packaging work.

## 5. AI assistance

AI tools assisted with search, packaging, verification-workflow cleanup,
adversarial test design, and documentation. The contribution is therefore
described transparently as AI-assisted. The repository is structured so that a
reader does not need to trust an AI-generated narrative: the finite certificate
and verification code are the inspectable objects.

## 6. Citation

Machine-readable citation metadata is provided in `CITATION.cff`.

Until a DOI-bearing archival release exists, cite the repository together with
the exact Git commit used. A DOI can later be added without changing the
mathematical claim boundary of this note.
