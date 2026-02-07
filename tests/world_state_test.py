import pytest
from bg_game.game_types import WorldState, Point, Points, WHITE, BLACK, NUM_POINTS, NUM_CHECKERS_EACH

def _empty_points_list() -> list[Point]:
    empty_point: Point = (0, None)
    return [empty_point] * NUM_POINTS

def _empty_points() -> Points:
    return tuple(_empty_points_list())

def test_build_with_sensible_data_is_consistent():

    points_list = _empty_points_list()

    """
    Place each players checkers at the very last field
    in their homebase
    """
    points_list[23] = (NUM_CHECKERS_EACH, WHITE)
    points_list[0] = (NUM_CHECKERS_EACH, BLACK)

    ws = WorldState(
        points = tuple(points_list),
        off = (0, 0),
        bar = (0, 0)
    )

    assert ws.bar == (0, 0)
    assert ws.off == (0, 0)

    assert ws.amount_bar(WHITE) == 0
    assert ws.amount_bar(BLACK) == 0
    assert ws.amount_off(WHITE) == 0
    assert ws.amount_off(BLACK) == 0

    assert len(ws.points) == NUM_POINTS

    assert ws.points[23] == (NUM_CHECKERS_EACH, WHITE)
    assert ws.points[0] == (NUM_CHECKERS_EACH, BLACK)

    for i in range(NUM_POINTS):
        if i not in (0, 23):
            assert ws.points[i] == (0, None)

    # All checkers are on the board in this scenario
    assert sum(n for n, c in ws.points if c == WHITE) == NUM_CHECKERS_EACH
    assert sum(n for n, c in ws.points if c == BLACK) == NUM_CHECKERS_EACH

    assert all((n == 0) == (c is None) for n, c in ws.points)

def test_amount_off_and_bar_indexing():
    ws = WorldState(points=_empty_points(), off=(3, 7), bar=(1, 2))
    assert ws.amount_off(WHITE) == 3
    assert ws.amount_off(BLACK) == 7
    assert ws.amount_bar(WHITE) == 1
    assert ws.amount_bar(BLACK) == 2

def test_invalid_points_length_triggers_assert():
    with pytest.raises(AssertionError):
        WorldState(points=tuple([(0, None)] * 23), off=(0, 0), bar=(0, 0))

def test_negative_checker_triggers_assert():
    bad = _empty_points_list()
    bad[0] = (-1, None)  # n < 0
    with pytest.raises(AssertionError):
        WorldState(points=tuple(bad), off=(0, 0), bar=(0, 0))

def test_nonzero_with_none_color_triggers_assert():
    bad = _empty_points_list()
    bad[0] = (1, None)  # n != 0 but c is None
    with pytest.raises(AssertionError):
        WorldState(points=tuple(bad), off=(0, 0), bar=(0, 0))

def test_zero_with_color_triggers_assert():
    bad = _empty_points_list()
    bad[0] = (0, WHITE)  # n == 0 but c not None
    with pytest.raises(AssertionError):
        WorldState(points=tuple(bad), off=(0, 0), bar=(0, 0))

def test_negative_off_or_bar_triggers_assert():
    with pytest.raises(AssertionError):
        WorldState(points=_empty_points(), off=(-1, 0), bar=(0, 0))
    with pytest.raises(AssertionError):
        WorldState(points=_empty_points(), off=(0, 0), bar=(0, -2))
