import random
from bg_agents.iagent import IAgent
from bg_game.game_types import AgentPerspectiveState, Action

class RandomAgent(IAgent):
    """
    Chooses random action from list of legal actions.
    """
    
    def choose_action(self, state: AgentPerspectiveState, actions: list[Action]) -> Action:
        assert actions, "Agent received no legal actions"
        return random.choice(actions)
