from .solution import Solution


class RVNS:
    @staticmethod
    def solve(initial_solution: Solution, shaking_neighborhood: list, MAX_ITERATIONS: int = 100) -> Solution:
        """
        Improve solution by RVNS
        :param initial_solution: Solution -- Initial solution
        :param shaking_neighborhood: list -- List of shaking neighborhood
        :param MAX_ITERATIONS: int -- Iterations number of RVNS
        :return: Solution -- Improved solution
        """
        x = initial_solution
        for _ in range(MAX_ITERATIONS):
            k = 0
            while k < len(shaking_neighborhood):
                cur_sh_neighborhood = shaking_neighborhood[k]
                x1 = cur_sh_neighborhood.shake_solution(x)
                if x1 is not None and x1.is_better(x):
                    x = x1
                    k = 0
                else:
                    k += 1
        return x
