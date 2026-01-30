import subprocess
import sys

from fullstack import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "fullstack", "--version"]
    assert (
        subprocess.check_output(cmd).decode().strip()
        == f"fullstack, version {__version__}"
    )
