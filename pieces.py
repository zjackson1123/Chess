#how to handle checkvalidmove conflict with invision checking
class ChessPieces():
    class ChessPiece():
        def __init__(self, name, img, color, index):
            self.name = name
            self.img = img
            self.color = color
            self.index = index
            self.moveRules = []

        def showMove(self, board, squaresToMove, setVision = False):
            for moveBy in self.moveRules:
                index = self.index
                for i in range(squaresToMove):
                    index = tuple(map(lambda a,b: a+b, index, moveBy))
                    if(board.checkValidMove(index, self)):
                        if setVision:
                            board.board[self.index].inVision.append(index)
                        else:
                            board.board[self.index].shownmoves.append(board.drawMove(index))
                    else:
                        break

    class Pawn(ChessPiece):
        def __init__(self, name, img, color, index, firstmove = True):
            super().__init__(name, img, color, index)
            self.firstMove = firstmove
            self.canEnPassant = False
            if color == "bk":
                self.moveRules.append((0,1))
            else:
                self.moveRules.append((0,-1))

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return
            if not self.firstMove:
                self.showMove(board, 1, setVision)
            else:
                self.showMove(board, 2, setVision)

            board.potentialMove = True
            
    class Bishop(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)
            self.moveRules.extend(((1, 1), (-1, 1), (-1, -1), (1, -1)))

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 8, setVision)
            board.potentialMove = True

    class Rook(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)
            self.moveRules.extend(((0, 1), (1, 0), (0, -1), (-1, 0)))
        
        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 8, setVision)
            board.potentialMove = True

    class Knight(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)
            self.moveRules.extend(((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)))

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 1, setVision)
            board.potentialMove = True

    class Queen(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)
            self.moveRules.extend(((1,1), (1,-1), (-1,1), (-1,-1), (0, 1), (1, 0), (0, -1), (-1, 0)))

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 8, setVision)
            board.potentialMove = True

    class King(ChessPiece):
        def __init__(self, name, img, color, index):
            super().__init__(name, img, color, index)
            self.moveRules.extend(((1,1), (1,-1), (-1,1), (-1,-1), (0,1), (1,0), (0,-1), (-1,0)))

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 1, setVision)
            board.potentialMove = True