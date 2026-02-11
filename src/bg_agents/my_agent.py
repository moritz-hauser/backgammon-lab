from .iagent import IAgent
from bg_game.game_types import (
    AgentPerspectiveState, Action,
    NUM_CHECKERS_EACH,
    OFF
)
import logging

log = logging.getLogger(__name__) 

class MyAgent(IAgent):
    """
    My attempt at making a strong agent.
    Utility based agent with one-step lookahead.
    Differentiates between normal, and bear-off phase.
    """

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

        # If contact-phase is over, we dont have to worry about building primes etc.
        if _is_safe(state):
            return _best_bear_off(actions)

        # If hitting is still possible, we must consider playing safe
        action_utilities = [
            (action, _utility(self.transition_model.result(state, action)))
            for action in actions
        ]

        best_action, util = max(action_utilities, key=lambda x: x[1])

        assert best_action is not None
        log.info(f"Highest utility ({util}) found for action {best_action}.")

        return best_action
    

def _is_safe(state: AgentPerspectiveState) -> bool:
    """
    Returns True if all checkers are past
    enemy checkers.
    Hitting is no longer possible after this point.
    """
    if state.bar_me != 0 or state.bar_enemy != 0:
        return False
    
    # Check if there is a checker behind enemy checkers
    count = state.off_enemy
    for amount in state.points:
        if amount < 0:
            count += abs(amount)
        elif amount > 0:
            # Found checker behind enemy lines
            return False
        if count == NUM_CHECKERS_EACH:
            break
    # Checkers are fully separated
    return True
           
    
def _best_bear_off(actions: list[Action]) -> Action:
    """ 
    1) Prefers action that move the 
       most amount of checkers off the board

    2) If many actions possible, choose the
       one which moves the furthes behind 
       checker
    """
    # Get actions with highest bear-off
    optimal_actions = []
    highest_off_count = 0
    for action in actions:
        off_count = 0
        for _, target in action:
            if target == OFF:
                off_count += 1
        if off_count == highest_off_count:
            optimal_actions.append(action)
        if off_count > highest_off_count:
            highest_off_count = off_count
            optimal_actions = [action]

    if len(optimal_actions) == 1:
        return optimal_actions[0]

    # Take action that moves the furthest behind checkers
    lowest_sum_frm = 1_000 # High number
    optimal_action = None
    for action in optimal_actions:
        # Furthest behind = lowest sum of from
        sum_frm = 0
        for frm, _ in action:
            sum_frm += frm
        if sum_frm < lowest_sum_frm:
            lowest_sum_frm = sum_frm
            optimal_action = action

    assert optimal_action is not None
    return optimal_action


def _utility(state: AgentPerspectiveState) -> float:
    util: float = 0.0

    # Increase utility for hit enemies
    util += state.bar_enemy

    # Increase utility for off moves
    util += 2 * state.off_me

    for amount_checkers in state.points:
        if amount_checkers >= 2:
            util += 1

    return util

