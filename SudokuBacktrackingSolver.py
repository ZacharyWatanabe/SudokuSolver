#!/usr/bin/env python
#coding:utf-8

"""
SudokuBacktrackingSolver.py
Zachary Watanabe-Gastel
"""

from copy import deepcopy
from SudokuConstraintSolver import SudokuConstraintSolver
from PuzzleManager import PuzzleManager
import math


#Notation for row and column indexes
ROWS = "ABCDEFGHI"
COLS = "123456789"
PLACEHOLDER = '0'

class SudokuBacktrackingSolver():
    """
    This class implements a DFS based approach to solving sudoku puzzles.
    
    The DFS starts from the initial puzzle and tries assumptions about the
    value at the position with the possible values. It will then backtrack 
    when it realizes a solution is inconsistent with the constraints. 
    Additionally forward checking has been implemented to prevent the 
    algorithm from assuming inconsistent values, thus speeding up the 
    recursion.
    """
    
    def __init__(self, input_file="sudokus.txt"):
        """Initize class by reading all of the sudoku puzzles"""
        self.sudokus = PuzzleManager(input_file)

    def backtracking(self):
        """Implements a backtracking DFS search.

    	Returns:
    		Return the unique solution or return False if there are multiple possible solutions
    	"""
        solution = {}
        
        #Use the SudokuConstraintSolver to minimize domain size. 
        #This will shrink the search space and consequentially
        #speed up the search
        constraintSolver = SudokuConstraintSolver()
        domains = constraintSolver.ac3(True, self.sudokus)
        
        #Determine uncertain positions
        positions = []
        for position in domains:
            if(len(domains[position]) > 1):
                positions.append(position)   
                
        #Recursive DFS        
        domains = self.recursive_backtracking(positions, domains)
        
        #Check for unique solution
        for pos in domains:
            if len(domains[pos]) == 1:
                solution[pos] = domains[pos].pop()
            else:
                return False
                
        self.sudokus.save_puzzle(solution)  
        self.sudokus.print_puzzle()
        return solution

    
    def recursive_backtracking(self, variables, domains):
        """Recursive helper for backtracking search.
        Args:
            variables: positions in puzzle with uncertain values
            domains: all possible value for each position
    	Returns:
    		Return the unique solution or return False if there are multiple possible solutions
    	"""
        #Return value if all positions in puzzle are solved
        if len(variables) == 0:
            return domains
        #Get position with smallest domain
        var_pos = variables.pop(variables.index(self.min_constraing_val(domains, variables)))
        constraints = self.get_constraints(var_pos[0], var_pos[1])
        for value in domains[var_pos]:
            inconsistent = False
            #Check if value in domain is inconsistent with constraints
            for (current_position, constraint_position) in constraints:
                if constraint_position not in variables and domains[constraint_position][0] == value:
                    inconsistent = True
            if not inconsistent:
                #Assume this possible value and recursively check solution that have it.
                tmpDomain = self.forward_checking(deepcopy(domains), var_pos, value)
                if not tmpDomain:
                    return False
                tmpDomain[var_pos] = [value]
                result = self.recursive_backtracking(deepcopy(variables), deepcopy(tmpDomain))
                if result:
                    return result
        return False

    def forward_checking(self, domain, var, value):
        """Prevents Assignments that garuntee a failed result later in the search.
        i.e. if a possible value would violate a constraint of the puzzle, then we
        will remove that value from the domain dictionary
        
        Args:
            domain: dictionary with positions within puzzle are keys are hashed to lists possible values
            var: the postion being considered for assignment =[row,column]
            value: teh value being considered for assignment
    	Returns:
    		returns the dictionary of domains
            returns false if a position does not have any possible values
    	"""
        constraints = self.get_constraints(var[0], var[1])
        for (col_1, col_2) in constraints:
            if value in domain[col_2]:
                domain[col_2].pop(domain[col_2].index(value))
            if len(domain[col_2]) < 1:
                return False
        return domain

    def min_constraing_val(self, domains, positions):
        """Finds the position in the puzzle with the smallest possible domain (fewest possible values).
        
        Args:
            domains: dictionary with positions within puzzle are keys are hashed to lists possible values
            positions: list of all positions within puzzle
    	Returns:
    		the position of the smallest domain
    	"""
        smallest = ""
        smallest_size = 9
        for pos in positions:
            if len(domains[pos]) < smallest_size:
                smallest = pos
                smallest_size = len(domains[pos])
        return smallest            
        
    def get_constraints(self, current_row, current_col):
        """Finds all the constraints that apply to a specified position.

    	Adds all positions in the same column, row, or box and adds them as
    	constraints for the specified position.

    	Args:
    		current_row: specifies the row position in the puzzle to find constraints for.
    		current_col: specifies the column position in the puzzle to find constraints for.
    	Returns:
    		A list of constraints as tuples where the first value is the position
    		index to being constrained by the second postion.
    	"""
        constraints = []
        #ROW constraints
        for row in ROWS:
            if row != current_row:
                constraints.append((current_row + current_col, row + current_col))
        #COL Constraints
        for col in COLS:
            if col != current_col:
                constraints.append((current_row + current_col, current_row + col))
        #BOX Constraints
        box_cols = ['123', '456', '789']
        box_rows = ['ABC', 'DEF', 'GHI']
        for b_rows in box_rows:
            if current_row in b_rows:
                box_row = b_rows
        for b_col in box_cols[int(math.ceil(float(current_col)/3)-1)]:
            for b_row in box_row:
                if current_row != b_row and current_col != b_col:
                    constraints.append((current_row + current_col, b_row + b_col))
        return constraints
        