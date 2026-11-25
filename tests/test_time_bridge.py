import subprocess
import sys
import unittest


class TimeBridgeTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "time_bridge.py", *args], text=True, capture_output=True
        )

    def test_invalid_later_zone_does_not_print_partial_output(self):
        result = self.run_cli("2026-11-23T14:30Z", "UTC", "Invalid/Zone")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("Invalid/Zone", result.stderr)

    def test_out_of_range_conversion_reports_a_usage_error(self):
        result = self.run_cli("9999-12-31T23:30Z", "Asia/Tokyo")
        self.assertEqual(result.returncode, 2)
        self.assertIn("out of range", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_fall_back_folds_resolve_to_distinct_instants(self):
        args = ["2026-11-01T01:30", "UTC", "--from", "America/Chicago", "--fold"]
        for fold, hour in (("0", "06"), ("1", "07")):
            with self.subTest(fold=fold):
                result = self.run_cli(*args, fold)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"2026-11-01 {hour}:30:00+00:00", result.stdout)
