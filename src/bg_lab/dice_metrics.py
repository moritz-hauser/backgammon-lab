from .imetric import IMetric
from .match_recorder import MatchRecording
from bg_game.game_types import Color, WHITE, BLACK, Dice
from typing import List
import statistics


def _get_dice_rolls(recording: MatchRecording, color: Color) -> List[Dice]:
    """Extract all individual dice values for a given color."""
    dices = []
    
    for snapshot, action in recording.rounds:
        if snapshot.player == color:
            dices.append(snapshot.dice)
    
    return dices

def _calculate_value(dice: Dice) -> int:
    """Double rolls count double"""
    x, y = dice
    sum = x + y
    if x == y: 
        return 2*sum
    return sum


class DiceSumAvgMetric(IMetric):
    def __init__(self, color: Color):
        self._color: Color = color
    
    @property
    def id(self) -> str:
        color_name = "white" if self._color == WHITE else "black"
        return f"dice_sum_avg_{color_name}"
    
    def compute(self, recording: MatchRecording) -> float:
        dices = _get_dice_rolls(recording, self._color)
        
        values = []
        for dice in dices:
            values.append(_calculate_value(dice))

        return statistics.mean(values) if dices else 0.0


class DiceSumVarianceMetric(IMetric):
    def __init__(self, color: Color):
        self._color: Color = color
    
    @property
    def id(self) -> str:
        color_name = "white" if self._color == WHITE else "black"
        return f"dice_sum_variance_{color_name}"
    
    def compute(self, recording: MatchRecording) -> float:
        dices = _get_dice_rolls(recording, self._color)
        
        values = []
        for dice in dices:
            values.append(_calculate_value(dice))

        return statistics.variance(values) if len(dices) > 1 else 0.0
    
class DoublesCountMetric(IMetric):
    """Count how many doubles (Pasch) were rolled."""
    def __init__(self, color: Color):
        self._color = color
    
    @property
    def id(self) -> str:
        color_name = "white" if self._color == WHITE else "black"
        return f"doubles_count_{color_name}"
    
    def compute(self, recording: MatchRecording) -> int:
        doubles = 0
        
        for snapshot, action in recording.rounds:
            if snapshot.player == self._color:
                if snapshot.dice[0] == snapshot.dice[1]:
                    doubles += 1
        
        return doubles