import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import numpy as np


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
    
    def train_step(self, last_move, action, reward, next_state, end):
        state = torch.tensor(np.array(last_move), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(np.array(action), dtype=torch.long)
        reward = torch.tensor(np.array(reward), dtype=torch.float)


        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            end = (end, )
            
        # 1: predicted Q values with current state
        pred = self.model(state)
        
        target = pred.clone()
        
        for i in range(len(end)):
            Q_new = reward[i]
            if not end[i]:
                next_pred = self.model(next_state[i])
                max_next_pred = torch.max(next_pred)
                Q_new = reward[i] + self.gamma * max_next_pred
            
            target[i][action[i]] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred.gather(1, action.unsqueeze(1)).squeeze(1))
        loss.backward()
        
        self.optimizer.step()