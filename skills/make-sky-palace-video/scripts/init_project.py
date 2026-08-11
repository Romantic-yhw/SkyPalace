#!/usr/bin/env python3
"""Create a safe, isolated SkyPalace production package."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Sequence


def safe_slug(value: str) -> str:
    """Return a filesystem-safe slug while preserving useful CJK characters."""
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^0-9a-z\u3400-\u9fff-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value or value in {".", ".."}:
        raise ValueError("slug 不能是空值或路径符号")
    return value[:80].rstrip("-")


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def create_project(
    output: Path,
    slug: str,
    source_prompt: str,
    *,
    duration_seconds: int = 30,
    shot_count: int = 6,
    aspect_ratio: str = "16:9",
    force: bool = False,
) -> Path:
    if not source_prompt.strip():
        raise ValueError("prompt 不能为空")
    if duration_seconds < 4 or duration_seconds > 300:
        raise ValueError("duration 必须在 4 到 300 秒之间")
    if shot_count < 1 or shot_count > 20:
        raise ValueError("shots 必须在 1 到 20 之间")
    if aspect_ratio not in {"16:9", "9:16", "1:1", "4:3", "3:4"}:
        raise ValueError("不支持的画幅比例")

    project = output.expanduser().resolve() / safe_slug(slug)
    if project.exists() and any(project.iterdir()) and not force:
        raise FileExistsError(f"项目目录已存在且非空：{project}")

    project.mkdir(parents=True, exist_ok=True)
    for relative in ("prompts/image", "prompts/video", "images", "clips"):
        (project / relative).mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(timezone.utc).isoformat()
    brief = {
        "schema_version": 1,
        "source_prompt": source_prompt.strip(),
        "title": slug.strip(),
        "duration_seconds": duration_seconds,
        "shot_count": shot_count,
        "aspect_ratio": aspect_ratio,
        "delivery_mode": "auto",
        "style": "电影级超写实东方神话史诗",
        "assumptions": [],
        "created_at": created_at,
    }
    status = {
        "schema_version": 1,
        "stage": "briefed",
        "blocked_reason": None,
        "paid_generation_authorized": False,
        "completed_shots": [],
        "failed_shots": [],
        "updated_at": created_at,
    }
    qa_report = {
        "schema_version": 1,
        "passed": False,
        "errors": ["尚未生成分镜和提示词"],
        "warnings": [],
        "shots": [],
    }

    write_json(project / "brief.json", brief)
    write_json(project / "status.json", status)
    write_json(project / "qa-report.json", qa_report)
    (project / "world-bible.md").write_text(
        "# 世界观圣经\n\n## 建筑与材料\n\n## 人物连续性\n\n## 光线与色彩\n\n## 空间连续性\n",
        encoding="utf-8",
    )
    (project / "storyboard.md").write_text(
        "# 分镜表\n\n生成分镜后，为每镜记录主奇观、不可能关系、四级尺度链、构图、动作和时长。\n",
        encoding="utf-8",
    )
    return project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="初始化天宫奇观视频生产包")
    parser.add_argument("--output", required=True, type=Path, help="项目父目录")
    parser.add_argument("--slug", required=True, help="项目短名称")
    parser.add_argument("--prompt", required=True, help="用户的一句话创意")
    parser.add_argument("--duration", type=int, default=30, help="总时长，默认 30 秒")
    parser.add_argument("--shots", type=int, default=6, help="镜头数，默认 6")
    parser.add_argument("--aspect-ratio", default="16:9", help="画幅，默认 16:9")
    parser.add_argument("--force", action="store_true", help="允许写入已存在目录，但不删除其他文件")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project = create_project(
        args.output,
        args.slug,
        args.prompt,
        duration_seconds=args.duration,
        shot_count=args.shots,
        aspect_ratio=args.aspect_ratio,
        force=args.force,
    )
    print(project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
