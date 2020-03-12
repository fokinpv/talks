from __future__ import annotations

from abc import ABC, abstractmethod, abstractclassmethod


class AbstractAdder(ABC):

    @abstractmethod
    def add(self, a, b):
        pass


class AbstractAdderFactory:

    @abstractmethod
    def get_adder(self, type_: type) -> AbstractAdder:
        pass


class IntegerAdder(AbstractAdder):

    def add(self, a: int, b: int) -> int:
        return a + b


class AdderFactory(AbstractAdderFactory):

    def get_adder(self, type_: type):
        if type_ is int:
            return IntegerAdder()
        else:
            raise NotImplementedError


def app():
    a = 1
    b = 2

    adder_factory: AbstractAdderFactory = AdderFactory()
    adder: AbstractAdder = adder_factory.get_adder(int)

    result = adder.add(a, b)

    print(result)


if __name__ == '__main__':
    app()
