from abc import ABC, abstractmethod
from bg_game.game_types import (
    AgentPerspectiveState, Action,
    WorldState, BLACK
    )
from bg_game.engine_adapter import EngineAdapter

class TransitionModel:
    """
    Predicts outcome of an action
    taken in a state.
    """

    def result(self, aps: AgentPerspectiveState, aps_action: Action) -> AgentPerspectiveState:
        """
        Predicts outcome of an action in agent perspective.
    
        We always treat the agent as BLACK when converting to WorldState.
        This works because:
        - In APS, both colors move 0→23 (agent's forward direction)
        - Converting with BLACK preserves this 0→23 direction in WS
        - Actions in APS map directly to WS actions without modification
        """
        COLOR = BLACK
        
        # Get WS representation of agents's perspective of the board
        before_ws = WorldState.from_agent_perspective_state(aps, COLOR)

        # Build an engine in with the current board
        ad = EngineAdapter()
        ad.engine.bar = before_ws.bar
        ad.engine.off = before_ws.off
        ad.engine.board = before_ws.points

        # aps_action = ws_action because color is BLACK
        ad.step(COLOR, aps_action)
        result_ws = ad.get_state()

        return AgentPerspectiveState.from_world_state(result_ws, COLOR)



class IAgent(ABC):
    """
    Interface for Backgammon-Playing-Agents.
    Provides self.transition_model to predict outcomes of actions.
    """
    def __init__(self) -> None:
        self.transition_model = TransitionModel()

    @abstractmethod
    def choose_action(
            self, 
            state: AgentPerspectiveState, 
            actions: list[Action]
            ) -> Action:
        ...
    