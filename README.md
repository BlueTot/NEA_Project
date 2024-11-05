# Sudoku - A Level NEA Project

I made a sudoku generator and solver application for my A Level NEA project, which can generate up to 33 different types of boards on the fly, ranging from killer sudoku to 16x16 sudoku. This appliation uses PyQt6 for the graphical user interface, and uses the Dancing Links (DLX) Algorithm to solve the sudoku puzzles during generation.

## Features

- An easy to use graphical user interface to play sudoku
- 33 different difficulties, in board sizes 4x4, 6x6, 9x9, 12x12, 16x16 and in normal and killer sudoku
- User account management system
- Colour presets to change fonts and background colours (choose from your system available fonts)
- Leaderboard system (only clientside, each app has a different leaderboard)
- Rating calculation system, ranging from Beginner to Master

## Installation

- Type this into your terminal:
  ```
  git clone https://github.com/BlueTot/NEA_Project
  ```
- Run the GUI by doing:
  ```
  python sudoku.py g
  ```

## Dependencies:

- There are multiple package dependencies for this program you must install first for the code to work.
- One of them is PyQt6, can be installed by doing `pip install PyQt6`
