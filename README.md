# Backgammon Lab

A framework for developing and evaluating backgammon AI agents.

## Overview

Backgammon Lab provides a modular environment for testing different backgammon agents against each other. Built on top of [gym-backgammon](https://github.com/dellalibera/gym-backgammon), it offers tools for running matches, recording games, and analyzing agent performance.

**Note:** This project uses the legacy `gym-backgammon` package (based on OpenAI Gym 0.26), not the newer Gymnasium framework.

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
from bg_lab.lab import Lab
from bg_lab.arena import Arena
from bg_agents.random_agent import RandomAgent

# Set up the lab
arena = Arena()
lab = Lab(arena)

# Create two agents
agent1 = RandomAgent()
agent2 = RandomAgent()

# Run a match
winner = lab.match_up(agent1, agent2)
print(f"Winner: {winner}")
```

See `examples/` for more usage examples.

## Project Structure
```
backgammon-lab/
├── src/
│   ├── bg_agents/      # Agent implementations
│   └── bg_lab/         # Core framework (Arena, Lab, etc.)
├── tests/              # Unit tests
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
