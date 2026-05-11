import random
import time
import os
from copy import deepcopy

# ---------------------------
# Utility Functions
# ---------------------------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def input_grid():
    print("Enter your Sudoku grid (9 rows, space-separated, use 0 for empty):")
    grid = []
    for i in range(9):
        while True:
            row = input(f"Row {i+1}: ").strip().split()
            if len(row) == 9 and all(x.isdigit() and 0 <= int(x) <= 9 for x in row):
                grid.append([int(x) for x in row])
                break
            else:
                print("Invalid input. Enter exactly 9 numbers between 0–9.")
    return grid


# ---------------------------
# Sudoku Solver
# ---------------------------
class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        self.domains = {}
        self.delay = 0.3
        self.steps = 0
        self.backtracks = 0

    def print_board(self, highlight=None):
        clear()
        print("\n" + "-" * 25)
        for i in range(9):
            row = ""
            for j in range(9):
                val = self.grid[i][j]
                cell = str(val) if val != 0 else "."

                if highlight == (i, j):
                    cell = f"\033[93m[{cell}]\033[0m"  # highlight
                else:
                    cell = f" {cell} "

                row += cell
                if j % 3 == 2 and j != 8:
                    row += "|"
            print(row)
            if i % 3 == 2 and i != 8:
                print("-" * 25)

        time.sleep(self.delay)

    def is_safe(self, row, col, num):
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        box_r, box_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if self.grid[r][c] == num:
                    return False
        return True

    def initialize_domains(self):
        for r, c in self.variables:
            if self.grid[r][c] != 0:
                self.domains[(r, c)] = [self.grid[r][c]]
            else:
                self.domains[(r, c)] = [
                    num for num in range(1, 10)
                    if self.is_safe(r, c, num)
                ]

    def get_neighbors(self, var):
        r, c = var
        neighbors = set()

        for i in range(9):
            neighbors.add((r, i))
            neighbors.add((i, c))

        box_r, box_c = 3 * (r // 3), 3 * (c // 3)
        for i in range(box_r, box_r + 3):
            for j in range(box_c, box_c + 3):
                neighbors.add((i, j))

        neighbors.remove(var)
        return neighbors

    def select_unassigned_variable(self):
        unassigned = [(r, c) for r, c in self.variables if self.grid[r][c] == 0]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def order_values(self, var):
        def impact(value):
            return sum(value in self.domains[n] for n in self.get_neighbors(var))
        return sorted(self.domains[var], key=impact)

    def forward_check(self, var, value):
        removed = []
        for neighbor in self.get_neighbors(var):
            if value in self.domains[neighbor]:
                self.domains[neighbor].remove(value)
                removed.append((neighbor, value))
                if not self.domains[neighbor]:
                    return False, removed
        return True, removed

    def backtrack(self):
        if all(self.grid[r][c] != 0 for r, c in self.variables):
            return True

        var = self.select_unassigned_variable()
        r, c = var

        for value in self.order_values(var):
            if self.is_safe(r, c, value):
                self.grid[r][c] = value
                self.steps += 1
                self.print_board(highlight=(r, c))

                backup = deepcopy(self.domains)
                self.domains[var] = [value]

                valid, _ = self.forward_check(var, value)

                if valid and self.backtrack():
                    return True

                # Backtrack
                self.grid[r][c] = 0
                self.domains = backup
                self.backtracks += 1
                self.print_board(highlight=(r, c))

        return False

    def solve(self):
        self.initialize_domains()
        self.print_board()

        start_time = time.time()
        self.backtrack()
        end_time = time.time()

        self.time_taken = end_time - start_time
        return self.grid


# ---------------------------
# Sudoku Generator
# ---------------------------
class SudokuGenerator:
    def __init__(self):
        self.grid = [[0] * 9 for _ in range(9)]

    def is_safe(self, row, col, num):
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        box_r, box_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if self.grid[r][c] == num:
                    return False
        return True

    def fill_grid(self):
        for i in range(81):
            row, col = divmod(i, 9)
            if self.grid[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if self.is_safe(row, col, num):
                        self.grid[row][col] = num
                        if self.fill_grid():
                            return True
                        self.grid[row][col] = 0
                return False
        return True

    def remove_numbers(self, difficulty=40):
        attempts = difficulty
        while attempts > 0:
            r, c = random.randint(0, 8), random.randint(0, 8)
            if self.grid[r][c] != 0:
                self.grid[r][c] = 0
                attempts -= 1

    def generate(self, difficulty=40):
        self.fill_grid()
        self.remove_numbers(difficulty)
        return self.grid


# ---------------------------
# Run Program
# ---------------------------
if __name__ == "__main__":
    print("Sudoku Program")
    print("1. Generate Random Grid")
    print("2. Input Your Own Grid")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        generator = SudokuGenerator()
        puzzle = generator.generate(difficulty=45)

    elif choice == "2":
        puzzle = input_grid()

    else:
        print("Invalid choice. Using generator.\n")
        generator = SudokuGenerator()
        puzzle = generator.generate(difficulty=45)

    solver = SudokuSolver(puzzle)

    print("\nInitial Puzzle:")
    solver.print_board()   # 👈 show formatted grid

    input("\nPress Enter to start solving...")  # optional pause
    
    print("\nSolving...\n")
    solution = solver.solve()

    print("\nFinal Solution:")
    for row in solution:
        print(row)

    print(f"\n⏱ Time taken: {solver.time_taken:.4f} seconds")
    print(f"Steps: {solver.steps}")
    print(f"Backtracks: {solver.backtracks}")