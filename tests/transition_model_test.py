from bg_agents.iagent import TransitionModel
from bg_game.game_types import (
    NUM_POINTS,
    Action,
    AgentPerspectiveState, WorldState,
    WHITE, BLACK
)

def _initial_aps() -> AgentPerspectiveState:
    # Returns initial board from agent perspective
    points_list = [0] * NUM_POINTS
    points_list[0] = 2
    points_list[5] = -5
    points_list[7] = -3
    points_list[11] = 5
    points_list[12] = -5
    points_list[16] = 3
    points_list[18] = 5
    points_list[23] = -2

    return AgentPerspectiveState(
        points=tuple(points_list),
        bar_me=0,
        bar_enemy=0,
        off_me=0,
        off_enemy=0
    )

def _enemy_hittable_aps() -> AgentPerspectiveState:
    # Returns board with open enemy checkers to hit
    points_list = [0] * NUM_POINTS
    points_list[0] = 2      # My checkers near start
    points_list[1] = 2
    points_list[4] = -1     # Enemy blot (hittable)
    points_list[8] = -1     # Enemy blot (hittable)
    points_list[12] = -1    # Enemy blot (hittable)
    points_list[15] = 3     # My safe stack
    points_list[18] = 3
    points_list[20] = -3    # Enemy safe
    points_list[22] = 2     # My checkers
    points_list[23] = -9    # Enemy mostly home
    
    return AgentPerspectiveState(
        points=tuple(points_list),
        bar_me=0,
        bar_enemy=0,
        off_me=3,
        off_enemy=0
    )

def _end_game_aps() -> AgentPerspectiveState:
    # Returns board where all checkers are in homezone and can exit
    points_list = [0] * NUM_POINTS
    points_list[18] = 3     # My home board (points 18-23)
    points_list[19] = 4
    points_list[20] = 2
    points_list[21] = 3
    points_list[22] = 2
    points_list[23] = 1
    # Enemy also in their home
    points_list[0] = -2
    points_list[1] = -3
    points_list[2] = -4
    points_list[3] = -3
    points_list[4] = -2
    points_list[5] = -1
    
    return AgentPerspectiveState(
        points=tuple(points_list),
        bar_me=0,
        bar_enemy=0,
        off_me=0,
        off_enemy=0
    )

def _hit_from_bar_aps():
    # Returns board where my checkers are on the bar and can hit the enemy from there
    points_list = [0] * NUM_POINTS
    # Enemy has blots in their home board (my entry points 0-5)
    points_list[0] = -1     # Enemy blot - hittable when entering with 1
    points_list[2] = -1     # Enemy blot - hittable when entering with 3
    points_list[4] = -1     # Enemy blot - hittable when entering with 5
    # Enemy has some safe checkers
    points_list[6] = -3
    points_list[11] = -5
    points_list[23] = -4
    # My checkers elsewhere on the board
    points_list[12] = 2
    points_list[15] = 3
    points_list[18] = 2
    points_list[20] = 3
    points_list[22] = 3
    
    return AgentPerspectiveState(
        points=tuple(points_list),
        bar_me=2,           # I have 2 checkers on the bar
        bar_enemy=0,
        off_me=0,
        off_enemy=0
    )

def test_transition_works_for_normal_move():
    tm = TransitionModel()
    init_aps: AgentPerspectiveState = _initial_aps()
    action: Action = ((0, 1), (0,3),) # legal action
    
    actual: AgentPerspectiveState = tm.result(init_aps, action)

    assert actual.bar_enemy == 0
    assert actual.bar_me == 0
    assert actual.off_enemy == 0
    assert actual.off_me == 0

    assert actual.points[0] == 0
    assert actual.points[1] == 1
    assert actual.points[3] == 1



def test_transition_works_for_hitting():
    # Build aps with open enemy
    tm = TransitionModel()
    aps: AgentPerspectiveState = _enemy_hittable_aps()
    
    # Test transition with hitting action
    # Move from point 1 to point 4 (hits enemy blot) and point 0 to point 4
    action: Action = ((1, 4), (0, 4))  # assuming we roll (3, 4) or similar
    actual: AgentPerspectiveState = tm.result(aps, action)
    
    # Check result
    assert actual.bar_enemy == 1  # Enemy checker was hit and sent to bar
    assert actual.bar_me == 0
    assert actual.points[1] == 1  # One checker left at point 1
    assert actual.points[0] == 1  # One checker left at point 0
    assert actual.points[4] == 2  # Two of my checkers now on point 4


