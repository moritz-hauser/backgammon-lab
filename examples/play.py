from bg_view.cli_view import CliView
from bg_game.game_controller import GameController
from bg_game.game_state_model import GameStateModel
from bg_game.game_types import (
    Color, WHITE, BLACK, 
    Action, AgentPerspectiveState,
    BAR, OFF
    )
from bg_agents.random_agent import IAgent
from bg_agents.simple_utility_based_agent import SimpleUtilityBasedAgent

"""
This script may be used to explore game mechanics by playing yourself.
"""

# Symbols for output
DIGITS = {  # Note: Number emojis are glitchy, may find something good to put here
        0: "0", 1: "1", 2: "2", 3: "3", 4: "4",
        5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
    }
OFF_SYM = "✅"
BAR_SYM = "⏸️ "
RIGHT_ARROW = "➡️ "
AND_SYM = "➕"

class CliControlledAgent(IAgent):
    """
    Asks user for desired action. 
    """
    
    # Note: _render* methods are copied from cli_view.py
    def _render_number(self, i: int) -> str:
            # Numbers should have equal width (3 -> 03, etc.)
            return DIGITS[0] + DIGITS[i] if i < 10 else DIGITS[i // 10] + DIGITS[i%10]
    
    def _render_action(self, action: Action) -> str:
        moves = []
        for frm, to in action:
            frm_render = BAR_SYM if frm == BAR else self._render_number(frm)
            to_render = OFF_SYM if to == OFF else self._render_number(to)
            moves.append(f"({frm_render} {RIGHT_ARROW} {to_render})")
        return f" {AND_SYM} ".join(moves)   

    def choose_action(self, state: AgentPerspectiveState, actions: list[Action]) -> Action:
        assert actions, "Agent received no legal actions"

        # Print actions with index
        print("-- Legal actions:")
        for i, action in enumerate(actions, start=1):
            print(f"[{i}]: {self._render_action(action)}")

        # Ask player for input
        while True:
            choice = input("Choose action number ('q' to quit): ").strip().lower()
            if choice == "q":
                quit()
            try:
                idx = int(choice)
                if 1 <= idx <= len(actions):
                    return actions[idx - 1]
                print(f"Invalid number. Must be 1..{len(actions)}")
            except ValueError:
                print("Please enter a number or 'q'.")
        
human = CliControlledAgent()
ai = SimpleUtilityBasedAgent()

# Human must be BLACK for WorldState to match AgentPerspectiveState (WHITE goes backwards in WorldState)
agents: dict[Color, IAgent] = {WHITE: ai, BLACK: human}

model = GameStateModel()
cli = CliView(model)
gc = GameController(model)

gc.compete(white_agent=agents[WHITE], black_agent=agents[BLACK])