import os
import random
import numpy as np
from game import Game


LR = 0.01

class Q_tab:
    def __init__(self, size=1000, default=-1):
        self.size = size
        self.default = default
        self.table:np.ndarray = np.random.rand(*(3,3))
    def save(self, file_name='model.pth'):
        folder_path = './Q_Tabel'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_name = os.path.join(folder_path, file_name)
        np.save('matrix.npy', self.table)

    def _hash_function(self, key):
        return np.argmax(key[0]), np.argmax(key[1]) 

    def __getitem__(self, key):
        state , action = self._hash_function(key)
        return self.table[state , action]

    def __setitem__(self, key, value):
        
        state , action = self._hash_function(key)
        self.table[state , action] = value 


    def get_values_with_first_key(self, first_key):
        first_key  = np.argmax(first_key)
        return self.table[first_key,:]

    def get_best_action(self, first_key):
        values = self.get_values_with_first_key(first_key)
        return values.argmax(axis=0)

    def max_aQ__s_a__(self, first_key):
        values = self.get_values_with_first_key(first_key)
        if values.any():
            return max(values)
        return -1

    def normalize(self):
        def np_soft_max(row_or_colum):
            return np.exp(row_or_colum ) / np.sum(np.exp(row_or_colum))
        self.table[0:1,:] = np_soft_max(self.table[0:1,:]) 
        self.table[1:2,:] = np_soft_max(self.table[1:2,:]) 
        self.table[2:3,:] = np_soft_max(self.table[2:3,:]) 

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.Q_tab:Q_tab = Q_tab()
    
    def get_state(self, game: Game):

        
        differs = game.get_differs()
        
        # + game.falling_object.width // 2 + game.player.width // 2
        is_inside = abs(differs)  < game.width_sum 
        is_on_right = not is_inside and (  differs > 0 ) 
        is_on_left = not is_inside and (  differs < 0 ) 
        state = [
            int(is_on_left),
            int(is_inside),
            int(is_on_right),
        ]
        return state





    def get_action(self, state,game: Game):
        
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 20 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon and(
            not ((self.n_games + 1) % 5 == 0)
        ):
            game.move_source = "rand"
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            
            game.move_source = "Q-Tab"
            move = self.Q_tab.get_best_action(state) # np.argmax(self.Q_tab.max_aQ__s_a__(state))
            final_move[move] = 1
            return final_move

        return final_move


