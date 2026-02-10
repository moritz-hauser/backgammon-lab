from typing import Optional
from bg_agents.iagent import IAgent
from bg_game.game_types import (
    AgentPerspectiveState, Action,
)
import logging



log = logging.getLogger(__name__) 

class SimpleUtilityBasedAgent(IAgent):
    """
    Very simple utility based agent with 
    one-step lookahead (greedy).
    """
    
    def _utility(self, state: AgentPerspectiveState) -> int:
        """
        Calculates the utility of a certain state. 
        The higher the utility, the more desirable the state.
        """
        utility = 0

        # Increase utility for hit enemies
        utility += state.bar_enemy

        # Increase utility for off moves
        utility += 2 * state.off_me

        for amount_checkers in state.points:
            # This agent likes safe points
            if amount_checkers >= 2: 
                utility += 1

        return utility
    
    def choose_action(
            self, 
            state: AgentPerspectiveState, 
            actions: list[Action]
        ) -> Action:
        """
        Choose action with highest utility.
        action* = argmax_{action} (U(Result(action)))
        """
        assert actions

        action_utilities = [
            (action, self._utility(self.transition_model.result(state, action)))
            for action in actions
        ]

        best_action, util = max(action_utilities, key=lambda x: x[1])

        assert best_action is not None
        log.info(f"Highest utility ({util}) found for action {best_action}.")

        return best_action