from typing import Iterable


class Interface:
    def do(self):
        raise NotImplementedError


class SubAlgorithm1(Interface):
    def do(self):
        print('subalgorithm1')


class SubAlgorithm2(Interface):
    def do(self):
        print('subalgorithm2')


class Algorithm(Interface):

    def __init__(self, algorithms: Iterable[Interface]):
        self.algorithms = algorithms

    def do(self):
        print('Algorithm')
        for algo in self.algorithms:
            algo.do()


class App:
    def __init__(self, algorithm: Interface):
        self.algorithm = algorithm

    def run(self):
        self.algorithm.do()


if __name__ == '__main__':

    subalgorithm1 = SubAlgorithm1()
    subalgorithm2 = SubAlgorithm2()

    algorithm = Algorithm([subalgorithm1, subalgorithm2])

    app = App(algorithm)
    app.run()
