from typing import Optional
from unittest.mock import MagicMock
from bg_game.game_controller import GameController, MaxRoundsError
from bg_agents.random_agent import RandomAgent
from bg_game.game_types import BLACK, WHITE, Color
import pytest

@pytest.mark.slow
def test_many_games_rand_agents():
    matches = 100
    for match in range(matches):

        gc: GameController = GameController(MagicMock())

        a1: RandomAgent = RandomAgent()
        a2: RandomAgent = RandomAgent()

        agents = {WHITE: a1, BLACK: a2}

        try:
            winner_color: Optional[Color] = gc.compete(
                white_agent=agents[WHITE],
                black_agent=agents[BLACK]
                )
        except MaxRoundsError as mre:
            continue
        
        assert winner_color is not None
        winner: RandomAgent = agents[winner_color]
        
        assert winner is a1 or winner is a2

        

