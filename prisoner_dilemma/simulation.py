"""
https://www.youtube.com/watch?v=mScpHTIi-kM&ab_channel=Veritasium
"""

import numpy as np

__all__ = [
    "Simulation",
]

import strategies as strat




class Simulation:
    """
    Runs a game between two bots.
    """
    
    
    def __init__(self, bot0, bot1, nturns=100, commentary=False):
        self._commentary = commentary
        
        self.bots = [bot0(commentary=self._commentary),
                     bot1(commentary=self._commentary)]
        self.points = np.array([0,0])
        
        self.nturns = nturns 
        
        
        
        if self.nturns <10 or self.nturns>599:
            raise ValueError("Set nturns in the range [50, 599]")
        
        # Initiatialize array as larger than necessary to support 
        # hiding the end turn from the strategies
        #
        # Define so the bot is always the first index, and the opponent
        # is always the second (so, fip the history when passing to bot 1)
        self.history = np.nan*np.ones([600, 2])
        
        self._executed = False

        
        
    def _enforce_order(self):
        if not self._executed:
            raise ValueError("Run game first!")
    

    def run(self):
        """
        1 -> cooperate
        0 -> defect
        """
        
        if self._commentary:
            print(f"{self.bots[0].__class__.__name__} vs. {self.bots[1].__class__.__name__}")
        
        for turn in range(self.nturns):
            
            # History up to this turn will be passed to players
            _history = self.history[:turn, :]

            choice_0 = self.bots[0].choose(_history)
            
            choice_1 = self.bots[1].choose(np.flip(_history, axis=1))
            
            if self._commentary:
                print(f"{turn}: ({choice_0}, {choice_1})")
            
            if (choice_0 == 1) and (choice_1 == 1):
                self.points[0] += 3
                self.points[1] += 3
            elif  (choice_0 == 0) and  (choice_1 == 0):
                self.points[0] += 1
                self.points[1] += 1
            elif  (choice_0 == 1) and  (choice_1 == 0):
                self.points[0] += 0
                self.points[1] += 5
            elif  (choice_0 == 0) and  (choice_1 == 1):
                self.points[0] += 5
                self.points[1] += 0
               
            self.history[turn, 0] = choice_0
            self.history[turn, 1] = choice_1
        
        self.history = self.history[:self.nturns, :]
        
        self._executed = True
        
        
    @property
    def winner_index(self):
        self._enforce_order()
        
        
        if self.points[0]==self.points[1]:
            return None
        else:
            return np.argmax(self.points)
        
    @property
    def winner(self):
        index = self.winner_index
        
        if index is None:
            return None
        else:
            return self.bots[index]
            
  
            
class SimulationSeries:
    """
    Runs a series of games with the same parameters between two bots.
    """
    
    def __init__(self, bot1, bot2, nsamples=10, nturns=100, commentary=False):
        self.bots = [bot1, bot2]
        self.nsamples = nsamples
        self.nturns = nturns
        
        self.points = np.array([0,0])
        
        # [bot1, bot2, tie]
        self.record = np.array([0,0,0])
        
        self.history = np.nan*np.zeros([self.nsamples, self.nturns, 2])
        
        self._executed = False
        self._commentary = commentary
        
        
    def run(self):
        
        for s in range(self.nsamples):
            
            sim = Simulation(*self.bots, nturns=self.nturns,
                             commentary=self._commentary)
            sim.run()
            self.points += sim.points
            
            # Record the history 
            self.history[s, :, :] = sim.history
            
            # Increment the win tracker
            if sim.winner_index is None:
                self.record[-1] += 1
            else:
                self.record[sim.winner_index] += 1
                
                
        if np.sum(self.record) != self.nsamples:
            raise ValueError("Record does not match number of samples")
            
        self._executed = True
        
    def _enforce_order(self):
        if not self._executed:
            raise ValueError("Run series first!")
            
    @property
    def avg_points(self):
        self._enforce_order()
        return self.points / self.nsamples
        
    @property
    def avg_guesses(self):
        self._enforce_order()
        return np.mean(self.history, axis=(0,1))
    
    
    @property
    def winner_index(self):
        self._enforce_order()
        
        if self.points[0]==self.points[1]:
            return None
        else:
            return np.argmax(self.points)
            
    
    @property
    def winner(self):
        index = self.winner_index
        
        if index is None:
            return None
        else:
            return self.bots[index]

        
    
            
            
     
            
class Tournament:
    def __init__(self, *bots, nsamples=100, nturns=200, commentary=False):
        self.bots = np.array(bots)
        self.nsamples = nsamples
        self.nturns = nturns 
        
        self.points = np.zeros(len(self.bots))
        self.record = np.zeros(len(self.bots))
        
        self._executed = False
        self._commentary=commentary
        
        
    def _enforce_order(self):
        if not self._executed:
            raise ValueError("Run series first!")
        
        
        
    def run(self):
        for i, bot1 in enumerate(self.bots):
            for j, bot2 in enumerate(self.bots):
                
                series = SimulationSeries(bot1, bot2,
                                          nsamples=self.nsamples,
                                          nturns=self.nturns,
                                          commentary=self._commentary)
                series.run()
                
                if series.winner is None:
                    winner = 'Tie!'
                else:
                    winner = series.winner.__name__
                
                print(f"{bot1.__name__} vs. {bot2.__name__} : {series.record}) : Winner = {winner}")
                
                self.points[i] += series.points[0]
                self.points[j] += series.points[1]
                
        self._executed = True
                
                
    @property
    def scores(self):
        return self.points
    
    
    def score_report(self):
        
        isort = np.flip(np.argsort(self.points))

        # Calculate the average points per turn 
        # Each bot plays N+1 games, since it plays itself once
        points_per_turn = self.points/ self.nsamples / self.nturns / (self.bots.size + 1)  
        
        points_per_turn_sorted = points_per_turn[isort] 
        
        bots_sorted = self.bots[isort]
        
        
        print("**** SCORE BOARD ****")
        for i in range(self.bots.size):
            print(f"{bots_sorted[i].__name__}: {points_per_turn_sorted[i]:.2f}")
            
            

                
                
                
                
if __name__ == '__main__':
   
    bots = [strat.RandomChoice, strat.TitForTat, strat.HoldsGrudge, strat.Joss]
    
    t = Tournament(*bots, nsamples=100, nturns=200)
    t.run()
    
    t.score_report()
 
    
    
    """
    series = SimulationSeries(strat.RandomChoice(), strat.TitForTat())
    series.run()
    
    print(series.avg_guesses)
    print(series.avg_points)
    """
    
    
    """
    sim = Simulation(strat.Joss(), strat.TitForTat(), nturns=20, commentary=True)
    sim.run()
    """
    
   
    
