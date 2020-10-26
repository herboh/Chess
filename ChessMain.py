#User Input and validation
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 #max of res
DIMENSION = 8 #Dimensions of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #animations
IMAGES = {}

#create dictionary of images. wikimedia commons
def loadImages():
    pieces = ['wP', 'bP', 'wN', 'wB', 'wK', 'wQ', 'wR','bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#Main Loop of Game
def main ():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made

    loadImages()#Load once, move images around
    running = True
    sqSelected = () #Intial selection is empty, tracks last click of user (row, col)
    playerClicks = [] #list with 2 tuples: [(6, 5), (4, 4)] pawn move tracked
    while running:
        for e in p.event.get():
            if e.type == p.QUIT: #exit strategy
                running = FALSE
                #MouseFunctions
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  #Where is the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #this clears the selection after a 2nd click on a square
                    sqSelected = ()
                    Playerclicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #Make a move on the second unique click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #reset the click count
                    playerClicks = []
                #Key functions
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when keyboard z is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            movemade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
#Creates graphics on the Board
def drawGameState(screen, gs):
    drawBoard(screen) #squares on the board
    drawPieces(screen, gs. board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range (DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen,  board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #Check if square is empty
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
