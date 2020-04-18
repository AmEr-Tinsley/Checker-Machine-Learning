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
class MCTS:
    def __init__(self):
        self.score = defaultdict(int)
        self.cnt = defaultdict(int)
        self.amaf_cnt = dict()
        self.amaf_score = dict()
        self.children  = dict()
    def discover(self,node):
        path = self.go_down(node)
        leaf = path[-1]
        self.expand(leaf)
        w = self.simulate(leaf)
        self.back_propagate(path,w)
    def go_down(self,node):
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node] or node.is_terminal():
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
        cnt = 0
        who = node.turn
        while cnt <= 120:
            if node.is_terminal() == True:
                return 1  if (node.turn == who) else 0
            node = node.find_random_child()
            cnt+=1
        return 1-node.heuristics() if (node.turn == who) else node.heuristics() 
    def back_propagate(self, path, reward):
        cnt = 0
        last = None

        for node in reversed(path):
            if(cnt > 0 and node.turn == last.turn):
                reward = 1 - reward

            self.cnt[node] = self.cnt[node]+1
            self.score[node] = self.score[node] + reward
            last = node
            cnt+=1
            reward = 1 - reward
    def get_beta(self,node):
        b = 0.5
        return self.amaf_cnt[node] / (self.cnt[node] + self.amaf_cnt[node] +
                                   4 * self.cnt[node] * self.amaf_cnt[node] * pow(b, 2))
            
    def uct_select(self, node):
        log_N_vertex = math.log(self.cnt[node])
        assert all(n in self.children for n in self.children[node])

        def uct(n): 
            if self.cnt[n]==0:
                return float("-inf")
            return self.score[n] / self.cnt[n] + math.sqrt(20*log_N_vertex / self.cnt[n])
        return max(self.children[node], key=uct)
        
    
    def get_the_best(self, node):
        start = time.time()
        cnt = 0 
        while time.time()-start <= 5:
            cnt+=1
            self.discover(node)
        print(cnt)
        if node not in self.children:
            return node.get_transition(node.find_random_child())
        def sc(n):
            if self.cnt[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.score[n] / self.cnt[n]  # average reward
        who =  max(self.children[node], key=sc)
        print(self.score[who]/self.cnt[who],self.score[who],self.cnt[who])
        return node.get_transition(who)

        
