from bg_game.engine_adapter import EngineAdapter as Engine
from bg_game.game_types import WHITE, BLACK, Dice, Color, WorldState, AgentPerspectiveState, Action
from bg_agents.iagent import IAgent
import random
import logging

log = logging.getLogger(__name__) 

MAX_ROUNDS = 2_000

class MaxRoundsError(RuntimeError):
    pass

class Arena:

    def _roll_dice(self) -> Dice:
        return (random.randint(1,6), random.randint(1,6))
    
    def _roll_for_opening(self)-> tuple[Dice, Color]:
        a, b = self._roll_dice()
        # Roll until dices are not equal
        while a == b: 
            a, b = self._roll_dice()

        # Pick random player to start
        if a > b:
            return (a,b), WHITE
        else:
            return (a,b), BLACK
        
    def compete(self, white_agent: IAgent, black_agent: IAgent) -> Color:
        engine: Engine = Engine()

        agents = {WHITE: white_agent, BLACK: black_agent}

        dice, current_color = self._roll_for_opening()
        first_roll: bool = True
        
        round = 0
        while engine.winner() is None:
            # Update player and round
            current_color = BLACK if current_color == WHITE else BLACK
            round += 1

            if round > MAX_ROUNDS:
                raise MaxRoundsError(f"Exceeded maximum amount of rounds allowed ({round}).")

            # First roll follows special rules
            if not first_roll: 
                dice = self._roll_dice()
            else:
                first_roll = False

            ws: WorldState = engine.get_state()
            ws_actions: list[Action] = engine.get_actions(current_color, dice)
            
            # Blocked
            if not ws_actions:
                continue
            
            # Get current players perspective on the board
            aps: AgentPerspectiveState = AgentPerspectiveState.from_world_state(ws, current_color)
            aps_actions: list[Action] = AgentPerspectiveState.ws_actions_to_aps_actions(ws_actions, current_color)

            current_agent = agents[current_color]
            aps_action: Action = current_agent.choose_action(
                state=aps, 
                actions=aps_actions
                )
            
            # Turn agent's action agent back to objective perspective of the board
            ws_action = AgentPerspectiveState.aps_action_to_ws_action(aps_action, current_color)
            engine.step(
                current_color, 
                ws_action
                )
        
        assert engine.winner() is not None, "Excited gameloop unexpectedly."
        return WHITE if engine.winner() == WHITE else BLACK
    