from z3 import Solver, Bool, And, Or, Not, Implies, sat, unsat
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
        self.variables = [
        [ [Bool(f"cell_{i}_{j}_{k+1}") for k in range(9)]
            for j in range(9)
        ]
        for i in range(9)
    ]
     

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
        # 1. Each cell must contain exactly one value between 1 and 9.
        for i in range(9):
            for j in range(9):
                # at least one value in each cell
                self.solver.add(Or(self.variables[i][j]))
                # at most one value in each cell
                for k in range(9):
                    for l in range(k + 1, 9):
                        self.solver.add(Not(And(self.variables[i][j][k], self.variables[i][j][l])))

        # Each row must contain each value exactly once.
        for i in range(9):
            for k in range(9):
                # at least one occurrence of each value in the row
                self.solver.add(Or(self.variables[i][j][k] for j in range(9)))
                # at most one occurenence of each value in the row
                for j in range(9):
                    for l in range(j+1,9):
                        self.solver.add(Not(And(self.variables[i][j][k], self.variables[i][l][k])))
        # 3. Each column must contain each value exactly once.
        for j in range(9):
            for k in range(9):
                # at least one occurrence of each value in the column
                self.solver.add(Or([self.variables[i][j][k] for i in range(9)]))
                # at most one occurrence of each value in the column
                for i in range(9):
                    for l in range(i + 1, 9):
                        self.solver.add(Not(And(self.variables[i][j][k], self.variables[l][j][k])))

        # 4. Each 3x3 subgrid must contain each value exactly once.
        for block_i in range(3):
            for block_j in range(3):
                for k in range(9):
                    block_cells = []
                    for i in range(3):
                        for j in range(3):
                            block_cells.append(self.variables[3 * block_i + i][3 * block_j + j][k])
                    # at least one occurrence of each value in the subgrid
                    self.solver.add(Or(block_cells))
                    # at most one occurrence of each value in the subgrid
                    for x1 in range(9):
                        for x2 in range(x1 + 1, 9):
                            self.solver.add(Not(And(block_cells[x1], block_cells[x2])))

        
    def encode_puzzle(self):
        """
        Encode the initial puzzle into the solver.
        """
        # Your code here
        for i in range(9):#iterating over each row
            for j in range(9): #iterating over each column
                value=self.puzzle[i][j]
                if value!=0: #if not empty
                    k=value-1 # getting the actual index
                    self.solver.add(self.variables[i][j][k])
        

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
