from pathlib import Path
import subprocess
import tempfile

import pytest

from py2js.compiler import Compiler


test_cases = (Path(__file__).parent / 'examples').iterdir()


@pytest.mark.parametrize('filename', test_cases)
def test_runs(filename):
    python_output = subprocess.check_output(['python3', filename])

    with tempfile.TemporaryDirectory() as tmpdir:
        compiler = Compiler(tmpdir)
        js_filename = compiler.compile_file(filename)
        js_output = subprocess.check_output(
            ['node', '--experimental-modules', js_filename]
        )

    assert python_output == js_output
