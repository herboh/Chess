# CLAUDE.md - Code Guidelines for Chess Project

## Run Commands
- Run game: `python ChessMain.py`
- Debug mode: `python ChessMain.py --debug`

## Code Style Guidelines
- **Indentation**: 4 spaces
- **Naming**:
  - Classes: PascalCase (GameState, Move)
  - Functions: camelCase (loadImages, makeMove)
  - Variables: camelCase (validMoves, playerClicks)
  - Constants: UPPERCASE (WIDTH, HEIGHT, MAX_FPS)
- **Imports**: Simple imports at top of file
  - Game modules: `import ChessEngine`
  - External: `import pygame as p`
- **Organization**:
  - ChessEngine.py: Game logic and board representation
  - ChessMain.py: UI handling with pygame
- **Documentation**: Docstrings for classes and non-trivial functions
- **Error handling**: Minimal, relies on pygame event handling
- **Move representation**: Tuples of start and end positions [(row1, col1), (row2, col2)]
- **Board representation**: 2D list, pieces as two-character strings (first character: color, second: piece type)