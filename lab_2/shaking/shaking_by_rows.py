from .abstract_shaking import AbstractShaking
from ..solution import Solution
from ..util import swap_rows
from random import randint


class ShakingByRows(AbstractShaking):
    @staticmethod
    def shake_solution(solution_to_shake: Solution) -> Solution:
        shaken_solution = solution_to_shake.copy()
        a1 = randint(0, shaken_solution.m - 1)
        a2 = randint(0, shaken_solution.m - 1)
        while (a2 == a1): a2 = randint(0, shaken_solution.m - 1)
        swap_rows(shaken_solution.matrix, a1, a2, shaken_solution.perm_row)
        return shaken_solution
