from abc import ABC, abstractstaticmethod
from ..solution import Solution
from typing import Optional


class AbstractShaking(ABC):
    @abstractstaticmethod
    def shake_solution(solution_to_shake: Solution) -> Optional[Solution]:
        pass
