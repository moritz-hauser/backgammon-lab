from bg_agents.iagent import IAgent
from bg_game.game_types import (
    AgentPerspectiveState,
    Action,
    Dice,
    NUM_CHECKERS_EACH,
)
import logging
import numpy as np
import math

log = logging.getLogger(__name__)

# Indices of features (for debugging)
BLOPS = 0
OFF_ME = 1
OFF_ENEM = 2
BAR_ME = 3
BAR_ENEM = 4

AMOUNT_FEATURES = 5

def starting_weights() -> np.ndarray:
    """
    Returns the weights to start 
    training with.
    """
    weight = np.empty(AMOUNT_FEATURES)
    
    # May kickstart by estimating
    weight[BLOPS] = 0.0
    weight[OFF_ME] = 0.0
    weight[OFF_ENEM] = 0.0
    weight[BAR_ME] = 0.0
    weight[BAR_ENEM] = 0.0

    return weight


def feature_functions() -> np.ndarray:
    """
    For each feature a function to extract
    it from a given AgentPerspectiveState.

    Features should be roughly on the same scale, to avoid 
    large features (like off_count) to dominate.
    For example:
    When bar_me is 1 and off_me is 8, this affects off way
    stronger, even though the checker on bar is usually the
    one that makes the position bad.
    """
    functions = [lambda s: 0.0 for _ in range(AMOUNT_FEATURES)]

    # We treat everything greater than 4 the same, 
    # making the low numbers more impactful
    functions[BLOPS] = lambda s: min(s.points.count(1)/5, 1.0)

    functions[OFF_ME] = lambda s: s.off_me / NUM_CHECKERS_EACH
    functions[OFF_ENEM] = lambda s: s.off_enemy / NUM_CHECKERS_EACH

    # Same rationale as for BLOPS above
    functions[BAR_ME] = lambda s: min(s.bar_me/4, 1.0)
    functions[BAR_ENEM] = lambda s: min(s.bar_enemy/4, 1.0)

    return np.array(functions)


def sigmoid(x): return 1 / (1 + math.exp(-x))

class TDAgent(IAgent):

    def __init__(self) -> None:
        super().__init__()

        self.weights: np.ndarray = starting_weights()
        self.feature_fn: np.ndarray = feature_functions()

        assert len(self.weights) == len(self.feature_fn)

        self.previous_features: list[float] = []
        self.previous_utility: float = 0.0

    
    def choose_action(
            self, 
            state: AgentPerspectiveState,
            dice: Dice, 
            actions: list[Action]
        ) -> Action:

        action_features_utility: list[tuple] = []
        for action in actions:
            next_state = self.transition_model.result(state, action)
            next_features = [f(next_state) for f in self.feature_fn]
            next_utility = sigmoid(self.weights @ next_features)

            action_features_utility.append((action, next_features, next_utility))

        best_action, features, utility =  max(action_features_utility, key=lambda x: x[2])

        log.debug(f"Decided on best action: {best_action}, resulting in features: {features}, with utility: {utility}")

        self._update_weights(new_utility=utility)

        log.debug(f"Updated weights to: {self.weights}")

        self.previous_features = features
        self.previous_utility = utility

        return best_action
    

    def on_game_over(self, won: bool) -> None:
        self._update_weights(new_utility=1.0) if won else self._update_weights(new_utility=0.0)

        log.info(f"{'Won' if won else 'Lost'} the game, updated weights to {self.weights}")

        self.previous_features = []
        self.previous_utility = 0.0

    
    def _update_weights(self, new_utility: float):
        # w += alpha * TDerror * feature
        # instead:
        # w += alpha * TDerror * eligibility_trace
        # where et measures how active a feature was in past couple rounds
        # to remember past moves
        
        # Cant update weights at first round
        if not self.previous_features:
            return
        
        # arbitrary, TODO decide 
        ALPHA = 0.01 

        # large if underestimated -> must increase weights
        td_error = new_utility - self.previous_utility
        
        for i, w in enumerate(self.weights):
            # we want features that contributed more
            # to the error to be changed more
            self.weights[i] = w + ALPHA * td_error * self.previous_features[i]
