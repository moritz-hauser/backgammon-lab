import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger('bg_game.game_controller').setLevel(logging.WARNING)
logging.getLogger('bg_game.engine_adapter').setLevel(logging.WARNING)