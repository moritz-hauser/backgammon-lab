from bg_agents.random_agent import RandomAgent


def test_no_actions_random_agent_returns_none():
    agent = RandomAgent()
    assert agent.choose_action([], None) is None

def test_some_actions_random_agent_return_one_of_them():
    agent = RandomAgent()
    actions = [("a",), ("b",), ("c",)]
    action = agent.choose_action(actions, None)
    assert action in actions
