import subprocess
from pathlib import Path


def test_registration_javascript_regressions():
    repo_root = Path(__file__).resolve().parents[3]
    result = subprocess.run(
        [
            "node",
            "--test",
            "paddle/frontend/tests/js/registerForm.test.js",
            "paddle/frontend/tests/js/passwordValidation.test.js",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
