from game import *
import random
import time
import numpy as np
from math import sqrt
import redis
import json

flip = {'X':'O','O':'X'}
curr = 'X'


def hash_board_r(board_matrix):
    total = 0
    k = 0
    r = len(board_matrix[0])
    for i in range(r):
        for j in range(r):
            total+= (r**k)*board_matrix[i][j]
            k+=1
    return str(int(total))

class Player:
    def __init__(self,symbol,epsilon,alpha=0.1,gamma=0.9,reward=1,punishment=-1,draw=0):
        self.epsilon = epsilon
        self.weighted_average = 0
        self.Q = {}
        self.symbol = symbol
        self.alpha = alpha 
        self.gamma = gamma
        self.reward = reward
        self.punishment = punishment
        self.draw = draw
    def policy(self,s,Board):
        if np.random.random() < self.epsilon:
        
            return random.choice(ACTION_SPACE)

        else:
           
            try:
                keys = [k for k,v in self.Q[s].items() if v == max(self.Q[s].values()) and Board.board[k[0]][k[1]]==0]
               
                return random.choice(keys) if keys else random.choice(ACTION_SPACE)
            except:
                return random.choice(ACTION_SPACE)
        




# X-epsilon = 0.15
# O-epsilon = 0.05


def train(X_alpha,X_epsilon,O_alpha,O_epsilon,X_gamma,O_gamma,Board):
    player1 = Player('X',epsilon=X_epsilon,alpha=X_alpha,gamma=X_gamma) # by default player 1 (the 'X' player) will start first
    player2 = Player('O',epsilon=O_epsilon,alpha=O_alpha,gamma=O_gamma)
    seen_states = {}
    STEPS = 1
    flip_player = {player1:player2, player2:player1}
    for _ in range(STEPS):
       
        curr = player1
    
        s = Board.reset()

        print(_)
        
        states = {player1:[],player2:[]} # used to keep track of states
        while Board.is_terminal(s) == False:
          
            
            s_hash = hash_board_r(s) # the board converted into a single number
            temp = seen_states.get(hash_board_r(s),None) # used to keep track of how many times a state has been seen
            if not temp:
                seen_states[hash_board_r(s)]=1
            else:
                seen_states[hash_board_r(s)]+=1
            if curr.Q.get(s_hash,None) is None:
                curr.Q[s_hash] = {str((0,0)):0,str((0,1)):0,str((0,2)):0,str((1,0)):0,str((1,1)):0,str((1,2)):0,str((2,0)):0,str((2,1)):0,str((2,2)):0}
            a = curr.policy(s_hash,Board) # action
            
            states[curr] = [hash_board_r(s),str(a)] # keep track of the state and action pair of current player
           
            Board.place(curr.symbol,a) # perform the action
        
        
            s2 = Board.current_state()
            

            s = s2
            curr = flip_player[curr] # switch players
           
            if states[curr] != []: # if the current player had a turn
                
                curr_r = Board.reward(curr.reward, curr.punishment, curr.draw, curr.symbol)
                
                if Board.is_terminal(s2):
                    curr_target = curr_r

                    other_player = flip_player[curr] 
                    other_reward = Board.reward(other_player.reward, other_player.punishment, other_player.draw, other_player.symbol)
                    if other_player.Q.get(s_hash,None) is not None:
                        other_player.Q[s_hash] = {str((0,0)):0,str((0,1)):0,str((0,2)):0,str((1,0)):0,str((1,1)):0,str((1,2)):0,str((2,0)):0,str((2,1)):0,str((2,2)):0}
                        
                    other_player.Q[s_hash][str(a)]+= other_player.alpha*(other_reward - other_player.Q[s_hash][str(a)])
                    
                    
                
                s_hash = states[curr][0]
                prev_a = states[curr][1]
                

                s2_hash = hash_board_r(s)
                if curr.Q.get(s2_hash,None) is None:
                    curr.Q[s2_hash] = {str((0,0)):0,str((0,1)):0,str((0,2)):0,str((1,0)):0,str((1,1)):0,str((1,2)):0,str((2,0)):0,str((2,1)):0,str((2,2)):0}
                a2 = random.choice([k for k,v in curr.Q[s2_hash].items() if v == max(curr.Q[s2_hash].values())])
                curr.Q[s_hash][prev_a] += curr.alpha*(curr_r+curr.gamma*curr.Q[s2_hash][a2]- curr.Q[s_hash][prev_a])
                

                states[curr] = []
    
    return player1,player2