# SkyPalace Video Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a provider-neutral Codex Skill that turns one Chinese sentence into a validated, production-ready Chinese celestial-wonder image-to-video package.

**Architecture:** Keep the orchestration contract concise in `SKILL.md`, route detailed visual and prompt knowledge to focused references, and place deterministic project scaffolding and package validation in two standard-library Python scripts. Validate instructions and documentation with contract tests, validate scripts with behavior tests, and use the prior “奇观感不足” result as the RED skill baseline.

**Tech Stack:** Codex Skill markdown, YAML, Python 3 standard library, `unittest`, Git.

---

## File map

| Path | Responsibility |
| --- | --- |
| `README.md` | Repository purpose, installation, one-line usage, modes, compatibility, cost and publishing boundaries |
| `skills/make-sky-palace-video/SKILL.md` | Triggered workflow, resource routing, gates, deliverables and stop conditions |
| `skills/make-sky-palace-video/agents/openai.yaml` | UI display name, description and default invocation |
| `skills/make-sky-palace-video/references/visual-bible.md` | Original Chinese celestial architecture, materials, people, palette and continuity |
| `skills/make-sky-palace-video/references/wonder-design.md` | Impossible relationship, scale ladder, framing, negative space and reveal design |
| `skills/make-sky-palace-video/references/image-prompts.md` | Exact image-prompt grammar and quality requirements |
| `skills/make-sky-palace-video/references/video-prompts.md` | Exact single-paragraph image-to-video prompt grammar and motion requirements |
| `skills/make-sky-palace-video/references/shot-library.md` | Composable shot archetypes and six-shot escalation patterns |
| `skills/make-sky-palace-video/references/quality-gates.md` | Brief, storyboard, image, motion, continuity and delivery gates |
| `skills/make-sky-palace-video/references/examples.md` | One complete one-line-to-six-shot example |
| `skills/make-sky-palace-video/scripts/init_project.py` | Safely initialize an isolated production package |
| `skills/make-sky-palace-video/scripts/validate_package.py` | Validate package structure and prompt quality signals |
| `tests/test_skill_contract.py` | Skill metadata, routing and documentation contract |
| `tests/test_init_project.py` | Project initializer behavior |
| `tests/test_validate_package.py` | Validator success and failure behavior |
| `tests/test_repository_docs.py` | Installation and usage documentation contract |
| `tests/fixtures/` | Valid and invalid package fixtures |

## Task 1: Capture the failing baseline and write Skill contract tests

**Files:**
- Create: `tests/test_skill_contract.py`
- Create: `tests/fixtures/baseline-v3-feedback.md`

- [x] **Step 1: Record the observed RED baseline**

Write the exact observed outcome and causes:

```markdown
# RED baseline: detailed but insufficient wonder

Input intent: generate six vast Chinese celestial-palace scenes with people and negative space.
Observed user verdict: 奇观感还是差了一些。

Failures:
- giant buildings lacked an impossible physical or spatial relationship;
- scale depended on adjectives instead of a four-level visual scale ladder;
- the six shots changed locations without a strong revelation curve;
- image prompts were detailed but motion prompts lacked an equally strict grammar.
```

- [x] **Step 2: Write the failing Skill contract test**

Create `tests/test_skill_contract.py` with `unittest`. It must assert that the Skill folder and all seven references exist, frontmatter contains only `name` and `description`, the description starts with `Use when`, `SKILL.md` routes the agent to the visual, wonder, image, video, shot and QA references, and the required terms `付费`, `一句话`, `status.json`, `单段` and `无遮挡` are present in the appropriate files.

```python
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "make-sky-palace-video"


class SkillContractTests(unittest.TestCase):
    def test_skill_and_required_references_exist(self):
        required = [
            "SKILL.md", "agents/openai.yaml", "references/visual-bible.md",
            "references/wonder-design.md", "references/image-prompts.md",
            "references/video-prompts.md", "references/shot-library.md",
            "references/quality-gates.md", "references/examples.md",
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
        for name in ["visual-bible.md", "wonder-design.md", "image-prompts.md",
                     "video-prompts.md", "shot-library.md", "quality-gates.md"]:
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
```

- [x] **Step 3: Run the test and verify RED**

Run:

```bash
python3 -m unittest tests.test_skill_contract -v
```

Expected: FAIL because `skills/make-sky-palace-video` does not exist.

## Task 2: Initialize the Skill and make the core contract pass

**Files:**
- Create: `skills/make-sky-palace-video/SKILL.md`
- Create: `skills/make-sky-palace-video/agents/openai.yaml`
- Create: `skills/make-sky-palace-video/references/*.md`
- Create: `skills/make-sky-palace-video/scripts/`

- [x] **Step 1: Run the official initializer**

Run:

