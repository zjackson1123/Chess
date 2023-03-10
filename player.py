

class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = {}
        self.checked = False
        self.drawnCheck = None
    
    def assignPiece(self, piece):
        self.pieces[piece.fullname] = piece

    def getPiece(self, name):
        return self.pieces[self.color + "-" + name]
        
    def handleCheck(self, piece, index, board):
        king = self.getPiece("king-1")
        for name in king.checkedBy.keys():
            for i in king.checkedBy[name]:
                if piece is not king: 
                    if index == i: 
                        return True
                    else:
                        return False
                else:
                    if index == i: 
                        if board.board[index].piece.fullname == name:
                            return True
                        else:
                            return False
                    else:
                        return True
    
        

            
                
            