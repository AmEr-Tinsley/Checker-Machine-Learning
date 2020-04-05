# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 19:53:26 2020

@author: WIKI
"""
from Board import Board
import pygame, sys, random,copy
from pygame.locals import *
from Player import Player
from PlayerAI import PlayerAI
import time
class Table():
    def __init__(self):
         self.WINDOWWIDTH = 800
         self.WINDOWHEIGHT = 700
         self.FPS = 60
         self.WT = pygame.image.load("Images/WT.png")
         self.KT = pygame.image.load("Images/KT.png")
         self.gold = (218,177,96)
         self.black = (0,0,0)
         self.cnt= 0
         self.turn = 0
         self.board = Board()
         self.player1 = Player(self.board.whitepieces)
         self.player2 = Player(self.board.blackpieces)
         self.states = []
         self.undoimg = pygame.image.load("Images/UNDO.png")
         pygame.init()
         self.FPSCLOCK = pygame.time.Clock()



    def text_objects(self,text, font,color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()
    def button(self,msg,x,y,w,h,ic,ac,color):
        mouse = pygame.mouse.get_pos()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.DISPLAYSURF, ac,(x,y,w,h))
            color = self.black
        else:
            pygame.draw.rect(self.DISPLAYSURF, ic,(x,y,w,h))
    
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = self.text_objects(msg, smallText,color)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.DISPLAYSURF.blit(textSurf, textRect)
    def set_up_players(self,player1,player2):
        self.board = Board()
        self.board.pieces = []
        self.board.blackpieces = []
        self.board.whitepieces = []
        self.board.board = []
        self.board.init_board()
        if player1 == 0:    
            self.player1 = PlayerAI(self.board.whitepieces)
        else:
            self.player1 = Player(self.board.whitepieces)
        if player2 == 0:
            self.player2 = PlayerAI(self.board.blackpieces)
        else:
            self.player2 = Player(self.board.blackpieces)
        
    def check_click(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 500 > pos[0] > 300 and 250 > pos[1] > 200:
                    self.set_up_players(1,1)
                    self.FPS = 60
                    self.load_game()
                elif 500 > pos[0] > 300 and 350 > pos[1] > 300:
                    self.set_up_players(1,0)
                    self.FPS = 30
                    self.load_game()
                elif 500 > pos[0] > 300 and 450 > pos[1] > 400:
                    self.set_up_players(0,0)
                    self.FPS = 1
                    self.load_game()
                elif 500 > pos[0] > 300 and 550 > pos[1] > 500:
                    self.quit()
                    
        
    def quit(self):
        pygame.quit()
        sys.exit()
    def build_button(self,text,x,y,w,h):
         self.button("",x,y,w,h,self.gold,self.gold,self.black)
         self.button(text,x+1,y+1,w-2,h-2,self.black,self.gold,self.gold)
        
        
    def menu(self):
        self.WINDOWWIDTH = 800
        self.WINDOWHEIGHT = 700

        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption("Dames")
        while True:
            largeText = pygame.font.SysFont("comicsansms",70)
            TextSurf, TextRect = self.text_objects("Menu", largeText,self.gold)
            TextRect.center = (400,50)
            self.DISPLAYSURF.blit(TextSurf, TextRect)
            
            self.build_button("Mutiplayer",300,200,200,50)
            self.build_button("Player Vs Pc",300,300,200,50)
            self.build_button("Pc Vs Pc",300,400,200,50)
            self.build_button("Quit",300,500,200,50)
            self.check_click()
    
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    def conv(self,x):
        H = int(x//60)
        M = int(x%60)
        x = str(H)
        y = str(M)
        if(len(x)==1):
            x = '0'+x
        if(len(y)==1):
            y = '0'+y
        return str(x)+':'+str(y)
    def display_text(self,text,x,y):
        Text = pygame.font.SysFont("comicsansms",20)
        TextSurf, TextRect = self.text_objects(text,Text,self.gold)
        TextRect.center = (x,y)
        self.DISPLAYSURF.blit(TextSurf, TextRect)
    def undo(self):
        if len(self.states)>1:
            self.states.pop()
        else:
            return
        self.player1,self.player2,self.board = self.player_copy(self.states[-1][0]),self.player_copy(self.states[-1][1]),self.board_copy(self.states[-1][2])
        self.turn = not self.turn
        self.cnt-=1
        self.board.pieces = []
        self.board.pieces.extend(self.player1.pieces)
        self.board.pieces.extend(self.player2.pieces)
        self.board.blackpieces = self.player2.pieces
        self.board.whitepieces = self.player1.pieces

    def player_copy(self,player):
        return copy.deepcopy(player)
    def board_copy(self,board):
        return copy.deepcopy(board)
    def check_game_over(self):
        if len(self.player1.pieces)==0 or len(self.player2.pieces)==0:
                self.quit()
        cnt = 0
        for piece in self.player1.pieces:
            cnt+=len(piece.display_possible_moves(self.board))
        if cnt == 0:
            self.quit()
        cnt = 0
        for piece in self.player2.pieces:
            cnt+=len(piece.display_possible_moves(self.board))
        if cnt == 0:
            self.quit()
    def load_game(self):
        self.states.clear()
        self.WINDOWWIDTH = 1200
        self.WINDOWHEIGHT = 700
        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption("Dames")
        self.turn = 0
        Timer = 0
        remaining_time = 300
        self.cnt = 0
        self.states.append((self.player_copy(self.player1),self.player_copy(self.player2),self.board_copy(self.board)))        
        while True:
            self.check_game_over()
            for x, line in enumerate(self.board.board):
                for y, box in enumerate(line):
                    if box == (102,204,25):
                        pygame.draw.rect(self.DISPLAYSURF, box, (x * self.board.BOXWIDTH, y * self.board.BOXHEIGHT, self.board.BOXWIDTH, self.board.BOXHEIGHT))
                    else:
                        if box == (255,255,255):
                            self.DISPLAYSURF.blit(self.KT, (x*self.board.BOXWIDTH,y*self.board.BOXHEIGHT))
                        else:
                           self. DISPLAYSURF.blit(self.WT, (x*self.board.BOXWIDTH,y*self.board.BOXHEIGHT))
            for piece in self.board.pieces:
                piece.draw(self.DISPLAYSURF)
            pygame.draw.rect(self.DISPLAYSURF, (0,0,0), (8 * self.board.BOXWIDTH, 0, 400, 700))
            Timer+=1
            if(Timer % 10 == 0):
                remaining_time-=1
            if remaining_time == 0:
                self.quit()
            who = "Who's playing ? : " + ('White' if self.turn == False else 'Black')
            timer =  "Remaining time : "+self.conv(remaining_time)
            self.display_text(who,1000,50)
            if self.FPS != 1:    
                self.display_text(timer,1000,100)
            self.build_button("Back To menu",900,600,200,50)
            
            if self.turn == 0:
                if self.player1.make_a_move(self):
                    self.turn = 1
                    Timer = 0
                    remaining_time = 300
                    self.cnt += 1
                    self.states.append((self.player_copy(self.player1),self.player_copy(self.player2),self.board_copy(self.board)))
            else:
                if self.player2.make_a_move(self):
                    self.turn = 0
                    Timer = 0
                    remaining_time = 300
                    self.cnt+=1
                    self.states.append((self.player_copy(self.player1),self.player_copy(self.player2),self.board_copy(self.board)))
            if self.cnt > 0 and self.FPS !=1 :
                self.display_text("Undo move : ",980,500)
                self.DISPLAYSURF.blit(self.undoimg, (1050,475))                
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
if __name__ == "__main__":
    table = Table()
    table.menu()
