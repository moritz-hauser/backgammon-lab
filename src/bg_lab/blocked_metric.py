from .imetric import IMetric
from .match_recorder import MatchRecording
from bg_game.game_types import (
    Color, WHITE, BLACK,
)

class BlockedMetric(IMetric):
    def __init__(self, color: Color):
        self._color = color
    
    @property
    def id(self) -> str:
        color_name = "white" if self._color == WHITE else "black"
        return f"blocked_{color_name}"
    
    def compute(self, recording: MatchRecording) -> int:
        times = 0
        for snapshot, action in recording.rounds:
            if action is None and snapshot.player == self._color:
                times += 1
        return times
