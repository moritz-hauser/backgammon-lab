import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger('bg_agents.simple_utility_based_agent').setLevel(logging.WARNING)
logging.getLogger('bg_agents.my_agent').setLevel(logging.WARNING)