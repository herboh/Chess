#Store Game Information and current State. Decide if moves are legal. Keep a log of moves.
class GameState():
    def __init__(self):
        #Create 8x8 2d list w/ 2 characters
        #Pieces w or b king (K) queen (Q) bishop (B) knight (N) rook (R) self.board = [ ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"], ["--", "--", "--", "--", "--", "--", "--", "--"],
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        # Castling rights
        self.whiteCastleKingside = True
        self.whiteCastleQueenside = True
        self.blackCastleKingside = True
        self.blackCastleQueenside = True
        self.castleRightsLog = [(True, True, True, True)]  # Log to track castling rights history
        # En passant possibility
        self.enpassantPossible = () # coordinates for the square where en passant capture is possible
        # Pawn promotion
        self.pawnPromotion = False
        self.promotionChoice = 'Q' # Default promotion to queen
        # Game state tracking
        self.checkmate = False
        self.stalemate = False

    def makeMove(self, move, checkForGameEnd=True):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move
        
        # Update king's position if king moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
            
        # Handle pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + self.promotionChoice
            self.pawnPromotion = False
            
        # Handle en passant captures
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"  # Capturing the pawn
            
        # Update en passant possibility
        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()
            
        # Handle castling move
        if move.isCastleMove:
            # Kingside castle (move right)
            if move.endCol - move.startCol == 2:
                # Move the rook from the corner to beside the king
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"
            # Queenside castle (move left)
            else:
                # Move the rook from the corner to beside the king
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"
                
        # Update castling rights
        self.updateCastleRights(move)
        
        self.whiteToMove = not self.whiteToMove #swap turns
        
        # Check for checkmate or stalemate only when actually making a real move
        # not when validating potential moves
        if checkForGameEnd:
            self.checkmate = self.isCheckmate()
            self.stalemate = self.isStalemate()
        
    def undoMove(self):
        if len(self.moveLog) != 0: #check that a move has been made
            move = self.moveLog.pop() # function to remove one from the list
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            
            # Update king's position
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
                
            # Undo en passant captures
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"  # Empty the end square
                self.board[move.startRow][move.endCol] = move.pieceCaptured  # Put captured pawn back
                self.enpassantPossible = (move.endRow, move.endCol)
                
            # Undo a 2 square pawn advance
            if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
                
            # Undo castling rights
            if move.isCastleMove:
                # Kingside castle (move right)
                if move.endCol - move.startCol == 2:
                    # Move the rook back
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                # Queenside castle (move left)
                else:
                    # Move the rook back
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"
                    
            # Restore castling rights
            self.castleRightsLog.pop()
            castleRights = self.castleRightsLog[-1]
            self.whiteCastleKingside = castleRights[0]
            self.whiteCastleQueenside = castleRights[1]
            self.blackCastleKingside = castleRights[2]
            self.blackCastleQueenside = castleRights[3]
            
            # Reset checkmate and stalemate flags
            self.checkmate = False
            self.stalemate = False
            
            self.whiteToMove = not self.whiteToMove #Other players turn
    def updateCastleRights(self, move):
        # Save current state of castling rights to log
        currentRights = (self.whiteCastleKingside, self.whiteCastleQueenside,
                         self.blackCastleKingside, self.blackCastleQueenside)
        self.castleRightsLog.append(currentRights)
        
        # Check if king moved
        if move.pieceMoved == "wK":
            self.whiteCastleKingside = False
            self.whiteCastleQueenside = False
        elif move.pieceMoved == "bK":
            self.blackCastleKingside = False
            self.blackCastleQueenside = False
            
        # Check if rook was moved
        if move.pieceMoved == "wR":
            if move.startRow == 7:  # White rook
                if move.startCol == 0:  # Queenside rook
                    self.whiteCastleQueenside = False
                elif move.startCol == 7:  # Kingside rook
                    self.whiteCastleKingside = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:  # Black rook
                if move.startCol == 0:  # Queenside rook
                    self.blackCastleQueenside = False
                elif move.startCol == 7:  # Kingside rook
                    self.blackCastleKingside = False
                    
        # Check if rook was captured
        if move.pieceCaptured == "wR":
            if move.endRow == 7:
                if move.endCol == 0:  # White queenside rook captured
                    self.whiteCastleQueenside = False
                elif move.endCol == 7:  # White kingside rook captured
                    self.whiteCastleKingside = False
        elif move.pieceCaptured == "bR":
            if move.endRow == 0:
                if move.endCol == 0:  # Black queenside rook captured
                    self.blackCastleQueenside = False
                elif move.endCol == 7:  # Black kingside rook captured
                    self.blackCastleKingside = False

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = (self.whiteCastleKingside, self.whiteCastleQueenside,
                           self.blackCastleKingside, self.blackCastleQueenside)
        
        # Get all possible moves
        moves = self.getAllPossibleMoves()
        movesToRemove = []
        
        # For each move, make the move and see if it puts/leaves the king in check
        for i in range(len(moves) - 1, -1, -1):  # Remove moves that put king in check
            self.makeMove(moves[i], checkForGameEnd=False)  # Don't check for game end during validation
            self.whiteToMove = not self.whiteToMove  # Switch to opponent's turn
            inCheck = self.inCheck()
            if inCheck:  # If the move puts/leaves the king in check, mark for removal
                movesToRemove.append(moves[i])
            self.whiteToMove = not self.whiteToMove  # Switch back
            self.undoMove()
            
        # Remove invalid moves
        for move in movesToRemove:
            if move in moves:
                moves.remove(move)
            
        # Restore original en passant and castling rights
        self.enpassantPossible = tempEnpassantPossible
        self.whiteCastleKingside, self.whiteCastleQueenside, self.blackCastleKingside, self.blackCastleQueenside = tempCastleRights
        
        # Check for checkmate or stalemate
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
            
        return moves

    def getAllPossibleMoves(self):
        moves = [] #empty list of moves
        for r in range(len(self.board)): ##number of rows
            for c in range(len(self.board[r])): ##number of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): ##check piece color and if it is their turn
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #calls the correct move per piece
        return moves


    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            # Normal forward move
            if self.board[r-1][c] == "--": # move white pawn up the board one if it is empty
                moves.append(Move((r, c), (r-1, c), self.board)) #empty list that we are adding moves to
                # Two square move from starting position
                if r == 6 and self.board[r-2][c] == "--": #check pawn is in start row and can move 2 ahead
                    moves.append(Move((r, c), (r-2, c), self.board))
            
            # Captures to the left
            if c-1 >= 0:
                if self.board[r-1][c-1][0] =='b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                # En passant capture to the left
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
                    
            # Captures to the right
            if c+1 <= 7: 
                if self.board[r-1][c+1][0] =='b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                # En passant capture to the right
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))

        else: #black pawn moves
            # Normal forward move
            if self.board[r+1][c] == "--": # move black pawn down the board one if it is empty
                moves.append(Move((r, c), (r+1, c), self.board)) #empty list that we are adding moves to
                # Two square move from starting position
                if r == 1 and self.board[r+2][c] == "--": #check pawn is in start row and can move 2 ahead
                    moves.append(Move((r, c), (r+2, c), self.board))
            
            # Captures to the left
            if c-1 >= 0:
                if self.board[r+1][c-1][0] =='w': #enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                # En passant capture to the left
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
                    
            # Captures to the right
            if c+1 <= 7: 
                if self.board[r+1][c+1][0] =='w': #enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                # En passant capture to the right
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    def getRookMoves(self,r ,c, moves):
        directions = ((-1,0), (0,1), (1,0), (0,-1)) #up / left / down / right
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
        self.getBishopMoves(r, c , moves)
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0,1), (1, -1), (1,0), (1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))
                    
        # Castling moves
        self.getCastleMoves(r, c, moves, allyColor)
                    
    def getCastleMoves(self, r, c, moves, allyColor):
        # If king is in check, can't castle
        if self.inCheck():
            return
            
        # Kingside castle
        if (self.whiteToMove and self.whiteCastleKingside) or (not self.whiteToMove and self.blackCastleKingside):
            self.getKingsideCastleMoves(r, c, moves, allyColor)
            
        # Queenside castle
        if (self.whiteToMove and self.whiteCastleQueenside) or (not self.whiteToMove and self.blackCastleQueenside):
            self.getQueensideCastleMoves(r, c, moves, allyColor)
            
    def getKingsideCastleMoves(self, r, c, moves, allyColor):
        # Check if squares between king and rook are empty
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            # Check if king passes through or ends up on an attacked square
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))
                
    def getQueensideCastleMoves(self, r, c, moves, allyColor):
        # Check if squares between king and rook are empty
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            # Check if king passes through or ends up on an attacked square
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))
                
    def isCheckmate(self):
        if not self.inCheck():
            return False
            
        # Get valid moves but don't recursively check for checkmate/stalemate
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = (self.whiteCastleKingside, self.whiteCastleQueenside,
                           self.blackCastleKingside, self.blackCastleQueenside)
        
        moves = self.getAllPossibleMoves()
        movesToRemove = []
        
        for move in moves:
            self.makeMove(move, checkForGameEnd=False)
            self.whiteToMove = not self.whiteToMove
            inCheck = self.inCheck()
            if inCheck:
                movesToRemove.append(move)
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            
        for move in movesToRemove:
            if move in moves:
                moves.remove(move)
                
        # Restore original en passant and castling rights
        self.enpassantPossible = tempEnpassantPossible
        self.whiteCastleKingside, self.whiteCastleQueenside, self.blackCastleKingside, self.blackCastleQueenside = tempCastleRights
        
        return len(moves) == 0
        
    def isStalemate(self):
        if self.inCheck():
            return False
            
        # Get valid moves but don't recursively check for checkmate/stalemate
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = (self.whiteCastleKingside, self.whiteCastleQueenside,
                           self.blackCastleKingside, self.blackCastleQueenside)
        
        moves = self.getAllPossibleMoves()
        movesToRemove = []
        
        for move in moves:
            self.makeMove(move, checkForGameEnd=False)
            self.whiteToMove = not self.whiteToMove
            inCheck = self.inCheck()
            if inCheck:
                movesToRemove.append(move)
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            
        for move in movesToRemove:
            if move in moves:
                moves.remove(move)
                
        # Restore original en passant and castling rights
        self.enpassantPossible = tempEnpassantPossible
        self.whiteCastleKingside, self.whiteCastleQueenside, self.blackCastleKingside, self.blackCastleQueenside = tempCastleRights
        
        return len(moves) == 0
        
    def isDraw(self):
        # Check for 50 move rule and threefold repetition
        return self.isStalemate() or self.isFiftyMove() or self.isThreefoldRepetition()
        
    def isFiftyMove(self):
        # TODO: Implement 50 move rule
        return False
        
    def isThreefoldRepetition(self):
        # TODO: Implement threefold repetition
        return False
        
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
            
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to opponent's turn
        
        # Check for attacks by pawns
        if self.whiteToMove:  # Looking for white pawn attacks
            if 0 <= r+1 < 8 and 0 <= c-1 < 8 and self.board[r+1][c-1] == 'wP':
                self.whiteToMove = not self.whiteToMove
                return True
            if 0 <= r+1 < 8 and 0 <= c+1 < 8 and self.board[r+1][c+1] == 'wP':
                self.whiteToMove = not self.whiteToMove
                return True
        else:  # Looking for black pawn attacks
            if 0 <= r-1 < 8 and 0 <= c-1 < 8 and self.board[r-1][c-1] == 'bP':
                self.whiteToMove = not self.whiteToMove
                return True
            if 0 <= r-1 < 8 and 0 <= c+1 < 8 and self.board[r-1][c+1] == 'bP':
                self.whiteToMove = not self.whiteToMove
                return True
                
        # Check for knight attacks
        knightMoves = ((-2,-1), (-2, 1), (-1, -2), (-1, 2), (1,-2), (1,2), (2,-1),(2,1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == ('w' if self.whiteToMove else 'b') and endPiece[1] == 'N':
                    self.whiteToMove = not self.whiteToMove
                    return True
                    
        # Check for rook/queen attacks in straight lines
        directions = ((-1,0), (0,1), (1,0), (0,-1))  # up, right, down, left
        enemyColor = 'w' if self.whiteToMove else 'b'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Empty square, keep checking
                        continue
                    if endPiece[0] == enemyColor and (endPiece[1] == 'R' or endPiece[1] == 'Q'):
                        self.whiteToMove = not self.whiteToMove
                        return True
                    break  # Blocked by a piece that can't attack in this direction
                else:
                    break  # Off the board
                    
        # Check for bishop/queen attacks in diagonal lines
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))  # diagonals
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Empty square, keep checking
                        continue
                    if endPiece[0] == enemyColor and (endPiece[1] == 'B' or endPiece[1] == 'Q'):
                        self.whiteToMove = not self.whiteToMove
                        return True
                    break  # Blocked by a piece that can't attack in this direction
                else:
                    break  # Off the board
                    
        # Check for king attacks (adjacent squares)
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'K':
                    self.whiteToMove = not self.whiteToMove
                    return True
                    
        self.whiteToMove = not self.whiteToMove  # switch turns back
        return False


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,#Dictionaries to map rank and file
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}#Reverses the dictionary
    filesToCols = {"a": 0, "b":1, "c": 2, "d": 3,
                   "e":4, "f": 5, "g": 6, "h": 7}
    colsToFiles = { v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] #Tracks all the details about a move for the log
        
        # Pawn promotion
        self.isPawnPromotion = (self.pieceMoved[1] == 'P' and 
                               ((self.endRow == 0 and self.pieceMoved[0] == 'w') or 
                                (self.endRow == 7 and self.pieceMoved[0] == 'b')))
                                
        # En passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved[0] == 'b' else 'bP'
            
        # Castle move
        self.isCastleMove = isCastleMove
        
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
    def getChessNotation(self):
        # Get basic move notation
        if self.isCastleMove:
            if self.endCol - self.startCol == 2:  # Kingside castle
                return "O-O"
            else:  # Queenside castle
                return "O-O-O"
        
        moveNotation = ""
        if self.pieceMoved[1] != 'P':
            moveNotation += self.pieceMoved[1]
            
        if self.pieceCaptured != "--":
            if self.pieceMoved[1] == 'P':
                moveNotation += self.colsToFiles[self.startCol]
            moveNotation += 'x'
            
        moveNotation += self.getRankFile(self.endRow, self.endCol)
        
        # Add promotion piece
        if self.isPawnPromotion:
            moveNotation += "=Q"  # Default to queen promotion
            
        return moveNotation
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
