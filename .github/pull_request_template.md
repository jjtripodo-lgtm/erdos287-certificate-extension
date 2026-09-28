## Change type

- [ ] verifier correctness / negative control
- [ ] certificate data
- [ ] documentation / citation / packaging
- [ ] CI / reproducibility

## Claim impact

Does this change the bounded mathematical claim, final endpoint, or expected
output? If yes, list every affected artifact.

## Verification

- [ ] `python3 verify.py certificate.json`
- [ ] `python3 -m unittest test_verify.py`
- [ ] malformed/adversarial input test added when verifier behavior changes
- [ ] hashes/expected output updated if bytes or output changed
- [ ] no full-#287 solve claim introduced
