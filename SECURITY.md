# Security and verifier-integrity policy

This repository does not run a network service or handle credentials. The main
integrity risk is a verifier defect that accepts an invalid mathematical
certificate.

If you find a verifier-soundness bug, malformed-certificate acceptance path, or
a discrepancy between the claimed output and a clean replay, please report it
through a GitHub issue or pull request with the smallest reproducible example
you can provide.

Do not include secrets or unrelated private data in reports.

Verifier defects are treated as research-integrity issues: accepted-certificate
behavior, affected versions, certificate-byte impact, and regression tests
should be documented explicitly.
