#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
from pathlib import Path


REVIEW_NEEDED = 2


def log(status: str, message: str, *, stream=None, detail: bool = False, last: bool = False) -> None:
    if detail:
        prefix_name = "GITHOOK_LOG_DETAIL_PREFIX"
    else:
        prefix_name = "GITHOOK_LOG_LAST_PREFIX" if last else "GITHOOK_LOG_ITEM_PREFIX"
    prefix = os.environ.get(prefix_name, "")
    label = "" if detail else "translate: "
    print(f"{prefix}[{status}] {label}{message}", file=stream or sys.stdout, flush=True)


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
    )
    from translate import run_translation_jobs  # pylint: disable=import-outside-toplevel

    return PartiallyStagedArticleError, find_staged_candidates, run_translation_jobs


def git_add(root_dir: Path, path: Path) -> None:
    subprocess.run(
        ["git", "-C", str(root_dir), "add", "--", str(path.relative_to(root_dir))],
        check=True,
    )


def worker_count_for(total: int) -> int:
    configured = os.environ.get("KB_TRANSLATOR_JOBS")
    if not configured:
        return total

    try:
        return min(max(int(configured), 1), total)
    except ValueError:
        log("warn", f"ignoring invalid KB_TRANSLATOR_JOBS={configured!r}", stream=sys.stderr)
        return total


def main() -> int:
    root_dir = repo_root()
    (
        partially_staged_error,
        find_staged_candidates,
        run_translation_jobs,
    ) = load_translator(root_dir)

    try:
        candidates = find_staged_candidates(root_dir, limit=None)
    except partially_staged_error as exc:
        log("fail", str(exc), stream=sys.stderr)
        log("fail", "stage the article fully or commit unstaged edits separately", stream=sys.stderr, last=True)
        return 1

    if not candidates:
        log("ok", "no staged articles need translation", last=True)
        return 0

    model = os.environ.get("KB_TRANSLATOR_MODEL")
    total = len(candidates)
    indexed_candidates = list(enumerate(candidates, start=1))

    log("run", f"{total} staged article(s) need translation")
    for index, candidate in indexed_candidates:
        relative_source = candidate.source_md.relative_to(root_dir).as_posix()
        log("job", f"[{index}/{total}] {candidate.status} {relative_source}", detail=True)

    worker_count = worker_count_for(total)
    log("run", f"starting {worker_count} worker(s)")
    results = run_translation_jobs(
        repo_root=root_dir,
        indexed_candidates=indexed_candidates,
        worker_count=worker_count,
        model=model,
        log_prefix=f"{os.environ.get('GITHOOK_LOG_DETAIL_PREFIX', '')}[job] ",
    )

    success_count = 0
    failure_count = 0
    for result in results:
        if result.error or not result.translation_path:
            failure_count += 1
            continue
        success_count += 1
        git_add(root_dir, root_dir / result.translation_path)

    if failure_count:
        log("fail", f"translated {success_count}, failed {failure_count}", stream=sys.stderr)
        log("fail", "review errors and run git commit again", stream=sys.stderr, last=True)
        return 1

    log("add", "staged generated translations", last=True)
    return REVIEW_NEEDED


if __name__ == "__main__":
    raise SystemExit(main())
