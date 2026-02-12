from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias, Literal

WHITE: Literal[0] = 0
BLACK: Literal[1] = 1
Color = Literal[0, 1]

BAR = -1
OFF = 24

NUM_POINTS = 24
NUM_CHECKERS_EACH = 15

Move: TypeAlias = tuple[int, int]
Action: TypeAlias = tuple[Move, ...]
Dice: TypeAlias = tuple[int, int]

Point: TypeAlias = tuple[int, Color | None]  # (checkers, color)
Points: TypeAlias = tuple[Point, ...]  # length 24

@dataclass(frozen=True, slots=True)
class RoundSnapshot:
    """
    Snapshot of the game at some round
    """
    world_state: WorldState
    player: Color
    dice: Dice
    legal_actions: list[Action]

@dataclass(frozen=True, slots=True)
class WorldState:
    """
    Default representation for a state of a backgammon game.
    Used for analysis.
    """
    points: Points               # length 24
    off: tuple[int, int]         # [WHITE, BLACK]
    bar: tuple[int, int]         # [WHITE, BLACK]

    def __post_init__(self):
        assert len(self.points) == NUM_POINTS
        for n, c in self.points:
            assert n >= 0
            assert (n == 0) == (c is None)
            if c is not None:
                assert c in (WHITE, BLACK)
        assert all(x >= 0 for x in self.off)
        assert all(x >= 0 for x in self.bar)

    def amount_off(self, color: Color) -> int:
        return self.off[color]

    def amount_bar(self, color: Color) -> int:
        return self.bar[color]
    
    @staticmethod
    def from_agent_perspective_state(aps: AgentPerspectiveState, me_color: Color) -> WorldState:
        # Order based on color
        ws_off = (aps.off_me, aps.off_enemy) if me_color == WHITE else (aps.off_enemy, aps.off_me)
        ws_bar = (aps.bar_me, aps.bar_enemy) if me_color == WHITE else (aps.bar_enemy, aps.bar_me)

        # Points
        ws_points: list[Point] = []
        aps_points: list[int] = list(aps.points)

        enemy_color = BLACK if me_color == WHITE else WHITE

        # Convert points in order of agent perspective
        for amount_checkers in aps_points:
            if amount_checkers < 0: # enemy-checkers
                point: Point = (abs(amount_checkers), enemy_color)
                ws_points.append(point)
            elif amount_checkers > 0: # my checkers
                point: Point = (amount_checkers, me_color)
                ws_points.append(point)
            else: # empty
                ws_points.append((0, None))

        # WHITE goes backwards in WS
        if me_color == WHITE:
            ws_points.reverse() 

        return WorldState(
            points=tuple(ws_points),
            off=ws_off,
            bar=ws_bar,
        )


@dataclass(frozen=True, slots=True)
class AgentPerspectiveState:
    """
    State from a specific agent's perspective.
    points[i] < 0 enemy checkers, > 0 my checkers.
    """
    points: tuple[int, ...]
    off_me: int
    off_enemy: int
    bar_me: int
    bar_enemy: int

    def __post_init__(self):
        assert len(self.points) == NUM_POINTS
        assert self.off_me >= 0
        assert self.off_enemy >= 0
        assert self.bar_me >= 0
        assert self.bar_enemy >= 0
        me_total = self.off_me + self.bar_me + sum(x for x in self.points if x > 0)
        enemy_total = self.off_enemy + self.bar_enemy + sum(-x for x in self.points if x < 0)
        assert me_total == NUM_CHECKERS_EACH
        assert enemy_total == NUM_CHECKERS_EACH

    @staticmethod
    def from_world_state(ws: WorldState, me: Color) -> AgentPerspectiveState:
        enemy = WHITE if me == BLACK else BLACK

        bar_me = ws.bar[me]
        bar_enemy = ws.bar[enemy]
        off_me = ws.off[me]
        off_enemy = ws.off[enemy]

        aps_points_list: list[int] = []

        for amount, color in ws.points:
            if color == me:
                aps_amount = amount
            elif color == enemy:
                aps_amount = -amount
            else:
                aps_amount = 0
            aps_points_list.append(aps_amount)

        if me == WHITE:
            aps_points_list.reverse() 

        return AgentPerspectiveState(
            points=tuple(aps_points_list),
            bar_me=bar_me,
            bar_enemy=bar_enemy,
            off_me=off_me,
            off_enemy=off_enemy
        )
    
    @staticmethod
    def _flip_actions_if_white(actions: list[Action], me: Color) -> list[Action]:
        """
        This is required because WHITE walks backwards in 
        WorldState but both players walk forward
        in their internal AgentPerspectiveState,
        and calculate their moves accordingly.
        """
        if me == BLACK:
            return actions

        def flip(i: int) -> int:
            # BAR and OFF are equal in WS and APS
            if i == OFF or i == BAR: 
                return i
            return NUM_POINTS - 1 - i

        def flip_move(m: Move) -> Move:
            frm, to = m
            return (flip(frm), flip(to))

        return [tuple(flip_move(mv) for mv in a) for a in actions]

    @staticmethod
    def ws_actions_to_aps_actions(
        actions: list[Action],
        me: Color
    ) -> list[Action]:
        return AgentPerspectiveState._flip_actions_if_white(actions, me)
    
    @staticmethod
    def aps_action_to_ws_action(
        action: Action,
        me: Color
    ) -> Action:
        flipped = AgentPerspectiveState._flip_actions_if_white([action], me)
        return flipped[0]
    
    @staticmethod
    def get_enemy_perspective(state: AgentPerspectiveState) -> AgentPerspectiveState:
        """
        Get same state from enemy's perspective.
        """
        return AgentPerspectiveState(
            # Reverse order and sign
            points=tuple(-p for p in state.points[::-1]),
            off_me=state.off_enemy,
            off_enemy=state.off_me,
            bar_me=state.bar_enemy,
            bar_enemy=state.bar_me
        )