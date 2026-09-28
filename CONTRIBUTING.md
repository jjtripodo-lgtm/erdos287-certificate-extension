# Contributing

This repository is a narrow, replayable research artifact. Contributions are
welcome when they improve verifier correctness, reproducibility, documentation,
or the exact bounded certificate claim.

## Before opening a pull request

Run:

```bash
python3 verify.py certificate.json
python3 -m unittest test_verify.py
```

A change to verifier behavior should include a regression/negative-control test.

## Claim boundary

Do not describe this repository as a proof of Erdős Problem #287. The claimed
contribution is the 60-step certificate extension inside the upstream public
good-prime-chain framework, together with its replayable verification bundle.

Changes that alter `certificate.json`, the final endpoint, or the numerical
conclusions must update:

- `expected_output.txt`;
- `SHA256SUMS`;
- `RESEARCH_NOTE.md`;
- `README.md`;
- citation/version metadata as appropriate.

Preserve upstream attribution and AI-assistance disclosure.
