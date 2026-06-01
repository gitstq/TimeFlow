"""测试追踪器功能."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from timeflow.core.tracker import TimeTracker
from timeflow.core.session import SessionManager
from timeflow.core.project import ProjectManager


class TestTimeTracker:
    """测试 TimeTracker 类."""
    
    def test_detect_project(self):
        """测试项目自动检测."""
        with patch('timeflow.core.config.Config') as MockConfig:
            config = MagicMock()
            config.get_data_dir.return_value = MagicMock()
            config.get_sessions_file.return_value = MagicMock()
            config.get_projects_file.return_value = MagicMock()
            MockConfig.return_value = config
            
            tracker = TimeTracker()
            
            with patch.object(tracker.project_manager, 'detect_project_from_files') as mock_files:
                with patch.object(tracker.project_manager, 'detect_project_from_path') as mock_path:
                    mock_files.return_value = None
                    mock_path.return_value = "DetectedProject"
                    
                    project = tracker._detect_project()
                    
                    assert project == "DetectedProject"
