

class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = {}
        self.checked = False
    
    def assignPiece(self, piece):
        self.pieces[piece.name + "-" + piece.id] = piece
        
    def handleCheck(self, index):
        king = self.pieces["king-1"]
        for name in king.checkedBy.keys():
            for i in king.checkedBy[name]:
                if index == i:
                    return True
        return False
            
                
            