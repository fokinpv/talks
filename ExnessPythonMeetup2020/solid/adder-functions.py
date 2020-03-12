add = lambda a, b: a + b


def add(a, b):
    return a + b


def get_adder(type_):
    if type_ is int:
        return add
    else:
        raise NotImplementedError


def app():
    a = 1
    b = 2

    #  adder = get_adder(int)
    if type_ is int:
        return add
    else:
        raise NotImplementedError

    add_result = adder(a, b)

    print(add_result)


if __name__ == '__main__':
    app()
