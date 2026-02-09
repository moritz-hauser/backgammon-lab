from typing import Optional
from bg_agents.iagent import IAgent
from bg_game.game_types import (
    AgentPerspectiveState, Action,
)
import logging

"""
Utility based agent with one-step lookahead.
(Greedy)
"""

log = logging.getLogger(__name__) 

class UtilityBasedAgent(IAgent):

    def _utility(self, state: AgentPerspectiveState) -> int:
        #raise NotImplementedError("Utility function has not been implemented")
        utility: int = 0

        # Increase utility for hit enemies
        utility += state.bar_enemy

        # Increase utility for off moves
        utility += 2 * state.off_me

        for amount_checkers in state.points:
            match amount_checkers:
                case 1: 
                    utility -= 1    # Decrease utility for blops
                case 2: 
                    utility += 1    # Prefer small stacks over large ones
                case 3:
                    utility += 2    # Stack of 3 considered optimal (for flexibility)

        return utility

    
    def choose_action(self, state: AgentPerspectiveState, actions: list[Action]) -> Action:
        """
        Choose action with highest utility.
        action* = argmax_{action} (U(Result(action)))
        """
        assert actions, "Received empty list of actions."

        best_action: Optional[Action] = None
        best_utility = -100_000 # very small

        for action in actions:
            result_state = self.transition_model.result(state, action)

            utility = self._utility(result_state)

            if utility > best_utility:
                best_action = action
                best_utility = utility

        assert best_action is not None

        log.info(f"Highest utility ({best_utility}) found for action {best_action}.")

        return best_action