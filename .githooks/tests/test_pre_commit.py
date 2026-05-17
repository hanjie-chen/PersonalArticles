import contextlib
import importlib.machinery
import importlib.util
import io
import subprocess
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


class PreCommitRunnerTests(unittest.TestCase):
    def test_runs_hook_scripts_in_order(self):
        module = load_module()
        scripts = [
            Path(".githooks/pre-commit.d/10-first.py"),
            Path(".githooks/pre-commit.d/20-second.py"),
        ]
        stdout = io.StringIO()

        with (
            mock.patch.object(module, "iter_hook_scripts", return_value=scripts),
            mock.patch.object(
                module.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0),
            ) as run,
            contextlib.redirect_stdout(stdout),
        ):
            exit_code = module.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            [call.args[0][1] for call in run.call_args_list],
            [str(scripts[0]), str(scripts[1])],
        )
        self.assertEqual(
            stdout.getvalue().strip().splitlines(),
            [
                "[pre-commit]",
                "├─ 10-first.py",
                "└─ 20-second.py",
            ],
        )

    def test_stops_after_first_failed_script(self):
        module = load_module()
        scripts = [
            Path(".githooks/pre-commit.d/10-first.py"),
            Path(".githooks/pre-commit.d/20-second.py"),
        ]
        stdout = io.StringIO()

        with (
            mock.patch.object(module, "iter_hook_scripts", return_value=scripts),
            mock.patch.object(
                module.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 1),
            ) as run,
            contextlib.redirect_stdout(stdout),
        ):
            exit_code = module.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(
            stdout.getvalue().strip().splitlines(),
            [
                "[pre-commit]",
                "├─ 10-first.py",
                "[pre-commit] failed: 10-first.py exited with status 1",
            ],
        )

    def test_continues_after_review_needed_and_stops_at_end(self):
        module = load_module()
        scripts = [
            Path(".githooks/pre-commit.d/10-first.py"),
            Path(".githooks/pre-commit.d/20-second.py"),
        ]
        stdout = io.StringIO()

        with (
            mock.patch.object(module, "iter_hook_scripts", return_value=scripts),
            mock.patch.object(
                module.subprocess,
                "run",
                side_effect=[
                    subprocess.CompletedProcess([], module.REVIEW_NEEDED),
                    subprocess.CompletedProcess([], 0),
                ],
            ) as run,
            contextlib.redirect_stdout(stdout),
        ):
            exit_code = module.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(run.call_count, 2)
        self.assertEqual(
            stdout.getvalue().strip().splitlines(),
            [
                "[pre-commit]",
                "├─ 10-first.py",
                "└─ 20-second.py",
                "",
                "[pre-commit] review required: generated changes were staged",
            ],
        )


if __name__ == "__main__":
    unittest.main()
