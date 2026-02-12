from bg_agents.iagent import IAgent
from bg_game.game_types import Action, AgentPerspectiveState, Dice
from bg_gnubg.gnubg_adapter import GnuBgAdapter


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

        assert action in actions

        return action
    
    def _reconstruct_dice(self, action: Action) -> Dice:
        # fails if only one move possible!
        # can we fully reconstruct dice from actions?
        # give agents dice? !!!
        diff = [to - frm for frm, to in action]
        return (diff[0], diff[1])