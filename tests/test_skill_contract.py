from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "make-sky-palace-video"


class SkillContractTests(unittest.TestCase):
    def test_skill_and_required_references_exist(self):
        required = [
            "SKILL.md",
            "agents/openai.yaml",
            "references/visual-bible.md",
            "references/wonder-design.md",
            "references/image-prompts.md",
            "references/video-prompts.md",
            "references/shot-library.md",
            "references/quality-gates.md",
            "references/examples.md",
        ]
        for relative in required:
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_frontmatter_and_routing_contract(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(match)
        keys = re.findall(r"^([a-zA-Z0-9_-]+):", match.group(1), re.M)
        self.assertEqual(keys, ["name", "description"])
        self.assertIn("name: make-sky-palace-video", match.group(1))
        self.assertRegex(match.group(1), r"description: [\"']?Use when")
        for name in [
            "visual-bible.md",
            "wonder-design.md",
            "image-prompts.md",
            "video-prompts.md",
            "shot-library.md",
            "quality-gates.md",
        ]:
            self.assertIn(name, text)
        self.assertIn("付费", text)
        self.assertIn("status.json", text)

    def test_prompt_contract_keywords_are_explicit(self):
        image = (SKILL / "references/image-prompts.md").read_text(encoding="utf-8")
        video = (SKILL / "references/video-prompts.md").read_text(encoding="utf-8")
        wonder = (SKILL / "references/wonder-design.md").read_text(encoding="utf-8")
        self.assertIn("无遮挡", image)
        self.assertIn("单段", video)
        self.assertIn("四级尺度链", wonder)


if __name__ == "__main__":
    unittest.main()
