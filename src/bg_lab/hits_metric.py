from .imetric import IMetric
from .match_recorder import MatchRecording
from bg_game.game_types import (
    Color, WHITE, BLACK
)

def _hits(recording: MatchRecording, color: Color) -> int:
    """Count how many times `color` hit an opponent checker."""
    hits = 0
    opponent_color = BLACK if color == WHITE else WHITE
    
    for i in range(len(recording.rounds) - 1):
        snapshot_before, _ = recording.rounds[i]
        snapshot_after, _ = recording.rounds[i + 1]
        
        if snapshot_before.player != color:
            continue
            
        bar_before = snapshot_before.world_state.bar[opponent_color]
        bar_after = snapshot_after.world_state.bar[opponent_color]
        
        if bar_after > bar_before:
            hits += bar_after - bar_before
    
    return hits

class HitsMetric(IMetric):
    def __init__(self, color: Color):
        self._color: Color = color
    
    @property
    def id(self) -> str:
        color_name = "white" if self._color == WHITE else "black"
        return f"hits_{color_name}"
    
    def compute(self, recording: MatchRecording) -> int:
        return _hits(recording, self._color)