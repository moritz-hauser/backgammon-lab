from bg_game.arena import Arena, MaxRoundsError
from bg_agents.random_agent import RandomAgent
from bg_game.game_types import BLACK, WHITE, Color

def test_many_games_rand_agents():
    matches = 100
    for match in range(matches):
        arena: Arena = Arena()

        a1: RandomAgent = RandomAgent()
        a2: RandomAgent = RandomAgent()

        agents = {WHITE: a1, BLACK: a2}

        try:
            winner_color: Color = arena.compete(
                white_agent=agents[WHITE],
                black_agent=agents[BLACK]
                )
        except MaxRoundsError as mre:
            continue

        winner: RandomAgent = agents[winner_color]
        
        assert winner is a1 or winner is a2

        