```bash
python3 /Users/admin/.codex/skills/.system/skill-creator/scripts/init_skill.py make-sky-palace-video \
  --path skills \
  --resources scripts,references \
  --interface 'display_name=天宫奇观视频' \
  --interface 'short_description=一句话生成东方天宫奇观视频生产包' \
  --interface 'default_prompt=使用 $make-sky-palace-video，把我的一句话做成天宫奇观视频。'
```

Expected: the Skill directory, `SKILL.md`, `agents/openai.yaml`, `scripts/` and `references/` are created.

- [x] **Step 2: Replace template content with the minimal orchestration contract**

Use exactly two frontmatter keys:

```yaml
---
name: make-sky-palace-video
description: Use when a user wants to create Chinese celestial-palace spectacle imagery or image-to-video sequences from a short idea, including 天宫、仙境、云海、天门、神殿、天河、东方神话、巨物奇观 or cinematic pilgrimage requests.
---
```

The body must require: one-sentence parsing with defaults; an original world bible; one primary wonder per shot; a four-level scale ladder; image prompt generation; single-paragraph video prompt generation; cost confirmation; tool-aware execution; `status.json`; targeted regeneration; and honest fallback when generation tools are unavailable.

- [x] **Step 3: Add minimal reference files with their permanent scope**

Each reference initially contains its final H1 and a concise contract:

```text
visual-bible.md   → original architecture, material, character and continuity rules
wonder-design.md  → impossible relationship, four-level scale ladder, framing and reveal
image-prompts.md  → one-paragraph image prompt grammar and unobstructed action path
video-prompts.md  → one-paragraph motion grammar, parallax, continuity and anti-drift
shot-library.md   → shot archetypes and escalation sequence
quality-gates.md  → pass/fail checks and regeneration boundary
examples.md       → one complete production example
```

- [x] **Step 4: Run the contract test and verify GREEN**

Run:

```bash
python3 -m unittest tests.test_skill_contract -v
```

Expected: all Skill contract tests PASS.

- [x] **Step 5: Commit the core Skill contract**

```bash
git add skills tests/test_skill_contract.py tests/fixtures/baseline-v3-feedback.md
git commit -m "feat: add sky palace skill contract"
```

## Task 3: Build the project initializer with TDD

**Files:**
- Create: `tests/test_init_project.py`
- Create: `skills/make-sky-palace-video/scripts/init_project.py`

- [x] **Step 1: Write failing initializer tests**

Test that `main(["--output", tmp, "--slug", "moon-gate", "--prompt", prompt])` creates the exact production tree, writes a UTF-8 `brief.json` with schema version `1`, defaults to six shots, 30 seconds and `16:9`, initializes `status.json` at `briefed`, and refuses to overwrite a non-empty project directory unless `--force` is present.

```python
class InitProjectTests(unittest.TestCase):
    def test_creates_default_project_without_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.assertEqual(init_project.main([
                "--output", str(out), "--slug", "moon-gate",
                "--prompt", "巨月打开天门，两位同行者赴约",
            ]), 0)
            project = out / "moon-gate"
            brief = json.loads((project / "brief.json").read_text(encoding="utf-8"))
            self.assertEqual(brief["schema_version"], 1)
            self.assertEqual(brief["shot_count"], 6)
            self.assertEqual(brief["duration_seconds"], 30)
            self.assertEqual(brief["aspect_ratio"], "16:9")
            self.assertTrue((project / "prompts/image").is_dir())
            self.assertTrue((project / "prompts/video").is_dir())
            with self.assertRaises(FileExistsError):
                init_project.main([
                    "--output", str(out), "--slug", "moon-gate", "--prompt", "重复",
                ])
```

- [x] **Step 2: Run the initializer test and verify RED**

Run `python3 -m unittest tests.test_init_project -v`.

Expected: import or file-not-found failure because `init_project.py` is not implemented.

- [x] **Step 3: Implement the minimal initializer**

Implement `build_parser()`, `safe_slug()`, `create_project()` and `main(argv=None)` using only `argparse`, `json`, `pathlib`, `re` and `datetime`. Create `prompts/image`, `prompts/video`, `images`, `clips`; write `brief.json`, empty `world-bible.md`, `storyboard.md`, `qa-report.json` and `status.json`; never remove existing content.

- [x] **Step 4: Run the test and verify GREEN**

Run `python3 -m unittest tests.test_init_project -v`.

Expected: PASS with no warnings.

- [x] **Step 5: Commit**

```bash
git add skills/make-sky-palace-video/scripts/init_project.py tests/test_init_project.py
git commit -m "feat: add sky palace project initializer"
```

## Task 4: Build the package validator with TDD

