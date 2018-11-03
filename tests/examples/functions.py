def args_with_default(a, b='b', c='c'):
    print(a, b, c)


args_with_default('a', 'b2')


def kwargs_with_default(a, *, msg='test', **kwargs):
    print(a, msg)


kwargs_with_default('hi', msg='test2')
