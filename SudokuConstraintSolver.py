#!/usr/bin/env python
#coding:utf-8
import math
from PuzzleManager import PuzzleManager

"""
SudokuConstraintSolver.py 
Zachary Watanabe-Gastel
"""

#Notation for row and column indexes
ROWS = "ABCDEFGHI"
COLS = "123456789"
PLACEHOLDER = '0'


class SudokuConstraintSolver(object):
    """ 
    The SudokuConstraintSolver class is a constraint based algorithm
    used to reduce the search space. It utilizes an AC3 algorithm 
    described below.
    """

    def __init__(self, input_file="sudokus.txt"):
        """Initize class by reading all of the sudoku puzzles"""
        self.sudokus = PuzzleManager(input_file)

    def ac3(self, return_domain=False, input_pm=False):
        """Utilizes the Arc Consistency Algorithm #3 to reduce the domains of possible values
    	in the puzzle.

    	This algorithm will initialize the domains and constraints of puzzle. Then apply its
    	constraints to the reduce domains of constrained values. It should be noted that more
    	often than not, AC-3 algorithm will not produce a unique solution but offers significant
    	speed up when used in conjuction with DFS based methods.

    	More info can be found at https://en.wikipedia.org/wiki/AC-3_algorithm

    	Args:
    		return_domain: specifies whether to return the resulting domain or unique solution.
            input_pm: class will not be using its own puzzle manager
    	Returns:
    		If return_domain is True, return the dictionary of possible domain values for entire puzzle.
    		Otherwise, return the unique solution or return False if there are multiple solutions
    	"""
        
        if input_pm:
            self.sudokus = input_pm
            
        #Determine all possible values at each position in the puzzle
        domains = self.sudokus.init_domains()
        solution = {}

        #Find all of the initial constraints for the sudoku puzzle
        queue = []
        for row in ROWS:
            for col in COLS:
                if self.sudokus.get_value(row, col) == int(PLACEHOLDER):
                    queue += self.get_constraints(row, col)

        #Loop while constraints are still being applied
        while queue:
            (pos_1, pos_2) = queue.pop()
            #Remove values inconsistent with the constrains from the domain of possible values
            if self.remove_inconsistent_values(domains, pos_1, pos_2):
                for (pos_1, pos_3) in self.get_constraints(pos_1[0], pos_1[1]):
                    queue.append((pos_3, pos_1))

        if return_domain:
            return domains
        #Check for unique solution
        for pos in domains:
            if len(domains[pos]) == 1:
                solution[pos] = domains[pos].pop()
            else:
                return False
        self.sudokus.save_puzzle(solution)  
        self.sudokus.print_puzzle()      
        return solution


    def get_constraints(self, current_row, current_col):
        """Finds all the constraints that apply to a specified position.

    	Adds all positions in the same column, row, or box and adds them as
    	constraints for the specified position.

    	Args:
    		current_row: specifies the row position in the puzzle to find constraints for.
    		current_col: specifies the column position in the puzzle to find constraints for.
    	Returns:
    		A list of constraints as tuples where the first value is the position
    		index to being constrained by the second value.
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


    def remove_inconsistent_values(self, domain, pos_1, pos_2):
        """Shrinks the domain of a position by removing values

        Test each domain value in position 1 and if no domain value in position 2
        is consistent with that domain value (i.e. can only be that value), remove
        that domain value from position 1.

        Args:
        	domain: a dictionary of all possible domain values
        	pos_1: the position of the domain that we are trying to reduce
        	pos_2: the position of the current constraint
        Returns:
        	returns True if domain of position 1 was reduced and False otherwise
        """
        removed = False
        for val_1 in domain[pos_1]:
            found = False
            for val_2 in domain[pos_2]:
                if val_1 != val_2:
                    found = True
            if not found:
                domain[pos_1].pop(domain[pos_1].index(val_1))
                removed = True
        return removed



