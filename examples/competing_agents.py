from typing import Optional

from bg_game.game_state_model import GameStateModel
from bg_view.cli_view import CliView
from bg_game.game_controller import GameController, MaxRoundsError
from bg_game.game_types import Color, WHITE, BLACK
from bg_agents.my_agent import MyAgent
from bg_agents.iagent import IAgent
from bg_agents.simple_utility_based_agent import SimpleUtilityBasedAgent

"""
This is an example to illustrate how to build two agents,
and have them compete with command line visualization.
To better understand agent behaviour.
"""

# Model-View-Controller pattern
model = GameStateModel()    # Stores information about current rounds and informs observers of changes
cli = CliView(model)        # Observers model, prints state of the game accordingly
gc = GameController(model)  # Manages match between two agents, updates the model

# Winner will be returned as Color, so it is important to remember which agent has which Color
agents: dict[Color, IAgent] = {WHITE: SimpleUtilityBasedAgent(), BLACK: MyAgent()}

# GameController::compete throws in case the maximum of rounds is exceeded
try:
    winner: Color = gc.compete(white_agent=agents[WHITE], black_agent=agents[BLACK])
except MaxRoundsError as e:
    print(f"Match terminated: {e}")
