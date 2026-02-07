import logging
from typing import Optional
from bg_game.game_types import NUM_CHECKERS_EACH, WorldState, Color, Action, Dice, NUM_POINTS, Point, WHITE, BLACK, BAR, OFF
from bg_game.backgammon import Backgammon

log = logging.getLogger(__name__)

class GameOverError(RuntimeError):
    pass

class EngineAdapter:
    """
    Adapter for https://github.com/dellalibera/gym-backgammon
    backgammon implemention.
    """
    def __init__(self):
        self.engine = Backgammon()
        self._winner: Optional[Color] = None

    def winner(self) -> Optional[Color]:
        """
        Warning:
            winner() == False
        if winner () == WHITE
        => Check with: winner() is not None
        """
        return self._winner
    
    def _update_winner_from_ws(self, ws: WorldState) -> None:
        if ws.off[WHITE] == NUM_CHECKERS_EACH:
            self._winner = WHITE
        elif ws.off[BLACK] == NUM_CHECKERS_EACH:
            self._winner = BLACK
        else:
            self._winner = None

    def _ensure_not_over(self) -> None:
        if self._winner is not None:
            raise GameOverError(f"Game is already over! Winner: {self._winner}")
	
    def get_state(self) -> WorldState:
        """
        Returns current state of the board in
        convenient representation.
        """
        self._ensure_not_over()

        ws: WorldState = self._current_world_state()
        log.debug(f"Built WorldState from FeatureVector:\n{ws}")
        return ws
    
    def _current_world_state(self) -> WorldState:
        """
        Gets Feature Vector representation from engine.
        Converts it to a more suitable representation for our agents
        to work with. 
        """
        fv = self.engine.get_board_features(WHITE) # color does not matter for us
        return EngineAdapter._feature_vector_to_world_state(fv)

	
    def get_actions(self, agent_color: Color, dice: Dice) -> list[Action]:
        """
        Returns list of all legal actions. 
        According to WorldState represenation;
        i.e. WHITE moves backwards.
        Provide non-negative Dice for both agents!
        """
        self._ensure_not_over()
        
        assert all(x > 0 for x in dice)

        # Engine expects WHITE to move backwards
        engine_dice = dice
        if agent_color == WHITE:
            x, y = dice
            engine_dice = (-x, -y)

        engine_actions = list(self.engine.get_valid_plays(agent_color, engine_dice))
        actions: list[Action] = self._convert_actions(engine_actions)
        log.debug(f"Received Dice: {dice} (handing over {engine_dice}) -> received valid actions:\n{actions}")
        return actions
    
    def _convert_actions(self, engine_actions) -> list[Action]:
        """
        Engine ("bar"/ <0 (white), >23 (black)) -> intern (BAR=-1/OFF=24).
        """
        converted: list[Action] = []

        for action in engine_actions:
            new_action: Action = tuple(
                (
                    (BAR if frm == "bar" else frm),
                    (OFF if 0 > to or to >= NUM_POINTS else to),
                )
                for (frm, to) in action
            )
            converted.append(new_action)
        
        for a in converted: 
            self._assert_internal_action(a) 
        
        return converted
    
    def _assert_internal_action(self, action: Action) -> None:
        for frm, to in action:
            assert isinstance(frm, int)
            assert frm == BAR or 0 <= frm < NUM_POINTS

            assert isinstance(to, int)
            assert to == OFF or 0 <= to < NUM_POINTS

    def step(self, agent_color: Color, action: Action) -> None:
        """
        Executes the Agent's action. 
        Updates the environment accordingly.
        Expects actions encoded according to WorldState;
        i.e. WHITE must go from higher to lower index.
        """
        log.debug(f"Agent with color {agent_color} attempts to take action {action}.")
        
        self._ensure_not_over()
        
        engine_action = self._convert_back(action, agent_color)
        self._assert_engine_action(engine_action)
        self.engine.execute_play(agent_color, engine_action)

        ws: WorldState = self._current_world_state()
        self._update_winner_from_ws(ws)

    def _convert_back(self, action: Action, color: Color) -> tuple:
        engine_actions_list = []
        for frm, to in action:
            engine_frm = "bar" if frm == BAR else frm

            engine_to = to 
            if to == OFF and color == WHITE:
                engine_to = -1
            if to == OFF and color == BLACK:
                engine_to = 24

            engine_actions_list.append((engine_frm, engine_to))

        return tuple(engine_actions_list)
        
    
    def _assert_engine_action(self, engine_action) -> None:
        """
        Assert that the generated engine action only contains
        valid entries.
        """
        for frm, to in engine_action:
            if isinstance(frm, int):
                assert 0 <= frm < NUM_POINTS   
            else:
                assert frm == "bar"
            """
            if isinstance(to, int):
                assert 0 <= to < NUM_POINTS    
            else:
                assert to == "off"
            """
            # off is represented by int<0 or int>23
            # -> all ints are allowed
            assert isinstance(to, int)

    @staticmethod
    def _feature_vector_to_world_state(feature_vector) -> WorldState:
        """
        Converts the engines representation of the board (feature-vector)
        to this projects general representation of the board (WorldState).
        """
        SZ_UNIT = 4 # [float, float, float, float] for each position
        SZ_BOARD_REP = NUM_POINTS * SZ_UNIT # each position is represented as a unit 

        # WHITE
        features_white = feature_vector[:SZ_BOARD_REP]
        bar_white = round(feature_vector[SZ_BOARD_REP] * 2) # FV stores bar/2
        off_white = round(feature_vector[SZ_BOARD_REP + 1] * 15) # FV stores off/15
        
        # BLACK
        features_black = feature_vector[SZ_BOARD_REP + 2: 2 * SZ_BOARD_REP + 2]
        bar_black = round(feature_vector[2 * SZ_BOARD_REP + 2] * 2)
        off_black = round(feature_vector[2 * SZ_BOARD_REP + 3] * 15)

        def _handle_unit(unit: list[float]) -> Point:
            """
            Transforms [float, float, float, float] to a Point.
            Expects black entries to be signed. 
            """
            if unit[0] == 0:
                return (0, None) # Position is empty
            elif unit[0] == 1.0:
                color = WHITE # WHITE is represented as 1
            else:
                color = BLACK # BLACK is represented as -1
            
            if unit[3] != 0:
                # encoded: unit[3] = (checkers - 3) / 2
                if color == WHITE:
                    no_checkers = round(unit[3] * 2) + 3
                    return (no_checkers, WHITE)
                else:
                    # change sign back to + for BLACK
                    no_checkers = round(-unit[3] * 2) + 3
                    return (no_checkers, BLACK)
            if unit[2] != 0:
                return (3,color)
            if unit[1] != 0:
                return (2, color)
            return (1, color)
        
        points_list: list[Point] = []

        # Combine WHITE/BLACK representation, where <0 represents BLACK presence
        combined_board_rep = [w - b for w, b in zip(features_white, features_black)]
        assert len(combined_board_rep) == NUM_POINTS * SZ_UNIT
        
        for i in range(0, len(combined_board_rep), SZ_UNIT):
            point = _handle_unit(combined_board_rep[i:i+SZ_UNIT])
            points_list.append(point)
        
        return WorldState(
            points = tuple(points_list),
            off = (off_white, off_black),
            bar = (bar_white, bar_black)
        ) 
