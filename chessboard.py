import tkinter as tk
from tkinter import *
import pieces as p
from PIL import Image,ImageTk
from pathlib import Path

class ChessBoard():
    board = []
    pieceArr = []
    imageNames = {}

    class BoardSpace():
        def __init__(self, x0, y0, x1, y1):
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1
            self.piece = None
            self.shownmoves = []

        def removeDots(self):
            for boardspace in self.board:
                for dot in boardspace.shownmoves:
                    self.canvas.delete(dot)

    def __init__(self, root):
        self.root = root
        self.entry = tk.Entry(root)
        self.canvas = tk.Canvas(root, width = 1080, height = 800, background="#000000")
        self.canvas.bind('<Button-1>', self.clickHandler)
        self.canvas.grid(row=0, column=0)
        frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky="n")
        clr = "#769656"
        lastX = 140
        lastY = 0
        for x in range(8):
            lastX+=80
            for y in range(8):
                lastY+=80
                self.canvas.create_rectangle(lastX, lastY, (x+1)*80+220, (y+1)*80+80, fill=clr)
                self.board.append(self.BoardSpace(lastX, lastY, (x+1)*80+220, (y+1)*80+80))
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
        self.addChessPiece("bk-rook", 0)
        self.addChessPiece("bk-rook", 56)
        self.addChessPiece("bk-knight", 8)
        self.addChessPiece("bk-knight", 48)
        self.addChessPiece("bk-bishop", 16)
        self.addChessPiece("bk-bishop", 40)
        self.addChessPiece("bk-queen", 24)
        self.addChessPiece("bk-king", 32)

        #white pieces
        self.addChessPiece("wh-rook", 7)
        self.addChessPiece("wh-rook", 63)
        self.addChessPiece("wh-knight", 15)
        self.addChessPiece("wh-knight", 55)
        self.addChessPiece("wh-bishop", 23)
        self.addChessPiece("wh-bishop", 47)
        self.addChessPiece("wh-queen", 31)
        self.addChessPiece("wh-king", 39)

        for i in range(8):
            self.addChessPiece("bk-pawn", i*8+1)
            self.addChessPiece("wh-pawn", i*8+6)

    def addChessPiece(self, name, index):
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
                newPiece = p.ChessPieces.Rook(pieceName, img, color, index)
            case "king":
                newPiece = p.ChessPieces.King(pieceName, img, color, index)
            case "pawn":
                newPiece = p.ChessPieces.Pawn(pieceName, img, color, index)
 
        self.pieceArr.append(newPiece)
        boardspace.piece = newPiece
        piece = self.canvas.create_image(self.pieceCoordinates(boardspace), image=img)
        return piece

    def drawDot(self, index, piece):
        if index < 64 and index >= 0:
            dotToDraw = self.board[index]
            if(dotToDraw.x0 > 80 and dotToDraw.y0 > 220 and dotToDraw.x1 < 860 and dotToDraw.y1 < 720):
                if(self.checkValidPosition(index, piece)):   
                    x,y = self.pieceCoordinates(dotToDraw)
                    dotObj = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="grey")
                    return dotObj

    def drawCircle(self, circleToDraw):
        x,y = self.pieceCoordinates(circleToDraw)
        circleObj = self.canvas.create_oval(x-25, y-25, x+25, y+25, fill="grey")
        return circleObj

    def checkValidPosition(self, index, piece):
        boardSpace = self.board[index]
        if boardSpace.piece is None:
            return True
        elif piece.color != boardSpace.piece.color:
            self.drawCircle(boardSpace)
            return False
        else:
            return False

    def pieceCoordinates(self, boardSpace):
        if(boardSpace != None):
            x = (boardSpace.x0 +boardSpace.x1)/2
            y = (boardSpace.y0 +boardSpace.y1)/2
            return x,y
        return None

    def clickHandler(self, event):
        self.BoardSpace.removeDots(self)
        for boardspace in self.board:
            if(boardspace.x0 < event.x and boardspace.x1 > event.x and boardspace.y0 < event.y and boardspace.y1 > event.y and boardspace.piece is not None):            
                boardspace.piece.showMoves(self)