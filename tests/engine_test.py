import random
import warnings
from bg_game.backgammon import Backgammon
from bg_game.game_types import BLACK, WHITE
import copy

import pytest

def test_initial_state_all_actions_are_executable():
    _assert_all_actions_executable(Backgammon())

def test_late_game_all_actions_are_executable():
    dice_sequence = [
        (6, 6), (3, 1), (4, 4), (5, 2), (1, 1),
        (6, 3), (2, 2), (5, 5), (4, 1), (3, 3),
    ]

    late_game_engine = _engine_after(dice_sequence)

    _assert_all_actions_executable(late_game_engine)

def test_end_game_all_actions_are_executable():
    dice_sequence = [
        (6, 6), (6, 6), (6, 6), (6, 6), (6, 6),
        (6, 6), (6, 6), (6, 6), (6, 6), (6, 6),
        (6, 6), (6, 6), (6, 6), (6, 6), (6, 6),
    ]

    end_game_engine = _engine_after(dice_sequence)
    
    _assert_all_actions_executable(end_game_engine)

def _engine_after(dice_sequence) ->  Backgammon:
    """
    Gets an engine after agents roll dice_sequence,
    starting with WHITE.
    Does not guarantee which action from action is chosen
    after each roll.
    """
    engine = Backgammon()
    for round, dice in enumerate(dice_sequence):
        color = WHITE if round % 2 == 0 else BLACK
        engine_dice = (-dice[0], -dice[1]) if color == WHITE else dice
        actions = list(engine.get_valid_plays(color, engine_dice))
        
        if not actions:
            continue

        engine.execute_play(color, actions[0])

    return engine 
                 
def _assert_all_actions_executable(engine: Backgammon) -> None:
    dices = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    for color in (WHITE, BLACK):
        for dice in dices:
            engine_dice = (-dice[0], -dice[1]) if color == WHITE else dice
            actions = engine.get_valid_plays(color, engine_dice)
            for action in actions:
                engine0 = copy.deepcopy(engine)
                try:
                    engine0.execute_play(current_player=color, action=action)
                except Exception as e:
                    raise AssertionError(
                        f"execute_play failed for color={color}, dice={engine_dice}, action={action}"
                    ) from e

# FUZZY-TEST
@pytest.mark.slow
def test_many_random_games():
    """Smoke test: random agents play without crashes"""
    seed = 123
    random.seed(seed)

    for game_num in range(100):
        engine = Backgammon()
        MAX_ROUNDS = 2000  # Prevent infinite games
        
        color = None
        for round in range(MAX_ROUNDS):
            color = WHITE if color == BLACK else BLACK

            dice = (random.randint(1,6), random.randint(1,6))
            engine_dice = (-dice[0], -dice[1]) if color == WHITE else dice
            
            actions = list(engine.get_valid_plays(color, engine_dice))
            if not actions:
                continue
                
            action = random.choice(actions)
            try:
                engine.execute_play(color, action)
            except Exception as e:
                # Bei Fehler: State ausgeben für Reproduzierbarkeit
                raise AssertionError(
                    f"Game {game_num}, turn {round}, color={color}, "
                    f"dice={engine_dice}, action={action}"
                ) from e
            
            if engine.get_winner() is not None:
                break

        if engine.get_winner() is None:
            warnings.warn(f"Game {game_num} exceeded {MAX_ROUNDS} rounds without finishing")

           

            