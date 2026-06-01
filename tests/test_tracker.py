"""测试追踪器功能."""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from timeflow.core.tracker import TimeTracker
from timeflow.core.session import SessionManager
from timeflow.core.project import ProjectManager


class TestTimeTracker:
    """测试 TimeTracker 类."""
    
    @pytest.fixture
    def tracker(self, tmp_path):
        """创建测试用的追踪器."""
        with patch('timeflow.core.config.Config') as MockConfig:
            config = MagicMock()
            config.get_data_dir.return_value = tmp_path
            config.get_sessions_file.return_value = tmp_path / "sessions.json"
            config.get_projects_file.return_value = tmp_path / "projects.json"
            MockConfig.return_value = config
            
            yield TimeTracker()
    
    def test_start_session(self, tracker):
        """测试开始会话."""
        session = tracker.start_session(
            project="TestProject",
            task="TestTask",
            tags=["tag1"],
        )
        
        assert session.project == "TestProject"
        assert session.task == "TestTask"
        assert session.tags == ["tag1"]
        assert session.is_active()
        assert tracker.is_tracking()
    
    def test_stop_session(self, tracker):
        """测试停止会话."""
        # 开始会话
        tracker.start_session(project="TestProject")
        assert tracker.is_tracking()
        
        # 停止会话
        session = tracker.stop_session(note="Test note")
        
        assert not tracker.is_tracking()
        assert session.note == "Test note"
        assert session.duration is not None
    
    def test_get_current_session(self, tracker):
        """测试获取当前会话."""
        # 没有活跃会话
        assert tracker.get_current_session() is None
        
        # 开始会话
        tracker.start_session(project="TestProject")
        
        # 获取当前会话
        session = tracker.get_current_session()
        assert session is not None
        assert session.project == "TestProject"
    
    def test_is_tracking(self, tracker):
        """测试追踪状态检查."""
        assert not tracker.is_tracking()
        
        tracker.start_session()
        assert tracker.is_tracking()
        
        tracker.stop_session()
        assert not tracker.is_tracking()
    
    def test_detect_project(self, tracker):
        """测试项目自动检测."""
        with patch('timeflow.core.project.ProjectManager.detect_project_from_files') as mock_files:
            with patch('timeflow.core.project.ProjectManager.detect_project_from_path') as mock_path:
                mock_files.return_value = None
                mock_path.return_value = "DetectedProject"
                
                project = tracker._detect_project()
                
                assert project == "DetectedProject"
    
    def test_switch_project(self, tracker):
        """测试切换项目."""
        # 开始第一个项目
        tracker.start_session(project="Project1")
        assert tracker.get_current_session().project == "Project1"
        
        # 切换到第二个项目
        tracker.switch_project("Project2")
        
        assert tracker.get_current_session().project == "Project2"
    
    def test_switch_task(self, tracker):
        """测试切换任务."""
        # 开始第一个任务
        tracker.start_session(project="Project1", task="Task1")
        
        # 切换到第二个任务
        tracker.switch_task("Task2")
        
        session = tracker.get_current_session()
        assert session.project == "Project1"  # 项目保持不变
        assert session.task == "Task2"  # 任务改变
    
    def test_get_daily_summary(self, tracker):
        """测试获取每日摘要."""
        # 创建一些会话
        tracker.start_session(project="Project1")
        tracker.stop_session()
        
        summary = tracker.get_daily_summary()
        
        assert "date" in summary
        assert "total_time" in summary
        assert "session_count" in summary
        assert "project_times" in summary
    
    def test_get_project_summary(self, tracker):
        """测试获取项目摘要."""
        # 创建项目会话
        tracker.start_session(project="TestProject", task="Task1")
        tracker.stop_session()
        
        summary = tracker.get_project_summary("TestProject")
        
        assert summary["project"] == "TestProject"
        assert summary["total_hours"] > 0
        assert summary["session_count"] == 1