def test_transition_works_for_going_off():
    # Build aps with checkers in homezone
    tm = TransitionModel()
    aps: AgentPerspectiveState = _end_game_aps()
    
    # Test transition with going off action
    # Bear off from points 23 and 22 (exact rolls)
    action: Action = ((23, -1), (22, -1))  # -1 indicates bearing off
    actual: AgentPerspectiveState = tm.result(aps, action)
    
    # Check result
    assert actual.off_me == 2  # Two checkers borne off
    assert actual.off_enemy == 0
    assert actual.points[23] == 0  # Checker removed from point 23
    assert actual.points[22] == 1  # One checker left at point 22
    assert actual.bar_me == 0
    assert actual.bar_enemy == 0


def test_transition_works_for_entering_from_bar():
    # Build aps with checkers on bar
    tm = TransitionModel()
    aps: AgentPerspectiveState = _hit_from_bar_aps()
    
    # Enter from bar
    # Roll (1, 3) - enter at points 0 and 2, both hitting enemy blots
    action: Action = ((-1, 0), (-1, 2))  # -1 as source indicates entering from bar
    actual: AgentPerspectiveState = tm.result(aps, action)
    
    # Check result
    assert actual.bar_me == 0  # Both checkers entered from bar
    assert actual.bar_enemy == 2  # Two enemy checkers were hit
    assert actual.points[0] == 1  # My checker now on point 0
    assert actual.points[2] == 1  # My checker now on point 2
    assert actual.off_me == 0
    assert actual.off_enemy == 0


def test_transition_for_complex_action():
    # Build aps
    tm = TransitionModel()
    aps: AgentPerspectiveState = _hit_from_bar_aps()
    
    # Checker on bar + open enemy
    # -> Enter hitting, then move another checker
    # Roll (3, 4): Enter from bar to point 2 (hitting), then move from 12 to 16
    action: Action = ((-1, 2), (12, 16))
    actual: AgentPerspectiveState = tm.result(aps, action)
    
    # Check result
    assert actual.bar_me == 1  # One checker still on bar
    assert actual.bar_enemy == 1  # Enemy blot at point 2 was hit
    assert actual.points[2] == 1  # My checker entered and hit
    assert actual.points[12] == 1  # One checker left at point 12
    assert actual.points[16] == 1  # One checker moved to point 16

def test_same_transition_model_used_multiple_times():
    # Test that the same TransitionModel instance can be reused
    # and doesn't accumulate state between calls
    tm = TransitionModel()
    init_aps: AgentPerspectiveState = _initial_aps()
    
    # Define multiple legal actions (doubles scenarios - 4 moves each)
    actions = [
        # Doubles 1-1: Move four checkers by 1
        ((11, 13), (11, 13), (11, 13), (11, 13)),
        
        # Doubles 3-3: Move from different positions
        ((11, 14), (11, 14), (16, 19), (16, 19)),
        
        # Doubles 2-2: Another combination
        ((0, 2), (0, 2), (11, 13), (11, 13)),
        
        # Doubles 6-6: Larger moves
        ((11, 17), (11, 17), (11, 17), (18, 24)),
    ]
    
    results = []
    for action in actions:
        result = tm.result(init_aps, action)
        results.append(result)
        
        # None of the action lead to bar/off increase
        assert result.bar_me == 0
        assert result.bar_enemy == 0
        # assert result.off_me == 0 # last action takes a checker off the board
        assert result.off_enemy == 0
        
        # Verify original state unchanged
        assert init_aps.points[0] == 2
        assert init_aps.points[11] == 5
    
    # Verify all results are different (different actions led to different states)
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            assert results[i].points != results[j].points, \
                f"Actions {i} and {j} produced identical states"
    
    # Verify we can still use the same TransitionModel again
    final_result = tm.result(init_aps, actions[0])
    assert final_result.points == results[0].points    
