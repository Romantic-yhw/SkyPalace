#!/usr/bin/env python3
"""Validate structure and quality signals in a SkyPalace production package."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Sequence


VALID_STAGES = {
    "briefed",
    "storyboard_ready",
    "image_prompts_ready",
    "images_ready",
    "video_prompts_ready",
    "clips_ready",
    "ready_for_edit",
    "complete",
    "blocked",
}


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {"ok": self.ok, "errors": self.errors, "warnings": self.warnings}


def load_json(path: Path, result: ValidationResult) -> dict[str, object] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.errors.append(f"缺少必需文件：{path.name}")
        return None
    except json.JSONDecodeError as exc:
        result.errors.append(f"{path.name} 不是合法 JSON：{exc.msg}")
        return None
    if not isinstance(payload, dict):
        result.errors.append(f"{path.name} 顶层必须是对象")
        return None
    return payload


def compact_length(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def validate_prompt_files(
    project: Path,
    shot_count: int,
    kind: str,
    minimum_length: int,
    result: ValidationResult,
) -> None:
    prompt_dir = project / "prompts" / kind
    if not prompt_dir.is_dir():
        result.errors.append(f"缺少提示词目录：prompts/{kind}")
        return

    files = sorted(
        path for path in prompt_dir.glob("*.txt") if not path.name.startswith("._")
    )
    if len(files) != shot_count:
        result.errors.append(
            f"prompts/{kind} 文件数量应为 {shot_count}，实际为 {len(files)}"
        )

    for index in range(1, shot_count + 1):
        expected = prompt_dir / f"{index:02d}.txt"
        if not expected.is_file():
            result.errors.append(f"缺少提示词：prompts/{kind}/{index:02d}.txt")
            continue
        text = expected.read_text(encoding="utf-8").strip()
        if compact_length(text) < minimum_length:
            result.errors.append(
                f"prompts/{kind}/{index:02d}.txt 过短，至少需要 {minimum_length} 个非空白字符"
            )
        if kind == "video" and re.search(r"\n\s*\n", text):
            result.errors.append(
                f"prompts/video/{index:02d}.txt 必须是无空行的单段提示词"
            )


def validate_shots(brief: dict[str, object], result: ValidationResult) -> int:
    shot_count = brief.get("shot_count")
    if not isinstance(shot_count, int) or not 1 <= shot_count <= 20:
        result.errors.append("brief.json 的 shot_count 必须是 1 到 20 的整数")
        return 0

    shots = brief.get("shots")
    if not isinstance(shots, list) or len(shots) != shot_count:
        actual = len(shots) if isinstance(shots, list) else 0
        result.errors.append(
            f"brief.json 的 shots 数量应为 {shot_count}，实际为 {actual}"
        )
        return shot_count

    wonders: list[str] = []
    for index, shot in enumerate(shots, start=1):
        prefix = f"shots[{index - 1}]"
        if not isinstance(shot, dict):
            result.errors.append(f"{prefix} 必须是对象")
            continue
        expected_id = f"{index:02d}"
        if shot.get("id") != expected_id:
            result.errors.append(f"{prefix}.id 必须是 {expected_id}")

        primary = shot.get("primary_wonder")
        if not isinstance(primary, str) or not primary.strip():
            result.errors.append(f"{prefix}.primary_wonder 不能为空")
        else:
            wonders.append(primary.strip())

        impossible = shot.get("impossible_relationship")
        if not isinstance(impossible, str) or len(impossible.strip()) < 8:
            result.errors.append(
                f"{prefix}.impossible_relationship 必须明确描述不可能关系"
            )

        scale = shot.get("scale_ladder")
        if not isinstance(scale, list) or len(scale) < 4 or len(set(map(str, scale))) < 4:
            result.errors.append(
                f"{prefix}.scale_ladder 必须包含至少四个不同层级"
            )

        character_mode = shot.get("character_mode")
        character_height = shot.get("character_height_percent")
        if character_mode == "none":
            if character_height not in {None, 0, 0.0}:
                result.errors.append(
                    f"{prefix}.character_height_percent 在无人镜头中必须是 0 或 null"
                )
        elif character_mode == "tiny":
            if not isinstance(character_height, (int, float)) or not 0.25 <= character_height <= 0.8:
                result.errors.append(
                    f"{prefix}.character_height_percent 必须在 0.25 到 0.8 之间"
                )
        else:
            result.errors.append(f"{prefix}.character_mode 必须是 tiny 或 none")

        colossus = shot.get("colossus_percent")
        if not isinstance(colossus, (int, float)) or not 45 <= colossus <= 65:
            result.errors.append(
                f"{prefix}.colossus_percent 必须在 45 到 65 之间"
            )

        negative = shot.get("negative_space_percent")
        if not isinstance(negative, (int, float)) or not 28 <= negative <= 42:
            result.errors.append(
                f"{prefix}.negative_space_percent 必须在 28 到 42 之间"
            )

        action = shot.get("action_space_percent")
        if not isinstance(action, (int, float)) or not 22 <= action <= 32:
            result.errors.append(
                f"{prefix}.action_space_percent 必须在 22 到 32 之间"
            )

    if len(set(wonders)) != len(wonders):
        result.errors.append("所有 shots[].primary_wonder 必须互不重复")
    return shot_count


def validate(project: Path | str) -> ValidationResult:
    project = Path(project).expanduser().resolve()
    result = ValidationResult()
    if not project.is_dir():
        result.errors.append(f"项目目录不存在：{project}")
        return result

    brief = load_json(project / "brief.json", result)
    status = load_json(project / "status.json", result)
    load_json(project / "qa-report.json", result)

    for name in ("world-bible.md", "storyboard.md"):
        path = project / name
        if not path.is_file():
            result.errors.append(f"缺少必需文件：{name}")
        elif compact_length(path.read_text(encoding="utf-8")) < 20:
            result.errors.append(f"{name} 内容过短")

    shot_count = validate_shots(brief, result) if brief else 0
    if brief and brief.get("schema_version") != 1:
        result.errors.append("brief.json.schema_version 必须是 1")

    if status:
        if "paid_generation_authorized" not in status:
            result.errors.append("status.json 缺少 paid_generation_authorized")
        elif not isinstance(status["paid_generation_authorized"], bool):
            result.errors.append("status.json.paid_generation_authorized 必须是布尔值")
        stage = status.get("stage")
        if stage not in VALID_STAGES:
            result.errors.append(f"status.json.stage 无效：{stage}")

    if shot_count:
        validate_prompt_files(project, shot_count, "image", 350, result)
        validate_prompt_files(project, shot_count, "video", 260, result)

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验天宫奇观视频生产包")
    parser.add_argument("project", type=Path, help="生产包目录")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate(args.project)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    elif result.ok:
        print("PASS：生产包通过校验")
        for warning in result.warnings:
            print(f"WARN：{warning}")
    else:
        print("FAIL：生产包未通过校验")
        for error in result.errors:
            print(f"- {error}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
