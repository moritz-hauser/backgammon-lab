from typing import cast
from bg_agents.random_agent import RandomAgent
from bg_game.game_types import Action, AgentPerspectiveState

def test_some_actions_random_agent_return_one_of_them():
    agent = RandomAgent()
    expected_actions: list[Action] = [
        ((1,2),(5,7)),
        ((19,23),(14,20)),
        ((7,13),(12,16)),
        ]
    # Agent doesnt actually state, so this is OK here
    state = cast(AgentPerspectiveState, object())

    chosen_action = agent.choose_action(state=state, actions=expected_actions)
    
    assert chosen_action in expected_actions
