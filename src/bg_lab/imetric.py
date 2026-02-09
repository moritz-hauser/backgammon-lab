from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from bg_lab.match_recorder import MatchRecording

@dataclass(frozen=True)
class MetricResult:
    metric_id: str # connects result to metric
    value: Any

class IMetric(ABC):

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for this metric."""
        ...

    @abstractmethod
    def compute(self, recording: MatchRecording) -> Any:
        """Compute the metric value from a recording."""
        ...
    
    def analyze(self, recording: MatchRecording) -> MetricResult:
        """Wrapper that creates the MetricResult with correct ID."""
        value = self.compute(recording)
        return MetricResult(metric_id=self.id, value=value)