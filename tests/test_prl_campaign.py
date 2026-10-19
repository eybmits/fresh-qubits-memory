"""Failure-path checks for the replay boundary, with real subprocess exit codes."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prl_campaign", ROOT / "scripts/run_prl_campaign.py")
campaign = importlib.util.module_from_spec(spec)
spec.loader.exec_module(campaign)


class PrlCampaignTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name) / "run"
        self.fixture = {model: [json.loads((campaign.SIM / f"results_main_{model}.json").read_text())[0]]
                        for model in campaign.MODELS}

    def command(self, model, data, code=0):
        # An actual child process writes a result, then succeeds or fails. This
        # exercises the same process boundary as the expensive scientific jobs.
        script = "from pathlib import Path; import sys; Path(sys.argv[1]).write_text(sys.argv[2]); sys.exit(int(sys.argv[3]))"
        return [sys.executable, "-c", script, f"results_main_{model}.json", json.dumps(data), str(code)]

    def plan(self, fixtures=None, codes=None):
        fixtures = fixtures if fixtures is not None else self.fixture
        codes = codes or {}
        return {model: [self.command(model, fixtures[model], codes.get(model, 0))] for model in campaign.MODELS}

    def assert_failed_without_merge(self):
        manifest = json.loads((self.output / "run_manifest.json").read_text())
        self.assertEqual(manifest["status"], "failed")
        self.assertFalse((self.output / "results_main.json").exists())
        return manifest

    def test_existing_output_rejected_even_when_saved_data_look_complete(self):
        self.output.mkdir()
        for model, data in self.fixture.items():
            (self.output / f"results_main_{model}.json").write_text(json.dumps(data))
        sentinel = self.output / "run_manifest.json"
        sentinel.write_text('{"status": "old run"}')
        with patch.object(campaign, "run_lane") as lane:
            with self.assertRaises(FileExistsError):
                campaign.run(self.output, smoke=True)
            lane.assert_not_called()
        self.assertEqual(sentinel.read_text(), '{"status": "old run"}')
        self.assertFalse((self.output / "results_main.json").exists())

    def test_nonzero_lane_cannot_succeed_with_complete_result_files(self):
        with patch.object(campaign, "commands", return_value=self.plan(codes={"ising": 7, "haar": 8})):
            with self.assertRaisesRegex(ValueError, "Failed simulation lane"):
                campaign.run(self.output, smoke=True)
        manifest = self.assert_failed_without_merge()
        self.assertEqual(manifest["lanes"]["ising"][0]["returncode"], 7)
        self.assertEqual(manifest["lanes"]["haar"][0]["returncode"], 8)

    def test_zero_exit_with_partial_realizations_fails_before_merge(self):
        partial = copy.deepcopy(self.fixture)
        partial["haar"][0]["W"].pop()
        with patch.object(campaign, "commands", return_value=self.plan(fixtures=partial)):
            with self.assertRaisesRegex(ValueError, "six realizations"):
                campaign.run(self.output, smoke=True)
        self.assert_failed_without_merge()

    def test_zero_exit_with_missing_file_fails_before_merge(self):
        plan = self.plan()
        plan["haar"] = [[sys.executable, "-c", "pass"]]
        with patch.object(campaign, "commands", return_value=plan):
            with self.assertRaisesRegex(ValueError, "Missing or unsafe result"):
                campaign.run(self.output, smoke=True)
        self.assert_failed_without_merge()

    def test_complete_jobs_merge_and_record_every_exit_code(self):
        with patch.object(campaign, "commands", return_value=self.plan()):
            manifest = campaign.run(self.output, smoke=True)
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(json.loads((self.output / "results_main.json").read_text()),
                         self.fixture["ising"] + self.fixture["haar"])
        self.assertEqual(len(manifest["lanes"]), 2)
        self.assertTrue(all(record["returncode"] == 0 for lane in manifest["lanes"].values() for record in lane))
        self.assertIn("results_main.json", manifest["result_sha256"])

    def test_smoke_rejects_numerical_drift_even_with_complete_records(self):
        changed = copy.deepcopy(self.fixture)
        changed["ising"][0]["curves"][0][0] += 0.01
        with patch.object(campaign, "commands", return_value=self.plan(fixtures=changed)):
            with self.assertRaisesRegex(ValueError, "smoke curve error"):
                campaign.run(self.output, smoke=True)
        self.assert_failed_without_merge()

    def test_full_contract_accepts_supplied_complete_campaign(self):
        validated = campaign.validate_results(campaign.SIM, smoke=False)
        self.assertEqual(len(validated["validate_pairs.json"]), 24)
        self.assertEqual(len(validated["results_main_ising.json"]), 15)
        self.assertEqual(len(validated["results_tau.json"]), 5)

    def test_duplicate_or_wrong_configuration_rejected(self):
        wrong = copy.deepcopy(self.fixture)
        wrong["haar"][0]["k"] = 2
        with patch.object(campaign, "commands", return_value=self.plan(fixtures=wrong)):
            with self.assertRaisesRegex(ValueError, "configuration mismatch"):
                campaign.run(self.output, smoke=True)
        self.assert_failed_without_merge()


if __name__ == "__main__":
    unittest.main()
