from bg_game.arena import Arena
from bg_agents.random_agent import RandomAgent
from bg_agents.iagent import IAgent
import logging
import numpy as np

log = logging.getLogger(__name__) 

class Lab:

    def __init__(self, arena: Arena, replayer: GameReplayer, analyzer: GameReplayAnalyzer):
        self.arena = arena
        self.replayer = replayer
        self.analyzer = analyzer

    def match_up(self, agent1, agent2):
        log.info("Called method match_up().")
        return self.arena.compete(agent1, agent2) 

    def compare_agents(self, agent1: IAgent, agent2: IAgent, metrics: List[IMetric], n_matches=100):
        log.info("Called method compare agents.")

        traces = [self.arena.compete(agent1, agent2) for _ in range(n_matches)]

        log.info(f"Recorded {len(traces)} matches.")

        game_reports = np.empty(len(traces))
        for i, trace in enumerate(traces):
            log.debug(f"Running analysis {i}/{len(traces)}")
            replay = self.replayer.replay_game(trace)
            game_reports[i] = self.analyzer.analyze(replay)

        return aggregate_reports(game_reports)
