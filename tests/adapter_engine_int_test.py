import pytest
from unittest.mock import MagicMock

from bg_game.engine_adapter import EngineAdapter
from bg_game.game_types import (
    WHITE, BLACK, Color,
    NUM_POINTS,
    Move, Action, Dice,
    Point, Points,
    WorldState,
    BAR, OFF,
)

def _empty_points_list() -> list[Point]:
        empty_point: Point = (0, None)
        return [empty_point] * NUM_POINTS

def _empty_points() -> Points:
    return tuple(_empty_points_list())

def _initial_ws() -> WorldState:
    """
    Returns expected initial WorldState.
    As of official Backgammon rules.
    """
    
    two_white: Point = (2, WHITE)
    two_black: Point = (2, BLACK)
    three_white: Point = (3, WHITE)
    three_black: Point = (3, BLACK)
    five_white: Point = (5, WHITE)
    five_black: Point = (5, BLACK)

    points_list: list[Point] = _empty_points_list()

    points_list[0] = two_black
    points_list[23] = two_white

    points_list[5] = five_white
    points_list[18] = five_black

    points_list[7] = three_white
    points_list[16] = three_black

    points_list[12] = five_white
    points_list[11] = five_black

    return WorldState(
        points=tuple(points_list),
        off=(0,0),
        bar=(0,0)
    )

def test_first_get_state_returns_initial_ws():
    ad = EngineAdapter()
    expected: WorldState = _initial_ws()
    
    actual: WorldState = ad.get_state()

    assert actual == expected

def test_state_changes_after_legal_step_and_remains_valid():
    ad = EngineAdapter()

    before = ad.get_state()
    dice: Dice = (1, 2)
    actions = ad.get_actions(WHITE, dice)
    assert len(actions) > 0

    ad.step(WHITE, actions[0])
    after = ad.get_state()

    def _total(ws: WorldState, color: Color) -> int:
        return sum(n for n, c in ws.points if c == color) + ws.off[color] + ws.bar[color]

    assert after != before
    assert len(after.points) == NUM_POINTS
    assert all(n >= 0 for n, _ in after.points)
    assert all((n == 0) == (c is None) for n, c in after.points)
    # after first move off/bar must still be 0
    assert all(x == 0 for x in after.off) 
    assert all(x == 0 for x in after.bar)
    # still 15 checkers of each color
    assert _total(after, WHITE) == 15
    assert _total(after, BLACK) == 15

def test_get_actions_returns_actions_in_expected_shape():
    ad = EngineAdapter()
    dice: Dice = (1, 2)
    actions: list[Action] = ad.get_actions(WHITE, dice)

    assert len(actions) > 0
    for action in actions:
        assert isinstance(action, tuple)
        assert len(action) > 0
        for move in action:
            assert isinstance(move, tuple) and len(move) == 2
            a, b = move
            assert isinstance(a, int) and isinstance(b, int)

def test_4_rounds_double_dice_and_blocked(): 
    ad: EngineAdapter = EngineAdapter()
    expected_initial_ws: WorldState = _initial_ws()
    actual_inital_ws: WorldState = ad.get_state()

    assert expected_initial_ws == actual_inital_ws

    """
    Round 1:
    - Standard opening
    """
    current_player: Color = BLACK
    dice: Dice = (6,1)
    desired_action: Action = ((11,17), (16,17),)
    actual_actions: list[Action] = ad.get_actions(current_player, dice)

    assert desired_action in actual_actions

    ad.step(current_player, desired_action)
    new_ws: WorldState = ad.get_state()

    # Check that the right checkers have moved to the target
    assert new_ws.points[17] == (2, BLACK)
    assert new_ws.points[11] == (4, BLACK)
    assert new_ws.points[16] == (2, BLACK)

    """
    Round 2:
    - Double dice
    - Long walk with the same checker
    - Leaving it open to be hit
    """
    current_player = WHITE
    dice = (1,1)
    desired_action = ((23,22),(22,21),(21,20),(20,19),)
    actual_actions: list[Action] = ad.get_actions(current_player, dice)

    assert desired_action in actual_actions

    ad.step(current_player, desired_action)
    new_ws = ad.get_state()

    # Check that the right checker has been moved to the target
    assert new_ws.points[23] == (1, WHITE)
    assert new_ws.points[19] == (1, WHITE)

    """
    Round 3: 
    - Hit both open checkers with a single black checker
    """
    current_player = BLACK
    dice = (1,4)
    desired_action = ((18,19),(19, 23))
    actual_actions = ad.get_actions(current_player, dice)

    assert desired_action in actual_actions

    ad.step(current_player, desired_action)
    new_ws = ad.get_state()

    # Check that the right checker has been moved to the target
    assert new_ws.points[18] == (4, BLACK)
    assert new_ws.points[23] == (1, BLACK)
    # Check that the WHITE checkers have been removed
    assert new_ws.points[19] == (0, None)
    assert new_ws.bar[WHITE] == 2

    """
    Round 4:
    - WHITE needs to enter two checkers on the bar
    - Rolls (6,6), which is blocked
    - No move possible
    """
    current_player = WHITE
    dice = (6,6)
    actual_actions = ad.get_actions(current_player, dice)

    # Actions should be empty
    assert not actual_actions

    # Nothing has changed from previous round
    assert new_ws == ad.get_state()

def test_game_reaches_bar_and_enters(capsys):
    ad: EngineAdapter = EngineAdapter()
    expected_initial_ws: WorldState = _initial_ws()
    actual_inital_ws: WorldState = ad.get_state()

    assert expected_initial_ws == actual_inital_ws

    """
    Round 1:
    - WHITE opens checkers to be hit
    """
    current_player: Color = WHITE
    dice: Dice = (1,1)
    #desired_action: Action = ((23, 22), (22,21), (5,4), (7,6) )
    desired_action: Action = ((23, 22), (22,21), (7,6), (5,4) )
    actual_actions: list[Action] = ad.get_actions(current_player, dice)

    assert desired_action in actual_actions
    captured = capsys.readouterr()
    print(captured.out)  

    ad.step(current_player, desired_action)

    """
    Round 2:
    - BLACK hits checkers @ 4 and 6
    """
    current_player = BLACK
    dice = (4,6)
    desired_action = ((0,4),(0,6),)
    actual_actions: list[Action] = ad.get_actions(current_player, dice)

    assert desired_action in actual_actions

    ad.step(current_player, desired_action)

    ws: WorldState = ad.get_state()

    assert ws.bar[WHITE] == 2

    """
    Round 3: 
    - WHITE enters both checker back into 23 and 22
    """
    current_player = WHITE
    dice = (1,2)
    desired_action = ((BAR, 23),(BAR, 22),)
    actual_actions = ad.get_actions(current_player, dice)

    assert desired_action in actual_actions

    ad.step(current_player, desired_action)

    ws = ad.get_state()
    
    assert ws.points[23] == (2, WHITE)
    assert ws.points[21] == (1, WHITE)
    assert ws.bar[WHITE] == 0
    assert ws.off[WHITE] == 0
    