**Files:**
- Create: `tests/test_validate_package.py`
- Create: `skills/make-sky-palace-video/scripts/validate_package.py`
- Create: `tests/fixtures/valid-package/`
- Create: `tests/fixtures/invalid-package/`

- [x] **Step 1: Write failing validator tests**

Create fixtures with two shots for fast tests. A valid fixture contains all required files, unique `primary_wonder` values, `impossible_relationship`, four `scale_ladder` items, positive percentages, continuous path text, one image prompt and one single-paragraph video prompt per shot. Invalid fixtures separately omit a scale ladder, duplicate a primary wonder, split a video prompt with blank lines, and omit paid-call status.

Test the public API:

```python
result = validate_package.validate(project_path)
self.assertTrue(result.ok)
self.assertEqual(result.errors, [])

bad = validate_package.validate(invalid_path)
self.assertFalse(bad.ok)
self.assertIn("scale_ladder", " ".join(bad.errors))
```

- [x] **Step 2: Run the validator test and verify RED**

Run `python3 -m unittest tests.test_validate_package -v`.

Expected: import or missing-function failure.

- [x] **Step 3: Implement the validator**

Use a `ValidationResult` dataclass. Validate required files, schema fields, shot count, sequential IDs, unique primary wonders, one impossible relationship, at least four scale references, `negative_space_percent` in `28..42`, `action_space_percent` in `22..32`, image prompt length at least 350 Chinese/Latin characters, video prompt length at least 260, no blank-line split in video prompts, and matching prompt file counts. Emit human-readable Chinese errors and optional JSON output from the CLI.

- [x] **Step 4: Run the validator test and verify GREEN**

Run `python3 -m unittest tests.test_validate_package -v`.

Expected: valid fixture passes and each invalid fixture fails for the intended reason.

- [x] **Step 5: Commit**

```bash
git add skills/make-sky-palace-video/scripts/validate_package.py tests/test_validate_package.py tests/fixtures
git commit -m "feat: validate sky palace production packages"
```

## Task 5: Expand the expert prompt system

**Files:**
- Modify: `skills/make-sky-palace-video/references/visual-bible.md`
- Modify: `skills/make-sky-palace-video/references/wonder-design.md`
- Modify: `skills/make-sky-palace-video/references/image-prompts.md`
- Modify: `skills/make-sky-palace-video/references/video-prompts.md`
- Modify: `skills/make-sky-palace-video/references/shot-library.md`
- Modify: `skills/make-sky-palace-video/references/quality-gates.md`
- Modify: `tests/test_skill_contract.py`

- [x] **Step 1: Strengthen tests before expanding references**

Add assertions for these observable requirements:

```text
wonder-design: impossible relationship, four-level scale ladder, off-frame continuation,
               foreground occlusion, active negative space, delayed reveal, escalation
image-prompts:  subject/world → core wonder → spatial layers → architecture → character →
                camera → composition percentages → lighting → palette/material → integrated failures
video-prompts:  locked first frame → camera path → character action → environment layers →
                parallax → reveal beat → end state → continuity/anti-drift in one paragraph
quality-gates:  score thresholds, blocking failures, targeted regeneration, no historic substitution
```

- [x] **Step 2: Run the strengthened contract test and verify RED**

Run `python3 -m unittest tests.test_skill_contract -v`.

Expected: FAIL on the new missing expert markers.

- [x] **Step 3: Write the final expert references**

Write concise tables for fast retrieval plus exact prompt assembly rules. Include measurable values, at least twelve original spectacle archetypes, three architecture families, character continuity templates, weather and light behavior, camera motion limits, common failure symptoms and exact corrections. Keep every reference directly linked from `SKILL.md`; do not create nested references.

- [x] **Step 4: Run the contract test and verify GREEN**

Run `python3 -m unittest tests.test_skill_contract -v`.

Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add skills/make-sky-palace-video/references tests/test_skill_contract.py
git commit -m "docs: add cinematic wonder prompt system"
```

## Task 6: Add one complete, high-detail production example

**Files:**
- Modify: `skills/make-sky-palace-video/references/examples.md`
- Modify: `tests/test_skill_contract.py`

- [x] **Step 1: Add failing example assertions**

Require one source sentence, one brief, one world bible, a six-row storyboard, six image prompts and six single-paragraph video prompts. Require the six primary wonders to be unique and require the sequence labels `召唤`, `仰望`, `进入`, `穿越`, `反转`, `抵达`.

- [x] **Step 2: Run and verify RED**

Run `python3 -m unittest tests.test_skill_contract -v`.

Expected: FAIL because the complete example is absent.

- [x] **Step 3: Write the complete example**

Use the input:

```text
巨月打开天门，两位旧友沿倒流天河赴九重天宫旧约，30秒横屏。
```

Design six escalating primary wonders: moon-sealed gate, inverted celestial river, mirror court beneath a suspended continent, mountain-scale colonnade piercing a cloud vortex, causeway crossing the inside of a moon, and a final gate revealing a palace wrapped around a sunrise star. Each image prompt must follow the exact grammar and each video prompt must be one paragraph with specific camera and layered motion.

- [x] **Step 4: Run and verify GREEN**

Run `python3 -m unittest tests.test_skill_contract -v`.

Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add skills/make-sky-palace-video/references/examples.md tests/test_skill_contract.py
git commit -m "docs: add complete sky palace production example"
```

