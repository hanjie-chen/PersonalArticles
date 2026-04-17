import argparse
from pathlib import Path

from workflow import default_repo_root, find_candidates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List translation candidates for the knowledge base."
    )
    parser.add_argument("root_dir", nargs="?", default=None, help="Repository root directory")
    parser.add_argument("--limit", type=int, default=1, help="Maximum number of candidates to print")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root_dir = (
        Path(args.root_dir).resolve() if args.root_dir else default_repo_root(Path(__file__))
    )
    for candidate in find_candidates(root_dir, max(args.limit, 0)):
        relative_path = candidate.source_md.relative_to(root_dir).as_posix()
        print(f"{candidate.status}\t{relative_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

