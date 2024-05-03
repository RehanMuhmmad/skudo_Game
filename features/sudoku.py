### Info ###
# Author: Ben Loos


### Imports ###
from random import shuffle, randint
from copy import deepcopy


### Sudoku Class ###
class Sudoku:

    ## Private Methods ##
    def __init__(self, field=[], boxwidth=3):
        """Constructor:
        Instantiates a new Sudoku object with an empty field.

        Args:
            boxwidth (int, optional):
            Defines the amount of numbers in one row of one box.
            Determines the amount of numbers per box and boxes per field as the square of boxwidth.
            Defaults to 3.
        """

        # Define width of one box
        self.__boxwidth = boxwidth

        # With boxwidth define how many boxes are in one row
        self.__fieldwidth = self.__boxwidth**2

        # Symbol used for empty cells
        self.__empty = "-"

        # Create the field with all numbers initialized to 0
        self.__field = field
        if self.__field == []:
            self.__emptyField()

        # Create deepcopy of the initial field for later reference
        self.__originalField = deepcopy(self.__field)

        # Store previous moves
        self.__previousMoves = {"row": [], "col": []}

    def __emptyField(self):
        """Replace the field with an empty field"""

        self.__field = []
        for i in range(self.__fieldwidth):
            self.__field.append([self.__empty] * self.__fieldwidth)

    def __printColumnNumbers(self, col=1):
        """Display column numbers for the user."""

        print()
        print(" " * (len(str(self.__fieldwidth)) + 1), end="")
        for i in range(self.__boxwidth):
            print("  ", end="")
            for j in range(self.__boxwidth):
                print(f"{col: >{len(str(self.__fieldwidth))}} ", end="")
                col += 1
        print()

    def __printRowNumbers(self, row):
        print(f"{row+1: >{len(str(self.__fieldwidth))}} ", end="")

    def __printHorizontalStructure(self):
        """Display - and + symbols above, below, and in between boxes according to the width of the field and length of the number strings"""

        print(
            " " * (len(str(self.__fieldwidth)) + 1)
            + "+"
            + ("-" * (self.__boxwidth * (len(str(self.__fieldwidth)) + 1) + 1) + "+")
            * self.__boxwidth
            + "\n",
            sep="",
            end="",
        )

    def __printVerticalStructure(self):
        """Display | symbol before, after, and in between boxes"""

        print("| ", sep="", end="")

    def __printNumber(self, row, column):
        """Display the number at field[row,col] with leading spaces if numbers can get larger than 9"""

        print(f"{self.__field[row][column]: >{len(str(self.__fieldwidth))}} ", end="")

    def __fillEmptyRow(self, row):
        """Empty entire row of numbers and try to fill it with random numbers.\n
        Returns True if the row was filled\n
        Returns False if there are no more possible numbers"""

        # Create and shuffle list of valid entries
        notUsed = list(range(1, self.__fieldwidth + 1))
        shuffle(notUsed)

        # Clear row
        for col in range(self.__fieldwidth):
            self.__field[row][col] = self.__empty

        # Refill row
        for col in range(self.__fieldwidth):
            if self.isValidMove(notUsed[0], row, col):
                self.__field[row][col] = notUsed[0]
                notUsed.pop(0)
            else:
                return False

        # print(self.__field[row])

        return True

    def __fillRow(self, row):
        """Fill the row with random valid numbers.\n
        Returns True if the row was filled.\n
        Returns False if there are no more possible numbers."""

        for col in range(self.__fieldwidth):
            if self.__field[row][col] == self.__empty:
                available = self.getValid(row, col)
                shuffle(available)
                # print(len(available), end="")
                if len(available) > 0:
                    self.__field[row][col] = available[0]
                else:
                    return False
        # print(self.__field[row])
        return True

    def __remove(self, number):
        """Randomly remove elements from the field and store it to be able to reset to it.

        Args:
            number (int): Number of elements to be removed from the field.
        """
        attempts = 1000
        for i in range(number):
            removedOne = False
            while not removedOne:
                row, col = randint(0, self.__fieldwidth - 1), randint(
                    0, self.__fieldwidth - 1
                )
                if self.__field[row][col] != self.__empty:
                    backup = self.__field[row][col]
                    self.__field[row][col] = self.__empty
                    if self.solve() == 1:
                        removedOne = True
                    else:
                        self.__field[row][col] = backup
                        attempts -= 1
                if not attempts:
                    self.__originalField = deepcopy(self.__field)
                    return
        self.__originalField = deepcopy(self.__field)

    ## Public Methods ##
    def display(self):
        """Display the current Sudoku grid"""

        self.__printColumnNumbers()
        self.__printHorizontalStructure()
        for i in range(self.__fieldwidth):
            self.__printRowNumbers(i)
            self.__printVerticalStructure()
            for j in range(self.__fieldwidth):
                self.__printNumber(i, j)
                if not (j + 1) % self.__boxwidth:
                    self.__printVerticalStructure()
                    if j == self.__fieldwidth - 1:
                        print()
            if not (i + 1) % self.__boxwidth:
                self.__printHorizontalStructure()

    def undo(self):
        """Undo the last move"""

        if len(self.__previousMoves["row"]) == 0:
            return False

        self.__field[
            self.__previousMoves["row"].pop(), self.__previousMoves["col"].pop()
        ]
        return True

    def insert(self, num, row, col):
        """Insert a number at the specified row and column

        Args:
            num (int): Number to insert
            row (int): Row in the field, starting at 0.
            col (int): Column in the field, starting at 0.

        Returns:
            True: if the insert was successful.\n
            False: otherwise
        """

        # Check if the number is valid
        if num < 1 or num > self.__fieldwidth:
            print("Invalid number!")
            return False

        # Check if cell is empty
        if self.__field[row][col] != self.__empty:
            print("Space already occupied!")
            return False

        # Check if the move is valid
        if not self.isValidMove(num, row, col):
            print("That number is not valid for that position.")
            return False

        # All cases passed, insert number
        self.__field[row][col] = num
        self.__previousMoves["row"].append(row)
        self.__previousMoves["col"].append(col)
        return True

    def resetField(self):
        """Reset the field to it's original state."""

        self.__field = deepcopy(self.__originalField)

    def getValid(self, row, col):
        """Get all valid numbers for a position in the field.

        Args:
            row (int): Row in the field, starting at 0.
            col (int): Column in the field, starting at 0.

        Returns:
            list: list of all valid numbers at field[row,col].
        """

        # Create and shuffle list of all available entries
        available = list(range(1, self.__fieldwidth + 1))

        # Run through each row and column and remove occuring numbers
        for i in range(self.__fieldwidth):
            elem = self.__field[i][col]
            if elem != self.__empty and elem in available:
                available.remove(elem)
            elem = self.__field[row][i]
            if elem != self.__empty and elem in available:
                available.remove(elem)

        # Check relevant box and remove occuring numbers
        box = [
            row // self.__boxwidth * self.__boxwidth,
            col // self.__boxwidth * self.__boxwidth,
        ]
        for boxRow in range(self.__boxwidth):
            for boxCol in range(self.__boxwidth):
                elem = self.__field[box[0] + boxRow][box[1] + boxCol]
                if elem != self.__empty and elem in available:
                    available.remove(elem)

        # Return filtered list
        return available

    def isValidMove(self, num, row, col):
        """Check whether or not inserting a number in a position in the field would follow all rules.

        Args:
            num (int): Number to check validity of
            row (int): Row in the field, starting at 0.
            col (int): Column in the field, starting at 0.

        Returns:
            True: if inserting num at field[row,col] would be a valid move.\n
            False: otherwise
        """

        # Check vertical and vertical
        for i in range(self.__fieldwidth):
            if num == self.__field[i][col] or num == self.__field[row][i]:
                return False

        # Check box
        box = [
            row // self.__boxwidth * self.__boxwidth,
            col // self.__boxwidth * self.__boxwidth,
        ]
        for boxRow in range(self.__boxwidth):
            for boxCol in range(self.__boxwidth):
                if num == self.__field[box[0] + boxRow][box[1] + boxCol]:
                    return False

        # All cases passed, the move is valid
        return True

    def validField(self):
        """Check whether the filled field follows all rules.

        Returns:
            True: if the Sudoku field is valid.\n
            False: otherwise
        """

        # Check each vertical
        for row in range(self.__fieldwidth):
            checkNum = []
            for col in range(self.__fieldwidth):
                elem = self.__field[row][col]
                if elem in checkNum:
                    return False
                else:
                    checkNum.append(elem)

        # Check each horizontal
        for col in range(self.__fieldwidth):
            checkNum = []
            for row in range(self.__fieldwidth):
                elem = self.__field[row][col]
                if elem in checkNum:
                    return False
                else:
                    checkNum.append(elem)

        # Check each box
        for boxRow in range(self.__boxwidth):
            for boxCol in range(self.__boxwidth):
                checkNum = []
                for rowInsideBox in range(self.__boxwidth):
                    for colInsideBox in range(self.__boxwidth):
                        elem = self.__field[rowInsideBox + boxRow * self.__boxwidth][
                            colInsideBox + boxCol * self.__boxwidth
                        ]
                        if elem in checkNum:
                            return False
                        else:
                            checkNum.append(elem)

        # All cases passed, the Sudoku grid is valid
        return True

    def isFull(self):
        """Check if field is full. Considering that only valid inputs are allowed, this implies that the Sudoku is solved."""

        for i in self.__field:
            if self.__empty in i:
                return False

        return True

    def chooseLevel(self, level):
        """Generates a Sudoku with the amount of defined cells determined by the Level\n
        Level 1: 33-36\n
        Level 2: 29-32\n
        Level 3: 26-28\n
        Level 4: 23-25

        Args:
            level (int): Level of choice
        """

        # Reshuffle the Sudoku
        self.__emptyField()
        self.solveIterative()

        # Remove cells
        if level == 1:
            self.__remove(self.__fieldwidth**2 - randint(33, 36))
        elif level == 2:
            self.__remove(self.__fieldwidth**2 - randint(29, 32))
        elif level == 3:
            self.__remove(self.__fieldwidth**2 - randint(26, 28))
        elif level == 4:
            self.__remove(self.__fieldwidth**2 - randint(23, 25))
        else:
            return

    def randomize(self):
        """Iterates through each row of the field and run fillEmptyRow until the field is entirely filled\n
        If there is no solution, retries the row until it finds a solution."""

        self.__emptyField()
        for row in range(self.__fieldwidth):
            while not self.__fillEmptyRow(row):
                continue

    def solveIterative(self):
        """Iterates through each row of the field and run fillRow until the field is entirely filled.\n
        If there is no solution, retries for a set amount of attempts. If runs out of attempts, go back to the previous row.
        """

        row = 0
        while row < self.__fieldwidth:
            attempts = 100
            while not self.__fillRow(row):
                # print()
                attempts -= 1
                self.__field[row] = self.__originalField[row].copy()
                if not attempts:
                    row -= 1
                    self.__field[row] = self.__originalField[row].copy()
            row += 1
            attempts = 100

    def solveRecursive(self):
        """Iterates through each row of the field and run fillRow until the field is entirely filled.\n
        If there is no solution, retries for a set amount of attempts. If runs out of attempts, go back to the previous row.
        """

        for row in range(self.__fieldwidth):
            for col in range(self.__fieldwidth):
                if self.__field[row][col] == self.__empty:
                    available = self.getValid(row, col)
                    shuffle(available)
                    for a in available:
                        self.__field[row][col] = a
                        if self.solveRecursive():
                            return True
                        self.__field[row][col] = self.__empty
                    return False
        return True

    def solve(self):
        """Iterates through each row of the field and run fillRow until the field is entirely filled.\n
        If there is no solution, retries for a set amount of attempts. If runs out of attempts, go back to the previous row.
        """

        nSolutions = 0

        for row in range(self.__fieldwidth):
            for col in range(self.__fieldwidth):
                if self.__field[row][col] == self.__empty:
                    available = self.getValid(row, col)
                    shuffle(available)
                    for a in available:
                        self.__field[row][col] = a
                        nSolutions += self.solve()
                        self.__field[row][col] = self.__empty
                    return nSolutions
        # self.display()
        # input("Next solution:")
        return nSolutions + 1
