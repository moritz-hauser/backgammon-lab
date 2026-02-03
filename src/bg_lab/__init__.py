import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger('bg_lab.lab').setLevel(logging.DEBUG)
logging.getLogger('bg_lab.arena').setLevel(logging.WARNING)