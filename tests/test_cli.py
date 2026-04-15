import subprocess
import sys

from fe_sequencers import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "fe_sequencers", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
