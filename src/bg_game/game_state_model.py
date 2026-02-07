from typing import Callable, Optional
from bg_game.game_types import (
    WorldState, Color, 
    Dice, Action, 
    RoundSnapshot
    )

GSObserver = Callable[[RoundSnapshot], None]
ATObserver = Callable[[Action], None]
WinnerObserver = Callable[[Optional[Color]], None]

class GameStateModel:
    """
    Implements Observer-Model to be observerd by UI-Elements and such. 
    """
    def __init__(self):
        self.gs: RoundSnapshot
        self.at: Action
        self.winner: Optional[Color] = None

        self.gs_observers: list[GSObserver] = []
        self.at_observers: list[ATObserver] = []
        self.winner_observers: list[WinnerObserver]= []

    # API for Controller
    def update_round_snapshot(self, round_snapshot: RoundSnapshot):
        self.gs = round_snapshot
        self._notify_gs_observers()

    def update_action_taken(self, action_taken: Action):
        self.at = action_taken
        self._notify_at_observers()

    def update_winner(self, winner: Optional[Color]):
        self.winner = winner
        self._notify_winner_observers()

    # API for Observers
    def on_new_round_snapshot(self, obs: GSObserver):
        self.gs_observers.append(obs)

    def on_new_action_taken(self, obs: ATObserver):
        self.at_observers.append(obs)

    def on_game_over(self, obs: WinnerObserver):
        self.winner_observers.append(obs)

    # Notify observers
    def _notify_gs_observers(self):
        for fn in self.gs_observers:
            fn(self.gs)

    def _notify_at_observers(self):
        for fn in self.at_observers:
            fn(self.at)

    def _notify_winner_observers(self):
        for fn in self.winner_observers:
            fn(self.winner)