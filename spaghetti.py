# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:18:10 2020

@author: WIKI
"""
import pygame, sys, random
from pygame.locals import *
from Piece import Piece
from copy import copy, deepcopy
import sqlite3

# this AI is based only on the experience of many games database that were played by expert players 
class PlayerMINMAX():
    def __init__(self,pieces,clicked_piece = 1,displayed_moves = [],eat_moves=[],completethemove=False):
        self.clicked_piece = clicked_piece
        self.pieces = pieces
        self.displayed_moves = displayed_moves
        self.eat_moves = []
        self.completethemove = completethemove
        self.moves_to_complete = []
        self.conn = sqlite3.connect("training.db")
        self.c=self.conn.cursor()
        self.grid=[]
        self.dx=[1,1,-1,-1]
        self.dy=[1,-1,1,-1]
        self.MAX_DEPTH=4
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
                    self.conn.close()
                    table.FPS = 60
                    table.menu()
                    return False

    def get_board(self,board):
        self.grid=[]
        for i in range (8):
            self.grid.append([])
            for j in range(8):
                self.grid[i].append('e')
        for piece in board.pieces:
            y = int((piece.x-10)//board.BOXWIDTH)
            x = int((piece.y-10)//board.BOXHEIGHT)
            self.grid[x][y]= piece.color[0]
            if piece.king:
                self.grid[x][y] = self.grid[x][y].upper()

    def valid(self,x,y):
        return x>=0 and x<8 and y>=0 and y<8
    
    def eat(self,x,y,xx,yy):
        xxx,yyy = x + 2 * (xx - x), y + 2 * (yy - y)
        return self.valid(xxx,yyy) and  self.grid[xxx][yyy]=='e' and self.grid[xx][yy].upper() != self.grid[x][y].upper()

    def can_eat(self,x,y,seq,moves):
        s , e = 0 , 4
        if   self.grid[x][y] == 'w':
            s=2
        elif self.grid[x][y] == 'b':
            e=2
        ok=True
        for d in range(s,e):
            xx = cur_x + self.dx[d]
            yy = cur_y + self.dy[d]
            if self.valid(xx,yy) and self.grid[xx][yy]!='e' and  self.eat(cur_x,cur_y,xx,yy):
                ok=False
                mid_x = x + (xx - x) // 2
                mid_y = y + (yy - y) // 2
                eaten = self.grid[mid_x][mid_y]
                simulate(x,y,xx,yy)
                if (len(seq) == 0):
                    seq.append(x,y)
                seq.append(xx,yy)
                can_eat(xx,yy,moves)
                if (len(seq) == 2):
                    seq.pop()
                seq.pop()
                simulate(xx,yy,x,y)
                self.grid[mid_x][mid_y] = eaten
        if (ok) and len(seq)!=0:
           moves.append(seq)

    def get_moves(self,piece):
        moves=[]
        x , y =  piece
        s , e = 0 , 4
        if   self.grid[x][y] == 'w':
            s=2
        elif self.grid[x][y] == 'b':
            e=2
        self.can_eat(x,y,[],moves)
        if len(moves)!=0:
            return True,moves
        for d in range(s,e):
            xx = x + self.dx[d]
            yy = y + self.dy[d]
            if not self.valid(xx,yy):
                continue
            if self.grid[xx][yy] == 'e':
                moves.append([(x,y),(xx,yy)])
        return False,moves

    def calc(self,player):
        h = 0
        pieces = 0
        for x in range (8):
            for y in range(8):
                if self.grid[x][y] == 'w':
                    h+= 200
                elif self.grid[x][y] == 'b':
                    h-= 200
                elif self.grid[x][y] == 'W':
                    h+=500
                elif self.grid[x][y] == 'B':
                    h-=500
        return h
    
    def simulate(self,x,y,xx,yy):
        if (abs(x-xx)>1 or abs(y-yy)>1):
            xxx,yyy = x + (xx - x)//2, y + (yy - y)//2
            self.grid[xx][yy]=self.grid[x][y]
            self.grid[xxx][yyy]='e'
            self.grid[x][y]='e'
        else:
            self.grid[x][y],self.grid[xx][yy]= self.grid[xx][yy],self.grid[x][y]
    
    def inv(self,c):
        if (c=='w'):
            return 'b'
        else:
            return 'w'
    
    def solve(self,player,depth):
        if (depth>self.MAX_DEPTH):
            return [],self.calc(player)
        pieces = []
        for x in range(8):
            for y in range(8):
                if self.grid[x][y].upper() ==  player.upper():
                    pieces.append((x,y))
        moves = []
        eat   = []
        for piece in pieces:
            can_eat,L = self.get_moves(piece)
            if (len(L)==0):
                continue
            if can_eat:
                eat.append(L)
            else:
                moves.append(L)
        if (len(eat)!=0):
            moves=eat
        mx_mn = 10000000000
        if player == 'w':
            mx_mn*= -1

        best_move = []
        for piece_moves in moves:
            for move in piece_moves:
                ate = []
                x,y,xx,yy = 0,0,0,0
                for i in range(1,len(move)):
                    x,y = move[i-1]
                    xx,yy = move[i]
                    xxx,yyy = x + (xx - x)//2, y + (yy - y)//2
                    if abs(x-xx)==2:
                        ate.append(self.grid[xxx][yyy])
                    else:
                        ate.append('e')
                    self.simulate(x,y,xx,yy)
                
                if (player ==  'w' and xx==0) or (player == 'b' and xx==7):
                    self.grid[xx][yy] = player.upper()
                cur_h = self.solve(self.inv(player),depth+1)[1]
                if   player == 'w' and cur_h>mx_mn:
                    best_move, mx_mn = move, cur_h
                elif player == 'b' and cur_h<mx_mn:
                    best_move, mx_mn = move, cur_h

                self.grid[xx][yy] = player

                for i in range(len(move) - 2 ,0):
                    x,y, = move[i+1]
                    xx,yy = move[i]
                    xxx,yyy = x + (xx - x)//2, y + (yy - y)//2
                    eaten = ate[i]
                    self.simulate(x,y,xx,yy)
                    if eaten!='e':
                            self.grid[xxx][yyy] = eaten

        return best_move,mx_mn
    
    def go(self,pieces,board,otherplayer,table):
        ok = self.human_intervention(table)
        if ok == False:
            return False
        ok = False
        
        self.get_board(board)
        
            
        if(len(self.moves_to_complete)==0):
            self.moves_to_complete = self.solve(self.pieces[0].color[0],1)[0]
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
            for piece in self.pieces:
                if len(piece.display_possible_moves(table.board))>0:
                    L.append(piece)
            return self.go(L,table.board,otherplayer,table)
    
