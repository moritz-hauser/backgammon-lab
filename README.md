# Backgammon Lab

A framework for developing and evaluating backgammon AI agents.

## Overview

Backgammon Lab provides a modular environment for testing different backgammon agents against each other. Built on top of [gym-backgammon](https://github.com/dellalibera/gym-backgammon), it offers tools for running matches, recording games, and analyzing agent performance.

To provide a strong enemy for benchmarks this project uses [gnubg-nn-pypi](https://github.com/reayd-falmouth/gnubg-nn-pypi/tree/main?tab=readme-ov-file). GNUBG is optional, and not required for core features.

## Key Features

- **Decoupled Architecture:** Clean Model-View-Controller (MVC) structure separating game logic from views and agent policies.
- **Pluggable AI Agents:** Easily implement and benchmark custom heuristics, RL models, or baseline algorithms against external engines.
- **GNU Backgammon Integration:** Includes a wrapper/adapter for `gnubg-nn-pypi` to provide high-level benchmarks against expert-level Neural Network evaluations.
- **Developer-Ready:** Fully type-hinted, includes custom type stubs, and features a complete `pytest` test suite.

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
Alternatively, to install developer tools (such as pytest):
```bash
pip install -e ".[dev]"
```
With GNU Backgammon support (optional):
```bash
pip install -e ".[gnubg]"
```

This will install all declared dependencies.  


### Development Setup

For running tests:
```bash
pip install -e ".[dev]"
```

## Quick Start
```python
from bg_game.game_state_model import GameStateModel
from bg_view.cli_view import CliView
from bg_game.game_controller import GameController
from bg_game.game_types import BLACK, WHITE
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

See `examples/` for more usage examples.

## Project Structure
```
backgammon-lab/
├── src/
│   ├── bg_agents/      # Agent implementations
│   ├── bg_lab/         # Components for analysis (Lab, etc.)
│   ├── bg_game/        # Core game engine (Engine, GameController, etc.)
│   ├── bg_gnubg/       # Adapter for GNUBG
│   └── bg_view/        # Views (CLI, etc.)
├── tests/              # Unit tests
├── typings/            # Type stubs for external libraries
├── documentation/      # UML
├── examples/           # Usage examples
└── pyproject.toml      # Project configuration
```

## Testing

Run tests with pytest:
```bash
pytest
```

Only run tests that are not marked slow:
```bash
pytest -m "not slow"
```

## VSCode
Add to your workspace settings:
```json
{
  "python.analysis.stubPath": "typings"
}
```

## Development Status

This project is in early development (v0.0.0). 

## License

TBD
