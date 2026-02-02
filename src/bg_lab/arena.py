from gym_backgammon.envs.backgammon import WHITE, BLACK
import random
from itertools import count
import gym

class Arena:

    def roll_dice(self):
        return (random.randint(1,6), random.randint(1,6))
        
    def compete(self, agent1, agent2):
        env = gym.make('gym_backgammon:backgammon-v0', disable_env_checker=True)

        agents = {WHITE: agent1, BLACK: agent2}
        
        agent_color, first_roll, observation = env.reset()
        
        current_agent = agents[agent_color] # Agent to start

        for round_i in count():
            # Environment handles the first roll
            if first_roll:
        	    roll = first_roll
        	    first_roll = None
            else: 
        	    roll = self.roll_dice()
        	    # WHITE goes "backwards"
        	    roll = roll if agent_color == BLACK else (-roll[0], -roll[1]) 
        		
            valid_actions = env.get_valid_actions(roll)
        	
            action = current_agent.choose_action(valid_actions, env)
        	
        	# Do not require reward for now
            observation, _, done, winner = env.step(action)
        	
            if done:
                env.close()
                # This may happen in case maximum amount of rounds is exceeded
                if winner is None:
                    return None
                return agents[winner]
        	
            agent_color = env.get_opponent_agent()
            current_agent = agents[agent_color]
        	