## Task 7: Write repository installation and usage documentation

**Files:**
- Create: `tests/test_repository_docs.py`
- Create: `README.md`

- [x] **Step 1: Write failing README tests**

Require the README to contain repository scope, prerequisites, installer and manual-copy installation, `$make-sky-palace-video`, one-line invocation, four delivery modes, generated directory tree, supported tool behavior, paid-call confirmation, no automatic publishing, validation commands and troubleshooting.

- [x] **Step 2: Run and verify RED**

Run `python3 -m unittest tests.test_repository_docs -v`.

Expected: FAIL because `README.md` does not exist.

- [x] **Step 3: Write README.md**

Document both installation forms:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo renmu2017/SkyPalace \
  --path skills/make-sky-palace-video
```

and:

```bash
git clone https://github.com/renmu2017/SkyPalace.git
cp -R SkyPalace/skills/make-sky-palace-video ~/.codex/skills/
```

Explain that media providers are optional, credentials remain outside the repo, generated media can cost money, and the Skill stops at `video_prompts_ready` when no provider is callable.

- [x] **Step 4: Run and verify GREEN**

Run `python3 -m unittest tests.test_repository_docs -v`.

Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add README.md tests/test_repository_docs.py
git commit -m "docs: add sky palace skill usage guide"
```

## Task 8: Run official validation and realistic package checks

**Files:**
- Modify as failures require: `skills/make-sky-palace-video/**`, `README.md`, `tests/**`

- [x] **Step 1: Run all unit and contract tests**

```bash
python3 -m unittest discover -s tests -v
```

Expected: all tests PASS with no warnings.

- [x] **Step 2: Run official Skill validation with the bundled Python runtime**

```bash
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  /Users/admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/make-sky-palace-video
```

Expected: `Skill is valid!`

- [x] **Step 3: Exercise the initializer and validator in a temporary directory**

```bash
tmpdir="$(mktemp -d)"
python3 skills/make-sky-palace-video/scripts/init_project.py \
  --output "$tmpdir" --slug moon-gate \
  --prompt '巨月打开天门，两位同行者去赴九重天宫旧约，30秒横屏。'
python3 skills/make-sky-palace-video/scripts/validate_package.py "$tmpdir/moon-gate" --json
```

Expected: initializer succeeds; the unfilled package fails validation with explicit missing-storyboard and prompt errors rather than a traceback.

- [x] **Step 4: Validate the checked-in valid and invalid fixtures**

```bash
python3 skills/make-sky-palace-video/scripts/validate_package.py tests/fixtures/valid-package
python3 skills/make-sky-palace-video/scripts/validate_package.py tests/fixtures/invalid-package
```

Expected: valid exits `0`; invalid exits nonzero and lists the intended defects.

- [x] **Step 5: Run repository hygiene checks**

```bash
git diff --check
rg -n 'TB[D]|TO[D]O|PLACEHOLDER|your-api-key|sk-[A-Za-z0-9]' README.md skills tests
git status --short
```

Expected: no placeholders, secrets or AppleDouble files; only intended changes.

- [x] **Step 6: Commit validation fixes if any**

```bash
git add README.md skills tests docs/superpowers/plans/2026-08-12-sky-palace-video-skill.md
git commit -m "test: verify sky palace skill end to end"
```

## Task 9: Publish and verify GitHub

**Files:** None unless remote verification finds a repository issue.

- [ ] **Step 1: Inspect final history and diff**

```bash
git status --short
git log --oneline --decorate -8
git diff HEAD~1..HEAD --stat
```

Expected: clean worktree and focused commits.

- [ ] **Step 2: Push the authorized branch**

```bash
git push -u origin main
```

Expected: push succeeds to `https://github.com/renmu2017/SkyPalace.git`.

- [ ] **Step 3: Verify remote hash and public file tree**

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Expected: local and remote hashes match. Confirm the remote README and `skills/make-sky-palace-video/SKILL.md` are readable.

- [ ] **Step 4: Report exact verification**

Report repository URL, commit hash, tests, official Skill validation, installed path instructions, paid-call boundary and any untested media-provider behavior. Do not claim actual image or video generation unless a paid provider was explicitly authorized and observed.
