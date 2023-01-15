class ChessPieces():
    class ChessPiece():
        def __init__(self, name, img, color, index, id):
            self.name = name
            self.id = id
            self.img = img
            self.color = color
            self.index = index
            self.fullname = color + "-" + name + "-" + str(id)
            self.inVision = []
            self.moveRules = []

        def showMove(self, board, squaresToMove, setVision = False):
            for moveBy in self.moveRules:
                index = self.index
                for i in range(squaresToMove):
                    index = tuple(map(lambda a,b: a+b, index, moveBy))
                    if(board.checkValidMove(index, self)):
                        if setVision:
                            self.addVision(board, index)
                            #board.board[self.index].piece.hasVision.append(index)
                        else:
                            board.board[self.index].shownmoves.append(board.drawMove(index))
                    else:
                        break
                    
        def addVision(self, board, index):
            self.inVision.append(index)
            piece = board.board[index].piece
            
            if piece is not None and piece.name == "king" and piece.color != self.color:
                piece.checked(board, index)
                    
    #make hasVision piece specific, a list of indices of squares that piece has vision of, like originally planned
    #if boardspace.piece.name == king, check if showmoves could put the piece on a square that would break the check, or move the king out of check
    #otherwise, don't show that move, e

    class Pawn(ChessPiece):
        def __init__(self, name, img, color, index, id, firstmove = True):
            super().__init__(name, img, color, index, id)
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
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((1, 1), (-1, 1), (-1, -1), (1, -1)))

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 8, setVision)
            board.potentialMove = True

    class Rook(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((0, 1), (1, 0), (0, -1), (-1, 0)))
        
        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 8, setVision)
            board.potentialMove = True

    class Knight(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)))

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 1, setVision)
            board.potentialMove = True

    class Queen(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((1,1), (1,-1), (-1,1), (-1,-1), (0, 1), (1, 0), (0, -1), (-1, 0)))

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return

            self.showMove(board, 8, setVision)
            board.potentialMove = True

    class King(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((1,1), (1,-1), (-1,1), (-1,-1), (0,1), (1,0), (0,-1), (-1,0)))
            self.checkedBy = {}

        def showMoves(self, board, setVision = False):
            if(board.turn != self.color):
                return
            self.showMove(board, 1, setVision)
            board.potentialMove = True
            
        def checked(self, index, piece):
            if piece.fullname not in self.checkedBy.keys():                
                self.checkedBy[piece.fullname] = []
            
            self.checkedBy[piece.fullname].append(index)
            
            