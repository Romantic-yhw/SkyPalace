from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryDocumentationTests(unittest.TestCase):
    def test_readme_documents_installation_and_one_line_usage(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for marker in [
            "SkyPalace",
            "make-sky-palace-video",
            "$make-sky-palace-video",
            "install-skill-from-github.py",
            "renmu2017/SkyPalace",
            "一句话",
            "巨月打开天门",
        ]:
            self.assertIn(marker, readme)

    def test_readme_documents_modes_outputs_and_boundaries(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for marker in [
            "仅提示词",
            "关键帧",
            "视频片段",
            "完整生产包",
            "brief.json",
            "world-bible.md",
            "status.json",
            "付费",
            "不自动发布",
            "video_prompts_ready",
            "0.25%–0.8%",
            "人物小于门钉",
            "45%–65%",
        ]:
            self.assertIn(marker, readme)

    def test_readme_documents_validation_and_troubleshooting(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for marker in [
            "quick_validate.py",
            "validate_package.py",
            "unittest discover",
            "故障排查",
            "验证码",
            "生成工具不可用",
        ]:
            self.assertIn(marker, readme)


if __name__ == "__main__":
    unittest.main()
