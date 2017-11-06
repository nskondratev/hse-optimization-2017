from .abstract_shaking import AbstractShaking
from lab_2.solution import Solution
from lab_2.util import swap_cols
from random import randint


class ShakingByColumns(AbstractShaking):
    @staticmethod
    def shake_solution(solution_to_shake: Solution) -> Solution:
        shaken_solution = solution_to_shake.copy()
        b1 = randint(0, shaken_solution.p - 1)
        b2 = randint(0, shaken_solution.p - 1)
        while (b2 == b1): b2 = randint(0, shaken_solution.p - 1)
        swap_cols(shaken_solution.matrix, b1, b2, shaken_solution.perm_col)
        return shaken_solution
