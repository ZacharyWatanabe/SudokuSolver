#!/usr/bin/env python
#coding:utf-8

"""
PuzzleManager.py 
Zachary Watanabe-Gastel
"""

#Notation for row and column indexes
ROWS = "ABCDEFGHI"
COLS = "123456789"
PLACEHOLDER = '0'

class PuzzleManager(object):

    """ 
    The PuzzleManager class encapsulates the management of sudoku puzzles.

    The PuzzleManager class manages the I/O, puzzle selection, and 
    puzzle solutions for each sudoku puzzle.

    Attributes:
    	puzzles: list of all the sudokus puzzles formated such that
    	each position is accessible by row, column concatenated string
    	current_puzzle_indx: spefifies which puzzle is currently in use.

    """

    def __init__(self, input_file="sudokus.txt"):
        """Initializes the PuzzleManager class.

        As part of the initialization of PuzzleManager, all of the
        puzzles are stored in list of dictionaries.

        Args:
        	input_file: the name of the input_file which defaults to
        	sample data in sudokus.txt contained in this repository.

        Raises:
        	IOerror if the file cannot be read
        """
        self.puzzles = []
        self.current_puzzle_indx = 0
        # Reading of sudoku list from file
        try:
            self.input_file = open(input_file, "r")
            for puzzle in self.input_file.read().split("\n"):
                #Reformat each puzzle into dictionary accessible by row and column index,
                #e.g. puzzle["A2"] = 1
                reformed = {ROWS[i] + COLS[j]: int(puzzle[9*i+j]) for i in range(9) for j in range(9)}
                self.puzzles.append(reformed)
        except IOError:
            print "ERROR: Reading the sudoku file."
            exit()

    def print_puzzle(self):
        """Utility function to print the current sudoku."""
        print "-----------------"
        for row in ROWS:
            for col in COLS:
                print self.puzzles[self.current_puzzle_indx][row + col],
            print ""

    def write_puzzle(self, out_file='output.txt'):
        """Utility function to write each sudoku to file."""
        try:
            fout = open(out_file, 'a')
        except IOError:
            print "Error in reading the sudoku file."
            exit()
        fout.write("\n-----------------")
        for row in ROWS:
            fout.write('\n')
            for col in COLS:
                fout.write(str(self.puzzles[self.current_puzzle_indx][row + col]))
        fout.close()

    def init_domains(self):
        """Determines the domains for each position in the puzzle
        Set the domain of each position within puzzle to its predetermined
     	value or all possible values if currently a placeholder (0).
        """
        domains = {}
        for pos in self.puzzles[self.current_puzzle_indx]:
           
            if str(self.puzzles[self.current_puzzle_indx][pos]) == PLACEHOLDER:
                domains[pos] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                domains[pos] = [int(self.puzzles[self.current_puzzle_indx][pos])]
        return domains


    def get_value(self, row, col):
        """Access the value at a position in the current sudoku.

        Args:
        	row:the row index of a position
        	col:the column index of a position

        Returns:
        	The value at the specified position in the sudoku.
        """
        return self.puzzles[self.current_puzzle_indx][row + col]

    def next_puzzle(self):
        """Increments the index of the current puzzle.

    	Returns:
    		True if there is another puzzle and False if not.
    	"""
        if len(self.puzzles) > (self.current_puzzle_indx + 1 ):
            self.current_puzzle_indx += 1
            return True
        else:
            return False

    def save_puzzle(self, sudoku):
    	"""Saves puzzle to sudoku

    	Args:
    		sudoku: puzzle to save
    	"""
    	self.puzzles[self.current_puzzle_indx] = sudoku        
    