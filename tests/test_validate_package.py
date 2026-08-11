from pathlib import Path
from contextlib import redirect_stdout
import importlib.util
import io
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "make-sky-palace-video" / "scripts" / "validate_package.py"
FIXTURES = ROOT / "tests" / "fixtures"


def load_script():
    spec = importlib.util.spec_from_file_location("validate_package", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidatePackageTests(unittest.TestCase):
    def test_valid_package_passes(self):
        validator = load_script()
        result = validator.validate(FIXTURES / "valid-package")
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.errors, [])

    def test_invalid_package_reports_each_intended_defect(self):
        validator = load_script()
        result = validator.validate(FIXTURES / "invalid-package")
        self.assertFalse(result.ok)
        errors = "\n".join(result.errors)
        self.assertIn("scale_ladder", errors)
        self.assertIn("primary_wonder", errors)
        self.assertIn("单段", errors)
        self.assertIn("paid_generation_authorized", errors)

    def test_cli_returns_nonzero_for_invalid_package(self):
        validator = load_script()
        output = io.StringIO()
        with redirect_stdout(output):
            result = validator.main([str(FIXTURES / "invalid-package"), "--json"])
        self.assertEqual(result, 1)
        self.assertIn('"ok": false', output.getvalue())


if __name__ == "__main__":
    unittest.main()
