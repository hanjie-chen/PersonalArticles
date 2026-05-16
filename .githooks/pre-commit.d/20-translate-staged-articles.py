#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=True,
        text=True,
    )
    return Path(result.stdout.strip())


def load_translator(root_dir: Path):
    translator_dir = root_dir / ".kb-tools" / "translator"
    sys.path.insert(0, str(translator_dir))
    from workflow import (  # pylint: disable=import-outside-toplevel
        PartiallyStagedArticleError,
        find_staged_candidates,
        translate_candidate,
    )

    return PartiallyStagedArticleError, find_staged_candidates, translate_candidate


def git_add(root_dir: Path, path: Path) -> None:
    subprocess.run(
        ["git", "-C", str(root_dir), "add", "--", str(path.relative_to(root_dir))],
        check=True,
    )


def main() -> int:
    root_dir = repo_root()
    (
        partially_staged_error,
        find_staged_candidates,
        translate_candidate,
    ) = load_translator(root_dir)

    print("[pre-commit:translate] checking staged articles...")
    try:
        candidates = find_staged_candidates(root_dir, limit=None)
    except partially_staged_error as exc:
        print(f"[pre-commit:translate] {exc}", file=sys.stderr)
        print(
            "[pre-commit:translate] commit stopped; stage the article fully or "
            "commit unstaged edits separately",
            file=sys.stderr,
        )
        return 1

    if not candidates:
        print("[pre-commit:translate] ok: no staged articles need translation")
        return 0

    model = os.environ.get("KB_TRANSLATOR_MODEL")
    total = len(candidates)

    for index, candidate in enumerate(candidates, start=1):
        relative_source = candidate.source_md.relative_to(root_dir).as_posix()
        print(
            f"[pre-commit:translate] [{index}/{total}] "
            f"{candidate.status}\t{relative_source}"
        )
        translation_path = translate_candidate(
            repo_root=root_dir,
            candidate=candidate,
            model=model,
        )
        git_add(root_dir, translation_path)
        relative_translation = translation_path.relative_to(root_dir).as_posix()
        print(f"[pre-commit:translate] translated\t{relative_translation}")

    print("[pre-commit:translate] updated staging area after translating articles")
    print("[pre-commit:translate] commit stopped; please review changes and run git commit again")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
