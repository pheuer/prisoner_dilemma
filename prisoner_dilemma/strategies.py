import numpy as np

__all__ = [
    "Strategy",
    "RandomChoice",
    "Gullible",
    "TitForTat",
]



class Strategy:
    
    def __init__(self):
        pass
    
    
    def choose(self, history):
        """
        history => Game history 
        
        # Define so the bot is always the first index, and the opponent
        # is always the second (so, fip the history when passing to bot 1)
        
        """
        
        
        ... 
        
class Gullible(Strategy):
    def choose(self, history):
        return 1
    
    
    
class HoldsGrudge(Strategy):
    """
    Cooperates until the oppoent defects once, then defects thereafter 
    """
    
    def choose(self, history):
        
        op_defections = np.where(history[:, 1]==0)
        
        if len(op_defections) == 0:
            return 1
        else:
            return 0
        
    
class RandomChoice(Strategy):
    def choose(self, history):
        return np.random.choice(np.array([0,1]),)
    
    
class TitForTat(Strategy):
    def choose(self, history):
        
        if history.shape[0] == 0:
            return 1
        
        other_player_last_move = history[-1, 1]
        
        if other_player_last_move == 1:
            return 1
        else:
            return 0
        
        
class Joss(Strategy):
    """
    TitForTat, except with a 10% chance of defection on any given round
    """
    def choose(self, history):
        
        if history.shape[0] == 0:
            return 1
        
        other_player_last_move = history[-1, 1]
        
        rint = np.random.random()
        
        if other_player_last_move == 1 and rint>0.1:
            return 1
        else:
            return 0
        
        
        
        
    
if __name__ == '__main__':
    bot = RandomChoice()