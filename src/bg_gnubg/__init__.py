import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger('bg_gnubg.gnubg_adapter').setLevel(logging.DEBUG)
