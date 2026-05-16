import argparse
from pathlib import Path

from workflow import default_repo_root, find_candidates, find_staged_candidates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List translation candidates for the knowledge base."
    )
    parser.add_argument("root_dir", nargs="?", default=None, help="Repository root directory")
    parser.add_argument("--limit", type=int, default=1, help="Maximum number of candidates to print")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Print every candidate instead of applying --limit",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Only list candidates for staged source articles",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="List every publishable article candidate even if SourceBlob already matches",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root_dir = (
        Path(args.root_dir).resolve() if args.root_dir else default_repo_root(Path(__file__))
    )
    limit = None if args.all else max(args.limit, 0)
    finder = find_staged_candidates if args.staged else find_candidates
    candidates = finder(root_dir, limit, force=args.force)
    print(f"Found {len(candidates)} candidate(s)")
    for index, candidate in enumerate(candidates, start=1):
        relative_path = candidate.source_md.relative_to(root_dir).as_posix()
        print(f"[{index}] {candidate.status}\t{relative_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
