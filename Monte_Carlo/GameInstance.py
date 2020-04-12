# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:05:47 2020

@author: WIKI
"""
from copy import copy, deepcopy
from Board import Board
import random
import multiprocessing as mp

class GameInstance:
    def __init__(self,turn,board,player,otherplayer):
        self.turn = turn
        self.board = board
        self.player = player
        self.otherplayer = otherplayer
        self.childrens = []
        
    def hash(self):
        return self.board.hash()
    def should_eat(self):
        L = []
        for piece in self.player.pieces:
            if len(piece.can_eat(self.board))>0:
                L.append(piece)
        return L  
    def __hash__(self):
        return hash((self.board.hash()))

    def __eq__(self, other):
        return self.board.hash() == other.board.hash()
    
    def player_score(self,who):
        ret = 0
        for piece in who.pieces:
            if piece.king:
                ret+=5
            else:
                ret+=2
        return ret
        
    def possible_pieces_to_move(self):
         L = []
         if(self.player.completethemove == True):
             L.append(self.player.clicked_piece)
         else:
            L = self.should_eat()
         if len(L)>0:
            return L
        
         for piece in self.player.pieces:
             if len(piece.display_possible_moves(self.board))>0:
                L.append(piece)
         return L

    def do_this_move(self,piece,mv):
        xx = (piece.x-10)//self.board.BOXWIDTH
        yy = (piece.y-10)//self.board.BOXHEIGHT
        x = mv[0]
        y = mv[1]
        ok=False
        board = deepcopy(self.board)
        board.init_board()
        board.pieces = []
        board.whitepiece= []
        board.blackpieces = []
        player = deepcopy(self.player)
        otherplayer = deepcopy(self.otherplayer)
        board.pieces.extend(player.pieces)
        board.pieces.extend(otherplayer.pieces)
        if player.pieces[0].color[0].upper()=='B':
            board.blackpieces = player.pieces
            board.whitepieces = otherplayer.pieces
        else:
            board.blackpieces = otherplayer.pieces
            board.whitepieces = player.pieces
        for piecee in player.pieces:
            if piecee.x == piece.x and piecee.y == piece.y:
                player.clicked_piece = piecee
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
            piece = player.pieces[0].who_is_there(xx+i,yy+j,board)
            otherplayer.pieces.remove(piece)
            board.pieces.remove(piece)
            ok = True
        
        
        wasking = player.clicked_piece.king
        player.clicked_piece.update(x*board.BOXWIDTH + 10,y*board.BOXHEIGHT + 10,board)
        if len(player.clicked_piece.can_eat(board)) !=0 and ok == True and wasking == player.clicked_piece.king:
            player.completethemove = True
        else:
            player.completethemove = False
        if  (not player.completethemove):
            return GameInstance(not self.turn,board,otherplayer,player)
        else:
            return GameInstance(self.turn,board,player,otherplayer)
        
    def find_random_child(self):
        if len(self.childrens)==0:
            pieces = self.possible_pieces_to_move()
            piece = random.choice(pieces)
            moves = piece.display_possible_moves(self.board)
            mv = random.choice(moves)
            return (self.do_this_move(piece,mv))
        ret = random.choice(self.childrens)
        return ret
    def get_childrens(self):
        if len(self.childrens)>0:
            return self.childrens
        pool = mp.Pool(5)
        pieces = self.possible_pieces_to_move()
        for piece in pieces:
            L = pool.apply_async(piece.display_possible_moves,(self.board,))
            L = L.get()
            for mv in L:
                self.childrens.append(self.do_this_move(piece,mv))
        
        return self.childrens
    def is_terminal(self):
        return self.board.game_over() != -1
    def show(self,s):
        grid = []
        cnt=0
        for x in range(8):
            grid.append([])
            for y in range(8):
                if ((x+y)%2 == 1):
                    if (s[cnt]=='e'):
                        grid[x].append('.')
                    else:
                        grid[x].append(s[cnt])
                    cnt+=1
                else:
                    grid[x].append('.')
            print(grid[x])
        print()
        print()
    def reward(self):
        if self.turn == (self.board.game_over()):
            return 1
        return 0
    def get_transition(self,wa):
        L = []
        K = []
        for piece in self.player.pieces:
            L.append(((piece.x-10)//self.board.BOXWIDTH,(piece.y-10)//self.board.BOXHEIGHT))
        if len(wa.player.pieces)>0 and wa.player.pieces[0].color[0].upper()==self.player.pieces[0].color[0].upper():
            for piece in wa.player.pieces:
                K.append(((piece.x-10)//self.board.BOXWIDTH,(piece.y-10)//self.board.BOXHEIGHT))
        else:
            for piece in wa.otherplayer.pieces:
                K.append(((piece.x-10)//self.board.BOXWIDTH,(piece.y-10)//self.board.BOXHEIGHT))
            
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
            
    
