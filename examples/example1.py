from typing import Optional

from bg_game.game_state_model import GameStateModel
from bg_view.cli_view import CliView
from bg_game.game_controller import GameController
from bg_game.game_types import Color, WHITE, BLACK
from bg_agents.random_agent import RandomAgent

# Model-View-Controller pattern
model = GameStateModel()    # Stores information about current rounds and informs observers of changes
cli = CliView(model)        # Observers model, prints state of the game accordingly
gc = GameController(model)  # Manages match between two agents, updates the model

# Winner will be returned as color, so it is important to remember which agent has which color
agents: dict[Color, RandomAgent] = {WHITE: RandomAgent(), BLACK: RandomAgent()}

# Winner may be None if maximum amount of rounds is exceeded
winner: Color = gc.compete(white_agent=agents[WHITE], black_agent=agents[BLACK])

print(f"Winner: {winner} / {agents[winner]}")
