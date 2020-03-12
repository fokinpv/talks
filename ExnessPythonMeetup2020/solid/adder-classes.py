class Adder:
    def add(self, a, b):
        return a + b


class AdderFactory:
    @classmethod
    def get_adder(cls, type_):
        if type_ is int:
            return Adder()
        else:
            raise NotImplementedError


def main():
    a = 1
    b = 2

    adder = AdderFactory.get_adder(int)
    result = adder.add(a, b)

    print(result)


if __name__ == '__main__':
    main()
