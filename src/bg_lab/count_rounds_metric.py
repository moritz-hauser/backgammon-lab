from bg_lab.imetric import IMetric, MatchRecording

class CountRoundsMetric(IMetric):
    @property
    def id(self) -> str:
        return "AmountOfRounds"
    
    def compute(self, recording: MatchRecording) -> int:
        return len(recording.rounds)