class ChessPieces():
    class ChessPiece():
        def __init__(self, name, img, color, index):
            self.name = name
            self.img = img
            self.color = color
            self.index = index 
            self.checkCheck = False
            self.inVision = {}

        def showMove(self, board, squaresToMove, moveBy, checkCheck = False):
            index = self.index
            for i in range(squaresToMove):
                index = tuple(map(lambda a,b: a+b, index, moveBy))
                if(board.checkValidMove(index, self)):
                    if(checkCheck):
                        board.inCheck()
                    else:
                        board.board[self.index].shownmoves.append(board.drawMove(index))
                else:
                    break

    class Pawn(ChessPiece):
        def __init__(self, name, img, color, index, firstmove = True):
            super().__init__(name, img, color, index)
            self.firstMove = firstmove
            self.canEnPassant = False

        def showMoves(self, board):
            if(board.turn != self.color):
                return
            if self.color == "bk":
                if not self.firstMove:
                    self.showMove(board, 1, (0,1))
                else:
                    self.showMove(board, 2, (0,1))
            else:
                if not self.firstMove:
                    self.showMove(board, 1, (0,-1))
                else:
                    self.showMove(board, 2, (0,-1))

            board.potentialMove = True
            
        
        def pawnAttack(self, board, checkCheck = False):
            if(board.turn != self.color):
                return

            self.checkCheck = checkCheck
            index = self.index
            Rdiag = None
            Ldiag = None
            if self.color == "bk":
                index = tuple(map(lambda a,b: a+b, index, (1,1)))
                Rdiag = board.board[index]
                index = tuple(map(lambda a,b: a+b, index, (-2,0)))
                Ldiag = board.board[index]
            else:
                index = tuple(map(lambda a,b: a+b, index, (1,-1)))
                Rdiag = board.board[index]
                index = tuple(map(lambda a,b: a+b, index, (-2,0)))
                Ldiag = board.board[index]
                

            if Rdiag.piece is not None and Rdiag.piece.color != self.color:
                x,y = board.pieceCoordinates(Rdiag)
                board.board[self.index].shownmoves.append(board.canvas.create_oval(x-35, y-35, x+35, y+35, fill='', outline="black", width=8))
                Rdiag.canMoveHere = True
            
            if Ldiag.piece is not None and Ldiag.piece.color != self.color  :
                x,y = board.pieceCoordinates(Ldiag)
                board.board[self.index].shownmoves.append(board.canvas.create_oval(x-35, y-35, x+35, y+35, fill='', outline="black", width=8))
                Ldiag.canMoveHere = True
            

    class Bishop(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)

        def showMoves(self, board, checkCheck = False):
            if(board.turn != self.color):
                return

            self.checkCheck = checkCheck
            self.showMove(board, 8, (1,1))
            self.showMove(board, 8, (-1,1))
            self.showMove(board, 8, (-1,-1))
            self.showMove(board, 8, (1,-1))
            board.potentialMove = True

    class Rook(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)
        
        def showMoves(self, board, checkCheck = False):
            if(board.turn != self.color):
                return

            self.checkCheck = checkCheck
            self.showMove(board, 8, (0,1))
            self.showMove(board, 8, (1,0))
            self.showMove(board, 8, (0,-1))
            self.showMove(board, 8, (-1,0))
            board.potentialMove = True

    class Knight(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)

        def showMoves(self, board, checkCheck = False):
            if(board.turn != self.color):
                return

            self.checkCheck = checkCheck
            self.showMove(board, 1, (2,1))
            self.showMove(board, 1, (2,-1))
            self.showMove(board, 1, (-2,1))
            self.showMove(board, 1, (-2,-1))
            self.showMove(board, 1, (1,2))
            self.showMove(board, 1, (1,-2))
            self.showMove(board, 1, (-1,-2))
            self.showMove(board, 1, (-1,2))
            board.potentialMove = True

    class Queen(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)

        def showMoves(self, board, checkCheck = False):
            if(board.turn != self.color):
                return

            self.checkCheck = checkCheck
            self.showMove(board, 8, (1,1))
            self.showMove(board, 8, (1,-1))
            self.showMove(board, 8, (-1,1))
            self.showMove(board, 8, (-1,-1))
            self.showMove(board, 8, (0,1))
            self.showMove(board, 8, (1,0))
            self.showMove(board, 8, (0,-1))
            self.showMove(board, 8, (-1,0))
            board.potentialMove = True

    class King(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)

        def showMoves(self, board, checkCheck = False):
            if(board.turn != self.color):
                return

            self.checkCheck = checkCheck
            self.showMove(board, 1, (1,1))
            self.showMove(board, 1, (1,-1))
            self.showMove(board, 1, (-1,1))
            self.showMove(board, 1, (-1,-1))
            self.showMove(board, 1, (0,1))
            self.showMove(board, 1, (1,0))
            self.showMove(board, 1, (0,-1))
            self.showMove(board, 1, (-1,0))
            board.potentialMove = True