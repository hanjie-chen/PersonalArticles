import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPO_ROOT / ".kb-tools" / "translator" / "list-candidates.py"


def run_git(args, cwd):
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


class ListTranslationCandidatesTest(unittest.TestCase):
    def init_repo(self, repo_root: Path) -> None:
        run_git(["init"], cwd=repo_root)
        run_git(["config", "user.name", "Codex"], cwd=repo_root)
        run_git(["config", "user.email", "codex@example.com"], cwd=repo_root)

    def write_publishable_article(self, article_dir: Path, md_name: str = "article.md") -> Path:
        resources_images = article_dir / "resources" / "images"
        resources_images.mkdir(parents=True)
        (resources_images / "cover.png").write_bytes(b"png")
        article_path = article_dir / md_name
        article_path.write_text(
            textwrap.dedent(
                """\
                ---
                Title: Example
                Author: Tester
                CoverImage: ./resources/images/cover.png
                RolloutDate: 2026-04-17
                ---

                ```
                BriefIntroduction: Example intro
                ```

                <!-- split -->

                ![cover](./resources/images/cover.png)
                """
            ),
            encoding="utf-8",
        )
        return article_path

    def source_blob(self, repo_root: Path, source_path: Path) -> str:
        result = run_git(
            ["-C", str(repo_root), "hash-object", str(source_path)],
            cwd=repo_root,
        )
        return result.stdout.strip()

    def test_lists_missing_translation_for_publishable_article(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.init_repo(repo_root)
            article_path = self.write_publishable_article(repo_root / "topic")

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(repo_root)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                result.stdout.strip(),
                f"missing_translation\t{article_path.relative_to(repo_root).as_posix()}",
            )

    def test_lists_outdated_translation_when_source_blob_differs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.init_repo(repo_root)
            article_dir = repo_root / "topic"
            article_path = self.write_publishable_article(article_dir, "basic.md")
            translation_dir = article_dir / "resources" / "i18n"
            translation_dir.mkdir(parents=True)
            (translation_dir / "basic-en.md").write_text(
                textwrap.dedent(
                    """\
                    <!-- source_blob: old-blob -->

                    # English
                    """
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(repo_root)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                result.stdout.strip(),
                f"outdated_translation\t{article_path.relative_to(repo_root).as_posix()}",
            )

    def test_skips_translation_when_source_blob_matches(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.init_repo(repo_root)
            article_dir = repo_root / "topic"
            article_path = self.write_publishable_article(article_dir, "basic.md")
            current_blob = self.source_blob(repo_root, article_path)
            translation_dir = article_dir / "resources" / "i18n"
            translation_dir.mkdir(parents=True)
            (translation_dir / "basic-en.md").write_text(
                textwrap.dedent(
                    f"""\
                    <!-- source_blob: {current_blob} -->

                    # English
                    """
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(repo_root)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "")

    def test_respects_default_limit_of_one(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self.init_repo(repo_root)
            first = self.write_publishable_article(repo_root / "alpha", "first.md")
            self.write_publishable_article(repo_root / "beta", "second.md")

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(repo_root)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                result.stdout.strip(),
                f"missing_translation\t{first.relative_to(repo_root).as_posix()}",
            )


if __name__ == "__main__":
    unittest.main()

