import importlib.machinery
import importlib.util
import types
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "pre-commit.d"
    / "20-translate-staged-articles.py"
)


def load_module():
    loader = importlib.machinery.SourceFileLoader("translate_staged_articles", str(MODULE_PATH))
    spec = importlib.util.spec_from_loader("translate_staged_articles", loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TranslateStagedArticlesHookTests(unittest.TestCase):
    def test_uses_one_worker_per_staged_candidate_by_default(self):
        module = load_module()
        root_dir = Path("/repo")
        candidates = [
            types.SimpleNamespace(source_md=root_dir / "first.md", status="outdated_translation"),
            types.SimpleNamespace(source_md=root_dir / "second.md", status="missing_translation"),
        ]
        results = [
            types.SimpleNamespace(translation_path="resources/i18n/first-en.md", error=None),
            types.SimpleNamespace(translation_path="resources/i18n/second-en.md", error=None),
        ]

        def run_translation_jobs(**kwargs):
            self.assertEqual(kwargs["worker_count"], 2)
            self.assertEqual(kwargs["indexed_candidates"], list(enumerate(candidates, start=1)))
            return results

        with (
            mock.patch.object(module, "repo_root", return_value=root_dir),
            mock.patch.object(
                module,
                "load_translator",
                return_value=(RuntimeError, lambda root, limit: candidates, run_translation_jobs),
            ),
            mock.patch.object(module, "git_add") as git_add,
            mock.patch.dict(module.os.environ, {}, clear=True),
        ):
            exit_code = module.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            [call.args for call in git_add.call_args_list],
            [
                (root_dir, root_dir / "resources/i18n/first-en.md"),
                (root_dir, root_dir / "resources/i18n/second-en.md"),
            ],
        )

    def test_respects_configured_worker_count(self):
        module = load_module()
        self.assertEqual(module.worker_count_for(3), 3)
        with mock.patch.dict(module.os.environ, {"KB_TRANSLATOR_JOBS": "2"}):
            self.assertEqual(module.worker_count_for(3), 2)
        with mock.patch.dict(module.os.environ, {"KB_TRANSLATOR_JOBS": "10"}):
            self.assertEqual(module.worker_count_for(3), 3)


if __name__ == "__main__":
    unittest.main()
