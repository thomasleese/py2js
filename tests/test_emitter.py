from py2js.emitter import Emitter


def test_simple_string():
    emitter = Emitter()
    emitter.emit('var a = 10;')
    assert str(emitter) == 'var a = 10;'


def test_indentation():
    emitter = Emitter()
    emitter.emit('function test() {\n')
    emitter.indent()
    emitter.emit('var a = 10;\nvar b = 10;\n')
    emitter.deindent()
    emitter.emit('}')

    assert str(emitter) == """
function test() {
  var a = 10;
  var b = 10;
}
    """.strip()
