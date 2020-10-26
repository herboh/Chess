#Store Game Information and current State. Decide if moves are legal. Keep a log of moves.
class GameState():
    def __init__(self):
        #Create 8x8 2d list w/ 2 characters
        #Pieces w or b king (K) queen (Q) bishop (B) knight (N) rook (R) self.board = [ ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"], ["--", "--", "--", "--", "--", "--", "--", "--"],
        self.board = [
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self. getQueenMoves}
        self.whiteToMove = True
        self.moveLog = []


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move
        self.whiteToMove = not self.whiteToMove #swap turns
    def undoMove(self):
        if len(self.moveLog) != 0: #check that a move has been made
            move = self.moveLog.pop() # function to remove one from the list
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Other players turn
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves =[] #empty list of moves
        for r in range(len(self.board)): ##number of rows
            for c in range(len(self.board[r])): ##number of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): ##check piece color and if it is their turn
                    piece = self.board[r][c][1]
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #calls the correct move per piece
        return moves


    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": # move white pawn up the board one if it is empty
                moves.append(Move((r, c), (r-1, c), self.board)) #empty list that we are adding moves to
                if r == 6 and self.board[r-2][c] == "--": #check pawn is in start row and can move 2 ahead
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] =='b': #2 square pawn advance
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: #capture to the right
                if self.board[r-1][c+1][0] =='b': #enemy piece to capture
                    move.append(Move((r, c), (r-1, c+1), self.board))

            else: #black pawn moves
                if self.board[r+1][c] == "--": # move black pawn down the board one if it is empty
                    moves.append(Move((r, c), (r+1, c), self.board)) #empty list that we are adding moves to
                    if r == 1 and self.board[r+2][c] == "--": #check pawn is in start row and can move 2 ahead
                        moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] =='w': #2 square pawn advance
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: #capture to the right
                if self.board[r+1][c+1][0] =='w': #enemy piece to capture
                    move.append(Move((r, c), (r+1, c+1), self.board))
            #missing pawn promotions

    def getRookMoves(self,r ,c, moves):
        directions = ((-1,0), (0,1), (1,0), (0,1)) #up / left / down / right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #check for empy
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #check enemy piece (first in list)
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break #breaks loop and checks another direction
                    else:
                        break #can't capture friendly piece pr jump a piece
                else:
                    break #not on the board


    def getKnightMoves(self,r ,c, moves):
        knightMoves = ((-2,-1), (-2, 1), (-1, -2), (-1, 2), (1,-2), (1,2), (2,-1),(2,1)) #only concern is this list. no iterate or running into piece
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow <8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece [0] != allyColor:
                    moves.append(Move((r,c), (endRow,endCol),self.board))

    def getBishopMoves(self,r ,c, moves):
        directions = ((-1,-1), (-1, 1), (1,-1), (1,1)) #1:1 movement = diagonal. Top Left / Top Right / Bottom Left / Bottom Right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #max of 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow  < 8 and 0 <= endCol < 8: #on board?
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break #friendly piece
                else:
                    break #off board

    def getQueenMoves(self,r ,c, moves):
        self.getRookMoves(r, c, moves)
        self.getBihopMoves(r, c , moves)

    def getKingMoves(self,r ,c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0,1), (1, -1), (1,0), (1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,#Dictionaries to map rank and file
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}#Reverses the dictionary
    filesToCols = {"a": 0, "b":1, "c": 2, "d": 3,
                   "e":4, "f": 5, "g": 6, "h": 7}
    colsToFiles = { v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] #Tracks all the details about a move for the log
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
