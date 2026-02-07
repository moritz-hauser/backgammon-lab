import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger('bg_lab.arena').setLevel(logging.INFO)
logging.getLogger('bg_game.engine_adapter').setLevel(logging.INFO)