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


def test_string(emitter, generator):
    generator.visit(ast.Str('test'))
    assert str(emitter) == "'test'"


def test_name(emitter, generator):
    generator.visit(ast.Name('test', None))
    assert str(emitter) == 'test'
