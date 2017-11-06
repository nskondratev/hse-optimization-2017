from abc import ABC, abstractstaticmethod
from lab_2.solution import Solution
from typing import Optional


class AbstractLocalSearch(ABC):
    @abstractstaticmethod
    def improve_solution(solution_to_improve: Solution) -> Optional[Solution]:
        """
        Get solution improved by local search
        :solution_to_improve:Solution -- Solution to improve
        :return:Solution
        """
        pass
