from dataclasses import dataclass
from typing import Optional, TypeAlias
from bg_game.game_state_model import GameStateModel
from bg_game.game_types import (
    RoundSnapshot, Action, Color
)

RoundsData: TypeAlias = tuple[tuple[RoundSnapshot, Optional[Action]], ...]

@dataclass (frozen=True)
class MatchRecording:
    rounds: RoundsData
    winner: Optional[Color]

    def get_winner(self)-> Optional[Color]:
        return self.winner
    
    def get_snapshots(self) -> tuple[RoundSnapshot, ...]:
        return tuple([snapshot for snapshot, _ in self.rounds])
    
    def get_actions(self) -> tuple[Optional[Action], ...]:
        return tuple([action for _, action in self.rounds])

class MatchRecorder:

    def __init__(self, model: GameStateModel):
        self.model = model
        self.model.on_new_round_snapshot(self.on_round_snapshot)
        self.model.on_new_action_taken(self.on_new_action)
        self.model.on_game_over(self.on_winner_updated)

        self.snapshots: list[RoundSnapshot] = []
        self.actions_taken: list[Optional[Action]] = []
        self.winner: Optional[Color] = None

    def on_round_snapshot(self, rs: RoundSnapshot):
        self.snapshots.append(rs)

    def on_new_action(self, action: Optional[Action]):
        self.actions_taken.append(action)

    def on_winner_updated(self, winner: Optional[Color]):
        self.winner = winner
    
    def get_recording(self) -> MatchRecording:
        assert len(self.actions_taken) > 0
        assert len(self.actions_taken) == len(self.snapshots), f"{len(self.actions_taken)} != {len(self.snapshots)}"

        n_rounds = len(self.actions_taken)
        rounds: RoundsData = tuple(zip(self.snapshots, self.actions_taken))

        return MatchRecording(
            rounds=rounds,
            winner=self.winner
        )
    