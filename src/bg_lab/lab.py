from bg_lab.arena import Arena
from bg_agents.random_agent import RandomAgent

class Lab:

    def __init__(self, arena):
        self.arena = arena

    def match_up(self, agent1, agent2):
        return self.arena.compete(agent1, agent2) 
