#!/usr/bin/env python3
"""
Verifier for a 60-step candidate extension of the good-prime-chain endpoint
used in the Erdős Problem #287 lower-bound certificate.

This verifies:
  1. recursive Pocklington-style primality certificates for all listed primes;
  2. each extension p_next = 2*q + 1 with q prime;
  3. the chain condition p_next <= 2*p_current - 3;
  4. the final coverage endpoint T = 2*p_final - 3;
  5. the integer bounds for floor(2*p_final/e^2) and floor((e-1)*B)+1
     using exact rational interval bounds for e.

This is a candidate verification bundle, not a full proof of Erdős #287.
"""

from __future__ import annotations
import json, math, sys
from fractions import Fraction
from pathlib import Path

SMALL_LIMIT = 10000

def trial_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    r = math.isqrt(n)
    while d <= r:
        if n % d == 0:
            return False
        d += 2
    return True

def verify_prime_cert(n: int, certs: dict[str, dict], memo: dict[int, bool]) -> bool:
    if n in memo:
        return memo[n]
    c = certs.get(str(n))
    if c is None:
        raise ValueError(f"missing certificate for {n}")
    if int(c["n"]) != n:
        raise ValueError(f"certificate key mismatch for {n}")
    if c.get("small", False):
        ok = n <= SMALL_LIMIT and trial_prime(n)
        memo[n] = ok
        return ok

    factors = {int(p): int(e) for p, e in c["factors"].items()}
    prod = 1
    for p, e in factors.items():
        prod *= p ** e
    if prod != n - 1:
        raise ValueError(f"bad factorization for n-1, n={n}")

    # Full factorization means F = n-1 > sqrt(n), satisfying Pocklington.
    if prod <= math.isqrt(n):
        raise ValueError(f"Pocklington product too small for n={n}")

    for p in factors:
        if not verify_prime_cert(p, certs, memo):
            raise ValueError(f"subfactor {p} of {n}-1 failed primality verification")

    bases = {int(p): int(a) for p, a in c["bases"].items()}
    for p in factors:
        a = bases.get(p)
        if a is None:
            raise ValueError(f"missing Pocklington base for n={n}, factor q={p}")
        if pow(a, n - 1, n) != 1:
            raise ValueError(f"Fermat congruence failed for n={n}, q={p}, a={a}")
        if math.gcd(pow(a, (n - 1) // p, n) - 1, n) != 1:
            raise ValueError(f"Pocklington gcd failed for n={n}, q={p}, a={a}")

    memo[n] = True
    return True

def e_bounds(N: int = 160) -> tuple[Fraction, Fraction]:
    # lower = sum_{i=0}^N 1/i!
    fact = 1
    lower = Fraction(1, 1)
    for i in range(1, N + 1):
        fact *= i
        lower += Fraction(1, fact)
    # R_N < (1/(N+1)!)/(1 - 1/(N+2)) = (N+2)/((N+1)!*(N+1)).
    fact_next = fact * (N + 1)
    tail_upper = Fraction(N + 2, fact_next * (N + 1))
    return lower, lower + tail_upper

def verify_floor_2p_over_e2(p: int, B: int) -> None:
    L, U = e_bounds()
    # To prove B = floor(2p/e^2):
    # B*e^2 <= 2p < (B+1)*e^2.
    # It suffices to show B*U^2 <= 2p and 2p < (B+1)*L^2.
    if not (Fraction(B, 1) * U * U <= 2 * p):
        raise ValueError("lower floor inequality B*e^2 <= 2p not certified")
    if not (2 * p < Fraction(B + 1, 1) * L * L):
        raise ValueError("upper floor inequality 2p < (B+1)*e^2 not certified")

def verify_k_bound(B: int, K: int) -> None:
    L, U = e_bounds()
    # K should be floor((e-1)B)+1, i.e. K-1 <= (e-1)B < K.
    if not (Fraction(K - 1, 1) <= Fraction(B, 1) * (L - 1)):
        raise ValueError("lower inequality for floor((e-1)B) not certified")
    if not (Fraction(B, 1) * (U - 1) < K):
        raise ValueError("upper inequality for floor((e-1)B) not certified")

def main(path: str) -> None:
    data = json.loads(Path(path).read_text())
    certs = data["certificates"]
    memo = {}

    p_current = int(data["start_endpoint_from_public_repo"])
    verify_prime_cert(p_current, certs, memo)

    for ext in data["extensions"]:
        q = int(ext["q"])
        p_next = int(ext["p_next"])
        if p_next != 2*q + 1:
            raise ValueError(f"step {ext['step']}: p_next != 2q+1")
        if p_next > 2*p_current - 3:
            raise ValueError(f"step {ext['step']}: chain condition failed")
        verify_prime_cert(q, certs, memo)
        verify_prime_cert(p_next, certs, memo)
        p_current = p_next

    p_final = int(data["final_endpoint"])
    if p_current != p_final:
        raise ValueError("final endpoint mismatch")
    T = 2*p_final - 3
    if T != int(data["coverage_endpoint_T_equals_2p_minus_3"]):
        raise ValueError("coverage endpoint mismatch")

    B = int(data["certified_n1_lower_bound_candidate"])
    K = int(data["certified_k_lower_bound_candidate"])
    verify_floor_2p_over_e2(p_final, B)
    verify_k_bound(B, K)

    print("OK: certificate chain verified")
    print(f"extensions: {len(data['extensions'])}")
    print(f"final p_m: {p_final}")
    print(f"T = 2*p_m - 3: {T}")
    print(f"candidate conclusion: n_1 > {B}")
    print(f"candidate conclusion: k >= {K}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 verify.py certificate.json", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
