import chessboard as cb

class ChessPieces():
    class ChessPiece():
        def __init__(self, name, img, color, index):
            self.name = name
            self.img = img
            self.color = color
            self.index = index
            self.hashPiece()

        def hashPiece(self):
            cb.ChessBoard.pieceArr.append(self)

        def showMoves(self, board):
            return cb.ChessBoard.board[self.index]

    class Pawn(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)
            self.firstMove = True
            self.canEnPassant = False

        def showMoves(self, board):
            currentPos = super().showMoves(board)
            currentPos.shownmoves.append(board.drawDot( self.index+1, self))
            if self.firstMove:
                currentPos.shownmoves.append(board.drawDot(self.index+2, self))

    class Bishop(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)

        def showMoves(self, board):
            currentPos = super().showMoves(board)
            for i in range(8):
                currentPos.shownmoves.append(board.drawDot(self.index+(i*8)+9))
                currentPos.shownmoves.append(board.drawDot(self.index+(i*8)-7))
                currentPos.shownmoves.append(board.drawDot(self.index+(i*8)-9))
                currentPos.shownmoves.append(board.drawDot(self.index+(i*8)+7))

    class Rook(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)
        
        def showMoves(self):
            currentPos = super().showMoves()
            for i in range(8):
                currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+(i*8)))
                currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+i))

    class Knight(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)

        def showMoves(self):
            currentPos = super().showMoves()
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+17))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-15))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+10))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-6))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+15))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-17))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+6))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-10))

    class Queen(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)

        def showMoves(self):
            currentPos = super().showMoves()
            for i in range(8):
                currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+(i*8)+9))
                currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+(i*8)-7))
                currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+(i*8)-9))
                currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+(i*8)+7))
                currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+(i*8)))
                currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+i))

    class King(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)

        def showMoves(self):
            currentPos, piece = super().showMoves()
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+1, piece))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-1, piece))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-8, piece))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-8, piece))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+9, piece))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-7, piece))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index-9, piece))
            currentPos.shownmoves.append(cb.ChessBoard.drawDot(self.index+7, piece))