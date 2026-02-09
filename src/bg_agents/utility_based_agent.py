from typing import Optional
from bg_agents.iagent import IAgent
from bg_game.game_types import (
    AgentPerspectiveState, Action,
)

"""
Utility based agent with one-step lookahead.
(Greedy)
"""

class UtilityBasedAgent(IAgent):

    def _utility(self, state: AgentPerspectiveState) -> int:
        raise NotImplementedError("Utility function has not been implemented")
    
    def _transition(self, state: AgentPerspectiveState, action: Action) -> AgentPerspectiveState:
        raise NotImplementedError("Result function has not been implemented.")
    
    def choose_action(self, state: AgentPerspectiveState, actions: list[Action]) -> Action:
        """
        Choose action with highest utility.
        action* = argmax_{action} (U(Result(action)))
        """
        assert actions, "Received empty list of actions."

        best_action: Optional[Action] = None
        best_utility = 0
        for action in actions:
            result_state = self.transition_model.result(state, action)
            utility = self._utility(result_state)
            if utility > best_utility:
                best_action = action
                best_utility = utility

        assert best_action is not None
        return best_action