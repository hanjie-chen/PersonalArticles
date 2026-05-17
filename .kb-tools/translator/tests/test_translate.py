import importlib.util
import io
import subprocess
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "workflow.py"
CLI_PATH = Path(__file__).resolve().parents[1] / "translate.py"
SPEC = importlib.util.spec_from_file_location("workflow", MODULE_PATH)
kb_translation = importlib.util.module_from_spec(SPEC)
sys.modules["workflow"] = kb_translation
assert SPEC.loader is not None
SPEC.loader.exec_module(kb_translation)
CLI_SPEC = importlib.util.spec_from_file_location("translate_cli", CLI_PATH)
translate_cli = importlib.util.module_from_spec(CLI_SPEC)
sys.modules["translate_cli"] = translate_cli
assert CLI_SPEC.loader is not None
CLI_SPEC.loader.exec_module(translate_cli)


def run_git(args, cwd):
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


def init_repo(repo_root: Path) -> None:
    run_git(["init"], cwd=repo_root)
    run_git(["config", "user.name", "Codex"], cwd=repo_root)
    run_git(["config", "user.email", "codex@example.com"], cwd=repo_root)


class TranslateArticlesTest(unittest.TestCase):
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

                # 中文标题

                正文段落。

                ```python
                print("hello")
                ```
                """
            ),
            encoding="utf-8",
        )
        return article_path

    def test_translate_candidate_writes_translation_with_source_blob(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            article_path = self.write_publishable_article(repo_root / "topic", "basic.md")
            candidate = kb_translation.Candidate(
                source_md=article_path,
                status="missing_translation",
            )

            with mock.patch.object(
                kb_translation,
                "compute_source_blob",
                return_value="a" * 40,
            ), mock.patch.object(
                kb_translation,
                "request_translation",
                return_value=textwrap.dedent(
                    """\
                    ---
                    Title: English title
                    ---

                    ```
                    BriefIntroduction: English intro
                    ```

                    <!-- split -->

                    # English title

                    English body.
                    """
                ),
            ):
                translation_path = kb_translation.translate_candidate(
                    repo_root=repo_root,
                    candidate=candidate,
                    model="test-model",
                )

            self.assertEqual(
                translation_path,
                article_path.parent / "resources" / "i18n" / "basic-en.md",
            )
            content = translation_path.read_text(encoding="utf-8")
            self.assertIn("---\nTitle: English title\nSourceBlob: " + ("a" * 40), content)
            self.assertIn("BriefIntroduction: English intro", content)
            self.assertIn("<!-- split -->", content)
            self.assertIn("# English title", content)
            self.assertIn("English body.", content)

    def test_translate_candidate_drops_leading_cover_image_line(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            article_path = self.write_publishable_article(repo_root / "topic", "basic.md")
            candidate = kb_translation.Candidate(
                source_md=article_path,
                status="missing_translation",
            )

            translated_markdown = textwrap.dedent(
                """\
                ---
                Title: English title
                ---

                ```
                BriefIntroduction: English intro
                ```

                <!-- split -->

                <img src="./resources/images/cover.png" alt="cover" style="zoom: 67%;" />

                # English title

                English body.
                """
            )

            with mock.patch.object(
                kb_translation,
                "compute_source_blob",
                return_value="c" * 40,
            ), mock.patch.object(
                kb_translation,
                "request_translation",
                return_value=translated_markdown,
            ):
                translation_path = kb_translation.translate_candidate(
                    repo_root=repo_root,
                    candidate=candidate,
                    model="test-model",
                )

            content = translation_path.read_text(encoding="utf-8")
            self.assertNotIn('<img src="./resources/images/cover.png"', content)
            self.assertIn("BriefIntroduction: English intro", content)
            self.assertIn("# English title", content)
            self.assertIn("English body.", content)

    def test_translate_candidate_preserves_existing_translation_on_failure(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            article_path = self.write_publishable_article(repo_root / "topic", "basic.md")
            translation_path = article_path.parent / "resources" / "i18n" / "basic-en.md"
            translation_path.parent.mkdir(parents=True, exist_ok=True)
            original = "<!-- source_blob: old -->\n\n# Existing\n"
            translation_path.write_text(original, encoding="utf-8")
            candidate = kb_translation.Candidate(
                source_md=article_path,
                status="outdated_translation",
            )

            with mock.patch.object(
                kb_translation,
                "compute_source_blob",
                return_value="b" * 40,
            ), mock.patch.object(
                kb_translation,
                "request_translation",
                side_effect=RuntimeError("translation failed"),
            ):
                with self.assertRaises(RuntimeError):
                    kb_translation.translate_candidate(
                        repo_root=repo_root,
                        candidate=candidate,
                        model="test-model",
                    )

            self.assertEqual(translation_path.read_text(encoding="utf-8"), original)

    def test_cli_exits_cleanly_when_no_candidates_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            result = subprocess.run(
                [sys.executable, str(CLI_PATH), str(repo_root)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "Found 0 candidate(s)")

    def test_build_parser_accepts_jobs_option(self):
        parser = translate_cli.build_parser()
        args = parser.parse_args(["--limit", "5", "--jobs", "2"])
        self.assertEqual(args.limit, 5)
        self.assertEqual(args.jobs, 2)

    def test_build_parser_accepts_force_option(self):
        parser = translate_cli.build_parser()
        args = parser.parse_args(["--force"])
        self.assertTrue(args.force)

    def test_build_parser_accepts_staged_and_all_options(self):
        parser = translate_cli.build_parser()
        args = parser.parse_args(["--staged", "--all"])
        self.assertTrue(args.staged)
        self.assertTrue(args.all)

    def test_build_parser_defaults_jobs_to_two(self):
        parser = translate_cli.build_parser()
        args = parser.parse_args([])
        self.assertEqual(args.jobs, 2)

    def test_main_prints_candidate_list_and_progress_summary(self):
        repo_root = Path("/tmp/repo").resolve()
        candidates = [
            kb_translation.Candidate(
                source_md=repo_root / "topic" / "first.md",
                status="missing_translation",
            ),
            kb_translation.Candidate(
                source_md=repo_root / "topic" / "second.md",
                status="outdated_translation",
            ),
        ]

        with mock.patch.object(
            translate_cli, "build_parser"
        ) as build_parser, mock.patch.object(
            translate_cli, "find_candidates", return_value=candidates
        ), mock.patch.object(
            translate_cli,
            "translate_candidate",
            side_effect=[
                repo_root / "topic" / "resources" / "i18n" / "first-en.md",
                repo_root / "topic" / "resources" / "i18n" / "second-en.md",
            ],
        ):
            build_parser.return_value.parse_args.return_value = mock.Mock(
                root_dir=str(repo_root),
                limit=5,
                all=False,
                staged=False,
                model=None,
                jobs=2,
                force=False,
            )
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = translate_cli.main()

        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Found 2 candidate(s)", output)
        self.assertIn("[1] missing_translation\ttopic/first.md", output)
        self.assertIn("[2] outdated_translation\ttopic/second.md", output)
        self.assertIn("Starting 2 worker(s)", output)
        self.assertIn("worker-", output)
        self.assertIn("[1/2] translating\ttopic/first.md", output)
        self.assertIn("[2/2] translating\ttopic/second.md", output)
        self.assertIn("Finished", output)
        self.assertIn("success: 2", output)

    def test_main_passes_force_to_candidate_finder(self):
        repo_root = Path("/tmp/repo").resolve()
        with mock.patch.object(
            translate_cli, "build_parser"
        ) as build_parser, mock.patch.object(
            translate_cli, "find_candidates", return_value=[]
        ) as find_candidates:
            build_parser.return_value.parse_args.return_value = mock.Mock(
                root_dir=str(repo_root),
                limit=5,
                all=False,
                staged=False,
                model=None,
                jobs=2,
                force=True,
            )
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = translate_cli.main()

        self.assertEqual(exit_code, 0)
        find_candidates.assert_called_once_with(repo_root, 5, force=True)
        self.assertIn("Found 0 candidate(s)", stdout.getvalue())

    def test_find_staged_candidates_only_checks_staged_source_articles(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            init_repo(repo_root)
            staged_article = self.write_publishable_article(repo_root / "staged", "basic.md")
            self.write_publishable_article(repo_root / "unstaged", "draft.md")
            run_git(["add", str(staged_article.relative_to(repo_root))], cwd=repo_root)

            candidates = kb_translation.find_staged_candidates(repo_root, limit=None)

            self.assertEqual(candidates, [
                kb_translation.Candidate(
                    source_md=staged_article,
                    status="missing_translation",
                )
            ])

    def test_find_staged_candidates_rejects_partially_staged_articles(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            init_repo(repo_root)
            article_path = self.write_publishable_article(repo_root / "topic", "basic.md")
            run_git(["add", "."], cwd=repo_root)
            run_git(["commit", "-m", "initial"], cwd=repo_root)

            with article_path.open("a", encoding="utf-8") as article:
                article.write("\nStaged paragraph.\n")
            run_git(["add", str(article_path.relative_to(repo_root))], cwd=repo_root)
            with article_path.open("a", encoding="utf-8") as article:
                article.write("\nUnstaged paragraph.\n")

            with self.assertRaises(kb_translation.PartiallyStagedArticleError):
                kb_translation.find_staged_candidates(repo_root, limit=None)

    def test_move_staged_translation_sidecars_follows_article_rename(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            init_repo(repo_root)
            article_path = self.write_publishable_article(repo_root / "topic", "basic.md")
            current_blob = run_git(["hash-object", str(article_path)], cwd=repo_root).stdout.strip()
            translation_path = article_path.parent / "resources" / "i18n" / "basic-en.md"
            translation_path.parent.mkdir(parents=True)
            translation_path.write_text(
                textwrap.dedent(
                    f"""\
                    ---
                    Title: English title
                    SourceBlob: {current_blob}
                    ---

                    ```
                    BriefIntroduction: English intro
                    ```

                    <!-- split -->

                    # English title
                    """
                ),
                encoding="utf-8",
            )
            run_git(["add", "."], cwd=repo_root)
            run_git(["commit", "-m", "initial"], cwd=repo_root)

            renamed_article = article_path.with_name("renamed.md")
            run_git(
                [
                    "mv",
                    str(article_path.relative_to(repo_root)),
                    str(renamed_article.relative_to(repo_root)),
                ],
                cwd=repo_root,
            )

            moved = kb_translation.move_staged_translation_sidecars(repo_root)

            renamed_translation = renamed_article.parent / "resources" / "i18n" / "renamed-en.md"
            self.assertEqual(
                moved,
                [
                    kb_translation.TranslationSidecarMove(
                        old_path=translation_path,
                        new_path=renamed_translation,
                    )
                ],
            )
            self.assertFalse(translation_path.exists())
            self.assertTrue(renamed_translation.exists())
            status = run_git(["status", "--short"], cwd=repo_root).stdout
            self.assertIn("R  topic/basic.md -> topic/renamed.md", status)
            self.assertIn(
                "R  topic/resources/i18n/basic-en.md -> topic/resources/i18n/renamed-en.md",
                status,
            )
            self.assertEqual(kb_translation.find_staged_candidates(repo_root, limit=None), [])

    def test_renamed_and_modified_article_still_becomes_outdated_after_sidecar_move(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            init_repo(repo_root)
            article_path = self.write_publishable_article(repo_root / "topic", "basic.md")
            original_blob = run_git(["hash-object", str(article_path)], cwd=repo_root).stdout.strip()
            translation_path = article_path.parent / "resources" / "i18n" / "basic-en.md"
            translation_path.parent.mkdir(parents=True)
            translation_path.write_text(
                textwrap.dedent(
                    f"""\
                    ---
                    Title: English title
                    SourceBlob: {original_blob}
                    ---

                    ```
                    BriefIntroduction: English intro
                    ```

                    <!-- split -->

                    # English title
                    """
                ),
                encoding="utf-8",
            )
            run_git(["add", "."], cwd=repo_root)
            run_git(["commit", "-m", "initial"], cwd=repo_root)

            renamed_article = article_path.with_name("renamed.md")
            run_git(
                [
                    "mv",
                    str(article_path.relative_to(repo_root)),
                    str(renamed_article.relative_to(repo_root)),
                ],
                cwd=repo_root,
            )
            with renamed_article.open("a", encoding="utf-8") as article:
                article.write("\n新段落。\n")
            run_git(["add", str(renamed_article.relative_to(repo_root))], cwd=repo_root)

            kb_translation.move_staged_translation_sidecars(repo_root)
            candidates = kb_translation.find_staged_candidates(repo_root, limit=None)

            self.assertEqual(
                candidates,
                [
                    kb_translation.Candidate(
                        source_md=renamed_article,
                        status="outdated_translation",
                    )
                ],
            )

    def test_default_repo_root_points_to_kb_root(self):
        expected = MODULE_PATH.parents[2]
        self.assertEqual(kb_translation.default_repo_root(MODULE_PATH), expected)

    def test_read_translation_source_blob_supports_new_frontmatter_field(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            translation_path = Path(temp_dir) / "basic-en.md"
            translation_path.write_text(
                textwrap.dedent(
                    """\
                    ---
                    Title: English title
                    SourceBlob: 1111111111111111111111111111111111111111
                    ---

                    ```
                    BriefIntroduction: English intro
                    ```

                    <!-- split -->

                    # English title
                    """
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                kb_translation.read_translation_source_blob(translation_path),
                "1111111111111111111111111111111111111111",
            )

    def test_request_translation_uses_codex_exec_and_returns_last_message(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)

            def fake_run(args, capture_output, check, text, input):
                self.assertIn("codex", args[0].lower())
                self.assertEqual(args[1], "exec")
                self.assertFalse(text)
                self.assertIsInstance(input, bytes)
                output_index = args.index("-o") + 1
                output_path = Path(args[output_index])
                output_path.write_text("# English\n\nTranslated body.\n", encoding="utf-8")
                return subprocess.CompletedProcess(args=args, returncode=0, stdout=b"", stderr=b"")

            with mock.patch.object(kb_translation.subprocess, "run", side_effect=fake_run):
                translated = kb_translation.request_translation(
                    repo_root=repo_root,
                    source_article=kb_translation.SourceArticle(
                        title="中文标题",
                        brief_intro="中文简介",
                        body="# 中文\n\n正文\n",
                    ),
                    model="gpt-test",
                )

            self.assertEqual(translated, "# English\n\nTranslated body.\n")

    def test_resolve_codex_command_prefers_system_path(self):
        with mock.patch.object(
            kb_translation.shutil,
            "which",
            side_effect=[None, r"C:\Users\Windows 10\.local\bin\codex.cmd"],
        ):
            command = kb_translation.resolve_codex_command()
        self.assertEqual(command, r"C:\Users\Windows 10\.local\bin\codex.cmd")


if __name__ == "__main__":
    unittest.main()
