### Info ###
# Author: Ben Loos


### Imports ###
from features.sudoku import Sudoku
from puzzles import puzzles


### Main ###
sg = Sudoku()  # field=puzzles["Sudoku"][0]
level = 0
while level < 1 or level > 4:
    level = int(input("\nChoose the level you want for the Sudoku (1-4): "))

sg.chooseLevel(level)

print(f"\nThe following Sudoku has \n{sg.solve()} solution:")

while not sg.isFull():
    sg.display()
    try:
        num = int(
            float(
                input(
                    "Enter the number you want to insert (1-9 / 0 to solve / -1 to undo): "
                )
            )
        )
        if num == 0:
            if sg.solveRecursive():
                sg.display()
                break
            else:
                sg.display()
                print("Sudoku has no solution")
                break
        elif num == -1:
            if not sg.undo():
                print("No moves to undo.")
                continue
        row = int(input("In which row? "))
        col = int(input("In which column? "))
    except ValueError:
        print("Invalid input.")
        continue
    except KeyboardInterrupt:
        print("\n\nNo solution found.")
        break

    sg.insert(num, row - 1, col - 1)
else:
    print("Well done!")
