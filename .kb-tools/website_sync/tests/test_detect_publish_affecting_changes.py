import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "detect_publish_affecting_changes.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "detect_publish_affecting_changes", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DetectPublishAffectingChangesTests(unittest.TestCase):
    def test_publish_affecting_paths_match_expected_rules(self):
        module = load_module()
        cases = {
            "README.md": False,
            "tools/README.md": False,
            "AGENTS.md": False,
            ".kb-tools/script.sh": False,
            ".github/workflows/test.yml": False,
            "__template__/article.md": False,
            "tools/powershell-guide/article.md": True,
            "tools/powershell-guide/resources/i18n/article-en.md": True,
            "tools/powershell-guide/resources/images/cover.png": True,
            "tools/powershell-guide/images/legacy.png": True,
            "tools/powershell-guide/assets/demo.gif": True,
            "tools/powershell-guide/notes.txt": False,
        }

        actual = {path: module.is_publish_affecting(path) for path in cases}

        self.assertEqual(actual, cases)


if __name__ == "__main__":
    unittest.main()
