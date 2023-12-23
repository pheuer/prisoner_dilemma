"""
https://www.youtube.com/watch?v=mScpHTIi-kM&ab_channel=Veritasium
"""

import numpy as np

__all__ = [
    "Simulation",
]

import strategies as strat




class Simulation:
    
    def __init__(self, bot0, bot1, nturns=100):
        self.bots = [bot0, bot1]
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
    

    def play(self):
        """
        1 -> cooperate
        0 -> defect
        """
        
        for turn in range(self.nturns):
            
            # History up to this turn will be passed to players
            _history = self.history[:turn, :]

            choice_0 = self.bots[0].choose(_history)
            
            choice_1 = self.bots[1].choose(np.flip(_history, axis=1))
            
            #print(turn, choice_0, choice_1)
            
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
    def winner(self):
        self._enforce_order()
        return np.argmax(self.points)
            
  
            
class SimulationSeries:
    
    def __init__(self, bot1, bot2, nsamples=10, nturns=100):
        self.bot1 = bot1
        self.bot2 = bot2
        self.nsamples = nsamples
        self.nturns = nturns
        
        self.points = np.array([0,0])
        
        self.record = np.array([0,0])
        
        self.history = np.nan*np.zeros([self.nsamples, self.nturns, 2])
        
        self._executed = False
        
        
    def run(self):
        
        for s in range(self.nsamples):
            
            sim = Simulation(self.bot1, self.bot2, nturns=self.nturns)
            sim.play()
            self.points += sim.points
            
            # Record the history 
            self.history[s, :, :] = sim.history
            
            # Increment the win tracker
            self.record[sim.winner] += 1
            
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
    def winner(self):
        self._enforce_order()
        return np.argmax(self.points)
            
            
            
     
            
class Tournament:
    def __init__(self, *bots, nsamples=10, nturns=200):
        self.bots = np.array(bots)
        self.nsamples = nsamples
        self.nturns = nturns 
        
        self.points = np.zeros(len(self.bots))
        self.record = np.zeros(len(self.bots))
        
        self._executed = False
        
        
    def _enforce_order(self):
        if not self._executed:
            raise ValueError("Run series first!")
        
        
        
    def run(self):
        for i, bot1 in enumerate(self.bots):
            for j, bot2 in enumerate(self.bots):
                
                series = SimulationSeries(bot1(), bot2())
                series.run()
                
                self.points[i] += series.points[0]
                self.points[j] += series.points[1]
                
        self._executed = True
                
                
    @property
    def scores(self):
        return self.points
    
    
    def score_report(self):
        
        isort = np.flip(np.argsort(self.points))

        
        points_sorted = self.points[isort]
        bots_sorted = self.bots[isort]
        
        for i in range(self.bots.size):
            print(f"{bots_sorted[i].__name__}: {points_sorted[i]}")
            
            

                
                
                
                
if __name__ == '__main__':
    bots = [strat.RandomChoice, strat.TitForTat, strat.Gullible, strat.HoldsGrudge, strat.Joss]
    
    t = Tournament(*bots, nsamples=50, nturns=200)
    t.run()
    
    t.score_report()
    
    
    """
    sim = Simulation(strat.RandomChoice(), strat.TitForTat())
    sim.play()
    """
    
    

    """
    series = SimulationSeries(strat.RandomChoice(), strat.TitForTat())
    series.run()
    
    print(series.avg_guesses)
    print(series.avg_points)
    """
   
    
