import numpy as np
from z3.z3 import Solver, Or, Bool, Not, And, sat


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
        self.variables = np.empty((9, 9, 9), dtype=object)  # initialize the 3D list
        for i in range(9):  # iterate over rows
            for j in range(9):  # iterate over columns
                for k in range(9):  # iterate over the list possible assignments for each cell
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
        for i in range(9):
            for j in range(9):
                self.solver.add(
                    Or(*[self.variables[i][j][k] for k in range(9)]))  # ensure that each cell has at least one
                # number assigned

        for i in range(9):
            for j in range(9):
                for k in range(9):
                    for l in range(9)[k + 1:]:
                        self.solver.add(Not(And(*[self.variables[i][j][k], self.variables[i][j][l]])))  # make sure
                        # that a cell does not get assigned more than one value

        """
        Logic for each row containing each value exactly once
        """
        for k in range(9):
            for i in range(9):
                self.solver.add(Or(*[self.variables[i][j][k] for j in
                                     range(9)]))  # make sure each row that each row has each value at least once
                for j in range(9):
                    for l in range(9)[j + 1:]:
                        self.solver.add(
                            Not(And(*[self.variables[i][j][k], self.variables[i][l][k]])))  # make sure each
                        # row does not have any value more than once

        """
        Logic for each column containing each value exactly once
        """
        for k in range(9):
            for i in range(9):
                self.solver.add(Or(*[self.variables[j][i][k] for j in
                                     range(9)]))  # make sure each column that each row has each value at least once
                for j in range(9):
                    for l in range(9)[j + 1:]:
                        self.solver.add(
                            Not(And(*[self.variables[j][i][k], self.variables[l][i][k]])))  # make sure each
                        # column does not have any value more than once

        """
        Logic for each 3x3 subgrid containing each value exactly once
         """
        for k in range(9):
            for i in range(0, 9, 3):  # iterate over the top left corner cells of each subgrid
                for j in range(0, 9, 3):
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
        for i in range(9):  # iterate over the puzzle
            for j in range(9):
                if (self.puzzle[i][j] != 0):  # if not empty
                    self.solver.add(self.variables[i][j][self.puzzle[i][
                                                             j] - 1] == True)  # assign true to the corresponding index for each value for each cell

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

        booleanAnswer = [[[model.evaluate(self.variables[i][j][k]) for k in range(9)] for j in range(9)] for i in
                         range(9)]  # extract boolean results in a 3d list
        answer = [[0 for _ in range(9)] for _ in range(9)]  # initialize the 2d integer list
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if booleanAnswer[i][j][k]:
                        answer[i][j] = k + 1  # convert the 3d list into integer list of only the true values
                        break  # only one is true so we can break after finding first true for each cell

        return answer  # return the answer

    def solve_with_precluded_solution(self, solution):
        previous_solution_clause = []#to store the assignments from lat solution
        for i in range(9):
            for j in range(9):
                k = solution[i][j] - 1
                previous_solution_clause.append(self.variables[i][j][k])
            # the variables that were true cannot all be true again
        self.solver.add(Not(And(previous_solution_clause)))
            # check for a new solution
        if self.solver.check() == sat:
            model = self.solver.model()
            new_solution = self.extract_solution(model)
            return new_solution
        else:
            return None

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
    puzzle =[ #hardest sudoku puzzle (question 1)
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]

    ]


    for row in puzzle:
        print(row)

    solver = SudokuSolver(puzzle)
    solution = solver.solve()

    if solution:
        print("Solution found:")
        for row in solution:
            print(row)

        newSolution = solver.solve_with_precluded_solution(solution)

        if newSolution:
             print("new solution found")
             for row in newSolution:
              print(row)

        else:
             print("one unique solution")
    else:

        print("No solution exists.")




if __name__ == "__main__":
    main()
