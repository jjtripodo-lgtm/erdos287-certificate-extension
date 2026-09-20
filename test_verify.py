import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent

class CertificateVerifierTest(unittest.TestCase):
    def run_data(self, data):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "certificate.json"
            p.write_text(json.dumps(data))
            return subprocess.run([sys.executable, str(ROOT / "verify.py"), str(p)],
                                  text=True, capture_output=True)

    def test_published_certificate_and_output(self):
        data = json.loads((ROOT / "certificate.json").read_text())
        result = self.run_data(data)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (ROOT / "expected_output.txt").read_text())

    def test_rejects_composite_extension(self):
        # The old verifier accepted q=4 and p_next=9: it ignored False returns.
        data = {
            "certificates": {str(n): {"n": n, "small": True} for n in [7, 4, 9]},
            "start_endpoint_from_public_repo": 7,
            "extensions": [{"step": 1, "q": 4, "p_next": 9}],
            "final_endpoint": 9, "coverage_endpoint_T_equals_2p_minus_3": 15,
            "certified_n1_lower_bound_candidate": 2, "certified_k_lower_bound_candidate": 4,
        }
        result = self.run_data(data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("small-prime certificate failed", result.stderr)

    def test_rejects_composite_initial_endpoint(self):
        data = {
            "certificates": {"9": {"n": 9, "small": True}},
            "start_endpoint_from_public_repo": 9, "extensions": [],
            "final_endpoint": 9, "coverage_endpoint_T_equals_2p_minus_3": 15,
            "certified_n1_lower_bound_candidate": 2, "certified_k_lower_bound_candidate": 4,
        }
        self.assertNotEqual(self.run_data(data).returncode, 0)

    def test_rejects_tampered_pocklington_base(self):
        data = json.loads((ROOT / "certificate.json").read_text())
        cert = data["certificates"][str(data["final_endpoint"]) ]
        cert["bases"][next(iter(cert["bases"]))] = "1"
        self.assertNotEqual(self.run_data(data).returncode, 0)

if __name__ == "__main__":
    unittest.main()
