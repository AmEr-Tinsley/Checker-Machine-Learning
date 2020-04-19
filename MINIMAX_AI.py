# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:18:10 2020

@author: WIKI
"""
import pygame, sys, random
from pygame.locals import *
from Piece import Piece
from copy import copy, deepcopy
from MINIMAX.MINIMAX import MINIMAX

# this AI is based only on the experience of many games database that were played by expert players 
class PlayerMINMAX():
    def __init__(self,pieces,clicked_piece = 1,displayed_moves = [],eat_moves=[],completethemove=False):
        self.clicked_piece = clicked_piece
        self.pieces = pieces
        self.displayed_moves = displayed_moves
        self.eat_moves = []
        self.completethemove = completethemove
        self.moves_to_complete = []

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
    def human_intervention(self,table):
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 1101 > pos[0] > 1050 and 526 > pos[1] > 475:
                    table.undo()
                    return False
                if 1100 > pos[0] > 900 and 650 > pos[1] > 600:
                    table.FPS = 60
                    table.menu()
                    return False

    
    def go(self,pieces,board,otherplayer,table):
        ok = self.human_intervention(table)
        if ok == False:
            return False
        ok = False
        if(len(self.moves_to_complete)==0):
            AI = MINIMAX()
            self.moves_to_complete,h = AI.get_move(self.pieces[0].color[0],board)
            xx,yy = self.moves_to_complete[0]
            del self.moves_to_complete[0]
            self.moves_to_complete.reverse()
            for piece in board.pieces:
                y = (piece.x - 10) // board.BOXWIDTH
                x = (piece.y - 10) // board.BOXHEIGHT
                if (x == xx and y == yy):
                    self.clicked_piece = piece
        xx,yy = self.moves_to_complete[-1]
        self.moves_to_complete.pop()
        x = (self.clicked_piece.x - 10) // board.BOXWIDTH
        y = (self.clicked_piece.y - 10) // board.BOXHEIGHT
        xx,yy = yy,xx
        if abs(xx-x) == 2 and abs(yy-y) == 2:
            i = xx-x
            j = yy-y
            if i<0:
                i+=1
            else:
                i-=1
            if j<0:
                j+=1
            else:
                j-=1
            piece = self.pieces[0].who_is_there(x+i,y+j,table.board)
            otherplayer.pieces.remove(piece)
            table.board.pieces.remove(piece)
            ok = True
        wasking = self.clicked_piece.king
        self.clicked_piece.update(xx*board.BOXWIDTH + 10,yy*board.BOXHEIGHT + 10,board)
        if(not (len(self.clicked_piece.can_eat(board))==0 or ok == False) and (wasking == self.clicked_piece.king)):
            self.completethemove = True
        else:
            self.completethemove = False
        return (len(self.clicked_piece.can_eat(board))==0 or ok == False) or (wasking != self.clicked_piece.king)
    def should_eat(self,board):
        L = []
        for piece in self.pieces:
            if len(piece.can_eat(board))>0:
                L.append(piece)
        return L
    def make_a_move(self,table,states_visited = None):
        L = []
        otherplayer = table.player1 if self.pieces[0].color =='black' else table.player2
        if(self.completethemove == True):
            L.append(self.clicked_piece)
        else:
            L = self.should_eat(table.board)
        if len(L)>0:
            return self.go(L,table.board,otherplayer,table)
        else:
            for piece in self.pieces:
                if len(piece.display_possible_moves(table.board))>0:
                    L.append(piece)
            return self.go(L,table.board,otherplayer,table)
    
