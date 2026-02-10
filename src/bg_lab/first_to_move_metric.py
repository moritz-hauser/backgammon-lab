from .imetric import IMetric
from .match_recorder import MatchRecording

from bg_game.game_types import Color, WHITE, BLACK

class FirstToMoveMetric(IMetric):
    @property
    def id(self) -> str:
        return "first_to_move"
    
    def compute(self, recording: MatchRecording) -> Color:
        first_state = recording.get_snapshots()[0]
        return first_state.player