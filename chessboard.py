import tkinter as tk
from tkinter import *
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

    def __init__(self, root):
        self.root = root
        self.entry = tk.Entry(root)
        self.canvas = tk.Canvas(root, width = 1080, height = 800, background="#000000")
        self.canvas.bind('<Button-1>', self.clickHandler)
        self.canvas.grid(row=0, column=0)
        self.potentialMove = False
        self.pieceToMove = None
        self.turn = "wh"
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
            clr = "#baca44"
        else:
            clr = "#769656"
        return clr
            
    def addChessPieces(self):
        directory = Path('Chess-Pieces').glob('*.png')
        for imageName in directory:
            if imageName is not self.imageNames.keys():
                self.imageNames[imageName.stem] = ImageTk.PhotoImage(Image.open(imageName.__str__()))
            
        #black pieces
        self.addChessPiece("bk-rook", (0,0))
        self.addChessPiece("bk-rook", (7,0))
        self.addChessPiece("bk-knight", (1,0))
        self.addChessPiece("bk-knight", (6,0))
        self.addChessPiece("bk-bishop", (2,0))
        self.addChessPiece("bk-bishop", (5,0))
        self.addChessPiece("bk-queen", (4,4))
        self.addChessPiece("bk-king", (4,0))

        #white pieces
        self.addChessPiece("wh-rook", (0,7))
        self.addChessPiece("wh-rook", (7,7))
        self.addChessPiece("wh-knight", (1,7))
        self.addChessPiece("wh-knight", (6,7))
        self.addChessPiece("wh-bishop", (2,7))
        self.addChessPiece("wh-bishop", (5,7))
        self.addChessPiece("wh-queen", (3,7))
        self.addChessPiece("wh-king", (4,7))

        for i in range(8):
            self.addChessPiece("bk-pawn", (i,1))
            self.addChessPiece("wh-pawn", (i,6))

    def addChessPiece(self, name, index, firstmove = True):
        img = self.imageNames[name]
        color = name.split("-")[0]
        pieceName = name.split("-")[1]
        boardspace = self.board[index]
        newPiece = None
        match pieceName:
            case "rook":
                newPiece = p.ChessPieces.Rook(pieceName, img, color, index)
            case "bishop":
                newPiece = p.ChessPieces.Bishop(pieceName, img, color, index)
            case "knight":
                newPiece = p.ChessPieces.Knight(pieceName, img, color, index)
            case "queen":
                newPiece = p.ChessPieces.Queen(pieceName, img, color, index)
            case "king":
                newPiece = p.ChessPieces.King(pieceName, img, color, index)
            case "pawn":
                newPiece = p.ChessPieces.Pawn(pieceName, img, color, index, firstmove)
 
        newPiece.img = self.canvas.create_image(self.pieceCoordinates(boardspace), image=img)
        boardspace.piece = newPiece

    def drawMove(self, i):
        moveToDraw = self.board[i]
        if(moveToDraw.x0 >= 80 and moveToDraw.y0 >= 220 and moveToDraw.x1 <= 860 and moveToDraw.y1 <= 720):
            x,y = self.pieceCoordinates(moveToDraw)
            drawnMove = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="black")
            moveToDraw.canMoveHere = True
            return drawnMove

    def drawAttack(self, atkToDraw):
        x,y = self.pieceCoordinates(atkToDraw)
        drawnAtk = self.canvas.create_oval(x-35, y-35, x+35, y+35, fill='', outline="black", width=8)
        return drawnAtk

    def checkValidMove(self, index, piece):
        if index[0] < 0 or index[0] > 7 or index[1] < 0 or index[1] > 7:
            return False

        boardSpace = self.board[index]
        if boardSpace.piece is not None:

            if boardSpace.piece.color == piece.color:
                return False

            boardSpace.canMoveHere = True
            if piece.color != boardSpace.piece.color:
                if piece.name == "pawn":
                    boardSpace.canMoveHere = False
                    piece.pawnAttack(self)
                else:
                    self.board[piece.index].shownmoves.append(self.drawAttack(boardSpace))           
                return False
        else:    
            return True
  

    def pieceCoordinates(self, boardSpace):
        if(boardSpace != None):
            x = (boardSpace.x0 +boardSpace.x1)/2
            y = (boardSpace.y0 +boardSpace.y1)/2
            return x,y
        return None

    def clickHandler(self, event):
        if not self.potentialMove:
            self.BoardSpace.clearMoves(self)
            for (x,y) in self.board.keys():
                boardspace = self.board[(x,y)]
                if(boardspace.x0 < event.x and boardspace.x1 > event.x and boardspace.y0 < event.y and boardspace.y1 > event.y and boardspace.piece is not None):            
                    boardspace.piece.showMoves(self)
                    self.pieceToMove = boardspace.piece 
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
        if self.pieceToMove.name == "pawn":
            self.pieceToMove.firstMove = False
        self.addChessPiece(self.pieceToMove.color + "-" + self.pieceToMove.name, index, False)
        self.canvas.delete(self.pieceToMove.img)
        self.potentialMove = False
        self.BoardSpace.clearMoves(self)
        self.checkPotentialCheck()
        self.board[self.pieceToMove.index].piece = None
        self.turnChange()


    def checkPotentialCheck(self):
        self.pieceToMove.showMoves(self)

    #def inCheck(self, color):

    def turnChange(self):
        if(self.turn == "wh"):
            self.turn = "bk"
        else:
            self.turn = "wh"