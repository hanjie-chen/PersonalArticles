#!/usr/bin/env python3

import argparse
from pathlib import PurePosixPath


def is_publish_affecting(path_str: str) -> bool:
    path = PurePosixPath(path_str.lstrip("./"))
    normalized = path.as_posix()

    if not normalized:
        return False

    if normalized.startswith((".githooks/", ".kb-tools/", "__template__/")):
        return False

    if any(part.startswith(".") for part in path.parts):
        return False

    if path.name in {"README.md", "AGENTS.md"}:
        return False

    if path.suffix.lower() == ".md":
        return True

    parts = path.parts
    if "resources" in parts:
        resource_index = parts.index("resources")
        if resource_index + 1 < len(parts) and parts[resource_index + 1] in {
            "images",
            "i18n",
        }:
            return True

    return "images" in parts or "assets" in parts


def read_changed_paths(changed_file: str) -> list[str]:
    with open(changed_file, "r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def build_outputs(changed_paths: list[str]) -> dict[str, str]:
    matched = [path for path in changed_paths if is_publish_affecting(path)]
    outputs = {
        "should_trigger": "true" if matched else "false",
        "matched_count": str(len(matched)),
    }
    if matched:
        summary = ", ".join(matched[:10])
        if len(matched) > 10:
            summary += ", ..."
        outputs["matched_summary"] = summary
    return outputs


def write_github_outputs(github_output: str, outputs: dict[str, str]) -> None:
    with open(github_output, "a", encoding="utf-8") as handle:
        for key, value in outputs.items():
            handle.write(f"{key}={value}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect whether changed files affect website-published content."
    )
    parser.add_argument("--changed-file", required=True)
    parser.add_argument("--github-output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    changed_paths = read_changed_paths(args.changed_file)
    outputs = build_outputs(changed_paths)
    write_github_outputs(args.github_output, outputs)


if __name__ == "__main__":
    main()
