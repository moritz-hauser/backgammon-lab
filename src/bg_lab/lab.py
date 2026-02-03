from bg_lab.arena import Arena
from bg_agents.random_agent import RandomAgent
import logging

log = logging.getLogger(__name__) 

class Lab:

    def __init__(self, arena):
        log.info("Called constructor for Lab.")
        self.arena = arena

    def match_up(self, agent1, agent2):
        log.info("Called method match_up().")
        return self.arena.compete(agent1, agent2) 
