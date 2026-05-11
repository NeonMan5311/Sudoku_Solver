#  Sudoku Solver & Generator

A Python-based **Sudoku Generator and Solver** featuring:

- Random Sudoku puzzle generation
- Custom puzzle input support
- Intelligent solving using:
  - Backtracking
  - Constraint Satisfaction Problem (CSP) techniques
  - Minimum Remaining Values (MRV)
  - Least Constraining Value (LCV)
  - Forward Checking
- Animated terminal visualization
- Performance statistics (steps, backtracks, solving time)

---

# Features

## Sudoku Puzzle Generator
Generate random Sudoku puzzles with adjustable difficulty by removing cells from a fully solved board.

## Smart Sudoku Solver
The solver uses advanced AI-inspired techniques:

| Technique | Description |
|---|---|
| Backtracking | Recursive search algorithm |
| MRV Heuristic | Chooses variable with minimum remaining values |
| LCV Heuristic | Chooses least constraining value first |
| Forward Checking | Eliminates invalid future possibilities |

## Terminal Visualization
- Live solving animation
- Highlighted current cell
- Clean Sudoku board formatting

## Performance Metrics
Displays:
- Total solving time
- Number of steps
- Number of backtracks

---

# Technologies Used

- Python 3
- Object-Oriented Programming (OOP)
- CSP (Constraint Satisfaction Problem) Concepts
- ANSI Terminal Coloring

---

# 📂 Project Structure

```bash
Sudoku_Solver/
│
├── main.py        # Main project file
├── index.html
├── README.md
