from .iagent import IAgent
from bg_game.game_types import (
    AgentPerspectiveState, Action,
    NUM_CHECKERS_EACH,
    OFF, Dice
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
            dice: Dice,
            actions: list[Action]
        ) -> Action:
        """
        Choose action with highest utility.
        action* = argmax_{action} (U(Result(action)))
        """
        assert actions

        # If contact-phase is over, we dont have to worry about building primes etc.
        if _is_safe(state):
            log.info("Decided that state is safe.")
            return _best_bear_off(actions)

        # If hitting is still possible, we must consider playing safe
        action_utilities = [
            (action, self._utility(state, action)) for action in actions
        ]

        best_action, util = max(action_utilities, key=lambda x: x[1])

        assert best_action is not None
        log.info(f"Highest utility ({util}) found for action {best_action}.")

        return best_action
    
    def _utility(self, before_state: AgentPerspectiveState, action: Action) -> float:
        after_state: AgentPerspectiveState = self.transition_model.result(before_state, action)

        log.debug(f"Calculating utility of {action}:")

        # Increase utility for hit enemies (decrease if risky!)
        hit_util = _hit_util(before_state=before_state,
                          after_state=after_state
                        )
        log.debug(f"- Utility from hits: {hit_util}")

        # Reward anchor on enemy side
        anchor_util = _anchor_util(after_state=after_state)
        log.debug(f"- Utility from anchor: {anchor_util}")

        # Reward primes
        prime_util = _primes_util(after_state=after_state)
        log.debug(f"- Utility from prime: {prime_util}")

        # Punish blops
        blop_util = _blops_util(after_state=after_state)
        log.debug(f"- Utility from blops: {blop_util}")

        # NOTE: this gamephase is not worried about bearing off!

        util = hit_util + anchor_util + prime_util + blop_util
        return util
    

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


# AREAS OF THE BOARD
ENEM_HOME = list(range(0, 6))       # Enemy's home board
MINE_HOME = list(range(18, 24))     # My home board
PRIME_AREA = list(range(14, 21))    # 14-20 is where i'd like to build a prime


def _hit_util(before_state: AgentPerspectiveState, after_state: AgentPerspectiveState) -> float:
    """
    Returns utility of a state as of regard to
    enemies on the bar.
    """

    # No hit happened
    if after_state.bar_enemy == 0:
        return 0.0

    # Figure out where the hit(s) happened
    points_hit: list[int] = []
    for i, amount_checkers in enumerate(before_state.points):
        # One checker was there, is gone now
        if amount_checkers == -1 and after_state.points[i] >= 0:
            points_hit.append(i)

    util = 0.0

    # The closer the enemy was to his board, the better
    for i in points_hit:
        util += 24 - i # Hitting on last point is only worth 1

    # Correct for own risk:
    # How many own in homefield are hitable?
    hitables: list[int] = []
    for i in MINE_HOME:
        if after_state.points[i] == 1: 
            hitables.append(i)

    for hitable in hitables:
        util -= hitable

    return util


def _anchor_util(after_state: AgentPerspectiveState) -> float:
    """
    Calculates utility derived from anchor.
    (ie. safe points on enemy side)
    """
    util = 0.0

    # This is where an anchor is valuable
    ANCHOR_POSITIONS = list(range(0, 7))

    for i in ANCHOR_POSITIONS:
        if after_state.points[i] > 1:
            # Further out brings is better
            util += (i+1) * 2

    return util


def _primes_util(after_state: AgentPerspectiveState) -> float:
    """
    Reward the longest prime in PRIME_AREA
    """

    # Find longest prime in PRIME_AREA
    longest_prime: list[int] = []
    current_prime: list[int] = []
    for i in PRIME_AREA:
        amount_checkers = after_state.points[i]
        if amount_checkers > 1:
            current_prime.append(i)
        if amount_checkers <= 1:
            # Prime unterbrochen
            if len(current_prime) >= len(longest_prime):
                longest_prime = current_prime
            current_prime = []

    # Letzte Prime checken
    if len(current_prime) > len(longest_prime):
        longest_prime = current_prime
    
    util = 0.0
    for point in longest_prime:
        # Reward further out primes more
        util += point

    return util


def _blops_util(after_state: AgentPerspectiveState) -> float:
    """
    Punish blops
    """
    util = 0.0

    for i, amount_checkers in enumerate(after_state.points):
        if amount_checkers == 1:
            util -= i

    return util

