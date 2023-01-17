import tkinter as tk
from tkinter import *
import player
import pieces as p
from PIL import Image,ImageTk
from pathlib import Path

class ChessBoard():
    imageNames = {}

    class BoardSpace():
        def __init__(self, x0, y0, x1, y1):
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1
            self.canMoveHere = False
            self.piece = None
            self.shownmoves = []

        def clearMoves(self):
            for (x,y) in self.board.keys():
                self.board[(x,y)].canMoveHere = False
                for dot in self.board[x,y].shownmoves:
                    self.canvas.delete(dot)
            self.potentialMove = False
            
        def drawSquare(self, board, color):
            square = board.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=color)
            board.canvas.tag_lower(square, self.piece.img)
            
            
            

    def __init__(self, root):
        self.root = root
        self.entry = tk.Entry(root)
        self.canvas = tk.Canvas(root, width = 1080, height = 800, background="#000000")
        self.canvas.bind('<Button-1>', self.clickHandler)
        self.canvas.grid(row=0, column=0)
        self.potentialMove = False
        self.pieceToMove = None
        self.p1 = player.Player("wh")
        self.p2 = player.Player("bk")
        self.turn = self.p1
        self.Checked = False
        frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky="n")
        clr = "#769656"
        lastX = 140
        lastY = 0
        self.board = {}
        for x in range(8):
            lastX += 80
            for y in range(8):
                lastY += 80
                if (x,y) not in self.board.keys():
                    self.canvas.create_rectangle(lastX, lastY, (x+1)*80+220, (y+1)*80+80, fill=clr)
                    self.board[(x, y)] = self.BoardSpace(lastX, lastY, (x+1)*80+220, (y+1)*80+80)
                clr = self.clrSwap(clr) 
            clr = self.clrSwap(clr)
            lastY = 0
        self.addChessPieces()
 
    def clrSwap(self, clr):
        if clr == "#769656":
            return "#baca44"   
        return "#769656"
            
    def addChessPieces(self):
        directory = Path('Chess-Pieces').glob('*.png')
        for imageName in directory:
            if imageName is not self.imageNames.keys():
                self.imageNames[imageName.stem] = ImageTk.PhotoImage(Image.open(imageName.__str__()))
            
        #black pieces
        self.addChessPiece("bk-rook-1", (0,0))
        self.addChessPiece("bk-rook-2", (7,0))
        self.addChessPiece("bk-knight-1", (1,0))
        self.addChessPiece("bk-knight-2", (6,0))
        self.addChessPiece("bk-bishop-1", (2,0))
        self.addChessPiece("bk-bishop-2", (5,0))
        self.addChessPiece("bk-queen-1", (4,4))
        self.addChessPiece("bk-king-1", (4,0))

        #white pieces
        self.addChessPiece("wh-rook-1", (0,7))
        self.addChessPiece("wh-rook-2", (7,7))
        self.addChessPiece("wh-knight-1", (1,7))
        self.addChessPiece("wh-knight-2", (6,7))
        self.addChessPiece("wh-bishop-1", (2,7))
        self.addChessPiece("wh-bishop-2", (5,7))
        self.addChessPiece("wh-queen-1", (3,7))
        self.addChessPiece("wh-king-1", (4,7))

        for i in range(8):
            self.addChessPiece("bk-pawn-" + str(i+1), (i,1))
            self.addChessPiece("wh-pawn-" + str(i+1), (i,6))
        for piece in self.p1.pieces.keys():
            self.p1.pieces[piece].setVision(self)
        for piece in self.p2.pieces.keys():
            self.p2.pieces[piece].setVision(self)

    def addChessPiece(self, name, index):
        name = name.split("-")
        img = self.imageNames[name[0] + "-" + name[1]]
        color = name[0]
        pieceName = name[1]
        id = name[2]
        boardspace = self.board[index]
        newPiece = None
        match pieceName:
            case "rook":
                newPiece = p.ChessPieces.Rook(pieceName, img, color, index, id)
            case "bishop":
                newPiece = p.ChessPieces.Bishop(pieceName, img, color, index, id)
            case "knight":
                newPiece = p.ChessPieces.Knight(pieceName, img, color, index, id)
            case "queen":
                newPiece = p.ChessPieces.Queen(pieceName, img, color, index, id)
            case "king":
                newPiece = p.ChessPieces.King(pieceName, img, color, index, id)
            case "pawn":
                newPiece = p.ChessPieces.Pawn(pieceName, img, color, index, id)
 
        newPiece.img = self.canvas.create_image(self.pieceCoordinates(boardspace), image=img)
        boardspace.piece = newPiece
        if color == "bk":
            self.p2.assignPiece(newPiece)
        else:
            self.p1.assignPiece(newPiece)

    def drawMove(self, index, pieceIndex):
        moveToDraw = self.board[index]
        if(moveToDraw.x0 >= 220 and moveToDraw.y0 >= 80 and moveToDraw.x1 <= 860 and moveToDraw.y1 <= 720):
            x,y = self.pieceCoordinates(moveToDraw)
            drawnMove = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="black")
            moveToDraw.canMoveHere = True
            self.potentialMove = True
            boardspace = self.board[pieceIndex]
            self.pieceToMove = boardspace.piece
            boardspace.shownmoves.append(drawnMove)

    def drawAttack(self, index, pieceIndex):
        boardspace = self.board[pieceIndex]
        atkToDraw = self.board[index]
        if boardspace.piece.color == atkToDraw.piece.color:
            return
        x,y = self.pieceCoordinates(atkToDraw)
        drawnAtk = self.canvas.create_oval(x-35, y-35, x+35, y+35, fill='', outline="black", width=8)
        atkToDraw.canMoveHere = True
        self.potentialMove = True
        self.pieceToMove = boardspace.piece
        boardspace.shownmoves.append(drawnAtk)
            
    def inBoard(self, index):
        if index[0] < 0 or index[0] > 7 or index[1] < 0 or index[1] > 7:
            return False
        return True

    def pieceCoordinates(self, boardSpace):
        if(boardSpace != None):
            x = (boardSpace.x0+boardSpace.x1)/2
            y = (boardSpace.y0+boardSpace.y1)/2
            return x,y
        return None

    def clickHandler(self, event):
        if not self.potentialMove:
            self.BoardSpace.clearMoves(self)
            for (x,y) in self.board.keys():
                boardspace = self.board[(x,y)]
                if(boardspace.x0 < event.x and boardspace.x1 > event.x and boardspace.y0 < event.y and boardspace.y1 > event.y and boardspace.piece is not None):                      
                    boardspace.piece.showMoves(self)
        else:
            self.checkPotentialMove(event)

    def checkPotentialMove(self, event):
        for (x,y) in self.board.keys():
            boardspace = self.board[(x,y)]
            if(boardspace.x0 < event.x and boardspace.x1 > event.x and boardspace.y0 < event.y and boardspace.y1 > event.y):
                if boardspace.canMoveHere:
                    self.makeMove((x,y))
                    break
        self.potentialMove = False
        self.BoardSpace.clearMoves(self)
    
    def makeMove(self, index):
        boardspace = self.board[index]
        if boardspace.piece is not None:
            self.canvas.delete(boardspace.piece.img)
        self.updatePiece(index)
        self.pieceToMove.setVision(self)
        self.potentialMove = False
        self.BoardSpace.clearMoves(self)
        self.turnChange()
        
    def updatePiece(self, index):
        self.board[self.pieceToMove.index].piece = None
        self.pieceToMove.index = index
        self.canvas.delete(self.pieceToMove.img)
        img = self.imageNames[self.pieceToMove.color+"-"+self.pieceToMove.name]
        self.pieceToMove.img = self.canvas.create_image(self.pieceCoordinates(self.board[index]), image=img)
        self.board[index].piece = self.pieceToMove

    def turnChange(self):
        if(self.turn == self.p1):
            self.turn = self.p2
        else:
            self.turn = self.p1