from pathlib import Path
import subprocess

import pytest

from py2js.compiler import compile


def load_test_cases():
    path = Path(__file__).parent / 'examples'

    test_cases = path.iterdir()

    return test_cases


test_cases = load_test_cases()


@pytest.mark.parametrize('filename', test_cases)
def test_runs(filename):
    python_output = subprocess.check_output(['python3', filename])
    assert python_output

    javascript_source = compile(filename)
    assert javascript_source

    javascript_output = subprocess.run(
        ['node'], input=bytes(javascript_source, 'UTF-8'), check=True,
        stdout=subprocess.PIPE
    ).stdout
    assert javascript_output

    assert python_output == javascript_output
