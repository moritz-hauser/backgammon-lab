from typing import Optional
from bg_game.engine_adapter import EngineAdapter as Engine
from bg_game.game_types import (
    WHITE, BLACK, 
    Dice, Color, WorldState, 
    AgentPerspectiveState, Action,
    RoundSnapshot
    )
from bg_agents.iagent import IAgent
from bg_game.game_state_model import GameStateModel
import random
import logging

log = logging.getLogger(__name__) 

MAX_ROUNDS = 2_000

class MaxRoundsError(RuntimeError):
    pass

class GameController:

    def __init__(self, model: GameStateModel):
        self.model = model

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

        # In case model still carries a winner from previous games
        self.model.update_winner(None)

        agents = {WHITE: white_agent, BLACK: black_agent}

        dice, current_color = self._roll_for_opening()
        first_roll: bool = True
        
        round = 0
        while engine.winner() is None:
            # Update player and round
            current_color = WHITE if current_color == BLACK else BLACK
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
            
            # Update model
            snapshot = RoundSnapshot(
                world_state=ws,
                player=current_color,
                dice=dice,
                legal_actions=ws_actions
            )
            self.model.update_round_snapshot(snapshot)

            # Blocked
            if not ws_actions:
                self.model.update_action_taken(None)
                continue
            
            # Get current players perspective on the board
            aps: AgentPerspectiveState = AgentPerspectiveState.from_world_state(ws, current_color)
            aps_actions: list[Action] = AgentPerspectiveState.ws_actions_to_aps_actions(ws_actions, current_color)

            current_agent = agents[current_color]
            aps_action: Action = current_agent.choose_action(
                state=aps, 
                dice=dice,
                actions=aps_actions
                )
            
            # Turn agent's action agent back to objective perspective of the board
            ws_action = AgentPerspectiveState.aps_action_to_ws_action(aps_action, current_color)

            # Update model with chosen action
            self.model.update_action_taken(action_taken=ws_action)

            engine.step(
                current_color, 
                ws_action
                )
            
        log.info(f"Match over after {round} rounds.")
        
        winner: Optional[Color] = engine.winner()
        
        # Update model with winner
        self.model.update_winner(winner)
        
        assert winner is not None, "Excited gameloop unexpectedly."
        return winner 
    