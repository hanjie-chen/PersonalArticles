from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from pathlib import Path

from workflow import default_repo_root, find_candidates, translate_candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Translate knowledge-base articles into resources/i18n English variants."
    )
    parser.add_argument("root_dir", nargs="?", default=None, help="Repository root directory")
    parser.add_argument("--limit", type=int, default=1, help="Maximum number of candidates to translate")
    parser.add_argument(
        "--jobs",
        type=int,
        default=2,
        help="Maximum number of Codex translation processes to run in parallel",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Optional Codex model name. Omit to let Codex choose the account default.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = (
        Path(args.root_dir).resolve() if args.root_dir else default_repo_root(Path(__file__))
    )
    candidates = find_candidates(repo_root, max(args.limit, 0))
    total = len(candidates)

    if total == 0:
        print("found 0 candidate(s)")
        return 0

    print(f"found {total} candidate(s)")
    indexed_candidates = list(enumerate(candidates, start=1))
    for index, candidate in indexed_candidates:
        relative_source = candidate.source_md.relative_to(repo_root).as_posix()
        print(f"[{index}] {candidate.status}\t{relative_source}")

    worker_count = min(max(args.jobs, 1), total)
    print(f"starting {worker_count} worker(s)")

    exit_code = 0
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_map = {}
        for index, candidate in indexed_candidates:
            relative_source = candidate.source_md.relative_to(repo_root).as_posix()
            print(f"[{index}/{total}] translating\t{relative_source}")
            future = executor.submit(
                translate_candidate,
                repo_root=repo_root,
                candidate=candidate,
                model=args.model,
            )
            future_map[future] = (index, candidate)

        for future in as_completed(future_map):
            index, candidate = future_map[future]
            relative_source = candidate.source_md.relative_to(repo_root).as_posix()
            try:
                translation_path = future.result()
            except Exception as exc:  # noqa: BLE001
                print(f"[{index}/{total}] failed\t{relative_source}\t{exc}", file=sys.stderr)
                exit_code = 1
                continue

            relative_translation = translation_path.relative_to(repo_root).as_posix()
            print(
                f"[{index}/{total}] translated\t{relative_source}\t{relative_translation}"
            )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
