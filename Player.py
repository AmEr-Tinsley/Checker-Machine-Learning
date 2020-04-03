# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 01:51:03 2020

@author: WIKI
"""
import pygame, sys, random
from pygame.locals import *
from Piece import Piece
from copy import copy, deepcopy

class Player():
    def __init__(self,pieces,clicked_piece = 1,displayed_moves = [],eat_moves=[],completethemove=False):
        self.clicked_piece = clicked_piece
        self.pieces = pieces
        self.displayed_moves = displayed_moves
        self.eat_moves = []
        self.completethemove = completethemove
    def __copy__(self):
        return type(self)(self.pieces,self.clicked_piece,self.displayed_moves,self.eat_moves,self.completethemove)
    def __deepcopy__(self, memo): # memo is a dict of id's to copies
        id_self = id(self)        # memoization avoids unnecesary recursion
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)(
                deepcopy(self.pieces,memo),
                deepcopy(self.clicked_piece,memo),
                deepcopy(self.displayed_moves,memo),
                deepcopy(self.eat_moves,memo),
                deepcopy(self.completethemove,memo))
            memo[id_self] = _copy 
        return _copy
    def reset_displayed_moves(self , board):
        for x in range(board.BOARDHEIGHT):
            for y in range(board.BOARDWIDTH):
                if board.board[x][y] == (102,204,25):
                    board.board[x][y] = (255, 255, 255)
    def go(self,pieces,board,otherplayer,table):
        for event in pygame.event.get():
            ok = False
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 1101 > pos[0] > 1050 and 526 > pos[1] > 475:
                    table.undo()
                    return False
                if 1100 > pos[0] > 900 and 650 > pos[1] > 600:
                    table.menu()
                    return False
                x = (pos[0])//board.BOXWIDTH
                y = (pos[1])//board.BOXHEIGHT
                for p in self.displayed_moves:
                    if p[0]==x and p[1]==y:
                        xx = (self.clicked_piece.x-10)//board.BOXWIDTH
                        yy = (self.clicked_piece.y-10)//board.BOXHEIGHT
                        if abs(xx-x) == 2 and abs(yy-y) == 2:
                            i = x-xx
                            j = y-yy
                            if i<0:
                                i+=1
                            else:
                                i-=1
                            if j<0:
                                j+=1
                            else:
                                j-=1
                            piece = self.pieces[0].who_is_there(xx+i,yy+j,table.board)
                            otherplayer.pieces.remove(piece)
                            table.board.pieces.remove(piece)
                            ok = True
                        self.clicked_piece.update(x*board.BOXWIDTH + 10,y*board.BOXHEIGHT + 10,board)
                        self.reset_displayed_moves(board)
                                
                        self.displayed_moves = []
                        if(not (len(self.clicked_piece.can_eat(board))==0 or ok == False)):
                            self.completethemove = True
                        else:
                            self.completethemove = False
                        return (len(self.clicked_piece.can_eat(board))==0 or ok == False)                       
                for piece in pieces:
                    if ((piece.x-10)//board.BOXWIDTH == pos[0]//board.BOXWIDTH) and ((piece.y-10)//board.BOXHEIGHT == pos[1]//board.BOXHEIGHT) :
                        self.reset_displayed_moves(board)
                        self.displayed_moves = piece.display_possible_moves(board)
                        self.clicked_piece = piece
        for p in self.displayed_moves:
            board.board[p[0]][p[1]]=(102,204,25)
        return False
    def should_eat(self,board):
        L = []
        for piece in self.pieces:
            if len(piece.can_eat(board))>0:
                L.append(piece)
        return L
    def make_a_move(self,table):
        L = []
        otherplayer = table.player1 if self.pieces[0].color =='black' else table.player2
        if(self.completethemove == True):
            L.append(self.clicked_piece)
        else:
            L = self.should_eat(table.board)
        if len(L)>0:
            return self.go(L,table.board,otherplayer,table)
        else:
            return self.go(self.pieces,table.board,otherplayer,table)
        
