# Backgammon Lab

A framework for developing and evaluating backgammon AI agents.

## Overview

Backgammon Lab provides a modular environment for testing different backgammon agents against each other. Built on top of [gym-backgammon](https://github.com/dellalibera/gym-backgammon), it offers tools for running matches, recording games, and analyzing agent performance.

**Note:** Since we are not primarily interested in RL this project only uses the core backgammon engine without the gym implementation with an adapter to better suit the requirements of this project.

## Installation

### Prerequisites

- Python 3.8+
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/moritz-hauser/backgammon-lab.git
cd backgammon-lab
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the package in editable mode:
```bash
pip install -e .
```

This will install all declared dependencies.  
Note: `gym-backgammon` must be available in the environment (e.g. installed from GitHub).

### Development Setup

For running tests:
```bash
pip install pytest
```

## Quick Start
```python
from bg_view.cli_view import CliView
from bg_game.game_controller import GameController
from bg_game.game_state_model import GameStateModel
from bg_view.cli_view import CliView
from bg_agents.random_agent import RandomAgent

# Setup Model-View-Controller
model = GameStateModel()
cli = CliView(model)
gc = GameController(model)

# Create two agents
agents = {WHITE: RandomAgent(), BLACK: RandomAgent()}

# Let the agents compete
winner = gc.compete(white_agent=agents[WHITE], black_agent=agents[BLACK])
```

Run the script for cli output.
See `examples/` for more usage examples.

## Project Structure
```
backgammon-lab/
├── src/
│   ├── bg_agents/      # Agent implementations
│   └── bg_lab/         # Components for analysis (Lab, etc.)
│   └── bg_game/        # Core game engine (Engine, GameController, etc.)
│   └── bg_view/        # Views (CLI, etc.)
├── tests/              # Unit tests
├── documentation/      # UML
├── examples/           # Usage examples
└── pyproject.toml      # Project configuration
```

## Testing

Run tests with pytest:
```bash
pytest
```

## Development Status

This project is in early development (v0.0.0). 
## License

TBD
