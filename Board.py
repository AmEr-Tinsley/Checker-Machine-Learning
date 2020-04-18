# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 01:51:03 2020

@author: WIKI
"""
import pygame, sys, random
from pygame.locals import *
from Piece import Piece
from copy import copy, deepcopy

class Board():
    
    def __init__(self,pieces=[],blackpieces=[],whitepieces=[],BOARDWIDTH=8,BOARDHEIGHT=8,BOXWIDTH=100,BOXHEIGHT=87.5,board=[]):
       
        self.pieces = pieces
        self.blackpieces = blackpieces
        self.whitepieces = []
        self.BOARDWIDTH = BOARDWIDTH
        self.BOARDHEIGHT = BOARDHEIGHT
        self.BOXWIDTH = BOXWIDTH
        self.BOXHEIGHT = BOXHEIGHT
        self.board = board
    
    def init_board(self):
        for x in range(0, self.BOARDWIDTH):
            line = []
            for y in range(0, self.BOARDHEIGHT):
                if (x + y) % 2 == 0:
                    line.append((153, 102, 51))
                else:
                    line.append((255, 255, 255))
                    if y<=2:
                        piece = Piece(x *  self.BOXWIDTH  + 10, y * self.BOXHEIGHT + 10,'black',False)
                        self.blackpieces.append(piece)
                        self.pieces.append(piece)
                    elif y>=5:
                        piece = Piece(x *  self.BOXWIDTH  + 10, y * self.BOXHEIGHT + 10,'white',False)
                        self.whitepieces.append(piece)
                        self.pieces.append(piece)
            self.board.append(line)
    def __copy__(self):
        return type(self)(self.pieces,self.blackpieces,self.whitepieces,self.BOARDWIDTH,self.BOARDHEIGHT,self.BOXWIDTH,
                   self.BOXHEIGHT,self.board)
    def __deepcopy__(self, memo): # memo is a dict of id's to copies
        id_self = id(self)        # memoization avoids unnecesary recursion
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)(deepcopy(self.pieces, memo),
                         deepcopy(self.blackpieces, memo),
                         deepcopy(self.whitepieces, memo),
                         deepcopy(self.BOARDWIDTH, memo),
                         deepcopy(self.BOARDHEIGHT, memo),
                         deepcopy(self.BOXWIDTH, memo),
                         deepcopy(self.BOXHEIGHT, memo),
                         deepcopy(self.board, memo)
                         )
            memo[id_self] = _copy 
        return _copy
    
    def hash(self):
        ret = ""
        for y in range(8):
            for x in range(8):
                if (x+y)%2==1:
                    X = (x *self.BOXWIDTH+10)
                    Y = (y*self.BOXHEIGHT+10)
                    flag = False
                    for piece in self.pieces:
                        if(X == piece.x and Y == piece.y):
                            ret+= (piece.color[0] if not piece.king else piece.color[0].upper())
                            flag = True
                    if flag==False:
                        ret+='.'
                else:
                    ret +='.'
        return ret
    def game_over(self):
        if(len(self.blackpieces)==0):
            return 1
        if(len(self.whitepieces)==0):
            return 0
        cnt = 0
        for piece in self.blackpieces:
            cnt+=len(piece.display_possible_moves(self))
        if cnt == 0:
            return 1 
        cnt = 0
        for piece in self.whitepieces:
            cnt+=len(piece.display_possible_moves(self))
        if cnt == 0:
            return 0
        return -1
    
        