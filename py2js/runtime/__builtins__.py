def print(*args, sep: str = ' ', end: str = '\n'):
    string_args = []
    for arg in args:
        string_args.append(str(arg))
    console.log(sep.join(string_args))

    # console.log(sep.join([str(arg) for arg in args]))
