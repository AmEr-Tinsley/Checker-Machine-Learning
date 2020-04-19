# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:05:47 2020

@author: WIKI
"""
from copy import copy, deepcopy
from Board import Board
import random
import multiprocessing as mp
import time
class GameInstance:
    def __init__(self,hashed_board,turn,piece = None):
        self.board = []
        curr = 0
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[i].append(hashed_board[curr])               
                curr+=1
        self.turn = turn
        self.piece_to_complete_the_move = piece
    def hash(self):
        ret =""
        for i in range(8):
            for j in range(8):
                ret+=self.board[i][j]
        return ret
    def __hash__(self):
        return hash(self.hash())

    def __eq__(self, other):
        return self.hash() == other.hash()
    def ok(self,x,y):
        return (x<=7 and y <= 7 and x>=0 and y>=0)
    def can_eat(self,i,j):
        i = int(i)
        j = int(j)
        dir = [-1,1] if self.board[i][j].istitle() else [(1 if self.turn == 'b' else -1)]
        ret = []
        for d in dir:
            for y in [-1,1]:
                x_opp,y_opp,x_free,y_free = int(i+d),int(j+y),int(i+2*d),int(j+2*y)
                if self.ok(x_opp,y_opp) and self.ok(x_free,y_free):
                    if self.board[x_free][y_free] =='.' and self.board[x_opp][y_opp].lower() not in [self.turn,'.']:
                        ret.append((i,j,x_free,y_free))
        return ret
    def normal_move(self,x,y):
        dir = [-1,1] if self.board[x][y].istitle() else [(1 if self.turn == 'b' else -1)]
        ret = []
        for d in dir:
            for k in [-1,1]:
                x_free,y_free = int(x+d),int(y+k)
                if self.ok(x_free,y_free) and self.board[x_free][y_free] == '.':
                    ret.append((x,y,x_free,y_free))
        return ret
    def allowed_moves(self):
        pieces = []
        ret = []
        if self.piece_to_complete_the_move != None:
            pieces.append(self.piece_to_complete_the_move)
        else:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j].lower() == self.turn:
                        pieces.append((int(i),int(j)))
        for piece in pieces:
            ret.extend(self.can_eat(piece[0],piece[1]))
        if len(ret)>0:
            return ret
        for piece in pieces:
            ret.extend(self.normal_move(piece[0],piece[1]))
        return ret
    def move(self,p):
        ret = deepcopy(self)
        from_x,from_y,to_x,to_y = p
        ret.piece_to_complete_the_move = None
        no = False
        if abs(from_x-to_x) == 1:
            ret.board[to_x][to_y]=ret.board[from_x][from_y]
            ret.board[from_x][from_y]='.'
        else:
            capt_x,capt_y = int((from_x+to_x)//2) , int((from_y+to_y)//2)
            ret.board[to_x][to_y] = ret.board[from_x][from_y]
            ret.board[from_x][from_y] = ret.board[capt_x][capt_y] = '.'
            if len(ret.can_eat(to_x,to_y)) > 0:
                no = True
                ret.piece_to_complete_the_move = (to_x,to_y)
        if no == False:
            ret.turn = 'b' if (self.turn == 'w') else 'w' 
        if to_x == 0 or to_x == 7:
            ret.board[to_x][to_y]=ret.board[to_x][to_y].upper()
        return ret
    
    def show(self):
        print(self.turn)
        for i in range(8):
            print(self.board[i])
    
    def get_childrens(self):
        L = self.allowed_moves()
        ret = []
        for p in L:
            ret.append(self.move(p))
        return ret
    
    def find_random_child(self):
        mv = random.choice(self.allowed_moves())
        ret = self.move(mv)
        #print(mv)
        return ret
    def is_terminal(self):
        return len(self.allowed_moves()) == 0
    def heuristics(self):
        All = me = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j]==self.turn:
                    me+= 15 if self.board[i][j].istitle() else (12-i if self.board[i][j] == 'w' else 5 + i)
                    All+=15 if self.board[i][j].istitle() else (12-i if self.board[i][j] == 'w' else 5 + i)
                elif self.board[i][j] != '.':
                    All+=15 if self.board[i][j].istitle() else (12-i if self.board[i][j] == 'w' else 5 + i)
        return me/All
    def get_transition(self,wa):
        L = []
        K = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].lower() == self.turn.lower():
                    L.append((i,j))
        for i in range(8):
            for j in range(8):
                if wa.board[i][j].lower() == self.turn.lower():
                    K.append((i,j))
        who1 = None
        who2 = None
        for p in L:
            if p not in K:
                who1 = p
                break
        for p in K:
            if p not in L:
                who2 = p
                break
        return (who1[0],who1[1],who2[0],who2[1])
        
            
            
        
    
