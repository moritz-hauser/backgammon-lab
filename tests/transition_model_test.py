from bg_agents.iagent import TransitionModel
from bg_game.game_types import (
    NUM_POINTS,
    Action,
    AgentPerspectiveState,
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
    points_list[20] = -2    # Enemy safe
    points_list[22] = 2     # My checkers
    points_list[23] = -9    # Enemy mostly home
    
    return AgentPerspectiveState(
        points=tuple(points_list),
        bar_me=0,
        bar_enemy=0,
        off_me=0,
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
    points_list[23] = -5
    # My checkers elsewhere on the board
    points_list[12] = 2
    points_list[15] = 3
    points_list[18] = 4
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
    desired_action: Action = ((0, 3), (),)
    # Build initials aps
    # Test with one transition
    # Check results manually


def test_transition_works_for_hitting():
    # Build aps with open enemy
    # Test transition with hitting action
    # Check result

def test_transition_works_for_going_off():
    # Build aps with checkers in homezone
    # Test transition with going off action
    # Check result

def test_transition_works_for_entering_from_bar():
    # Build aps with checkers on bar
    # Enter from bar
    # Check result

def test_transition_for_complex_action():
    # Build aps
    # Checker on bar
    # Open enemy
    # -> Enter hitting
    # Check result
