import ast

import pytest

from py2js.emitter import Emitter
from py2js.generator import Generator


@pytest.fixture
def emitter():
    return Emitter()


@pytest.fixture
def generator(emitter):
    return Generator(emitter)


def test_temporary_variables(generator):
    temp_vars = generator.temp_vars

    with temp_vars['test'] as arg:
        assert arg == '__test1__'

        with temp_vars['test'] as arg2:
            assert arg2 == '__test2__'

    with temp_vars['test'] as arg:
        assert arg == '__test1__'


def test_string(emitter, generator):
    generator.visit(ast.Str('test'))
    assert str(emitter) == "'test'"


def test_name(emitter, generator):
    generator.visit(ast.Name('test', None))
    assert str(emitter) == 'test'
