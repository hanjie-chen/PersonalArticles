from __future__ import annotations

import argparse
from dataclasses import dataclass
from queue import Empty, Queue
import sys
from threading import Lock, Thread
from pathlib import Path

from workflow import default_repo_root, find_candidates, translate_candidate


SECTION_LINE = "=" * 48
SUBSECTION_LINE = "-" * 48


@dataclass(frozen=True)
class TranslationResult:
    index: int
    source_path: str
    translation_path: str | None
    error: str | None


def print_section(title: str) -> None:
    print(SECTION_LINE)
    print(title)
    print(SECTION_LINE)


def print_subsection(title: str) -> None:
    print(SUBSECTION_LINE)
    print(title)
    print(SUBSECTION_LINE)


def run_translation_jobs(
    *,
    repo_root: Path,
    indexed_candidates,
    worker_count: int,
    model: str | None,
) -> list[TranslationResult]:
    total = len(indexed_candidates)
    task_queue: Queue[tuple[int, object]] = Queue()
    for item in indexed_candidates:
        task_queue.put(item)

    print_lock = Lock()
    results_lock = Lock()
    results: list[TranslationResult] = []

    def log(message: str, *, stream=None) -> None:
        with print_lock:
            print(message, file=stream or sys.stdout)

    def worker(worker_id: int) -> None:
        while True:
            try:
                index, candidate = task_queue.get_nowait()
            except Empty:
                return

            relative_source = candidate.source_md.relative_to(repo_root).as_posix()
            log(f"worker-{worker_id} [{index}/{total}] translating\t{relative_source}")
            try:
                translation_path = translate_candidate(
                    repo_root=repo_root,
                    candidate=candidate,
                    model=model,
                )
            except Exception as exc:  # noqa: BLE001
                log(
                    f"worker-{worker_id} [{index}/{total}] failed\t{relative_source}\t{exc}",
                    stream=sys.stderr,
                )
                result = TranslationResult(
                    index=index,
                    source_path=relative_source,
                    translation_path=None,
                    error=str(exc),
                )
            else:
                relative_translation = translation_path.relative_to(repo_root).as_posix()
                log(
                    "worker-"
                    f"{worker_id} [{index}/{total}] translated\t{relative_source}\t{relative_translation}"
                )
                result = TranslationResult(
                    index=index,
                    source_path=relative_source,
                    translation_path=relative_translation,
                    error=None,
                )

            with results_lock:
                results.append(result)
            task_queue.task_done()

    threads = [
        Thread(target=worker, args=(worker_id,), daemon=True)
        for worker_id in range(1, worker_count + 1)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return sorted(results, key=lambda item: item.index)


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
        print("Found 0 candidate(s)")
        return 0

    print_section(f"Found {total} candidate(s)")
    indexed_candidates = list(enumerate(candidates, start=1))
    for index, candidate in indexed_candidates:
        relative_source = candidate.source_md.relative_to(repo_root).as_posix()
        print(f"[{index}] {candidate.status}\t{relative_source}")

    worker_count = min(max(args.jobs, 1), total)
    print_subsection(f"Starting {worker_count} worker(s)")
    results = run_translation_jobs(
        repo_root=repo_root,
        indexed_candidates=indexed_candidates,
        worker_count=worker_count,
        model=args.model,
    )

    success_count = sum(1 for result in results if result.error is None)
    failure_count = len(results) - success_count
    print_subsection("Finished")
    print(f"success: {success_count}")
    print(f"failed: {failure_count}")
    exit_code = 1 if failure_count else 0
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
