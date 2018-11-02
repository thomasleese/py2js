def print(*args, sep: str = ' ', end: str = '\n'):
    console.log(sep.join([str(arg) for arg in args]))
