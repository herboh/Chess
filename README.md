# Chess Game
## IF you are reading this, beware of LLM Slop ahead. I used an old project to test Claude Code


A complete chess game implementation using PyGame, with both local and online multiplayer support.

## Features

- Complete chess rules implementation:
  - Standard piece movements
  - Castling (kingside and queenside)
  - En passant captures
  - Pawn promotion
  - Check, checkmate, and stalemate detection
- Graphical user interface:
  - Piece highlighting
  - Move animations
  - Valid move highlighting
  - Last move indication
  - Evaluation bar showing material advantage
- Game controls:
  - 'z' key to undo moves
  - 'r' key to reset the game
  - 'q' key to quit
- Online multiplayer:
  - Server-client architecture
  - Create or join games
  - Spectator mode
  - Turn-based gameplay

## How to Play Locally

1. Run the game with: `python ChessMain.py`
2. Click on a piece to select it
3. Click on a valid destination square to move the piece
4. For pawn promotion, select the desired promotion piece from the menu
5. The game will automatically detect checkmate and stalemate

## How to Play Online

### Setting up the Server

1. Install the required dependencies: `pip install -r requirements.txt`
2. Run the server: `python ChessServer.py`
3. The server will start on the specified IP address and port (default: 5000)

### Connecting as a Client

1. Run the client: `python ChessClient.py`
2. Enter the server URL when prompted (e.g., http://136.47.134.71:5000)
3. Choose to create a new game or join an existing game
4. If creating a game, share the game ID with your opponent
5. If joining a game, enter the game ID provided by the host
6. Play the game following the same controls as the local version

## Implementation Details

The game is structured with:

- `ChessEngine.py`: Game logic, board representation, move validation
- `ChessMain.py`: UI handling with pygame for local play
- `ChessServer.py`: Socket.IO server for online multiplayer
- `ChessClient.py`: Socket.IO client for online multiplayer
- `images/`: Piece images for visualization

## Requirements

- Python 3.x
- PyGame library
- Python-SocketIO
- Eventlet (for server)

Install all dependencies with: `pip install -r requirements.txt`
