import random

class RandomAgent:
    def choose_action(self, actions, env):
        return random.choice(list(actions)) if actions else None
