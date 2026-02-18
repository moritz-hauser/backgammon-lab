from typing import Optional
from unittest.mock import MagicMock
import pytest

from bg_agents.random_agent import RandomAgent
from bg_game.game_controller import GameController, MaxRoundsError
from bg_game.game_types import BLACK, WHITE, Color
from bg_agents.gnubg_agent import GnubgAgent
from bg_agents.simple_utility_based_agent import SimpleUtilityBasedAgent

@pytest.mark.slow
def test_gnubg_agent_vs_rand_agent():
    matches = 100

    for match in range(matches):

        gc: GameController = GameController(MagicMock())

        gnubg: GnubgAgent = GnubgAgent()
        rand: RandomAgent = RandomAgent()

        agents = {WHITE: gnubg, BLACK: rand}

        try:
            winner_color: Optional[Color] = gc.compete(
                white_agent=agents[WHITE],
                black_agent=agents[BLACK]
                )
        except MaxRoundsError as mre:
            continue
        
        assert winner_color is not None
        winner: RandomAgent = agents[winner_color]
        
        assert winner is gnubg or winner is rand

@pytest.mark.slow
def test_gnubg_agent_vs_util_agent():
    matches = 100

    for match in range(matches):

        gc: GameController = GameController(MagicMock())

        gnubg: GnubgAgent = GnubgAgent()
        util: SimpleUtilityBasedAgent = SimpleUtilityBasedAgent()

        agents = {WHITE: gnubg, BLACK: util}

        try:
            winner_color: Optional[Color] = gc.compete(
                white_agent=agents[WHITE],
                black_agent=agents[BLACK]
                )
        except MaxRoundsError as mre:
            continue
        
        assert winner_color is not None
        winner: RandomAgent = agents[winner_color]
        
        assert winner is gnubg or winner is util

