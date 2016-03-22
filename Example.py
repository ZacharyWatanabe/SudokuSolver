from SudokuConstraintSolver import SudokuConstraintSolver
from SudokuBacktrackingSolver import SudokuBacktrackingSolver

"""
Example.py 
Zachary Watanabe-Gastel
Iterate through the list of sudoku puzzles and print the solutions
"""



def sub_routine1(solver):
    #written for constraint solver
    success = solver.ac3(False) #AC3 is passed false to return if a unique solution was found
    if success:
        solver.sudokus.write_puzzle('output_constraint_solver.txt')
        
def sub_routine2(solver):
    #written for backtracking solver	
    success = solver.backtracking() #Backtracking() returns if a unique solution was found
    if success:
        solver.sudokus.write_puzzle('output_backtracking_solver.txt')

# Example usage of sudoku solvers

#Constraint Solver Iterates through puzzle list and prints the puzzles it solves
s1 = SudokuConstraintSolver()
sub_routine1(s1)
while s1.sudokus.next_puzzle():
	sub_routine1(s1)

#Backtracking Solver iterates through puzzle list and prints the puzzles it solves
s2 = SudokuBacktrackingSolver()
sub_routine2(s2)
while s2.sudokus.next_puzzle():
	sub_routine2(s2)
    
    
