from z3 import Solver, Bool, And, Or, Not, Implies, sat, unsat
import numpy as np

n = 9


class SudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.solver = None
        self.variables = None

    def create_variables(self):
        """
        Set self.variables as a 3D list containing the Z3 variables. 
        self.variables[i][j][k] is true if cell i,j contains the value k+1.
        """
        self.variables = np.empty((n, n, n), dtype=object)  # initialize the 3D list
        for i in range(n):  # iterate over rows
            for j in range(n):  # iterate over columns
                for k in range(n):  # iterate over the list possible assignments for each cell
                    self.variables[i][j][k] = Bool(f"b{i}{j}{k + 1}")  # initialize the boolean variables

    def encode_rules(self):
        """
        Encode the rules of Sudoku into the solver.

        The rules are:
        1. Each cell must contain a value between 1 and 9.
        2. Each row must contain each value exactly once.
        3. Each column must contain each value exactly once.
        4. Each 3x3 subgrid must contain each value exactly once.
        """
        # Your code here
        """
        Logic for each cell having exactly one value assigned
        """
        for i in range(n):
            for j in range(n):
                self.solver.add(
                    Or(*[self.variables[i][j][k] for k in range(n)]))  # ensure that each cell has at least one
                # number assigned

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n)[k + 1:]:
                        self.solver.add(Not(And(*[self.variables[i][j][k], self.variables[i][j][l]])))  # make sure
                        # that a cell does not get assigned more than one value

        """
        Logic for each row containing each value exactly once
        """
        for k in range(n):
            for i in range(n):
                self.solver.add(Or(*[self.variables[i][j][k] for j in
                                     range(n)]))  # make sure each row that each row has each value at least once
                for j in range(n):
                    for l in range(n)[j + 1:]:
                        self.solver.add(
                            Not(And(*[self.variables[i][j][k], self.variables[i][l][k]])))  # make sure each
                        # row does not have any value more than once

        """
        Logic for each column containing each value exactly once
        """
        for k in range(n):
            for i in range(n):
                self.solver.add(Or(*[self.variables[j][i][k] for j in
                                     range(n)]))  # make sure each column that each row has each value at least once
                for j in range(n):
                    for l in range(n)[j + 1:]:
                        self.solver.add(
                            Not(And(*[self.variables[j][i][k], self.variables[l][i][k]])))  # make sure each
                        # column does not have any value more than once

        """
        Logic for each 3x3 subgrid containing each value exactly once
         """
        for k in range(n):
            for i in range(0, n, 3):  # iterate over the top left corner cells of each subgrid
                for j in range(0, n, 3):
                    self.solver.add(Or(*[self.variables[a][b][k]  # ensure each subgrid has each number at least once
                                         for a in range(i, i + 3)
                                         for b in range(j, j + 3)]))
                    for a in range(i, i + 3):
                        for b in range(j, j + 3):
                            for c in range(i, i + 3):
                                for d in range(j, j + 3):
                                    if a != c and b != d:  # consider implies
                                        self.solver.add(Not(And(*[self.variables[a][b][k], self.variables[c][d][
                                            k]])))  # iterate over each subgrid to ensure that each number does not appear more than once

    def encode_puzzle(self):
        """
        Encode the initial puzzle into the solver.
        """
        # Your code here
        for i in range(n):  # iterate over the puzzle
            for j in range(n):
                if (self.puzzle[i][j] != 0):  # if not empty
                    self.variables[i][j][self.puzzle[i][
                                             j] - 1] = True  # assign true to the corresponding index for each value for each cell

    def extract_solution(self, model):
        """
        Extract the satisfying assignment from the given model and return it as a 
        9x9 list of lists.
        Args:
            model: The Z3 model containing the satisfying assignment.
        Returns:
            A 9x9 list of lists of integers representing the Sudoku solution.
        Hint:
            To access the value of a variable in the model, you can use:
            value = model.evaluate(var)
            where `var` is the Z3 variable whose value you want to retrieve.
        """
        # Your code here
        answer = np.empty(n, n)  # initialize 9x9 grid that will represent the answer
        for i in range(n):  # iterate over the grid
            for j in range(n):
                answer[i][j] = model.evaluate(self.variables[i][
                                                  j]) + 1  # access the value from the z3 3D list and add 1 to correct for indexing and assign that to the corresponding position in the grid

        return answer  # return the answer

    def solve(self):
        """
        Solve the Sudoku puzzle.
        
        :return: A 9x9 list of lists representing the solved Sudoku puzzle, or None if no solution exists.
        """
        self.solver = Solver()
        self.create_variables()
        self.encode_rules()
        self.encode_puzzle()

        if self.solver.check() == sat:
            model = self.solver.model()
            solution = self.extract_solution(model)
            return solution
        else:
            return None


def main():
    print("Attempting to solve:")
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    for row in puzzle:
        print(row)

    solver = SudokuSolver(puzzle)
    solution = solver.solve()

    if solution:
        print("Solution found:")
        for row in solution:
            print(row)
    else:
        print("No solution exists.")


if __name__ == "__main__":
    main()
