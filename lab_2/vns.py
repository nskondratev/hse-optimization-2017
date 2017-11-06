from lab_2.solution import Solution

class GVNS:
    @staticmethod
    def solve(initial_solution: Solution, shaking_neighborhood: list, ls_neighborhood: list) -> Solution:
        k = 0
        x = initial_solution
        while k < len(shaking_neighborhood):
            cur_sh_neighborhood = shaking_neighborhood[k]
            x1 = cur_sh_neighborhood.shake_solution(x)
            l = 0
            while l < len(ls_neighborhood):
                cur_ls_neighborhood = ls_neighborhood[l]
                x2 = cur_ls_neighborhood.improve_solution(x1)
                if x2 is not None and x2.is_better(x1):
                    x1 = x2
                    l = 0
                else:
                    l += 1
            if x1.is_better(x):
                x = x1
                k = 0
            else:
                k += 1
        return x
