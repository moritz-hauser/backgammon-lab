from typing import Callable, Optional
from bg_game.game_types import (
    WorldState, Color, 
    Dice, Action, 
    RoundSnapshot
    )

SnapshotObserver = Callable[[RoundSnapshot], None]
ActionObserver = Callable[[Action], None]
WinnerObserver = Callable[[Optional[Color]], None]

class GameStateModel:
    """
    Implements Observer-Model to be observerd by UI-Elements and such. 
    """
    def __init__(self):
        self.round_snapshot: RoundSnapshot
        self.action_taken: Action
        self.winner: Optional[Color] = None

        self.snapshot_observers: list[SnapshotObserver] = []
        self.action_observers: list[ActionObserver] = []
        self.winner_observers: list[WinnerObserver]= []

    # API for Controller
    def update_round_snapshot(self, round_snapshot: RoundSnapshot):
        self.round_snapshot = round_snapshot
        self._notify_snapshot_observers()

    def update_action_taken(self, action_taken: Action):
        self.action_taken = action_taken
        self._notify_action_observers()

    def update_winner(self, winner: Optional[Color]):
        self.winner = winner
        self._notify_winner_observers()

    # API for Observers
    def on_new_round_snapshot(self, obs: SnapshotObserver):
        self.snapshot_observers.append(obs)

    def on_new_action_taken(self, obs: ActionObserver):
        self.action_observers.append(obs)

    def on_game_over(self, obs: WinnerObserver):
        self.winner_observers.append(obs)

    # Notify observers
    def _notify_snapshot_observers(self):
        for fn in self.snapshot_observers:
            fn(self.round_snapshot)

    def _notify_action_observers(self):
        for fn in self.action_observers:
            fn(self.action_taken)

    def _notify_winner_observers(self):
        for fn in self.winner_observers:
            fn(self.winner)