#User Input and validation
import pygame as p
import ChessEngine
import sys

WIDTH = 562 #max of res (512 + 50 for evaluation bar)
HEIGHT = 512
DIMENSION = 8 #Dimensions of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #animations
EVAL_BAR_WIDTH = 50
IMAGES = {}

# Colors
WHITE = p.Color("white")
BLACK = p.Color("black")
GRAY = p.Color("gray")
BLUE = p.Color(100, 100, 255, 100)  # Transparent blue for highlighting
DARK_GREEN = p.Color(0, 100, 0)
GREEN = p.Color(0, 200, 0)
RED = p.Color(240, 0, 0)
YELLOW = p.Color(255, 255, 0, 100)  # Transparent yellow for highlighting

#create dictionary of images. wikimedia commons
def loadImages():
    pieces = ['wP', 'bP', 'wN', 'wB', 'wK', 'wQ', 'wR','bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#Main Loop of Game
def main():
    p.init()
    p.display.set_caption("Chess with Evaluation")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(WHITE)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False  # Flag for when to animate a move
    gameOver = False  # Flag for when game is over
    
    # For pawn promotion
    promotionPieces = ['Q', 'R', 'B', 'N']
    promotionChoice = 0  # Default to queen

    loadImages()  # Load once, move images around
    running = True
    sqSelected = ()  # Initial selection is empty, tracks last click of user (row, col)
    playerClicks = []  # list with 2 tuples: [(6, 5), (4, 4)] pawn move tracked
    movePlayed = []  # To track the last move played for highlighting
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # exit strategy
                running = False
                
            # Mouse functions
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:  # Ignore clicks if game is over
                    location = p.mouse.get_pos()  # Where is the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    
                    # Handle promotion selection
                    if gs.pawnPromotion:
                        if WIDTH // 2 - SQ_SIZE <= location[0] <= WIDTH // 2 + SQ_SIZE:
                            for i, piece in enumerate(promotionPieces):
                                if HEIGHT // 2 - 2 * SQ_SIZE + i * SQ_SIZE <= location[1] <= HEIGHT // 2 - 2 * SQ_SIZE + (i + 1) * SQ_SIZE:
                                    gs.promotionChoice = piece
                                    gs.pawnPromotion = False
                                    moveMade = True
                        continue  # Skip regular move logic when in promotion mode
                    
                    if sqSelected == (row, col):  # this clears the selection after a 2nd click on a square
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        
                    if len(playerClicks) == 2:  # Make a move on the second unique click
                        startSq = playerClicks[0]
                        endSq = playerClicks[1]
                        
                        # Guard against invalid input
                        if not (0 <= startSq[0] < 8 and 0 <= startSq[1] < 8 and 0 <= endSq[0] < 8 and 0 <= endSq[1] < 8):
                            sqSelected = ()
                            playerClicks = []
                            continue
                            
                        move = ChessEngine.Move(startSq, endSq, gs.board)
                        
                        move_is_valid = False
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                movePlayed = [move.startRow, move.startCol, move.endRow, move.endCol]
                                print(move.getChessNotation())
                                
                                # Check for pawn promotion
                                if validMoves[i].isPawnPromotion:
                                    gs.pawnPromotion = True
                                    sqSelected = ()
                                    playerClicks = []
                                    break
                                
                                moveMade = True
                                animate = True
                                sqSelected = ()  # reset the click count
                                playerClicks = []
                                move_is_valid = True
                                break
                                
                        if not move_is_valid and not gs.pawnPromotion:  # Only reset clicks if not in promotion mode
                            playerClicks = [sqSelected]
            
            # Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when keyboard z is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    
                if e.key == p.K_r:  # reset the game when r is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    movePlayed = []
                    
                if e.key == p.K_q:  # quit game when q is pressed
                    running = False
                    
        # Update game state
        if moveMade:
            if animate:
                animateMove(screen, gs.board, clock, movePlayed, gs)
                animate = False
            validMoves = gs.getValidMoves()
            moveMade = False
            
        # Draw the game state
        drawGameState(screen, gs, validMoves, sqSelected, movePlayed)
        
        # Check for end of game
        if gs.checkmate:
            gameOver = True
            drawEndGameText(screen, "Checkmate! " + ("Black" if gs.whiteToMove else "White") + " wins!")
        elif gs.stalemate:
            gameOver = True
            drawEndGameText(screen, "Stalemate! Draw!")
            
        # Draw promotion selection if active
        if gs.pawnPromotion:
            drawPromotionOptions(screen, gs.whiteToMove)
            
        clock.tick(MAX_FPS)
        p.display.flip()

# Animate the move
def animateMove(screen, board, clock, move, gs):
    global colors
    startRow, startCol, endRow, endCol = move
    dR = endRow - startRow
    dC = endCol - startCol
    framesPerSquare = 5  # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (startRow + dR * frame / frameCount,
                startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # Erase the piece moved from its ending square
        color = WHITE if (endRow + endCol) % 2 == 0 else GRAY
        endSquare = p.Rect(endCol * SQ_SIZE, endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # Draw the moving piece
        if board[endRow][endCol] != '--':
            screen.blit(IMAGES[board[endRow][endCol]], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

# Draw promotion options
def drawPromotionOptions(screen, whiteToMove):
    color = "w" if whiteToMove else "b"
    
    # Draw background
    p.draw.rect(screen, BLACK, p.Rect(WIDTH//2 - SQ_SIZE, HEIGHT//2 - 2*SQ_SIZE, 2*SQ_SIZE, 4*SQ_SIZE))
    
    # Draw each promotion option
    promotionPieces = ['Q', 'R', 'B', 'N']
    for i, piece in enumerate(promotionPieces):
        screen.blit(IMAGES[color + piece], p.Rect(WIDTH//2 - SQ_SIZE//2, HEIGHT//2 - 2*SQ_SIZE + i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.draw.rect(screen, WHITE, p.Rect(WIDTH//2 - SQ_SIZE, HEIGHT//2 - 2*SQ_SIZE + i*SQ_SIZE, 2*SQ_SIZE, SQ_SIZE), 2)

# Draw end game text
def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, False, RED)
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH//2 - textObject.get_width()//2, HEIGHT//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)

# Creates graphics on the Board
def drawGameState(screen, gs, validMoves, sqSelected, movePlayed):
    drawBoard(screen)  # squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected, movePlayed)
    drawPieces(screen, gs.board)  # pieces on top of the board
    drawEvaluationBar(screen, gs)  # evaluation bar on the side

def drawBoard(screen):
    colors = [WHITE, GRAY]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, sqSelected, movePlayed):
    # Highlight last move
    if len(movePlayed) == 4:
        startRow, startCol, endRow, endCol = movePlayed
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # transparency value (0-255)
        s.fill(YELLOW)
        screen.blit(s, (startCol * SQ_SIZE, startRow * SQ_SIZE))
        screen.blit(s, (endCol * SQ_SIZE, endRow * SQ_SIZE))
    
    # Highlight selected square
    if sqSelected != ():
        r, c = sqSelected
        # Highlight only if it's the player's piece
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(BLUE)
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            
            # Highlight valid moves from this square
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    # Different highlight for captures versus moves
                    if gs.board[move.endRow][move.endCol] == '--':
                        p.draw.circle(screen, GREEN, 
                                     (move.endCol * SQ_SIZE + SQ_SIZE//2, move.endRow * SQ_SIZE + SQ_SIZE//2), 
                                     SQ_SIZE//8)
                    else:
                        p.draw.circle(screen, RED, 
                                     (move.endCol * SQ_SIZE + SQ_SIZE//2, move.endRow * SQ_SIZE + SQ_SIZE//2), 
                                     SQ_SIZE//2, 4)

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Check if square is empty
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Material values for simple evaluation
def evaluateBoard(gs):
    # Piece values: pawn = 1, knight/bishop = 3, rook = 5, queen = 9
    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,  # King has no material value
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0  # Negative for black pieces
    }
    
    # Normalize to a value between -1 and 1 for drawing
    total = 0
    max_value = 39  # Maximum possible advantage (all pieces minus one king)
    
    for row in gs.board:
        for piece in row:
            if piece != "--":
                # Convert piece code to value (e.g., 'wP' -> 'P', 'bQ' -> 'q')
                piece_type = piece[1] if piece[0] == 'w' else piece[1].lower()
                total += piece_values.get(piece_type, 0)
    
    # Normalize to range between -1 and 1
    return max(min(total / max_value, 1.0), -1.0)

def drawEvaluationBar(screen, gs):
    # Evaluation bar on the right side
    p.draw.rect(screen, GRAY, p.Rect(HEIGHT, 0, EVAL_BAR_WIDTH, HEIGHT))
    
    # Calculate evaluation score from -1 to 1 (where positive is white advantage)
    score = evaluateBoard(gs)
    
    # Calculate how to draw the bar
    bar_height = HEIGHT // 2
    
    # Draw white's portion (top half if white is winning)
    white_height = int(HEIGHT // 2 - score * (HEIGHT // 2))
    p.draw.rect(screen, WHITE, p.Rect(HEIGHT, 0, EVAL_BAR_WIDTH, white_height))
    
    # Draw black's portion (bottom half is black is winning)
    black_height = HEIGHT - white_height
    p.draw.rect(screen, BLACK, p.Rect(HEIGHT, white_height, EVAL_BAR_WIDTH, black_height))
    
    # Draw center line
    p.draw.line(screen, GRAY, (HEIGHT, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
    
    # Draw evaluation text if significant advantage
    if abs(score) > 0.05:
        advantage = abs(round(score * 10, 1))  # Format as float with 1 decimal place
        color = WHITE if score < 0 else BLACK  # Text color opposite of background
        bg_color = BLACK if score < 0 else WHITE
        font = p.font.SysFont("Arial", 14, True, False)
        text = f"+{advantage}"
        text_obj = font.render(text, True, color)
        text_pos = (HEIGHT + (EVAL_BAR_WIDTH - text_obj.get_width()) // 2, HEIGHT // 2 - 10)
        p.draw.rect(screen, bg_color, (text_pos[0]-2, text_pos[1], text_obj.get_width()+4, text_obj.get_height()))
        screen.blit(text_obj, text_pos)

if __name__ == "__main__":
    main()
