import pytest

from py2js.emitter import Emitter


@pytest.fixture
def emitter():
    return Emitter()


def test_simple_string(emitter):
    emitter.emit('var a = 10;')
    assert str(emitter) == 'var a = 10;'


def test_indentation(emitter):
    emitter.emit('function test() {\n')
    emitter.indentation += 1
    emitter.emit('var a = 10;\nvar b = 10;\n')
    emitter.indentation -= 1
    emitter.emit('}')

    assert str(emitter) == """
function test() {
  var a = 10;
  var b = 10;
}
    """.strip()
