from __future__ import annotations

import argparse
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

    exit_code = 0
    for candidate in candidates:
        relative_source = candidate.source_md.relative_to(repo_root).as_posix()
        try:
            translation_path = translate_candidate(
                repo_root=repo_root,
                candidate=candidate,
                model=args.model,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"failed\t{relative_source}\t{exc}", file=sys.stderr)
            exit_code = 1
            continue

        relative_translation = translation_path.relative_to(repo_root).as_posix()
        print(f"translated\t{relative_source}\t{relative_translation}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

