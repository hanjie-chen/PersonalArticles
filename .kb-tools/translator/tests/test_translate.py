import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "workflow.py"
CLI_PATH = Path(__file__).resolve().parents[1] / "translate.py"
SPEC = importlib.util.spec_from_file_location("workflow", MODULE_PATH)
kb_translation = importlib.util.module_from_spec(SPEC)
sys.modules["workflow"] = kb_translation
assert SPEC.loader is not None
SPEC.loader.exec_module(kb_translation)


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
                return_value="# English title\n\nEnglish body.\n",
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
            self.assertTrue(content.startswith(f"<!-- source_blob: {'a' * 40} -->\n\n"))
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
            self.assertEqual(result.stdout.strip(), "")

    def test_default_repo_root_points_to_kb_root(self):
        expected = MODULE_PATH.parents[2]
        self.assertEqual(kb_translation.default_repo_root(MODULE_PATH), expected)

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
                    source_markdown="# 中文\n\n正文\n",
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

