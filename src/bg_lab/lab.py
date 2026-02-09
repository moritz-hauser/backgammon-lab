from typing import TypeAlias
from bg_game.game_controller import GameController
from bg_agents.random_agent import RandomAgent
from bg_agents.iagent import IAgent
from bg_game.game_state_model import GameStateModel
import logging
from bg_lab.match_recorder import MatchRecorder, MatchRecording
from bg_lab.imetric import IMetric, MetricResult

MatchMetrics: TypeAlias = list[MetricResult]

log = logging.getLogger(__name__) 

class DuplicateMetricIdError(RuntimeError):
    pass

class Lab:

    # Allow caller to use his own model, in case of desired cli output
    def __init__(self):
        self.metrics: dict[str, IMetric] = {}  # id -> metric
        for metric in self._default_metrics():
            self.add_metric(metric)
    
    @classmethod
    def _default_metrics(cls) -> list[IMetric]:
        return [] # TODO: Add default metrics here
    
    @classmethod
    def _check_metric_ids_unique(cls, metrics: list[IMetric]) -> bool:
        ids = [metric.id for metric in metrics]
        return len(ids) == len(set(ids))

    
    def add_metric(self, metric: IMetric):
        if metric.id in self.metrics:
            raise DuplicateMetricIdError(
                f"Metric-ID '{metric.id}' is already in use. "
                f"Unavailable IDs: {', '.join(sorted(self.metrics.keys()))}"
            )
        self.metrics[metric.id] = metric
    
    def compare_agents(
            self, 
            white_agent: IAgent, 
            black_agent: IAgent, 
            n_matches: int=100
        ) -> list[MatchMetrics]:
        log.info("Called method compare agents.")

        all_matches_data: list[MatchMetrics] = []

        for i in range(n_matches):
            # Avoid hidden state dependencies 
            model = GameStateModel()
            gc = GameController(model)
            recorder = MatchRecorder(model)

            gc.compete(white_agent=white_agent, black_agent=black_agent)

            recording: MatchRecording = recorder.get_recording()

            # Analyze recording
            match_metrics: MatchMetrics = []
            for metric in self.metrics.values():
                metric_result: MetricResult = metric.analyze(recording)
                match_metrics.append(metric_result)

            all_matches_data.append(match_metrics)

        return all_matches_data




        