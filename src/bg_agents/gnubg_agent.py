from bg_agents.iagent import IAgent
from bg_game.game_types import Action, AgentPerspectiveState, Dice
from bg_gnubg.gnubg_adapter import GnuBgAdapter

import logging

log = logging.getLogger(__name__) 

class GnubgAgent(IAgent):
    """
    Uses the GnuBG Neural Network to determine the best
    possible move.
    """

    def __init__(self, ply: int = 1):
        self.ply = ply

    def choose_action(self, state: AgentPerspectiveState, dice: Dice, actions: list[Action]) -> Action:
        assert actions

        action = GnuBgAdapter.best_action_from_aps(aps=state, dice=dice)

        # Convert to sets for comparison (order doesn't matter)
        action_set = set(action) if action else set()
        
        # Find matching action in list
        for valid_action in actions:
            if set(valid_action) == action_set:
                #return valid_action
                return action # return original order of action
        
        # If no match found:
        #raise AssertionError(f"{action} (as set: {action_set}) not found in {actions}")

        """
        NOTE:
        - backgammon.py has a bug where dice(1,1) during bearing-off 
          does not generating moves to OFF
        - Engine can still execute the move, but it wont be in legal_action
        """

        log.warning(f"""
                    Desired action:
                    \n{action} 
                    \nis not in list of legal actions:
                    \n{actions}
                    \nCurrentState:
                    \n{state}
                    \nCurrent Dice:\n
                    {dice}
                    """)
        
        return action
    