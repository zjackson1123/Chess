class ChessPieces():
    class ChessPiece():
        def __init__(self, name, img, color, index, id):
            self.name = name
            self.id = id
            self.img = img
            self.color = color
            self.index = index
            self.fullname = color + "-" + name + "-" + str(id)
            self.onBoard = True
            self.inVision = {}
            self.moveBy = 0
            self.moveRules = []
            
        def showMoves(self, board):
            if board.turn.color != self.color:
                return              
            for dictIndex in self.inVision.keys():
                for index in self.inVision[dictIndex]:
                    if board.turn.checked and not board.turn.handleCheck(self, index, board):
                        break
                    if board.board[index].piece is not None:
                        board.drawAttack(index, self.index)
                        break
                    board.drawMove(index, self.index)    
                    board.potentialMove = True
                    
                        
        def setVision(self, board):
            if not self.onBoard:
                return
            i = 0
            for moveRule in self.moveRules:
                index = self.index
                indices = []
                for x in range(self.moveBy):
                    index = tuple(map(lambda a,b: a+b, index, moveRule))
                    if not board.inBoard(index):
                        break
                    indices.append(index)          
                self.addVision(board, indices, i)
                i += 1
                    
        def addVision(self, board, indices, dictIndex): 
            self.inVision[dictIndex] = {}
            for index in indices:
                piece = board.board[index].piece
                if piece is not None:
                    self.inVision[dictIndex][index] = piece            
                    if piece.name == "king" and piece.color != self.color:
                        piece.checked(indices, self, board)
                else:
                    self.inVision[dictIndex][index] = None

    class Pawn(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.canEnPassant = False
            self.moveBy = 2
            self.atkBy = 1
            if color == "bk":
                self.moveRules.extend(((0,1), (1,1), (-1,1)))
            else:
                self.moveRules.extend(((0,-1), (1,-1), (-1,-1))) 

        def showMoves(self, board):
            if board.turn.color != self.color:
                return              
            for dictIndex in self.inVision.keys():
                for index in self.inVision[dictIndex]:
                    if dictIndex < 1:   
                        if board.turn.checked and not board.turn.handleCheck(self, index, board):
                            break
                        if board.board[index].piece is not None:
                            break
                        board.drawMove(index, self.index)
                    else:
                        if board.turn.checked and not board.turn.handleCheck(self, index, board):
                            break
                        if board.board[index].piece is not None: 
                            board.drawAttack(index, self.index)
                    
        def setVision(self, board):
            i = 0
            for moveRule in self.moveRules:
                index = self.index
                indices = []
                if i < 1:
                    for x in range(self.moveBy):
                        index = tuple(map(lambda a,b: a+b, index, moveRule))
                        if not board.inBoard(index):
                            break
                        indices.append(index)
                    self.addVision(board, indices, i)
                    i += 1
                else:
                    index = tuple(map(lambda a,b: a+b, index, moveRule))
                    if board.inBoard(index):
                        indices.append(index)
                    self.addVision(board, indices, i)
                    i += 1                      
                           
    class Bishop(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((1, 1), (-1, 1), (-1, -1), (1, -1)))
            self.moveBy = 7

    class Rook(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((0, 1), (1, 0), (0, -1), (-1, 0)))
            self.moveBy = 7

    class Knight(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)))
            self.moveBy = 1

    class Queen(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((1,1), (1,-1), (-1,1), (-1,-1), (0, 1), (1, 0), (0, -1), (-1, 0)))
            self.moveBy = 7

    class King(ChessPiece):
        def __init__(self, name, img, color, index, id):
            super().__init__(name, img, color, index, id)
            self.moveRules.extend(((1,1), (1,-1), (-1,1), (-1,-1), (0,1), (1,0), (0,-1), (-1,0)))
            self.moveBy = 1
            self.canCheck = {}
            self.checkedBy = {}
            
        def showMoves(self, board):
            if board.turn.color != self.color:
                return              
            for dictIndex in self.inVision.keys():
                for index in self.inVision[dictIndex]:
                    if board.turn.checked and not board.turn.handleCheck(self, index, board):
                        break
                    if board.board[index].piece is not None:
                        board.drawAttack(index, self.index)
                        break
                    board.drawMove(index, self.index)    
                    board.potentialMove = True
            
        def checked(self, indices, atkPiece, board):             
            self.canCheck[atkPiece.fullname] = indices
            self.checkedBy[atkPiece.fullname] = []

            for index in self.canCheck[atkPiece.fullname]:
                piece = board.board[index].piece
                if piece is not None:
                    if piece.name == "king":
                        self.checkedBy[atkPiece.fullname] = indices
                        self.checkedBy[atkPiece.fullname].append(atkPiece.index)  
                        self.checkedBy[atkPiece.fullname].remove(piece.index)
                        board.board[index].drawSquare(board, "red")   
                        board.check(piece.color)
                    else:
                        break
                
                
