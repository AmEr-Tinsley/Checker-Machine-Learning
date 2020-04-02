# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 16:53:28 2020

@author: WIKI
"""
import pygame, sys, random
from pygame.locals import *
from copy import copy, deepcopy
class Piece():
    
    def __init__(self,x,y,color,k):
        self.x = x
        self.y = y
        self.color = color
        self.king = k
    def __copy__(self):
        return type(self)(self.x,self.y,self.color)
    def __deepcopy__(self, memo): # memo is a dict of id's to copies
        id_self = id(self)        # memoization avoids unnecesary recursion
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)(
                deepcopy(self.x, memo),
                deepcopy(self.y,memo),
                deepcopy(self.color,memo),
                deepcopy(self.king,memo))
            memo[id_self] = _copy 
        return _copy
    def update(self,x,y,board):
        self.x = x
        self.y = y
        x = (x-10)//board.BOXWIDTH
        y = (y-10)//board.BOXHEIGHT
        if y==0 or y==7:
            self.king=True
            if self.color == 'black':    
                self.image = pygame.image.load("Images/blackking.png")
            else:
                self.image = pygame.image.load("Images/whiteking.png")
    def draw(self, target_surface):
        image = pygame.image.load("Images/black.png") if self.color == 'black' else pygame.image.load("Images/white.png")
        if self.king == True:
            if self.color == 'black':    
                image = pygame.image.load("Images/blackking.png")
            else:
                image = pygame.image.load("Images/whiteking.png")
        target_surface.blit(image, (self.x,self.y))
    def check(self,x,y,board):
        for piece in board.pieces:
            xx = (piece.x-10)//board.BOXWIDTH
            yy = (piece.y-10)//board.BOXHEIGHT
            if xx==x and yy ==y:
                return False
        return True
    def who_is_there(self,x,y,board):
        x = x * board.BOXWIDTH + 10
        y = y * board.BOXHEIGHT + 10
        for piece in board.pieces:
            if(piece.x == x and piece.y == y):
                return piece
        return -1
    def can_eat(self,board):
        x = (self.x-10)//board.BOXWIDTH
        y = (self.y-10)//board.BOXHEIGHT
        L = []
        for i in [-2,2]:
            if (i == -2 and x<=1) or (i==2 and x>=6):
                continue
            for j in [-2,2]:
                if (j==-2 and y<=1) or (j==2 and y>=6):
                    continue
                elif(j<0 and self.color=='black' and self.king==False):
                    continue
                elif(j>0 and self.color=='white' and self.king==False):
                    continue
                if self.check(x+i,y+j,board):
                    jj = j 
                    ii = i
                    if ii<0:
                        ii+=1
                    else:
                        ii-=1
                    if jj<0:
                        jj+=1
                    else:
                        jj-=1
                    piece = self.who_is_there(x+ii,y+jj,board)
                    if piece == -1:
                        continue
                    if piece.color != self.color:
                        L.append((int(x+i),int(y+j)))
                    
        return L
            
        
    def display_possible_moves(self,board):
        x = (self.x-10)//board.BOXWIDTH
        y = (self.y-10)//board.BOXHEIGHT
        L = self.can_eat(board)
        if len(L)>0:
            return L
        for i in [-1,1]:
            if (i==-1 and x==0) or (i==1 and x==7):
                continue
            for j in [-1,1]:
                if (j==-1 and y==0) or (j==1 and y==7):
                    continue
                elif(j<0 and self.color=='black' and self.king==False):
                    continue
                elif(j>0 and self.color=='white' and self.king==False):
                    continue
                if self.check(x+i,y+j,board):
                    L.append((int(x+i),int(y+j)))
        return L
        