import contextlib
import importlib.machinery
import importlib.util
import io
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "pre-commit"


def load_module():
    loader = importlib.machinery.SourceFileLoader("pre_commit", str(MODULE_PATH))
    spec = importlib.util.spec_from_loader("pre_commit", loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PreCommitHookTests(unittest.TestCase):
    def test_prints_visible_success_when_no_uppercase_image_extensions_exist(self):
        module = load_module()
        stdout = io.StringIO()

        with (
            mock.patch.object(
                module,
                "get_staged_files",
                return_value=["article.md", "resources/images/cover.png"],
            ),
            mock.patch.object(module, "rename_image_extensions", return_value=False),
            contextlib.redirect_stdout(stdout),
            self.assertRaises(SystemExit) as exit_context,
        ):
            module.main()

        self.assertEqual(exit_context.exception.code, 0)
        self.assertEqual(
            stdout.getvalue().strip().splitlines(),
            [
                "[pre-commit] checking staged image extensions...",
                "[pre-commit] ok: no uppercase image extensions found",
            ],
        )

    def test_prints_review_instruction_when_image_extensions_are_renamed(self):
        module = load_module()
        stdout = io.StringIO()

        with (
            mock.patch.object(
                module,
                "get_staged_files",
                return_value=["resources/images/cover.JPG"],
            ),
            mock.patch.object(module, "rename_image_extensions", return_value=True),
            contextlib.redirect_stdout(stdout),
            self.assertRaises(SystemExit) as exit_context,
        ):
            module.main()

        self.assertEqual(exit_context.exception.code, 1)
        self.assertEqual(
            stdout.getvalue().strip().splitlines(),
            [
                "[pre-commit] checking staged image extensions...",
                "[pre-commit] updated staging area after lowercasing image extensions",
                "[pre-commit] commit stopped; please review changes and run git commit again",
            ],
        )


if __name__ == "__main__":
    unittest.main()
