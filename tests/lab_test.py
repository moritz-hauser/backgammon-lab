from unittest.mock import Mock, MagicMock, patch, call
import pytest
from bg_lab.lab import Lab, DuplicateMetricIdError
from bg_lab.imetric import IMetric, MetricResult


def test_add_metric_stores_metric():
    lab = Lab()
    mock_metric = Mock(spec=IMetric)
    mock_metric.id = "test_metric"
    
    lab.add_metric(mock_metric)
    
    assert "test_metric" in lab.metrics
    assert lab.metrics["test_metric"] == mock_metric


def test_add_metric_duplicate_id_raises_error():
    lab = Lab()
    metric1 = Mock(spec=IMetric)
    metric1.id = "duplicate_id"
    metric2 = Mock(spec=IMetric)
    metric2.id = "duplicate_id"
    
    lab.add_metric(metric1)
    
    with pytest.raises(DuplicateMetricIdError) as exc_info:
        lab.add_metric(metric2)
    
    assert "duplicate_id" in str(exc_info.value)
    assert "already in use" in str(exc_info.value)


def test_add_metrics_each_gets_called():
    lab = Lab()
    
    # Create mock metrics
    mock_metric1 = Mock(spec=IMetric)
    mock_metric1.id = "metric_1"
    mock_metric1.analyze = Mock(return_value=MetricResult(metric_id="metric_1", value=42))
    
    mock_metric2 = Mock(spec=IMetric)
    mock_metric2.id = "metric_2"
    mock_metric2.analyze = Mock(return_value=MetricResult(metric_id="metric_2", value=3.14))
    
    mock_metric3 = Mock(spec=IMetric)
    mock_metric3.id = "metric_3"
    mock_metric3.analyze = Mock(return_value=MetricResult(metric_id="metric_3", value="test"))
    
    lab.add_metric(mock_metric1)
    lab.add_metric(mock_metric2)
    lab.add_metric(mock_metric3)
    
    # Mock agents and dependencies
    mock_white_agent = Mock()
    mock_black_agent = Mock()
    
    # Mock GameController, GameStateModel, MatchRecorder
    with patch('bg_lab.lab.GameStateModel') as mock_model_class, \
         patch('bg_lab.lab.GameController') as mock_gc_class, \
         patch('bg_lab.lab.MatchRecorder') as mock_recorder_class:
        
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        
        mock_gc = Mock()
        mock_gc_class.return_value = mock_gc
        
        mock_recorder = Mock()
        mock_recording = Mock()
        mock_recorder.get_recording.return_value = mock_recording
        mock_recorder_class.return_value = mock_recorder
        
        # Run with n_matches=2 to test multiple iterations
        n_matches = 2
        result = lab.compare_agents(mock_white_agent, mock_black_agent, n_matches=n_matches)
        
        # Verify each metric's analyze was called exactly n_matches times
        assert mock_metric1.analyze.call_count == n_matches
        assert mock_metric2.analyze.call_count == n_matches
        assert mock_metric3.analyze.call_count == n_matches
        
        # Verify analyze was called with the recording
        for call_args in mock_metric1.analyze.call_args_list:
            assert call_args[0][0] == mock_recording
        
        for call_args in mock_metric2.analyze.call_args_list:
            assert call_args[0][0] == mock_recording
            
        for call_args in mock_metric3.analyze.call_args_list:
            assert call_args[0][0] == mock_recording
        
        # Verify structure of returned data
        assert len(result) == n_matches
        for match_metrics in result:
            assert len(match_metrics) == 3
            assert all(isinstance(mr, MetricResult) for mr in match_metrics)


def test_compare_agents_returns_correct_structure():
    lab = Lab()
    
    mock_metric = Mock(spec=IMetric)
    mock_metric.id = "test_metric"
    mock_metric.analyze = Mock(return_value=MetricResult(metric_id="test_metric", value=100))
    
    lab.add_metric(mock_metric)
    
    mock_white_agent = Mock()
    mock_black_agent = Mock()
    
    with patch('bg_lab.lab.GameStateModel'), \
         patch('bg_lab.lab.GameController'), \
         patch('bg_lab.lab.MatchRecorder') as mock_recorder_class:
        
        mock_recorder = Mock()
        mock_recorder.get_recording.return_value = Mock()
        mock_recorder_class.return_value = mock_recorder
        
        result = lab.compare_agents(mock_white_agent, mock_black_agent, n_matches=3)
        
        assert len(result) == 3
        for match_metrics in result:
            assert len(match_metrics) == 1
            assert match_metrics[0].metric_id == "test_metric"
            assert match_metrics[0].value == 100


def test_compare_agents_creates_fresh_instances_each_match():
    lab = Lab()
    
    mock_white_agent = Mock()
    mock_black_agent = Mock()
    
    with patch('bg_lab.lab.GameStateModel') as mock_model_class, \
         patch('bg_lab.lab.GameController') as mock_gc_class, \
         patch('bg_lab.lab.MatchRecorder') as mock_recorder_class:
        
        mock_recorder = Mock()
        mock_recorder.get_recording.return_value = Mock()
        mock_recorder_class.return_value = mock_recorder
        
        n_matches = 5
        lab.compare_agents(mock_white_agent, mock_black_agent, n_matches=n_matches)
        
        # Verify fresh instances created for each match
        assert mock_model_class.call_count == n_matches
        assert mock_gc_class.call_count == n_matches
        assert mock_recorder_class.call_count == n_matches


def test_check_metric_ids_unique():
    metric1 = Mock(spec=IMetric)
    metric1.id = "id1"
    metric2 = Mock(spec=IMetric)
    metric2.id = "id2"
    metric3 = Mock(spec=IMetric)
    metric3.id = "id1"  # duplicate
    
    assert Lab._check_metric_ids_unique([metric1, metric2]) is True
    assert Lab._check_metric_ids_unique([metric1, metric2, metric3]) is False
    assert Lab._check_metric_ids_unique([]) is True