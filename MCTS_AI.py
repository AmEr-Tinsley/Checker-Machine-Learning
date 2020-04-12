# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 18:04:27 2020

@author: WIKI
"""

from Monte_Carlo.GameInstance import GameInstance
from Monte_Carlo.MCTS import MCTS
import pygame, sys, random
from pygame.locals import *
from Piece import Piece
from copy import copy, deepcopy
import time
class MCTS_AI:
    
    
    def __init__(self,pieces,clicked_piece = 1,displayed_moves = [],eat_moves=[],completethemove=False):
        self.clicked_piece = clicked_piece
        self.pieces = pieces
        self.displayed_moves = displayed_moves
        self.eat_moves = []
        self.completethemove = completethemove
    
    def __copy__(self): 
        return type(self)(self.pieces,self.clicked_piece,self.displayed_moves,self.eat_moves,self.completethemove)
    def __deepcopy__(self, memo):
        id_self = id(self)        
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
        return True
    def go(self,Tree,instance,table):
        ok = self.human_intervention(table)
        otherplayer = table.player1 if self.pieces[0].color =='black' else table.player2
        if ok == False:
            return False
        ok = False
        xx,yy,x,y = Tree.get_the_best(instance)
        for piece in self.pieces:
            if piece.x == (xx*table.board.BOXWIDTH + 10) and piece.y == (yy*table.board.BOXHEIGHT+10):
                self.clicked_piece = piece
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
        wasking = self.clicked_piece.king
        self.clicked_piece.update(x*table.board.BOXWIDTH + 10,y*table.board.BOXHEIGHT + 10,table.board)
        if( len(self.clicked_piece.can_eat(table.board))!=0 and ok == True and (wasking == self.clicked_piece.king)):
            self.completethemove = True
        else:
            self.completethemove = False
        return not self.completethemove
    def make_a_move(self,table):
        otherplayer = table.player1 if self.pieces[0].color =='black' else table.player2
        turn = 0 if self.pieces[0].color[0].upper() == 'W' else 1
       # print(self.completethemove)
        inst = GameInstance(turn,deepcopy(table.board),deepcopy(self),deepcopy(otherplayer))
        Tree = MCTS()
        return self.go(Tree,inst,table)
    
    
