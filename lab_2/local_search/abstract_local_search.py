from abc import ABC, abstractmethod
from lab_2.solution import Solution


class AbstractLocalSearch(ABC):
    def __init__(self, solution: Solution):
        self.initial_solution = solution.copy()

    @abstractmethod
    def get_improved_solution(self) -> Solution:
        """
        Get solution improved by local search
        :return:Solution
        """
        pass
