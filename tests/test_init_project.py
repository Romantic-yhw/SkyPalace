from pathlib import Path
import importlib.util
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "make-sky-palace-video" / "scripts" / "init_project.py"


def load_script():
    spec = importlib.util.spec_from_file_location("init_project", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InitProjectTests(unittest.TestCase):
    def test_creates_default_project_without_overwriting(self):
        init_project = load_script()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            result = init_project.main(
                [
                    "--output",
                    str(out),
                    "--slug",
                    "moon-gate",
                    "--prompt",
                    "巨月打开天门，两位同行者赴约",
                ]
            )
            self.assertEqual(result, 0)
            project = out / "moon-gate"
            brief = json.loads((project / "brief.json").read_text(encoding="utf-8"))
            status = json.loads((project / "status.json").read_text(encoding="utf-8"))
            self.assertEqual(brief["schema_version"], 1)
            self.assertEqual(brief["shot_count"], 6)
            self.assertEqual(brief["duration_seconds"], 30)
            self.assertEqual(brief["aspect_ratio"], "16:9")
            self.assertEqual(brief["source_prompt"], "巨月打开天门，两位同行者赴约")
            self.assertEqual(status["stage"], "briefed")
            for relative in ["prompts/image", "prompts/video", "images", "clips"]:
                self.assertTrue((project / relative).is_dir(), relative)
            for relative in ["world-bible.md", "storyboard.md", "qa-report.json"]:
                self.assertTrue((project / relative).is_file(), relative)
            with self.assertRaises(FileExistsError):
                init_project.main(
                    [
                        "--output",
                        str(out),
                        "--slug",
                        "moon-gate",
                        "--prompt",
                        "重复",
                    ]
                )

    def test_custom_options_and_slug_safety(self):
        init_project = load_script()
        with tempfile.TemporaryDirectory() as tmp:
            result = init_project.main(
                [
                    "--output",
                    tmp,
                    "--slug",
                    "Rain 天宫 / 15s",
                    "--prompt",
                    "暴雨散去后女剑客进入天宫",
                    "--duration",
                    "15",
                    "--shots",
                    "4",
                    "--aspect-ratio",
                    "9:16",
                ]
            )
            self.assertEqual(result, 0)
            projects = list(Path(tmp).iterdir())
            self.assertEqual(len(projects), 1)
            self.assertNotIn("/", projects[0].name)
            brief = json.loads((projects[0] / "brief.json").read_text(encoding="utf-8"))
            self.assertEqual(brief["duration_seconds"], 15)
            self.assertEqual(brief["shot_count"], 4)
            self.assertEqual(brief["aspect_ratio"], "9:16")


if __name__ == "__main__":
    unittest.main()
