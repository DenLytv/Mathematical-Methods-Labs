from scipy.optimize import linprog
from dataclasses import dataclass, field
from enum import Enum

class OptimizationGoal(Enum):
    MIN = "min"
    MAX = "max"

@dataclass
class LPData:
    a_matrix: list[list] = field(default_factory=list)
    b_vector: list = field(default_factory=list)
    f_vector: list = field(default_factory=list)
    signs: list = field(default_factory=list)
    optimization_goal: OptimizationGoal = OptimizationGoal.MIN
    x_count: int = 0


class DataHandler:
    def __init__(self):
        self.lp_data = LPData()

    def input(self):
        print("""::: Example of Input :::
Enter the linear constraint system and the objective function at the end:
1 6 2 <= 18
3 -1 2 <= 12
2 3 -1 <= 16
F = 3 -6 -2
Choose a goal [1]min or [2]max
> 1
""")
        print("Enter the linear constraint system and the objective function at the end:")
        while True:
            line = input().strip()
            if not line:
                continue

            if line.startswith(('F', 'f')):
                self.lp_data.f_vector = list(map(float, line.split('=')[1].strip().split()))
                break

            parts = line.split()
            coefficients = list(map(float, parts[:-2]))
            sign = parts[-2]
            b_value = float(parts[-1])

            self.lp_data.a_matrix.append(coefficients)
            self.lp_data.b_vector.append(b_value)
            self.lp_data.signs.append(sign)

        self.lp_data.x_count = len(self.lp_data.a_matrix[0])
        while True:
            answer = int(input("Choose a goal [1]min or [2]max\n> "))
            if answer == 1:
                self.lp_data.optimization_goal = OptimizationGoal.MIN
                break
            elif answer == 2:
                self.lp_data.optimization_goal = OptimizationGoal.MAX
                break
            print("\nOops! Incorrect input. Please try again.")

    def get(self):
        return self.lp_data

    def show_data(self):
        print("Linear constraint system:")
        for i in range(len(self.lp_data.a_matrix)):
            line = "{"
            first_term = True
            for j in range(self.lp_data.x_count):
                coef = self.lp_data.a_matrix[i][j]
                if coef != 0:
                    if not first_term:
                        line += ' ' if coef < 0 else ' + '
                    first_term = False
                    if coef == -1:
                        line += "-"
                    elif coef != 1:
                        line += format_num(coef)
                    line += f"x{j + 1}"
            sign = "≤" if self.lp_data.signs[i] == "<=" else "≥" if self.lp_data.signs[i] == ">=" else "="
            line += f" {sign} {format_num(self.lp_data.b_vector[i])}"
            print(line)

        print("Objective function:")
        line = "F = "
        first_term = True
        for i in range(len(self.lp_data.f_vector)):
            coef = self.lp_data.f_vector[i]
            if coef != 0:
                if not first_term:
                    line += ' ' if coef < 0 else ' + '
                first_term = False
                if coef == -1:
                    line += "-"
                elif coef != 1:
                    line += format_num(coef)
                line += f"x{i + 1}"
        line += " -> " + self.lp_data.optimization_goal.value
        print(line)
        print("Desired production plan:")
        print(f"X = ({', '.join(f'x{i + 1}' for i in range(self.lp_data.x_count))}) - ?")


def format_num(number) -> str:
    return f"{number:.0f}" if number.is_integer() else f"{number}"


def solve_lp(lp_data: LPData):
    A_ub, b_ub, A_eq, b_eq = [], [], [], []

    for i, sign in enumerate(lp_data.signs):
        if sign == "<=":
            A_ub.append(lp_data.a_matrix[i])
            b_ub.append(lp_data.b_vector[i])
        elif sign == ">=":
            A_ub.append([-x for x in lp_data.a_matrix[i]])
            b_ub.append(-lp_data.b_vector[i])
        elif sign == "=":
            A_eq.append(lp_data.a_matrix[i])
            b_eq.append(lp_data.b_vector[i])

    c = lp_data.f_vector
    if lp_data.optimization_goal == OptimizationGoal.MAX:
        c = [-x for x in c]

    bounds = [(0, None)] * lp_data.x_count

    result = linprog(c, A_ub=A_ub if A_ub else None, b_ub=b_ub if b_ub else None,
                     A_eq=A_eq if A_eq else None, b_eq=b_eq if b_eq else None,
                     bounds=bounds, method='highs')

    if result.success:
        for i, x in enumerate(result.x):
            print(f"x{i+1} = {x:.2f}")
        optimal_value = -result.fun if lp_data.optimization_goal == OptimizationGoal.MAX else result.fun
        print(f"Optimal value: {optimal_value:.2f}")
    else:
        print("No solution found.")


if __name__ == '__main__':
    data_handler = DataHandler()

    print("================= Inputting =================")
    data_handler.input()

    print("================ You entered ================")
    data_handler.show_data()

    print("================= Result =================")
    solve_lp(data_handler.get())

#1
# 2 1 <= 40
# 3 2 <= 65
# 4 2 <= 80
# F = 25 15


#3
# 1 0 <= 50
# 0 1 <= 80
# 1 1 <= 105
# 4 1 <= 240
# -3 1 <= 0
# 1 0 >= 0
# 0 1 >= 0
# F = 1 5