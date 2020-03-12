from typing import Iterable


class SubAlgorithm1(Interface):
    def do(self):
        print('subalgorithm1')


class SubAlgorithm2(Interface):
    def do(self):
        print('subalgorithm2')


class Interface:
    def do(self):
        raise NotImplementedError


class Algorithm(Interface):
    def __init__(self, algorithms: Iterable[Interface]):
        self.algorithms = algorithms

    def do(self):
        for algorithm in self.algorithms:
            algorithm.do()


class App:
    def __init__(self, algorithms: Interface):
        self.algorithm = algorithm

    def run(self):
        self.algorithm.do()


def subalgorithm1():
    print('subalgorithm1')


def subalgorithm2():
    print('subalgorithm2')


def algorithm():
    subalgorithm1()
    subalgorithm2()


def main():
    algorithm()


if __name__ == '__main__':
    main()

    subalgorithm1 = SubAlgorithm1()
    subalgorithm2 = SubAlgorithm2()

    algorithm = Algorithm((subalgorithm1, subalgorithm2))
    # algorithm = Algorithm()
    app = App(algorithm)
    app.run()
