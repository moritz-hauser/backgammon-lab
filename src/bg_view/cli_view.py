from typing import Optional
from bg_game.game_state_model import GameStateModel
from bg_game.game_types import (
    BLACK, WHITE, Color,
    WorldState, 
    Point, 
    NUM_POINTS, 
    Dice, Action,
    BAR, OFF,
    RoundSnapshot
)

PLAYERS = {WHITE: "🤖 (White)", BLACK: "🤓 (Black)"}

OFF_SYM = "✅"
BAR_SYM = "⏸️"

RIGHT_ARROW = "➡️ "
AND_SYM = "➕"

# Dice emojis are glitchy
SINGLE_DICE = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
}

CHECKERS = {WHITE: "⚪", BLACK: "⚫", None: "⬜"}
SEPARATOR = "⬛"

# Left in case I find non-glitchy emojis
DIGITS = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4",
    5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
}

NUM_SEP_L = ") "
NUM_SEP_R = " ("

class CliView:
    """
    Implements Observer-Pattern to observe
    GameStateModel.
    """

    def __init__(self, model: GameStateModel, show_legal_actions: bool = False):
        self.model = model
        self.show_legal_actions = show_legal_actions
        self.model.on_new_round_snapshot(self.on_round_snapshot)
        self.model.on_new_action_taken(self.on_new_action)
        self.model.on_game_over(self.on_winner_updated)
    
    # Functions to execute on Model notification
    def on_round_snapshot(self, rs: RoundSnapshot):
        self._display_round_snapshot(rs)

    def on_new_action(self, action: Action):
        self._display_action_taken(action)

    def on_winner_updated(self, winner: Optional[Color]):
        if winner is not None:
            self._display_winner(winner)

    # Methods to print rendered stuff
    def _display_round_snapshot(self, rs: RoundSnapshot):
        dice_rendered: str = self._render_dice(rs.dice)
        actions_rendered: str = self._render_actions(rs.legal_actions)
        player_rendered: str = self._render_player(rs.player)
        board_rendered: str = self._render_board(ws=rs.world_state)
    
        print("="*10 + f"{player_rendered} rolled dice: {dice_rendered}" + "="*10)
        
        colors: list[Color] = [WHITE, BLACK]
        for color in colors:
            if rs.world_state.off[color] != 0:
                print(OFF_SYM + " " + self._render_off(rs.world_state, color))
        
        print(board_rendered)

        for color in colors:
            if rs.world_state.bar[color] != 0:
                print(BAR_SYM + " " + self._render_bar(rs.world_state, color))

        if self.show_legal_actions:
            print("Available actions:")
            print(actions_rendered)

    def _display_action_taken(self, action: Action):
        action_rendered = self._render_action(action)
        print(f"=> decided on action: {action_rendered}\n")

    def _display_winner(self, winner: Optional[Color]):
        if winner is None:
            print("NO WINNER DETERMINED")
        else:
            winner_rendered = self._render_player(winner)
            print(f"Winner: {winner_rendered}")

    # Methods to render stuff
    def _render_number(self, i: int) -> str:
            # Numbers should have equal width (3 -> 03, etc.)
            return DIGITS[0] + DIGITS[i] if i < 10 else DIGITS[i // 10] + DIGITS[i%10]
    
    def _render_player(self, color: Color):
        return PLAYERS[color]

    def _render_dice(self, dice: Dice):
        a, b = dice
        return f"({SINGLE_DICE[a]} - {SINGLE_DICE[b]})"

    def _render_board(self, ws: WorldState) -> str:

        BOARD_HEIGHT = NUM_POINTS // 2

        def _highest_tower() -> int:
            max = 0
            for amount, _ in ws.points:
                max = amount if amount > max else max
            return max

        def _render_point(pnt: Point) -> str:
            POINT_LENGTH = max(_highest_tower(), 5)

            symbol = CHECKERS[pnt[1]]
            amount_symbol = pnt[0]
            amount_empty = POINT_LENGTH - pnt[0] # Fill the rest with filler

            return symbol * amount_symbol + CHECKERS[None] * amount_empty
        
        def _render_left_edge() -> list[str]:
            """Indices of the fist half (00-11)"""
            return [self._render_number(i) + NUM_SEP_L for i in range(BOARD_HEIGHT)]
        
        def _render_right_edge() -> list[str]:
            """Indices of the second half (12-23)"""
            return [NUM_SEP_R + self._render_number(i) for i in range(BOARD_HEIGHT, NUM_POINTS)][::-1]
        
        def _render_middle_lane() -> list[str]:
            """
            Renders middle lane containting bar and separator
            """
            result = []
            height = BOARD_HEIGHT # from top to bottom

            for i in range(height):
                result.append(SEPARATOR + " " + SEPARATOR)
            
            return result
        
        def _comb_rows(rows: list[list[str]]) -> list[str]:
            result = [""] * (BOARD_HEIGHT)

            for row in rows:
                result = [result[i] + symbols for i, symbols in enumerate(row)]

            return result
        
        left_pts = ws.points[0:BOARD_HEIGHT]                    # Left row [0-11]
        right_pts = ws.points[BOARD_HEIGHT:NUM_POINTS][::-1]    # Right row [12-23] (start at bottom)

        left_edge = _render_left_edge()
        left_half = [_render_point(pnt) for pnt in left_pts]
        middle_lane = _render_middle_lane()
        right_half = [_render_point(pnt)[::-1] for pnt in right_pts] # Stack starts from the right
        right_edge = _render_right_edge()

        comb = _comb_rows([left_edge, left_half, middle_lane, right_half, right_edge])

        board = '\n'.join(comb)

        return board
    
    def _render_action(self, action: Action) -> str:
        moves = []
        for frm, to in action:
            frm_render = BAR_SYM+" " if frm == BAR else self._render_number(frm)
            to_render = OFF_SYM if to == OFF else self._render_number(to)
            moves.append(f"({frm_render} {RIGHT_ARROW} {to_render})")
        return f" {AND_SYM} ".join(moves)

    def _render_actions(self, actions: list[Action]) -> str:
        actions_render = [self._render_action(action) for action in actions]
        return '\n'.join(actions_render)

    def _render_off(self, ws: WorldState, color: Color) -> str:
        return CHECKERS[color] * ws.amount_off(color)  
    
    def _render_bar(self, ws: WorldState, color: Color) -> str:
        return CHECKERS[color] * ws.amount_bar(color) 
            