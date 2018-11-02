from pathlib import Path

import pytest

from py2js.compiler import compile_source


def load_test_cases():
    path = Path(__file__).parent / 'examples'

    test_cases = []

    for category_path in path.iterdir():
        for test_path in category_path.iterdir():
            python = (test_path / 'python.py').open().read()
            javascript = (test_path / 'javascript.js').open().read()
            test_cases.append((python, javascript))

    return test_cases


test_cases = load_test_cases()


@pytest.mark.parametrize('python,javascript', test_cases)
def test_example(python, javascript):
    assert compile_source(python) == javascript
