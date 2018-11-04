from pathlib import Path
import subprocess
import tempfile

import pytest

from py2js.compiler import Compiler


test_cases = ['functions.py', 'modules.py']


@pytest.mark.parametrize('filename', test_cases)
def test_runs(filename):
    path = Path(__file__).parent / 'examples' / filename
    python_output = subprocess.check_output(['python3', path])

    with tempfile.TemporaryDirectory() as tmpdir:
        compiler = Compiler(tmpdir)
        js_path = compiler.compile_file(path)
        js_output = subprocess.check_output(
            ['node', '--experimental-modules', js_path]
        )

    assert python_output == js_output
