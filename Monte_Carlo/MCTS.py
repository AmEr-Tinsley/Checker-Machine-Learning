# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:48:16 2020

@author: WIKI
"""
from collections import defaultdict
import math
import time
import random
from copy import deepcopy
import multiprocessing as mp
class MCTS:
    def __init__(self):
        self.score = defaultdict(int)
        self.cnt = defaultdict(int)
        self.children  = dict()
    def discover(self,node):
        path = self.go_down(node)
        leaf = path[-1]
        self.expand(leaf)
        w = self.simulate(leaf)
        self.back_propagate(path,w)
        return [self.cnt,self.score,self.children]
    def go_down(self,node):
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self.uct_select(node)
    def expand(self,node):
        if node in self.children:
            return
        self.children[node] = node.get_childrens()

    
    
    def simulate(self,node):
        invert_reward = True
        cnt = 0
        while cnt <= 60:
            if node.is_terminal() == True:
                return node.reward()  if invert_reward else 1 - node.reward()
            x = node
            node = node.find_random_child()
            if(x.turn != node.turn):
                invert_reward = not invert_reward
            cnt+=1
        
        return 0.5
    def get_heuristic(self,node):
        h = 0
        for piece in node.board.pieces:
            if piece.color[0] == 'w':
                if piece.king:
                    h+= 10
                else:
                    x = (piece.y - 10) // node.board.BOXHEIGHT
                    h+= 5 + 2 * int(x<4)
            else:
                if piece.king:
                    h-= 10
                else:
                    x = (piece.y - 10) // node.board.BOXHEIGHT
                    h-= 5 + 2 * int(x>=4)

        if node.player.pieces[0].color[0] == 'b':
            h*=-1
        return h

            
    
    def back_propagate(self, path, reward):
        cnt = 0
        last = None
        for node in reversed(path):
            if(cnt > 0 and node.turn == last.turn):
                reward = 1 - reward
            self.cnt[node] += 1
            self.score[node] += reward
            last = node
            cnt+=1
            reward = 1 - reward
            
    def uct_select(self, node):
        log_N_vertex = math.log(self.cnt[node])
        def uct(n):
            return self.score[n] / self.cnt[n] + math.sqrt(log_N_vertex / self.cnt[n])
        return max(self.children[node], key=uct)
    def get_the_best(self, node):
        self.discover(node)
        self.discover(node)
        if node not in self.children:
            return node.get_transition(node.find_random_child())
        def sc(n):
            if self.cnt[n]==0:
                return -1000000000
            return self.score[n]/self.cnt[n]
        who = max(self.children[node],key=sc)
        return node.get_transition(who)
        
