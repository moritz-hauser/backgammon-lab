from typing import TypeAlias
from bg_game.game_controller import GameController
from bg_agents.random_agent import RandomAgent
from bg_agents.iagent import IAgent
from bg_game.game_state_model import GameStateModel
import logging
from bg_lab.match_recorder import MatchRecorder, MatchRecording
from bg_lab.imetric import IMetric, MetricResult
from bg_lab.count_rounds_metric import CountRoundsMetric
import pandas as pd

MatchMetrics: TypeAlias = list[MetricResult]

log = logging.getLogger(__name__) 

class DuplicateMetricIdError(RuntimeError):
    pass

class Lab:

    def __init__(self, include_defaults: bool=True):
        self.metrics: dict[str, IMetric] = {}  # id -> metric
        if include_defaults:
            for metric in self._default_metrics():
                self.add_metric(metric)
    
    @classmethod
    def _default_metrics(cls) -> list[IMetric]:
        # TODO: Add default metrics here
        return [
            CountRoundsMetric(),
        ] 
    
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
        ) -> pd.DataFrame:
        log.info("Called method compare agents.")

        all_matches_data: list[MatchMetrics] = []

        for i in range(n_matches):
            log.debug(f"Conducting match {i} / {n_matches}.")
            
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

        # Convert to DataFrame
        return self._to_dataframe(all_matches_data)
    
    def _to_dataframe(self, all_matches_data: list[MatchMetrics]) -> pd.DataFrame:
        """Convert list of match metrics to DataFrame."""
        rows = []
        for match_idx, match_metrics in enumerate(all_matches_data):
            row = {result.metric_id: result.value for result in match_metrics}
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.index = [f"match_{i}" for i in range(len(df))]
        df.index.name = "match_id"
        
        return df
        