from SudokuConstraintSolver import SudokuConstraintSolver
from SudokuBacktrackingSolver import SudokuBacktrackingSolver

"""
Example.py 
Zachary Watanabe-Gastel
"""

# Example usage of sudoku solvers

def sub_routine1(solver):
    success = solver.ac3(False)
    if success:
        solver.sudokus.write_puzzle('output_constraint_solver.txt')
        
def sub_routine2(solver):
    success = solver.backtracking()
    if success:
        solver.sudokus.write_puzzle('output_backtracking_solver.txt')



s1 = SudokuConstraintSolver()
sub_routine1(s1)
while s1.sudokus.next_puzzle():
	sub_routine1(s1)
   
s2 = SudokuBacktrackingSolver()
sub_routine2(s2)
while s2.sudokus.next_puzzle():
	sub_routine2(s2)
    
    
