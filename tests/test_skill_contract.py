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

    def test_wonder_design_defines_observable_spectacle_mechanics(self):
        text = (SKILL / "references/wonder-design.md").read_text(encoding="utf-8")
        for marker in [
            "不可能关系",
            "四级尺度链",
            "出框延伸",
            "前景遮挡",
            "有效留白",
            "延迟揭示",
            "奇观升级",
        ]:
            self.assertIn(marker, text)

    def test_image_prompt_reference_covers_full_visual_grammar(self):
        text = (SKILL / "references/image-prompts.md").read_text(encoding="utf-8")
        for marker in [
            "输出约束",
            "核心奇观",
            "前景",
            "中景",
            "远景",
            "极远景",
            "建筑结构",
            "人物连续性",
            "摄影机",
            "巨构占比",
            "有效留白",
            "行动区",
            "光线",
            "色彩",
            "材质",
            "失败规避",
        ]:
            self.assertIn(marker, text)

    def test_video_prompt_reference_covers_motion_and_stability(self):
        text = (SKILL / "references/video-prompts.md").read_text(encoding="utf-8")
        for marker in [
            "首帧锁定",
            "摄影机轨迹",
            "人物动作",
            "分层环境运动",
            "视差",
            "揭示节拍",
            "结束状态",
            "连续性",
            "防漂移",
            "单段",
        ]:
            self.assertIn(marker, text)

    def test_quality_gates_block_weak_or_fake_delivery(self):
        text = (SKILL / "references/quality-gates.md").read_text(encoding="utf-8")
        for marker in ["100分", "85分", "阻塞", "局部重做", "历史素材"]:
            self.assertIn(marker, text)

    def test_shot_library_has_twelve_distinct_archetypes(self):
        text = (SKILL / "references/shot-library.md").read_text(encoding="utf-8")
        for code in [f"W{i:02d}" for i in range(1, 13)]:
            self.assertIn(code, text)


if __name__ == "__main__":
    unittest.main()
