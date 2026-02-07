from abc import ABC, abstractmethod
from bg_game.game_types import AgentPerspectiveState, Action

class IAgent(ABC):
    """
    Interface for Backgammon-Playing-Agents
    """
    @abstractmethod
    def choose_action(
            self, 
            state: AgentPerspectiveState, 
            actions: list[Action]
            ) -> Action:
        ...
    