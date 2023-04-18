from Chess import *
import torch
import random
from collections import deque
from Model import Linear_QNet, QTrainer
import numpy as np


MAX_MEM = 100000
BATCH_SIZE = 100
GENERAL_RANDOMNESS = 500
TRAIN_FOR = 40
LR = 0.005
GAMMA = 0.8



class Agent:
    
    def __init__(self, game: Chess, group: Groups):
        self.memory = deque(maxlen=MAX_MEM)
        self.game = game
        self.group = group
        self.n_games = 0
        self.model = Linear_QNet(32, 4, 1024)
        self.trainer = QTrainer(self.model, lr=LR, gamma=GAMMA)
        
    def get_relevant_information(self):
        infos = self.game.get_all_subject_info(Groups.WHITE) + self.game.get_all_subject_info(Groups.BLACK)
        print(len(infos))
        return np.array(infos, dtype=float)

    def remember(self, last_move, action, reward, next_state, end):
        self.memory.append((last_move, action, reward, next_state, end)) # Popleft if max memory
    
    def train_long_mem(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, end = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, end)
    
    
    def train_short_mem(self, last_move, action, reward, next_state, end):
        self.trainer.train_step(last_move, action, reward, next_state, end)
    
    
    def get_action(self, state) -> list[int]:
        self.randomness = GENERAL_RANDOMNESS - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 250) < self.randomness:
            final_move = [random.randint(1, KING_ID), random.randint(1, 8), random.randint(1, 8)] # as the king is the last element
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()

        return final_move
    
def train():
    plot_scores = []
    avg = []
    total_score = 0
    record = 0
    game = Chess()
    members = [Agent(game, Groups.WHITE), Agent(game, Groups.BLACK)]
    while True:
        agent = members[game.turn % 2]
        accepted = False
        state_old = agent.get_relevant_information()
        
        while not accepted:
            last_move = agent.get_action(state_old)
            print(last_move)
            try:
                game.create_playing_field()
                whose_turn = game.parties[game.turn % len(game.parties)]
                reward = game.play_next_move(whose_turn, [last_move[0], last_move[1], last_move[2]])
                reward += game.check_and_collide(game.id_into_character(whose_turn, last_move[0]))
                game.turn += 1
                accepted = True
            except UnallowedCoordinateError:
                pass

        
        state_new = agent.get_relevant_information()
        agent.train_short_mem(state_old, last_move, reward, state_new, game.is_dead)
        agent.remember(state_old, last_move, reward, state_new, game.is_dead)
        
        if game.is_dead:
            agent.train_long_mem()
            agent.n_games += 1
            
            if game.score > record:
                record = game.score
            print("Game: {}, Score: {}, Record: {}".format(agent.n_games, game.score, record))
            
            plot_scores.append(game.score)
            avg.append(np.mean(plot_scores))
            #plot.plot(plot_scores, avg)
    
if __name__ == "__main__":
    train()