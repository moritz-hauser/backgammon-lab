from typing import Optional
from .match_recorder import MatchRecording
from .imetric import IMetric
from bg_game.game_types import Color

class WinnerMetric(IMetric):
    @property
    def id(self) -> str:
        return "winner"
    
    def compute(self, recording: MatchRecording) -> Optional[Color]:
        return recording.winner