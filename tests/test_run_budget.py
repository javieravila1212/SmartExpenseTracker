import unittest
import subprocess
import sys
import os


class TestBudgetRun(unittest.TestCase):
    def test_budget_runs_and_adds_entries(self):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        script = os.path.join(repo_root, "budget.py")
        proc = subprocess.run([sys.executable, script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, msg=f"Script failed: {proc.stderr}")
        out = (proc.stdout or "") + (proc.stderr or "")
        self.assertIn("Shawarma", out)
        self.assertIn("Netflix Monthly Plan", out)
        self.assertIn("Outdoor Games with friends", out)


if __name__ == "__main__":
    unittest.main()
